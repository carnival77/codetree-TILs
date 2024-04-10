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

#   우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

for no in range(m):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    # 기준 : dx1,dy1 (우,하,좌,상)
    if d==1:
        d=0 # 우
    else:
        d=1 # 하
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
inx=1

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def getRouteDirs(kind):
    route=[]
    dirs=[]

    if kind==1:
        x=y=n//2
        route.append([x,y])
        dirs.append(3)
        for size in range(3,n+1,2):
            x+=dx[3]
            y+=dy[3]
            route.append([x,y])
            dirs.append(0)
            for d in range(4):
                loop=size-1
                if d==0:
                    loop-=1
                for i in range(loop):
                    x+=dx[d]
                    y+=dy[d]
                    route.append([x,y])
                    # 루프의 마지막 번째 칸에서 방향 바뀜. 하지만 x=y인 칸의 경우 방향 그대로.
                    if i==loop-1:
                        if x==y and x<n//2 and y<n//2: pass
                        else:
                            d = (d + 1) % 4
                    dirs.append(d)
        dirs[-1]=1

    else:
        x=y=0
        d=1
        visit=[[False]*n for _ in range(n)]
        route.append([x,y])
        visit[x][y]=True

        for _ in range(n*n-1):
            nx=x+dx[d]
            ny=y+dy[d]
            if not inBoard(nx,ny) or visit[nx][ny]:
                d=(d-1)%4
                nx,ny=x+dx[d],y+dy[d]
            x,y=nx,ny
            visit[x][y]=True
            route.append([x,y])
            dirs.append(d)
        dirs.append(3)

    return [route,dirs]

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

def tagMove():
    global b,alive,ans,inx,tx,ty,td

    tx,ty=route[inx]
    td=dirs[inx]
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

route,dirs=getRouteDirs(kind)

for turn in range(1,K+1):

    if turn%(n**2-1)==0:
        if kind==1:kind=2
        else:kind=1
        route,dirs=getRouteDirs(kind)
        inx=0
        
    # 도망자 이동
    fleeMove()
    # 술래 이동
    tagMove()
    
    inx+=1
    
print(ans)