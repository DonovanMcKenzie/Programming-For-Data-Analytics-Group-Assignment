import pygame
import os
import subprocess
import sys
from pygame.locals import *
import pickle

pygame.init()
#initializes pygames modules for actual game functions

clock = pygame.time.Clock()
fps = 49
#initalizes an ingame clock and frame rate to control how often the gameplay loop runs

screen_width = 1500
screen_height = 700
#defines screen measurements

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dog Dash')
#constructs the screen, names the window

#gamevariables below credits to AxulArt @ https://axulart.itch.io/dirt-grass-2d-platform-tileset-ver-2
tile_size = 50
gameover = 0
menustate = True
gamestate = "playing"
level = 0


def draw_grid():
    for line in range(0, 30):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



#loaded images below
lvlbg = pygame.image.load('dd_assets/mainlvlbg.png')
restart_img = pygame.image.load('dd_assets/restartimg.png')
back_img = pygame.image.load('dd_assets/back bttn.png')
pause_bttn = pygame.image.load('dd_assets/pause.png')
unpause_bttn = pygame.image.load('dd_assets/unpause.png')
to_mainBttn = pygame.image.load('dd_assets/to main.png')
exitgame = pygame.image.load('dd_assets/gamequit.png')
level1img = pygame.image.load('dd_assets/level1_img.png')
level2img = pygame.image.load('dd_assets/level2_img.png')


