"""Benchmarks for `networkx_mermaid.formatters`."""

import networkx as nx
import pytest

from networkx_mermaid.builders import DiagramBuilder
from networkx_mermaid.formatters import html, markdown


@pytest.fixture(scope="session")
def medium_diagram(medium_graph: nx.Graph) -> str:
    return DiagramBuilder().build(medium_graph)


def test_markdown(benchmark, medium_diagram: str):
    assert benchmark(markdown, medium_diagram)


def test_html(benchmark, medium_diagram: str):
    assert benchmark(html, medium_diagram)


def test_html_with_title(benchmark, medium_diagram: str):
    assert benchmark(lambda: html(medium_diagram, title="Benchmark Diagram"))
