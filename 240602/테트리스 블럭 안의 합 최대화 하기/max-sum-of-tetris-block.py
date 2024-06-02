# 시간 복잡도
# 도형은 19가지 모양이 나올 수 있고, N * M 격자의 각 칸에 도형의 시작점이 놓일 수 있으므로,
# O(19 * (N*M)^2) < 1억

# 솔루션
# 뫼 산 모양 하나를 제외한 나머지 모양은, 임의의 칸에서 시작하여, 연속하는 3개의 인접 칸을 방문한 것으로 나타낼 수 있다.
# 따라서 뫼 산 모양 하나를 제외한 나머지는 재귀 함수로 나타낼 수 있다.


dx = [0,0,1,-1]
dy = [1,-1,0,0]
n,m = map(int,input().split())
a = [list(map(int,input().split())) for _ in range(n)]
c = [[False]*m for _ in range(n)]
def go(x,y,sum,cnt):
    if cnt == 4:
        global ans
        if ans < sum:
            ans = sum
        return
    if x < 0 or x >= n or y < 0 or y >= m:
        return
    if c[x][y]:
        return
    c[x][y] = True
    for k in range(4):
        go(x+dx[k],y+dy[k],sum+a[x][y],cnt+1)
    c[x][y] = False
ans = 0
for i in range(n):
    for j in range(m):
        go(i,j,0,0)
        if j+2 < m:
            temp = a[i][j] + a[i][j+1] + a[i][j+2]
            if i-1 >= 0:
                temp2 = temp + a[i-1][j+1]
                if ans < temp2:
                    ans = temp2
            if i+1 < n:
                temp2 = temp + a[i+1][j+1]
                if ans < temp2:
                    ans = temp2
        if i+2 < n:
            temp = a[i][j] + a[i+1][j] + a[i+2][j]
            if j+1 < m:
                temp2 = temp + a[i+1][j+1]
                if ans < temp2:
                    ans = temp2
            if j-1 >= 0:
                temp2 = temp + a[i+1][j-1]
                if ans < temp2:
                    ans = temp2
print(ans)