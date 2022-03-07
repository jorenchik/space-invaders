import pygame
import random
import pathlib
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


class Enemy:
    def __init__(self,index):
        self.index = index
        spriteIndex = random.randint(0, len(enemySprites)-1)
        sprite = enemySprites[spriteIndex]
        self.sprite = pygame.image.load(sprite)
        for i, row in enumerate(positions):
            if self.index in row:
                position = [i, row.index(self.index)]
        self.pos = pygame.Vector2(position[1]*(64+enemyXGap)+startEnemyX,position[0]*(64+enemyXGap)+startEnemyY)
        self.speed = pygame.Vector2([1*enemySpeed, 0*enemySpeed])
        self.hitboxWidth = 64
        self.hitboxHeight = 64
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
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

class Player:
    def __init__(self):
        self.pos = pygame.Vector2((370,580))
        self.speed = pygame.Vector2((0,0))
        self.sprite = pygame.image.load("assets/player_sprite.png")
        self.hitboxWidth = 64
        self.hitboxHeight = 64
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))
    def changeSpeedX(self, x):
        self.speed.x = x
    def checkBorderCollision(self):
        if self.rect.colliderect(game.leftBorder):
            return 'left'
        if self.rect.colliderect(game.rightBorder):
            return 'right'
        return False
    def moveRect(self):
        self.rect.center = (self.pos.x+self.hitboxWidth/2,self.pos.y+self.hitboxHeight/2)
        
class Fireball: 
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.sprite = pygame.image.load("assets/fireball_sprite.png")
        self.state = 'ready'
        self.hitboxWidth = 52
        self.hitboxHeight = 52
        self.rect = pygame.Rect(self.pos.x,self.pos.y,self.hitboxWidth,self.hitboxWidth)
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))
    def moveRect(self):
        self.rect.center = (self.pos.x+32,self.pos.y+32)
class Ball: 
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.sprite = pygame.image.load("assets/ball.png")
        self.state = 'ready'
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))

class Hearth:
    def __init__(self, index):
        self.index = index
        self.pos = pygame.Vector2(((index*(32+5)-16),45))
        self.sprite = pygame.image.load('assets/heart.png')
    def move(self,x,y):
        game.screen.blit(self.sprite, (x,y))