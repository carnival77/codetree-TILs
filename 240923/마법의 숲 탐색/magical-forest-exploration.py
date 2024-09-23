from collections import deque

n,m,K=map(int,input().split())
N=n+3
a=[[0]*m for _ in range(N)]
answer=0

#  상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

def insert(no,sx,sy,d):
   global a

   a[sx][sy]=a[sx+1][sy]=a[sx][sy-1]=a[sx][sy+1]=a[sx-1][sy]=no
   if d==0:
       a[sx-1][sy]=-no
   elif d==1:
       a[sx][sy+1]=-no
   elif d==2:
       a[sx+1][sy]=-no
   else:
       a[sx][sy-1]=-no

def inBoard(nx,ny):
    if 0<=nx<N and 0<=ny<m:
        return True
    return False

def valid(nx,ny):
    if inBoard(nx,ny) and a[nx][ny]==0:
        return True
    return False

def move1():
    global sx,sy

    # 아래로 한 칸
    if valid(sx+1,sy-1) and valid(sx+1,sy+1) and valid(sx+2,sy):

        a[sx+2][sy]=a[sx+1][sy]
        a[sx+1][sy-1]=a[sx][sy-1]
        a[sx+1][sy]=a[sx][sy]
        a[sx+1][sy+1]=a[sx][sy+1]
        a[sx][sy]=a[sx-1][sy]

        a[sx][sy-1]=a[sx-1][sy]=a[sx][sy+1]=0

        sx+=1

        return True
    # 왼쪽으로 회전하여 아래로 한 칸
    if valid(sx-1,sy-1) and valid(sx,sy-2) and valid(sx+1,sy-1) and valid(sx+1,sy-2) and valid(sx+2,sy-1):

        a[sx+2][sy-1]=a[sx][sy-1]
        a[sx+1][sy-1]=a[sx][sy]
        a[sx+1][sy-2]=a[sx-1][sy]
        a[sx][sy-1]=a[sx][sy+1]

        a[sx][sy]=a[sx-1][sy]=a[sx][sy+1]=0

        sx+=1
        sy-=1

        return True
    # 오른쪽으로 회전하여 아래로 한 칸
    if valid(sx-1,sy+1) and valid(sx,sy+2) and valid(sx+1,sy+1) and valid(sx+1,sy+2) and valid(sx+2,sy+1):

        a[sx+2][sy+1]=a[sx][sy+1]
        a[sx+1][sy+1]=a[sx][sy]
        a[sx+1][sy+2]=a[sx-1][sy]
        a[sx][sy+1]=a[sx][sy-1]

        a[sx][sy]=a[sx-1][sy]=a[sx][sy-1]=0

        sx+=1
        sy+=1

        return True

    return False

def check():

    for x in range(3):
        for y in range(m):
            if a[x][y]!=0:
                return True

    return False

def remove():
    global a

    for x in range(N):
        for y in range(m):
            a[x][y]=0

def move2():
    global answer

    q=deque()
    q.append((sx,sy))
    visit=[[False]*m for _ in range(N)]
    visit[sx][sy]=True
    ex=sx

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny] or a[nx][ny]==0:continue
            if abs(a[nx][ny])==abs(a[x][y]) or a[x][y]<0:
                q.append((nx,ny))
                visit[nx][ny]=True
                if ex<nx:ex=nx
    answer+=ex-2

for no in range(1,K+1):
    c,d=map(int,input().split())
    sx=1
    sy=c-1

    insert(no,sx,sy,d)
    flag1=0
    while True:
        ok1=move1()
        if ok1:
            continue
        else:
            ok2=check()
            if ok2:
                remove()
            else:
                move2()
            break

print(answer)