import sys
from collections import deque
input=sys.stdin.readline

n,m=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)]
ans=0

dice=[0,1,2,3,4,5,6]
# 주사위는 항상 초기에 격자판의 1행 1열에 놓여져 있고, 처음에는 항상 오른쪽으로 움직입니다.
sx=sy=0
sd=0

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

def roll(a,d):
    b=[0]*7
    # 우
    if d == 0:
        b[1],b[2],b[3],b[4],b[5],b[6]=a[4],a[2],a[1],a[6],a[5],a[3]
    # 하
    elif d == 1:
        b[1],b[2],b[3],b[4],b[5],b[6]=a[5],a[1],a[3],a[4],a[6],a[2]
    # 좌
    elif d == 2:
        b[1], b[2], b[3], b[4], b[5], b[6]=a[3],a[2],a[6],a[1],a[5],a[4]
    # 상
    else:
        b[1], b[2], b[3], b[4], b[5], b[6]=a[2],a[6],a[3],a[4],a[1],a[5]

    return b

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def move():
    global sx,sy,sd,dice

    d=sd
    # 주사위 이동
    # 주사위를 구르면서 이동을 하기 때문에 이렇게 한 칸을 이동한 뒤에는 다음과 같이 바라보는 면이 바뀌게 될 것입니다.
    nx=sx+dx[d]
    ny=sy+dy[d]
    # 진행 도중 다음과 같이 격자판을 벗어나게 된다면, 반사되어 방향이 반대로 바뀌게 된 뒤 한 칸 움직이게 됩니다.
    if not inBoard(nx,ny):
        d=(d+2)%4
        nx,ny=sx+dx[d],sy+dy[d]
    dice = roll(dice, d)
    sx,sy=nx,ny
    sd=d

def changeDir():
    global sd

    d=sd
    # 방향 전환
    # 주사위의 아랫면이 보드의 해당 칸에 있는 숫자보다 크면 현재 진행방향에서
    # 90' 시계방향으로 회전하여 다시 이동을 진행하게 되고,
    # 주사위의 아랫면의 숫자가 더 작다면 현재 진행방향에서 90' 반시계방향으로 회전하게 되며,
    # 동일하다면 현재 방향으로 계속 진행하게 됩니다.
    x=dice[6]
    y=a[sx][sy]

    if x>y:
        d=(d+1)%4
    elif x<y:
        d=(d-1)%4
    else:
        pass

    sd=d

def getScore():
    global ans

    q=deque()
    q.append((sx,sy))
    visit=[[False]*n for _ in range(n)]
    visit[sx][sy]=True
    num=a[sx][sy]
    cnt=1

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny]:
                continue
            if a[nx][ny]==num:
                q.append((nx,ny))
                visit[nx][ny]=True
                cnt+=1

    ans+=num*cnt

for round in range(1,m+1):
    # 주사위 움직임
    move()
    # 방향 전환
    changeDir()
    # 점수 획득
    getScore()

print(ans)