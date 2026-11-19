---
name: preserve-reference-operations
description: Speed up equivalent implementations by retaining operations that determine exact outputs and changing the surrounding work first.
---

Use when optimizing correct code or filling a faster implementation that must match a supplied reference. Before rewriting, identify the operations that determine the promised output: selection/order, numeric reduction, conversion and state changes.

Keep those actual operations initially. Accelerate the expensive work around them: remove repeated lookups, prepare contiguous data once, batch independent computation, improve access paths, or replace expensive row access. Preserve numeric precision and operation order when exact values are required. Algebraic equivalence alone does not preserve floating-point keys or sums. Keep existing public functions, including slow reference helpers, available.

For ranked outputs, retain the reference's actual sorting/selection operation after accelerating key computation. Do not replace its tie behavior with a convenient policy. If the task requires a native implementation, a library call through its supported interface may preserve that operation; otherwise port its observed semantics explicitly. A cheaper subset selection followed by sorting is not equivalent when the cutoff intersects equal keys.

Measure this conservative implementation against the required performance target. Only if it is still too slow, change one remaining costly operation at a time and compare that change with the unchanged reference on a small discriminating input plus the normal workload. Compare all promised outputs, including caller state. Keep a mismatch as a failure until repaired; do not quietly relax exact equality to numerical similarity.

This preserves required behavior, not a broken reference or a forbidden slow algorithm. If the task explicitly permits different valid choices, use its objective/feasibility requirement. Finish with the actual final consumer and performance result.
