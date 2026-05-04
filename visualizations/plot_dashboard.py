"""
Figure 5 — Project summary dashboard (2x3 panel grid).

Panels:
  [0,0] Mini full network graph
  [0,1] Mini MST (green edges)
  [0,2] Mini Dijkstra shortest path (blue edges)
  [1,0] Mini DP Gantt chart (optimal schedule)
  [1,1] Algorithm cost comparison bar chart
  [1,2] Text summary card
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from matplotlib.lines import Line2D

from visualizations.plot_schedule import URGENCY_COLORS, _ALGO_COLORS


# ---------------------------------------------------------------------------
# Mini graph helpers
# ---------------------------------------------------------------------------

def _mini_graph_base(graph, positions, ax, node_colors=None,
                     highlight_edges=None, highlight_color="#27AE60",
                     highlight_width=2.5, node_size=700):
    """Draw a compact version of the network on ax."""
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        graph, positions, ax=ax,
        edge_color="#CCCCCC", width=1.2, alpha=0.4,
    )
    if highlight_edges:
        nx.draw_networkx_edges(
            graph, positions, edgelist=highlight_edges, ax=ax,
            edge_color=highlight_color, width=highlight_width, alpha=1.0,
        )

    if node_colors is None:
        node_colors = "#2E86AB"
    nx.draw_networkx_nodes(
        graph, positions, ax=ax,
        node_color=node_colors, node_size=node_size, alpha=0.92,
    )

    labels    = {n: d["display_name"] for n, d in graph.nodes(data=True)}
    pos_lbl   = {n: (x, y + 0.38) for n, (x, y) in positions.items()}
    nx.draw_networkx_labels(
        graph, pos_lbl, labels=labels, ax=ax,
        font_size=6.5, font_weight="bold",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1),
    )

    ax.axis("off")
    ax.margins(0.22)


def _panel_full_graph(graph, positions, ax):
    _mini_graph_base(graph, positions, ax)
    ax.set_title("Full Network (5 sites, 10 roads)",
                 fontsize=10, fontweight="bold", pad=5)


def _panel_mst(graph, positions, ax, mst_edges):
    green_list = [(u, v) for u, v, _ in mst_edges]
    _mini_graph_base(graph, positions, ax,
                     highlight_edges=green_list, highlight_color="#27AE60")
    ax.set_title(f"Kruskal MST ({len(mst_edges)} edges)",
                 fontsize=10, fontweight="bold", pad=5)


def _panel_dijkstra(graph, positions, ax, path, source, target):
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    # Node colours: source=orange, target=green, others=default
    node_colors = []
    for n in graph.nodes():
        if n == source:
            node_colors.append("#FF8C00")
        elif n == target:
            node_colors.append("#2ECC71")
        else:
            node_colors.append("#2E86AB")

    _mini_graph_base(graph, positions, ax,
                     node_colors=node_colors,
                     highlight_edges=path_edges,
                     highlight_color="#2980B9",
                     highlight_width=3.5)
    src_name = graph.nodes[source]["display_name"]
    tgt_name = graph.nodes[target]["display_name"]
    ax.set_title(f"Dijkstra: {src_name} -> {tgt_name}",
                 fontsize=10, fontweight="bold", pad=5)


# ---------------------------------------------------------------------------
# Mini Gantt
# ---------------------------------------------------------------------------

def _panel_gantt(ax, gantt_data, title):
    ax.set_facecolor("white")
    for i, entry in enumerate(gantt_data):
        color    = URGENCY_COLORS[entry["urgency"]]
        duration = entry["end"] - entry["start"]
        ax.barh(i, duration, left=entry["start"],
                color=color, edgecolor="white", height=0.55, alpha=0.92)
        if duration >= 0.3:
            mid = entry["start"] + duration / 2
            ax.text(mid, i, entry["id"],
                    ha="center", va="center",
                    fontsize=6.5, fontweight="bold", color="white")

    ax.set_yticks(range(len(gantt_data)))
    ax.set_yticklabels([e["id"] for e in gantt_data], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Time (hours)", fontsize=8)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")


# ---------------------------------------------------------------------------
# Cost comparison bars
# ---------------------------------------------------------------------------

def _panel_cost_bars(ax, fcfs_cost, greedy_cost, dp_cost):
    ax.set_facecolor("white")
    names  = ["FCFS", "Greedy", "DP\n(optimal)"]
    vals   = [fcfs_cost, greedy_cost, dp_cost]
    colors = [_ALGO_COLORS["FCFS"], _ALGO_COLORS["Greedy"], _ALGO_COLORS["DP"]]

    bars = ax.bar(names, vals, color=colors, edgecolor="white",
                  width=0.5, alpha=0.88)
    y_off = max(vals) * 0.015
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + y_off, f"{v:.1f}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylabel("Total Weighted Wait", fontsize=9)
    ax.set_title("Scheduling Cost Comparison", fontsize=10, fontweight="bold", pad=5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.2)


# ---------------------------------------------------------------------------
# Text summary card
# ---------------------------------------------------------------------------

def _panel_text_card(ax, graph, mst_edges, mst_cost,
                     dijkstra_result, schedule_results):
    ax.set_facecolor("#F8F9FA")
    ax.axis("off")

    fcfs_cost   = schedule_results["fcfs"]["cost"]
    greedy_cost = schedule_results["greedy"]["cost"]
    dp_cost     = schedule_results["dp"]["cost"]
    greedy_pct  = (greedy_cost - dp_cost) / dp_cost * 100

    path     = dijkstra_result["path"]
    src_name = graph.nodes[path[0]]["display_name"]
    tgt_name = graph.nodes[path[-1]]["display_name"]

    sep = "-" * 31
    text = (
        "HAJJ CROWD MANAGEMENT SYSTEM\n"
        f"{sep}\n"
        f"Network: {graph.number_of_nodes()} sites, "
        f"{graph.number_of_edges()} roads\n"
        "\n"
        "Kruskal MST:\n"
        f"  Edges: {len(mst_edges)} of {graph.number_of_edges()}\n"
        f"  Total cost: {mst_cost} km\n"
        "  Complexity: O(E log E)\n"
        "\n"
        f"Dijkstra ({src_name} to {tgt_name}):\n"
        f"  Path: {dijkstra_result['total_distance']} km\n"
        f"  Congestion weight: {dijkstra_result['total_weight']}\n"
        "  Complexity: O((V+E) log V)\n"
        "\n"
        "Pilgrim Scheduling (10 groups):\n"
        f"  FCFS:   {fcfs_cost:.1f}\n"
        f"  Greedy: {greedy_cost:.1f}\n"
        f"  DP:     {dp_cost:.1f}  <- optimal\n"
        f"  Greedy is {greedy_pct:.1f}% off optimal\n"
        "\n"
        "Algorithms covered:\n"
        "  [OK] Graph Modeling\n"
        "  [OK] Kruskal's MST\n"
        "  [OK] Dijkstra's Shortest Path\n"
        "  [OK] Greedy Scheduling\n"
        "  [OK] Dynamic Programming"
    )

    ax.text(
        0.05, 0.97, text,
        transform=ax.transAxes,
        fontsize=8.5, family="monospace",
        va="top", ha="left", linespacing=1.55,
        bbox=dict(boxstyle="round,pad=0.6",
                  facecolor="white", edgecolor="#CCCCCC", alpha=0.95),
    )
    ax.set_title("Project Summary", fontsize=10, fontweight="bold", pad=5)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plot_dashboard(
    graph,
    positions:        dict,
    mst_edges:        list,
    mst_cost:         float,
    dijkstra_result:  dict,
    schedule_results: dict,
    output_path:      str,
    dijkstra_source:  str = "mina",
    dijkstra_target:  str = "jamarat",
) -> None:
    """Generate Figure 5 — full project summary dashboard (2x3 grid).

    Args:
        graph:             NetworkX Graph.
        positions:         Dict mapping node id -> (x, y).
        mst_edges:         List of (u, v, dist) tuples from kruskal_mst().
        mst_cost:          Total MST distance (km).
        dijkstra_result:   Dict returned by dijkstra_shortest_path().
        schedule_results:  Dict with keys 'fcfs', 'greedy', 'dp', each
                           containing 'cost' and 'gantt' sub-keys.
        output_path:       Relative path for the output PNG.
        dijkstra_source:   Source node id used in Dijkstra (default 'mina').
        dijkstra_target:   Target node id used in Dijkstra (default 'jamarat').
    """
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.patch.set_facecolor("white")

    # --- top row: graph panels ---
    _panel_full_graph(graph, positions, axes[0, 0])
    _panel_mst(graph, positions, axes[0, 1], mst_edges)
    _panel_dijkstra(graph, positions, axes[0, 2],
                    dijkstra_result["path"], dijkstra_source, dijkstra_target)

    # --- bottom row: scheduling panels ---
    dp_gantt = schedule_results["dp"]["gantt"]
    _panel_gantt(axes[1, 0], dp_gantt,
                 f"DP Schedule (optimal, TW={schedule_results['dp']['cost']:.1f})")
    _panel_cost_bars(axes[1, 1],
                     schedule_results["fcfs"]["cost"],
                     schedule_results["greedy"]["cost"],
                     schedule_results["dp"]["cost"])
    _panel_text_card(axes[1, 2], graph, mst_edges, mst_cost,
                     dijkstra_result, schedule_results)

    fig.suptitle(
        "Hajj Crowd Management System — Project Summary Dashboard",
        fontsize=16, fontweight="bold", y=1.01,
    )

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
