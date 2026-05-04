"""
Hajj Crowd Management System — entry point (Phase 1 + 2 + 3).

Run from the hajj_crowd_management/ directory with the venv activated:

    python main.py
"""

from graph_model import build_hajj_graph, get_node_positions

from visualizations.plot_graph    import plot_full_graph
from visualizations.plot_mst      import plot_kruskal_steps
from visualizations.plot_dijkstra import plot_dijkstra_steps
from visualizations.plot_schedule import plot_schedule_comparison
from visualizations.plot_dashboard import plot_dashboard

from algorithms.kruskal_mst import kruskal_mst
from algorithms.dijkstra    import dijkstra_shortest_path
from algorithms.scheduler   import fcfs_schedule, greedy_schedule, dp_schedule

from data.pilgrim_groups import PILGRIM_GROUPS

OUT_FIG1     = "output/fig1_full_graph.png"
OUT_FIG2     = "output/fig2_kruskal_steps.png"
OUT_FIG3     = "output/fig3_dijkstra_steps.png"
OUT_FIG4     = "output/fig4_schedule_comparison.png"
OUT_FIG5     = "output/fig5_dashboard.png"

DIJKSTRA_SRC = "mina"
DIJKSTRA_TGT = "jamarat"


# ---------------------------------------------------------------------------
# Phase 1 — Graph model
# ---------------------------------------------------------------------------

def _phase1(graph, positions) -> None:
    total_dist   = sum(d["distance"] for _, _, d in graph.edges(data=True))
    avg_capacity = (
        sum(d["capacity"] for _, _, d in graph.edges(data=True))
        / graph.number_of_edges()
    )

    print("================================")
    print("Hajj Crowd Management System")
    print("Phase 1: Graph Model")
    print("================================")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    print(f"Total network distance: {total_dist:.1f} km")
    print(f"Average road capacity: {avg_capacity:,.0f} people/hour")
    print("================================")

    plot_full_graph(graph, positions, OUT_FIG1)
    print(f"[OK] Figure 1 saved to {OUT_FIG1}")


# ---------------------------------------------------------------------------
# Phase 2a — Kruskal's MST
# ---------------------------------------------------------------------------

def _phase2a(graph, positions) -> tuple:
    print()
    print("================================")
    print("Phase 2a: Kruskal's MST")
    print("================================")
    print("Running Kruskal's algorithm...")

    mst_edges, total_cost, steps = kruskal_mst(graph)

    for i, step in enumerate(steps):
        u, v, dist = step["edge"]
        action = step["action"]
        reason = step["reason"]
        tag = "ADDED   " if action == "added" else "REJECTED"
        print(f"  Step {i + 1}: {tag} {u}-{v} ({dist} km) - {reason}")

    print(f"MST total cost: {total_cost} km")
    print(f"MST edges: {len(mst_edges)} out of {graph.number_of_edges()}")

    plot_kruskal_steps(graph, positions, steps, OUT_FIG2)
    print(f"[OK] Figure 2 saved to {OUT_FIG2}")

    return mst_edges, total_cost, steps


# ---------------------------------------------------------------------------
# Phase 2b — Dijkstra's Shortest Path
# ---------------------------------------------------------------------------

def _phase2b(graph, positions) -> dict:
    print()
    print("================================")
    print("Phase 2b: Dijkstra's Shortest Path")
    print("================================")

    src_name = graph.nodes[DIJKSTRA_SRC]["display_name"]
    tgt_name = graph.nodes[DIJKSTRA_TGT]["display_name"]
    print(f"Source: {src_name}  ->  Target: {tgt_name}")

    result = dijkstra_shortest_path(graph, DIJKSTRA_SRC, DIJKSTRA_TGT)

    path_names = " -> ".join(
        graph.nodes[n]["display_name"] for n in result["path"]
    )
    print(f"Path found: {path_names}")
    print(f"Total congestion-weighted cost: {result['total_weight']:.2f}")
    print(f"Total actual distance: {result['total_distance']:.1f} km")

    plot_dijkstra_steps(
        graph, positions,
        result["steps"],
        DIJKSTRA_SRC, DIJKSTRA_TGT,
        result["path"],
        OUT_FIG3,
    )
    print(f"[OK] Figure 3 saved to {OUT_FIG3}")

    return result


# ---------------------------------------------------------------------------
# Phase 3 — Pilgrim Group Scheduling
# ---------------------------------------------------------------------------

def _phase3(graph, positions, mst_edges, mst_cost, dijkstra_result) -> None:
    groups = PILGRIM_GROUPS
    total_pilgrims = sum(g["size"] for g in groups)

    print()
    print("================================")
    print("Phase 3: Pilgrim Group Scheduling")
    print("================================")
    print(f"Loaded {len(groups)} pilgrim groups "
          f"(total pilgrims: {total_pilgrims:,})")

    # FCFS
    print()
    print("Running FCFS...")
    _, fcfs_cost, fcfs_gantt = fcfs_schedule(groups)
    print(f"  Total weighted wait: {fcfs_cost:.1f}")

    # Greedy
    print()
    print("Running Greedy (urgency-first priority)...")
    _, greedy_cost, greedy_gantt = greedy_schedule(groups)
    greedy_vs_fcfs = (fcfs_cost - greedy_cost) / fcfs_cost * 100
    print(f"  Total weighted wait: {greedy_cost:.1f}")
    print(f"  Improvement vs FCFS: {greedy_vs_fcfs:.1f}%")

    # DP
    print()
    print("Running DP (bitmask, optimal)...")
    _, dp_cost, dp_gantt = dp_schedule(groups)
    dp_vs_greedy = (greedy_cost - dp_cost) / greedy_cost * 100
    greedy_off   = (greedy_cost - dp_cost) / dp_cost * 100
    print(f"  Total weighted wait: {dp_cost:.1f}")
    print(f"  Improvement vs Greedy: {dp_vs_greedy:.1f}%")
    print(f"  Greedy was {greedy_off:.1f}% off the true optimum")

    plot_schedule_comparison(
        fcfs_gantt, fcfs_cost,
        greedy_gantt, greedy_cost,
        dp_gantt, dp_cost,
        OUT_FIG4,
    )
    print()
    print(f"[OK] Figure 4 saved to {OUT_FIG4}")

    # Dashboard
    print()
    print("================================")
    print("Final Dashboard")
    print("================================")

    schedule_results = {
        "fcfs":   {"cost": fcfs_cost,   "gantt": fcfs_gantt},
        "greedy": {"cost": greedy_cost, "gantt": greedy_gantt},
        "dp":     {"cost": dp_cost,     "gantt": dp_gantt},
    }
    plot_dashboard(
        graph, positions,
        mst_edges, mst_cost,
        dijkstra_result,
        schedule_results,
        OUT_FIG5,
        dijkstra_source=DIJKSTRA_SRC,
        dijkstra_target=DIJKSTRA_TGT,
    )
    print(f"[OK] Figure 5 saved to {OUT_FIG5}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    graph     = build_hajj_graph()
    positions = get_node_positions(graph)

    _phase1(graph, positions)
    mst_edges, mst_cost, _ = _phase2a(graph, positions)
    dijkstra_result         = _phase2b(graph, positions)
    _phase3(graph, positions, mst_edges, mst_cost, dijkstra_result)

    print()
    print("================================")
    print("ALL PHASES COMPLETE")
    print("5 figures generated in output/")
    print("================================")


if __name__ == "__main__":
    main()
