from enum import Enum
from typing import Any

import networkx as nx

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


def _graph_title(graph: nx.Graph) -> str:
    """Generate a graph title string."""
    return f"title: {graph.name}\n" if graph.name else ""


class Layout(Enum):
    """Layout of a Mermaid diagram"""
    DAGRE = 'dagre'
    ELK = 'elk'


class Look(Enum):
    """Look of a Mermaid diagram"""
    NEO = 'neo'


class Theme(Enum):
    """Theme of a Mermaid diagram"""
    NEUTRAL = 'neutral'


class Orientation(Enum):
    """Orientation of a Mermaid graph"""
    TOP_DOWN = 'TD'
    BOTTOM_UP = 'BT'
    LEFT_RIGHT = 'LR'
    RIGHT_LEFT = 'RL'


class NodeShape(Enum):
    """Shapes of a Mermaid graph node"""
    DEFAULT = ("(", ")")
    RECTANGLE = ("[", "]")
    ROUND_RECTANGLE = ("([", "])")
    SUBROUTINE = ("[[", "]]")
    DATABASE = ("[(", ")]")
    CIRCLE = ("((", "))")
    DOUBLE_CIRCLE = ("(((", ")))")
    FLAG = (">", "]")
    DIAMOND = ("{", "}")
    HEXAGON = ("{{", "}}")
    PARALLELOGRAM = ("[/", "/]")
    PARALLELOGRAM_ALT = ("[\\", "\\]")
    TRAPEZOID = ("[/", "\\]")
    TRAPEZOID_ALT = ("[\\", "/]")


class MermaidDiagramBuilder:
    """
    A class to generate Mermaid diagrams from NetworkX graphs.
    """

    def __init__(
            self,
            orientation: Orientation = Orientation.LEFT_RIGHT,
            node_shape: NodeShape = NodeShape.DEFAULT,
            layout: str = DEFAULT_LAYOUT,
            look: str = DEFAULT_LOOK,
            theme: str = DEFAULT_THEME,
    ):
        """
        Initialize the MermaidDiagramGenerator.

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

        if not isinstance(orientation, Orientation):
            raise TypeError("orientation must be a valid Orientation enum")
        if not isinstance(node_shape, NodeShape):
            raise TypeError("node_shape must be a valid NodeShape enum")

    def build(self, graph: nx.Graph) -> MermaidDiagram:
        """
        Materialize a graph as a Mermaid flowchart.

        Returns:
            A string representation of the graph as a Mermaid graph.
        """
        config = (
            f"---\n"
            f"{_graph_title(graph)}"
            f"config:\n"
            f"  layout: {self.layout}\n"
            f"  look: {self.look}\n"
            f"  theme: {self.theme}\n"
            f"---\n"
        )

        bra, ket = self.node_shape.value

        nodes = "\n".join(
            f"{u}{bra}{v.get('label', u)}{ket}{_node_style(u, v)}"
            for u, v in graph.nodes.data()
        )

        edges = "\n".join(
            f"{u} -->{_edge_label(d)} {v}" for u, v, d in graph.edges.data()
        )

        return (
            f"{config}"
            f"graph {self.orientation.value}\n"
            f"{nodes}\n"
            f"{edges}"
        )

