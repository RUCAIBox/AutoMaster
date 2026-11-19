# Contributing

Use a feature branch and open a pull request against `main`.

- Keep AutoMaster-specific recipes and documentation here. Propose general inference-harness changes upstream in AweAgent.
- Each skill lives in `skills/<domain>/<name>/SKILL.md`, with `name` and `description` YAML frontmatter. Original research skills are archived versions: describe any revised variant explicitly rather than silently changing its provenance.
- Update `skills/catalog.json` and domain indexes when changing the skill collection.
- Keep downloaded weights, datasets, results and local `.env` files outside Git.

For recipe changes, parse the configuration with AweAgent, check shell syntax, and describe the relevant test in the PR. For documentation changes, verify the affected links and commands.

When updating AweAgent, check out an explicit public commit inside `third_party/AweAgent`, validate the integration, and commit the updated gitlink with the corresponding recipe changes. Do not track a moving branch or rewrite the submodule's source inside this repository.

Bug reports should include the config name, model ID/revision, AweAgent commit, relevant package versions and a small redacted error excerpt. Remove credentials and private paths before sharing logs.