class Player():
    def __init__(self, x, y):
        self.reset(x,y)
        
    def update(self, gameover ):
        dx = 0 #these measure changes in position b4 they are updated in player pos
        dy = 0
        walkrate = 35
        #keypress
        if gameover == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.isjumping == 0 and self.airtime == False:
                self.yvelocity = -14
                self.isjumping = 1
            if key[pygame.K_UP] == 0:
                self.isjumping = 0
                
            if key[pygame.K_LEFT]:
                self.facing = -1
                dx -= 4
                self.counter +=1 #increments when pressing directional keys to progress animation
                
            if key[pygame.K_RIGHT]:
                self.facing = 1
                dx += 4
                self.counter +=1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.facing == 1:
                    self.image = self.images_moveright[self.index]
                if self.facing == -1:
                    self.image = self.images_moveleft[self.index]
                
            #doge animations
            self.counter += 1
            if self.counter > walkrate:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_moveright):
                    self.index = 0 #keeps the value of self .index from exceeding # of images in list
                if self.facing == 1:
                    self.image = self.images_moveright[self.index]
                if self.facing == -1:
                    self.image = self.images_moveleft[self.index]
                
            #gravity calculations
            self.yvelocity += 1
            if self.yvelocity > 10:
                self.yvelocity = 10
            dy += self.yvelocity
            
            #check for collisions
            self.airtime = True
            for tile in world.tile_list:
                #x axis collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                
                #y axis collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if doge hits head when jumping
                    if self.yvelocity < 0:
                        dy = tile[1].bottom - self.rect.top #sets the allowable change in y value to the position right b4 collision with a block
                        self.yvelocity =0
                    #check if doge is headed to floor
                    elif self.yvelocity >= 0:
                        dy = tile[1].top - self.rect.bottom #sets the allowable change in y value to the position right b4 collision with a block
                        self.yvelocity =0
                        self.airtime = False
                        
            #check for hostile contact
            if pygame.sprite.spritecollide(self, meanboar_group, False):
                gameover = -1
        
            if pygame.sprite.spritecollide(self, spikesup_group, False):
                gameover = -1
                
            #update player position 
            self.rect.x += dx
            self.rect.y += dy
            
        elif gameover == -1:
            self.image = self.dead
            if self.rect.y > 0:
                self.rect.y -=5
        
        #draws the instance of the player to the screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        return gameover
    
    def reset(self, x, y):
        self.images_moveright = [] #empty list to store individual images in an animation cycle
        self.images_moveleft = []
        self.index = 0
        self.counter = 0
        # iterates through images to load them, appends the image to the empty list
        for num in range (1, 9):
            lab_move_r = pygame.image.load(f"dd_assets/Lab{num}.png")
            lab_move_r = pygame.transform.scale(lab_move_r, (40, 30))
            lab_move_l = pygame.transform.flip(lab_move_r, True, False)
            self.images_moveright.append(lab_move_r)
            self.images_moveleft.append(lab_move_l)
        self.dead = pygame.image.load(f"dd_assets/dead.png")
        self.dead = pygame.transform.scale(self.dead, (40, 30))
        self.image = self.images_moveright[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.yvelocity = 0 #calculates gravity/vertical acceleration, a negative value means up
        self.isjumping = 0
        self.facing = 0
        self.airtime = True

class World():
    def __init__(self, data):
        self.tile_list = []

#load images
        grasscube = pygame.image.load('dd_assets/grassblock.png')
        dirtcube = pygame.image.load('dd_assets/rawdirt.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirtcube, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grasscube, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    meanboar = Baddies1(col_count * tile_size, row_count * tile_size + 6)
                    meanboar_group.add(meanboar)
                if tile == 4:
                    #creating an instance of the spikes class
                    spikesup = Spikes(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    spikesup_group.add(spikesup)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Baddies1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dd_assets/meanboar.png')
        self.image = pygame.transform.scale(self.image, (25, 45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.movecount = 0
    
    def update(self):
        self.rect.x += self.direction
        self.movecount += 1
        if abs(self.movecount) > 150:
            self.direction *= -1
            self.movecount *= -1
            
class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('dd_assets/spikesup.png')
        self.image = pygame.transform.scale(spike_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
            
            
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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


world_datalvl1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world_datalvl2 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

]

#instances
restart = Button(650, 100, restart_img)
back = Button(720, 200, back_img)
pause = Button(1455, 6, pause_bttn)

unpause = Button(100, 100, unpause_bttn)
mainBttn = Button(200, 200, to_mainBttn)
exitgamebttn = Button(300, 300, exitgame)

level1_bttn = Button(100, 100, level1img)
level2_bttn = Button(200, 200, level2img)

player_lab = Player(100, screen_height - 90)
meanboar_group = pygame.sprite.Group()
spikesup_group = pygame.sprite.Group()


#game paths
curr_dir = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(curr_dir, "combinedmenu.py")

runtime = 1
#run var to control game execution


  


while runtime == 1:
#gameloop 
    
    clock.tick(fps)# sets a frame rate for the execution
    screen.blit(lvlbg, (0,0))
    #here we draw the bg image on screen
      
    
    
    if menustate == True:
        if level1_bttn.draw():
            level = 1
            menustate = False
        if level2_bttn.draw():
            level = 2
            menustate = False
        if exitgamebttn.draw():
                runtime = 0
    else:
        
        if level == 1:
            world = World(world_datalvl1)
        if level == 2:
            world = World(world_datalvl2)

        world.draw()#draws the terrain on screen
            
        
        
        if gameover == 0:
            meanboar_group.update()
        
        if pause.draw():
            gamestate = "paused"
            print(f"paused press")
       
       
       #gamestate checker
        if gamestate == "paused":
            if exitgamebttn.draw():
                runtime = 0
            
            if mainBttn.draw():
                subprocess.Popen(["python", menu_path])
                runtime = 0
            if unpause.draw():
                gamestate = "playing"
            
            
        else:
            #regular game loop
            player_lab.update(gameover)#calls the update method from the player class to draw the lab
            
            
            meanboar_group.draw(screen)
              
            spikesup_group.draw(screen)
            
            gameover = player_lab.update(gameover)
            
            #player has died
            if gameover == - 1:
                if restart.draw():
                    player_lab.reset(100, screen_height - 90)
                    gameover = 0
                
                if back.draw():
                    subprocess.Popen(["python", menu_path])
                    runtime = 0            
    
    draw_grid()
    
    #event handler including paused
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamestate = "paused"
                print(f"paused")
        if event.type == pygame.QUIT:
            runtime = 0
#serves as the program exit via X'ing the tab
            
    pygame.display.update()
#updates our screen to keep the code looping
            
pygame.quit()
sys.exit()
    