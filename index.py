import pygame
import random
import click
import time
from models import *
from game import *
from helpers import *
from sprites import *

# Clear the console
click.clear()

# Colors
RED = (255,0,0)

# Create entities
enemies = []
positions = getEnemyPositions()
for index in range(0,enemyLimit):
    for i, row in enumerate(positions):
        if index+1 in row:
            rowIndex = i
            position = [i, row.index(index+1)]
    pos = pygame.Vector2(position[1]*(64+enemyXGap)+startEnemyX,position[0]*(64+enemyXGap)+startEnemyY)
    sprite = enemySprites[rowIndex]
    enemies.append(Enemy(index+1, sprite, pos))
player = Player(1, playerSprite, pygame.Vector2((370,580)))
fireball = Fireball(1,fireballSprite,pygame.Vector2(player.pos.x,player.pos.y))
hearts = []
for i in range(0, heartCount):
    hearts.append(Heart(i+1,heartSprite,pygame.Vector2(((i+1)*(32+5)-16),45)))
ball = Ball(1,ballSprite)
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
        changeXPos(player,-1, 1)
    else:
        changeXPos(player,5,dt)
    player.move(player.pos.x, player.pos.y)
    collision = isCollision(player.rect,ball.rect)
    if collision and ball.state != "ready":
        if len(hearts) > 1:
            if not godMode:
                hearts.remove(hearts[-1])
        else:
            game.playerAlive = False
        ball.state = "ready"

    # Enemy logic
    groupCollision = checkEnemyGroupCollision(enemies)
    enemyCount = len(enemies)
    enemiesLost = enemyLimit-enemyCount
    for enemy in enemies:
        enemy.changeSpeedMulitplier(.04*enemiesLost)
        enemy.moveRect()
        if hitboxesVisible:
            pygame.draw.rect(game.screen, RED, enemy.rect, 2)
        changeXPos(enemy, enemy.speed.x,dt)
        changeYPos(enemy, enemy.speed.y,dt)
        borderCollision = enemy.checkBorderCollision()
        if borderCollision:
            print(borderCollision)
        if(groupCollision and enemy.speed.x>0 and groupCollision == 'right'):
            game.enemiesMovingDown = time.time()
            game.enemiesLastSideCollision = 'right'
            enemy.rotateDirection(90)
        if(groupCollision and enemy.speed.x<0 and groupCollision == 'left'):
            game.enemiesMovingDown = time.time()
            game.enemiesLastSideCollision = 'left'
            enemy.rotateDirection(-90)
        enemy.move(enemy.pos.x, enemy.pos.y)

    if game.enemiesMovingDown and (time.time() - game.enemiesMovingDown) > enemyMovingDownDur:
        for enemy in enemies:
            if game.enemiesLastSideCollision == 'right':
                enemy.rotateDirection(90)
            if game.enemiesLastSideCollision == 'left':
                enemy.rotateDirection(-90)
        game.enemiesMovingDown = False

    # Ball logic
    if len(enemies) > 0:
        enemiesReadyToShoot = getEnemiesReadyToShoot(enemies, positions)
        shootingEnemyPos = random.choice(enemiesReadyToShoot)
        shootingEnemyIndex = positions[shootingEnemyPos[1]][shootingEnemyPos[0]]
        shootingEnemy = None
        for enemy in enemies:
            if enemy.index == shootingEnemyIndex:
                shootingEnemy = enemy
        if isCollision(ball.rect, game.bottomBorder):
            ball.state = 'ready'
            ball.changeSpeedY(0)
            ball.changePos(0,-1)
        if ball.state == 'ready':
            ball.pos.x = shootingEnemy.pos.x
            ball.pos.y = shootingEnemy.pos.y
            ball.move(ball.pos.x, ball.pos.y)
            ball.changeSpeedY(-fireballSpeed)
            ball.state = 'fire'
        elif ball.state == 'fire':
            ball.move(ball.pos.x, ball.pos.y)
            changeYPos(ball, -ball.speed.y,dt)

    # Draw independant hitboxes
    if hitboxesVisible:
        pygame.draw.rect(game.screen, RED, game.leftBorder, 2)
        pygame.draw.rect(game.screen, RED, game.rightBorder, 2)
        pygame.draw.rect(game.screen, RED, game.topBorder, 2)
        pygame.draw.rect(game.screen, RED, game.bottomBorder, 2)
        pygame.draw.rect(game.screen, RED, game.bottomEnemyBorder, 2)
        pygame.draw.rect(game.screen, RED, game.topEnemyBorder, 2)
        pygame.draw.rect(game.screen, RED, player.rect, 2)
        pygame.draw.rect(game.screen, RED, ball.rect, 2)
    player.moveRect()
    ball.moveRect()

    # Fireball logic
    colidedEnemies = []
    fireball.moveRect()
    if hitboxesVisible and not fireball.state == 'ready':
            pygame.draw.rect(game.screen, RED, fireball.rect, 2)
    for enemy in enemies:
        if isCollision(fireball.rect, enemy.rect):
            colidedEnemies.append(enemy)
    if fireball.pos.y <= 0:
        if len(colidedEnemies) == 0:
            game.score -= missScoreDec
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
        game.score += len(colidedEnemies) * enemyKillScoreInc
    for enemy in colidedEnemies:
        enemies.remove(enemy)
    
    for heart in hearts:
        heart.move(heart.pos.x, heart.pos.y)

    pygame.display.update()