"""
Figure 2 — Kruskal's MST algorithm, step-by-step (2×2 panel grid).

Panel selection:
  1. First edge added.
  2. First edge rejected (cycle detected).
  3. Second-to-last edge added (~3/4 complete).
  4. Final MST (all V-1 edges placed).
"""

import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _draw_panel(graph, positions, ax, mst_edges, current_edge, action,
                panel_title, cost_so_far):
    """Render one Kruskal step onto ax."""
    ax.set_facecolor("white")

    # All edges — faded background
    nx.draw_networkx_edges(
        graph, positions, ax=ax,
        edge_color="#CCCCCC", width=1.5, alpha=0.35,
    )

    # MST edges added so far — solid green
    if mst_edges:
        green_list = [(u, v) for u, v, _ in mst_edges]
        nx.draw_networkx_edges(
            graph, positions, edgelist=green_list, ax=ax,
            edge_color="#27AE60", width=3.5, alpha=1.0,
        )

    # Rejected edge — red dashed
    if action == "rejected":
        u, v, _ = current_edge
        nx.draw_networkx_edges(
            graph, positions, edgelist=[(u, v)], ax=ax,
            edge_color="#E74C3C", width=2.5, style="dashed", alpha=1.0,
        )

    # Nodes
    nx.draw_networkx_nodes(
        graph, positions, ax=ax,
        node_color="#2E86AB", node_size=2200, alpha=0.95,
    )

    # Labels above each node with white backing box
    node_labels = {node: data["display_name"] for node, data in graph.nodes(data=True)}
    pos_labels  = {node: (x, y + 0.45) for node, (x, y) in positions.items()}
    nx.draw_networkx_labels(
        graph, pos_labels, labels=node_labels, ax=ax,
        font_size=9, font_weight="bold",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=2),
    )

    # Panel title and cost badge
    ax.set_title(panel_title, fontsize=11, fontweight="bold", pad=8)
    ax.text(
        0.02, 0.97,
        f"MST cost so far: {cost_so_far} km",
        transform=ax.transAxes, fontsize=9, va="top", ha="left",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#EAF4FB",
                  edgecolor="#AED6F1", alpha=0.92),
    )
    ax.axis("off")
    ax.margins(0.2)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plot_kruskal_steps(graph, positions: dict, steps: list,
                       output_path: str) -> None:
    """Generate Figure 2 — 4-panel Kruskal MST step-by-step visualization.

    Args:
        graph:       NetworkX Graph (full network).
        positions:   Dict mapping node id -> (x, y).
        steps:       List of step dicts returned by kruskal_mst().
        output_path: Relative path for the output PNG file.
    """
    added_idx    = [i for i, s in enumerate(steps) if s["action"] == "added"]
    rejected_idx = [i for i, s in enumerate(steps) if s["action"] == "rejected"]

    # Select 4 representative steps
    panel_indices = [
        added_idx[0],                                             # 1st edge added
        rejected_idx[0] if rejected_idx else added_idx[0],        # 1st rejection
        added_idx[-2] if len(added_idx) >= 2 else added_idx[-1],  # 2nd-to-last added
        len(steps) - 1,                                           # final state
    ]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor("white")
    axes = axes.flatten()

    for panel_num, step_idx in enumerate(panel_indices):
        step   = steps[step_idx]
        u, v, dist = step["edge"]
        action = step["action"]
        label  = "ADDED" if action == "added" else "REJECTED"
        title  = f"Step {step_idx + 1}: {label}  {u} – {v}  ({dist} km)"

        _draw_panel(
            graph, positions, axes[panel_num],
            mst_edges    = step["mst_so_far"],
            current_edge = step["edge"],
            action       = action,
            panel_title  = title,
            cost_so_far  = step["total_cost_so_far"],
        )

    fig.suptitle(
        "Kruskal's MST Algorithm — Step-by-Step Construction",
        fontsize=15, fontweight="bold", y=1.01,
    )

    legend_elements = [
        Line2D([0], [0], color="#27AE60", linewidth=3,   label="MST edge (added)"),
        Line2D([0], [0], color="#E74C3C", linewidth=2.5, linestyle="--",
               label="Rejected (cycle detected)"),
        Line2D([0], [0], color="#CCCCCC", linewidth=1.5, label="Candidate road"),
    ]
    fig.legend(
        handles=legend_elements, loc="lower center", ncol=3,
        fontsize=10, bbox_to_anchor=(0.5, -0.02), frameon=True,
    )

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
