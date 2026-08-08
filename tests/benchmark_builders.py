import timeit
from functools import lru_cache
from typing import Any

import networkx as nx
from mappingtools.collectors import AutoMapper

from networkx_mermaid.builders import (
    DEFAULT_LAYOUT,
    DEFAULT_LOOK,
    DEFAULT_THEME,
    DiagramBuilder,
    DiagramNodeShape,
    DiagramOrientation,
)

# --- Original Implementation (Recreated for Benchmark) ---

def _original_edge_label(data: dict[str, Any]) -> str:
    """Generate an edge label string."""
    label = data.get("label")
    return f"|{label}|" if label else ""


@lru_cache(maxsize=1024)
def _original_contrast_color(color: str) -> str:
    if not (isinstance(color, str) and color.startswith("#") and len(color) == 7):
        raise ValueError(f"Invalid color format: {color}. Expected a 6-digit hex code.")
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return "#000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#ffffff"


def _original_node_style(node_id: str, data: dict[str, Any]) -> str:
    """Generate a node style string."""
    color = data.get("color")
    if color:
        return f"\nstyle {node_id} fill:{color}, color:{_original_contrast_color(color)}"
    return ""


def _original_graph_title(graph: nx.Graph, title: str | None = None) -> str:
    """Generate a graph title string."""
    title = title if title is not None else graph.name
    return f"title: {title}\n" if title else ""


class OriginalDiagramBuilder:
    def __init__(
            self,
            orientation: DiagramOrientation = DiagramOrientation.LEFT_RIGHT,
            node_shape: DiagramNodeShape = DiagramNodeShape.DEFAULT,
            layout: str = DEFAULT_LAYOUT,
            look: str = DEFAULT_LOOK,
            theme: str = DEFAULT_THEME,
    ):
        self.orientation = orientation
        self.node_shape = node_shape
        self.layout = layout
        self.look = look
        self.theme = theme

    def _diagram_config(self, graph, title: str | None = None) -> str:
        return (
            f"---\n"
            f"{_original_graph_title(graph, title)}"
            f"config:\n"
            f"  layout: {self.layout}\n"
            f"  look: {self.look}\n"
            f"  theme: {self.theme}\n"
            f"---\n"
        )

    def build(self, graph: nx.Graph, title: str | None = None, with_edge_labels: bool = True) -> str:
        config = self._diagram_config(graph, title)
        bra, ket = self.node_shape.value
        minifier = AutoMapper()

        # Pre-calculate node IDs to avoid repeated function calls
        node_map = {u: minifier.get(u) for u in graph.nodes()}

        nodes = "\n".join(
            f"{node_map[u]}{bra}{d.get('label', u)}{ket}{_original_node_style(node_map[u], d)}" for u, d in
            graph.nodes.data())

        _edges = ((node_map[u], node_map[v], d) for u, v, d in graph.edges.data())
        edges = "\n".join(f"{u} -->{_original_edge_label(d) if with_edge_labels else ''} {v}" for u, v, d in _edges)

        return (
            f"{config}"
            f"graph {self.orientation.value}\n"
            f"{nodes}\n"
            f"{edges}"
        )


# --- Benchmark Setup ---

def generate_large_graph(num_nodes=1000, num_edges=2000):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    for i in range(num_nodes):
        G.nodes[i]['label'] = f"Node {i}"
        if i % 2 == 0:
            G.nodes[i]['color'] = "#FF0000"

    for u, v in G.edges():
        G.edges[u, v]['label'] = f"Edge {u}-{v}"
    return G


def run_benchmark():
    # Setup graph
    num_nodes = 5000
    num_edges = 10000
    graph = generate_large_graph(num_nodes=num_nodes, num_edges=num_edges)
    
    print(f"Benchmarking with {len(graph.nodes)} nodes and {len(graph.edges)} edges...")
    
    # Setup builders
    original_builder = OriginalDiagramBuilder()
    new_builder = DiagramBuilder()
    
    # Number of iterations
    number = 1000
    
    # Benchmark Original
    original_time = timeit.timeit(lambda: original_builder.build(graph), number=number)
    avg_original = original_time / number
    print(f"Original Implementation: {avg_original:.4f} seconds (avg over {number} runs)")

    # Benchmark New
    new_time = timeit.timeit(lambda: new_builder.build(graph), number=number)
    avg_new = new_time / number
    print(f"New Implementation:      {avg_new:.4f} seconds (avg over {number} runs)")

    improvement = (avg_original - avg_new) / avg_original * 100
    print(f"Improvement:             {improvement:.2f}%")


if __name__ == "__main__":
    run_benchmark()
