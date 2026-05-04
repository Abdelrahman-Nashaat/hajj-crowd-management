# Hajj Crowd Management System

An algorithmic optimization study of pilgrim flow during Hajj, implemented as a
final project for **Algorithm Design & Analysis** (Tanta University, 4th-year Engineering).

## Problem

Every year ~2.5 million pilgrims move between five holy sites — Masjid Al Haram, Mina,
Arafat, Muzdalifah, and Jamarat — on a schedule defined by Islamic ritual. Crowd
congestion on the limited road network has caused fatal stampedes (Mina 1990: 1,426
deaths; Mina 2015: 2,431 deaths). This project models the problem as a weighted graph
and applies five core algorithm-design techniques to optimize infrastructure, routing,
and group scheduling.

> **Data disclaimer:** All distances, capacities, congestion levels, and pilgrim group
> properties are **simulated values** inspired by published statistics. They are for
> academic algorithm demonstration only, not real-world planning.

## Algorithms Implemented

| Phase | Algorithm | Purpose | Complexity |
|-------|-----------|---------|------------|
| 1 | Graph Modeling | 5 sites, 10 weighted edges | — |
| 2 | Kruskal's MST | Minimum-cost spanning infrastructure | O(E log E) |
| 2 | Dijkstra's Shortest Path | Congestion-aware routing | O((V+E) log V) |
| 3 | Greedy Scheduling | Fast urgency-first group ordering | O(n log n) |
| 3 | Dynamic Programming | Optimal group ordering (bitmask) | O(n × 2ⁿ) |

## Key Results

| Metric | Value |
|--------|-------|
| Network | 5 sites, 10 roads, 91.5 km total |
| MST | 4 edges, **21.5 km** total cost |
| Shortest path (Mina → Jamarat) | **1.5 km**, congestion-weighted cost **2.85** |
| FCFS weighted wait | 174.0 |
| Greedy weighted wait | 103.1 (40.7% better than FCFS) |
| DP weighted wait | **89.8** (12.9% better than Greedy) |

### Key Finding — Greedy is NOT Optimal

The greedy heuristic (process most-urgent groups first) improves dramatically over FCFS,
but is still **14.8% worse** than the true optimum found by DP. The reason: a
high-urgency group with a long processing time blocks all subsequent groups, accumulating
unnecessary weighted wait. The optimal rule (Weighted Shortest Processing Time — urgency
divided by processing time) is what the bitmask DP rediscovers through exhaustive search.

## Output Figures

After running `python main.py`, five PNG files appear in `output/`:

| File | Contents |
|------|----------|
| `fig1_full_graph.png` | Full network — all 5 nodes, 10 edges, distances and capacities |
| `fig2_kruskal_steps.png` | 4-panel MST construction (added edges green, rejected edges red-dashed) |
| `fig3_dijkstra_steps.png` | 3-panel shortest-path search (node states colour-coded) |
| `fig4_schedule_comparison.png` | Gantt charts for FCFS / Greedy / DP + cost bar chart |
| `fig5_dashboard.png` | One-page project summary dashboard |

## Project Structure

```
hajj_crowd_management/
├── main.py                    # Entry point — runs all three phases
├── graph_model.py             # build_hajj_graph() and get_node_positions()
├── algorithms/
│   ├── kruskal_mst.py         # UnionFind + kruskal_mst()
│   ├── dijkstra.py            # dijkstra_shortest_path()
│   └── scheduler.py           # fcfs_schedule / greedy_schedule / dp_schedule
├── visualizations/
│   ├── plot_graph.py          # Figure 1
│   ├── plot_mst.py            # Figure 2
│   ├── plot_dijkstra.py       # Figure 3
│   ├── plot_schedule.py       # Figure 4
│   └── plot_dashboard.py      # Figure 5
├── data/
│   ├── hajj_data.py           # Node and edge definitions
│   └── pilgrim_groups.py      # 10 pilgrim groups for scheduling
├── output/                    # Generated PNG figures (not committed)
├── venv/                      # Virtual environment (not committed)
└── requirements.txt
```

## How to Run

### On Windows (Git Bash)

```bash
cd hajj_crowd_management

# Create and activate the virtual environment
python -m venv venv
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run all three phases
python main.py
```

### Expected console output (abridged)

```
================================
Hajj Crowd Management System
Phase 1: Graph Model
================================
Nodes: 5  |  Edges: 10  |  Total distance: 91.5 km
[OK] Figure 1 saved to output/fig1_full_graph.png

================================
Phase 2a: Kruskal's MST
================================
  Step 1: ADDED    mina-jamarat (1.5 km)
  Step 3: REJECTED muzdalifah-jamarat (5 km) - would create cycle
  ...
MST total cost: 21.5 km
[OK] Figure 2 saved to output/fig2_kruskal_steps.png

================================
Phase 3: Pilgrim Group Scheduling
================================
  FCFS:   174.0
  Greedy: 103.1  (40.7% better than FCFS)
  DP:      89.8  (12.9% better than Greedy, 14.8% off optimal for Greedy)
[OK] Figure 5 saved to output/fig5_dashboard.png
```

## Dependencies

```
matplotlib==3.10.9
networkx==3.6.1
numpy==2.4.4
```

Install with `pip install -r requirements.txt` inside the activated virtual environment.

## Author

[Student Name] — Tanta University, Faculty of Engineering, 4th Year
