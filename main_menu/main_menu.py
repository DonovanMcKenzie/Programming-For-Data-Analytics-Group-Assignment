#heres where I'll drop the main menu stuff
#test changes

import pygame
pygame.init()

screen_width = 1500
screen_height = 754

screen = pygame.display.set_mode((screen_width, screen_height))

main_menu_bg_img = pygame.image.load('main_menu_assets\main background.png')
#imports the background image (yes i drew it in Ms paint sue me)

runtime = 1
#gameloop runtime variable

while runtime == 1:
#gameloop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
    #exit code definition
            
    screen.blit(main_menu_bg_img, (0, 0))
    
    pygame.display.update()
    #screen upkeep
    
pygame.quit()
#exit code execution