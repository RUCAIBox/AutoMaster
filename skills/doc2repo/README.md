# Repository construction

Three selected original skills from AutoMaster research runs. Each skill is a self-contained directory with a `SKILL.md` entrypoint.

| Skill | When it is useful | Evidence in the archive |
|---|---|---|
| [collaborator-contracts](collaborator-contracts/SKILL.md) | Probe actual dependency construction, activation and ownership contracts before building cooperating objects. | Paired FastAPI/TestClient case; included in training. |
| [run-observed-public-call](run-observed-public-call/SKILL.md) | Exercise the real public call chain and record effects at the external boundary instead of mocking away owned code. | Paired HTTP-client case; both executions remained partially correct. |
| [owned-regions](owned-regions/SKILL.md) | Give each parser layer explicit ownership of an input region, then verify child-to-parent and sibling handoff. | Paired nested-stream case; included in training. |
