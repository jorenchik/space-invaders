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