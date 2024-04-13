import sys
from collections import deque
input=sys.stdin.readline

n,m,K=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)]
b=[[0]*n for _ in range(n)]

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

ans=0
team_no=5
teams=dict()
round=0
visit=[[False]*n for _ in range(n)]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs(sx,sy,team_no):
    global visit,b,teams

    q=deque()
    q.append((sx,sy))
    visit[sx][sy]=True
    b[sx][sy]=team_no
    team=deque()
    team.append([sx,sy])

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny]:continue
            if a[nx][ny]==2 or (a[nx][ny]==3 and (sx,sy)!=(x,y)):
                q.append((nx,ny))
                visit[nx][ny]=True
                team.append([nx,ny])
                b[nx][ny]=team_no

    teams[team_no]=team

def init():
    global visit,team_no

    for x in range(n):
        for y in range(n):
            if not visit[x][y] and a[x][y]==1:
                bfs(x,y,team_no)
                team_no+=1

def move():
    global teams,a,b

    for no,team in teams.items():
        # 꼬리 처리
        tx,ty=team.pop()
        a[tx][ty]=4
        b[tx][ty]=0
        # 새로 꼬리 삼기
        x,y=team[-1]
        a[x][y]=3
        # 머리 처리
        sx,sy=team[0]
        a[sx][sy]=2
        b[sx][sy]=no
        for k in range(4):
            nx,ny=sx+dx[k],sy+dy[k]
            if not inBoard(nx,ny):continue
            if a[nx][ny]==4:
                team.appendleft([nx,ny])
                a[nx][ny]=1
                b[nx][ny]=no
                break
        teams[no]=team

def throw():

    dir=(round//n)%4
    offset=round%4

    if dir==0:
        sx=offset
        sy=0
    elif dir==1:
        sx=n-1
        sy=offset
    elif dir==2:
        sx=n-1-offset
        sy=n-1
    else:
        sx=0
        sy=n-1-offset

    return [dir,sx,sy]

def getScore(res):
    global ans,teams,a

    dir,sx,sy=res

    for i in range(n):
        nx,ny=sx+dx[dir]*i,sy+dy[dir]*i
        if b[nx][ny]>=5:
            team_no=b[nx][ny]
            team=teams[team_no]
            ans+=(team.index([nx,ny])+1)**2
            team.reverse()
            teams[team_no]=team
            for no,[x,y] in enumerate(team):
                if no==0:
                    a[x][y]=1
                elif no==len(team)-1:
                    a[x][y]=3
                else:
                    a[x][y]=2
            break

init()

for round in range(K):
    # 이동
    move()
    # 공 던지기
    res=throw()
    # 점수 얻고 팀 조작
    getScore(res)

print(ans)