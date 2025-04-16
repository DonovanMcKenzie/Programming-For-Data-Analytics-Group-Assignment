import pygame
from pygame.locals import *

pygame.init()
#initializes pygames modules for actual game functions

screen_width = 1500
screen_height = 720
#defines screen measurements

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Animal Adventure')
#constructs the screen, names the window

#gamevariables below credits to AxulArt @ https://axulart.itch.io/dirt-grass-2d-platform-tileset-ver-2
grasscube = pygame.image.load('dd_assets/grassblock.png')
dirtcube = pygame.image.load('dd_assets/rawdirt.png')


runtime = 1
#run var to control game execution

lvlbg = pygame.image.load('dd_assets/mainlvlbg.png')
#loaded images above   


while runtime == 1:
#gameloop 
    
    screen.blit(lvlbg, (0,0))
    #here we draw the bg image on screen
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
#serves as the program exit via X'ing the tab
            
    pygame.display.update()
#updates our screen to keep the code looping
            
pygame.quit()
    