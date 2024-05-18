k, m = map(int, input().split()) # 반복 횟수, 유물 조각 개수
graph = []
for _ in range(5):
    graph.append(list(map(int,input().split())))
blocks = list(map(int,input().split()))

def print_g(graph):
    print('@@@')
    for x in range(5):
        for y in range(5):
            print(graph[x][y], end = ' ')
        print()

def rotate(graph, opt):
    new_graph = [[0]*3 for _ in range(3)]
    for x in range(3):
        for y in range(3):
            if opt==0:
                new_graph[y][-1-x] = graph[x][y]
            elif opt==1:
                new_graph[-1-x][-1-y] = graph[x][y]
            elif opt==2:
                new_graph[-y-1][x] = graph[x][y]
    return new_graph

def find_g(raw,col):
    tmp_g = []
    for x in range(raw-1,raw+2):
        tmp_g.append(graph[x][col-1:col+2])
    return tmp_g

def make_g(raw,col, rotate_g):
    tmp_g = []
    for x in range(5):
        tmp_g.append(graph[x][:])
    for r in range(3):
        for c in range(3):
            tmp_g[r+raw][c+col] = rotate_g[r][c]
    return tmp_g

dxs, dys = [0,0,1,-1], [-1,1,0,0]

def in_range(x,y):
    return 0<=x<5 and 0<=y<5

def bfs(raw,col,rotate_graph):
    global cnt
    for dx,dy in zip(dxs,dys):
        nx,ny = raw+dx, col+dy
        if not in_range(nx,ny):
            continue
        if visited[nx][ny]:
            continue
        if rotate_graph[nx][ny]==rotate_graph[raw][col]:
            cnt+=1
            visited[nx][ny]=True
            bfs(nx,ny,rotate_graph)


def block_bfs(raw,col,rotate_graph):
    for dx,dy in zip(dxs,dys):
        nx,ny = raw+dx, col+dy
        if not in_range(nx,ny):
            continue
        if visited[nx][ny]:
            continue
        if rotate_graph[nx][ny]==rotate_graph[raw][col]:
            block_lst.append((nx,ny))
            visited[nx][ny]=True
            block_bfs(nx,ny,rotate_graph)

def copy(rotate_graph):
    for x in range(5):
        for y in range(5):
            graph[x][y] = rotate_graph[x][y]


block_idx=0
for time in range(k):
    # 처음 회전 찾기
    total_move = []
    for raw in range(1,4):
        for col in range(1,4):
            temp_g = find_g(raw,col)
            for opt in range(3):
                rotate_g = rotate(temp_g,opt)
                rotate_graph = make_g(raw-1,col-1,rotate_g)
                # bfs
                total_cnt = 0
                visited = [[False]*5 for _ in range(5)]
                for x in range(5):
                    for y in range(5):
                        if visited[x][y]:
                            continue
                        cnt=1
                        visited[x][y]=True
                        bfs(x,y,rotate_graph)
                        if cnt>=3:
                            total_cnt+=cnt

                total_move.append((total_cnt,opt,raw,col))
    first_cnt, first_opt, first_raw, first_col = sorted(total_move, key=lambda x:(-x[0],x[1],x[3],x[2]))[0] # 체크하기
    if first_cnt==0:
        break
    # 회전, 턴 점수, 2번 3번 반복
    turn_score = 0

    # print(first_cnt, first_opt, first_raw, first_col)
    temp_g = find_g(first_raw,first_col)
    rotate_g = rotate(temp_g,first_opt)
    rotate_graph = make_g(first_raw-1,first_col-1,rotate_g)

    # block_bfs
    while True: # 2번 3번 반복
        visited = [[False]*5 for _ in range(5)]
        total_block=[]
        for x in range(5):
            for y in range(5):
                if visited[x][y]:
                    continue
                block_lst=[(x,y)]
                visited[x][y]=True
                block_bfs(x,y,rotate_graph)
                if len(block_lst)>=3:
                    total_block.extend(block_lst)
        if len(total_block)<3:
            break
        turn_score+= len(total_block)
        total_block.sort(key=lambda x:(x[1],-x[0]))
        
        for raw, col in total_block:
            rotate_graph[raw][col] = blocks[block_idx]
            block_idx+=1
    copy(rotate_graph)

    print(turn_score, end =' ')