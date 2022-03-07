import pygame
import random
import pathlib

import scipy as sp
from game import game
from settings import *
from helpers import *

# Enemy sprite load
absPath = pathlib.Path.cwd()
assets = pathlib.Path(absPath/'assets')
enemySprites = list(assets.glob("enemy_*.png"))

# Enemy starting positions
rows = 5
cols = 10
positions = [[0 for x in range(cols)] for x in range(rows)]
enemyCount = 0
if(enemyLimit>0):
    num = 1
    positions[2][4] = num
    neighbours = getNeighbours(2,4,positions)
    while num <= enemyLimit and len(neighbours)>0:
        i = neighbours[0][0]
        n = neighbours[0][1]
        num += 1
        positions[i][n]=num
        if len(neighbours) > 1:
            neighbours.remove(neighbours[0])
        else:
            current = neighbours[0]
            neighbours = getNeighbours(current[0], current[1], positions)
            if len(neighbours) == 0:
                break
    unfilledPositions = []
    for i, row in enumerate(positions):
        zeros = [i for i, x in enumerate(row) if x == 0]
        for ind, v in enumerate(zeros):
            unfilledPositions.append([i, ind])
    if num < enemyLimit:
        unfilledPositionCount = enemyLimit - num
        for i in range(0, unfilledPositionCount):
            randomPos = random.choice(unfilledPositions)
            positions[randomPos[0]][randomPos[1]] = num+1
            unfilledPositions.remove(randomPos)
            num += 1

class Entity:
    def __init__(self,index,sprite,speed):
        self.index = index
        self.sprite = pygame.image.load(sprite)
        self.hitboxWidth = self.sprite.get_width()
        self.hitboxHeight = self.sprite.get_height()
        self.speed = speed
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))
    def changeDirectionSymmetrically(self, ax):
        self.speed = pygame.Vector2((-self.speed.x, self.speed.y)) if ax == 'x' else pygame.Vector2((self.speed.x, -self.speed.y))
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
    def __init__(self,index,sprite):
        speed = pygame.Vector2((1*enemySpeed, 0*enemySpeed))
        Entity.__init__(self,index,sprite,speed)
        for i, row in enumerate(positions):
            if self.index in row:
                position = [i, row.index(self.index)]
        self.pos = pygame.Vector2(position[1]*(64+enemyXGap)+startEnemyX,position[0]*(64+enemyXGap)+startEnemyY)
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
        for i, row in enumerate(positions):
            if self.index in row:
                position = [i, row.index(self.index)]

class Player(Entity):
    def __init__(self,index,sprite):
        speed = pygame.Vector2((0,0))
        Entity.__init__(self,index,sprite,speed)
        self.pos = pygame.Vector2((370,580))
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
        
class Fireball(Entity): 
    def __init__(self,index,sprite,pos):
        speed = pygame.Vector2((0,-fireballSpeed))
        Entity.__init__(self,index,sprite,speed)
        self.pos = pos
        self.state = 'ready'
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)

class Ball(Entity): 
    def __init__(self, index,sprite):
        speed = pygame.Vector2(0, -fireballSpeed)
        Entity.__init__(self,index,sprite,speed)
        self.pos = pygame.Vector2((0,0))
        self.speed = speed
        self.state = 'ready'
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)

class Hearth(Entity):
    def __init__(self, index,sprite):
        self.index = index
        speed = pygame.Vector2((0,0))
        Entity.__init__(self,index,sprite,speed)
        self.pos = pygame.Vector2(((index*(32+5)-16),45))
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))