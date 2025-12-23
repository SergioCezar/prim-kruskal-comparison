#Mateus Scarpin Ribeiro
#Sergio de Almeida Cezar
#!/usr/bin/env python3
import argparse
import sys
from auxilio.grafo import bytes_to_mb, ler_instancia
from auxilio.grafo import contar_componentes
from algoritmos.kruskal import kruskal, kruskal_simples
from algoritmos.prim import prim_heap, prim_quadratico
from auxilio.metricas import medir_execucao
from experimento.unico import validar
from auxilio.relatorio import salvar_relatorio_txt, construir_texto_relatorio
import os
import csv

# ============================================================
# ---------------------- EXECUÇÃO ÚNICA ----------------------
# ============================================================

def run_single(nodes_file, edges_file, out_dir="results", repeats=3, alg="all"):
    nodes, edges_list, adj = ler_instancia(nodes_file, edges_file)

    n_vertices = len(nodes)
    n_edges = len(edges_list)
    comps, comp_nodes = contar_componentes(nodes, adj)

    results = {}

    to_run = []
    if alg == "all":
        to_run = ["kruskal", "kruskal2", "prim", "prim2"]
    else:
        to_run = [alg]

    if "kruskal" in to_run:
        results["kruskal"] = medir_execucao(kruskal, nodes, edges_list, repeats=repeats)

    if "kruskal2" in to_run:
        results["kruskal2"] = medir_execucao(kruskal_simples, nodes, edges_list, repeats=repeats)

    if "prim" in to_run:
        results["prim"] = medir_execucao(prim_heap, nodes, adj, repeats=repeats)

    if "prim2" in to_run:
        results["prim2"] = medir_execucao(prim_quadratico, nodes, adj, repeats=repeats)

    validation_warnings = []
    if "kruskal" in results and "prim" in results:
        validation_warnings = validar(nodes, adj, results["kruskal"]["value"], results["prim"]["value"])
    else:
        keys = list(results.keys())
        if len(keys) >= 2:
            validation_warnings = validar(nodes, adj, results[keys[0]]["value"], results[keys[1]]["value"])

    nome_base = os.path.basename(nodes_file).replace("Nodes", "").replace(".csv", "")
    nome_rel = f"relatorio_grafo{nome_base}.txt"
    path_out = os.path.join(out_dir, nome_rel)

    texto = construir_texto_relatorio(
        nome_base, nodes_file, edges_file,
        n_vertices, n_edges, comps, results, validation_warnings
    )

    salvar_relatorio_txt(path_out, texto)

    print(texto)
    print(f"\nRelatório salvo em: {path_out}")

    return results


# ============================================================
# ---------------------- EXECUÇÃO EM LOTE --------------------
# ============================================================

def run_batch_experiments(graphs_dir, n_instances, repeats, out_dir="results", alg="all"):
    os.makedirs(out_dir, exist_ok=True)

    csv_out = os.path.join(out_dir, "resultados_experimento.csv")
    header = [
        "Grafo", "Vertices", "Arestas", "Components",
        "TempoMedio_Kruskal", "MemPeakMB_Kruskal",
        "TempoMedio_Kruskal2", "MemPeakMB_Kruskal2",
        "TempoMedio_Prim", "MemPeakMB_Prim",
        "TempoMedio_Prim2", "MemPeakMB_Prim2"
    ]

    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for i in range(1, n_instances + 1):
            nf = os.path.join(graphs_dir, f"Nodes{i}.csv")
            ef = os.path.join(graphs_dir, f"Edges{i}.csv")

            if not os.path.exists(nf) or not os.path.exists(ef):
                print(f"Instância {i} não encontrada, pulando...")
                continue

            print(f"\nExecutando Grafo {i}...")
            res = run_single(nf, ef, out_dir=out_dir, repeats=repeats, alg=alg)

            def safe_tm(key):
                if key not in res:
                    return ""
                r = res[key]
                if r.get("timeout"):
                    return "TIMEOUT"
                return f"{r['time_mean']:.6f}"

            def safe_mem(key):
                if key not in res:
                    return ""
                r = res[key]
                if r.get("timeout"):
                    return "TIMEOUT"
                return f"{bytes_to_mb(r['mem_peak_bytes']):.3f}"

            nodes, edges, adj = ler_instancia(nf, ef)
            comps, _ = contar_componentes(nodes, adj)

            writer.writerow([
                f"Grafo{i}",
                len(nodes),
                len(edges),
                comps,
                safe_tm("kruskal"),
                safe_mem("kruskal"),
                safe_tm("kruskal2"),
                safe_mem("kruskal2"),
                safe_tm("prim"),
                safe_mem("prim"),
                safe_tm("prim2"),
                safe_mem("prim2"),
            ])
            f.flush()

    print(f"\nResultados agregados em {csv_out}")


