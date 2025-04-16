import pygame
import buttons
pygame.init()
#here i import and initialize pygames

screen_width = 1500
screen_height = 754

screen = pygame.display.set_mode((screen_width, screen_height))
#window creation
pygame.display.set_caption('Select your game')

runtime = 1
#runtime is a gameloop cont variable

selectionscrn_bg = pygame.image.load('main_menu_assets\game select bg.png')
#add background image

dogdash_img = pygame.image.load('main_menu_assets\dogdash selection bttn.png')
dominoes_img = pygame.image.load('main_menu_assets\dominoes selecbttn.png')
snekNladder_img = pygame.image.load('main_menu_assets\Snakes n ladders selecbttn.png')
vinfo_img2 = pygame.image.load('main_menu_assets/version info.png')
ach_img = pygame.image.load('main_menu_assets/achievements.png')
#added the images for the buttons


dd_bttn = buttons.Button( 300, 189, dogdash_img)
dominoes_bttn = ( 832, 191, dominoes_img)
snek_bttn = ( 832, 339, snekNladder_img)
vinfo_img2 = ( 4, 702, vinfo_img2)
ach_bttn = (36, 37, ach_img)
#added the buttons

#gameloop below
while runtime == 1:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
    #serves as the program exit via X'ing the tab
            
    screen.blit(selectionscrn_bg, (0 , 0))
    
    if v
    
    if dd_bttn.draw(screen):
        print(f"Doge")
    ##this is underneath the screen back ground cuz when it was above, the back ground rendered over it? i'll figure it out someday
    
    if snek_bttn.draw(screen):
    
    if dominoes_bttn.draw(screen):
        print(f"Doge")
        
    pygame.display.update()#updates our screen to keep the code looping
            
pygame.quit()
#exits the game once the gameloop ends


