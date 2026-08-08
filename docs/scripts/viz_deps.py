import ast
import os
import networkx as nx
import networkx_mermaid as nxm
from pathlib import Path

def get_imports(file_path):
    """
    Parses a python file and returns a list of imported module names
    using the AST (Abstract Syntax Tree).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0]) # Get top-level module
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    return imports

def build_dependency_graph(root_dir):
    """
    Walks the directory, maps relationships, and builds a NetworkX graph.
    """
    g = nx.DiGraph(name="Project Dependencies")
    root_path = Path(root_dir)

    # Files to exclude (optional)
    EXCLUDES = {'__init__', 'tests', 'setup', 'conftest'}

    print(f"🔍 Scanning {root_dir}...")

    # First pass: Identify all modules (nodes)
    module_files = {} # module_name -> file_path

    for path in root_path.rglob("*.py"):
        module_name = path.stem

        if module_name in EXCLUDES or "test" in path.name:
            continue

        # exclude the script itself if picked up
        if path.name == "viz_deps.py":
            continue

        # Add the file as a node
        g.add_node(module_name, shape="rect")
        module_files[module_name] = path

    # Second pass: Add edges
    for module_name, path in module_files.items():
        # Find what this file imports
        imported_modules = get_imports(path)

        for imp in imported_modules:
            # Only link if the imported module exists in our project source
            if imp in g.nodes and imp != module_name:
                g.add_edge(module_name, imp)

    return g

def generate_mermaid(graph):
    """
    Uses erivlis/networkx-mermaid to generate the diagram code.
    """
    # 1. Configure the Builder
    builder = nxm.builders.DiagramBuilder(
        orientation=nxm.DiagramOrientation.LEFT_RIGHT,
        node_shape=nxm.DiagramNodeShape.ROUND_RECTANGLE
    )

    # 2. Build the Mermaid Diagram Object
    diagram = builder.build(graph)

    # 3. Format to Markdown string
    return nxm.formatters.markdown(diagram)

if __name__ == "__main__":
    # Determine project root (2 levels up from docs/scripts)
    # script is in <repo>/docs/scripts/viz_deps.py
    repo_root = Path(__file__).resolve().parent.parent.parent
    PROJECT_PATH = repo_root

    # 1. Build NetworkX Graph
    dep_graph = build_dependency_graph(PROJECT_PATH)

    print(f"✅ Graph built: {len(dep_graph.nodes)} nodes, {len(dep_graph.edges)} edges.")

    # 2. Convert to Mermaid
    mermaid_code = generate_mermaid(dep_graph)

    # 3. Output
    # Output file: <repo>/docs/dependencies.md
    output_path = repo_root / "docs" / "dependencies.md"

    print("\n--- Copy the code below into a Markdown file or GitHub Issue ---\n")
    print(mermaid_code)
    print("\n--------------------------------------------------------------")

    # Save to file
    with open(output_path, "w") as f:
        f.write(f"# Project Structure\n\n{mermaid_code}")
    print(f"📁 Saved to {output_path}")
