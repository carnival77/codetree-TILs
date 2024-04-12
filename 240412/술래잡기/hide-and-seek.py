import sys
input=sys.stdin.readline

class Runaway:
    def __init__(self,no,x,y,d):
        self.no=no
        self.x=x
        self.y=y
        self.d=d

n,m,h,K=map(int,input().split())
ans=0
rs=[]
alive=[True]*m
a=[[0]*n for _ in range(n)] # 나무 맵. 1 : 나무 존재, 0 : 빈 칸
b=[[[] for _ in range(n)] for _ in range(n)] # 도망자 맵

#   상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

for no in range(m):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    # 기준 : dx1,dy1 (우,하,좌,상)
    if d==1:
        d=1 # 우
    else:
        d=2 # 하
    rs.append(Runaway(no,x,y,d))
    b[x][y].append(no)

for _ in range(h):
    x,y=map(int,input().split())
    x-=1
    y-=1
    a[x][y]=1

tx,ty=n//2,n//2
td=0
kind=1

next=[[0]*n for _ in range(n)]
rev=[[0]*n for _ in range(n)]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def setDirs():
    global next,rev

    x=y=n//2
    d=0
    move_num=1

    while x or y:
        for _ in range(move_num):
            next[x][y]=d
            x,y=x+dx[d],y+dy[d]
            rev[x][y]=(d+2)%4

            if (x,y)==(0,0):
                break

        d=(d+1)%4
        if d==0 or d==2:
            move_num+=1

    next[0][0]=2
    rev[n//2][n//2]=0

def fleeMove():
    global rs,b

    for no in range(m):
        if not alive[no] or rs[no] is None:continue
        r=rs[no]
        x,y,d=r.x,r.y,r.d
        dist=abs(x-tx)+abs(y-ty)
        if dist<=3:
            nx,ny=x+dx[d],y+dy[d]
            if not inBoard(nx,ny):
                d = (d + 2) % 4
                nx, ny = x + dx[d], y + dy[d]
                r.d=d
            if (nx,ny)!=(tx,ty):
                r.x,r.y=nx,ny
                b[x][y].remove(no)
                b[nx][ny].append(no)

def getTaggerDir():

    if kind==1:
        return next[tx][ty]
    else:
        return rev[tx][ty]

def checkFacing():
    global kind

    if kind==1 and (tx,ty)==(0,0):
        kind=2
    if kind==2 and (tx,ty)==(n//2,n//2):
        kind=1

def tagMove():
    global tx,ty,td

    td=getTaggerDir()
    tx,ty=tx+dx[td],ty+dy[td]

    checkFacing()
    td = getTaggerDir()

def getScore():
    global b,alive,ans

    x,y,d=tx,ty,td
    cnt=0

    for k in range(3):
        nx,ny=x+dx[d]*k,y+dy[d]*k
        if inBoard(nx,ny) and a[nx][ny]==0 and len(b[nx][ny])>0:
            cnt+=len(b[nx][ny])
            for no in b[nx][ny]:
                alive[no]=False
                rs[no]=None
            b[nx][ny].clear()

    ans+=turn*cnt

setDirs()

for turn in range(1,K+1):
    # 도망자 이동
    fleeMove()
    # 술래 이동
    tagMove()
    # 점수 획득
    getScore()
    
print(ans)