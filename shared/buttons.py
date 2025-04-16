import pygame
pygame.init()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()#defines the rectangle on screen that our button occupies
        self.rect.topleft = (x, y)#sets the coords for the shape
        self.clicked = False
        
    
    def draw(self, surface):
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
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

