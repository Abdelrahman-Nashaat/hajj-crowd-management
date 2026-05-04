"""
Graph model for the Hajj Crowd Management System.

Builds a NetworkX undirected weighted graph from the five holy sites
and ten connecting roads defined in data/hajj_data.py.
"""

import networkx as nx
from data.hajj_data import NODES, EDGES


def build_hajj_graph() -> nx.Graph:
    """Build and return the Hajj holy-sites network as a NetworkX Graph.

    Each edge carries four attributes:
      - distance   : road length in km
      - capacity   : maximum throughput in people/hour
      - load       : current utilisation as a percentage (0–100)
      - weight     : congestion-aware cost = distance * (1 + load / 100)
                     used by Dijkstra's algorithm in Phase 2

    Returns:
        nx.Graph: Undirected graph with node and edge attributes populated.
    """
    graph = nx.Graph()

    for node in NODES:
        graph.add_node(
            node["id"],
            display_name=node["display_name"],
            coordinates=node["coordinates"],
        )

    for edge in EDGES:
        congestion_weight = edge["distance_km"] * (1 + edge["current_load_percent"] / 100)
        graph.add_edge(
            edge["source"],
            edge["target"],
            distance=edge["distance_km"],
            capacity=edge["capacity_per_hour"],
            load=edge["current_load_percent"],
            weight=round(congestion_weight, 4),
        )

    return graph


def get_node_positions(graph: nx.Graph) -> dict:
    """Return a positions dict suitable for NetworkX drawing functions.

    Args:
        graph: A graph built by build_hajj_graph().

    Returns:
        Dict mapping node id -> (x, y) coordinate tuple.
    """
    return {node: data["coordinates"] for node, data in graph.nodes(data=True)}
