import base64
from collections import defaultdict
from typing import Any

import networkx as nx
from mappingtools.operators import unique_strings

from .models import DiagramNodeShape, DiagramOrientation
from .typing import MermaidDiagram

DEFAULT_LAYOUT = "dagre"
DEFAULT_LOOK = "neo"
DEFAULT_THEME = "neutral"


def _edge_label(data: dict[str, Any]) -> str:
    """Generate an edge label string."""
    label = data.get("label")
    return f"|{label}|" if label else ""


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

    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return "#000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#ffffff"


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


def _node_id(node_id) -> str:
    """Generate a node id string."""
    n_repr = repr(node_id)
    n_b64 = base64.urlsafe_b64encode(n_repr.encode())
    n_id = n_b64.decode().rstrip('=')
    return n_id


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
            orientation: The orientation of the graph (default: LEFT_RIGHT).
            node_shape: The shape of the nodes (default: DEFAULT).
            layout: the layout to use (default: 'dagre')
            look: the look to use (default: 'neo')
            theme: the theme to use (default: 'neutral')
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

    def build(self, graph: nx.Graph, title: str | None = None, with_edge_labels: bool = True) -> MermaidDiagram:
        """
        Materialize a graph as a Mermaid flowchart.

        Args:
            graph: The NetworkX graph to convert.
            title: The title of the graph (default: None).
                   If None, the graph name will be used if available.
                   Supplying and empty string will remove the title.
            with_edge_labels: Whether to include edge labels (default: True).

        Returns:
            A string representation of the graph as a Mermaid graph.
        """
        config = (
            f"---\n"
            f"{_graph_title(graph, title)}"
            f"config:\n"
            f"  layout: {self.layout}\n"
            f"  look: {self.look}\n"
            f"  theme: {self.theme}\n"
            f"---\n"
        )

        bra, ket = self.node_shape.value

        _us = unique_strings()

        def _next_id():
            return next(_us)

        _minified_ids = defaultdict(_next_id)

        def _minify_id(key):
            return _minified_ids[key]

        nodes = "\n".join(
            f"{_minify_id(u)}{bra}{d.get('label', u)}{ket}{_node_style(_minify_id(u), d)}" for u, d in
            graph.nodes.data())

        _edges = ((_minify_id(u), _minify_id(v), d) for u, v, d in graph.edges.data())
        edges = "\n".join(f"{u} -->{_edge_label(d) if with_edge_labels else ''} {v}" for u, v, d in _edges)

        return (
            f"{config}"
            f"graph {self.orientation.value}\n"
            f"{nodes}\n"
            f"{edges}"
        )
