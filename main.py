import pygame
import random
import time

# Initializes pygame
pygame.init()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Make the screen
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Cube Racer")

def make_wall():
    ground_or_ceiling = random.randint(1, 2) # Picks if the wall will be on the ground or ceiling
    
    height = random.randint(100, 400) # Chooses it's length

    if ground_or_ceiling == 1:
        def wall_func(x): # Creates a function to be returned
            pygame.draw.rect(screen, BLACK, (x, 0, 50, height))
        return wall_func, 1100, 0
    else:
        def wall_func(x): # Creates a function to be returned
            pygame.draw.rect(screen, BLACK, (x, 650-height, 50, height))
        return wall_func, 1100, 600

# Just some variables for my program
walls = []
last_time = time.perf_counter()
game_over = False
running = True
jump = False
player_y = 600
while running:
    screen.fill(GREY)
    if not game_over: # Checks if the game is over
        pygame.draw.rect(screen, RED, (100, player_y, 50, 50))
        pygame.draw.rect(screen, BLACK, (0, 650, 1200, 150))

        if time.perf_counter()-last_time >= 1: # Basically spawns a new wall every... 1-3 seconds
            wall_func, x, y_range = make_wall()
            walls.append([wall_func, x, y_range])
            last_time = time.perf_counter()

        for i, wall in enumerate(walls): # Loops through all the walls and constantly moves them towards you
            wall[0](wall[1]-5)
            walls[i][1] = wall[1]-5

            if wall[1]-5 == 100 and wall[2] == 0 and player_y == 0:
                game_over = True
            elif wall[1]-5 == 100 and wall[2] == 600 and player_y == 600:
                game_over = True

            if wall[1]-5 == 0:
                walls.pop(i)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed()[0]: # Switches gravity when left key is pressed
                if jump:
                    player_y = 600
                    jump = False
                else:
                    player_y = 0
                    jump = True
    else: # The game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP: # Checks if space is hit and exits the game over screen
                if event.key == pygame.K_SPACE:
                    game_over = False
                    player_y = 600
                    jump = False
                    walls = []

        # Displays the text
        font = pygame.font.Font(pygame.font.get_default_font(), 100)
        text_surface = font.render('Game Over!', True, (0, 0, 0))
        screen.blit(text_surface, (325, 400))
    
    pygame.display.update() # Updates the screen
