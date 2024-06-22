from collections import deque
from itertools import combinations

n,m=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)] # 0 : 빈칸, 1 : 사람, 2 : 병원
b=[[0]*n for _ in range(n)]
ans=int(1e9)

dx=[-1,0,1,0]
dy=[0,-1,0,1]

# 사람,병원 위치 찾기
p,h=[],[]
for x in range(n):
    for y in range(n):
        if a[x][y]==2:
            h.append([x,y])
        elif a[x][y]==1:
            p.append([x,y])
            b[x][y]=1

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs(sx,sy):
    q=deque()
    q.append((sx,sy))
    d=[[-1]*n for _ in range(n)]
    d[sx][sy]=0
    cand=[]

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or d[nx][ny]!=-1:
                continue
            q.append((nx,ny))
            d[nx][ny]=d[x][y]+1
            if b[nx][ny]==2:
                return d[nx][ny]
                # cand.append(d[nx][ny])
    # cand.sort()
    # return cand[0]

# 병원들 중 m개 뽑는 경우의 수
for comb in combinations(h,m):
    res=0
    # 병원 설치
    for x,y in comb:
        b[x][y]=2
    # 각 사람 위치에서 bfs 로 제일 가까운 병원까지의 거리 탐색
    for x,y in p:
        dist=bfs(x,y)
        res+=dist
    # 병원 해체
    for x,y in comb:
        b[x][y]=0
    # 최솟값 갱신
    ans=min(ans,res)

print(ans)