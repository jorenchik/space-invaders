import pygame
import math
import random
import click

# Clear the console
click.clear()

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

enemySprite = pygame.image.load("assets/enemy_sprite.png")
enemyX = random.randint(0,736)
enemyY = random.randint(50,150)
enemyXChange = 0.2
enemyYChange = 10

bulletSprite =  pygame.image.load("assets/bullet_sprite.png")
bulletX = playerX
bulletY = playerY
bulletXChange = 0
bulletYChange = 0.5

# State variables
bulletState = "ready"
score = 0

# Display functions
def player(x,y):
    screen.blit(playerSprite, (x,y))
def enemy(x,y):
    screen.blit(enemySprite, (x,y))
def bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletSprite, (x+16,y-10))

# Helpers
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 40:
        return True
    else:
        return False

# Update cycle
active = True
while active:
    screen.fill([138,43,226])

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
                if bulletState == "ready":
                    bulletX = playerX
                    bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    if (playerX + playerXChange > 0) and (playerX + playerXChange < 736):
        playerX += playerXChange
    player(playerX, playerY)

    # Enemy logic
    enemyX+=enemyXChange
    enemyY+=enemyYChange
    if enemyX + enemyXChange >= 736:
        enemyXChange = -.2
    if enemyX + enemyXChange <= 0:
        enemyXChange = .2
    if enemyY + enemyYChange >= 336:
        enemyYChange = -.1
    if enemyY + enemyYChange <= 50:
        enemyYChange = .1
    enemy(enemyX, enemyY)


    # Bullet logic
    if bulletY <= 0:
        bulletY = playerY
        bulletState = "ready"
    if bulletState is "fire":
        bullet(bulletX,bulletY)
        bulletY -= bulletYChange
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY= playerY
        bulletState ="ready"
        score += 1
        print(score)
        enemyX = random.randint(0,736)
        enemyY = random.randint(50,150)
            
    pygame.display.update()