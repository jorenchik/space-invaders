import pygame
import random
import click
import time
from models import *
from game import *
from helpers import *

# Clear the console
click.clear()

# Colors
RED = (255,0,0)

# Create entities
enemies = []
for i in range(0,enemyLimit):
    spriteIndex = random.randint(0, len(enemySprites)-1)
    sprite = enemySprites[spriteIndex]
    enemies.append(Enemy(i+1, sprite))
player = Player(1, "assets/player_sprite.png")
fireball = Fireball(1,"assets/fireball_sprite.png",pygame.Vector2(player.pos.x,player.pos.y))
hearts = []
for i in range(0, heartCount):
    hearts.append(Hearth(i+1,"assets/heart.png"))
ball = Ball(1,"assets/ball.png")
ball.move(-70,0)

# Update cycle
prevTime = time.time()
while game.active:
    game.screen.fill([53,69,172])

    if not game.playerAlive:
        game.waitForKey("GAME OVER. PRESS SPACE TO RESTART")

    # Display score
    textsurface = game.font.render(f"Score: {game.score}", False, (0, 0, 0))
    game.screen.blit(textsurface,(20,20))

    # Calculates deltatime
    clock.tick(fpsLimit)
    now = time.time()
    dt = (now - prevTime) * 1000
    prevTime = now

    # Player/event logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.active = False
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
    elif playerBorderCollision =='right':
        changeXPos(player,-5,dt)
    else:
        changeXPos(player,5,dt)
    player.move(player.pos.x, player.pos.y)
    collision = isCollision(player,ball,27)
    if collision and ball.state != "ready":
        if len(hearts) > 1:
            hearts.remove(hearts[-1])
        else:
            game.playerAlive = False
            
        ball.state = "ready"

    # Enemy logic
    groupCollision = checkEnemyGroupCollision(enemies)
    for enemy in enemies:
        enemy.moveRect()
        if hitboxesVisible:
            pygame.draw.rect(game.screen, RED, enemy.rect, 2)
        changeXPos(enemy, enemy.speed.x,dt)
        changeYPos(enemy, enemy.speed.y,dt)
        borderCollision = enemy.checkBorderCollision()
        if(groupCollision and enemy.speed.x>0 and groupCollision == 'right'):
                enemy.changeDirectionSymmetrically('x')
        if(groupCollision and enemy.speed.x<0 and groupCollision == 'left'):
                enemy.changeDirectionSymmetrically('x')
        enemy.move(enemy.pos.x, enemy.pos.y)

    if len(enemies) > 0:
        enemiesReadyToShoot = getEnemiesReadyToShoot(enemies, positions)
        shootingEnemyPos = random.choice(enemiesReadyToShoot)
        shootingEnemyIndex = positions[shootingEnemyPos[1]][shootingEnemyPos[0]]
        shootingEnemy = None
        for enemy in enemies:
            if enemy.index == shootingEnemyIndex:
                shootingEnemy = enemy

        if ball.state == 'ready':
            ball.pos.x = shootingEnemy.pos.x
            ball.pos.y = shootingEnemy.pos.y
            ball.move(ball.pos.x, ball.pos.y)
            ball.state = 'fire'
        elif ball.state == 'fire':
            ball.move(ball.pos.x, ball.pos.y)
            changeYPos(ball, fireballSpeed,dt)

    if hitboxesVisible:
        pygame.draw.rect(game.screen, RED, game.leftBorder, 2)
        pygame.draw.rect(game.screen, RED, game.rightBorder, 2)
        pygame.draw.rect(game.screen, RED, player.rect, 2)
    player.moveRect()

    # Fireball logic
    colidedEnemies = []
    fireball.moveRect()
    if hitboxesVisible and not fireball.state == 'ready':
            pygame.draw.rect(game.screen, RED, fireball.rect, 2)
    for enemy in enemies:
        if isCollision(fireball, enemy, 50):
            colidedEnemies.append(enemy)
    if fireball.pos.y <= 0:
        if len(colidedEnemies) == 0:
            game.score -= 1
            if game.score < 0:
                game.score = 0 
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
    if fireball.state == 'fire':
        fireball.move(fireball.pos.x, fireball.pos.y)
        changeYPos(fireball, fireball.speed.y,dt)
    if(len(colidedEnemies) > 0):
        fireball.pos.y = player.pos.y
        fireball.state = 'ready'
        game.score += 1
    for enemy in colidedEnemies:
        enemies.remove(enemy)
    
    for heart in hearts:
        heart.move(heart.pos.x, heart.pos.y)

    pygame.display.update()