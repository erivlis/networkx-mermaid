"""Benchmarks for `networkx_mermaid.builders`."""

import networkx as nx

from networkx_mermaid import DiagramNodeShape, DiagramOrientation
from networkx_mermaid.builders import DiagramBuilder, _contrast_color, _edge_label, _node_style

COLORS = [f"#{r:02x}{g:02x}{b:02x}" for r in range(0, 256, 32) for g in range(0, 256, 32) for b in range(0, 256, 32)]


def test_build_tiny_graph(benchmark, tiny_graph: nx.Graph):
    diagram = benchmark(DiagramBuilder().build, tiny_graph)
    assert diagram


def test_build_small_graph(benchmark, small_graph: nx.Graph):
    diagram = benchmark(DiagramBuilder().build, small_graph)
    assert diagram


def test_build_medium_graph(benchmark, medium_graph: nx.Graph):
    diagram = benchmark(DiagramBuilder().build, medium_graph)
    assert diagram


def test_build_large_graph(benchmark, large_graph: nx.Graph):
    diagram = benchmark(DiagramBuilder().build, large_graph)
    assert diagram


def test_build_medium_directed_graph(benchmark, medium_directed_graph: nx.DiGraph):
    diagram = benchmark(DiagramBuilder().build, medium_directed_graph)
    assert diagram


def test_build_medium_styled_graph(benchmark, medium_styled_graph: nx.Graph):
    """Node colors and node/edge labels exercise the styling and labelling paths."""
    diagram = benchmark(DiagramBuilder().build, medium_styled_graph)
    assert diagram


def test_build_medium_styled_graph_without_edge_labels(benchmark, medium_styled_graph: nx.Graph):
    builder = DiagramBuilder()
    diagram = benchmark(lambda: builder.build(medium_styled_graph, with_edge_labels=False))
    assert diagram


def test_build_medium_graph_custom_options(benchmark, medium_graph: nx.Graph):
    builder = DiagramBuilder(
        orientation=DiagramOrientation.TOP_DOWN,
        node_shape=DiagramNodeShape.HEXAGON,
        layout="elk",
        look="neo",
        theme="neutral",
    )
    diagram = benchmark(lambda: builder.build(medium_graph, title="Custom"))
    assert diagram


def test_contrast_color_cold_cache(benchmark):
    """Measure the color computation itself, without the `lru_cache` shortcut."""

    def run():
        _contrast_color.cache_clear()
        return [_contrast_color(color) for color in COLORS]

    assert benchmark(run)


def test_contrast_color_warm_cache(benchmark):
    for color in COLORS:
        _contrast_color(color)

    assert benchmark(lambda: [_contrast_color(color) for color in COLORS])


def test_node_style(benchmark):
    data = {"color": "#FFCCCC", "label": "Node"}
    assert benchmark(_node_style, "A", data)


def test_edge_label(benchmark):
    data = {"label": "edge"}
    assert benchmark(_edge_label, data)
