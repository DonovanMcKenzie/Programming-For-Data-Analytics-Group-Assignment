#heres where I'll drop the main menu stuff
#https://stackoverflow.com/questions/tagged/pygame| for my questions and bug fixes

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
        
    #this part actually draws the button
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        
#below i'll create the actual instances of the button
start_bttn = Button(588, 327, start_img)
quit_bttn = Button(621, 460, quit_img)
vinfo = Button(4, 702, vinfo_img)
    
    

runtime = 1
#gameloop runtime variable

while runtime == 1:
#gameloop
    
    #now we call the instances of buttons to the screen
    start_bttn.draw()
    quit_bttn.draw()
    vinfo.draw()
    
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