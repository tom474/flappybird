import pygame  # use pygame module
import random
import button
import HandDetector as hd
import threading 

class HandDetectorThread:
    def __init__(self):
        self.hand_detector = hd.HandDetector()
        self.hand_detector_thread = threading.Thread(target=self.hand_detector.start)
        self.hand_detector_thread.start()
    
''' Hand Controller '''
hand_detector = HandDetectorThread()    
   
''' RGB color selector '''
GREEN = (0, 200, 0)  
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


def level(speed, acceleration, tube_change):
    pygame.init()  # initialize pygame functions
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))  # set the width and height of the game screen
    pygame.display.set_caption("Flappy Bird")  # set the game caption
    clock = pygame.time.Clock()  # use clock function in pygame
    running = True  # while the game is running, the while loop is infinity

    tube_width = 50  # tube width
    tube_velocity = speed  # tube speed
    tube_change_oy = tube_change
    acceleration = acceleration
    tube_gap = 150

    # tubes changing condition
    is_change1 = False
    is_change2 = False
    is_change3 = False

    # start position of the tube
    tube1_x = width + 300
    tube2_x = width + 600
    tube3_x = width + 900

    # start tube
    tube_y = 0

    # random height of the tube
    tube1_height = random.randint(100, 400)
    tube2_height = random.randint(100, 400)
    tube3_height = random.randint(100, 400)

    tube1_pass = False  # at the beginning, the bird does not pass the tube
    tube2_pass = False
    tube3_pass = False

    bird_x = 50
    bird_y = 200
    bird_width = 35
    bird_height = 35
    bird_drop_velocity = 0
    gravity = 0.3

    # initialize score
    score = 0
    font = pygame.font.SysFont("san", 20)  # create font and size for text on screen

    pausing = False  # haven't lost the game

    # import images
    background_image = pygame.image.load("images/background.png")
    bird_image = pygame.image.load("images/bird.png")
    bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

    while running:  # game running process
        clock.tick(60)  # 1 sec run 60 frames
        screen.fill(GREEN)  # screen background color
        screen.blit(background_image, (0, 0))

        ''' Draw tubes '''
        tube1_rect = pygame.draw.rect(screen, BLUE, (tube1_x, tube_y, tube_width, tube1_height))
        tube2_rect = pygame.draw.rect(screen, BLUE, (tube2_x, tube_y, tube_width, tube2_height))
        tube3_rect = pygame.draw.rect(screen, BLUE, (tube3_x, tube_y, tube_width, tube3_height))

        ''' Draw inverse tubes '''
        tube1_rect_inv = pygame.draw.rect(screen, BLUE, (tube1_x, tube1_height + tube_gap, tube_width, height - tube1_height - tube_gap))
        tube2_rect_inv = pygame.draw.rect(screen, BLUE, (tube2_x, tube2_height + tube_gap, tube_width, height - tube2_height - tube_gap))
        tube3_rect_inv = pygame.draw.rect(screen, BLUE, (tube3_x, tube3_height + tube_gap, tube_width, height - tube3_height - tube_gap))

        ''' Move faster '''
        tube_velocity += acceleration

        ''' Move tubes on Ox '''
        tube1_x = tube1_x - tube_velocity
        tube2_x = tube2_x - tube_velocity
        tube3_x = tube3_x - tube_velocity

        ''' Change tube's height '''
        # tube 1
        if is_change1 is False:
            tube1_height = tube1_height - tube_change_oy
            if tube1_height <= 100:
                is_change1 = True
        if is_change1 is True:
            tube1_height = tube1_height + tube_change_oy
            if tube1_height >= 300:
                is_change1 = False

        # tube 2
        if is_change2 is False:
            tube2_height = tube2_height - tube_change_oy
            if tube2_height <= 100:
                is_change2 = True
        if is_change2 is True:
            tube2_height = tube2_height + tube_change_oy
            if tube2_height >= 300:
                is_change2 = False

        # tube 3
        if is_change3 is False:
            tube3_height = tube3_height - tube_change_oy
            if tube3_height <= 100:
                is_change3 = True
        if is_change3 is True:
            tube3_height = tube3_height + tube_change_oy
            if tube3_height >= 300:
                is_change3 = False

        ''' Draw sand '''
        sand_rect = pygame.draw.rect(screen, YELLOW, (0, height - 50, width, 50))

        ''' Create new tubes when old tubes disappear'''
        if tube1_x < -tube_width:
            tube1_x = width + 50
            tube1_height = random.randint(100, 400)
            tube1_pass = False  # reset the tube pass
        if tube2_x < -tube_width:
            tube2_x = width + 50
            tube2_height = random.randint(100, 400)
            tube2_pass = False  # reset the tube pass
        if tube3_x < -tube_width:
            tube3_x = width + 50
            tube3_height = random.randint(100, 400)
            tube3_pass = False  # reset the tube pass

        ''' Draw bird'''
        bird_rect = screen.blit(bird_image, (bird_x, bird_y))

        ''' Bird fall '''
        bird_y += bird_drop_velocity
        bird_drop_velocity += gravity

        ''' Update score '''
        score_txt = font.render("Score: " + str(score), True, BLACK)  # render text with color
        screen.blit(score_txt, (5, 5))  # write text on screen
        if tube1_x + tube_width <= bird_x and tube1_pass is False:  # 1 point for each time pass the tube
            score += 1
            tube1_pass = True
        if tube2_x + tube_width <= bird_x and tube2_pass is False:
            score += 1
            tube2_pass = True
        if tube3_x + tube_width <= bird_x and tube3_pass is False:
            score += 1
            tube3_pass = True

        ''' Check collision '''
        for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_rect_inv, tube2_rect_inv, tube3_rect_inv, sand_rect]:
            if bird_rect.colliderect(tube):
                pausing = True  # lost the game
                tube_velocity = 0  # tubes stop moving
                bird_drop_velocity = 0  # bird stops dropping
                game_over_txt = font.render("GAME OVER, YOUR SCORE: " + str(score), True, RED)
                screen.blit(game_over_txt, (300, 300))
                space_txt = font.render("PRESS SPACE TO JUMP", True, RED)
                screen.blit(space_txt, (300, 70))

        ''' Set event such as mouse-click, keyboard buttons, quit'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when you click on X button, it will exit the game
                running = False
            elif event.type == pygame.KEYDOWN:  # use keyboard
                if event.key == pygame.K_SPACE:  # space button
                    # reset
                    if pausing:  # if player lost the game, reset all
                        bird_y = 400
                        tube_velocity = 3
                        tube1_x = width + 300
                        tube2_x = width + 600
                        tube3_x = width + 900
                        score = 0
                        pausing = False  # start again
                if event.key == pygame.K_SPACE:  # space button
                    bird_drop_velocity = 0  # reset the bird's drop speed (no gravity)
                    bird_drop_velocity -= 5  # make the bird jump

        pygame.display.flip()  # apply the colors changes to the screen

    pygame.quit()  # finish using pygame


def set_mode():
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mode")

    easy_img = pygame.image.load('images/EASY.png').convert_alpha()
    medium_img = pygame.image.load('images/MEDIUM.png').convert_alpha()
    hard_img = pygame.image.load('images/HARD.png').convert_alpha()

    easy_button = button.Button(400, 150, easy_img, 1)
    medium_button = button.Button(400, 250, medium_img, 1)
    hard_button = button.Button(400, 350, hard_img, 1)

    running = True
    while running:
        screen.fill((52, 78, 91))
        if easy_button.draw(screen):
            start_game("easy")
        if medium_button.draw(screen):
            start_game("medium")
        if hard_button.draw(screen):
            start_game("hard")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()


def start_game(game_mode):
    if game_mode == "easy":
        level(1, 0.001, 0)  # easy
    if game_mode == "medium":
        level(2, 0.004, 0)  # medium
    if game_mode == "hard":
        level(3, 0.002, 0.6)  # hard


def main_menu():
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Main Menu")

    start_img = pygame.image.load("images/START.png").convert_alpha()
    quit_img = pygame.image.load("images/QUIT.png").convert_alpha()

    start_button = button.Button(80, 200, start_img, 1)
    quit_button = button.Button(80, 300, quit_img, 1)

    running = True
    while running:
        screen.fill((52, 78, 91))
        if start_button.draw(screen):
            set_mode()
            running = False
        if quit_button.draw(screen):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
    pygame.quit()
    hand_detector.hd.stop()
    
main_menu()
