## 2026-01-16 - Method Lookup Overhead in Hot Loops
**Learning:** Hoisting `AutoMapper.get` to a local variable in the main node loop reduced build time by ~40% (0.39s -> 0.23s for 100k nodes). Python's attribute lookup in tight loops is a measurable bottleneck.
**Action:** Identify and hoist method lookups in all core builder loops involving large node/edge counts.
