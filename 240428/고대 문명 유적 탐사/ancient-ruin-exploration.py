from collections import deque

K,m=map(int,input().split())
n=5
a=[list(map(int,input().split())) for _ in range(n)]
b=deque(map(int,input().split()))

dx=[-1,0,1,0]
dy=[0,-1,0,1]

ans=[]
round=0
visit=[]

def rotateClockwise(a):
    return list(map(list, zip(*a[::-1])))

def rotate(tmp,x,y,k):

    part=[[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            part[i][j]=tmp[x-1+i][y-1+j]
    for t in range(k):
        part=rotateClockwise(part)
    for i in range(3):
        for j in range(3):
            tmp[x-1+i][y-1+j]=part[i][j]

    return tmp

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs(a,sx,sy,no):
    global visit

    q=deque()
    q.append((sx,sy))
    visit[sx][sy]=True
    group=[]
    group.append([sx,sy])
    cnt=1

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if inBoard(nx,ny) and not visit[nx][ny] and a[nx][ny]==no:
                q.append((nx,ny))
                visit[nx][ny]=True
                group.append([nx,ny])
                cnt+=1

    return [group,cnt]

def seize(a):
    global visit

    groups=[]
    points=0
    visit=[[False]*n for _ in range(n)]
    for no in range(1,8):
        for x in range(n):
            for y in range(n):
                if a[x][y]==no:
                    group,point=bfs(a,x,y,no)
                    if len(group)>=3:
                        groups.append(group)
                        points+=point
    if len(groups)>0:
        return [groups,points]
    else:
        return [None,-1]

def copyBoard(a):
    return [row[:] for row in a]

def find():
    global a

    cand=[]

    for x in range(1,n-1):
        for y in range(1,n-1):
            for k in range(1,4):
                tmp=copyBoard(a)
                rotated_tmp=rotate(tmp,x,y,k)
                groups,total=seize(rotated_tmp)
                if groups!=None:
                    cand.append([groups,total,x,y,k,rotated_tmp])

    if len(cand)==0:
        return [None,-1]
    else:
        cand.sort(key=lambda x:(-x[1],x[4],x[3],x[2]))
        a=cand[0][-1]
        return [cand[0][0],cand[0][1]]

def remake(groups):
    global a,b

    cand=[]
    for group in groups:
        for x,y in group:
            cand.append([x,y])
    cand.sort(key=lambda x:(x[1],-x[0]))
    for x,y in cand:
        a[x][y]=b.popleft()

def getPoint(point):
    global ans

    ans[round]+=point

def fill():
    global a,b

    pass

def process(groups,point):

    # 유물 제거 및 채우기
    remake(groups)
    # 포인트 획득
    getPoint(point)

for round in range(K):
    ans.append(0)
    # 탐사 진행
    groups,point=find()
    if groups==None:
        ans.pop()
        break
    # 유물 획득
    process(groups,point)
    # 유물 연쇄 획득
    while True:
        # res=find()
        # groups,point=res[0],res[1]
        groups,point=seize(a)
        if groups==None:
            break
        process(groups,point)

print(*ans)