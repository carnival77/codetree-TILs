from collections import deque

dx=[-1,0,1,0]
dy=[0,-1,0,1]

n,m,K=map(int,input().split())
a=[[0]*m for _ in range(n)]
ans=0

# 출구 위치
def getExit(x,y,d):
    if d==0:
        return [x-1,y]
    elif d==1:
        return [x,y+1]
    elif d==2:
        return [x+1,y]
    else:
        return [x,y-1]


def inBoard(nx,ny):
    # if 0<=nx<n and 0<=ny<m:
    if nx<n and 0<=ny<m:
        return True
    return False

def check(x,y):
    if not inBoard(x,y):
        return False
    if a[x][y]!=0:
        return False
    return True

# 골렘 이동
def move(c,d,no):
    global a

    x,y=-1,c # 골렘 내 중앙의 정령 위치
    while True:
        # 골렘 수직 이동
        # if a[x+2][y]==0 and a[x+1][y-1]==0 and a[x+1][y+1]==0:
        if check(x+2,y) and check(x+1,y-1) and check(x+1,y+1):
            x+=1
        # 골렘 왼쪽 이동
        # elif a[x+1][y-1]==0 and a[x-1][y-1]==0 and a[x][y-2]==0 and a[x+1][y-2]==0 and a[x+2][y-1]==0:
        elif check(x+1,y-1) and check(x-1,y-1) and check(x,y-2) and check(x+1,y-2) and check(x+2,y-1):
            x+=1
            y-=1
            d=(d-1)%4
        # 골렘 오른쪽 이동
        # elif a[x+1][y+1]==0 and a[x-1][y+1]==0 and a[x][y+2]==0 and a[x+1][y+2]==0 and a[x+2][y+1]==0:
        elif check(x+1,y+1) and check(x-1,y+1) and check(x,y+2) and check(x+1,y+2) and check(x+2,y+1):
            x+=1
            y+=1
            d=(d+1)%4
        else:
            break

    # 골렘 지도에 표시
    # if a[x][y]==0 and a[x+1][y]==0 and a[x-1][y]==0 and a[x][y+1]==0 and a[x][y-1]==0:
    if check(x,y) and check(x+1,y) and check(x-1,y) and check(x,y+1) and check(x,y-1):
        a[x][y]=a[x+1][y]=a[x-1][y]=a[x][y+1]=a[x][y-1]=no
        ex, ey = getExit(x, y, d)# 출구 위치
        a[ex][ey]=-no
        return [True,x,y]
    else:
        return [False,-1,-1]

# 정령 이동
def bfs(sx,sy,no):
    global ans

    cand=[]
    q=deque()
    q.append((sx,sy))
    visit=[[False]*m for _ in range(n)]
    visit[sx][sy]=True

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny]:
                continue
            if a[nx][ny]==no or a[nx][ny]==-no:
                q.append((nx,ny))
                visit[nx][ny]=True
                cand.append(nx)
                continue
            if a[x][y]==-no and a[nx][ny]!=0 and a[nx][ny]!=no:
                q.append((nx,ny))
                visit[nx][ny]=True
                cand.append(nx)
                no=abs(a[nx][ny])

    cand.sort(reverse=True)
    return cand[0]+1

for no in range(1,K+1):
    c,d=map(int,input().split())
    c-=1

    # 골렘 이동
    res=move(c,d,no)
    inBound,x,y=res

    # 골렘 몸 일부가 숲 벗어나있는지 확인
    if inBound:
        # 정령 이동
        ans+=bfs(x,y,no)
    else:
        # 숲 초기화
        a=[[0]*m for _ in range(n)]

print(ans)