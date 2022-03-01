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
    def __init__(self, sprite=None, x=None, y=None, xChange=None, yChange=None, skin=None):
        spriteIndex = random.randint(0, len(enemySprites)-1)
        sprite = sprite if sprite else enemySprites[spriteIndex]
        self.sprite = pygame.image.load(sprite)
        self.pos = pygame.Vector2(x if x else random.randint(0,736), y if y else random.randint(50,150))
        speedModule = math.sqrt(pow(.2, 2)+pow(.1,2))
        angle = random.uniform(0, 2.0*math.pi)
        self.speed = pygame.Vector2([speedModule* math.cos(angle), speedModule * math.sin(angle)]) 
        self.x = x if x else random.randint(0,736)
        self.y = y if y else random.randint(50,150)
        self.xChange = xChange if xChange else .2
        self.yChange = yChange if yChange else .1
        self.skin = skin if skin else 'default'
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

# Settings
enemyLimit = 7

# Game initialization
pygame.init()
pygame.display.set_caption("Space invaders")
gameIcon = pygame.image.load("assets/icon.ico")
screen = pygame.display.set_mode((800,800))
screenImage = pygame.image.load("assets/screen.png")

# SPRITES
playerSprite = pygame.image.load("assets/player_sprite.png")
playerX =  370
playerY =  580
playerXChange = 0

fireballSprite =  pygame.image.load("assets/fireball_sprite.png")
fireballX = playerX
# fireballY has a slight offset
fireballY = playerY-25
fireballXChange = 0
fireballYChange = 0.5

# State variables
fireballState = "ready"
score = 0

# Display functions
def player(x,y):
    screen.blit(playerSprite, (x,y))
def fireball(x,y):
    global fireballState
    fireballState = "fire"
    screen.blit(fireballSprite, (x+16,y-10))

# Helpers
def isCollision(enemyX, enemyY, fireballX, fireballY):
    distance = math.sqrt(math.pow(enemyX-fireballX,2)+math.pow(enemyY-fireballY,2))
    if distance < 40:
        return True
    else:
        return False

# Create enemies
enemies = []
for i in range(0,enemyLimit):
    enemies.append(Enemy())

# Update cycle
active = True
while active:
    screen.fill([53,69,172])

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -.25
            if event.key == pygame.K_RIGHT:
                playerXChange = .25
            if event.key == pygame.K_SPACE:
                if fireballState == "ready":
                    # fireballX has a slight offset
                    fireballX = (playerX-15)
                    fireball(fireballX,fireballY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    if (playerX + playerXChange > 0) and (playerX + playerXChange < 736):
        playerX += playerXChange
    player(playerX, playerY)

    # Enemy logic
    for enemy in enemies:
        enemy.pos.x += enemy.speed.x
        enemy.pos.y += enemy.speed.y
        borderCollision = enemy.checkBorderCollision()
        if(borderCollision):
            enemy.changeDirectionSymmetrically(borderCollision)
        enemy.move(enemy.pos.x, enemy.pos.y)


    # fireball logic
    # if fireballY <= 0:
    #     fireballY = playerY
    #     fireballState = "ready"
    # if fireballState is "fire":
    #     fireball(fireballX,fireballY)
    #     fireballY -= fireballYChange
    # collision = isCollision(enemyX, enemyY, fireballX, fireballY)
    # if collision:
    #     fireballY= playerY
    #     fireballState ="ready"
    #     score += 1
    #     print(score)
    #     enemyX = random.randint(0,736)
    #     enemyY = random.randint(50,150)
            
    pygame.display.update()