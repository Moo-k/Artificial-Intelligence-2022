import math
import sys
import numpy as np
import heapq

class Iterator:
    def __init__(self):
        self.a = 0

    def __next__(self):
        self.a += 1
        return self.a

class Node:
    def __init__(self,r,c,parent=None,cost=0,order=0):
        self.r = r
        self.c = c
        self.parent = parent
        self.cost = cost
        self.order = order

    def __lt__(self,compare):  # overloaded less than comparison for nodes (to add to heap)
        if self.cost != compare.cost:
            return self.cost < compare.cost
        else:
            return self.order < compare.order


# def checkValid(r,c,v,m,sz):
#     if (r < 0 or c < 0 or r >= sz[0] or c >= sz[1]):
#         return False
#     if (v[r][c]):
#         return False
#     if (m[r][c] == "X"):
#         return False
#     return True

def checkValid2(r,c,m,sz):
    if (r < 0 or c < 0 or r >= sz[0] or c >= sz[1]):
        return False
    if (m[r][c] == "X"):
        return False
    return True


def bfs(s,e,sz,tmap,vis):
    queue = [(s, [])]

    while len(queue) > 0:
        pos,route = queue.pop(0)
        route.append(pos)
        vis[pos[0]][pos[1]] = 1

        if pos == e:
            return route
        neighbors = []
        if checkValid2(pos[0]-1,pos[1],tmap,sz) and not vis[pos[0]-1][pos[1]]:  # up
            neighbors.append([pos[0]-1,pos[1]])
        if checkValid2(pos[0]+1,pos[1],tmap,sz) and not vis[pos[0]+1][pos[1]]:  # down
            neighbors.append([pos[0]+1,pos[1]])
        if checkValid2(pos[0],pos[1]-1,tmap,sz) and not vis[pos[0]][pos[1]-1]:  # left
            neighbors.append([pos[0],pos[1]-1])
        if checkValid2(pos[0],pos[1]+1,tmap,sz) and not vis[pos[0]][pos[1]+1]:  # right
            neighbors.append([pos[0],pos[1]+1])

        if len(neighbors) > 0:
            for n in neighbors:
                # print(n)
                if vis[n[0]][n[1]] == 0:
                    queue.append((n,route[:]))
    return None

def ucs(s,e,sz,tmap):
    queue = [Node(s[0],s[1])]
    # add starting point to queue, and turn it into a heap
    heapq.heapify(queue)
    vis = set()
    # initialise visited set, so that there are no repeats
    vis.add((s[0],s[1]))
    # step count
    counter = Iterator()

    while queue:
        n = heapq.heappop(queue)
        # print("at: ",n.r,", ",n.c)
        # print("vis: \n", vis)

        if [n.r,n.c] == e:  # if end is reached
            upath = []
            back = n
            while back is not None:
                upath.append([back.r, back.c])
                # backtrack to parent node
                back = back.parent
            # print("ucs returning")
            return upath

        neighbors = []
        # print("neighbors ok")
        if checkValid2(n.r-1,n.c,tmap,sz) and ((n.r-1,n.c) not in vis):  # up
            neighbors.append(Node(n.r-1,n.c))
            # print("neighbor added: ",n.r-1,", ",n.c)
        if checkValid2(n.r+1,n.c,tmap,sz) and ((n.r+1,n.c) not in vis):  # down
            neighbors.append(Node(n.r+1, n.c))
            # print("neighbor added: ", n.r+1, ", ", n.c)
        if checkValid2(n.r,n.c-1,tmap,sz) and ((n.r,n.c-1) not in vis):  # left
            neighbors.append(Node(n.r, n.c-1))
            # print("neighbor added: ", n.r, ", ", n.c-1)
        if checkValid2(n.r,n.c+1,tmap,sz) and ((n.r,n.c+1) not in vis):  # right
            neighbors.append(Node(n.r, n.c+1))
            # print("neighbor added: ", n.r, ", ", n.c+1)

        if len(neighbors) > 0:
            for k in neighbors:
                cost = 1
                if int(tmap[k.r][k.c]) - int(tmap[n.r][n.c]) > 0:
                    cost += int(tmap[k.r][k.c]) - int(tmap[n.r][n.c])
                neighborNode = Node(k.r, k.c, n, cost, next(counter))
                heapq.heappush(queue, neighborNode)
                vis.add((k.r, k.c))
    return None

