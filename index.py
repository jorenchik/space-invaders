from xml.dom.expatbuilder import FilterVisibilityController
import pygame
import random
import time
from models import *
from game import *
from helpers import *
from sprites import *

def main():
    # Create entities
    enemies = []
    positions = getEnemyPositions()
    for index in range(0,enemyLimit):
        for i, row in enumerate(positions):
            if index+1 in row:
                rowIndex = i
                position = [i, row.index(index+1)]
        size = (32,32)
        pos = pygame.Vector2(position[1]*(size[0]+enemyXGap)+startEnemyX,position[0]*(size[1]+enemyXGap)+startEnemyY)
        sprite = enemySprites[((rowIndex+1) % 4) - 1]
        enemy = Enemy(index+1, sprite, pos, size)
        enemies.append(enemy)
    player = Player(1, playerSprite, pygame.Vector2((370,720)),(50,50))
    fireballs = []
    hearts = []
    for i in range(0, heartCount):
        heart = Heart(i+1,heartSprite,pygame.Vector2(((i+1)*(32+5)-16),55), (32,32))
        hearts.append(heart)
    ball = Ball(1,ballSprite,pygame.Vector2((0,0)),(24,24))
    ball.move(-70,0)
    background = pygame.transform.scale(pygame.image.load(bg), (800,800))

    # Update cycle
    prevTime = time.time()
    while game.active:
        game.screen.blit(background, (0,0))

        # Display score
        textsurface = game.font.render(f"Score: {game.score}", False, (255, 255, 255))
        game.screen.blit(textsurface,(20,20))

        # Calculates deltatime
        clock.tick(fpsLimit)
        now = time.time()
        dt = (now - prevTime) * 1000
        prevTime = now

        # Player/event logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changeSpeedX(-playerSpeed)
                if event.key == pygame.K_RIGHT:
                    player.changeSpeedX(playerSpeed)
                if event.key == pygame.K_SPACE:
                    if not game.fireballPrevShotTime or (time.time() - game.fireballPrevShotTime) >= fireballCooldown:
                        fireball = Fireball(1,fireballSprite,pygame.Vector2(player.pos.x,player.pos.y), (32,32))
                        fireballs.append(fireball)
                        fireball.pos.x = (player.pos.x)
                        fireball.move(fireball.pos.x,fireball.pos.y)
                        game.fireballPrevShotTime = time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.changeSpeedX(0)
        
        playerBorderCollision = player.checkBorderCollision()
        if not playerBorderCollision:
            changeXPos(player, player.speed.x,dt)
        elif playerBorderCollision =='right':
            changeXPos(player,-1, 1)
        elif playerBorderCollision =='left':
            changeXPos(player,1, 1)
        else:
            changeXPos(player,5,dt)

        player.move(player.pos.x, player.pos.y)

        # Player death / lives
        collision = isCollision(player.rect,ball.rect)
        if collision and ball.state != "ready":
            if not godMode:
                player.ballHit()
                if player.timesHit % 2 == 0:
                    if len(hearts) > 1:
                        hearts.remove(hearts[-1])
                    else:       
                        game.playerAlive = False
                        game.active = False
            ball.state = "ready"
            ball.move(0,-70)
        for heart in hearts:
            heart.move(heart.pos.x, heart.pos.y)    
        
        # Enemy logic
        if len(enemies) == 0:
            game.playerAlive = False
            game.active = False
        groupCollision = checkEnemyGroupCollision(enemies)
        enemyCount = len(enemies)
        enemiesLost = enemyLimit-enemyCount
        for enemy in enemies:
            collision = isCollision(player.rect, enemy.rect)
            if collision:
                game.playerAlive = False
                game.active = False
            collision = isCollision(game.bottomBorder, enemy.rect)
            if collision:
                game.playerAlive = False
                game.active = False
            enemy.changeSpeedMulitplier(.04*enemiesLost)
            enemy.moveRect()
            if hitboxesVisible:
                pygame.draw.rect(game.screen, RED, enemy.rect, 2)
            changeXPos(enemy, enemy.speed.x,dt)
            changeYPos(enemy, enemy.speed.y,dt)
            borderCollision = enemy.checkBorderCollision()
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

        # Draw hitboxes
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

        # Fireball logic
        for fireball in fireballs:
            fireball.moveRect()
            colidedEnemies = []
            if hitboxesVisible:
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
                fireballs.remove(fireball)
            fireball.move(fireball.pos.x, fireball.pos.y)
            changeYPos(fireball, fireball.speed.y,dt)
            if(len(colidedEnemies) > 0):
                fireball.pos.y = player.pos.y
                game.score += len(colidedEnemies) * enemyKillScoreInc
                fireballs.remove(fireball)
            for enemy in colidedEnemies:
                enemies.remove(enemy)

        pygame.display.update()

def gameOver():
     # Game over if player isn't alive
    waiting = True
    while waiting:
        background = pygame.transform.scale(pygame.image.load(bg), (800,800))
        game.screen.blit(background, (0,0))
        gameOverText = game.font.render("Game over. Press space to restart.", False, (255, 255, 255))
        textRect = gameOverText.get_rect(center=(game.SCREEN_WIDTH/2, game.SCREEN_HEIGHT/2))
        game.screen.blit(gameOverText,textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.score = 0
                    game.playerAlive = True
                    game.active = True
                    waiting = False
                    break
        pygame.display.update()

while True:
    main()
    gameOver()