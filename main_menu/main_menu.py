#heres where I'll drop the main menu stuff
#https://stackoverflow.com/questions/tagged/pygame| and on youtube 'Coding with Russ', great tutorials' |

import pygame
pygame.init()
import buttons
import webbrowser

#while i tried my darndest to get python to register the folder as a directory by creating __init__.py files, it refuses to see it. so i will default to the simplest option, pasting the buttons module into every folder that has code that wants to use it. i refuse to burn anymore time

screen_width = 1500
screen_height = 754

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('KASD Game Launcher')

main_menu_bg_img = pygame.image.load('main_menu_assets\main background.png')
#imports the background image (yes i drew it in Ms paint sue me)

start_img = pygame.image.load('main_menu_assets\start button.png').convert_alpha()
quit_img = pygame.image.load('main_menu_assets\Quit.png').convert_alpha()
vinfo_img = pygame.image.load('main_menu_assets/version info.png').convert_alpha()
#imports images to use as buttons on screen. the .convert_alpha() preserves the transparency of png images

repo = 'https://github.com/DonovanMcKenzie/Programming-For-Data-Analytics-Group-Assignment'
#link to repository for version info button
        
#below are button instances of the button
start_bttn = buttons.Button(588, 327, start_img)
quit_bttn = buttons.Button(621, 460, quit_img)
vinfo = buttons.Button(4, 702, vinfo_img)



runtime = 1
#gameloop runtime variable

while runtime == 1:
#gameloop
    
    #now we call the instances of buttons to the screen     
    if quit_bttn.draw(screen):
        runtime = 0
        
    if vinfo.draw(screen):
        webbrowser.open(repo)
        
    if start_bttn.draw(screen):
        import gameselect
        
    
    #below is the event handler
    for event in pygame.event.get():
        #this checks for the X being pressed to close the window
        if event.type == pygame.QUIT:
            runtime = 0

            
            
    screen.blit(main_menu_bg_img, (0, 0))
    
    pygame.display.update()
    #screen upkeep
    
pygame.quit()
#exit code execution