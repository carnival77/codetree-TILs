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
        if not inBoard(nx,ny) or visit[nx][ny]:continue
        visit[nx][ny]=True
        dfs(nx,ny,cnt+1,s+a[nx][ny],visit)
        visit[nx][ny]=False

for x in range(n):
    for y in range(m):
        visit=[[False]*m for _ in range(n)]
        visit[x][y]=True
        dfs(x,y,1,a[x][y],visit)
        visit[x][y]=False

print(ans)