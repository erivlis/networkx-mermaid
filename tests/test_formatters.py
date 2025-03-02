from networkx_mermaid.formatters import html, markdown


def test_markdown():
    # Arrange
    diagram = "graph LR\nA-->B"

    # Act
    result = markdown(diagram)

    # Assert
    assert result == "```mermaid\ngraph LR\nA-->B\n```"


def test_html_without_title():
    # Arrange
    diagram = "graph LR\nA-->B"
    expected_html_template = """<!doctype html>
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
graph LR
A-->B
    </pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      let config = { startOnLoad: true, flowchart: { useMaxWidth: false, htmlLabels: true } };
      mermaid.initialize(config);
    </script>
  </body>
</html>
"""

    # Act
    result = html(diagram)

    # Assert
    assert result == expected_html_template


def test_html_with_title():
    # Arrange
    diagram = "graph LR\nA-->B"
    title = "My Diagram"
    expected_html_template = """<!doctype html>
<html lang="en">
  <head>
    <link rel="icon" type="image/x-icon" href="https://mermaid.js.org/favicon.ico">
    <meta charset="utf-8">
    <title>My Diagram</title>
    <style>
    pre.mermaid {
      font-family: "Fira Mono", "Roboto Mono", "Source Code Pro", monospace;
    }
    </style>
  </head>
  <body>
    <pre class="mermaid">
graph LR
A-->B
    </pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      let config = { startOnLoad: true, flowchart: { useMaxWidth: false, htmlLabels: true } };
      mermaid.initialize(config);
    </script>
  </body>
</html>
"""

    # Act
    result = html(diagram, title=title)

    # Assert
    assert result == expected_html_template
