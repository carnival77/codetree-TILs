class Player:
    def __init__(self,no,x,y,d,s,g):
        self.no=no
        self.x=x
        self.y=y
        self.d=d
        self.s=s # 능력치
        self.g=g # 공격력

n,m,K=map(int,input().split())

a=[[[] for _ in range(n)] for _ in range(n)] # 총 맵
b=[[[] for _ in range(n)] for _ in range(n)] # 플레이어 객체 맵
c=[[[] for _ in range(n)] for _ in range(n)] # 플레이어 디버깅 맵 ( 번호 배열 )
gs=[None]+[0]*m # 플레이어 디버깅용 공격력 배열
point=[None]+[0]*m # 포인트
ps=[None] # 플레이어 배열

init=[list(map(int,input().split())) for _ in range(n)] # 초기 주어진 총
for x in range(n):
    for y in range(n):
        if init[x][y]==0:continue
        a[x][y].append(init[x][y])

#  상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

for no in range(1,m+1):
    x,y,d,s=map(int,input().split())
    x-=1
    y-=1
    p=Player(no, x, y, d, s, 0)
    ps.append(p)
    b[x][y].append(p)
    c[x][y].append(no)

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def leave(p):
    global a,gs

    if p.g>0:
        x,y,gun=p.x,p.y,p.g
        a[x][y].append(gun)
        p.g=0
        gs[p.no]=0

def get(p):
    global a,gs

    leave(p)

    x,y=p.x,p.y
    guns=a[x][y]
    if len(guns)>0:
        guns.sort(reverse=True)
        gun=guns[0]
        p.g=gun
        gs[p.no]=gun
        a[x][y].remove(gun)

def fight(p1,p2):
    global point

    winner,loser=None,None

    s1,g1,s2,g2=p1.s,p1.g,p2.s,p2.g
    sum1,sum2=s1+g1,s2+g2

    if sum1>sum2:
        winner,loser=p1,p2
    elif sum1<sum2:
        winner,loser=p2,p1
    else:
        if s1>s2:
            winner, loser = p1, p2
        elif s1<s2:
            winner, loser = p2, p1
    dif = abs(sum1 - sum2)
    point[winner.no] += dif

    return [winner,loser]

round=0
for round in range(1,K+1):
    # 이동
    for p in ps[1:]:
        no,x,y,d,g=p.no,p.x,p.y,p.d,p.g
        nx,ny=x+dx[d],y+dy[d]
        if not inBoard(nx,ny):
            nd=(d+2)%4
            p.d=nd
            nx, ny = x + dx[nd], y + dy[nd]
        # 이동
        p.x, p.y = nx, ny
        b[nx][ny].append(p)
        b[x][y].remove(p)
        c[nx][ny].append(no)
        c[x][y].remove(no)
        flag1=0
        # 이동할 칸에 플레이어 X
        if len(b[nx][ny])==1:
            # 총 획득
            get(p)
        # 이동할 칸에 플레이어 O
        if len(b[nx][ny])==2:
            p1,p2=b[nx][ny]
            winner,loser=fight(p1,p2)
            # 패배자 활동
            leave(loser)
            lnx,lny=nx+dx[loser.d],ny+dy[loser.d]
            if not inBoard(lnx,lny) or len(b[lnx][lny])>=1:
                for _ in range(4):
                    loser.d=(loser.d+1)%4
                    lnx, lny = nx + dx[loser.d], ny + dy[loser.d]
                    if inBoard(lnx,lny) and len(b[lnx][lny])==0:
                        break
            # 패배자 이동
            loser.x,loser.y=lnx,lny
            b[lnx][lny].append(loser)
            b[nx][ny].remove(loser)
            c[lnx][lny].append(loser.no)
            c[nx][ny].remove(loser.no)
            flag2=0
            # 패배자 총 획득
            get(loser)
            # 승리자 활동
            get(winner)

print(*point[1:])