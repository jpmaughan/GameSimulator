# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:27:11 2019

@author: MaughanJ1
"""

### Game Simulator - Currently for 3-a-side football ###
 
# need to slow down the game so it happens in real time
# import the pygame module
import pygame
import random
import math
from pygame.locals import *
import pygame
import pygame.gfxdraw
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# picture path
pic_path = 'C:/Users/maughanj1/Pictures/Saved Pictures/'


### GLOBAL VARIABLES ###
player_size = 30
ball_size = 15
goal_one_position = (0, 300)
goal_two_position = (800, 300)

# add a net 
# source for most of the code for this project - might want to remove 
# https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py


### GOALPOSTS ###

class GoalpostOne(pygame.sprite.Sprite):
      
    def __init__(self):
        super(GoalpostOne, self).__init__()
        self.surf = pygame.Surface((30, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=goal_one_position)
        self.speed = random.randint(5,6)
        
class GoalpostTwo(pygame.sprite.Sprite):
      
    def __init__(self):
        super(GoalpostTwo, self).__init__()
        self.surf = pygame.Surface((30, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=goal_two_position)
        self.speed = random.randint(5,6)        
 
# Just player one - need to repeat for other plates
        
### HUMAN CONTROL PLAYER ###    
    
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
        self.surf = pygame.Surface((player_size, player_size))
        self.surf.fill((223, 42, 42))
        self.rect = self.surf.get_rect(center=(150, 300))
        self.speed = 15
        self.power = 35
        self.accuracy = 0.85
        self.control_space = 10
        self.cont_surf = pygame.Surface((player_size+self.control_space,
                                         player_size+self.control_space
                                         ))
        self.decision = 'dribble'
        self.dx = 0
        self.dy = 0
        self.average_movement_x = [0,0,0,0]
        self.average_movement_y = [0,0,0,0]
        self.recent_dx = 0
        self.recent_dy = 0
        self.scored = 0
    
    def update(self, pressed_keys):
        # add movement
        # add a speed variab'e
        speed = self.speed
        self.decision = 'dribble'

        # add the recent movement 
        self.average_movement_x.append(self.dx)
        self.average_movement_y.append(self.dy)
        
        # reset the current movement to be nil - unless input otherwise
        self.dx = 0
        self.dy = 0
        
        # delete the previous movement
        del(self.average_movement_x[0])
        del(self.average_movement_y[0])
    
        # add action inputs
        if pressed_keys[K_UP]:
            self.dy = -1 * speed
            self.recent_dy = -1
            self.rect.move_ip(0, self.dy)
        if pressed_keys[K_DOWN]:
            self.dy = 1 * speed
            self.recent_dy = 1
            self.rect.move_ip(0, self.dy)
        if pressed_keys[K_LEFT]:
            self.dx = -1 * speed
            self.recent_dx = -1
            self.rect.move_ip(self.dx, 0)
        if pressed_keys[K_RIGHT]:
            self.dx = 1 * speed
            self.recent_dx = 1
            self.rect.move_ip(self.dx, 0)
        if pressed_keys[K_SPACE]:
            self.decision = 'kick'
        

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
 
    
    
### COMPUTER CONTROLLED PLAYER ###    
    
class PlayerTwo(pygame.sprite.Sprite):
    
# ==============================contains the code for my face==================
#     def __init__(self):
#         super(Player, self).__init__()
#         self.image = pygame.image.load(pic_path + 'MyFace.png').convert()
#         self.image.set_colorkey((255, 255, 255), RLEACCEL)
#         self.rect = self.image.get_rect()
# =============================================================================
    
    ## Introduce the knowledge of the ball location ## 
    ## EASY ?? Get the person to move towards the middle from a random location
        
    def __init__(self):
        super(PlayerTwo, self).__init__() 
        self.surf = pygame.Surface((player_size, player_size))
        self.surf.fill((42, 243, 42,128))
        #self.rect = self.surf.get_rect(center=(450, 300))
        self.rect = self.surf.get_rect(center=(random.randint(0,600), random.randint(0,600)))
        self.speed = 1
        self.power = 4
        self.accuracy = 0.85
        self.decision = 'kick'
        self.control_space = 10
        self.dx = 0
        self.dy = 0
        self.average_movement_x = [0,0,0,0,0]
        self.average_movement_y = [0,0,0,0,0]
        self.recent_dx = 0
        self.recent_dy = 0
        self.scored = 0
    
    ## need input for the ball position 
    
    def pred_move(self, ball):
        
        # get the ball position
        ball_x = ball.rect.x
        ball_y = ball.rect.y
        
        
    def update(self, ball):
        
        # get the player speed
        speed = self.speed
        
        # get the ball position
        ball_x = ball.rect.x
        ball_y = ball.rect.y
        
        # get the player 2 postion
        p_x = self.rect.x
        p_y = self.rect.y
        
        # difference between 
        dx = ball_x - p_x
        dy = ball_y - p_y
        
        # move the player towards the ball
        # need to change this to reward the player to move so much.
        # could replace with random action 
        if dx > 0:
            self.rect.x += 1 * speed
        else:
            self.rect.x += -1 * speed
        if dy > 0:
            self.rect.y += 1 * speed
        else:
            self.rect.y += -1 * speed

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600



ATOM_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
 
# add the ball
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Ball, self).__init__()
        #make the ball spherical
        #self.image = pygame.image.load(pic_path + 'LeoFace.png').convert()
        #self.rect = self.image.get_rect(center=(150, 200))
        self.surf = pygame.Surface((ball_size, ball_size))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(400, 300)
        )
        self.speed_x = 1
        self.speed_y = 1
        self.power = 1
        self.ball_vel = (0,0)
        self.dc = 0.85
    
    
    def reset_ball(self):
        self.rect = self.surf.get_rect(center=(400, 300))
        self.ball_vel = (0,0)

    def update(self):
        
        # coeffeient of collisons - dampening 
        dc = self.dc
        self.ball_vel = (self.ball_vel[0] * dc, self.ball_vel[1] * dc)

        # update the ball velocity once hit
        ball_x_vel = self.ball_vel[0] 
        ball_y_vel = self.ball_vel[1]
        
        # change the ball direction
        self.rect.x +=  ball_x_vel * 0.1  
        self.rect.y +=  ball_y_vel * 0.1  
        
        # keep the ball on the screen with bounces
        if self.rect.left < 0:
            self.rect.left = 0
            self.ball_vel = (-self.ball_vel[0], self.ball_vel[1])
        elif self.rect.right > 800:
            self.rect.right = 800
            self.ball_vel = (-self.ball_vel[0], self.ball_vel[1])
        if self.rect.top <= 0:
            self.rect.top = 0
            self.ball_vel = (self.ball_vel[0], -self.ball_vel[1])
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.ball_vel = (self.ball_vel[0], -self.ball_vel[1])
     
    # need to create a function which allows the player to make a decision
        
    def kick(self, player):
        # add the power of the kick
        power = player.power
        speed = player.speed
        player_position = player.rect.x, player.rect.y
        
        # new movement - tracks the previous n movements
        player_movement_x = sum(player.average_movement_x) / len(player.average_movement_x)
        player_movement_y = sum(player.average_movement_y) / len(player.average_movement_y)
        
        # also add the current speed of the player   
        # add interactions between Player and the ball 
        dx1 = self.rect.x - player_position[0]
        dy1 = self.rect.y - player_position[1]
        
        # change the new ball velocity - and standing kick
        # change this so the negative values are not impeded as much
        if (abs(player_movement_x) + abs(player_movement_y) == 0):
            ball_vel_x = 5 * power*player.recent_dx
            ball_vel_y = 5 * power*player.recent_dy
        else:
            ball_vel_x = (5*speed) + (player_movement_x*power)
            ball_vel_y = (5*speed) +(player_movement_y*power)
            
        # change the ball direction                 
        self.ball_vel = (ball_vel_x, ball_vel_y)
        
        
    def dribble(self, player):
        # add the power of the kick
        power = player.power
        speed = player.speed 
        player_position = player.rect.x, player.rect.y
        player_control = player_size * 15 #player.control_space
        
        # add interactions between Player and the ball 
        dx1 = self.rect.x - player_position[0]
        dy1 = self.rect.y - player_position[1]
        
        # keep the ball close
        if abs(dx1 < player_control):
            if dx1 >= 0:
                self.rect.x = player_position[0] + (ball_size/5)
            else:
                self.rect.x = player_position[0] - (ball_size/5)
        if abs(dy1 < player_control):
            if dy1 >= 0:
                self.rect.y = player_position[1] + (ball_size/5)
            else:
                self.rect.y = player_position[1] - (ball_size/5)

        
    
    def shoot(self, player):     
        # player stats
        power =  player.power
        accuracy = player.accuracy
        
        # aim towards goals - pick one to target
        player_position = player.rect.x, player.rect.y
        goal_position = goal_one_position
        
        # add interactions between Player and the ball 
        dx1 = goal_position[0] - player_position[0]
        dy1 = goal_position[1] - player_position[1]
        
        # change the ball direction
        self.rect.x += accuracy * dx1
        self.rect.y += accuracy * dy1
        pass
    
        
    def passball(self, player):
        pass
 

    def move(self, player):
        
        # get the player control space
        player_control = player.control_space
        player_space = player.rect.x, player.rect.y
        
        # define the ball space 
        ball_space = self.rect.x , self.rect.y
        
        # if ball 
        dx = self.rect.x - player.rect.x
        dy = self.rect.y - player.rect.y
        
        if (abs(dx) + abs(dy) < player_size + player_control):

            # add in the interactions with the plauer
            player_decision = player.decision
            
            # 
            if player_decision == 'kick':
                self.kick(player)
            elif player_decision == 'dribble':
                self.dribble(player)
            elif player_decision == 'shoot':
                self.shoot(player)
            elif player_decision == 'passball':
                self.passball(player)

            
 
        
 
# Change the game into a CLASS
            # collision : https://stackoverflow.com/questions/19823805/pygame-collision-interaction
    
 

# get it so it bounces off the wales - five a side-esc

class Game():
    
    def __init__(self):
        
        # initialise the clock
        self.FPS = 20
        self.fpsClock = pygame.time.Clock() 
        
        # initialize pygame
        pygame.init()
        
        # set the screen dimensions
        self.screen = pygame.display.set_mode((800, 600))
        
        # set up some basic background features of the game
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
         
        # create our sprites
        self.ball = Ball()
        self.player1 = Player()
        self.player2 = PlayerTwo()
        
        # create the goalpost
        self.goalpost1 = GoalpostOne()
        self.goalpost2 = GoalpostTwo()
        
        # intiitalise the scores
        self.score_team_1 = 0
        self.score_team_2 = 0
        
        
    def run(self):
        
        # basic setup for the running
        running = True
        
        # check the time
        t = 0
        t1 = 0
                
        # set the game to run
        while running:
        
            # Set yup the basic running of the game - quit when quit
            for event in pygame.event.get():
                
                # set up a few if statements to escape the game
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
            
            # add a frames per second
            self.fpsClock.tick(self.FPS)
            
            # get the background colour
            self.screen.blit(self.background, (0, 0))
            
            # add the control movements
            pressed_keys = pygame.key.get_pressed()
            
            # update the characters in play
            self.player1.update(pressed_keys)
            self.player2.update(self.ball)
            self.ball.update()
            
            # add interactions between the ball and each of the players
            self.ball.move(self.player1)
            self.ball.move(self.player2)
            
            # add the sprites to the screen
            self.screen.blit(self.ball.surf, self.ball.rect)
            self.screen.blit(self.player1.surf, self.player1.rect)
            self.screen.blit(self.player2.surf, self.player2.rect)
            self.screen.blit(self.goalpost1.surf, self.goalpost1.rect)
            self.screen.blit(self.goalpost2.surf, self.goalpost2.rect)
                
            # add interaction between player and the ball
            # can group together the players to functionise this part.
            # can just input this into the update part of the class i reckon #
            # just have every player as an input 

            #if pygame.sprite.collide_rect(self.player1, self.ball):
            #    #player_decision = 'kick'
            #    self.ball.move(self.player1)
                
            #if pygame.sprite.collide_rect(self.player2, self.ball):
            #    #player_decision = 'kick'
            #   self.ball.move(self.player2)
                
                
            ## SCORINIG ## 
            # this is basically the reward system of the game #
            # Need to reset once scored # 
            # Change the kick off taker too #
            # THis now breaks if there is a goal to loop through the randstate
            
            if pygame.sprite.collide_rect(self.goalpost1, self.ball):
                self.score_team_2 += 1
                self.player1.scored += 1
                print(self.score_team_1 , ' - ' , self.score_team_2)
                self.ball.reset_ball()
                break

            if pygame.sprite.collide_rect(self.goalpost2, self.ball):
                self.score_team_1 += 1
                self.player2.scored += 1
                print(self.score_team_1 , ' - ' , self.score_team_2)
                self.ball.reset_ball()
                break


            # Show the scores
            myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
            label1 = myfont1.render("Team A - "+str(self.score_team_1)+ ' : ' +
                                    str(self.score_team_2)+ ' - Team B', 1, 
                                    (255,255,0))
            self.screen.blit(label1, (300,20))
        

            # The Passage of time # might not need
            t+= 1
            if (t%1000) == 1:
                t1 += 1
                #print(t1)
                
            #enemies.update()
            pygame.display.flip()
        # -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:27:11 2019

@author: MaughanJ1
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:48:29 2019

@author: MaughanJ1
"""

