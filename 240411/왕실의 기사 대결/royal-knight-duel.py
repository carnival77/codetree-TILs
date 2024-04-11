import sys
from collections import deque
input=sys.stdin.readline

n,m,K=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)] # 0:빈칸, 1:함정, 2:벽

#  상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

r=[0]*m
c=[0]*m
nr=[0]*m
nc=[0]*m
h=[0]*m
w=[0]*m
k=[0]*m
init_k=[0]*m
dmg=[0]*m
moved=[False]*m

for no in range(m):
    data=list(map(int,input().split()))
    data[0]-=1
    data[1]-=1
    r[no]=data[0]
    c[no]=data[1]
    h[no]=data[2]
    w[no]=data[3]
    k[no]=data[4]
    init_k[no]=data[4]

def tryMove(now,d):

    # 이동 관련 값 현재 값 또는 0으로 초기화
    for i in range(m):
        nr[i]=r[i]
        nc[i]=c[i]
        dmg[i]=0
        moved[i]=False

    q=deque() # 위치를 옮길 기사 후보 큐
    q.append(now)
    moved[now]=True

    while q:
        me=q.popleft()
        nr[me]+=dx[d]
        nc[me]+=dy[d]

        # 이동할 곳이 범위 내인지 체크
        if not (0<=nr[me]+h[me] and nr[me]<n and 0<=nc[me]+w[me] and nc[me]<n):
            return False

        # 이동할 곳에 벽이나 함정이 있는지 체크
        for x in range(nr[me],nr[me]+h[me]):
            for y in range(nc[me],nc[me]+w[me]):
                if a[x][y]==2:
                    return False
                if a[x][y]==1:
                    dmg[me]+=1

        # 이번 기사가 위치를 옮긴 결과 이번 기사의 영역이 다른 기사의 영역과 중복될 경우,
        # 다른 기사도 위치를 옮길 후보가 되어 큐에 추가된다.
        for other in range(m):
            # 만약 이미 움직였거나 사라진 기사는 제외
            if moved[other] or k[other]<=0:continue
            # 이번 기사의 이동 결과 다른 기사와 영역이 중복되는 지 아래 4가지 경우를 통해 체크한다.
            # 아래 4가지 경우는 4가지 방향으로 이동 시 영역이 중복되지 않는 경우의 수이다.
            # 4가지 경우 모두 True 여야 이동 시 겹치지 않는다.
            # 이번 기사가
            # 1) 아래로 이동 시, 위치를 옮긴 기사의 맨 아랫 칸(a)보다 다른 기사의 맨 윗 칸(b)이 더 아래
            #    즉, a이 b보다 더 작은 숫자로 더 위에 위치하는 지 체크
            # 2) 위로 이동 시, 위치를 옮긴 기사의 맨 윗 칸(a)보다 다른 기사의 맨 아랫 칸(b)이 더 위
            #    즉, a이 b보다 더 큰 숫자로 더 아래 위치하는 지 체크
            # 3) 오른쪽으로 이동 시, 위치를 옮긴 기사의 맨 오른쪽 칸(a)보다 다른 기사의 맨 왼쪽 칸(b)이 더 오른쪽
            #    즉, a이 b보다 더 작은 숫자로 더 왼쪽에 위치하는 지 체크
            # 4) 왼쪽으로 이동 시, 위치를 옮긴 기사의 맨 왼쪽 칸(a)보다 다른 기사의 맨 오른쪽 칸(b)이 더 왼쪽
            #    즉, a이 b보다 더 큰 숫자로 더 오른쪽에 위치하는 지 체크
            if r[other]>nr[me]+h[me]-1 and nr[me]>r[other]+h[other]-1 and c[other]>nc[me]+w[me]-1 and nc[me]>c[other]+w[other]-1 : continue

            moved[other]=True
            q.append(other)

    dmg[now]=0

    return True

for _ in range(K):
    now,d=map(int,input().split())
    now-=1
    if k[now]<=0:
        continue
    if tryMove(now,d):
        for i in range(m):
            r[i]=nr[i]
            c[i]=nc[i]
            k[i]-=dmg[i]

ans=0
for no in range(m):
    if k[no]<=0:continue
    ans+=(init_k[no]-k[no])

print(ans)