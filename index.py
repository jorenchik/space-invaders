from re import X
from turtle import speed
from numpy import empty
import pygame
import math
import random
import click
import pathlib
import time

clock = pygame.time.Clock()

# Clear the console
click.clear()

# Enemy sprite load
absPath = pathlib.Path.cwd()
assets = pathlib.Path(absPath/'assets')
enemySprites = list(assets.glob("enemy_*.png"))

# Settings
enemyLimit = 2
startEnemyX = 30
startEnemyY = 50
endEnemyY = 410
enemyXGap = 5
enemyYGap = 5
enemiesXPadding = 30
enemyDefaultXSpeed = .2
enemyDefaultYSpeed = .1
enemySpeedMultiplier = 10

# Calculate enemy positions
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

# print(positions)
# exit()

class Enemy:
    def __init__(self,index,sprite=None, pos=None, speed=None):
        self.index = index
        spriteIndex = random.randint(0, len(enemySprites)-1)
        sprite = sprite if sprite else enemySprites[spriteIndex]
        self.sprite = pygame.image.load(sprite)
        if pos:
            x = pos.x
            y = pos.y
        else:
            x = None
            y = None
        for i, row in enumerate(positions):
            if self.index in row:
                position = [i, row.index(self.index)]
        self.pos = pygame.Vector2(x if x else position[1]*(64+enemyXGap)+startEnemyX, y if y else position[0]*(64+enemyXGap)+startEnemyY)
        if speed:
            customSpeed = True
            xSpeed = speed.x*enemySpeedMultiplier
            ySpeed = speed.y*enemySpeedMultiplier
        else:
            customSpeed = None
            xSpeed = None
            ySpeed = None
        angle = random.uniform(0, 2.0*math.pi)
        if customSpeed:
            self.speed = pygame.Vector2([xSpeed, ySpeed]) 
        else:
            speedModule = math.sqrt(pow(xSpeed if xSpeed else .2*enemySpeedMultiplier, 2)+pow(ySpeed if ySpeed  else .1*enemySpeedMultiplier,2))
            self.speed = pygame.Vector2([speedModule* math.cos(angle), speedModule * math.sin(angle)]) 
    def move(self,x,y):
        screen.blit(self.sprite, (x,y))
    def changeDirectionSymmetrically(self, ax):
        self.speed = pygame.Vector2((-self.speed.x, self.speed.y)) if ax == 'x' else pygame.Vector2((self.speed.x, -self.speed.y))
    def checkBorderCollision(self):
        if self.pos.x + self.speed.x >= 736:
            return 'x'
        if self.pos.x + self.speed.x <= 0:
            return 'x'
        if self.pos.y + self.speed.y >= 600:
            return 'y'
        if self.pos.y + self.speed.y <= 0:
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
        if self.pos.x + self.speed.x >= 736:
            return True
        if self.pos.x + self.speed.x <= 0:
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


# Game initialization
pygame.init()
pygame.display.set_caption("Space invaders")
gameIcon = pygame.image.load("assets/icon.ico")
screen = pygame.display.set_mode((800,800))
screenImage = pygame.image.load("assets/screen.png")


# Create entities
speedModule = math.sqrt(pow(enemyDefaultXSpeed, 2)+pow(enemyDefaultYSpeed,2))
enemyCommonSpeed = pygame.Vector2((speedModule, 0))
enemies = []
for i in range(0,enemyLimit):
    enemies.append(Enemy(i+1,None,None,enemyCommonSpeed))
player = Player()
fireball = Fireball(pygame.Vector2(player.pos.x,player.pos.y), pygame.Vector2(0, -.5))


def isCollision(obj1, obj2, distance):
    if obj1.pos.distance_to(obj2.pos) <= distance:
        return True
    return False

def changeXPos(obj, x, dt):
    obj.pos.x += x

def changeYPos(obj, y, dt):
    obj.pos.y += y


# State 
fireballState = 'ready'
score = 0
leftTouched = False
rightTouched = False

# Update cycle
active = True
while active:
    dt = 0
    screen.fill([53,69,172])

    # Player logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changeSpeedX(-.25)
            if event.key == pygame.K_RIGHT:
                player.changeSpeedX(.25)
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

    groupCollision = checkEnemyGroupCollision(enemies)

    # Enemy logic
    for enemy in enemies:
        changeXPos(enemy, enemy.speed.x,dt)
        changeYPos(enemy, enemy.speed.y,dt)
        borderCollision = enemy.checkBorderCollision()
        # if(borderCollision):
        #         enemy.changeDirectionSymmetrically(borderCollision)
        if(groupCollision):
                enemy.changeDirectionSymmetrically('x')
        enemy.move(enemy.pos.x, enemy.pos.y)

    # Fireball logic
    if fireball.pos.y <= 0:
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
    if fireball.state == 'fire':
        fireball.move(fireball.pos.x, fireball.pos.y)
        changeYPos(fireball, fireball.speed.y,dt)
    colidedEnemies = []
    for enemy in enemies:
        if isCollision(fireball, enemy, 50):
            colidedEnemies.append(enemy)
    if(len(colidedEnemies) > 0):
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
        score += 1
        print(score)
    for enemy in colidedEnemies:
        enemies.remove(enemy)
            
    pygame.display.update()