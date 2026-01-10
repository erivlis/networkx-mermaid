from functools import lru_cache
from typing import Any

import networkx as nx
from mappingtools.collectors import AutoMapper

from .models import DiagramNodeShape, DiagramOrientation
from .typing import MermaidDiagram

DEFAULT_LAYOUT = "dagre"
DEFAULT_LOOK = "neo"
DEFAULT_THEME = "neutral"


def _edge_label(data: dict[str, Any]) -> str:
    """Generate an edge label string."""
    label = data.get("label")
    return f"|{label}|" if label else ""


@lru_cache(maxsize=1024)
def _contrast_color(color: str) -> str:
    """
    Return black or white by choosing the best contrast to input color.

    Args:
        color: str - hex color code

    Returns:
        color: str - hex color code
    """
    if not (isinstance(color, str) and color.startswith("#") and len(color) == 7):
        raise ValueError(f"Invalid color format: {color}. Expected a 6-digit hex code.")

    # Parsing hex string as single integer with bitwise operations is faster than string slicing
    rgb = int(color[1:], 16)
    r = (rgb >> 16) & 0xFF
    g = (rgb >> 8) & 0xFF
    b = rgb & 0xFF

    # Using scaled integer arithmetic (x1000) instead of floating point math
    # Threshold: 186 * 1000 = 186000
    return "#000000" if (r * 299 + g * 587 + b * 114) > 186000 else "#ffffff"


def _node_style(node_id: str, data: dict[str, Any]) -> str:
    """Generate a node style string."""
    color = data.get("color")
    if color:
        return f"\nstyle {node_id} fill:{color}, color:{_contrast_color(color)}"
    return ""


def _graph_title(graph: nx.Graph, title: str | None = None) -> str:
    """Generate a graph title string."""
    title = title if title is not None else graph.name
    return f"title: {title}\n" if title else ""


class DiagramBuilder:
    """
    A class to generate Mermaid diagrams from NetworkX graphs.
    """

    def __init__(
            self,
            orientation: DiagramOrientation = DiagramOrientation.LEFT_RIGHT,
            node_shape: DiagramNodeShape = DiagramNodeShape.DEFAULT,
            layout: str = DEFAULT_LAYOUT,
            look: str = DEFAULT_LOOK,
            theme: str = DEFAULT_THEME,
    ):
        """
        Initialize the DiagramBuilder.

        Args:
            orientation: DiagramOrientation - The orientation of the graph (default: LEFT_RIGHT).
            node_shape: DiagramNodeShape - The shape of the nodes (default: DiagramNodeShape.DEFAULT).
            layout: str - the layout to use (default: 'dagre')
            look: str - the look to use (default: 'neo')
            theme: str - the theme to use (default: 'neutral')
        """
        self.orientation = orientation
        self.node_shape = node_shape
        self.layout = layout
        self.look = look
        self.theme = theme

        if not isinstance(orientation, DiagramOrientation):
            raise TypeError("orientation must be a valid Orientation enum")
        if not isinstance(node_shape, DiagramNodeShape):
            raise TypeError("node_shape must be a valid NodeShape enum")

    def _diagram_config(self, graph, title: str | None = None) -> str:
        return (
            f"---\n"
            f"{_graph_title(graph, title)}"
            f"config:\n"
            f"  layout: {self.layout}\n"
            f"  look: {self.look}\n"
            f"  theme: {self.theme}\n"
            f"---\n"
        )

    def build(self, graph: nx.Graph, title: str | None = None, with_edge_labels: bool = True) -> MermaidDiagram:
        """
        Materialize a graph as a Mermaid flowchart.

        Args:
            graph: nx.Graph - The NetworkX graph to convert.
            title: str - The title of the graph (default: None).
                   If None, the graph name will be used if available.
                   Supplying and empty string will remove the title.
            with_edge_labels: bool - Whether to include edge labels (default: True).

        Returns:
            A string representation of the graph as a Mermaid graph.
        """
        config = self._diagram_config(graph, title)

        bra, ket = self.node_shape.value

        minifier = AutoMapper()

        # Pre-calculate node IDs to avoid repeated function calls
        node_map = {u: minifier.get(u) for u in graph.nodes()}

        nodes = "\n".join(
            f"{node_map[u]}{bra}{d.get('label', u)}{ket}{_node_style(node_map[u], d)}" for u, d in
            graph.nodes.data())

        _edges = ((node_map[u], node_map[v], d) for u, v, d in graph.edges.data())
        edges = "\n".join(f"{u} -->{_edge_label(d) if with_edge_labels else ''} {v}" for u, v, d in _edges)

        return (
            f"{config}"
            f"graph {self.orientation.value}\n"
            f"{nodes}\n"
            f"{edges}"
        )
