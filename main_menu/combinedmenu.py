#heres where I'll drop the main menu stuff
#https://stackoverflow.com/questions/tagged/pygame| and on youtube 'Coding with Russ', great tutorials' |

import pygame
import buttons
import webbrowser #necessary for the version info button
import subprocess #necessary to give functionality to the buttons switching from menu to game and vice versa
import os #same as above
import sys

pygame.init()

screen_width = 1500
screen_height = 754

#sets up screen as a callable variable, names the window vv
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('KASD Game Launcher')

main_menu_bg_img = pygame.image.load('main_menu_assets\main background.png')
#imports the background image (yes i drew it in Ms paint sue me)

#main buttons image import vv
start_img = pygame.image.load('main_menu_assets\start button.png').convert_alpha()
quit_img = pygame.image.load('main_menu_assets\Quit.png').convert_alpha()
vinfo_img = pygame.image.load('main_menu_assets/version info.png').convert_alpha()
#imports images to use as buttons on screen. the .convert_alpha() preserves the transparency of png images

#gameselect buttons vv
dogdash_img = pygame.image.load('main_menu_assets\dogdash selection bttn.png')
dominoes_img = pygame.image.load('main_menu_assets\dominoes selecbttn.png')
snekNladder_img = pygame.image.load('main_menu_assets\Snakes n ladders selecbttn.png')
ach_img = pygame.image.load('main_menu_assets/achievements.png')
back_img = pygame.image.load('main_menu_assets/back bttn.png')

repo = 'https://github.com/DonovanMcKenzie/Programming-For-Data-Analytics-Group-Assignment'
#link to repository for version info button
        
#below are button instances of buttons
#main vv
start_bttn = buttons.Button(588, 327, start_img)
quit_bttn = buttons.Button(621, 460, quit_img)
vinfo = buttons.Button(4, 702, vinfo_img)
#game select vv
dd_bttn = buttons.Button( 300, 270 , dogdash_img)
dominoes_bttn = buttons.Button( 730, 270, dominoes_img)
snek_bttn = buttons.Button( 730, 430, snekNladder_img)
ach_bttn = buttons.Button(36, 37, ach_img)
back_bttn = buttons.Button(638, 600, back_img)

#game paths
curr_dir = os.path.dirname(os.path.abspath(__file__))
dogdash_path = os.path.join(curr_dir, "dogdash.py")


runtime = 1
#gameloop runtime variable

#gamestate variables
menustate = "main"

while runtime == 1:
#gameloop
    
    screen.blit(main_menu_bg_img, (0, 0))
    
    
    if vinfo.draw(screen):#draws the vinfo button regardless
            webbrowser.open(repo)
    #below checks which menu we are to be in, determining which buttons to show.
    if menustate == "main": 
    #now we call the instances of buttons to the screen     
        if quit_bttn.draw(screen):
            runtime = 0
        if start_bttn.draw(screen):
            menustate = "gameselect"
    if menustate == "gameselect":#checks for the start button being pressed and changes the buttons
        if ach_bttn.draw(screen):
            print(f"High score")
        
        if dd_bttn.draw(screen):
            dogdash_path = os.path.join(curr_dir, "dogdash.py")
            subprocess.Popen(["python", dogdash_path])
            runtime = 0
    
        if snek_bttn.draw(screen):
            print(f"snek")
    
        if dominoes_bttn.draw(screen):
            print(f"domino")
        if back_bttn.draw(screen):
            menustate = "main"
    
    #below is the event handler
    for event in pygame.event.get():
        #this checks for the X being pressed to close the window
        if event.type == pygame.QUIT:
            runtime = 0

            
    
    pygame.display.update()
    #screen upkeep
    
pygame.quit()
#exit pygame execution
sys.exit()