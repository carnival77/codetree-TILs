from collections import deque
MAX=int(1e9)

n,K,m,c,d=map(int,input().split())

rx,ry=map(int,input().split())
rx-=1
ry-=1

pos=[None]*(m+1)
panic=[None]+[0]*m
point=[None]+[0]*m
tmp=[]

a=[[0]*n for _ in range(n)] # 산타 맵
for _ in range(m):
    no,x,y=map(int,input().split())
    x-=1
    y-=1
    a[x][y]=no
    pos[no]=[x,y]

#  상,우,하,좌 포함 8방향
dx=[-1,0,1,0,-1,1,-1,1]
dy=[0,1,0,-1,-1,1,1,-1]

def getDistance(x,y,nx,ny):
    return (x-nx)**2 + (y-ny)**2

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def interaction(sx,sy,xdir,ydir):
    global tmp

    q=deque()
    q.append((sx,sy))

    while q:
        x,y=q.popleft()
        no=a[x][y]
        nx,ny=x+xdir,y+ydir
        if inBoard(nx,ny):
            tmp[nx][ny]=no
            if a[nx][ny]>0:
                q.append((nx,ny))

def crash(sx,sy,xdir,ydir,kind):
    global a,pos,panic,tmp,point

    no=a[sx][sy]
    a[sx][sy]=0
    tmp=[[0]*n for _ in range(n)]

    if kind==1:
        z=c
    else:
        z=d

    point[no]+=z
    panic[no]=turn+1
    nx,ny=sx+xdir*z,sy+ydir*z
    if not inBoard(nx,ny):
        pos[no]=None
    else:
        tmp[nx][ny]=no
        if a[nx][ny]>0:
            interaction(nx,ny,xdir,ydir)

    for x in range(n):
        for y in range(n):
            if tmp[x][y]>0:
                a[x][y]=tmp[x][y]
                no=tmp[x][y]
                pos[no]=[x,y]
    flag1=0

def move1():
    global rx,ry

    cand=[]
    for no in range(1,m+1):
        if pos[no] is None:continue
        x,y=pos[no]
        dist=getDistance(x,y,rx,ry)
        cand.append([dist,x,y])

    cand.sort(key=lambda x:(x[0],-x[1],-x[2]))
    tx,ty=cand[0][-2],cand[0][-1]

    cand=[]
    for k in range(8):
        xdir=dx[k]
        ydir=dy[k]
        nx,ny=rx+xdir,ry+ydir
        dist=getDistance(nx,ny,tx,ty)
        cand.append([dist,[nx,ny],[xdir,ydir]])

    cand.sort()
    nx,ny=cand[0][-2]
    xdir,ydir=cand[0][-1]

    if a[nx][ny]>0:
        crash(nx,ny,xdir,ydir,1)
    rx,ry=nx,ny

def check():

    for e in pos:
        if e is not None:
            return True
    return False

def move2():
    global pos,a

    for no in range(1,m+1):
        if panic[no]>=turn or pos[no] is None:continue
        x,y=pos[no]
        cand=[]
        for k in range(4):
            xdir=dx[k]
            ydir=dy[k]
            nx,ny=x+xdir,y+ydir
            if not inBoard(nx,ny) or a[nx][ny]>0:continue
            dist=getDistance(nx,ny,rx,ry)
            cand.append([dist,k,[nx,ny],[xdir,ydir]])

        if len(cand)>0:
            cand.sort()
            nx,ny=cand[0][-2]
            xdir,ydir=cand[0][-1]
            a[x][y]=0
            a[nx][ny]=no
            pos[no]=[nx,ny]

            if (nx,ny)==(rx,ry):
                crash(nx,ny,-xdir,-ydir,2)

def getPoint():
    global point

    for no in range(1,m+1):
        if pos[no] is not None:
            point[no]+=1

turn=0
for turn in range(1,K+1):
    # 루돌프 이동
    move1()
    # 산타 존재 여부
    if not check():
        break
    # 산타 이동
    move2()
    # 산타 존재 여부
    if not check():
        break
    # 생존 산타 점수 1 획득
    getPoint()

print(*point[1:])