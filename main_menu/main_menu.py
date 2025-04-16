#heres where I'll drop the main menu stuff
#test changes

import pygame
pygame.init()

screen_width = 1500
screen_height = 820

screen = pygame.display.set_mode((screen_width, screen_height))

runtime = 1
#gameloop runtime variable

while runtime == 1:
#gameloop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
    #exit code definition
    
    pygame.display.update()
    #screen upkeep
    
pygame.quit()
#exit code execution