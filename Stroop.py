import pygame
import sys
import random
import time
from pygame.locals import *


# a class to help the program to randomly spawn two cards
# each card will have its meaning of color and its ink color simulated by random integers
class Draw_card:
    
    upper_card_meaning = 0
    upper_card_color = 0
    lower_card_meaning = 0
    lower_card_color = 0
    
    # n represents the number of colors will be used in the test
    def __init__(self, n):
        while n < 4 or n > 7:
            try:
                raise ValueError()
            except ValueError:
                entered = int(input("please enter an integer between 4, 5, 6, and 7: "))
                if entered >= 4 and entered <= 7:
                    self.n = entered
                    break
        self.n = n
    
    # randomly draw card, the upper card will always print in the same ink color
    def draw_card_easy(self):
        self.upper_card_meaning = random.randint(0,self.n)
        self.upper_card_color = 0
        self.lower_card_meaning = random.randint(0,self.n)
        self.lower_card_color = random.randint(0,self.n)
        # extra code to make sure the matching/non-matching rate will be around 0.5
        target = 0.6 - (1/self.n) - ((self.n - 3) ** 2) * 0.001
        if random.random() >= target:
            self.lower_card_color = random.randint(0,self.n)
        else:
            self.lower_card_color = self.upper_card_meaning
    
    # randomly draw card
    def draw_card_normal(self):
        self.upper_card_meaning = random.randint(0,self.n)
        self.upper_card_color = random.randint(0,self.n)
        self.lower_card_meaning = random.randint(0,self.n)
        # extra code to make sure the matching/non-matching rate will be around 0.5
        target = 0.6 - (1/self.n) - ((self.n - 3) ** 2) * 0.001
        if random.random() >= target:
            self.lower_card_color = random.randint(0,self.n)
        else:
            self.lower_card_color = self.upper_card_meaning
    
    # matching the text of the upper card to the color of the lower card
    def matching(self, level):
        if level == 0:
            self.draw_card_easy()
        elif level == 1:
            self.draw_card_normal()
            
        if self.upper_card_meaning == self.lower_card_color:
            return (True, ((self.upper_card_meaning, self.upper_card_color), 
                           (self.lower_card_meaning, self.lower_card_color)))
        else:
            return (False, ((self.upper_card_meaning, self.upper_card_color), 
                           (self.lower_card_meaning, self.lower_card_color)))

        
        
