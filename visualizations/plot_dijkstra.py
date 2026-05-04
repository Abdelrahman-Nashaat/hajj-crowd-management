"""
Figure 3 — Dijkstra's shortest-path algorithm, step-by-step (1×3 panel row).

Node colour legend:
  Orange  — source node (initial panel: about to be processed).
  Green   — visited (shortest distance finalised).
  Yellow  — frontier (tentative distance known, in priority queue).
  Gray    — not yet reached.

Panel 3 also draws the final shortest path in bold blue.
"""

import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from matplotlib.lines import Line2D


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_ORANGE = "#FF8C00"
_GREEN  = "#2ECC71"
_YELLOW = "#FFD700"
_GRAY   = "#CCCCCC"
_BLUE   = "#2980B9"
_NODE   = "#2E86AB"


def _node_color(node: str, step: dict) -> str:
    """Return fill colour for a node based on its state in this step."""
    if node == step["current_node"] and node not in step["visited"]:
        return _ORANGE   # source / about-to-be-processed (Panel 1 only)
    if node in step["visited"]:
        return _GREEN    # shortest path finalised
    if node in step["frontier"]:
        return _YELLOW   # in priority queue
    return _GRAY         # not yet reached


def _fmt_dist(d) -> str:
    """Format a distance value for the node label."""
    return "∞" if d == math.inf else f"{d:.1f}"


def _draw_dijkstra_panel(graph, positions, ax, step, path_edges,
                         panel_title, source, target):
    """Render one Dijkstra step onto ax."""
    ax.set_facecolor("white")

    # All edges — faded background
    nx.draw_networkx_edges(
        graph, positions, ax=ax,
        edge_color="#CCCCCC", width=1.5, alpha=0.4,
    )

    # Shortest path edges — bold blue (Panel 3 only)
    if path_edges:
        nx.draw_networkx_edges(
            graph, positions, edgelist=path_edges, ax=ax,
            edge_color=_BLUE, width=4.5, alpha=1.0,
        )

    # Nodes with state-based colours
    node_list   = list(graph.nodes())
    node_colors = [_node_color(n, step) for n in node_list]
    nx.draw_networkx_nodes(
        graph, positions, nodelist=node_list, ax=ax,
        node_color=node_colors, node_size=2200, alpha=0.95,
    )

    # Node labels: display_name + current best distance, placed above the node
    node_labels = {}
    for node, data in graph.nodes(data=True):
        d = _fmt_dist(step["distances"][node])
        node_labels[node] = f"{data['display_name']}\n({d})"

    pos_labels = {node: (x, y + 0.52) for node, (x, y) in positions.items()}
    nx.draw_networkx_labels(
        graph, pos_labels, labels=node_labels, ax=ax,
        font_size=9, font_weight="bold",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=2),
    )

    ax.set_title(panel_title, fontsize=11, fontweight="bold", pad=8)
    ax.axis("off")
    ax.margins(0.22)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plot_dijkstra_steps(graph, positions: dict, steps: list,
                        source: str, target: str, path: list,
                        output_path: str) -> None:
    """Generate Figure 3 — 3-panel Dijkstra step-by-step visualization.

    Panels:
      1. Initial state — source orange, all other nodes gray, distances = 0 / ∞.
      2. After processing source — frontier expanded, tentative distances shown.
      3. Target reached — final shortest path highlighted in blue.

    Args:
        graph:       NetworkX Graph.
        positions:   Dict mapping node id -> (x, y).
        steps:       List of step dicts from dijkstra_shortest_path().
        source:      Source node id.
        target:      Target node id.
        path:        Ordered list of node ids on the shortest path.
        output_path: Relative path for the output PNG file.
    """
    src_name = graph.nodes[source]["display_name"]
    tgt_name = graph.nodes[target]["display_name"]

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    panels = [
        # (step, path_edges_to_draw, title)
        (
            steps[0],
            [],
            f"Panel 1 — Initial State\n"
            f"Source: {src_name}  (dist = 0)  |  all others unreached",
        ),
        (
            steps[1],
            [],
            f"Panel 2 — After Processing {graph.nodes[steps[1]['current_node']]['display_name']}\n"
            f"Frontier updated with tentative distances",
        ),
        (
            steps[-1],
            path_edges,
            f"Panel 3 — Shortest Path Found\n"
            f"{src_name} → {tgt_name}  "
            f"(congestion cost = {steps[-1]['distances'][target]:.2f})",
        ),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor("white")

    for ax, (step, pedges, title) in zip(axes, panels):
        _draw_dijkstra_panel(graph, positions, ax, step, pedges, title,
                             source, target)

    fig.suptitle(
        "Dijkstra's Shortest Path — From Mina to Jamarat (Congestion-Aware)\n"
        "Edge weight = distance × (1 + load%)  —  accounts for road congestion",
        fontsize=13, fontweight="bold", y=1.04,
    )

    legend_elements = [
        mpatches.Patch(facecolor=_ORANGE, label="Source node (initial)"),
        mpatches.Patch(facecolor=_GREEN,  label="Visited (dist. finalised)"),
        mpatches.Patch(facecolor=_YELLOW, label="Frontier (tentative dist.)"),
        mpatches.Patch(facecolor=_GRAY,   label="Unvisited"),
        Line2D([0], [0], color=_BLUE, linewidth=4, label="Shortest path"),
    ]
    fig.legend(
        handles=legend_elements, loc="lower center", ncol=5,
        fontsize=9, bbox_to_anchor=(0.5, -0.06), frameon=True,
    )

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