# ============================================================
# ---------------------------- CLI ----------------------------
# ============================================================

def escolher_algoritmo_menu():
    print("\nEscolha o algoritmo:")
    print(" 1 - Prim (Heap)")
    print(" 2 - Prim (Quadrático)")
    print(" 3 - Kruskal (Otimizado)")
    print(" 4 - Kruskal (Simples)")
    print(" 5 - TODOS")

    op = input("Opção: ").strip()
    mapping = {
        "1": "prim",
        "2": "prim2",
        "3": "kruskal",
        "4": "kruskal2",
        "5": "all"
    }
    return mapping.get(op, None)


def build_argparser():
    p = argparse.ArgumentParser(
        description=(
            "Prim vs Kruskal — Avaliação 3 (UEM)\n\n"
            "Modo 1 — Instância única:\n"
            "  python main.py --nodes grafos/Nodes1.csv --edges grafos/Edges1.csv\n\n"
            "Modo 2 — Batch:\n"
            "  python main.py --experiments --graphs_dir grafos --n_instances 6 --repeats 30\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument("--nodes", help="Arquivo NodesX.csv")
    p.add_argument("--edges", help="Arquivo EdgesX.csv")

    p.add_argument("--out_dir", default="results", help="Diretório de saída")
    p.add_argument("--repeats", type=int, default=3, help="Execuções por algoritmo")

    p.add_argument("--alg", choices=["prim", "prim2", "kruskal", "kruskal2", "all"], default="all")

    p.add_argument("--experiments", action="store_true", help="Rodar lote de grafos")
    p.add_argument("--graphs_dir", default="grafos", help="Pasta dos grafos")
    p.add_argument("--n_instances", type=int, default=6)

    return p


# ============================================================
# ------------------------------ MAIN -------------------------
# ============================================================

def main():
    parser = build_argparser()
    args = parser.parse_args()

    # ==========================
    #   MODO INTERATIVO
    # ==========================
    if len(sys.argv) == 1:
        print("\n=== Prim vs Kruskal — Modo Interativo ===")
        print("1 - Executar um grafo único")
        print("2 - Executar vários grafos (batch)")
        escolha = input("Escolha o modo: ").strip()

        alg = escolher_algoritmo_menu()
        if not alg:
            print("Algoritmo inválido.")
            return

        if escolha == "1":
            n = input("Digite o número do grafo (1 a 6): ").strip()
            nodes = f"grafos/Nodes{n}.csv"
            edges = f"grafos/Edges{n}.csv"
            run_single(nodes, edges, repeats=3, alg=alg)
            return

        elif escolha == "2":
            reps = int(input("Repetições por algoritmo: ").strip())
            run_batch_experiments("grafos", 6, reps, alg=alg)
            return

        else:
            print("Opção inválida.")
            return

    # ==========================
    #   MODO BATCH VIA CLI
    # ==========================
    if args.experiments:
        run_batch_experiments(args.graphs_dir, args.n_instances, args.repeats,
                            out_dir=args.out_dir, alg=args.alg, timeout=args.timeout)

        return

    # ==========================
    #   MODO NORMAL VIA CLI
    # ==========================
    if not args.nodes or not args.edges:
        print("Uso incorreto. Forneça --nodes e --edges.")
        return

    run_single(args.nodes, args.edges, out_dir=args.out_dir,
            repeats=args.repeats, alg=args.alg, timeout=args.timeout)

if __name__ == "__main__":
    main()
