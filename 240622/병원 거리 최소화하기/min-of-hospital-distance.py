import sys
from itertools import combinations
input=sys.stdin.readline

MAX=int(1e9)

n,m=map(int,input().split())

a=[list(map(int,input().split())) for _ in range(n)]

ans=MAX

house=[]
chicken=[]

for x in range(n):
    for y in range(n):
        if a[x][y]==1:
            house.append([x,y])
        elif a[x][y]==2:
            chicken.append([x,y])

for comb in combinations(chicken,m):
    res=0
    for hx,hy in house:
        min_d=MAX
        for cx,cy in comb:
            d=abs(hx-cx)+abs(hy-cy)
            min_d=min(d,min_d)
        res+=min_d
    ans=min(ans,res)

print(ans)