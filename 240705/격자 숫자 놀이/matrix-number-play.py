from collections import Counter

r,c,K=map(int,input().split())
r-=1
c-=1

a=[list(map(int,input().split())) for _ in range(3)]
n,m=3,3
time=0

def transpose(a):
    return list(map(list,zip(*a)))

def R(a):

    b=[]
    length=0

    for row in a:
        arr=[]
        for x in row:
            if x!=0:
                arr.append(x)
        counter=Counter(arr)
        l = list(counter.items())
        l.sort(key=lambda x: (x[1], x[0]))
        res=[]
        for x,y in l:
            res.append(x)
            res.append(y)
        b.append(res)
        length=max(length,len(res))

    c=[]

    for row in b:
        res=row[:]
        if len(row)<length:
            dif=length-len(row)
            res+=[0]*dif
        c.append(res)

    return c

def C(a):

    return transpose(R(transpose(a)))

while time<=100:

    if n>=m:
        a=R(a)
    else:
        a=C(a)
    n = len(a)
    m = len(a[0])
    time+=1

    if 0<=r<n and 0<=c<m and a[r][c]==K:
        print(time)
        break

if time>100:
    print(-1)