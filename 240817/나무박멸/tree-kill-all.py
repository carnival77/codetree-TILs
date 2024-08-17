n,m,K,c=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)] # 나무 맵. 빈 칸 = 0, 벽 = -1, 나무 : 1 이상
b=[[0]*n for _ in range(n)] # 제초제 맵
ans=0

#  상,하,좌,우
dx1=[-1,1,0,0]
dy1=[0,0,-1,1]

#  대각선 4방향
dx2=[-1,-1,1,1]
dy2=[-1,1,-1,1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def grow():
    global a

    tmp=[[0]*n for _ in range(n)]
    dx,dy=dx1,dy1

    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cnt=0
                for k in range(4):
                    nx,ny=x+dx[k],y+dy[k]
                    if inBoard(nx,ny) and a[nx][ny]>0:
                        cnt+=1
                tmp[x][y]+=cnt

    for x in range(n):
        for y in range(n):
            a[x][y]+=tmp[x][y]

def copyBoard(a):
    return [row[:] for row in a]

def duplicate():
    global a

    tmp=copyBoard(a)
    dx,dy=dx1,dy1

    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cnt=0
                cand=[]
                for k in range(4):
                    nx,ny=x+dx[k],y+dy[k]
                    if inBoard(nx,ny) and a[nx][ny]==0 and b[nx][ny]<year:
                        cnt+=1
                        cand.append([nx,ny])
                for nx,ny in cand:
                    tmp[nx][ny]+=a[x][y]//cnt

    a=tmp

def remove():
    global a,b,ans

    dx,dy=dx2,dy2
    cand=[]

    for x in range(n):
        for y in range(n):
            if a[x][y]>0:
                cnt=a[x][y]
                # b[x][y]=c
                pos=[]
                pos.append([x,y])
                for k in range(4):
                    for i in range(1,K+1):
                        nx,ny=x+dx[k]*i,y+dy[k]*i
                        if not inBoard(nx,ny):break
                        # b[nx][ny] = c
                        pos.append([nx,ny])
                        if a[nx][ny]>0:
                            cnt+=a[nx][ny]
                        else:
                            break
                cand.append([cnt,x,y,pos])

    if len(cand)>0:
        cand.sort(key=lambda x:(-x[0],x[1],x[2]))
        cnt=cand[0][0]
        ans+=cnt
        pos=cand[0][-1]
        for nx,ny in pos:
            b[nx][ny]=year+c
            a[nx][ny]=0

# def decrease():
#     global b
#
#     for x in range(n):
#         for y in range(n):
#             if b[x][y]>0:
#                 b[x][y]-=1

year=0
for year in range(1,m+1):

    # 성장
    grow()
    # 번식
    duplicate()
    # # 제초제 감소
    # decrease()
    # 박멸
    remove()

print(ans)