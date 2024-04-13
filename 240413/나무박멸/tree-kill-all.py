import sys
input=sys.stdin.readline

n,m,t,c=map(int,input().split())
# 총 나무의 그루 수는 1 이상 100 이하의 수로, 빈 칸은 0, 벽은 -1
a=[list(map(int,input().split())) for _ in range(n)]
b=[[0]*n for _ in range(n)] # 제초제 존재
ans=0

# 상하좌우
dx=[-1,0,1,0]
dy=[0,1,0,-1]
# 대각선
dx1=[-1,-1,1,1]
dy1=[-1,1,-1,1]

year=0

def copyBoard(a):
    return [row[:] for row in a]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

# 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다.
# 성장은 모든 나무에게 동시에 일어납니다.
def grow():
    global a

    tmp=copyBoard(a)

    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cnt=0
                for k in range(4):
                    nx,ny=x+dx[k],y+dy[k]
                    if inBoard(nx,ny) and a[nx][ny]>0:
                        cnt+=1
                tmp[x][y]+=cnt

    a=tmp

# 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행합니다.
# 이때 각 칸의 나무 그루 수에서 총 번식이 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식이 되며,
# 나눌 때 생기는 나머지는 버립니다.
# 번식의 과정은 모든 나무에서 동시에 일어나게 됩니다.
def duplicate():
    global a

    tmp = copyBoard(a)

    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cand=[]
                for k in range(4):
                    nx,ny=x+dx[k],y+dy[k]
                    # if inBoard(nx,ny) and a[nx][ny]==0 and b[nx][ny]<year:
                    if inBoard(nx,ny) and a[nx][ny]==0 and b[nx][ny]==0:
                        cand.append([nx,ny])
                if len(cand)>0:
                    for tx,ty in cand:
                        tmp[tx][ty]+=(a[x][y]//len(cand))
    a=tmp

# 제초제의 경우 t의 범위만큼 대각선으로 퍼지며, 벽이 있는 경우 가로막혀서 전파되지 않습니다.
# 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제를 뿌립니다.
# 나무가 없는 칸에 제초제를 뿌리면 박멸되는 나무가 전혀 없는 상태로 끝이 나지만,
# 나무가 있는 칸에 제초제를 뿌리게 되면 4개의 대각선 방향으로 k칸만큼 전파되게 됩니다.
# 단 전파되는 도중 벽이 있거나 나무가 아얘 없는 칸이 있는 경우,
# 그 칸 까지는 제초제가 뿌려지며 그 이후의 칸으로는 제초제가 전파되지 않습니다
# 만약 박멸시키는 나무의 수가 동일한 칸이 있는 경우에는 행이 작은 순서대로,
# 만약 행이 같은 경우에는 열이 작은 칸에 제초제를 뿌리게 됩니다.
def select():

    sx,sy=-1,-1
    tmp=[[0]*n for _ in range(n)]
    cand=[]
    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cnt=a[x][y]
                # point=[]
                # point.append([x,y])
                for k in range(4):
                    for i in range(1,t+1):
                        nx,ny=x+dx1[k]*i,y+dy1[k]*i
                        if not inBoard(nx,ny):
                            break
                        if a[nx][ny]<=0:
                            # point.append([nx,ny])
                            break
                        if a[nx][ny]>0:
                            cnt+=a[nx][ny]
                            # point.append([nx,ny])
                # cand.append([cnt,x,y,point])
                cand.append([cnt,x,y])
                tmp[x][y]=cnt

    if len(cand)>0:
        cand.sort(key=lambda x:(-x[0],x[1],x[2]))
        sx,sy=cand[0][1],cand[0][2]
        return [sx,sy]
    else:
        return None

# 제초제가 뿌려진 칸에는 c년만큼 제초제가 남아있다가 c+1년째가 될 때 사라지게 됩니다.
# 제초제가 뿌려진 곳에 다시 제초제가 뿌려지는 경우에는 새로 뿌려진 해로부터 다시 c년동안 제초제가 유지됩니다.
def kill(cand):
    global a,b,ans

    # cnt,sx,sy,point=cand
    sx,sy=cand

    if (sx,sy)!=(-1,-1):
        x,y=sx,sy
        b[x][y]=c
        if a[x][y]==0:
            return
        ans+=a[x][y]
        a[x][y]=0
        for k in range(4):
            for i in range(1,t+1):
                nx, ny = x + dx1[k] * i, y + dy1[k] * i
                if not inBoard(nx, ny):
                    break
                b[nx][ny]=c
                if a[nx][ny] <= 0:
                    break
                else:
                    ans+=a[nx][ny]
                    a[nx][ny]=0

    # for x,y in point:
    #     a[x][y]=0
    #     b[x][y]=c

def decrease():
    global b

    for x in range(n):
        for y in range(n):
            if b[x][y]>0:
                b[x][y]-=1

# def remove():
#     global b
#
#     for x in range(n):
#         for y in range(n):
#             if b[x][y]==year:
#                 b[x][y]=0

for year in range(m):
    # 나무 성장
    grow()
    # 나무 번식
    duplicate()
    # 제초제 뿌릴 칸 선정
    cand=select()
    # 제초제 제거
    if year>=1:
        decrease()
    # 제초제 뿌리기
    if cand is not None:
        kill(cand)

print(ans)