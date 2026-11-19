---
name: run-observed-public-call
description: Build a small executable public API scenario whose assertions require both the specified outgoing request and the returned public value.
---

# Run an observed public call

Use this procedure for a library that prepares requests, calls an external API, or adapts a dependency's response. Select one representative public operation. Write a small runnable scratch script with three parts: a specification example, the actual public invocation, and assertions over observed effects. Run it once the operation is implemented and keep the same scenario when diagnosing a failure.

In the example, state the public input, expected outgoing arguments, the external raw response, and expected public result. Derive expectations from the specification, not by printing the implementation's result and adopting it. Preserve documented verb functions, sessions, injection points and override hooks. If the boundary is unspecified, inspect the supported dependency interface. Do not replace a dependency's implementation to fit the probe.

Install a recorder at that external boundary. Keep the repository's resource wrapper, authentication, request construction and response conversion active. Use the dependency's response type or a small explicit fake with its actual signature and raw return protocol. For async operations, supply the required awaitable/context manager and await the real operation. A resource with its owned request method mocked out checks only that resource's delegation.

Make the check consume the observations, for example:

```python
# Adapt these names and expected values to the specification.
calls.clear()
result = public_operation(public_input)  # real installed package entry
assert calls == expected_calls          # nonempty for this request scenario
assert public_fields(result) == expected_fields
```

Use a fresh ledger for the call. Compare URL/method/body/options and a meaningful returned value; constructing the client or installing a mock supplies neither observation. For one sanity check of this script, omit the public invocation in a temporary copy and run it: the unchanged assertions must fail. Restore the invocation and rerun. This checks the probe, not the repository; keep that distinction in the report. A preparation-only API instead asserts the returned request fields and must not gain network execution; omission must leave its result unavailable or wrong.

An expected-error check must also fail if the operation returns normally. Use a specific exception with `pytest.raises`, or put the failure in `else`:

```python
try:
    public_operation(invalid_input)
except ExpectedError as error:
    assert expected_detail in str(error)
else:
    raise AssertionError("expected rejection")
```

If the recorder is untouched, trace the real call to the first wrong handoff. Repair that handoff or a demonstrably incorrect fixture; do not move the fake above owned code to obtain a pass. Exercise one neighboring operation or state change where behavior should differ. Mutable package configuration must affect the next call; intentionally fixed instance settings remain fixed. Keep internal control flags out of transport arguments.

Report executed paths and unresolved failures accurately. Complete the remaining repository and required verification; this one scenario is evidence about its path, not all endpoints.
