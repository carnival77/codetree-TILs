n,m,h,K=map(int,input().split())

class Runaway:
    def __init__(self,no,x,y,d):
        self.no=no
        self.x=x
        self.y=y
        self.d=d

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

a=[[0]*n for _ in range(n)] # 0 : 빈 칸, 1 : 나무
b=[[[] for _ in range(n)] for _ in range(n)] # 도망자 번호 맵. 디버깅용
ax=ay=n//2 # 술래 위치
ad=3
runaways=[None] # 도망자 배열
done=[None]+[False]*m # 도망자 잡힘 여부
ans=0

for no in range(1,m+1):
    x,y,d=map(int,input().split())
    x-=1
    y-=1
    # d가 1인 경우 좌우로 움직임을, 2인 경우 상하로만 움직임
    # 좌우로 움직이는 사람은 항상 오른쪽을 보고 시작하며, 상하로 움직이는 사람은 항상 아래쪽을 보고 시작함
    if d==1:
        d=0
    elif d==2:
        d=1
    runaway=Runaway(no,x,y,d)
    runaways.append(runaway)
    b[x][y].append(no)

# 나무가 도망자와 초기에 겹쳐져 주어지는 것 역시 가능
for _ in range(h):
    x, y= map(int, input().split())
    x-=1
    y-=1
    a[x][y]=1

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

# 술래는 처음 위 방향으로 시작하여 달팽이 모양으로 움직입니다.
# 만약 끝에 도달하게 되면 다시 거꾸로 중심으로 이동하고, 다시 중심에 오게 되면 처음처럼 위 방향으로 시작하여 시계뱡향으로 도는 것을 k턴에 걸쳐 반복하게 됩니다.
# 이동 후의 위치가 만약 이동방향이 틀어지는 지점이라면, 방향을 바로 틀어줍니다.
# 만약 이동을 통해 양끝에 해당하는 위치인 (1행, 1열) 혹은 정중앙에 도달하게 된다면 이 경우 역시 방향을 바로 틀어줘야 함에 유의합니다.
def getRouteAndDirection(kind):

    route=[]
    dirs=[]

    if kind==1:
        x=y=n//2
        route.append([x, y])
        dirs.append(3)
        for size in range(3,n+1,2):
            d = 3
            x+=dx[d]
            y+=dy[d]
            d=(d+1)%4
            route.append([x,y])
            dirs.append(d)
            for d in range(4):
                loop=size-1
                if d==0:
                    loop-=1
                for i in range(loop):
                    x+=dx[d]
                    y+=dy[d]
                    route.append([x,y])
                    if i==loop-1 and d!=3:
                        d=(d+1)%4
                    dirs.append(d)
        dirs.pop()
        dirs.append(1)
    else:
        visit=[[False]*n for _ in range(n)]
        x=y=0
        d=1
        route.append([x,y])
        visit[x][y]=True
        for i in range(n*n-1):
            nx,ny=x+dx[d],y+dy[d]
            if not inBoard(nx,ny) or visit[nx][ny]:
                d=(d-1)%4
                nx, ny = x + dx[d], y + dy[d]
            x,y=nx,ny
            route.append([x,y])
            dirs.append(d)
            visit[x][y] = True
        dirs.append(3)

    return [route,dirs]

# 도망자가 움직일 때 현재 술래와의 거리가 3 이하인 도망자만 움직입니다.
# 도망자의 위치가 (x1, y1), 술래의 위치가 (x2, y2)라 했을 때 두 사람간의 거리는 |x1 - x2| + |y1 - y2|로 정의됩니다.
# 술래와의 거리가 3 이하인 도망자들은 1턴 동안 다음 규칙에 따라 움직이게 됩니다
# 현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나지 않는 경우
# 움직이려는 칸에 술래가 있는 경우라면 움직이지 않습니다.
# 움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동합니다. 해당 칸에 나무가 있어도 괜찮습니다.
# 현재 바라보고 있는 방향으로 1칸 움직인다 했을 때 격자를 벗어나는 경우
# 먼저 방향을 반대로 틀어줍니다. 이후 바라보고 있는 방향으로 1칸 움직인다 했을 때 해당 위치에 술래가 없다면 1칸 앞으로 이동합니다.
def moveRunaway():
    global b

    for r in runaways:
        if r is None: continue
        no,x,y,d=r.no,r.x,r.y,r.d
        if done[no]:continue
        dist=abs(ax-x)+abs(ay-y)
        if dist>3: continue
        nx,ny=x+dx[d],y+dy[d]
        if not inBoard(nx,ny):
            d=(d+2)%4
            r.d=d
            nx, ny = x + dx[d], y + dy[d]
        if (nx,ny)!=(ax,ay):
            b[x][y].remove(no)
            r.x,r.y=nx,ny
            b[nx][ny].append(no)

# 이동 직후 술래는 턴을 넘기기 전에 시야 내에 있는 도망자를 잡게 됩니다.
# 술래의 시야는 현재 바라보고 있는 방향을 기준으로 현재 칸을 포함하여 총 3칸입니다.
# 격자 크기에 상관없이 술래의 시야는 항상 3칸임에 유의합니다.
# 하지만 만약 나무가 놓여 있는 칸이라면, 해당 칸에 있는 도망자는 나무에 가려져 보이지 않게 됩니다
# 잡힌 도망자는 사라지게 되고, 술래는 현재 턴을 t번째 턴이라고 했을 때 t x 현재 턴에서 잡힌 도망자의 수만큼의 점수를 얻게 됩니다
def catch():
    global done,runaways,ans

    d=dirs[round]
    x,y=ax,ay

    cnt=0
    for i in range(3):
        nx,ny=x+dx[d]*i,y+dy[d]*i
        if inBoard(nx,ny) and a[nx][ny]!=1 and len(b[nx][ny])>0:
            cnt+=len(b[nx][ny])
            for rno in b[nx][ny]:
                done[rno]=True
                runaways[rno]=None
            b[nx][ny].clear()

    ans+=cnt*total

route1,dirs1=getRouteAndDirection(1)
route2,dirs2=getRouteAndDirection(2)
route,dirs=route1,dirs1

round=0
total=0
for _ in range(K):

    round += 1
    total += 1

    # 술래 사이클 방향 전환
    if round % (n*n-1) == 0:
        if (route, dirs) == (route1, dirs1):
            route, dirs = route2, dirs2
        else:
            route, dirs = route1, dirs1
        round %= (n*n-1)

    # 도망자 이동
    moveRunaway()
    # 술래 이동
    ax,ay=route[round]
    ad=dirs[round]
    # 도망자 잡기
    catch()

print(ans)