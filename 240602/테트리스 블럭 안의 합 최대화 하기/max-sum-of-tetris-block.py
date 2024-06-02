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

for i in range(n):
    for j in range(m):
        visit=[[0]*m for _ in range(n)]
        visit[i][j]=1
        dfs(i,j,1,a[i][j],visit)
        visit[i][j]=0
        if j + 2 < m:
            temp = a[i][j] + a[i][j + 1] + a[i][j + 2]
            if i - 1 >= 0:
                temp2 = temp + a[i - 1][j + 1]
                if ans < temp2:
                    ans = temp2
            if i + 1 < n:
                temp2 = temp + a[i + 1][j + 1]
                if ans < temp2:
                    ans = temp2
        if i + 2 < n:
            temp = a[i][j] + a[i + 1][j] + a[i + 2][j]
            if j + 1 < m:
                temp2 = temp + a[i + 1][j + 1]
                if ans < temp2:
                    ans = temp2
            if j - 1 >= 0:
                temp2 = temp + a[i + 1][j - 1]
                if ans < temp2:
                    ans = temp2

print(ans)