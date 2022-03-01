from re import X
from turtle import speed
import pygame
import math
import random
import click
import pathlib

# Clear the console
click.clear()

# Enemy sprite load
absPath = pathlib.Path.cwd()
assets = pathlib.Path(absPath/'assets')
enemySprites = list(assets.glob("enemy_*.png"))

class Enemy:
    def __init__(self, sprite=None, pos=None, speed=None):
        spriteIndex = random.randint(0, len(enemySprites)-1)
        sprite = sprite if sprite else enemySprites[spriteIndex]
        self.sprite = pygame.image.load(sprite)
        if pos:
            x = pos.x
            y = pos.y
        else:
            x = None
            y = None
        self.pos = pygame.Vector2(x if x else random.randint(0,736), y if y else random.randint(50,150))
        if speed:
            xSpeed = speed.x
            ySpeed = speed.y
        else:
            xSpeed = None
            ySpeed = None
        speedModule = math.sqrt(pow(xSpeed if xSpeed else .2, 2)+pow(ySpeed if ySpeed  else .1,2))
        angle = random.uniform(0, 2.0*math.pi)
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
        if self.pos.y + self.speed.y >= 336:
            return 'y'
        if self.pos.y + self.speed.y <= 50:
            return 'y'
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

# Settings
enemyLimit = 7

# Game initialization
pygame.init()
pygame.display.set_caption("Space invaders")
gameIcon = pygame.image.load("assets/icon.ico")
screen = pygame.display.set_mode((800,800))
screenImage = pygame.image.load("assets/screen.png")


# Create entities
enemies = []
for i in range(0,enemyLimit):
    enemies.append(Enemy())
player = Player()
fireball = Fireball(pygame.Vector2(player.pos.x,player.pos.y), pygame.Vector2(0, -.5))

def isCollision(obj1, obj2, distance):
    if obj1.pos.distance_to(obj2.pos) <= distance:
        return True
    return False

def changeXPos(obj, x):
    obj.pos.x += x

def changeYPos(obj, y):
    obj.pos.y += y


# State 
fireballState = 'ready'
score = 0

# Update cycle
active = True
while active:
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
        changeXPos(player, player.speed.x)
    player.move(player.pos.x, player.pos.y)

    # Enemy logic
    for enemy in enemies:
        changeXPos(enemy, enemy.speed.x)
        changeYPos(enemy, enemy.speed.y)
        borderCollision = enemy.checkBorderCollision()
        if(borderCollision):
            enemy.changeDirectionSymmetrically(borderCollision)
        enemy.move(enemy.pos.x, enemy.pos.y)

    # Fireball logic
    if fireball.pos.y <= 0:
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
    if fireball.state == 'fire':
        fireball.move(fireball.pos.x, fireball.pos.y)
        changeYPos(fireball, fireball.speed.y)
    colidedEnemies = []
    for enemy in enemies:
        if isCollision(fireball, enemy, 27):
            colidedEnemies.append(enemy)
    if(len(colidedEnemies) > 0):
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
        score += 1
        print(score)
    for enemy in colidedEnemies:
        enemies.remove(enemy)
            
    pygame.display.update()