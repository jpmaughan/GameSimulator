# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:51:27 2019

@author: MaughanJ1
"""

import sys

import pygame
from pygame.locals import *
pic_path = 'C:/Users/maughanj1/Pictures/Saved Pictures/'

#----------------------------------------------------------------------

UP   = 1
DOWN = 2 

#----------------------------------------------------------------------

class Player():

    def __init__(self, screen, x, y):

        self.screen = screen

        self.rect = pygame.Rect(0,0,0,0)

        self.image = pygame.image.load(pic_path + 'MyFace.jpg')

        self.rect.size = self.image.get_size()

        self.rect.center = (x, y)

        self.speed_x = 0
        self.speed_y = 15

        self.direction = None

    def draw(self):
        self.screen.blit(self.image,(self.rect.x,self.rect.y))

    def move(self):
        if self.direction:
            if self.direction == UP :
                self.rect.y -= self.speed_y
                if self.rect.y < 0 :
                    self.rect.y = 0
            elif self.direction == DOWN :
                self.rect.y += self.speed_y
                if self.rect.y > self.screen.get_size()[1] - self.rect.height :
                    self.rect.y = self.screen.get_size()[1] - self.rect.height

#----------------------------------------------------------------------

class Ball():

    def __init__(self, screen, x, y):

        self.screen = screen

        self.rect = pygame.Rect(0,0,0,0)

        self.image = pygame.image.load(pic_path + 'MyFace.jpg')

        self.rect.size = self.image.get_size()

        self.rect.center = (x, y)

        self.speed_x = 15
        self.speed_y = 15

    def draw(self):
        self.screen.blit(self.image,(self.rect.x,self.rect.y))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > self.screen.get_size()[0]:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > self.screen.get_size()[1]:
            self.speed_y = -self.speed_y

#----------------------------------------------------------------------

class Game():

    def __init__(self):

        self.FPS = 25

        pygame.init()


        self.fpsClock = pygame.time.Clock()

        self.background = pygame.image.load(pic_path + 'MyFace.jpg')
        self.size = self.width, self.height = self.background.get_size()

        self.screen = pygame.display.set_mode(self.size,0,32)

        self.ball = Ball(self.screen, 100, 100)

        self.player1 = Player(self.screen, 35, self.height/2)
        self.player2 = Player(self.screen, self.width-35, self.height/2)

 

        font = pygame.font.SysFont("", 72)

        self.text_paused = font.render("PAUSE", True, (255, 0, 0))

 
        screen_rect = self.screen.get_rect()
        self.text_rect = self.text_paused.get_rect()
        self.text_rect.center = screen_rect.center

 
    def run(self):

        RUNNING = True

        PAUSED = False
        while RUNNING:

            # --- events ---

            for event in pygame.event.get():
                if event.type==QUIT:
                    RUNNING = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        RUNNING = False
                    elif event.key == K_SPACE:
                        PAUSED = not PAUSED
                    elif not PAUSED:
                        if event.key == K_w:
                            self.player1.direction = UP
                        elif event.key == K_s:
                            self.player1.direction = DOWN
                        elif event.key == K_UP:
                            self.player2.direction = UP
                        elif event.key == K_DOWN:
                            self.player2.direction = DOWN

                if event.type == KEYUP:
                    if not PAUSED:
                        if event.key in (K_w, K_s):
                            self.player1.direction = None
                        elif event.key in (K_UP, K_DOWN):
                            self.player2.direction = None

            # --- recalculations ---

            if not PAUSED:      
                self.player1.move()
                self.player2.move()
                self.ball.move()

            #~ print self.ball.get_rect()

            if pygame.sprite.collide_rect(self.ball, self.player1):
                self.ball.speed_x = -self.ball.speed_x

            if pygame.sprite.collide_rect(self.ball, self.player2):
                self.ball.speed_x = -self.ball.speed_x

            # --- drawing ---

            self.screen.blit(self.background,(0,0))
            self.player1.draw()
            self.player2.draw()
            self.ball.draw()

            if PAUSED:

                self.screen.blit(self.text_paused, self.text_rect.topleft)

            pygame.display.update()

            # --- FPS ---

            self.fpsClock.tick(self.FPS)

        # --- finish ---

        pygame.quit()
        sys.exit()

#----------------------------------------------------------------------

Game().run()