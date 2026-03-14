import time
import heapq
from collections import deque
import matplotlib.pyplot as plt

SIZE = 10
SOURCE = (0, 0)
DEST = (9, 9)

walls = {(3,3),(3,4),(3,5),(4,5),(5,5)}

steps = [(1,0),(-1,0),(0,1),(0,-1)]

def adjacent(cell):
    x,y = cell
    for dx,dy in steps:
        nx,ny = x+dx, y+dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx,ny) not in walls:
            yield (nx,ny)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


# ---------------- Algorithms ---------------- #

def bfs_search():
    start = time.perf_counter()

    q = deque([SOURCE])
    visited = {SOURCE}
    explored = 0

    while q:
        node = q.popleft()
        explored += 1

        if node == DEST:
            break

        for nxt in adjacent(node):
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)

    return explored, time.perf_counter() - start


def dfs_search():
    start = time.perf_counter()

    stack = [SOURCE]
    visited = {SOURCE}
    explored = 0

    while stack:
        node = stack.pop()
        explored += 1

        if node == DEST:
            break

        for nxt in adjacent(node):
            if nxt not in visited:
                visited.add(nxt)
                stack.append(nxt)

    return explored, time.perf_counter() - start


def bidirectional():
    start = time.perf_counter()

    front = deque([SOURCE])
    back = deque([DEST])

    seen_front = {SOURCE}
    seen_back = {DEST}

    explored = 0

    while front and back:

        node = front.popleft()
        explored += 1

        for nxt in adjacent(node):
            if nxt in seen_back:
                return explored, time.perf_counter() - start
            if nxt not in seen_front:
                seen_front.add(nxt)
                front.append(nxt)

        node = back.popleft()
        explored += 1

        for nxt in adjacent(node):
            if nxt in seen_front:
                return explored, time.perf_counter() - start
            if nxt not in seen_back:
                seen_back.add(nxt)
                back.append(nxt)

    return explored, time.perf_counter() - start


def uniform_cost():
    start = time.perf_counter()

    pq = [(0, SOURCE)]
    visited = set()
    explored = 0

    while pq:
        cost,node = heapq.heappop(pq)
        explored += 1

        if node == DEST:
            break

        if node in visited:
            continue

        visited.add(node)

        for nxt in adjacent(node):
            heapq.heappush(pq,(cost+1,nxt))

    return explored, time.perf_counter() - start


def greedy_best():
    start = time.perf_counter()

    pq = [(manhattan(SOURCE,DEST), SOURCE)]
    visited = set()
    explored = 0

    while pq:
        _,node = heapq.heappop(pq)
        explored += 1

        if node == DEST:
            break

        if node in visited:
            continue

        visited.add(node)

        for nxt in adjacent(node):
            heapq.heappush(pq,(manhattan(nxt,DEST),nxt))

    return explored, time.perf_counter() - start


def a_star():
    start = time.perf_counter()

    pq = [(0, SOURCE)]
    visited = set()
    explored = 0

    while pq:
        cost,node = heapq.heappop(pq)
        explored += 1

        if node == DEST:
            break

        if node in visited:
            continue

        visited.add(node)

        for nxt in adjacent(node):
            g = cost + 1
            f = g + manhattan(nxt, DEST)
            heapq.heappush(pq,(f,nxt))

    return explored, time.perf_counter() - start


# ---------------- Main Comparison ---------------- #

algorithms = {
    "BFS": bfs_search,
    "DFS": dfs_search,
    "Bi-BFS": bidirectional,
    "UCS": uniform_cost,
    "BestFS": greedy_best,
    "A*": a_star
}

print("\n--- Search Algorithm Evaluation ---\n")

algo_names = []
nodes_list = []
time_list = []

for name, algo in algorithms.items():
    nodes, runtime = algo()

    print(f"Algorithm : {name}")
    print(f"Nodes visited : {nodes}")
    print(f"Execution time : {runtime:.6f} seconds")
    print("-"*40)

    algo_names.append(name)
    nodes_list.append(nodes)
    time_list.append(runtime)

plt.figure(figsize=(10,5))

# Graph 1: Nodes Explored
plt.subplot(1,2,1)
plt.bar(algo_names, nodes_list)
plt.title("Nodes Explored")
plt.xlabel("Algorithm")
plt.ylabel("Nodes")

# Graph 2: Execution Time
plt.subplot(1,2,2)
plt.bar(algo_names, time_list)
plt.title("Execution Time")
plt.xlabel("Algorithm")
plt.ylabel("Seconds")

plt.tight_layout()
plt.show()