import pygame
pygame.init()
#here i import and initialize pygames

screen_width = 1500
screen_height = 820
#these are variables defined for screen width and height to be called later

screen = pygame.display.set_mode((screen_width, screen_height))
#creates the screen for the game to be displayed on with the screen width and height varibales used

runtime = 1
#runtime is a gameloop cont variable

player = pygame.Rect((300, 250, 50, 50))
#defines shape ^^

#gameloop below
while runtime == 1:
    
    screen.fill((0,0,0))
    #fills the screen with black b4 anything is drawn serving as a refresh for the screen
    
    
    
    pygame.draw.rect(screen, (255, 0, 0), player)
#creates shape on screen
    
    key = pygame.key.get_pressed()
    #allows the program to know which key was pressed
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)
#moves the player on screen accoridngly. the entire code above essentially serves as our controller
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
    #serves as the program exit via X'ing the tab
            
    pygame.display.update()#updates our screen to keep the code looping
            
pygame.quit()
#exits the game once the gameloop ends


