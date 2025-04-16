import pygame
from pygame.locals import *

pygame.init()
#initializes pygames modules for actual game functions

screen_width = 1500
screen_height = 754
#defines screen measurements

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Animal Adventure')
#constructs the screen, names the window

runtime = 1
#run var to control game execution

while runtime == 1:
#gameloop
    
#loaded images above    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
#serves as the program exit via X'ing the tab
            
    pygame.display.update()
#updates our screen to keep the code looping
            
pygame.quit()
    