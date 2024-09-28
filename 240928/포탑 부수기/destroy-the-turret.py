from collections import deque

n,m,K=map(int,input().split()) # 4≤N,M≤10, 1≤K≤1,000

a=[list(map(int,input().split())) for _ in range(n)] # 포탑 맵. 0 = 부서진 포탑, 1 이상 : 생존 포탑 공격력
b=[[0]*m for _ in range(n)] # 공격 시점 맵
c=[[0]*m for _ in range(n)] # 공격 관여 시점 맵

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

#  8방향
dx1=[0,1,0,-1,1,-1,1,-1]
dy1=[1,0,-1,0,1,1,-1,-1]

ax,ay=-1,-1 # 공격자
tx,ty=-1,-1 # 공격 대상
damage=0

# def selectAttacker():
def select():
    global ax,ay,tx,ty

    cand=[]
    for x in range(n):
        for y in range(m):
            if a[x][y]==0:continue
            cand.append([a[x][y],b[x][y],x+y,y,x])

    cand.sort(key=lambda x:(x[0],-x[1],-x[2],-x[3]))
    ax=cand[0][-1]
    ay=cand[0][-2]
    a[ax][ay]+=n+m
    tx,ty=cand[-1][-1],cand[-1][-2]

# def selectTarget():
#     global tx,ty
# 
#     cand=[]
#     for x in range(n):
#         for y in range(m):
#             if a[x][y] == 0 or (x,y)==(ax,ay): continue
#             cand.append([a[x][y],b[x][y],x+y,y,x])
# 
#     cand.sort(key=lambda x: (-x[0], x[1], x[2], x[3]))
#     tx = cand[0][-1]
#     ty = cand[0][-2]

def outBound(nx,ny):

    if 0<=nx<n and 0<=ny<m:
        return [nx,ny]
    else:
        if ny>m-1:
            ny=0
        if ny<0:
            ny=m-1
        if nx>n-1:
            nx=0
        if nx<0:
            nx=n-1

    return [nx,ny]

def getRoute():

    canReach=False
    q=deque()
    q.append((ax,ay))
    visit=[[False]*m for _ in range(n)]
    visit[ax][ay]=True
    parent=dict()

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=outBound(x+dx[k],y+dy[k])
            if a[nx][ny]==0 or visit[nx][ny]: continue
            q.append((nx,ny))
            visit[nx][ny]=True
            parent[(nx,ny)]=(x,y)
            if (nx,ny)==(tx,ty):
                canReach=True

    if canReach:
        start=(ax,ay)
        end=(tx,ty)
        current=end
        route=[]
        while current!=start:
            route.append(current)
            current=parent[current]
        route.append(start)
        route.reverse()

        return route

    else:
        return None

def laser():
    global a,c

    route=getRoute()
    if route is None:
        return False

    for x,y in route[1:-1]:
        a[x][y]-=damage//2
        c[x][y]=turn

    return True

def canon():
    global a,c

    for k in range(8):
        nx,ny=outBound(tx+dx1[k],ty+dy1[k])
        if a[nx][ny]==0 or (nx,ny)==(ax,ay):continue
        a[nx][ny]-=damage//2
        c[nx][ny]=turn

def attack():
    global a,b,c,damage

    b[ax][ay]=turn
    c[ax][ay]=turn
    damage=a[ax][ay]
    a[tx][ty]-=damage
    c[tx][ty]=turn

    ok=laser()
    if not ok:
        canon()

def check():

    cnt=0
    for x in range(n):
        for y in range(m):
            if a[x][y]>0:
                cnt+=1
    if cnt==1:
        return True
    else:
        return False

def remove():
    global a

    for x in range(n):
        for y in range(m):
            if a[x][y]<0:
                a[x][y]=0

def fix():
    global a

    for x in range(n):
        for y in range(m):
            if c[x][y]!=turn and a[x][y]>0:
                a[x][y]+=1

turn=0
for turn in range(1,K+1):
    # 공격자, 공격 대상 선정
    select()
    # selectAttacker()
    # 공격 대상 선정
    # selectTarget()
    # 공격
    attack()
    # 포탑 1개 남았는지 확인
    if check():
        break
    # 부서진 포탑 체크
    remove()
    # 포탑 정비
    fix()

answer=0
for x in range(n):
    for y in range(m):
        answer=max(answer,a[x][y])
print(answer)