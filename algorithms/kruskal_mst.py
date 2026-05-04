"""
Kruskal's Minimum Spanning Tree algorithm for the Hajj holy-sites network.

The MST gives the lowest-total-distance spanning road network — useful for
identifying the minimal infrastructure needed to keep all sites connected.

Edge weight used: physical distance (km), NOT the congestion-aware weight.

Time complexity:  O(E log E)  — dominated by sorting E edges.
Space complexity: O(V)        — Union-Find stores one entry per node.
"""

import networkx as nx


class UnionFind:
    """Disjoint-set data structure with path compression and union by rank.

    Supports near-O(1) amortised find and union operations, making it the
    ideal companion for Kruskal's algorithm.
    """

    def __init__(self, nodes):
        """Initialise each node as its own component."""
        self.parent = {n: n for n in nodes}
        self.rank   = {n: 0  for n in nodes}

    def find(self, x) -> str:
        """Return the root of x's component (with path compression)."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y) -> bool:
        """Merge the components containing x and y.

        Returns:
            True  — merge succeeded; no cycle created.
            False — x and y share a root; adding this edge would create a cycle.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                     # already connected → cycle
        if self.rank[rx] < self.rank[ry]:    # union by rank: attach smaller tree
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal_mst(graph: nx.Graph) -> tuple:
    """Run Kruskal's algorithm and return the MST with step-by-step tracking.

    Algorithm overview:
      1. Sort all edges by distance (ascending).
      2. For each edge (u, v) in sorted order:
           - find(u) ≠ find(v)  →  add to MST, call union(u, v).
           - find(u) == find(v) →  skip (would create a cycle).
      3. Stop as soon as the MST has V−1 edges (all nodes are connected).

    Time complexity:  O(E log E)
    Space complexity: O(V)

    Args:
        graph: NetworkX Graph with a 'distance' attribute on every edge.

    Returns:
        (mst_edges, total_cost, steps) where:

        mst_edges  — list of (source, target, distance) tuples in the MST.
        total_cost — total distance of the MST (km).
        steps      — list of per-edge decision dicts, each containing:
                       'edge'              : (source, target, distance)
                       'action'            : 'added' | 'rejected'
                       'reason'            : short explanation string
                       'mst_so_far'        : MST edges up to and including this step
                       'total_cost_so_far' : cumulative MST distance (km)
    """
    sorted_edges = sorted(
        [(data["distance"], u, v) for u, v, data in graph.edges(data=True)],
        key=lambda e: e[0],
    )

    uf         = UnionFind(graph.nodes())
    mst_edges  = []
    total_cost = 0.0
    steps      = []
    n_needed   = graph.number_of_nodes() - 1   # V-1 edges needed for a spanning tree

    for dist, u, v in sorted_edges:
        if len(mst_edges) == n_needed:
            break                              # MST complete — stop early

        added = uf.union(u, v)
        if added:
            mst_edges.append((u, v, dist))
            total_cost += dist
            action = "added"
            reason = "no cycle"
        else:
            action = "rejected"
            reason = "would create cycle"

        steps.append({
            "edge":              (u, v, dist),
            "action":            action,
            "reason":            reason,
            "mst_so_far":        list(mst_edges),       # snapshot (copy)
            "total_cost_so_far": round(total_cost, 2),
        })

    return mst_edges, round(total_cost, 2), steps
