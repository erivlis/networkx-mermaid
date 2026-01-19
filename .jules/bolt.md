## 2026-01-16 - Method Lookup Overhead in Hot Loops
**Learning:** Hoisting `AutoMapper.get` to a local variable in the main node loop reduced build time by ~40% (0.39s -> 0.23s for 100k nodes). Python's attribute lookup in tight loops is a measurable bottleneck.
**Action:** Identify and hoist method lookups in all core builder loops involving large node/edge counts.

## 2026-01-16 - Global Lookup and List Append Overhead
**Learning:** Hoisting `list.append` and global function lookups (`_node_style`, `_edge_label`) in `DiagramBuilder.build` further reduced build time by ~53% (1.17s -> 0.55s for 200k nodes).
**Action:** Always hoist global lookups and method attributes (like `list.append`) inside hot loops.
