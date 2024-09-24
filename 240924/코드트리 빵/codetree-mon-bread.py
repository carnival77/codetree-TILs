from collections import deque

n,m=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)] # 베이스캠프, 편의점 맵 ( 0 = 빈칸, 1~30=편의점 번호, -1=베이스캠프, -2=출입금지 )
b=[[[] for _ in range(n)] for _ in range(n)] # 플레이어 디버깅 맵 ( 번호 배열 )
ps=[None]*(m+1) # 플레이어 위치
cs=[None]*(m+1) # 플레이어별 목표 편의점 위치
fin=[None]+[False]*m # 플레이어별 도착 여부

#  상,좌,우,하
dx=[-1,0,0,1]
dy=[0,-1,1,0]

for x in range(n):
    for y in range(n):
        if a[x][y]==1:
            a[x][y]=-1

for no in range(1,m+1):
    x,y=map(int,input().split())
    x-=1
    y-=1
    a[x][y]=no
    cs[no]=[x,y]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def getNext(no):

    sx,sy=ps[no]
    q=deque()
    q.append((sx,sy))
    dist=[[-1]*n for _ in range(n)]
    dist[sx][sy]=0
    ex,ey=cs[no]
    parent=dict()

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or dist[nx][ny]!=-1 or a[nx][ny]==-2:continue
            q.append((nx,ny))
            dist[nx][ny]=dist[x][y]+1
            parent[(nx,ny)]=(x,y)

    end=(ex,ey)
    current=end
    start=(sx,sy)
    route=[]
    while current!=start:
        route.append(current)
        current=parent[current]
    route.append(start)

    return route[-2]

def move(no):
    global ps,fin

    nx,ny=getNext(no)
    ps[no]=[nx,ny]
    if ps[no]==cs[no]:
        fin[no]=True
        return True
    return False

def check():

    if False not in fin:
        return True
    else:
        return False

def bfs(no):

    sx,sy=cs[no]
    q=deque()
    q.append((sx,sy))
    dist = [[-1] * n for _ in range(n)]
    dist[sx][sy] = 0
    cand=[]

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx, ny) or dist[nx][ny] != -1 or a[nx][ny] == -2: continue
            q.append((nx, ny))
            dist[nx][ny] = dist[x][y] + 1
            if a[nx][ny]==-1:
                cand.append([dist[nx][ny],nx,ny])

    if len(cand)>0:
        cand.sort()
        return [cand[0][1],cand[0][2]]

def enter(no):
    global a,ps

    tx,ty=bfs(no)
    ps[no]=[tx,ty]
    a[tx][ty]=-2

t=0
while True:
    t+=1
    res=[] # 편의점 도착한 사람 번호
    # 플레이어가 편의점 향해 이동
    for no in range(1,m+1):
        if fin[no] or ps[no] is None: continue
        if move(no):
            res.append(no)
    # 편의점 도착
    for no in res:
        x,y=ps[no]
        a[x][y]=-2
    # 모든 플레이어 편의점 도착 여부 체크
    if check():
        break
    # 플레이어가 자신의 목표 편의점과 가장 가까운 베이스 캠프 입장
    if t<=m:
        enter(t)

print(t)