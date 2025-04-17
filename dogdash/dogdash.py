import pygame
from pygame.locals import *

pygame.init()
#initializes pygames modules for actual game functions

clock = pygame.time.Clock()
fps = 60
#initalizes an ingame clock and frame rate to control how often the gameplay loop runs

screen_width = 1500
screen_height = 700
#defines screen measurements

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dog Dash')
#constructs the screen, names the window

#gamevariables below credits to AxulArt @ https://axulart.itch.io/dirt-grass-2d-platform-tileset-ver-2
tile_size = 50


def draw_grid():
    for line in range(0, 30):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Player():
    def __init__(self, x, y):
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
        self.image = self.images_moveright[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.yvelocity = 0 #calculates gravity/vertical acceleration, a negative value means up
        self.isjumping = 0
        self.facing = 0
        
    def update(self):
        dx = 0 #these measure changes in position b4 they are updated in player pos
        dy = 0
        walkrate = 14
        
        #logs keystrokes to act as controls
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.isjumping == 0:
            self.yvelocity = -12
            self.isjumping = 1
        if key[pygame.K_UP] == 0:
            self.isjumping = 0
            
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter +=1 #increments when pressing directional keys to progress animation
            self.facing = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter +=1
            self.facing = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.facing == 1:
                self.image = self.images_moveright[self.index]
            if self.facing == -1:
                self.image = self.images_moveleft[self.index]
            
        #doge animations
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
        #update player position 
        self.rect.x += dx
        self.rect.y += dy
        #draws the instance of the player to the screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)



class Baddies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dd_assets/meanboar.png')
        



world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



#here we implement the terrain as an instance of the world class
world = World(world_data)

#here we implement an instance of the player class
player_lab = Player(100, screen_height - 90)

runtime = 1
#run var to control game execution

lvlbg = pygame.image.load('dd_assets/mainlvlbg.png')
#loaded images above   


while runtime == 1:
#gameloop 
    
    clock.tick(fps)# sets a frame rate for the execution
    screen.blit(lvlbg, (0,0))
    #here we draw the bg image on screen
      
    world.draw()#draws the terrain on screen
    player_lab.update()#calls the update method from the player class to draw the lab
    #draw_grid()#draws out grid, used during lvl creation, and i dont wanna get rid of it
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = 0
#serves as the program exit via X'ing the tab
            
    pygame.display.update()
#updates our screen to keep the code looping
            
pygame.quit()
    