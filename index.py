from re import X
from turtle import position, showturtle, speed
from numpy import empty
import pygame
import math
import random
import click
import pathlib
import time

from pyparsing import col

# Initialize clock for dt and limiting the framerate
clock = pygame.time.Clock()

# Clear the console
click.clear()

# Enemy sprite load
absPath = pathlib.Path.cwd()
assets = pathlib.Path(absPath/'assets')
enemySprites = list(assets.glob("enemy_*.png"))

# Settings
fpsLimit = 60
enemyLimit = 6
heartCount = 2
startEnemyX = 30
startEnemyY = 100
endEnemyY = 450
enemyXGap = 5
enemyYGap = 5
enemyCollisionYStart = 0
enemyCollisionYEnd = 600
enemyCollisionXStart = 0
enemyCollisionXEnd = 736
playerCollisionXStart = 0
playerCollisionXEnd = 736
enemySpeed = 2
fireballSpeed = 8
playerSpeed = 3

# Enemy starting positions
def getNeighbours(i, n, arr):
    neighbours = []
    try:
        if(arr[i-1][n] == 0):
            neighbours.append([i-1,n])
    except:
        print()
    try:
        if(arr[i+1][n] == 0):
            neighbours.append([i+1,n])
    except:
        print()
    try:
        if(arr[i][n-1] == 0):
            neighbours.append([i,n-1])
    except:
        print()
    try:
        if(arr[i][n+1] == 0):
            neighbours.append([i,n+1])
    except:
        print() 
    return neighbours
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
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))
    def changeDirectionSymmetrically(self, ax):
        self.speed = pygame.Vector2((-self.speed.x, self.speed.y)) if ax == 'x' else pygame.Vector2((self.speed.x, -self.speed.y))
    def checkBorderCollision(self):
        if self.pos.x + self.speed.x <= enemyCollisionXStart:
            return 'x'
        if self.pos.x + self.speed.x >= enemyCollisionXEnd:
            return 'x'
        if self.pos.y + self.speed.y <= enemyCollisionYStart:
            return 'y'
        if self.pos.y + self.speed.y >= enemyCollisionYEnd:
            return 'y'
        return False

def checkEnemyGroupCollision(group):
    enemiesCollided = []
    for enemy in group:
        collision = enemy.checkBorderCollision()
        if collision:
            enemiesCollided.append(enemy)
    if len(enemiesCollided) > 0:
        return True
    return False

class Player:
    pos = pygame.Vector2((370,580))
    speed = pygame.Vector2((0,0))
    sprite = pygame.image.load("assets/player_sprite.png")
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))
    def changeSpeedX(self, x):
        self.speed.x = x
    def checkBorderCollision(self):
        if self.pos.x + self.speed.x <= playerCollisionXStart:
            return True
        if self.pos.x + self.speed.x >= playerCollisionXEnd:
            return True
        return False
        
class Fireball: 
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.sprite = pygame.image.load("assets/fireball_sprite.png")
        self.state = 'ready'
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))

class Ball: 
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.sprite = pygame.image.load("assets/ball.png")
        self.state = 'ready'
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))

class Hearth:
    def __init__(self, index):
        self.index = index
        self.pos = pygame.Vector2(((index*(32+5)-16),45))
        self.sprite = pygame.image.load('assets/heart.png')
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))

# Game initialization
pygame.init()
pygame.display.set_caption("Space invaders")
gameIcon = pygame.image.load("assets/icon.ico")
screen = pygame.display.set_mode((800,800))
screenImage = pygame.image.load("assets/screen.png")

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)


# Create entities
enemies = []
for i in range(0,enemyLimit):
    enemies.append(Enemy(i+1))
player = Player()
fireball = Fireball(pygame.Vector2(player.pos.x,player.pos.y), pygame.Vector2(0, -fireballSpeed))
hearts = []
for i in range(0, heartCount):
    hearts.append(Hearth(i+1))
