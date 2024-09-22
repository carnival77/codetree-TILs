from collections import deque

n=5
K,m=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)]
candidate=deque(list(map(int,input().split())))
visit=[]

dx=[-1,0,1,0]
dy=[0,1,0,-1]

points=[]

def rotateClockwise(a):
    return list(map(list,zip(*a[::-1])))

def copyBoard(a):
    return [row[:] for row in a]

def inBoard(nx,ny):
    if 0<=nx<n and 0<=ny<n:
        return True
    return False

def bfs(a,sx,sy,no):
    global visit

    q=deque()
    q.append((sx,sy))
    visit[sx][sy]=True
    cnt=1
    group=[]
    group.append([sx,sy])

    while q:
        x,y=q.popleft()
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            if not inBoard(nx,ny) or visit[nx][ny] or a[nx][ny]!=no:
                continue
            q.append((nx,ny))
            visit[nx][ny]=True
            group.append([nx,ny])
            cnt+=1

    if cnt>=3:
        return [group,cnt]
    else:
        return [None,-1]

def find(a):
    global visit

    visit=[[False]*n for _ in range(n)]
    groups=[]
    score=0
    for no in range(1,8):
        for x in range(n):
            for y in range(n):
                if a[x][y]==no and not visit[x][y]:
                    group,cnt=bfs(a,x,y,no)
                    if group is not None:
                        groups+=group
                        score+=cnt
    if score>0:
        return [groups,score]
    else:
        return [None,-1]

def search():
    
    cand=[]
    for x in range(1,n-1):
        for y in range(1,n-1):
            b=copyBoard(a)
            part=[[0]*3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    part[i][j]=b[x-1+i][y-1+j]
            for k in range(1,4):
                part=rotateClockwise(part)
                for i in range(3):
                    for j in range(3):
                        b[x-1+i][y-1+j] = part[i][j]
                group,score=find(b)
                if group is not None:
                    cand.append([score,k,y,x,group,copyBoard(b)])
    if len(cand)>0:
        cand.sort(key=lambda x:(-x[0],x[1],x[2],x[3]))
        return [cand[0][0],cand[0][-2],cand[0][-1]]
    else:
        return [None,None,None]

def remove_fill(group):
    global a

    group.sort(key=lambda x:(x[1],-x[0]))
    for x,y in group:
        a[x][y]=candidate.popleft()

def get(score):
    global point

    point+=score

def process(group,score):
    get(score)
    remove_fill(group)

for turn in range(1,K+1):
    point=0
    
    score,group,b=search()
    if group is not None:
        a=b
        process(group,score)
    else:
        break
        
    while True:
        group,score=find(a)
        if group is not None:
            process(group, score)
        else:
            break

    points.append(point)

print(*points)