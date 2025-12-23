import time
import heapq
import math

def prim_heap(nodes, adj):
    start = time.perf_counter()
    visited = set()
    mst = []
    total = 0.0

    for start_node in nodes:
        if start_node in visited:
            continue
        heap = [(0.0, start_node, None)]
        while heap:
            w, u, parent = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            if parent is not None:
                mst.append((parent, u, w))
                total += w
            for w2, v in adj[u]:
                if v not in visited:
                    heapq.heappush(heap, (w2, v, u))

    end = time.perf_counter()
    return mst, total, end - start


def prim_quadratico(nodes, adj):
    start = time.perf_counter()
    verts = list(nodes.keys())
    n = len(verts)

    key = {v: float('inf') for v in verts}
    parent = {v: None for v in verts}
    in_mst = {v: False for v in verts}

    if n == 0:
        return [], 0.0, 0.0

    start_node = verts[0]
    key[start_node] = 0.0

    mst = []
    total = 0.0

    for _ in range(n):
        u = None
        min_key = float('inf')
        for v in verts:
            if not in_mst[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u is None:
            break

        in_mst[u] = True

        if parent[u] is not None:
            w = key[u]
            mst.append((parent[u], u, w))
            total += w

        for w2, v in adj[u]:
            if not in_mst[v] and w2 < key[v]:
                key[v] = w2
                parent[v] = u

    end = time.perf_counter()
    return mst, total, end - start