ball = Ball(pygame.Vector2(0,0), pygame.Vector2(0, fireballSpeed))
ball.move(-70,0)

# Helpers
def isCollision(obj1, obj2, distance):
    if obj1.pos.distance_to(obj2.pos) <= distance:
        return True
    return False
def changeXPos(obj, x, dt):
    obj.pos.x += x
def changeYPos(obj, y, dt):
    obj.pos.y += y
def getEnemiesReadyToShoot(enemies, positions):
    candidates = []
    columns = [[] for x in range(10)]
    for enemy in enemies:
        for i, row in enumerate(positions):
            if enemy.index in row:
                columns[row.index(enemy.index)-1].append([row.index(enemy.index),i])
    for column in columns:
        if len(column) > 0:
            column.sort(key = lambda x: x[1])
            candidates.append(column[-1])
    return candidates
    


# State 
fireballState = 'ready'
score = 0
leftTouched = False
rightTouched = False

# Update cycle
active = True
prevTime = time.time()
while active:
    screen.fill([53,69,172])

    # Display score
    textsurface = myfont.render(f"Score: {score}", False, (0, 0, 0))
    screen.blit(textsurface,(20,20))

    # Calculates deltatime
    clock.tick(fpsLimit)
    now = time.time()
    dt = (now - prevTime) * 1000
    prevTime = now

    # Player/event logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changeSpeedX(-playerSpeed)
            if event.key == pygame.K_RIGHT:
                player.changeSpeedX(playerSpeed)
            if event.key == pygame.K_SPACE:
                if fireball.state == "ready":
                    # fireballX has a slight offset
                    fireball.state = 'fire'
                    fireball.pos.x = (player.pos.x)
                    fireball.move(fireball.pos.x,fireball.pos.y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.changeSpeedX(0)
    playerBorderCollision = player.checkBorderCollision()
    if not playerBorderCollision:
        changeXPos(player, player.speed.x,dt)
    player.move(player.pos.x, player.pos.y)

    # Enemy logic
    groupCollision = checkEnemyGroupCollision(enemies)
    for enemy in enemies:
        changeXPos(enemy, enemy.speed.x,dt)
        changeYPos(enemy, enemy.speed.y,dt)
        borderCollision = enemy.checkBorderCollision()
        if(groupCollision):
                enemy.changeDirectionSymmetrically('x')
        enemy.move(enemy.pos.x, enemy.pos.y)

    enemiesReadyToShoot = getEnemiesReadyToShoot(enemies, positions)
    print(enemiesReadyToShoot)
    shootingEnemyPos = random.choice(enemiesReadyToShoot)
    shootingEnemyIndex = positions[shootingEnemyPos[1]][shootingEnemyPos[0]]
    shootingEnemy = None
    for enemy in enemies:
        if enemy.index == shootingEnemyIndex:
            shootingEnemy = enemy

    if(ball.state == 'ready'):
        ball.pos.x = shootingEnemy.pos.x
        ball.pos.y = shootingEnemy.pos.y
        ball.move(ball.pos.x, ball.pos.y)
        ball.state = 'fire'
    elif ball.state == 'fire':
        ball.move(ball.pos.x, ball.pos.y)
        changeYPos(ball, fireballSpeed,dt)

    # Fireball logic
    colidedEnemies = []
    for enemy in enemies:
        if isCollision(fireball, enemy, 50):
            colidedEnemies.append(enemy)
    if fireball.pos.y <= 0:
        if len(colidedEnemies) == 0:
            score -= 1
            if score < 0:
                score = 0 
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
    if fireball.state == 'fire':
        fireball.move(fireball.pos.x, fireball.pos.y)
        changeYPos(fireball, fireball.speed.y,dt)
    if(len(colidedEnemies) > 0):
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
        score += 1
    for enemy in colidedEnemies:
        enemies.remove(enemy)
    
    for heart in hearts:
        heart.move(heart.pos.x, heart.pos.y)

    pygame.display.update()