def manhattan(s,e):
    return abs(s[0]-e[0]) + abs(s[1]-e[1])

def euclidean(s,e):
    return math.sqrt((e[0]-s[0])**2 + (e[1]-s[1])**2)

def astar(s,e,sz,tmap,h):
    # heuristic value of starting point
    if h == "manhattan":
        starth = manhattan(s,e)
    if h == "euclidean":
        starth = euclidean(s,e)

    queue = [(starth,0,Node(s[0],s[1]))]
    # add starting point to queue, and turn it into a heap
    heapq.heapify(queue)
    vis = set()
    # initialise visited set, so that there are no repeats
    vis.add((s[0], s[1]))
    # step count
    counter = Iterator()

    while queue:
        g2, order, n = heapq.heappop(queue)

        if [n.r,n.c] == e:  # if end is reached
            upath = []
            back = n
            while back is not None:
                upath.append([back.r, back.c])
                # backtrack to parent node
                back = back.parent
            return upath

        neighbors = []
        # print("neighbors ok")
        if checkValid2(n.r-1,n.c,tmap,sz) and ((n.r-1,n.c) not in vis):  # up
            neighbors.append(Node(n.r-1,n.c))
            # print("neighbor added: ",n.r-1,", ",n.c)
        if checkValid2(n.r+1,n.c,tmap,sz) and ((n.r+1,n.c) not in vis):  # down
            neighbors.append(Node(n.r+1, n.c))
            # print("neighbor added: ", n.r+1, ", ", n.c)
        if checkValid2(n.r,n.c-1,tmap,sz) and ((n.r,n.c-1) not in vis):  # left
            neighbors.append(Node(n.r, n.c-1))
            # print("neighbor added: ", n.r, ", ", n.c-1)
        if checkValid2(n.r,n.c+1,tmap,sz) and ((n.r,n.c+1) not in vis):  # right
            neighbors.append(Node(n.r, n.c+1))
            # print("neighbor added: ", n.r, ", ", n.c+1)

        if len(neighbors) > 0:
            for k in neighbors:
                cost = 1 + n.cost
                if int(tmap[k.r][k.c]) - int(tmap[n.r][n.c]) > 0:
                    cost += int(tmap[k.r][k.c]) - int(tmap[n.r][n.c])
                g = cost
                if h == "manhattan":
                    g += manhattan((k.r,k.c),e)
                if h == "euclidean":
                    g += euclidean((k.r,k.c),e)
                heapq.heappush(queue, (g, order, Node(k.r, k.c, n, cost, next(counter))))
                vis.add((k.r, k.c))








    return None

if __name__ == "__main__":
    mapFile = sys.argv[1]
    algorithm = sys.argv[2]

    if len(sys.argv) > 3:
        heuristic = sys.argv[3]
    else:
        heuristic = None

    f = open(mapFile, "r")

    themap = []
    for line in f.readlines():
        line = line.strip().split()
        themap.append(line)

    size = themap[0]
    start = themap[1]
    end = themap[2]
    themap.pop(0)  # size
    themap.pop(0)  # start
    themap.pop(0)  # end

    path = []
    rows = size[0].strip().split()
    cols = size[1].strip().split()
    size = [int(rows[0]),int(cols[0])]

    sr = start[0].strip().split()
    sc = start[1].strip().split()
    start = [int(sr[0])-1,int(sc[0])-1]

    er = end[0].strip().split()
    ec = end[1].strip().split()
    end = [int(er[0])-1,int(ec[0])-1]

    visited = np.zeros(size)

    if algorithm == "bfs":
        path = bfs(start,end,size,themap,visited)
    if algorithm == "ucs":
        path = ucs(start,end,size,themap)
    if algorithm == "astar":
        path = astar(start,end,size,themap,heuristic)

    if path:
        for i in path:
            themap[i[0]][i[1]] = '*'
        for j in themap:
            line = " ".join(j)
            print(line)
    else:
        print("null")
