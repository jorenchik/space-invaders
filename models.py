import pygame
from game import game
from settings import *
from helpers import *

class Entity:
    def __init__(self,index,sprite,pos,speed):
        self.index = index
        self.sprite = pygame.image.load(sprite)
        self.hitboxWidth = self.sprite.get_width()
        self.hitboxHeight = self.sprite.get_height()
        self.speed = speed
        self.pos = pos
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))
    def changeDirectionSymmetrically(self, ax):
        self.speed = pygame.Vector2((-self.speed.x, self.speed.y)) if ax == 'x' else pygame.Vector2((self.speed.x, -self.speed.y))
    def rotateDirection(self, deg):
        self.speed = self.speed.rotate(deg)
    def checkBorderCollision(self):
        if self.rect.colliderect(game.leftBorder):
            return 'left'
        if self.rect.colliderect(game.rightBorder):
            return 'right'
        return False
    def moveRect(self):
        self.rect.center = (self.pos.x+self.hitboxWidth/2,self.pos.y+self.hitboxHeight/2)
    def changePos(self,x,y):
        self.pos.x=x
        self.pos.y=y
    def changeSpeedX(self, x):
        self.speed.x = x
    def changeSpeedY(self, y):
        self.speed.y = y

class Enemy(Entity):
    def __init__(self,index,sprite,pos):
        speed = pygame.Vector2((1*enemySpeed, 0*enemySpeed))
        Entity.__init__(self,index,sprite,pos,speed)
    def checkBorderCollision(self):
        if self.rect.colliderect(game.bottomEnemyBorder):
            return 'bottom'
        if self.rect.colliderect(game.topEnemyBorder):
            return 'top'
        return super().checkBorderCollision()
class Player(Entity):
    def __init__(self,index,sprite,pos):
        speed = pygame.Vector2((0,0))
        Entity.__init__(self,index,sprite,pos,speed)
        
class Fireball(Entity): 
    def __init__(self,index,sprite,pos):
        speed = pygame.Vector2((0,-fireballSpeed))
        Entity.__init__(self,index,sprite,pos,speed)
        self.state = 'ready'

class Ball(Entity): 
    def __init__(self, index,sprite, pos=pygame.Vector2((0,0))):
        speed = pygame.Vector2(0, -fireballSpeed)
        Entity.__init__(self,index,sprite,pos,speed)
        self.state = 'ready'

class Heart(Entity):
    def __init__(self, index,sprite,pos):
        self.index = index
        speed = pygame.Vector2((0,0))
        Entity.__init__(self,index,sprite,pos,speed)
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))