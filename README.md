# networkx-mermaid

Create a Mermaid graph from a NetworkX graph

## Quick Start

```python
from tempfile import TemporaryDirectory

import networkx as nx

from src import networkx_mermaid as nxm

# colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
pastel_colors = ['#FFCCCC', '#CCFFCC', '#CCCCFF', '#FFFFCC', '#CCFFFF', '#FFCCFF']
graphs: list[nx.Graph] = [nx.tetrahedral_graph(), nx.dodecahedral_graph()]

for i, g in enumerate(graphs):
    nx.set_node_attributes(g, {n: {'color': pastel_colors[i]} for n in g.nodes})

graph: nx.Graph = nx.disjoint_union_all(graphs)

graph.name = ' + '.join(g.name for g in graphs)

mermaid_diagram = nxm.mermaid(graph,
                              orientation=nxm.Orientation.LEFT_RIGHT,
                              node_shape=nxm.NodeShape.ROUND_RECTANGLE)

with TemporaryDirectory() as temp_dir:
    with open(f"{temp_dir}/index.html", 'w') as f:
        rendered = nxm.html(mermaid_diagram, title=graph.name)
        f.write(rendered)

    import http.server
    import socketserver

    PORT = 8073


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=temp_dir, **kwargs)


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
```