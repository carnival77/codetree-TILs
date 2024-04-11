import sys
input=sys.stdin.readline
from collections import deque

n,m,K=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)] # 체스판
b=[[0]*n for _ in range(n)] # 디버깅용 기사맵

#  상,우,하,좌
dx=[-1,0,1,0]
dy=[0,1,0,-1]

units=dict()
init_k=[0]*(m+1)

for no in range(1,m+1):
    x,y,h,w,k=map(int,input().split())
    x-=1
    y-=1
    units[no]=[x,y,h,w,k]
    init_k[no]=k
    for i in range(x, x + h):
        for j in range(y, y + w):
            b[i][j] = no

def try_movement(start,d):

    q=deque()
    q.append(start)
    dmg = [0] * (m + 1)
    move=set() # 움직일 기사 후보
    move.add(start)

    while q:
        now=q.popleft()
        x,y,h,w=units[now][:4]
        nx,ny=x+dx[d],y+dy[d]

        # 기사가 이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없게 됩니다
        # 범위 체크
        if not (nx>=0 and nx+h-1<n and ny>=0 and ny+w-1<n): return
        # 벽과 함정 체크
        for i in range(nx,nx+h):
            for j in range(ny,ny+w):
                if a[i][j]==2:
                    return
                # 각 기사들은 해당 기사가 이동한 곳에서 w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해를 입게 됩니다.
                if a[i][j]==1:
                    dmg[now]+=1

        # 연쇄적으로 다른 기사를 밀치는 지 체크하고, 밀치는 기사는 큐와 움직일 기사 후보에 삽입
        for other in units.keys():
            # 이미 움직인 기사 제외
            if other in move:
                continue
            ox,oy,oh,ow=units[other][:4]

            # 겹치지 않는 경우
            if nx>ox+oh-1 or ny>oy+ow-1 or nx+h-1<ox or ny+w-1<oy:
                continue
            move.add(other)
            q.append(other)

    # 명령을 받은 기사는 피해를 입지 않으며
    dmg[start]=0

    # 움직일 기사 후보 내 기사들을 움직이고 정보 업데이트
    for no in move:
        x,y,h,w,k=units[no]
        # 각 기사마다 피해를 받은 만큼 체력이 깎이게 되며, 현재 체력 이상의 대미지를 받을 경우 기사는 체스판에서 사라지게 됩니다
        # 기사들은 모두 밀린 이후에 대미지를 입게 됩니다.
        if k<=dmg[no]:
            units.pop(no)
        else:
            nx,ny=x+dx[d],y+dy[d]
            units[no]=[nx,ny,h,w,k-dmg[no]]

    b = [[0] * n for _ in range(n)]
    for no in range(1,m+1):
        if no in units.keys():
            x,y,h,w,k=units[no]
            for i in range(x,x+h):
                for j in range(y,y+w):
                    b[i][j]=no+1

for round in (1,K+1):
    no,d=map(int,input().split())

    # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 됩니다.
    if no in units.keys():
        try_movement(no,d)

ans=0
for no in units:
    ans+=init_k[no]-units[no][4]
print(ans)