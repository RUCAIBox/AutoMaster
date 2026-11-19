# Skills discovered by AutoMaster

Nine selected skills from historical AutoMaster research runs, organized by domain:

- [Terminal tasks](tb2.1/README.md): numerical acceptance, final-deliverable verification, and semantics-preserving optimization.
- [BrowseComp / web search](bc/README.md): stalled-search recovery, faithful interpretation of measurements, and source-language retrieval.
- [Repository construction](doc2repo/README.md): dependency contracts, observable public calls, and parser ownership.

Each skill has its own directory and a `SKILL.md` with `name` and `description` frontmatter. The original skill text is preserved byte-for-byte. Domain indexes describe applicability and available evidence; `catalog.json` records file paths and hashes.

## Use

Choose skills whose stated conditions match the task. In AutoMaster, selected skill bodies guide the Teacher through its system prompt during execution. Different task subsets can use different combinations; one task may use several skills, and one skill may serve many tasks. These entries are not a bundle to inject wholesale.

For Codex-style installation, copy an individual skill directory into the skill discovery directory used by your agent, rather than copying the enclosing domain folder. The files specify behavior; they do not install tools or grant permissions.

These are Teacher-generation skills. The released Student checkpoints use the inference recipes without requiring these skills in their prompts. This collection illustrates reusable interventions from research runs; it is not the complete training recipe for every checkpoint. Case evidence and training inclusion do not by themselves establish an isolated skill's effect on student performance.
