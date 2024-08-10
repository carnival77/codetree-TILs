from itertools import product

n=4
a=[[[[0]*8 for _ in range(n)] for _ in range(n)] for _ in range(26)]
b=[]
c=[[0]*n for _ in range(n)]

#  몬스터 방향
dx1=[-1,-1,0,1,1,1,0,-1]
dy1=[0,-1,-1,-1,0,1,1,1]

# 팩맨 방향
#   상,좌,하,우
dx2=[-1,0,1,0]
dy2=[0,-1,0,1]

m,T=map(int,input().split())
sx,sy=map(int,input().split())
sx-=1
sy-=1

turn=1

for _ in range(m):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    d-=1

    a[turn][x][y][d]+=1

def duplicate():
    global a,b

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[turn][x][y][d]>0:
                    b[x][y][d]=a[turn][x][y][d]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def MonsterMove():
    global a

    dx,dy=dx1,dy1
    tmp=[[[0]*8 for _ in range(n)] for _ in range(n)]

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[turn][x][y][d]>0:
                    ok=False
                    nd=d
                    nx,ny=x+dx[nd],y+dy[nd]
                    if not inBoard(nx,ny) or (nx,ny)==(sx,sy) or c[x][y]!=0:
                        for i in range(8):
                            nd=(nd+1)%8
                            nx,ny=x+dx[nd],y+dy[nd]
                            if inBoard(nx,ny) and (nx,ny)!=(sx,sy) and c[x][y]==0:
                                ok=True
                                break
                    else:
                        ok=True
                    if ok:
                        tmp[nx][ny][nd]+=a[turn][x][y][d]
                    else:
                        tmp[x][y][d]+=a[turn][x][y][d]

    a[turn]=tmp

def copyBoard(a):
    tmp=[[[0]*8 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[x][y][d]>0:
                    tmp[x][y][d]=a[x][y][d]
    return tmp

def PanmanMove():
    global a,c,sx,sy

    dx,dy=dx2,dy2
    arr=[0,1,2,3]
    cand=[]
    for prod in product(arr,repeat=3):
        tmp=copyBoard(a[turn])
        ok=True
        prod=list(prod)
        cnt=0
        x,y=sx,sy
        for dir in prod:
            nx,ny=x+dx[dir],y+dy[dir]
            if not inBoard(nx,ny):
                ok=False
                break
            for d in range(8):
                if tmp[nx][ny][d]>0:
                    cnt+=tmp[nx][ny][d]
                    tmp[nx][ny][d]=0
            x,y=nx,ny
        if ok and cnt>0:
            cand.append([cnt,prod])

    if len(cand)>0:
        cand.sort(key=lambda x:(-x[0],x[1]))
        route=cand[0][1]
        flag=0
        for dir in route:
            nx, ny = sx + dx[dir], sy + dy[dir]
            for d in range(8):
                if a[turn][nx][ny][d]>0:
                    a[turn][nx][ny][d]=0
                    c[nx][ny]=turn+2
            sx,sy=nx,ny

def remove():
    global b

    for x in range(n):
        for y in range(n):
            if c[x][y]==turn:
                c[x][y]=0

def complete():
    global a

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if b[x][y][d]>0:
                    a[turn][x][y][d]+=b[x][y][d]

def copy():
    global a

    for x in range(n):
        for y in range(n):
            for d in range(8):
                if a[turn][x][y][d]>0:
                    a[turn+1][x][y][d]+=a[turn][x][y][d]

for turn in range(1,T+1):

    # 몬스터 복제 시도
    b=[[[0]*8 for _ in range(n)] for _ in range(n)]
    duplicate()
    # 몬스터 이동
    MonsterMove()
    # 팩맨 이동
    PanmanMove()
    # 몬스터 시체 소멸
    remove()
    # 몬스터 복제 완료
    complete()
    # 남은 몬스터 다음 턴 맵으로 이동
    copy()

ans=0
for x in range(n):
    for y in range(n):
        for d in range(8):
            ans+=a[T][x][y][d]
print(ans)