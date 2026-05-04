"""
Dijkstra's shortest-path algorithm for the Hajj holy-sites network.

Uses congestion-aware edge weights:  weight = distance × (1 + load / 100)
A road under heavy load is penalised so the algorithm naturally avoids
bottlenecks and reroutes pilgrims to less-congested roads.

The 'weight' attribute was pre-computed in graph_model.build_hajj_graph().

Time complexity:  O((V + E) log V)  — binary-heap priority queue.
Space complexity: O(V + E).
"""

import heapq
import math
import networkx as nx


def dijkstra_shortest_path(graph: nx.Graph, source: str, target: str) -> dict:
    """Find the minimum congestion-weighted path between source and target.

    Algorithm overview:
      1. dist[source] = 0;  dist[all others] = ∞.
         Push (0, source) onto a min-heap.
      2. Pop node u with the smallest tentative distance:
           a. If u is already visited → skip (stale heap entry).
           b. Mark u visited (shortest path to u is now final).
           c. If u == target → done; reconstruct and return path.
           d. For each unvisited neighbour v:
                new_d = dist[u] + weight(u, v)
                if new_d < dist[v] → relax: dist[v] = new_d, record prev[v] = u, push (new_d, v).
      3. Repeat until target is settled or heap is empty.

    Step snapshots are recorded AFTER relaxing neighbours so each snapshot
    reflects fully-updated distances — useful for visualisation.

    Time complexity:  O((V + E) log V)
    Space complexity: O(V + E)

    Args:
        graph:  NetworkX Graph with 'weight' (congestion cost) and
                'distance' (km) on every edge.
        source: Starting node id (e.g. 'mina').
        target: Destination node id (e.g. 'jamarat').

    Returns:
        dict with keys:
          'path'           — ordered list of node ids from source to target.
          'total_weight'   — sum of congestion-aware weights along the path.
          'total_distance' — sum of physical distances (km) along the path.
          'steps'          — list of per-iteration state snapshots (see below).

        Each step dict:
          'current_node' : node that was just settled (None for initial snapshot).
          'distances'    : snapshot of best-known distance from source to every node.
          'visited'      : set of nodes whose shortest distance is finalised.
          'frontier'     : set of nodes currently queued (tentative distance known).
    """
    inf  = math.inf
    dist = {n: inf   for n in graph.nodes()}
    prev = {n: None  for n in graph.nodes()}
    dist[source] = 0.0
    visited = set()
    heap    = [(0.0, source)]
    steps   = []

    # Snapshot 0 — initial state before any node is settled
    steps.append({
        "current_node": source,       # source is highlighted orange in Panel 1
        "distances":    dict(dist),
        "visited":      set(),
        "frontier":     set(),        # nothing in queue yet besides the source itself
    })

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue                  # stale heap entry
        visited.add(u)

        # Relax neighbours before snapshotting so the step shows updated distances
        if u != target:
            for v in graph.neighbors(u):
                if v in visited:
                    continue
                new_d = dist[u] + graph[u][v]["weight"]
                if new_d < dist[v]:
                    dist[v] = new_d
                    prev[v] = u
                    heapq.heappush(heap, (new_d, v))

        frontier = {n for _, n in heap if n not in visited}
        steps.append({
            "current_node": u,
            "distances":    dict(dist),
            "visited":      set(visited),
            "frontier":     set(frontier),
        })

        if u == target:
            break

    # Reconstruct path by tracing prev[] back from target to source
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    total_distance = sum(
        graph[path[i]][path[i + 1]]["distance"] for i in range(len(path) - 1)
    )

    return {
        "path":           path,
        "total_weight":   round(dist[target], 4),
        "total_distance": round(total_distance, 2),
        "steps":          steps,
    }
