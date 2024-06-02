n,m=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)]
ans=0

#  우,하,좌,상
dx=[0,1,0,-1]
dy=[1,0,-1,0]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<m:
        return True
    return False

def dfs(sx,sy,cnt,s,visit):
    global ans

    if cnt==4:
        ans=max(ans,s)
        return

    for k in range(4):
        nx,ny=sx+dx[k],sy+dy[k]
        if not inBoard(nx,ny) or visit[nx][ny]==1:continue
        visit[nx][ny]=1
        dfs(nx,ny,cnt+1,s+a[nx][ny],visit)
        visit[nx][ny]=0

def simulate(x,y,s):
    global ans

    if inBoard(x-1,y) and inBoard(x+1,y):
        ns=s+a[x-1][y]+a[x+1][y]
        if inBoard(x,y+1):
            ans=max(ans,ns+a[x][y+1])
        if inBoard(x,y-1):
            ans=max(ans,ns+a[x][y-1])

    if inBoard(x,y-1) and inBoard(x,y+1):
        ns=s+a[x][y-1]+a[x][y+1]
        if inBoard(x+1,y):
            ans=max(ans,ns+a[x+1][y])
        if inBoard(x-1,y):
            ans=max(ans,ns+a[x-1][y])

for x in range(n):
    for y in range(m):
        visit=[[0]*m for _ in range(n)]
        visit[x][y]=1
        dfs(x,y,1,a[x][y],visit)
        visit[x][y]=0
        simulate(x,y,a[x][y])

print(ans)