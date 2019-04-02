# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:48:29 2019

@author: MaughanJ1
"""

### Game Simulator - Currently for 3-a-side football ###
 
# import the pygame module
import pygame
import random
import math
from pygame.locals import *

# picture path
pic_path = 'C:/Users/maughanj1/Pictures/Saved Pictures/'

# source for most of the code for this project - might want to remove 
# https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py

class Player(pygame.sprite.Sprite):
    
# ==============================contains the code for my face==================
#     def __init__(self):
#         super(Player, self).__init__()
#         self.image = pygame.image.load(pic_path + 'MyFace.png').convert()
#         self.image.set_colorkey((255, 255, 255), RLEACCEL)
#         self.rect = self.image.get_rect()
# =============================================================================
        
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((223, 42, 42))
        self.rect = self.surf.get_rect()
        self.speed = random.randint(5,6)
    
    # need to change so the computer moves 
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

    def kick(self, target):
        power = 1
        

 
# add the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        #self.image = pygame.image.load(pic_path + 'MyFace.png').convert()
        #self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(400, 300)
        )
        self.speed = random.randint(1, 3)
        self.vector = 1
        
    def update(self):
        
        # if the player comes into contact with the player move.
        #if pygame.sprite.spritecollideany(player, enemies):
        if pygame.sprite.spritecollideany(player, balls):
            newpos = self.calcnewpos(self.rect,self.vector)
            self.rect.move_ip(newpos)
            
        # keep the ball on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
        
    def calcnewpos(self, rect, vector):
        (angle,z) = (45, 1)
        (dx,dy) = (z*math.cos(angle), z*math.sin(angle))
        print(dx, dy)
        return dx, dy

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > self.screen.get_size()[0]:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > self.screen.get_size()[1]:
            self.speed_y = -self.speed_y
        
 
# Change the game into a CLASS
            # collision : https://stackoverflow.com/questions/19823805/pygame-collision-interaction
    
# initialize pygame
pygame.init()

### SET THE SCREEN ### 
screen = pygame.display.set_mode((800, 600))

# set up some basic background features of the game
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
 

### SET OUR SPRITES ###

# create our 'player'; right now he's just a rectangle
player = Player()

# create our ball
ball = Ball()

# add some 'enemies' wont be need for now
balls = pygame.sprite.Group()

# add all sprites together into a group
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

# basic setup fo the running
running = True

while running:

    # Set yup the basic running of the game - quit when quit
    for event in pygame.event.get():
        
        # set up a few if statements to escape the game
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
 
            
    # get the background colour
    screen.blit(background, (0, 0))
    
    # add the control movements
    pressed_keys = pygame.key.get_pressed()
    
    # update the eys pressed
    player.update(pressed_keys)
    
    # update the enemies movement - can add the ball here
    ball.update()
    
    # loop through the entitities list - need 3 players per team
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    # add the ball to the screen
    screen.blit(ball.surf, ball.rect)
        
    # KILL THE PLAYER
    #if pygame.sprite.spritecollideany(player, balls):
    #    ball.update()
    
    if pygame.sprite.collide_rect(player, balls):
         self.ball.speed_x = -self.ball.speed_x

    #enemies.update()
    pygame.display.flip()
    
    

## Next thing to do is to add contact when hit with the player so the ball