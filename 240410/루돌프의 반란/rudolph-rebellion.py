# (x, y)가 보드 내의 좌표인지 확인하는 함수입니다.
def inBoard(x, y):
    return 1 <= x and x <= n and 1 <= y and y <= n

n, m, p, c, d = map(int, input().split())
# rudolf = tuple(map(int, input().split()))
rx,ry = map(int, input().split())

point = [0 for _ in range(p + 1)]
pos = [(0, 0) for _ in range(p + 1)]
a = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
alive = [False for _ in range(p + 1)]
panic = [0 for _ in range(p + 1)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

a[rx][ry] = -1

for _ in range(p):
    id, x, y = tuple(map(int, input().split()))
    pos[id] = (x, y)
    a[pos[id][0]][pos[id][1]] = id
    alive[id] = True

for t in range(1, m + 1):
    closestX, closestY, closestIdx = 10000, 10000, 0

    # 가장 가까운 산타 선택
    cand = []

    # 살아있는 산타 중 루돌프에 가장 가까운 산타를 찾습니다.
    for i in range(1, p + 1):
        if not alive[i]:
            continue

        currentBest = ((closestX - rx) ** 2 + (closestY - ry) ** 2, (-closestX, -closestY))
        currentValue = ((pos[i][0] - rx) ** 2 + (pos[i][1] - ry) ** 2, (-pos[i][0], -pos[i][1]))

        if currentValue < currentBest:
            closestX, closestY = pos[i]
            closestIdx = i

    # 가장 가까운 산타의 방향으로 루돌프가 이동합니다.
    if closestIdx:
        prx,pry=rx,ry
        moveX = 0
        if closestX > rx:
            moveX = 1
        elif closestX < rx:
            moveX = -1

        moveY = 0
        if closestY > ry:
            moveY = 1
        elif closestY < ry:
            moveY = -1

        rx,ry = (rx + moveX, ry + moveY)
        a[prx][pry] = 0

    # 루돌프의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
    if rx == closestX and ry == closestY:
        # 산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
        firstX = closestX + moveX * c
        firstY = closestY + moveY * c
        lastX, lastY = firstX, firstY

        panic[closestIdx] = t + 1

        # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
        while inBoard(lastX, lastY) and a[lastX][lastY] > 0:
            lastX += moveX
            lastY += moveY

        # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해, 충돌된 맨 첫 산타까지,
        # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY

            # 만약 밀쳐져서 나간 이번 산타의 이전 위치가 격자 밖이면 중지
            # if not inBoard(beforeX, beforeY):
            #     break

            idx = a[beforeX][beforeY]

            # 밀쳐진 위치가 격자 밖이면 탈락
            if not inBoard(lastX, lastY):
                alive[idx] = False
            # 격자 안이면 이동
            else:
                a[lastX][lastY] = a[beforeX][beforeY]
                pos[idx] = (lastX, lastY)

            lastX, lastY = beforeX, beforeY

        # 루돌프가 움직여서 충돌이 일어난 경우, 해당 산타는 C만큼의 점수를 얻게 됩니다
        point[closestIdx] += c
        # pos[closestIdx] = (firstX, firstY)
        # 충돌된 산타가 이동한 위치가 격자 안이면 이동
        if inBoard(firstX, firstY):
            pos[closestIdx] = (firstX, firstY)
            a[firstX][firstY] = closestIdx
        # 아니면 탈락
        else:
            alive[closestIdx] = False

    # 루돌프 이동 위치 업데이트
    a[rx][ry] = -1

    # 각 산타들은 루돌프와 가장 가까운 방향으로 한칸 이동합니다.
    for i in range(1, p+1):
        # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
        if not alive[i] or panic[i] >= t:
            continue

        # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동합니다.
        minDist = (pos[i][0] - rx)**2 + (pos[i][1] - ry)**2
        moveDir = -1

        for dir in range(4):
            nx = pos[i][0] + dx[dir]
            ny = pos[i][1] + dy[dir]

            # 산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
            if not inBoard(nx, ny) or a[nx][ny] > 0:
                continue

            dist = (nx - rx)**2 + (ny - ry)**2
            if dist < minDist:
                minDist = dist
                moveDir = dir

        # 움직일 수 있는 칸이 없다면 산타는 움직이지 않습니다.
        # 움직일 수 있는 칸이 있더라도 만약 루돌프로부터 가까워질 수 있는 방법이 없다면 산타는 움직이지 않습니다.
        # 움직일 수 있는 방향이 있다면, 이동
        if moveDir != -1:
            nx = pos[i][0] + dx[moveDir]
            ny = pos[i][1] + dy[moveDir]

            # 산타의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
            if nx == rx and ny == ry:
                panic[i] = t + 1

                #  산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
                moveX = -dx[moveDir]
                moveY = -dy[moveDir]

                firstX = nx + moveX * d
                firstY = ny + moveY * d
                lastX, lastY = firstX, firstY

                # 만약 산타의 힘이 1이라면, 제자리로 돌아오는 것이므로 포인트만 얻는다.
                if d == 1:
                    point[i] += d
                else:
                    # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
                    while inBoard(lastX, lastY) and a[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY

                    # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해,
                    # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
                    while not (lastX == firstX and lastY == firstY):
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY

                        idx = a[beforeX][beforeY]

                        if not inBoard(lastX, lastY):
                            alive[idx] = False
                        else:
                            a[lastX][lastY] = a[beforeX][beforeY]
                            pos[idx] = (lastX, lastY)

                        lastX, lastY = beforeX, beforeY

                    # 산타가 움직여서 충돌이 일어난 경우, 해당 산타는 D만큼의 점수를 얻게 됩니다
                    point[i] += d
                    a[pos[i][0]][pos[i][1]] = 0
                    # pos[i] = (firstX, firstY)
                    if inBoard(firstX, firstY):
                        pos[i] = (firstX, firstY)
                        a[firstX][firstY] = i
                    else:
                        alive[i] = False
            else:
                a[pos[i][0]][pos[i][1]] = 0
                pos[i] = (nx, ny)
                a[nx][ny] = i

    # 라운드가 끝나고 탈락하지 않은 산타들의 점수를 1 증가시킵니다.
    for i in range(1, p+1):
        if alive[i]:
            point[i] += 1


# 결과를 출력합니다.
for i in range(1, p + 1):
    print(point[i], end=" ")