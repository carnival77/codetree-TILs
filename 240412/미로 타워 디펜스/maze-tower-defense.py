import sys
input=sys.stdin.readline

n,m=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)]

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

sx=sy=n//2
a[sx][sy]=-1

ans=0
b=[]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def getRoute():

    route=[]
    x=y=0
    route.append([x,y])
    d=0
    visit=[[False]*n for _ in range(n)]
    visit[x][y]=True
    for _ in range(n**2-1):
        nx,ny=x+dx[d],y+dy[d]
        if not inBoard(nx,ny) or visit[nx][ny]:
            d=(d+1)%4
            nx, ny = x + dx[d], y + dy[d]
        route.append([nx,ny])
        visit[nx][ny]=True
        x,y=nx,ny
    route.pop()
    route.reverse()

    return route

def attack(d,p):
    global a,ans

    for i in range(1,p+1):
        x,y=sx+dx[d]*i,sy+dy[d]*i
        ans+=a[x][y]
        a[x][y]=0

def insert():
    global a

    tmp=[[0]*n for _ in range(n)]

    for (x,y),no in zip(route,b):
        tmp[x][y]=no

    a=tmp

def move():
    global b

    tmp=[]
    for x,y in route:
        if a[x][y]!=0:
            tmp.append(a[x][y])
    b=tmp

    insert()

def check():
    tmp=b[:]

    tmp.append(0)
    cnt=1
    start=tmp[0]
    startInx=0
    cand=dict()

    for inx,no in enumerate(tmp):
        if inx==0:continue
        if start!=no:
            start=no
            startInx=inx
            cnt=1
        else:
            cnt += 1
            if cnt>=4:
                cand[startInx]=cnt
                # cand.append([startInx,cnt])

    if len(cand)>0:
        return [True,cand]

    return [False,None]

def delete(cand):
    global ans,b

    for startInx in cand:
        cnt=cand[startInx]
        no=b[startInx]

        for i in range(cnt):
            b[startInx+i]=0
        ans+=no*cnt

    tmp=[]
    for no in b:
        if no!=0:
            tmp.append(no)
    b=tmp

def duplicate():
    global b

    c=b[:]
    c.append(0)
    tmp=[]
    cnt=1
    start=b[0]

    for inx,no in enumerate(c):
        if inx==0:continue
        if start!=no:
            tmp.append(cnt)
            tmp.append(start)
            start=no
            cnt=1
        else:
            cnt+=1

    b=tmp

route=getRoute()
for round in range(1,m+1):
    d,p=map(int,input().split())

    # 공격
    attack(d,p)
    # 몬스터 이동
    move()
    # 삭제 가능한 몬스터 모두 삭제
    ok=False
    while True:
        canDelete,cand=check()
        if canDelete:
            delete(cand)
            ok=True
            insert() # b의 몬스터 정보 a에 넣기
        else:
            break
    # # b의 몬스터 정보 a에 넣기
    # if ok:
    #     insert()
    # 몬스터 복제
    duplicate()
    # b의 몬스터 정보 a에 넣기
    insert()

print(ans)