### Game Simulator - Currently for 3-a-side football ###
 
# need to slow down the game so it happens in real time
# import the pygame module
import pygame
import random
import math
from pygame.locals import *
import pygame
import pygame.gfxdraw
from random import randint
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# picture path
pic_path = 'C:/Users/maughanj1/Pictures/Saved Pictures/'


### GLOBAL VARIABLES ###
player_size = 30
ball_size = 15
goal_one_position = (0, 300)
goal_two_position = (800, 300)

# add a net 
# source for most of the code for this project - might want to remove 
# https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py


### GOALPOSTS ###

class GoalpostOne(pygame.sprite.Sprite):
      
    def __init__(self):
        super(GoalpostOne, self).__init__()
        self.surf = pygame.Surface((30, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=goal_one_position)
        self.speed = random.randint(5,6)
        
class GoalpostTwo(pygame.sprite.Sprite):
      
    def __init__(self):
        super(GoalpostTwo, self).__init__()
        self.surf = pygame.Surface((30, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=goal_two_position)
        self.speed = random.randint(5,6)        
 
# Just player one - need to repeat for other plates
        
### HUMAN CONTROL PLAYER ###    
    
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
        self.surf = pygame.Surface((player_size, player_size))
        self.surf.fill((223, 42, 42))
        self.rect = self.surf.get_rect(center=(150, 300))
        self.speed = 15
        self.power = 35
        self.accuracy = 0.85
        self.control_space = 10
        self.cont_surf = pygame.Surface((player_size+self.control_space,
                                         player_size+self.control_space
                                         ))
        self.decision = 'dribble'
        self.dx = 0
        self.dy = 0
        self.average_movement_x = [0,0,0,0]
        self.average_movement_y = [0,0,0,0]
        self.recent_dx = 0
        self.recent_dy = 0
        self.scored = 0
    
    def update(self, pressed_keys):
        # add movement
        # add a speed variab'e
        speed = self.speed
        self.decision = 'dribble'

        # add the recent movement 
        self.average_movement_x.append(self.dx)
        self.average_movement_y.append(self.dy)
        
        # reset the current movement to be nil - unless input otherwise
        self.dx = 0
        self.dy = 0
        
        # delete the previous movement
        del(self.average_movement_x[0])
        del(self.average_movement_y[0])
    
        # add action inputs
        if pressed_keys[K_UP]:
            self.dy = -1 * speed
            self.recent_dy = -1
            self.rect.move_ip(0, self.dy)
        if pressed_keys[K_DOWN]:
            self.dy = 1 * speed
            self.recent_dy = 1
            self.rect.move_ip(0, self.dy)
        if pressed_keys[K_LEFT]:
            self.dx = -1 * speed
            self.recent_dx = -1
            self.rect.move_ip(self.dx, 0)
        if pressed_keys[K_RIGHT]:
            self.dx = 1 * speed
            self.recent_dx = 1
            self.rect.move_ip(self.dx, 0)
        if pressed_keys[K_SPACE]:
            self.decision = 'kick'
        

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
 
    
    
### COMPUTER CONTROLLED PLAYER ###    
    
class PlayerTwo(pygame.sprite.Sprite):
    
# ==============================contains the code for my face==================
#     def __init__(self):
#         super(Player, self).__init__()
#         self.image = pygame.image.load(pic_path + 'MyFace.png').convert()
#         self.image.set_colorkey((255, 255, 255), RLEACCEL)
#         self.rect = self.image.get_rect()
# =============================================================================
    
    ## Introduce the knowledge of the ball location ## 
    ## EASY ?? Get the person to move towards the middle from a random location
        
    def __init__(self):
        super(PlayerTwo, self).__init__() 
        self.surf = pygame.Surface((player_size, player_size))
        self.surf.fill((42, 243, 42,128))
        #self.rect = self.surf.get_rect(center=(450, 300))
        self.rect = self.surf.get_rect(center=(random.randint(0,600), random.randint(0,600)))
        self.speed = 1
        self.power = 4
        self.accuracy = 0.85
        self.decision = 'kick'
        self.control_space = 10
        self.dx = 0
        self.dy = 0
        self.average_movement_x = [0,0,0,0,0]
        self.average_movement_y = [0,0,0,0,0]
        self.recent_dx = 0
        self.recent_dy = 0
        self.scored = 0
    
    ## need input for the ball position 
    
    def pred_move(self, ball):
        
        # get the ball position
        ball_x = ball.rect.x
        ball_y = ball.rect.y
        
        
    def update(self, ball):
        
        # get the player speed
        speed = self.speed
        
        # get the ball position
        ball_x = ball.rect.x
        ball_y = ball.rect.y
        
        # get the player 2 postion
        p_x = self.rect.x
        p_y = self.rect.y
        
        # difference between 
        dx = ball_x - p_x
        dy = ball_y - p_y
        
        # move the player towards the ball
        # need to change this to reward the player to move so much.
        # could replace with random action 
        if dx > 0:
            self.rect.x += 1 * speed
        else:
            self.rect.x += -1 * speed
        if dy > 0:
            self.rect.y += 1 * speed
        else:
            self.rect.y += -1 * speed

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600



ATOM_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
 
# add the ball
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Ball, self).__init__()
        #make the ball spherical
        #self.image = pygame.image.load(pic_path + 'LeoFace.png').convert()
        #self.rect = self.image.get_rect(center=(150, 200))
        self.surf = pygame.Surface((ball_size, ball_size))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(400, 300)
        )
        self.speed_x = 1
        self.speed_y = 1
        self.power = 1
        self.ball_vel = (0,0)
        self.dc = 0.85
    
    
    def reset_ball(self):
        self.rect = self.surf.get_rect(center=(400, 300))
        self.ball_vel = (0,0)

    def update(self):
        
        # coeffeient of collisons - dampening 
        dc = self.dc
        self.ball_vel = (self.ball_vel[0] * dc, self.ball_vel[1] * dc)

        # update the ball velocity once hit
        ball_x_vel = self.ball_vel[0] 
        ball_y_vel = self.ball_vel[1]
        
        # change the ball direction
        self.rect.x +=  ball_x_vel * 0.1  
        self.rect.y +=  ball_y_vel * 0.1  
        
        # keep the ball on the screen with bounces
        if self.rect.left < 0:
            self.rect.left = 0
            self.ball_vel = (-self.ball_vel[0], self.ball_vel[1])
        elif self.rect.right > 800:
            self.rect.right = 800
            self.ball_vel = (-self.ball_vel[0], self.ball_vel[1])
        if self.rect.top <= 0:
            self.rect.top = 0
            self.ball_vel = (self.ball_vel[0], -self.ball_vel[1])
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.ball_vel = (self.ball_vel[0], -self.ball_vel[1])
     
    # need to create a function which allows the player to make a decision
        
    def kick(self, player):
        # add the power of the kick
        power = player.power
        speed = player.speed
        player_position = player.rect.x, player.rect.y
        
        # new movement - tracks the previous n movements
        player_movement_x = sum(player.average_movement_x) / len(player.average_movement_x)
        player_movement_y = sum(player.average_movement_y) / len(player.average_movement_y)
        
        # also add the current speed of the player   
        # add interactions between Player and the ball 
        dx1 = self.rect.x - player_position[0]
        dy1 = self.rect.y - player_position[1]
        
        # change the new ball velocity - and standing kick
        # change this so the negative values are not impeded as much
        if (abs(player_movement_x) + abs(player_movement_y) == 0):
            ball_vel_x = 5 * power*player.recent_dx
            ball_vel_y = 5 * power*player.recent_dy
        else:
            ball_vel_x = (5*speed) + (player_movement_x*power)
            ball_vel_y = (5*speed) +(player_movement_y*power)
            
        # change the ball direction                 
        self.ball_vel = (ball_vel_x, ball_vel_y)
        
        
    def dribble(self, player):
        # add the power of the kick
        power = player.power
        speed = player.speed 
        player_position = player.rect.x, player.rect.y
        player_control = player_size * 15 #player.control_space
        
        # add interactions between Player and the ball 
        dx1 = self.rect.x - player_position[0]
        dy1 = self.rect.y - player_position[1]
        
        # keep the ball close
        if abs(dx1 < player_control):
            if dx1 >= 0:
                self.rect.x = player_position[0] + (ball_size/5)
            else:
                self.rect.x = player_position[0] - (ball_size/5)
        if abs(dy1 < player_control):
            if dy1 >= 0:
                self.rect.y = player_position[1] + (ball_size/5)
            else:
                self.rect.y = player_position[1] - (ball_size/5)

        
    
    def shoot(self, player):     
        # player stats
        power =  player.power
        accuracy = player.accuracy
        
        # aim towards goals - pick one to target
        player_position = player.rect.x, player.rect.y
        goal_position = goal_one_position
        
        # add interactions between Player and the ball 
        dx1 = goal_position[0] - player_position[0]
        dy1 = goal_position[1] - player_position[1]
        
        # change the ball direction
        self.rect.x += accuracy * dx1
        self.rect.y += accuracy * dy1
        pass
    
        
    def passball(self, player):
        pass
 

    def move(self, player):
        
        # get the player control space
        player_control = player.control_space
        player_space = player.rect.x, player.rect.y
        
        # define the ball space 
        ball_space = self.rect.x , self.rect.y
        
        # if ball 
        dx = self.rect.x - player.rect.x
        dy = self.rect.y - player.rect.y
        
        if (abs(dx) + abs(dy) < player_size + player_control):

            # add in the interactions with the plauer
            player_decision = player.decision
            
            # 
            if player_decision == 'kick':
                self.kick(player)
            elif player_decision == 'dribble':
                self.dribble(player)
            elif player_decision == 'shoot':
                self.shoot(player)
            elif player_decision == 'passball':
                self.passball(player)

            
 
        
 
