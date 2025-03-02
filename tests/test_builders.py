import networkx as nx
import pytest

from networkx_mermaid import DiagramNodeShape, DiagramOrientation
from networkx_mermaid.builders import (
    DEFAULT_LAYOUT,
    DEFAULT_LOOK,
    DEFAULT_THEME,
    DiagramBuilder,
    _contrast_color,
    _edge_label,
    _graph_title,
    _node_style,
)


def test_default_initialization():
    # Arrange
    builder = DiagramBuilder()

    # Act & Assert
    assert builder.orientation == DiagramOrientation.LEFT_RIGHT
    assert builder.node_shape == DiagramNodeShape.DEFAULT
    assert builder.layout == DEFAULT_LAYOUT
    assert builder.look == DEFAULT_LOOK
    assert builder.theme == DEFAULT_THEME


def test_custom_initialization():
    # Arrange
    builder = DiagramBuilder(
        orientation=DiagramOrientation.TOP_DOWN,
        node_shape=DiagramNodeShape.RECTANGLE,
        layout="elk",
        look="neo",
        theme="neutral"
    )

    # Act & Assert
    assert builder.orientation == DiagramOrientation.TOP_DOWN
    assert builder.node_shape == DiagramNodeShape.RECTANGLE
    assert builder.layout == "elk"
    assert builder.look == "neo"
    assert builder.theme == "neutral"


def test_invalid_orientation_type():
    # Arrange & Act & Assert
    with pytest.raises(TypeError):
        DiagramBuilder(orientation="invalid")


def test_invalid_node_shape_type():
    # Arrange & Act & Assert
    with pytest.raises(TypeError):
        DiagramBuilder(node_shape="invalid")


def test_build_empty_graph():
    # Arrange
    graph = nx.Graph()
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "graph LR" in diagram


def test_build_simple_graph():
    # Arrange
    graph = nx.Graph()
    graph.add_edge(1, 2)
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "graph LR" in diagram
    assert "1(1)" in diagram
    assert "2(2)" in diagram
    assert "1 --> 2" in diagram


def test_build_graph_with_node_labels():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1, label="Node 1")
    graph.add_node(2, label="Node 2")
    graph.add_edge(1, 2)
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "1(Node 1)" in diagram
    assert "2(Node 2)" in diagram


def test_build_graph_with_edge_labels():
    # Arrange
    graph = nx.Graph()
    graph.add_edge(1, 2, label="Edge 1-2")
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "1 -->|Edge 1-2| 2" in diagram


def test_build_graph_with_node_colors():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1, color="#FF0000")
    graph.add_node(2, color="#00FF00")
    graph.add_edge(1, 2)
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "style 1 fill:#FF0000, color:#ffffff" in diagram
    assert "style 2 fill:#00FF00, color:#ffffff" in diagram


def test_build_graph_with_custom_node_shape():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder(node_shape=DiagramNodeShape.RECTANGLE)

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "1[1]" in diagram


def test_build_graph_with_custom_orientation():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder(orientation=DiagramOrientation.TOP_DOWN)

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "graph TD" in diagram


def test_build_graph_with_custom_layout():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder(layout='elk')

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "layout: elk" in diagram


def test_build_graph_with_custom_look():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder(look='neo')

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "look: neo" in diagram


def test_build_graph_with_custom_theme():
    # Arrange
    graph = nx.Graph()
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder(theme='neutral')

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "theme: neutral" in diagram


def test_build_graph_with_title():
    # Arrange
    graph = nx.Graph(name="My Graph")
    graph.add_node(1)
    graph.add_edge(1, 1)
    builder = DiagramBuilder()

    # Act
    diagram = builder.build(graph)

    # Assert
    assert "title: My Graph" in diagram


def test_edge_label_with_label():
    # Arrange
    data = {"label": "Edge Label"}

    # Act
    result = _edge_label(data)

    # Assert
    assert result == "|Edge Label|"


def test_edge_label_without_label():
    # Arrange
    data = {}

    # Act
    result = _edge_label(data)

    # Assert
    assert result == ""


@pytest.mark.parametrize(
    ('color', 'expected_contrast'),
    [
        ("#FFFFFF", "#000000"),
        ("#000000", "#ffffff"),
        ("#FF0000", "#ffffff"),
        ("#00FF00", "#ffffff"),
        ("#0000FF", "#ffffff"),
        ("#ABCDEF", "#000000"),
        ("#123456", "#ffffff"),
    ],
)
def test_contrast_color_valid_hex(color, expected_contrast):
    # Arrange (done by parametrizing)
    # Act
    result = _contrast_color(color)

    # Assert
    assert result == expected_contrast


@pytest.mark.parametrize(
    "color",
    ["FFFFFF", "#FFFFF", "#GGGGGG", 123456, None],
)
def test_contrast_color_invalid_hex(color):
    # Arrange (done by parametrizing)
    # Act & Assert
    with pytest.raises(ValueError):
        _contrast_color(color)


def test_node_style_with_color():
    # Arrange
    data = {"color": "#FF0000"}

    # Act
    result = _node_style("1", data)

    # Assert
    assert result == "\nstyle 1 fill:#FF0000, color:#ffffff"


def test_node_style_without_color():
    # Arrange
    data = {}

    # Act
    result = _node_style("1", data)

    # Assert
    assert result == ""


def test_graph_title_with_name():
    # Arrange
    graph = nx.Graph(name="My Graph")

    # Act
    result = _graph_title(graph)

    # Assert
    assert result == "title: My Graph\n"


def test_graph_title_without_name():
    # Arrange
    graph = nx.Graph()

    # Act
    result = _graph_title(graph)

    # Assert
    assert result == ""
