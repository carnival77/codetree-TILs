from itertools import combinations

n,m = map(int,input().split())

board=[]

for _ in range(n):
    board.append(list(map(int,input().split())))

houses=[]
chickens=[]

for i in range(n):
    for j in range(n):
        if board[i][j] == 1:
            houses.append((i+1,j+1))
        elif board[i][j] == 2:
            chickens.append((i+1,j+1))

# 치킨집들 중에 m개 고르는 모든 경우의 수
chicken_comb = list(combinations(chickens,m))

# 도시의 치킨 거리 = 모든 집의 치킨 거리 합
# 각 집의 치킨 거리 = min(각 집 위치 부터 m개의 치킨집 중 각 치킨집까지의 거리)
def get_sum(m_chicken):
    sum=0
    for house in houses:
        x,y = house
        each_cd = 1000
        for chicken in m_chicken:
            a,b=chicken
            dist = abs(x - a) + abs(y - b)
            each_cd = min(each_cd, dist)
        sum += each_cd
    return sum

answer=1000

# m개 치킨집들의 각 경우
for m_chicken in chicken_comb:
    # 도시의 치킨 거리의 최솟값
    answer = min(answer,get_sum(m_chicken))

print(answer)

# print(chicken_comb)
# sum=0
#
# for house in houses:
#     x,y = house
#     each_cd = 1000
#     for m_chicken in chicken_comb:
#         print("m_chicken : ",m_chicken)
#         for chicken in m_chicken:
#             print("chicken : " ,chicken)
#             a,b = chicken
#             dist = abs(x-a) + abs(y-b)
#             print("dist :",dist)
#             each_cd = min(each_cd,dist)
#             print("each_cd : ",each_cd)
#     sum += each_cd
#
# print(sum)