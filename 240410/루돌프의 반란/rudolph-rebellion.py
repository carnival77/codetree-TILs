import sys
input=sys.stdin.readline

n,m,p,c,d=map(int,input().split())
rx,ry=map(int,input().split())
rx-=1
ry-=1

a=[[0]*n for _ in range(n)]
a[rx][ry]=-1

spos=[None]*(p+1)
panic=[None]+[0]*(p)
alive=[None]+[True]*(p)
points=[None]+[0]*(p)

for _ in range(p):
    no,x,y=map(int,input().split())
    x-=1
    y-=1
    a[x][y]=no
    spos[no]=[x,y]

round=0

# 산타 방향
#   상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

# 루돌프 방향
dx1=[-1,-1,-1,0,1,1,1,0]
dy1=[-1,0,1,1,1,0,-1,-1]

# 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 선택해야 합니다.
# 만약 가장 가까운 산타가 2명 이상이라면, r 좌표가 큰 산타를 향해 돌진합니다.
# r이 동일한 경우, c 좌표가 큰 산타를 향해 돌진합니다.
def getClosest():

    cand=[]

    for no in range(1,p+1):
        if not alive[no]:continue
        x,y=spos[no]
        dist=(rx-x)**2+(ry-y)**2
        cand.append([dist,x,y,no])
    cand.sort(key=lambda x:(x[0],-x[1],-x[2]))

    return cand[0][3]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

# 루돌프와의 충돌 후 산타는 포물선의 궤적으로 이동하여 착지하게 되는 칸에서만 상호작용이 발생할 수 있습니다.
# 산타는 충돌 후 착지하게 되는 칸에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려나게 됩니다.
# 그 옆에 산타가 있다면 연쇄적으로 1칸씩 밀려나는 것을 반복하게 됩니다.
# 게임판 밖으로 밀려나오게 된 산타의 경우 게임에서 탈락됩니다.
def interaction(no,mx,my):
    global alive,spos

    x,y=spos[no]
    nx,ny=x+mx,y+my

    if not inBoard(nx,ny):
        alive[no]=False
        return
    else:
        if a[nx][ny]>0:
            interaction(a[nx][ny],mx,my)
        a[nx][ny]=no
        spos[no]=[nx,ny]

# 밀려나는 것은 포물선 모양을 그리며 밀려나는 것이기 때문에 이동하는 도중에
# 충돌이 일어나지는 않고 정확히 원하는 위치에 도달하게 됩니다.
# 만약 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락됩니다.
def crush(kind,no,mx,my):
    global panic,points,alive,spos,a

    x,y=spos[no]
    # 산타는 루돌프와의 충돌 후 기절을 하게 됩니다.
    # 현재가 k번째 턴이었다면, (k+1)번째 턴까지 기절하게 되어 (k+2)번째 턴부터 다시 정상상태가 됩니다.
    panic[no]=round+1

    # 루돌프가 움직여서 충돌이 일어난 경우, 해당 산타는 C만큼의 점수를 얻게 됩니다.
    # 이와 동시에 산타는 루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
    if kind==1:
        points[no]+=c
        nx,ny=x+mx*c,y+my*c
    # 산타가 움직여서 충돌이 일어난 경우, 해당 산타는 D만큼의 점수를 얻게 됩니다.
    # 이와 동시에 산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
    else:
        points[no]+=d
        mx,my=-mx,-my
        nx,ny=x+mx*d,y+my*d

    # 만약 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락됩니다.
    if not inBoard(nx,ny):
        alive[no]=False
        spos[no]=None
    # 만약 밀려난 칸에 다른 산타가 있는 경우 상호작용이 발생합니다.
    else:
        if a[nx][ny]>0:
            interaction(a[nx][ny],mx,my)
        a[nx][ny]=no
        spos[no]=[nx,ny]

# 루돌프는 가장 가까운 산타를 향해 1칸 돌진합니다.
# 루돌프는 상하좌우, 대각선을 포함한 인접한 8방향 중 하나로 돌진할 수 있습니다.
# (편의상 인접한 대각선 방향으로 전진하는 것도 1칸 전진하는 것이라 생각합니다.)
# 가장 우선순위가 높은 산타를 향해 8방향 중 가장 가까워지는 방향으로 한 칸 돌진합니다.
def rmove():
    global rx,ry,a

    no=getClosest() # 가장 가까운 산타 선택
    sx,sy=spos[no]
    x,y=rx,ry
    a[rx][ry]=0
    dx,dy=dx1,dy1
    next_rx,next_ry=0,0
    mx,my=0,0
    mDist=(rx-sx)**2+(ry-sy)**2

    for k in range(8):
        nx,ny=x+dx[k],y+dy[k]
        if not inBoard(nx,ny):continue
        dist=(nx-sx)**2+(ny-sy)**2
        if dist<mDist:
            mDist=dist
            next_rx,next_ry=nx,ny
            mx,my=dx[k],dy[k]

    # 산타와 루돌프가 같은 칸에 있게 되면 충돌이 발생합니다.
    if a[next_rx][next_ry]>0:
        crush(1,a[next_rx][next_ry],mx,my)
    a[next_rx][next_ry]=-1
    rx,ry=next_rx,next_ry

# 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동합니다.
# 산타는 상하좌우로 인접한 4방향 중 한 곳으로 움직일 수 있습니다.
# 이때 가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위에 맞춰 움직입니다.
def smove():
    global a,spos

    # 산타는 1번부터 P번까지 순서대로 움직입니다.
    for no in range(1,p+1):
        # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
        if not alive[no] or panic[no]>=round:continue
        x,y=spos[no]
        a[x][y]=0
        mDist=(rx-x)**2+(ry-y)**2
        next_sx,next_sy=0,0
        mx,my=0,0
        canMove=False

        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or a[nx][ny]>0: continue
            dist=(rx-nx)**2+(ry-ny)**2
            if mDist>dist:
                mDist=dist
                next_sx,next_sy=nx,ny
                mx,my=dx[k],dy[k]
                canMove=True

        if canMove:
            spos[no]=[next_sx,next_sy]
            if a[next_sx][next_sy]==-1:
                crush(2,no,mx,my)
            else:
                a[next_sx][next_sy]=no
        else:
            a[x][y]=no

def check():
    for no in range(1,p+1):
        if alive[no]:
            return False
    return True

def getAllPoint():
    global points

    for no in range(1,p+1):
        if alive[no]:
            points[no]+=1

for round in range(1,m+1):
    # 루돌프 움직임
    rmove()
    # 산타 움직임
    smove()
    # 산타 모두 탈락 여부
    if check():
        break
    # 생존 산타 1포인트 획득
    getAllPoint()

print(*points[1:])