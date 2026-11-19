---
name: collaborator-contracts
description: Build cooperating objects using their actual construction, activation and ownership contracts.
---

# Construct cooperating objects correctly

Apply this when a component extends a framework, constructs another component, registers
callbacks, or passes itself to a collaborator. A small independent function needs no
extra object structure. Implement the specified public behavior throughout.

## Establish who owns each operation

For the boundary you are implementing, distinguish the configuration or policy object,
the factory or adapter that consumes it, and the live object returned for use. Determine
which object owns startup, processing and cleanup. Similar names do not establish
interchangeability. In particular, a context manager and the value it yields can have
different methods and lifetimes.

For an uncertain third-party API, run a small dependency-only program before encoding
the assumption into your component. Import the actual dependency, inspect the relevant
signature or short implementation, create the minimal real object, and perform the
operation you intend to use. Print its concrete returned type and relevant state. The
dependency already exists, so this probe can run while your repository is incomplete.
Use only permitted third-party dependencies; the target project's implementation must
come from the specification and your own code.

Prefer the dependency's supported factory, registration or adapter API when constructing
its specialized objects. Preserve required field metadata, validation and lifecycle
behavior through that API. When subclassing is required, inspect what the base initializer
assigns and calls before overriding its attributes or hooks. A getter-only property can
break a base initializer that assigns that name.

## Keep construction separate from activation

Trace what a child constructor or registration call does immediately. A call such as
`Child(self)` can read the parent or invoke callbacks before it returns. Establish every
required parent invariant before that call:

```python
self.config = validated_config
self.state = initial_state
self.listeners = []
# Child may now read these fields during its constructor.
self.child = Child(self)
# Activate only after the cooperating objects are ready.
register(self.child)
```

Derive the actual fields and order from the callee's implementation and specification.
Use meaningful initial values. If two objects require each other, separate allocation
and configuration from the operation that activates their interaction. Some frameworks
copy registration data: complete configuration before the consuming registration call,
and use an explicit supported update mechanism for later changes.

## Verify the actual collaboration

Exercise the public entry path once the cooperating objects exist. Observe the required
state, result or event after activation, and a specified alternate or failure case.
Keep lifecycle management on its actual owner, including cleanup on exceptional paths.
Mock external effects when needed, while retaining real constructors and framework
dispatch at the boundary being checked. A mock that accepts arbitrary methods cannot
establish that the real protocol works.

On a boundary failure, inspect the first mismatched owner, field or lifecycle phase;
repair that decision and rerun the same entry path. Preserve the demonstrated contract
while completing the remaining repository features and final verification.
