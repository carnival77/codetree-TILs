import sys
from collections import deque
input=sys.stdin.readline

n,m,K=map(int,input().split())
a=[list(map(int,input().split())) for _ in range(n)]
b=[[0]*n for _ in range(n)]

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
    for i in range(x,x+h):
        for j in range(y,y+w):
            b[i][j]=no

def try_movement(start,d):

    q=deque()
    q.append(start)
    move=set()
    move.add(start)
    dmg=[0]*(m+1)

    while q:
        now=q.popleft()
        x,y,h,w,k=units[now]
        nx,ny=x+dx[d],y+dy[d]

        if not (nx>=0 and ny>=0 and nx+h-1<n and ny+w-1<n):return

        for i in range(nx,nx+h):
            for j in range(ny,ny+w):
                if a[i][j]==2:
                    return
                if a[i][j]==1:
                    dmg[now]+=1

        for other in units.keys():
            if other in move:continue

            ox,oy,oh,ow,ok=units[other]
            if nx+h-1<ox or ny+w-1<oy or nx>ox+oh-1 or ny>oy+ow-1:
                continue
            q.append(other)
            move.add(other)

    dmg[start]=0

    for no in move:
        x,y,h,w,k=units[no]
        if dmg[no]>=k:
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
                    b[i][j]=no

for round in range(1,K+1):
    no,d=map(int,input().split())
    if no in units.keys():
        try_movement(no,d)

ans=0
for no in units:
    ans+=(init_k[no]-units[no][4])
print(ans)