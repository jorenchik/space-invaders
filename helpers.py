from settings import *

# Helper functions
def isCollision(rect1, rect2):
    if rect1.colliderect(rect2):
        return True
    return False
def changeXPos(obj, x, dt):
    obj.pos.x += x*dt
def changeYPos(obj, y, dt):
    obj.pos.y += y*dt
def getEnemiesReadyToShoot(enemies, positions):
    candidates = []
    columns = [[] for x in range(enemyColumns)]
    for enemy in enemies:
        for i, row in enumerate(positions):
            if enemy.index in row:
                columns[row.index(enemy.index)-1].append([row.index(enemy.index),i])
    for column in columns:
        if len(column) > 0:
            column.sort(key = lambda x: x[1])
            candidates.append(column[-1])
    return candidates
def checkEnemyGroupCollision(group):
    enemiesCollided = []
    for enemy in group:
        collision = enemy.checkBorderCollision()
        if collision:
            enemiesCollided.append([enemy, collision])
    if len(enemiesCollided) > 0:
        return enemiesCollided[0][1]
    return False
def getEnemyPositions():
    cols = enemyColumns
    positions = [[0 for x in range(cols)] for x in range(maximalEnemyRows)]
    usedRows = int((enemyLimit-1) / enemyColumns) + 1
    currentRowIndex = 0
    enemyIndex = 1
    while currentRowIndex <= usedRows:
        row = positions[currentRowIndex]
        remainingEnemies = enemyLimit - currentRowIndex * enemyColumns
        if remainingEnemies >= enemyColumns: remainingEnemies = enemyColumns
        if remainingEnemies:
            for i in range(0, remainingEnemies):
                del row[i]
                row.insert(i, enemyIndex)
                enemyIndex += 1
                i += 1
        currentRowIndex += 1
    return positions
