## 2024-05-23 - Local Variable Caching for Loop Optimization
**Learning:** In `builders.py`, caching method lookups (`minifier.get`) and global function lookups (`_node_style`) to local variables before the loop resulted in a ~30% performance improvement (from ~10ms to ~7ms for 1000 nodes). This confirms that repeated attribute and global lookups are a measurable bottleneck in tight loops in this codebase.
**Action:** Always cache `AutoMapper.get` and frequently used global functions to local variables before iterating over large graphs.