# the main class for the game
class StroopGame:
    
    window_width = 640
    window_height = 480
    card_pair = Draw_card(4)
    T_or_F = []
    upper_cards = []
    lower_cards = []
    total_card_pair_seen = 0
    correct_responded = 0
    level = 1
    
    # load in color schemes
    colors = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink"]
    RGB_code = [(0, 0, 0), (220, 0, 0), (0, 220, 0), (0, 0, 220), 
                (255, 240, 0), (255, 120, 0), (120, 0, 240), (255, 120, 255)]
    
    # prepare color dictionaries
    color_RGB_dict = {k: v for (k, v) in zip(colors, RGB_code)}
    index_color_dict = {k: v for k, v in enumerate(colors)}
    
    def __init__(self, n):
        self._running = True
        # initialize total number of colors used in the game
        self.card_pair = Draw_card(n)
        # initialize the game mode: easy or normal
        self.level = int(input("Enter 0 for easy, or 1 for normal level of difficulty, (0/1)? "))               
        if self.level != 0 and self.level != 1:
            try:
                raise TypeError()
            except TypeError:
                print("Alright, let's save some time and let the program picks the level of difficulty ...")
                self.level = 0 if random.random()  >= 0.5 else 1
                if self.level == 1:
                    print("Level Easy picked.")
                elif self.level == 0:
                    print("Level Normal picked.")
        
        # initialize a deck of card with 100 pairs
        # card_pairs_res: [(Bool, ((int, int), (int, int)))]
        card_pairs_res= [self.card_pair.matching(self.level) for i in range(100)]
        
        # small helper function to convert the matching results into the game's format
        def convert(tp):
            return (self.index_color_dict[tp[0]], self.color_RGB_dict[self.colors[tp[1]]])
        
        # prepare all the 100 cards
        self.upper_cards = [convert(cp[1][0]) for cp in card_pairs_res]
        self.lower_cards = [convert(cp[1][1]) for cp in card_pairs_res]
        self.T_or_F = [cp[0] for cp in card_pairs_res]
        
    def on_init(self):
        # start pygame video system
        pygame.init()
        pygame.display.set_caption('Stroop Game')
        
     
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        # load screen
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        screen.fill((255, 255, 255))
        
        # set fonts
        font1 = pygame.font.SysFont("comicsansms.ttf", 72)
        font2 = pygame.font.Font(None, 30)

        # load in timer
        clock_surface = pygame.Surface((120, 60))
        clock_surface.fill((255,255,255))
        screen.blit(clock_surface, (520, 10))
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        timer = 20
        timer_s = str(timer) + "s"
        count_down = timer_s.rjust(2)
        
        # load in score board
        score_surface = pygame.Surface((120, 40))
        score_surface.fill((255, 255, 255))
        screen.blit(score_surface, (520, 70))
        score1 = str(self.correct_responded).rjust(2) + " /" + str(self.total_card_pair_seen).rjust(3)
        screen.blit(font2.render(score1, True, (150, 150, 150)), (550, 80))
        
        # display the first two words
        text_upper = font1.render(self.upper_cards[0][0], True, 
                                  self.upper_cards[0][1])
        screen.blit(text_upper, (320 - text_upper.get_width() // 2, 
                                 200 - text_upper.get_height() // 2))
        text_lower = font1.render(self.lower_cards[0][0], True, 
                                  self.lower_cards[0][1])
        screen.blit(text_lower, (320 - text_lower.get_width() // 2, 
                                 300 - text_lower.get_height() // 2))
        
        i = 0
        done = False
        while self._running and not done:
            for event in pygame.event.get():    
                # start the timer
                if event.type == pygame.USEREVENT:
                    timer  -= 1
                    timer_s = str(timer) + "s"
                    count_down = timer_s.rjust(2) if timer >= 0 else "..."
                    # when time runs out
                    if count_down == "...":
                        done = True
                        screen.fill((255, 255, 255))
                        pygame.display.update()
                        times_up = font2.render("Times up!", True, 
                                               self.RGB_code[random.randint(0,7)])
                        final_score = font2.render("You got " + str(self.correct_responded) + " out of " +
                        str(self.total_card_pair_seen) + " tasks right.", True, self.RGB_code[random.randint(0,7)])
                        screen.blit(times_up, 
                                    (320 - times_up.get_width() // 2, 
                                     200 - times_up.get_height() // 2))
                        screen.blit(final_score, 
                                    (320 - final_score.get_width() // 2, 
                                     300 - final_score.get_height() // 2))
                
                # event that will terminate the program
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._running = False
                    
                # main game logic loop
                if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if event.key == pygame.K_RIGHT and self.T_or_F[i] == True:
                        self.correct_responded += 1
                    elif event.key == pygame.K_LEFT and self.T_or_F[i] == False:
                        self.correct_responded += 1
                    
                    i += 1
                    screen.fill((255, 255, 255))
                    text_upper = font1.render(self.upper_cards[i][0], True, 
                                              self.upper_cards[i][1])
                    screen.blit(text_upper, 
                                (320 - text_upper.get_width() // 2, 
                                 200 - text_upper.get_height() // 2))
                    text_lower = font1.render(self.lower_cards[i][0], True, 
                                              self.lower_cards[i][1])
                    screen.blit(text_lower, 
                                (320 - text_lower.get_width() // 2, 
                                 300 - text_lower.get_height() // 2))
                    
                    # some rare cases when all the 100 cards are all get examined before times up
                    self.total_card_pair_seen = i
                    if self.total_card_pair_seen == 99:
                        done = True
                        screen.fill((255, 255, 255))
                        pygame.display.update()
                        max_reached = font2.render("Maximum number of tasks meet", True, 
                                                   self.RGB_code[random.randint(0,7)])
                        final_score = font2.render("You got " + str(self.correct_responded) + " out of " +
                        str(self.total_card_pair_seen) + " tasks right.", True, self.RGB_code[random.randint(0,7)])
                        screen.blit(max_reached, 
                                    (320 - max_reached.get_width() // 2, 
                                     200 - max_reached.get_height() // 2))
                        screen.blit(final_score, 
                                    (320 - final_score.get_width() // 2, 
                                     300 - final_score.get_height() // 2))

            # update the score board            
            screen.blit(score_surface, (520, 70))
            score_surface.fill((255, 255, 255))
            score1 = str(self.correct_responded).rjust(2) + " /" + str(self.total_card_pair_seen).rjust(3)
            screen.blit(font2.render(score1, True, (150, 150, 150)), (550, 80))
    
            # update the timer   
            screen.blit(clock_surface, (520, 10))
            clock_surface.fill((255, 255, 255))
            count_down_timer = font2.render(count_down, True, (150, 150, 150))
            screen.blit(count_down_timer, (570, 30))
            
            pygame.display.flip()
            clock.tick(60)
            pygame.display.update()
        
        # the done branch for game over
        done = True
        
        if done == True:
            while self._running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self._running = False
                    if event.type == pygame.KEYDOWN and \
                    (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                
                        screen.fill((255, 255, 255))
                        game_over = font1.render("Game Over", True, (0, 0, 0))
                        screen.blit(game_over, 
                                    (320 - game_over.get_width() // 2, 
                                     250 - game_over.get_height() // 2))
                        pygame.display.flip()
            
        # quiting the pygame video system
        if self._running == False:
            pygame.display.quit()
            pygame.quit()
            quit()

            
if __name__ == "__main__" :
    # information about the game
    about_the_game = "The Stroop's Game is a classic neuropsychological test\
 used to assess our brains' ability to inhibit cognitive interference when a\
 mismatch in stimuli and task occurs. \nTo learn more, google 'Stroop Effect'."
    game_rule = "How to: \
    \nif the ink color of the LOWER word MATCHES the color that the UPPER word\
 describes, press ->, the right arrorw key on your keyboard. Otherwise, press <-\
 to continue.\
    \nWhen ready, following the intruction to start your trial."
    
    # start main()
    print(about_the_game)
    print("***********************************************")
    print(game_rule)
    print("***********************************************")
    x = int(input("To begin, please key in an integer from 4 to 7, inclusive: "))
    game = StroopGame(x)
    game.on_execute()