# Helper functions
def isCollision(obj1, obj2, distance):
    if obj1.pos.distance_to(obj2.pos) <= distance:
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
            enemiesCollided.append(enemy)
    if len(enemiesCollided) > 0:
        return True
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