---
name: execute-numeric-decision
description: Make numerical acceptance an executed decision and use a failed comparison to direct the repair.
---

# Execute the numerical decision

When correctness depends on numerical accuracy or convergence, put the relevant acceptance condition into the check you run. Adapt this finite-scalar example to the task's actual error convention:

```python
error = abs(actual - reference)
passed = math.isfinite(error) and error <= allowed_error
print(actual, reference, error, allowed_error, "PASS" if passed else "FAIL")
assert passed, "numerical requirement remains unresolved"
```

Define the reference and bound before running this block. Use the specified absolute, relative, or norm error and strictness; the example does not authorize substituting absolute error for a relative requirement. Keep prescribed input scale and iteration budget. If no bound is specified, justify a diagnostic bound and label it as such. An existing test that already makes the decision suffices. Returning a comparison from a test function does not enforce it: its result must reach the assertion or failure branch.

Base the reference on an independent analytic case, trusted implementation, or mathematical identity. Preserve exact comparisons for discrete results. Treat zero references and expected NaN/Inf according to the interface; apply finite-value checks only where finite output is required.

If the check fails, retain that case and condition while investigating. Save a random failing input or its reproducible seed. A common scale error suggests units, normalization or weights; an error near the bound suggests stopping criteria or error estimates. Inspect the responsible computation, make a justified correction, and rerun the same condition. Correct a mistaken reference only from independent evidence. Do not widen a required tolerance or replace a failing input with a passing one.

Connect completion to the observed decision, or state the unresolved requirement. More suites and repeated unchanged runs are unnecessary.
