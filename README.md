# networkx-mermaid

> Create a Mermaid graph from a NetworkX graph

[![codecov](https://codecov.io/gh/erivlis/networkx-mermaid/graph/badge.svg?token=lwajrOGQ8o)](https://codecov.io/gh/erivlis/networkx-mermaid)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/f0d3c12c51d2484eb8f92e9f29615def)](https://app.codacy.com/gh/erivlis/networkx-mermaid/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2d6220d81d1a48cba762842eb88fee41)](https://app.codacy.com/gh/erivlis/networkx-mermaid?utm_source=github.com&utm_medium=referral&utm_content=erivlis/networkx-mermaid&utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/erivlis/networkx-mermaid/badge)](https://www.codefactor.io/repository/github/erivlis/networkx-mermaid)
[![DeepSource](https://app.deepsource.com/gh/erivlis/networkx-mermaid.svg/?label=active+issues&show_trend=true&token=CA0lpqHi7MBnUi3L3AIDlEsJ)](https://app.deepsource.com/gh/erivlis/networkx-mermaid/)
[![DeepSource](https://app.deepsource.com/gh/erivlis/networkx-mermaid.svg/?label=resolved+issues&show_trend=true&token=CA0lpqHi7MBnUi3L3AIDlEsJ)](https://app.deepsource.com/gh/erivlis/networkx-mermaid/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=erivlis_networkx-mermaid&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=erivlis_networkx-mermaid)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=erivlis_networkx-mermaid&metric=bugs)](https://sonarcloud.io/summary/new_code?id=erivlis_networkx-mermaid)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=erivlis_networkx-mermaid&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=erivlis_networkx-mermaid)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=erivlis_networkx-mermaid&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=erivlis_networkx-mermaid)

[![Snyk](https://snyk.io/test/github/erivlis/networkx-mermaid/badge.svg)](https://snyk.io/test/github/erivlis/networkx-mermaid)

![Test](https://github.com/erivlis/networkx-mermaid/actions/workflows/test.yml/badge.svg)
![Test](https://github.com/erivlis/networkx-mermaid/actions/workflows/test-beta.yml/badge.svg)
![Test](https://github.com/erivlis/networkx-mermaid/actions/workflows/publish.yml/badge.svg)

<a href="https://www.jetbrains.com/pycharm/"><img alt="PyCharm" src="https://img.shields.io/badge/PyCharm-FCF84A.svg?logo=PyCharm&logoColor=black&labelColor=21D789&color=FCF84A"></a>
<a href="https://github.com/astral-sh/uv"><img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" style="max-width:100%;"></a>
<a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" style="max-width:100%;"></a>
<a href="https://hatch.pypa.io"><img alt="Hatch project" class="off-glb" loading="lazy" src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg"></a>

## Example

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


def create_server(port: int, root_directory: str, open_browser: bool = True) -> threading.Thread:
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

## Example Output Diagram

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