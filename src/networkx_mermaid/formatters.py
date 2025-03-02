from .typing import MermaidDiagram

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <link rel="icon" type="image/x-icon" href="https://mermaid.js.org/favicon.ico">
    <meta charset="utf-8">
    <title>Mermaid Diagram</title>
    <style>
    pre.mermaid {
      font-family: "Fira Mono", "Roboto Mono", "Source Code Pro", monospace;
    }
    </style>
  </head>
  <body>
    <pre class="mermaid">
    </pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      let config = { startOnLoad: true, flowchart: { useMaxWidth: false, htmlLabels: true } };
      mermaid.initialize(config);
    </script>
  </body>
</html>
"""


def markdown(diagram: MermaidDiagram) -> str:
    """
    Generate Markdown code for a Mermaid diagram.
    """
    return f"```mermaid\n{diagram}\n```"


def html(diagram: MermaidDiagram, title: str | None = None) -> str:
    """
    Generate HTML code for a Mermaid diagram.
    """
    output = HTML_TEMPLATE.replace(
        '<pre class="mermaid">', f'<pre class="mermaid">\n{diagram}'
    )
    if title:
        output = output.replace(
            "<title>Mermaid Diagram</title>", f"<title>{title}</title>"
        )
    return output
