#heres where I'll drop the main menu stuff
#https://stackoverflow.com/questions/tagged/pygame| and on youtube 'Coding with Russ', great tutorials' |

import pygame
pygame.init()

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

#below we're gonna create the button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()#defines the rectangle on screen that our button occupies
        self.rect.topleft = (x, y)#sets the coords for the shape
        self.clicked = False
        
    
    def draw(self):
        action = False #used later to differentiate button clicks
        #below stores the position of the mouse in the game window
        pos = pygame.mouse.get_pos()
        
        #this checks if the mouse is over a button and registers clicks
        if self.rect.collidepoint(pos) == True:#if at any point theres a collision between the defined rectangle's coords and the mouse
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:#checks for left click, 1 is middle and 2 is right
                self.clicked = True
                action = True
                
        #resets the button after a click        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
                
        #this part actually draws the button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        
        
#below i'll create the actual instances of the button
start_bttn = Button(588, 327, start_img)
quit_bttn = Button(621, 460, quit_img)
vinfo = Button(4, 702, vinfo_img)
    
    

runtime = 1
#gameloop runtime variable

while runtime == 1:
#gameloop
    
    #now we call the instances of buttons to the screen
    if start_bttn.draw():
        print(f"head to game selection screen")
        
    if quit_bttn.draw():
        runtime = 0
        
    if vinfo.draw():
        print(f"paste code for github")
    
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