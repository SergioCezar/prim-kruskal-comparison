# Prim vs Kruskal – Computational Analysis

This repository contains an academic project developed for the **Graph Algorithms** course at the
State University of Maringá (UEM).

The goal of this project is to evaluate and compare the computational performance of different
implementations of the **Prim** and **Kruskal** algorithms for computing Minimum Spanning Trees (MST).

## Implemented Algorithms

- Prim with Binary Heap (O(E log V))
- Prim Quadratic Version (O(V²))
- Kruskal with Union-Find (Path Compression + Rank)
- Kruskal without optimizations (baseline)

## Evaluation Criteria

- Execution time
- Memory consumption
- Scalability with respect to graph size

## Technologies

- Python 3
- Standard libraries only (heapq, tracemalloc, time)
- No external graph libraries (e.g., NetworkX)

## License

This project is licensed under the MIT License.
