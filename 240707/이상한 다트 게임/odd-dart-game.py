from collections import deque

n,m,q=map(int,input().split())
ans=0

a=[None]
for _ in range(n):
    a.append(deque(list(map(int,input().split()))))

for turn in range(1,q+1):
    x,d,k=map(int,input().split())

    # 원판에 남은 수 없으면 중지
    ok2 = False
    for i in range(1, n + 1):
        for j in range(m):
            if a[i][j] != 0:
                ok2 = True
    if not ok2:
        break

    # 회전
    for no in range(1,n+1):
        if no%x==0:
            if d==0:
                a[no].rotate(k)
            else:
                a[no].rotate(-k)

    # 인접한 같은 수 찾기
    b=[[0]*m for _ in range(n+1)]
    ok=False
    for i in range(1,n+1):
        for j in range(m-1):
            # 왼쪽
            if j==0: # 맨 왼쪽. 원형으로 이어진 부분 탐색
                if a[i][j]==a[i][m-1]:
                    b[i][j]=b[i][m-1]=1
                    ok=True
            else:
                if a[i][j]==a[i][j-1]:
                    b[i][j]=b[i][j-1]=1
                    ok = True
            # 오른쪽
            if a[i][j]==a[i][j+1]:
                b[i][j]=b[i][j+1]=1
                ok=True
            # 아래쪽
            if i==n: #맨 아래쪽(바깥쪽). -> 아래(바깥) 탐색 X
                continue
            else:
                if a[i][j]==a[i+1][j]:
                    b[i][j]=b[i+1][j]=1
                    ok=True
    # 인접한 같은 수가
    if ok: # 존재하면 제거
        for i in range(1,n+1):
            for j in range(m):
                if b[i][j]==1:
                    a[i][j]=0
    else: # 존재 안 하면
        # 정규화
        cnt=0
        s=0
        for i in range(1,n+1):
            for j in range(m):
                if a[i][j]!=0:
                    s+=a[i][j]
                    cnt+=1
        avg=s//cnt

        for i in range(1,n+1):
            for j in range(m):
                if a[i][j]>avg:
                    a[i][j]-=1
                elif a[i][j]<avg:
                    a[i][j]+=1

for i in range(1,n+1):
    for j in range(m):
        if a[i][j]!=0:
            ans+=a[i][j]
print(ans)