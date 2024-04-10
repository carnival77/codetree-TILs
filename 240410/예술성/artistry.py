import sys
from collections import deque
from itertools import combinations
input=sys.stdin.readline

MAX=sys.maxsize
n=int(input())
ans=0

a=[list(map(int,input().split())) for _ in range(n)] # 보드
g=[[0]*n for _ in range(n)] # 그룹 리스트
gnum=[None] # 그룹을 이루고 있는 숫자 값 리스트
gcnt=[None] # 그룹에 속한 칸의 수 리스트
near=[] # 그룹 간 인접 정보
gn=0 # 그룹 개수

dx=[-1,0,1,0]
dy=[0,1,0,-1]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs1(sx,sy,num,gn,visit):
    global gcnt,g

    q=deque()
    q.append((sx,sy))
    visit[sx][sy]=True
    g[sx][sy]=gn
    cnt=1

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny]:continue
            if a[nx][ny]==num:
                q.append((nx,ny))
                visit[nx][ny]=True
                cnt+=1
                g[nx][ny]=gn

    gcnt.append(cnt)
    return visit

def groupCheck():
    global gnum,gn

    visit=[[False]*n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if visit[x][y]:continue
            num=a[x][y]
            gnum.append(num)
            gn+=1
            visit=bfs1(x,y,num,gn,visit)

def nearCheck():
    global near

    near=[[0]*(gn+1) for _ in range(gn+1)]

    for x in range(n):
        for y in range(n):
            g1=g[x][y]
            for k in range(4):
                nx,ny=x+dx[k],y+dy[k]
                if inBoard(nx,ny) and g[nx][ny]!=g1:
                    g2=g[nx][ny]
                    near[g1][g2]+=1

def getPoint():
    global ans

    arr=[i for i in range(1,gn+1)]
    cand=[]
    for comb in combinations(arr,2):
        g1,g2=comb
        if near[g1][g2] == 0: continue
        cand.append([g1,g2])

    points=[]
    for g1,g2 in cand:
        point = (gcnt[g1] + gcnt[g2]) * gnum[g1] * gnum[g2] * near[g1][g2]
        points.append(point)
    ans += sum(points)
    # for g1 in range(gn):
    #     for g2 in range(gn):
    #         if near[g1][g2]==0:continue
    #         point=(gcnt[g1]+gcnt[g2])*gnum[g1]*gnum[g2]*near[g1][g2]
    #         ans+=point

def copyBoard(a):
    return [row[:] for row in a]

def rotateCounterClockwise(a):
    return list(map(list,zip(*a)))[::-1]

def rotate1():
    global a

    b=copyBoard(a)
    b=rotateCounterClockwise(b)

    for x in range(n):
        for y in range(n):
            if x==n//2 or y==n//2:
                a[x][y]=b[x][y]

def rotateClockwise(a):
    return list(map(list,zip(*a[::-1])))

def rotate2():
    global a

    N=n//2

    for x in range(0,n,N+1):
        for y in range(0,n,N+1):
            b = [[0] * N for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    b[i][j]=a[x+i][y+j]
            b=rotateClockwise(b)
            for i in range(N):
                for j in range(N):
                    a[x+i][y+j]=b[i][j]

def rotate():

    # 십자 모양 반시계 방향 90도 회전
    rotate1()
    # 십자 모양 제외 4개 정사각형 90도 시계 방향 개별 회전
    rotate2()

for round in range(4):
    # 그룹 정보 파악
    groupCheck()
    # 그룹 간 인접 관계 파악
    nearCheck()
    # 예술성 점수 구하기
    getPoint()
    # 3회차까지만 진행
    if round>=3:
        break
    # 그림 회전
    rotate()

print(ans)