import csv
import math
from collections import deque


# ----------------------------------------------------
# Cálculos auxiliares
# ----------------------------------------------------

def calcular_distancia(n1, n2):
    return math.hypot(n1['x'] - n2['x'], n1['y'] - n2['y'])


def bytes_to_mb(b):
    return b / (1024 * 1024)


# ----------------------------------------------------
# Leitura de arquivos e construção de grafos
# ----------------------------------------------------

def ler_instancia(arquivo_nodes, arquivo_edges):
    nodes = {}

    with open(arquivo_nodes, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  
        for line in reader:
            if not line or all(not c.strip() for c in line):
                continue
            nid = int(line[0])
            nodes[nid] = {
                'x': float(line[1]),
                'y': float(line[2]),
            }

    adj = {nid: [] for nid in nodes}
    edges_list = []

    with open(arquivo_edges, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)

        for line in reader:
            if not line or all(not c.strip() for c in line):
                continue

            u = int(line[0])
            v = int(line[1])

            if u in nodes and v in nodes:
                w = calcular_distancia(nodes[u], nodes[v])

                edges_list.append((u, v, w))
                adj[u].append((w, v))
                adj[v].append((w, u))

    return nodes, edges_list, adj


# ----------------------------------------------------
# Análise estrutural: contagem de componentes
# ----------------------------------------------------

def contar_componentes(nodes, adj):
    visited = set()
    componentes = 0
    lista_componentes = []

    for start in nodes:
        if start in visited:
            continue

        componentes += 1
        q = deque([start])
        visited.add(start)
        comp = [start]

        while q:
            u = q.popleft()
            for _, v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
                    comp.append(v)

        lista_componentes.append(comp)

    return componentes, lista_componentes
