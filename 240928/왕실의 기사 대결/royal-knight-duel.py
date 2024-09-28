from collections import deque

n,m,K=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)]
b=[[0]*n for _ in range(n)]
init_hp=[None]+[0]*m
hp=[None]+[0]*m
pos=[None]*(m+1)
size=[None]*(m+1)

for no in range(1,m+1):
    x,y,h,w,k=map(int,input().split())
    x-=1
    y-=1
    pos[no]=[x,y]
    size[no]=[h,w]
    init_hp[no]=k
    hp[no]=k

    for i in range(x,x+h):
        for j in range(y,y+w):
            b[i][j]=no

#  상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def process(no,dir):
    global pos,b,hp

    # ok=True
    willMove=set()
    tmp=[[0]*n for _ in range(n)]
    q=deque()
    q.append((no,dir))

    # 이동 대상 선정
    while q:
        no,dir=q.popleft()
        willMove.add(no)
        sx,sy=pos[no]
        h,w=size[no]

        nx,ny=sx+dx[dir],sy+dy[dir]
        for x in range(nx,nx+h):
            for y in range(ny,ny+w):
                if not inBoard(x,y) or a[x][y]==2:
                    return
                    # ok=False
                    # break
                else:
                    if b[x][y]>0 and b[x][y]!=no:
                        q.append([b[x][y],dir])
        #     if ok==False:
        #         break
        # if ok==False:
        #     break

    flag1=0
    # 이동 및 데미지 입기
    for move_no in willMove:
        sx,sy=pos[move_no]
        h,w=size[move_no]
        nx,ny=sx+dx[dir],sy+dy[dir]
        pos[move_no]=[nx,ny]
        for x in range(nx,nx+h):
            for y in range(ny,ny+w):
                tmp[x][y]=move_no
                if a[x][y]==1:
                    if hp[move_no]>0 and no!=move_no:
                        hp[move_no]-=1

    b=tmp
    flag2=0

turn=0
for turn in range(1,K+1):

    no,dir=map(int,input().split())

    if hp[no]<=0:continue

    process(no,dir)

ans=0
for no in range(1,m+1):
    if hp[no]>0:
        ans+=init_hp[no]-hp[no]
print(ans)