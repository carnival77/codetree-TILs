n, m, K = map(int, input().split())
a = [[0]*m for _ in range(n)]
molds=[None]*(K+1)

class Mold:
    def __init__(self,no,x,y,b,s,d):
        self.no=no
        self.x=x
        self.y=y
        self.b=b
        self.s=s
        self.d=d

for no in range(1,K+1):
    x, y, s, d, b = map(int, input().split())
    x -= 1
    y -= 1
    mold=Mold(no,x,y,b,s,d)
    a[x][y]=no
    molds[no]=mold

ans = 0

def get(y):
    global a, ans

    for x in range(n):
        if a[x][y]!=0:
            no=a[x][y]
            if molds[no]==None:
                continue
            mold=molds[no]
            ans += mold.b
            a[x][y]=0
            molds[no]=None

            break

def changeDirection(d):
    if d == 1:
        return 2
    elif d == 2:
        return 1
    elif d == 3:
        return 4
    else:
        return 3


# def move(x, y, d, s):
#     if d == 1:  # 위
#         remain = x
#     elif d == 2:  # 아래
#         remain = (n - 1) - x
#     elif d == 3:  # 오른쪽
#         remain = (m - 1) - y
#     else:  # 왼쪽
#         remain = y
#
#     if remain >= s:
#         nd = d
#         if d == 1:
#             nx = x - s
#             ny = y
#         elif d == 2:
#             nx = x + s
#             ny = y
#         elif d == 3:
#             nx = x
#             ny = y + s
#         else:
#             nx = x
#             ny = y - s
#     else:  # remain < s
#         s -= remain
#         if d == 1:
#             nx = s
#             ny = y
#         elif d == 2:
#             nx = (n - 1) - s
#             ny = y
#         elif d == 3:
#             nx = x
#             ny = (m - 1) - s
#         else:
#             nx = x
#             ny = s
#         nd = changeDirection(d)
#
#     return [nx, ny, nd]


def get_next_pos(sx, sy, d, s):
    x, y = sx, sy
    if 1 <= d <= 2:  # 위,아래
        s %= 2 * (n - 1)
        # ny=y
    else:  # 오른쪽, 왼쪽
        s %= 2 * (m - 1)
        # nx=x

    # if h<1:
    #     nx,ny,nd=move(x,y,d,s)
    # else: # h>=1
    #     if h%2==1: # 홀수
    #         if d==1: # 위
    #             x=0
    #         elif d==2: # 아래
    #             x=n-1
    #         elif d==3: # 오른쪽
    #             y=m-1
    #         else: # 왼쪽
    #             y=0
    #         d = changeDirection(d)  # 방향전환
    #     else: # (h%2==0. 짝수)
    #         pass
    #     nx,ny,nd=move(x,y,d,r+1)

    while s>0:
        if d==1: # 위
            x=x-1
            if x<0:
                d=changeDirection(d)
                x=1
        elif d==2: # 아래
            x=x+1
            if x>n-1:
                d=changeDirection(d)
                x=n-2
        elif d==3: # 오른쪽
            y=y+1
            if y>m-1:
                d=changeDirection(d)
                y=m-2
        else: # 왼쪽
            y=y-1
            if y<0:
                d=changeDirection(d)
                y=1
        s-=1

    return [x, y, d]


def process():
    global a

    tmp=[[0]*m for _ in range(n)]

    for no in range(1,K+1):
        if molds[no] is None: continue
        mold=molds[no]
        x, y,s,d,b = mold.x,mold.y,mold.s,mold.d,mold.b
        if s == 0:
            tmp[x][y]=no
            continue
        nx, ny, nd = get_next_pos(x, y, d, s)
        mold.x,mold.y,mold.d=nx,ny,nd
        if tmp[nx][ny]==0:
            tmp[nx][ny]=a[x][y]
        else:
            other_no=tmp[nx][ny]
            other=molds[other_no]
            if other==None:continue
            if other.b<b:
                tmp[nx][ny]=no
                molds[other_no]=None
            else:
                molds[no]=None
    a=tmp

for col in range(m):
    # 탐색 및 채취
    get(col)
    # 곰팡이 이동 및 싸움
    process()

print(ans)