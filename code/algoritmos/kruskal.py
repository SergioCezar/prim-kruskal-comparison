import time
from algoritmos.unionfind import UnionFind, UnionFindSimples

def kruskal(nodes, edges_list):
    start = time.perf_counter()
    edges_sorted = sorted(edges_list, key=lambda e: e[2])
    uf = UnionFind(nodes.keys())

    mst = []
    total = 0.0

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w

    end = time.perf_counter()
    return mst, total, end - start


def kruskal_simples(nodes, edges_list):
    start = time.perf_counter()
    edges_sorted = sorted(edges_list, key=lambda e: e[2])
    uf = UnionFindSimples(nodes.keys())

    mst = []
    total = 0.0

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w

    end = time.perf_counter()
    return mst, total, end - start
