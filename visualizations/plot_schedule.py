"""
Figure 4 — Pilgrim group scheduling: FCFS vs Greedy vs DP (2x2 panel grid).

Layout:
  Top-left     FCFS Gantt chart
  Top-right    Greedy Gantt chart
  Bottom-left  DP Gantt chart (optimal)
  Bottom-right Bar chart comparing total weighted wait for all 3 algorithms
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Urgency colour palette (consistent across all panels)
URGENCY_COLORS = {
    5: "#D32F2F",   # red       — critical
    4: "#F57C00",   # orange    — high
    3: "#FBC02D",   # yellow    — medium
    2: "#0288D1",   # blue      — low
    1: "#9E9E9E",   # gray      — minimal
}

_ALGO_COLORS = {
    "FCFS":   "#C62828",
    "Greedy": "#E65100",
    "DP":     "#2E7D32",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _draw_gantt(ax, gantt_data: list, title: str, total_weighted_wait: float) -> None:
    """Render a horizontal Gantt chart on ax."""
    ax.set_facecolor("white")

    for i, entry in enumerate(gantt_data):
        color    = URGENCY_COLORS[entry["urgency"]]
        duration = entry["end"] - entry["start"]
        ax.barh(
            i, duration, left=entry["start"],
            color=color, edgecolor="white", height=0.6, alpha=0.92,
        )
        if duration >= 0.25:
            mid = entry["start"] + duration / 2
            ax.text(mid, i, entry["id"],
                    ha="center", va="center",
                    fontsize=8, fontweight="bold", color="white")

    ax.set_yticks(range(len(gantt_data)))
    ax.set_yticklabels([e["id"] for e in gantt_data], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Time (hours)", fontsize=9)
    ax.set_ylabel("Group (scheduled order)", fontsize=9)
    ax.set_title(
        f"{title}\nTotal weighted wait: {total_weighted_wait:.1f}",
        fontsize=11, fontweight="bold", pad=6,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")


def _draw_cost_bars(ax, costs: dict) -> None:
    """Render a bar chart comparing the three algorithm costs."""
    ax.set_facecolor("white")

    names  = ["FCFS", "Greedy", "DP\n(optimal)"]
    vals   = [costs["FCFS"], costs["Greedy"], costs["DP"]]
    colors = [_ALGO_COLORS["FCFS"], _ALGO_COLORS["Greedy"], _ALGO_COLORS["DP"]]

    bars = ax.bar(names, vals, color=colors, edgecolor="white", width=0.5, alpha=0.88)

    y_offset = max(vals) * 0.012
    for bar, v in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + y_offset,
            f"{v:.1f}",
            ha="center", va="bottom", fontsize=11, fontweight="bold",
        )

    dp_cost     = costs["DP"]
    greedy_cost = costs["Greedy"]
    fcfs_cost   = costs["FCFS"]
    save_greedy = (greedy_cost - dp_cost) / greedy_cost * 100
    save_fcfs   = (fcfs_cost   - dp_cost) / fcfs_cost   * 100

    ax.text(
        0.97, 0.97,
        f"DP saves {save_greedy:.1f}% vs Greedy\n"
        f"DP saves {save_fcfs:.1f}% vs FCFS",
        transform=ax.transAxes, fontsize=9,
        va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFFDE7",
                  edgecolor="#F9A825", alpha=0.9),
    )

    ax.set_ylabel("Total Weighted Waiting Time", fontsize=10)
    ax.set_title("Algorithm Cost Comparison", fontsize=11, fontweight="bold", pad=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.18)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plot_schedule_comparison(
    fcfs_gantt:   list,
    fcfs_cost:    float,
    greedy_gantt: list,
    greedy_cost:  float,
    dp_gantt:     list,
    dp_cost:      float,
    output_path:  str,
) -> None:
    """Generate Figure 4 — 2x2 scheduling comparison figure.

    Args:
        fcfs_gantt / fcfs_cost:     FCFS Gantt data and total weighted wait.
        greedy_gantt / greedy_cost: Greedy Gantt data and total weighted wait.
        dp_gantt / dp_cost:         DP Gantt data and total weighted wait.
        output_path:                Relative path for the output PNG.
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.patch.set_facecolor("white")

    _draw_gantt(axes[0, 0], fcfs_gantt,   "FCFS (arrival order)",           fcfs_cost)
    _draw_gantt(axes[0, 1], greedy_gantt, "Greedy (urgency-first)",         greedy_cost)
    _draw_gantt(axes[1, 0], dp_gantt,     "DP — Bitmask (optimal)",         dp_cost)
    _draw_cost_bars(
        axes[1, 1],
        {"FCFS": fcfs_cost, "Greedy": greedy_cost, "DP": dp_cost},
    )

    fig.suptitle(
        "Pilgrim Group Scheduling — FCFS vs Greedy vs DP",
        fontsize=15, fontweight="bold", y=1.01,
    )

    # Shared urgency legend below the title
    legend_patches = [
        mpatches.Patch(facecolor=URGENCY_COLORS[u], label=f"Urgency {u}")
        for u in sorted(URGENCY_COLORS, reverse=True)
    ]
    fig.legend(
        handles=legend_patches, loc="upper center", ncol=5,
        fontsize=9, bbox_to_anchor=(0.5, 0.99), frameon=True,
        title="Bar colour = group urgency level",
    )

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
