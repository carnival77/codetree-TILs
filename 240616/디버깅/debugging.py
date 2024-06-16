import sys
from copy import deepcopy
from itertools import combinations

input=sys.stdin.readline
MAX=int(1e9)

n,m,h=map(int,input().split())

a=[[0]*(n+1) for _ in range(h+2)]

ans=MAX

for _ in range(m):
    x,y=map(int,input().split())
    a[x][y]=1
    a[x][y+1]=2

# 가로선 넣을 자리 후보 뽑기
cand=[]
for x in range(1,h+1):
    for y in range(1,n):
        if 1<=a[x][y]<=2 or 1<=a[x][y+1]<=2:
            continue
        cand.append([x,y])

def check(a):
    result=True

    # i열이 i가 나오는 지 검사
    for y in range(1,n+1):
        col=y
        # 아래로 내려가며 탐색
        for x in range(1,h+1):
            # 1인 경우 오른쪽
            if a[x][y]==1:
                y+=1
            # 2인 경우 왼쪽
            elif a[x][y]==2:
                y-=1
        if y!=col:
            result=False
            break

    return result

if check(a):
    print(0)
    sys.exit(0)

for num in range(1,4):
    for comb in combinations(cand,num):
        for x,y in comb:
            a[x][y]=1
            a[x][y+1]=2
        if check(a):
            print(num)
            sys.exit(0)
        for x, y in comb:
            a[x][y]=0
            a[x][y+1]=0


# def dfs(a,res):
#     global ans
#
#     if res>3:
#         return
#
#     # i번 세로선 결과가 i번이면 종료
#     if check(a):
#         ans=min(ans,res)
#         return

    # 가로선 넣어보기
    # for x in range(1,h+1):
    #     for y in range(1,n):
    #         if 1<=a[x][y]<=2 or 1<=a[x][y+1]<=2:
    #             continue
    #         a[x][y]=1
    #         a[x][y+1]=2
    #         dfs(deepcopy(a),res+1)
    #         a[x][y]=0
    #         a[x][y+1]=0

# dfs(a,0)

# if ans==MAX:
#     print(-1)
# else:
#     print(ans)

print(-1)