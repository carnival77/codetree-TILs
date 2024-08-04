from collections import deque

n,m,K=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)] # 맵
b=[[0]*n for _ in range(n)] # 위쪽 벽 맵. ( 0 : 빈 칸, 1 : 위쪽 벽 )
b2=[[0]*n for _ in range(n)] # 왼쪽 벽 맵. ( 0 : 빈 칸, 1 : 왼쪽 벽 )
c=[[0]*n for _ in range(n)] # 시원함 맵

#  좌,상,우,하
dx=[0,-1,0,1]
dy=[-1,0,1,0]

# 벽 설치
for _ in range(m):
    x,y,s=map(int,input().split()) # 0:위쪽, 1:왼쪽
    if s==0:
        b[x-1][y-1]=1
    elif s==1:
        b2[x-1][y-1]=1

# 에어컨 위치
aircon=[] # 에어컨 위치, 종류
for x in range(n):
    for y in range(n):
        if 2<=a[x][y]<=5:
            aircon.append([x,y,a[x][y]-2])

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def spread():
    global c

    for sx,sy,d in aircon:
        tmp = [[0] * n for _ in range(n)]
        nx,ny=sx+dx[d],sy+dy[d]
        num=5
        if not inBoard(nx,ny):continue
        q=deque()
        q.append([nx,ny,num])
        while q:
            x,y,num=q.popleft()
            tmp[x][y] = num
            num-=1
            if num==0:continue
            # 좌
            if d==0:
                # 바라보는 방향에서 우측 대각선 45도
                nd1 = (d + 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1,ny1) and b[x][y]==0:
                    nd2 = (nd1 - 1) % 4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2,ny2) and b2[nx1][ny1]==0:
                        q.append([nx2,ny2,num])
                # 바라보는 방향 정면
                nx1,ny1=x+dx[d],y+dy[d]
                if inBoard(nx1,ny1) and b2[x][y]==0:
                    q.append([nx1,ny1,num])
                # 바라보는 방향에서 좌측 대각선 45도
                nd1 = (d - 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1, ny1) and b[nx1][ny1] == 0:
                    nd2 = (nd1 + 1) % 4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2, ny2) and b2[nx1][ny1] == 0:
                        q.append([nx2, ny2, num])
            # 상
            elif d==1:
                # 바라보는 방향에서 좌측 대각선 45도
                nd1 = (d - 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1, ny1) and b2[x][y] == 0:
                    nd2 = (nd1 + 1) % 4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2, ny2) and b[nx1][ny1] == 0:
                        q.append([nx2, ny2, num])
                # 바라보는 방향 정면
                nx1, ny1 = x + dx[d], y + dy[d]
                if inBoard(nx1, ny1) and b[x][y] == 0:
                    q.append([nx1, ny1, num])
                # 바라보는 방향에서 우측 대각선 45도
                nd1 = (d + 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1, ny1) and b2[nx1][ny1] == 0:
                    nd2 = (nd1 - 1) % 4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2, ny2) and b[nx1][ny1] == 0:
                        q.append([nx2, ny2, num])
            # 우
            elif d==2:
                # 바라보는 방향에서 좌측 대각선 45도
                nd1 = (d - 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1,ny1) and b[x][y]==0:
                    nd2=(nd1+1)%4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2,ny2) and b2[nx2][ny2]==0:
                        q.append([nx2,ny2,num])
                # 바라보는 방향 정면
                nx1,ny1=x+dx[d],y+dy[d]
                if inBoard(nx1,ny1) and b[nx1][ny1]==0:
                    q.append([nx1,ny1,num])
                # 바라보는 방향에서 우측 대각선 45도
                nd1=(d+1)%4
                nx1,ny1=x+dx[nd1],y+dy[nd1]
                if inBoard(nx1,ny1) and b[nx1][ny1]==0:
                    nd2=(nd1-1)%4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2,ny2) and b2[nx2][ny2]==0:
                        q.append([nx2,ny2,num])
            # 하
            else:
                # 바라보는 방향에서 좌측 대각선 45도
                nd1 = (d + 1) % 4
                nx1, ny1 = x + dx[nd1], y + dy[nd1]
                if inBoard(nx1,ny1) and b2[x][y]==0:
                    nd2=(nd1-1)%4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2,ny2) and b[nx2][ny2]==0:
                        q.append([nx2,ny2,num])
                # 바라보는 방향 정면
                nx1,ny1=x+dx[d],y+dy[d]
                if inBoard(nx1,ny1) and b[nx1][ny1]==0:
                    q.append([nx1,ny1,num])
                # 바라보는 방향에서 우측 대각선 45도
                nd1=(d-1)%4
                nx1,ny1=x+dx[nd1],y+dy[nd1]
                if inBoard(nx1,ny1) and b2[nx1][ny1]==0:
                    nd2=(nd1+1)%4
                    nx2, ny2 = nx1 + dx[nd2], ny1 + dy[nd2]
                    if inBoard(nx2,ny2) and b[nx2][ny2]==0:
                        q.append([nx2,ny2,num])
        for x in range(n):
            for y in range(n):
                c[x][y]+=tmp[x][y]
        flag1=0

def mix():
    global c

    tmp=[row[:] for row in c]

    for x in range(n):
        for y in range(n):
            for k in range(4):
                nx,ny=x+dx[k],y+dy[k]
                if not inBoard(nx,ny): continue
                # 좌
                if k==0:
                    if b2[x][y]==1:
                        continue
                # 상
                elif k==1:
                    if b[x][y]==1:
                        continue
                # 우
                elif k==2:
                    if b2[nx][ny]==1:
                        continue
                # 하
                else:
                    if b[nx][ny]==1:
                        continue
                dif=abs(c[x][y]-c[nx][ny])//4
                if dif==0: continue
                if c[x][y]>c[nx][ny]:
                    tmp[nx][ny]+=dif
                    tmp[x][y]-=dif
                elif c[x][y]<c[nx][ny]:
                    tmp[nx][ny]-=dif
                    tmp[x][y]+=dif
    c=tmp

def decrease():
    global c

    for x in range(0,n-1):
        if c[x][0]>0:
            c[x][0]-=1
    for y in range(0,n-1):
        if c[n-1][y]>0:
            c[n-1][y]-=1
    for x in range(1,n):
        if c[x][n-1]>0:
            c[x][n-1]-=1
    for y in range(1,n):
        if c[0][y]>0:
            c[0][y]-=1

def check():

    ok=True
    for x in range(n):
        for y in range(n):
            if a[x][y]==1 and c[x][y]<K:
                ok=False
                return ok

    return ok

time=0
while True:
    time+=1

    spread()

    mix()

    decrease()

    if check():
        break

    if time>100:
        break

if time>100:
    print(-1)
else:
    print(time)