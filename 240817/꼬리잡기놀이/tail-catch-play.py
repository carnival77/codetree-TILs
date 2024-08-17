from collections import deque

n,m,K=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)] # 0=빈칸, 1=머리사람, 2=나머지, 3=꼬리사람, 4=이동선
b=[[0]*n for _ in range(n)] # 팀 이동선 구분
teams=[None]*(m+1) # 팀별 데크 리스트. 각 팀별 0번째 인덱스가 머리사람, 마지막 인덱스가 꼬리사람
visit=[[False]*n for _ in range(n)]

ans=0

dx=[-1,1,0,0]
dy=[0,0,-1,1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs(no,sx,sy):
    global b,teams,visit

    b[sx][sy]=no
    visit[sx][sy]=True
    q=deque()
    q.append((sx,sy))

    team=deque()
    head,tail=None,None

    if a[sx][sy]==1:
        head=[sx,sy]
    elif a[sx][sy]==2:
        team.append([sx,sy])
    elif a[sx][sy]==3:
        tail=[sx,sy]

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or a[nx][ny]==0 or visit[nx][ny]:continue
            q.append((nx,ny))
            visit[nx][ny]=True
            b[nx][ny]=no
            if a[nx][ny]==1:
                head=[nx,ny]
            elif a[nx][ny]==2:
                team.append([nx,ny])
            elif a[nx][ny]==3:
                tail=[nx,ny]

    team.appendleft(head)
    team.append(tail)
    teams[no]=team

def init():

    no=1
    for x in range(n):
        for y in range(n):
            if a[x][y]>0 and not visit[x][y]:
                bfs(no,x,y)
                no+=1

def getNext(kind,x,y,no):

    if kind==1:
        for k in range(4):
            nx, ny = x + dx[k], y + dy[k]
            if not inBoard(nx, ny): continue
            if b[nx][ny] == no and 3 <= a[nx][ny] <= 4:
                return [nx,ny]

    elif kind==3:
        for k in range(4):
            nx, ny = x + dx[k], y + dy[k]
            if not inBoard(nx, ny): continue
            if b[nx][ny]==no and 1<=a[nx][ny]<=2:
                return [nx,ny]

def move():
    global teams,b,a

    for no in range(1,m+1):
        team=teams[no]
        if team is None: continue

        new_team=deque()

        head=team[0]
        tail=team[-1]
        hx,hy=head
        tx,ty=tail

        # 머리, 꼬리 다음 이동 위치 구하기
        nhx,nhy=getNext(1,hx,hy,no)
        ntx, nty = getNext(3, tx, ty, no)

        # 중간(나머지) 이동
        for x,y in list(team)[:-2]:
            new_team.append([x,y])

        # 꼬리 이동
        a[ntx][nty]=3
        a[tx][ty]=4
        new_team.append([ntx,nty])

        # 머리 이동
        a[nhx][nhy]=1
        a[hx][hy]=2
        new_team.appendleft([nhx,nhy])

        teams[no]=new_team

def throw(round):

    R=round%(4*n)

    if 1<=R<=n:
        x=R-1
        for y in range(n):
            if 1<=a[x][y]<=3:
                return [True,x,y]
    elif n+1<=R<=2*n:
        y=R%(n+1)-1
        for x in range(n-1,-1,-1):
            if 1 <= a[x][y] <= 3:
                return [True, x, y]
    elif 2*n+1<=R<=3*n:
        R=R%(2*n+1)
        x=(n-1)-R
        for y in range(n-1,-1,-1):
            if 1 <= a[x][y] <= 3:
                return [True, x, y]
    else:
        R = R % (3 * n + 1)
        y=(n-1)-R
        for x in range(n):
            if 1 <= a[x][y] <= 3:
                return [True, x, y]

    return [False,-1,-1]

def process(sx,sy):
    global ans,teams,a

    no=b[sx][sy]
    team=teams[no]
    ans+=(team.index([sx,sy])+1)**2
    team.reverse()
    teams[no]=team

    # 방향 전환 맵에 반영
    head=team[0]
    tail=team[-1]
    hx,hy=head
    tx,ty=tail
    a[hx][hy]=1
    a[tx][ty]=3

round=0
# 팀 파악
init()

for round in range(1,K+1):

    # 팀 이동
    move()
    # 공 던지기
    res=throw(round)
    ok,sx,sy=res
    # 공 맞으면
    if ok:
        # 점수 획득 및 해당 팀 방향 전환
        process(sx,sy)

print(ans)