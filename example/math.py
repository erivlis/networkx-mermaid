from networkx_mermaid.builders import MermaidDiagramBuilder, NodeShape, Orientation
from networkx_mermaid.formatters import markdown, html
from networkx_mermaid.typing import MermaidDiagram

from tempfile import TemporaryDirectory

import networkx as nx


def create_graph():
    # colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
    pastel_colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#CCFFFF", "#FFCCFF"]
    graphs: list[nx.Graph] = [nx.tetrahedral_graph(), nx.dodecahedral_graph()]

    for i, g in enumerate(graphs):
        nx.set_node_attributes(g, {n: {"color": pastel_colors[i]} for n in g.nodes})

    graph: nx.Graph = nx.disjoint_union_all(graphs)

    graph.name = " + ".join(g.name for g in graphs)

    return graph


def create_builder():
    builder = MermaidDiagramBuilder(
        orientation=Orientation.LEFT_RIGHT,
        node_shape=NodeShape.ROUND_RECTANGLE,
    )
    return builder


def main():
    graph = create_graph()
    builder = create_builder()

    mermaid_diagram: MermaidDiagram = builder.build(graph)

    markdown_diagram: str = markdown(mermaid_diagram)
    html_diagram: str = html(mermaid_diagram, title=graph.name)

    print('Mermaid Diagram:')
    print(mermaid_diagram)
    print(markdown_diagram)
    print(html_diagram)

    with TemporaryDirectory() as temp_dir:
        with open(f"{temp_dir}/index.html", 'w') as f:
            f.write(html_diagram)

        import http.server
        import socketserver

        PORT = 8073

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=temp_dir, **kwargs)

        with socketserver.TCPServer(('', PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()


if __name__ == "__main__":
    main()
