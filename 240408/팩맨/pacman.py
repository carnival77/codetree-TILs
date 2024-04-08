import sys
from itertools import product
input=sys.stdin.readline

n=4
m,K=map(int,input().split())
px,py=map(int,input().split())
px-=1
py-=1
round=0

#   상,좌,하,우
dx1=[-1,0,1,0]
dy1=[0,-1,0,1]

# 8가지 방향
dx2=[-1,-1,0,1,1,1,0,-1]
dy2=[0,-1,-1,-1,0,1,1,1]

a=[[[] for _ in range(n)] for _ in range(n)]
b=[[[] for _ in range(n)] for _ in range(n)]
c=[[0]*n for _ in range(n)]

for _ in range(m):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    d-=1
    a[x][y].append(d)

def duplicate():
    global b

    for x in range(n):
        for y in range(n):
            if len(a[x][y])>0:
                for i in a[x][y]:
                    b[x][y].append(i)

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def monsterMove():
    global a

    tmp=[[[] for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if len(a[x][y])==0:continue
            for d in a[x][y]:
                nx,ny=x+dx2[d],y+dy2[d]
                nd=d
                canMove=False
                if inBoard(nx,ny) and (nx,ny)!=(px,py) and c[nx][ny]==0:
                    canMove=True
                else:
                    while True:
                        nd = (nd + 1) % 8
                        nx, ny = x + dx2[nd], y + dy2[nd]
                        if inBoard(nx,ny) and (nx,ny)!=(px,py) and c[nx][ny]==0:
                            canMove=True
                            break
                if canMove:
                    tmp[nx][ny].append(nd)
                else:
                    tmp[x][y].append(d)
    a=tmp

def copyBoard(a):
    tmp=[[[] for _ in range(n)] for _ in range(n)]

    for x in range(n):
        for y in range(n):
            if len(a[x][y])>0:
                for d in a[x][y]:
                    tmp[x][y].append(d)

    return tmp

def pacmanMove():
    global px,py,c,a

    cand=[]
    for prod in product([0,1,2,3],repeat=3):
        tmp = copyBoard(a)
        x, y = px, py
        cnt=0
        ok=True
        for d in prod:
            nx,ny=x+dx1[d],y+dy1[d]
            if not inBoard(nx,ny):
                ok=False
                break
            if len(tmp[nx][ny])>0:
                cnt+=len(tmp[nx][ny])
                tmp[nx][ny].clear()
            x,y=nx,ny
        if ok:
            cand.append([cnt,prod])

    if len(cand)==0:
        return
    cand.sort(key=lambda x:(-x[0],x[1]))
    prod=cand[0][1]
    for d in prod:
        nx,ny=px+dx1[d],py+dy1[d]
        if len(a[nx][ny])>0:
            a[nx][ny].clear()
            c[nx][ny]=round
        px,py=nx,ny
    tmp=-1

def remove():
    global c

    for x in range(n):
        for y in range(n):
            if c[x][y]!=0 and round>=c[x][y]+2:
                c[x][y]=0

def complete():
    global a,b

    for x in range(n):
        for y in range(n):
            if len(b[x][y])>0:
                for d in b[x][y]:
                    a[x][y].append(d)
                b[x][y].clear()

for round in range(1,K+1):
    # 몬스터 복제 시도
    duplicate()
    # 몬스터 이동
    monsterMove()
    # 팩맨 이동
    pacmanMove()
    # 몬스터 시체 소멸
    remove()
    # 몬스터 복제 완성
    complete()

ans=0
for x in range(n):
    for y in range(n):
        if len(a[x][y])>0:
            ans+=len(a[x][y])
print(ans)