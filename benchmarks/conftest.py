"""Shared fixtures for the CodSpeed benchmarks."""

import networkx as nx
import pytest

PASTEL_COLORS = ("#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#CCFFFF", "#FFCCFF")


def _colorize(graph: nx.Graph) -> nx.Graph:
    """Attach a color attribute to every node, so node styles are generated."""
    colors = {n: {"color": PASTEL_COLORS[i % len(PASTEL_COLORS)]} for i, n in enumerate(graph.nodes)}
    nx.set_node_attributes(graph, colors)
    return graph


def _label(graph: nx.Graph) -> nx.Graph:
    """Attach labels to every node and every edge."""
    nx.set_node_attributes(graph, {n: {"label": f"Node {n}"} for n in graph.nodes})
    nx.set_edge_attributes(graph, {(u, v): {"label": f"{u}->{v}"} for u, v in graph.edges})
    return graph


@pytest.fixture(scope="session")
def tiny_graph() -> nx.Graph:
    """4 nodes, 6 edges."""
    return nx.tetrahedral_graph()


@pytest.fixture(scope="session")
def small_graph() -> nx.Graph:
    """20 nodes, 30 edges."""
    return nx.dodecahedral_graph()


@pytest.fixture(scope="session")
def medium_graph() -> nx.Graph:
    """500 nodes, ~2500 edges."""
    graph = nx.gnm_random_graph(500, 2500, seed=42)
    graph.name = "medium"
    return graph


@pytest.fixture(scope="session")
def large_graph() -> nx.Graph:
    """5000 nodes, ~25000 edges."""
    graph = nx.gnm_random_graph(5000, 25000, seed=42)
    graph.name = "large"
    return graph


@pytest.fixture(scope="session")
def medium_styled_graph() -> nx.Graph:
    """500 nodes with colors and labels on both nodes and edges."""
    graph = nx.gnm_random_graph(500, 2500, seed=42)
    graph.name = "medium styled"
    return _label(_colorize(graph))


@pytest.fixture(scope="session")
def medium_directed_graph() -> nx.DiGraph:
    """500 nodes, ~2500 directed edges."""
    graph = nx.gnm_random_graph(500, 2500, seed=42, directed=True)
    graph.name = "medium directed"
    return graph
