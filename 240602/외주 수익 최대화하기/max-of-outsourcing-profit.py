n=int(input())

data=[]
for _ in range(n):
    t,p=map(int,input().split())
    data.append([t,p])

dp=[0]*(n+1)

for i in range(n):
    t,p=data[i]
    # t-=1
    dp[i+t]=max(dp[i]+p,dp[i+t])

print(dp[n])