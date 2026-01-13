## 2025-05-13 - [Loop Fusion and Inlining]
**Learning:** Merging node mapping lookup with processing loop and inlining small helper functions (`_node_style`, `_edge_label`) reduced execution time by ~3% in `DiagramBuilder.build`. Explicit loops with `list.append` performed similarly to generator expressions, but avoiding double iteration and function call overheads provided the edge.
**Action:** When optimizing tight loops in builders, prefer explicit single-pass loops and inline small conditional logic to minimize overhead.
