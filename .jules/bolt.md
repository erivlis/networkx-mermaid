## 2025-05-23 - Micro-optimization in Hex Color Parsing
**Learning:** Parsing a hex color string (e.g., "#RRGGBB") as a single integer and using bitwise operations to extract RGB components is ~1.6x faster than slicing the string and calling `int()` three times.
**Action:** Use bitwise extraction for color manipulation in performance-sensitive loops.
