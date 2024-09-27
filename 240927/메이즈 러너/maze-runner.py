n,m,K=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)] # 0 = 빈 칸, 1~9 : 벽 내구도, -11 : 출구
b=[[[] for _ in range(n)] for _ in range(n)] # 1~10 : 참가자 번호

dist=[None]+[0]*m
leave=[None]+[False]*m

for no in range(1,m+1):
    x,y=map(int,input().split())
    x-=1
    y-=1
    b[x][y].append(no)

ex,ey=map(int,input().split())
ex-=1
ey-=1
a[ex][ey]=-1

#  상,하,좌,우
dx=[-1,1,0,0]
dy=[0,0,-1,1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def move():
    global dist,leave,b

    tmp=[[[] for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if len(b[x][y])==0:continue
            for no in b[x][y]:
                cand=[]
                distance=abs(x-ex)+abs(y-ey)
                for k in range(4):
                    nx,ny=x+dx[k],y+dy[k]
                    if not inBoard(nx,ny) or a[nx][ny]>0:continue
                    d=abs(nx-ex)+abs(ny-ey)
                    if distance>d:
                        cand.append([d,k,[nx,ny]])
                if len(cand)>0:
                    cand.sort()
                    nx,ny=cand[0][-1]
                    dist[no]+=1
                    if (nx,ny)==(ex,ey):
                        leave[no]=True
                    else:
                        tmp[nx][ny].append(no)
                else:
                    tmp[x][y].append(no)
    b=tmp

def check():

    if False not in leave:
        return True
    return False

def valid(sx,sy,size):

    ok1=False
    ok2=False
    for i in range(size):
        for j in range(size):
            if a[sx+i][sy+j]==-1:
                ok1=True
            if len(b[sx+i][sy+j])>0:
                ok2=True

    if ok1 and ok2:
        return True
    return False

def rotateClockwise(a):
    return list(map(list,zip(*a[::-1])))

def rotate():
    global a,b,ex,ey

    cand=[]
    for x in range(n):
        for y in range(n):
            max_size=min(n-x,n-y)
            for size in range(2,max_size+1):
                if valid(x,y,size):
                    cand.append([size,x,y])
    if len(cand)>0:
        cand.sort()
        size,x,y=cand[0]
        a_part=[[0]*size for _ in range(size)]
        b_part=[[[] for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                a_part[i][j]=a[x+i][y+j]
                b_part[i][j]=b[x+i][y+j][:]
                if a_part[i][j]>=1:
                    a_part[i][j]-=1
        rotated_a_part=rotateClockwise(a_part)
        rotated_b_part=rotateClockwise(b_part)
        for i in range(size):
            for j in range(size):
                a[x+i][y+j]=rotated_a_part[i][j]
                b[x+i][y+j]=rotated_b_part[i][j][:]
    flag1=0
    for x in range(n):
        for y in range(n):
            if a[x][y]==-1:
                ex,ey=x,y
    flag2=0

turn=0
for turn in range(1,K+1):

    move()
    if check():
        break
    rotate()

print(sum(dist[1:]))
print(ex+1,ey+1)