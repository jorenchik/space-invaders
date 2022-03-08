from settings import *

# Helper functions
def isCollision(rect1, rect2):
    if rect1.colliderect(rect2):
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
def checkEnemyGroupCollision(group):
    enemiesCollided = []
    for enemy in group:
        collision = enemy.checkBorderCollision()
        if collision:
            enemiesCollided.append([enemy, collision])
    if len(enemiesCollided) > 0:
        return enemiesCollided[0][1]
    return False
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

# Enemy starting positions
def getEnemyPositions():
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
    return positions