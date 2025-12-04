# Usage

## Examples

### Basic
Here's a basic example of how to use `networkx-mermaid`:

```python
import networkx as nx
import networkx_mermaid as nxm

# 1. Create a NetworkX graph
G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("B", "C")

# 2. Create a diagram builder
#    The builder can be customized with different orientations, node shapes, etc.
builder = nxm.builders.DiagramBuilder()

# 3. Build the Mermaid diagram from the graph
diagram = builder.build(G)

# 4. Print the Mermaid diagram text
print(diagram)
```

This will output the following Mermaid syntax:

```mermaid
graph TD
    A --- B
    B --- C
```

### Advanced

The following is a more advanced example that demonstrates more of the library's features, taken from the project's `README.md`.

#### Code

```python title="Create a Mermaid Diagram from a NetworkX Graph"
import threading
import webbrowser
from tempfile import TemporaryDirectory

import networkx as nx
import networkx_mermaid as nxm


# An example of a graph with multiple components
def create_graph():
    pastel_colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#CCFFFF", "#FFCCFF"]
    graphs: list[nx.Graph] = [nx.tetrahedral_graph(), nx.dodecahedral_graph()]

    for i, g in enumerate(graphs):
        nx.set_node_attributes(g, {n: {"color": pastel_colors[i]} for n in g.nodes})

    graph: nx.Graph = nx.disjoint_union_all(graphs)

    graph.name = " + ".join(g.name for g in graphs)

    return graph


def create_builder():
    # Create a Mermaid Diagram Builder with custom settings

    builder = nxm.builders.DiagramBuilder(
        orientation=nxm.DiagramOrientation.LEFT_RIGHT,
        node_shape=nxm.DiagramNodeShape.ROUND_RECTANGLE,
    )
    return builder


def create_server(port: int,
                  root_directory: str,
                  open_browser: bool = True) -> threading.Thread:
    import http.server
    import socketserver

    url = f"http://localhost:{port}"

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root_directory, **kwargs)

    def serve():
        with socketserver.TCPServer(('', port), Handler) as httpd:
            print("Serving at:", url)
            httpd.serve_forever()

    server_thread = threading.Thread(target=serve)
    server_thread.daemon = True
    server_thread.start()

    if open_browser:
        webbrowser.open(url)


def main():
    graph = create_graph()
    builder = create_builder()

    # Build the Mermaid Diagram
    mermaid_diagram: nxm.typing.MermaidDiagram = builder.build(graph)

    # Format the Mermaid Diagram for Markdown embedding
    markdown_diagram: str = nxm.formatters.markdown(mermaid_diagram)

    # or as single page HTML
    html_diagram: str = nxm.formatters.html(mermaid_diagram, title=graph.name)

    print('Mermaid Diagram:')
    print(mermaid_diagram)
    print(markdown_diagram)
    print(html_diagram)

    ## Save the HTML diagram to a file and serve it
    with TemporaryDirectory() as temp_dir:
        with open(f"{temp_dir}/index.html", 'w') as f:
            f.write(html_diagram)

        # Serve the HTML diagram
        create_server(port=8073, root_directory=temp_dir, open_browser=True)

        # Keep the main thread alive to allow the server to run
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Server stopped")


if __name__ == "__main__":
    main()
```

#### Output

```mermaid
---
title: Platonic Tetrahedral Graph + Dodecahedral Graph
config:
  layout: dagre
  look: neo
  theme: neutral
---
graph LR
    AAA([0])
    style AAA fill: #FFCCCC, color: #000000
    AAE([1])
    style AAE fill: #FFCCCC, color: #000000
    AAI([2])
    style AAI fill: #FFCCCC, color: #000000
    AAM([3])
    style AAM fill: #FFCCCC, color: #000000
    AAQ([4])
    style AAQ fill: #CCFFCC, color: #000000
    AAU([5])
    style AAU fill: #CCFFCC, color: #000000
    AAY([6])
    style AAY fill: #CCFFCC, color: #000000
    AAc([7])
    style AAc fill: #CCFFCC, color: #000000
    AAg([8])
    style AAg fill: #CCFFCC, color: #000000
    AAk([9])
    style AAk fill: #CCFFCC, color: #000000
    AAo([10])
    style AAo fill: #CCFFCC, color: #000000
    AAs([11])
    style AAs fill: #CCFFCC, color: #000000
    AAw([12])
    style AAw fill: #CCFFCC, color: #000000
    AA0([13])
    style AA0 fill: #CCFFCC, color: #000000
    AA4([14])
    style AA4 fill: #CCFFCC, color: #000000
    AA8([15])
    style AA8 fill: #CCFFCC, color: #000000
    ABA([16])
    style ABA fill: #CCFFCC, color: #000000
    ABE([17])
    style ABE fill: #CCFFCC, color: #000000
    ABI([18])
    style ABI fill: #CCFFCC, color: #000000
    ABM([19])
    style ABM fill: #CCFFCC, color: #000000
    ABQ([20])
    style ABQ fill: #CCFFCC, color: #000000
    ABU([21])
    style ABU fill: #CCFFCC, color: #000000
    ABY([22])
    style ABY fill: #CCFFCC, color: #000000
    ABc([23])
    style ABc fill: #CCFFCC, color: #000000
    AAA --> AAE
    AAA --> AAI
    AAA --> AAM
    AAE --> AAI
    AAE --> AAM
    AAI --> AAM
    AAQ --> AAU
    AAQ --> ABc
    AAQ --> AA4
    AAU --> AAY
    AAU --> AAw
    AAY --> AAc
    AAY --> AAo
    AAc --> AAg
    AAc --> ABc
    AAg --> AAk
    AAg --> ABU
    AAk --> AAo
    AAk --> ABM
    AAo --> AAs
    AAs --> AAw
    AAs --> ABI
    AAw --> AA0
    AA0 --> AA4
    AA0 --> ABE
    AA4 --> AA8
    AA8 --> ABA
    AA8 --> ABY
    ABA --> ABE
    ABA --> ABQ
    ABE --> ABI
    ABI --> ABM
    ABM --> ABQ
    ABQ --> ABU
    ABU --> ABY
    ABY --> ABc
```