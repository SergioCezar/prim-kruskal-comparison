import os
from auxilio.grafo import ler_instancia
from auxilio.grafo import contar_componentes
from auxilio.metricas import medir_execucao
from auxilio.relatorio import salvar_relatorio_txt, construir_texto_relatorio
from algoritmos.prim import prim_heap, prim_quadratico
from algoritmos.kruskal import kruskal, kruskal_simples


def validar(nodes, adj, resA, resB, tol=1e-6):
    mst_a, w_a, _ = resA
    mst_b, w_b, _ = resB
    warnings = []

    if abs(w_a - w_b) > tol:
        warnings.append(f"Pesos diferentes: {w_a:.6f} vs {w_b:.6f}")

    if len(mst_a) != len(mst_b):
        warnings.append(f"Nº arestas diferente: {len(mst_a)} vs {len(mst_b)}")

    return warnings


def run_single(nodes_file, edges_file, out_dir="results", repeats=3, alg="all"):
    nodes, edges_list, adj = ler_instancia(nodes_file, edges_file)

    n_vertices = len(nodes)
    n_edges = len(edges_list)
    comps, _ = contar_componentes(nodes, adj)

    results = {}

    to_run = (
        ["kruskal", "kruskal2", "prim", "prim2"]
        if alg == "all" else [alg]
    )

    if "kruskal" in to_run:
        results["kruskal"] = medir_execucao(kruskal, nodes, edges_list, repeats=repeats)

    if "kruskal2" in to_run:
        results["kruskal2"] = medir_execucao(kruskal_simples, nodes, edges_list, repeats=repeats)

    if "prim" in to_run:
        results["prim"] = medir_execucao(prim_heap, nodes, adj, repeats=repeats)

    if "prim2" in to_run:
        results["prim2"] = medir_execucao(prim_quadratico, nodes, adj, repeats=repeats)

    warnings = []
    keys = list(results.keys())
    if len(keys) >= 2:
        warnings = validar(nodes, adj, results[keys[0]]["value"], results[keys[1]]["value"])

    nome_base = os.path.basename(nodes_file).replace("Nodes", "").replace(".csv", "")
    path_out = os.path.join(out_dir, f"relatorio_grafo{nome_base}.txt")

    texto = construir_texto_relatorio(
        nome_base, nodes_file, edges_file, n_vertices, n_edges, comps, results, warnings
    )
    salvar_relatorio_txt(path_out, texto)

    print(texto)
    print(f"\nRelatório salvo em: {path_out}")

    return results