# Change the game into a CLASS
            # collision : https://stackoverflow.com/questions/19823805/pygame-collision-interaction
    
 

# get it so it bounces off the wales - five a side-esc

class Game():
    
    def __init__(self):
        
        # initialise the clock
        self.FPS = 20
        self.fpsClock = pygame.time.Clock() 
        
        # initialize pygame
        pygame.init()
        
        # set the screen dimensions
        self.screen = pygame.display.set_mode((800, 600))
        
        # set up some basic background features of the game
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
         
        # create our sprites
        self.ball = Ball()
        self.player1 = Player()
        self.player2 = PlayerTwo()
        
        # create the goalpost
        self.goalpost1 = GoalpostOne()
        self.goalpost2 = GoalpostTwo()
        
        # intiitalise the scores
        self.score_team_1 = 0
        self.score_team_2 = 0
        
        
    def run(self):
        
        # basic setup for the running
        running = True
        
        # check the time
        t = 0
        t1 = 0
                
        # set the game to run
        while running:
        
            # Set yup the basic running of the game - quit when quit
            for event in pygame.event.get():
                
                # set up a few if statements to escape the game
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
            
            # add a frames per second
            self.fpsClock.tick(self.FPS)
            
            # get the background colour
            self.screen.blit(self.background, (0, 0))
            
            # add the control movements
            pressed_keys = pygame.key.get_pressed()
            
            # update the characters in play
            self.player1.update(pressed_keys)
            self.player2.update(self.ball)
            self.ball.update()
            
            # add interactions between the ball and each of the players
            self.ball.move(self.player1)
            self.ball.move(self.player2)
            
            # add the sprites to the screen
            self.screen.blit(self.ball.surf, self.ball.rect)
            self.screen.blit(self.player1.surf, self.player1.rect)
            self.screen.blit(self.player2.surf, self.player2.rect)
            self.screen.blit(self.goalpost1.surf, self.goalpost1.rect)
            self.screen.blit(self.goalpost2.surf, self.goalpost2.rect)
                
            # add interaction between player and the ball
            # can group together the players to functionise this part.
            # can just input this into the update part of the class i reckon #
            # just have every player as an input 

            #if pygame.sprite.collide_rect(self.player1, self.ball):
            #    #player_decision = 'kick'
            #    self.ball.move(self.player1)
                
            #if pygame.sprite.collide_rect(self.player2, self.ball):
            #    #player_decision = 'kick'
            #   self.ball.move(self.player2)
                
                
            ## SCORINIG ## 
            # this is basically the reward system of the game #
            # Need to reset once scored # 
            # Change the kick off taker too #
            # THis now breaks if there is a goal to loop through the randstate
            
            if pygame.sprite.collide_rect(self.goalpost1, self.ball):
                self.score_team_2 += 1
                self.player1.scored += 1
                print(self.score_team_1 , ' - ' , self.score_team_2)
                self.ball.reset_ball()
                break

            if pygame.sprite.collide_rect(self.goalpost2, self.ball):
                self.score_team_1 += 1
                self.player2.scored += 1
                print(self.score_team_1 , ' - ' , self.score_team_2)
                self.ball.reset_ball()
                break


            # Show the scores
            myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
            label1 = myfont1.render("Team A - "+str(self.score_team_1)+ ' : ' +
                                    str(self.score_team_2)+ ' - Team B', 1, 
                                    (255,255,0))
            self.screen.blit(label1, (300,20))
        

            # The Passage of time # might not need
            t+= 1
            if (t%1000) == 1:
                t1 += 1
                #print(t1)
                
            #enemies.update()
            pygame.display.flip()
        
    
#### RUN THE GAME ####
            
from multiprocessing import Process
import random
from MAMEToolkit.sf_environment import Environment
game_counter = 0




while game_counter < 10:
    
    # count the number of games ran
    game_counter += 1
    print(game_counter)
    
    # set the game
    Game().run()


##### NOTES FOR THE DEEP REINFORCEMENT LEARNING ##### 
# =============================================================================
# 
# The only things the output can have is move up, down, left, right etc
# eventually we will be able to put in the decision to kick - dribble 
#
# Inputs can be the position of players and the ball
# 
# 
# 
# 
# 
# =============================================================================


    


