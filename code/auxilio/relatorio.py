import os
from auxilio.grafo import bytes_to_mb

def salvar_relatorio_txt(path, texto):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(texto)

def construir_texto_relatorio(nome_base, nodes_file, edges_file,
                              n_vertices, n_edges, comps, results, warnings):

    txt_lines = []
    txt_lines.append("============================================================")
    txt_lines.append(f" RELATÓRIO DO GRAFO {nome_base}")
    txt_lines.append("============================================================\n")

    txt_lines.append(f"Arquivo Nodes: {nodes_file}")
    txt_lines.append(f"Arquivo Edges: {edges_file}")
    txt_lines.append(f"Vértices: {n_vertices}")
    txt_lines.append(f"Arestas:  {n_edges}")
    txt_lines.append(f"Componentes: {comps}\n")

    txt_lines.append("------------------------------------------------------------")
    txt_lines.append(" ALGORITMOS - DESEMPENHO")
    txt_lines.append("------------------------------------------------------------")

    order = ["kruskal", "kruskal2", "prim", "prim2"]
    names_map = {
        "kruskal": "KRUSKAL (otimizado)",
        "kruskal2": "KRUSKAL (simples)",
        "prim": "PRIM (heap)",
        "prim2": "PRIM (quadrático)"
    }

    # ------------------------------------------------------------
    # Resultados por algoritmo
    # ------------------------------------------------------------
    for key in order:
        if key not in results:
            continue

        r = results[key]

        txt_lines.append(f"\n[{names_map[key]}]")

        # Caso timeout
        if r.get("timeout"):
            txt_lines.append(f" TIMEOUT: excedeu {r['timeout_seconds']} segundos.")
            txt_lines.append("  Algoritmo não concluído.")
            continue

        # Caso normal
        mst, wt, _ = r["value"]
        mem_mb = bytes_to_mb(r["mem_peak_bytes"])

        txt_lines.append(f"  Arestas MST: {len(mst)}")
        txt_lines.append(f"  Peso Total:  {wt:.6f}")
        txt_lines.append(f"  Tempo Médio: {r['time_mean']:.6f}s")
        txt_lines.append(f"  Tempo Mínimo: {r['time_min']:.6f}s")
        txt_lines.append(f"  Memória Pico: {mem_mb:.3f} MB")

    # ------------------------------------------------------------
    # VALIDAÇÃO
    # ------------------------------------------------------------

    txt_lines.append("\n------------------------------------------------------------")
    txt_lines.append(" VALIDAÇÃO")
    txt_lines.append("------------------------------------------------------------")

    msts_validas = [
        key for key, r in results.items()
        if not r.get("timeout") and r.get("value") is not None
    ]

    if len(msts_validas) <= 1:
        txt_lines.append("Não há algoritmos suficientes para comparar MSTs.")
        return "\n".join(txt_lines)

    if warnings:
        txt_lines.append("Diferenças encontradas:")
        for w in warnings:
            txt_lines.append(f" - {w}")
    else:
        txt_lines.append("Todas as MSTs coincidem.")

    return "\n".join(txt_lines)
