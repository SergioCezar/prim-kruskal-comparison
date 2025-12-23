import os
import csv

from experimento.unico import run_single
from auxilio.grafo import ler_instancia
from auxilio.grafo import contar_componentes
from auxilio.grafo import bytes_to_mb

def run_batch_experiments(graphs_dir, n_instances, repeats, out_dir="results", alg="all"):
    os.makedirs(out_dir, exist_ok=True)

    csv_out = os.path.join(out_dir, "resultados_experimento.csv")

    header = [
        "Grafo", "Vertices", "Arestas", "Componentes",
        "Tempo_Kruskal", "Mem_Kruskal_MB",
        "Tempo_Kruskal2", "Mem_Kruskal2_MB",
        "Tempo_Prim", "Mem_Prim_MB",
        "Tempo_Prim2", "Mem_Prim2_MB"
    ]

    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for i in range(1, n_instances + 1):
            nf = os.path.join(graphs_dir, f"Nodes{i}.csv")
            ef = os.path.join(graphs_dir, f"Edges{i}.csv")

            if not os.path.exists(nf) or not os.path.exists(ef):
                print(f"Grafo {i} não encontrado, pulando...")
                continue

            print(f"\n>> Executando Grafo {i}...")
            res = run_single(nf, ef, out_dir=out_dir, repeats=repeats, alg=alg)

            nodes, edges, adj = ler_instancia(nf, ef)
            comps, _ = contar_componentes(nodes, adj)

            def tm(k):
                return f"{res[k]['time_mean']:.6f}" if k in res else ""

            def mm(k):
                return f"{bytes_to_mb(res[k]['mem_peak_bytes']):.3f}" if k in res else ""

            row = [
                f"Grafo{i}",
                len(nodes),
                len(edges),
                comps,
                tm("kruskal"), mm("kruskal"),
                tm("kruskal2"), mm("kruskal2"),
                tm("prim"), mm("prim"),
                tm("prim2"), mm("prim2")
            ]

            writer.writerow(row)
            f.flush()

    print(f"\nResultados salvos em: {csv_out}")
