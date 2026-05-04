"""
Figure 1 — Full network graph of the five Hajj holy sites.

Shows all nodes, all 10 edges, and per-edge labels for distance (km)
and hourly capacity. Saved to output/fig1_full_graph.png.
"""

import os
import matplotlib.pyplot as plt
import networkx as nx


def plot_full_graph(graph: "nx.Graph", positions: dict, output_path: str) -> None:
    """Draw the complete Hajj network and save it as a PNG.

    Args:
        graph:       NetworkX Graph with node attribute 'display_name' and
                     edge attributes 'distance' and 'capacity'.
        positions:   Dict mapping node id -> (x, y) for layout.
        output_path: Relative path for the output PNG file.
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # --- edges (drawn first, behind nodes) ---
    nx.draw_networkx_edges(
        graph, positions, ax=ax,
        edge_color="#AAAAAA", width=2.2, alpha=0.9,
    )

    # --- nodes ---
    nx.draw_networkx_nodes(
        graph, positions, ax=ax,
        node_color="#2E86AB", node_size=3000, alpha=0.95,
    )

    # --- node labels placed ABOVE each node with a white backing box ---
    node_labels = {node: data["display_name"] for node, data in graph.nodes(data=True)}
    pos_labels = {node: (x, y + 0.4) for node, (x, y) in positions.items()}
    nx.draw_networkx_labels(
        graph, pos_labels, labels=node_labels, ax=ax,
        font_size=12, font_weight="bold",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=2),
    )

    # --- edge labels: distance and capacity on two lines ---
    # mina-jamarat is a very short edge; shift its label toward jamarat
    # to keep it clear of the mina node label.
    all_edge_labels = {
        (u, v): f"{data['distance']} km\ncap: {data['capacity']:,}/h"
        for u, v, data in graph.edges(data=True)
    }
    short_edge_keys = {("mina", "jamarat"), ("jamarat", "mina")}
    main_labels   = {k: v for k, v in all_edge_labels.items() if k not in short_edge_keys}
    offset_labels = {k: v for k, v in all_edge_labels.items() if k in short_edge_keys}

    label_style = dict(
        ax=ax,
        font_size=8,
        rotate=False,
        bbox=dict(
            boxstyle="round,pad=0.2",
            facecolor="#FFFDE7",
            edgecolor="#CCCCCC",
            alpha=0.88,
        ),
    )
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=main_labels,   label_pos=0.5,  **label_style)
    if offset_labels:
        nx.draw_networkx_edge_labels(graph, positions, edge_labels=offset_labels, label_pos=0.65, **label_style)

    # --- title and subtitle ---
    ax.set_title(
        "Hajj Holy Sites — Full Network Graph",
        fontsize=16, fontweight="bold", pad=14,
    )
    ax.text(
        0.5, 0.01,
        "5 sites, 10 connecting roads — distances and hourly capacities",
        ha="center", va="bottom", transform=ax.transAxes,
        fontsize=11, color="#555555", style="italic",
    )
    ax.axis("off")

    # add breathing room so top labels aren't clipped
    ax.margins(0.15)

    # --- save ---
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
