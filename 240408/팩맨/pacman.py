import sys
from itertools import product
input=sys.stdin.readline

n=4
m,turn=map(int,input().split())
px,py=map(int,input().split())
px-=1
py-=1
t=0

#   상,좌,하,우
dx1=[-1,0,1,0]
dy1=[0,-1,0,1]

# 8가지 방향
dx2=[-1,-1,0,1,1,1,0,-1]
dy2=[0,-1,-1,-1,0,1,1,1]

a=[[[[0]*8 for j in range(n)] for i in range(n)] for _ in range(26)] # 몬스터 맵. t턴의 (x,y) 에 d 방향 몬스터 수
b=[[[] for _ in range(n)] for _ in range(n)] # 몬스터 시체 맵. 시체가 사라질 각각의 턴을 저장
# c=[[0]*n for _ in range(n)]

for _ in range(m):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    d-=1
    a[0][x][y][d]+=1

def duplicate():
    global a

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[t][x][y][d]==0:
                    continue
                a[t+1][x][y][d]+=a[t][x][y][d]

def canMove(nx,ny):
    if inBoard(nx,ny) and (nx,ny)!=(px,py) and len(b[nx][ny])==0:
        return True
    return False

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def monsterMove():
    global a

    tmp=[[[0]*8 for j in range(n)] for i in range(n)]
    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[t][x][y][d]==0:continue
                nx,ny=x+dx2[d],y+dy2[d]
                nd=d
                ok=False
                if canMove(nx,ny):
                    ok=True
                else:
                    for _ in range(7):
                        nd = (nd + 1) % 8
                        nx, ny = x + dx2[nd], y + dy2[nd]
                        if canMove(nx,ny):
                            ok=True
                            break
                if ok:
                    tmp[nx][ny][nd]+=a[t][x][y][d]
                else:
                    tmp[x][y][d]+=a[t][x][y][d]
    a[t]=tmp

def copyBoard(a):
    tmp=[[[[0]*8 for j in range(n)] for i in range(n)] for _ in range(26)]

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[t][x][y][d]==0:continue
                tmp[t][x][y][d]=a[t][x][y][d]

    return tmp

def pacmanMove():
    global px,py,b,a

    cand=[]
    for prod in product([0,1,2,3],repeat=3):
        tmp = copyBoard(a)
        x, y = px, py
        cnt=0
        ok=True
        for dir in prod:
            nx,ny=x+dx1[dir],y+dy1[dir]
            if not inBoard(nx,ny):
                ok=False
                break
            for d in range(8):
                if tmp[t][nx][ny][d]!=0:
                    cnt+=tmp[t][nx][ny][d]
                    tmp[t][nx][ny][d]=0
            x,y=nx,ny
        if ok:
            cand.append([cnt,prod])

    if len(cand)==0:
        return
    cand.sort(key=lambda x:(-x[0],x[1]))
    prod=cand[0][1]
    for dir in prod:
        nx,ny=px+dx1[dir],py+dy1[dir]
        for d in range(8):
            if a[t][nx][ny][d]!=0:
                a[t][nx][ny][d]=0
                if t not in b[nx][ny]:
                    b[nx][ny].append(t)
        px,py=nx,ny

def remove():
    global b

    for x in range(n):
        for y in range(n):
            if len(b[x][y])==0:continue
            if t-2 in b[x][y]:
                b[x][y].remove(t-2)

def add():
    global a

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[t][x][y][d]==0:continue
                a[t+1][x][y][d]+=a[t][x][y][d]

for t in range(turn):
    # 몬스터 복제 시도
    duplicate()
    # 몬스터 이동
    monsterMove()
    # 팩맨 이동
    pacmanMove()
    # 몬스터 시체 소멸
    remove()
    # 이번 턴 생존 몬스터 다음 턴에도 추가
    add()

ans=0
for x in range(n):
    for y in range(n):
        for d in range(8):
            if a[turn][x][y][d]==0:continue
            ans+=a[turn][x][y][d]

print(ans)