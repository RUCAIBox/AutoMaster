<div align="center">

<img src="assets/AutoMaster.png" alt="AutoMaster — a teacher robot sharing a skill with a student robot" width="760">

### Autonomous Post-Training by Making the Same Model a Better Teacher

*Beyond task success: **autonomously shaping teacher behavior to improve what students learn**.*

[Inside AutoMaster](#inside-automaster) · [Results](#results) · [Insights](#key-insights) · [Skills](skills/README.md) · [Quick start](#quick-start) · [Models & data](https://huggingface.co/collections/RUC-AIBOX/automaster) · [Citation](#citation)

[![Paper](https://img.shields.io/badge/Paper-PDF-98644f.svg?logo=arxiv&logoColor=white)](https://aweai-team.github.io/AutoMaster-site/assets/paper.pdf)
[![Homepage](https://img.shields.io/badge/Project-Homepage-606f2e.svg)](https://aweai-team.github.io/AutoMaster-site/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Collection-d5ac58.svg)](https://huggingface.co/collections/RUC-AIBOX/automaster)<br>
[![Skills](https://img.shields.io/badge/Skills-9-7c8b62.svg)](skills/README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-a29a7d.svg)](LICENSE)

</div>

**Task success alone does not specify which behaviors post-training should reinforce.** A successful teacher can still make unsupported claims, repeat unproductive searches, or test a substitute instead of the implementation it delivers.

**Skill-FT** uses natural-language skills to shape the Teacher's actual execution, then fine-tunes a Student on the resulting demonstrations. **AutoMaster** automates the research process: analyze trajectories, design and test interventions, curate data, train, evaluate, and refine.

This first release provides **nine selected skills** and **inference recipes for three domains**, backed by a pinned public [AweAgent](https://github.com/AweAI-Team/AweAgent) dependency. See the [project page](https://aweai-team.github.io/AutoMaster-site/) and [Hugging Face collection](https://huggingface.co/collections/RUC-AIBOX/automaster) for the paper and released resources. The autonomous training controller is outside this release.

## Inside AutoMaster

<p align="center">
  <a href="assets/framework.png"><img src="assets/framework.png" alt="AutoMaster: an LLM research agent analyzes trajectories, designs skills for task subsets, tests teacher rollouts, selects demonstrations, and uses Student training and evaluation feedback to guide the next round." width="100%"></a>
</p>

1. **Analyze & design.** Study Student, unguided Teacher and available reference-model trajectories to identify useful behavioral interventions.
2. **Generate & curate.** Inject selected skills into the Teacher's system prompt, execute tasks, inspect the resulting behavior, and select training demonstrations. Skills and task subsets have a many-to-many relationship.
3. **Train & evaluate.** Fine-tune the Student with skill context retained in the training input. Evaluate without adding the generated skills, then use the results to guide further research.

The Teacher stays fixed; the research agent improves how it produces teaching demonstrations. Read the [method guide](docs/method.md) for the distinction between AutoMaster, Skill-FT and the released skills.

## Results

Scores (%) with **sample SD over three evaluations**. Terminal-Bench 2.1 and BrowseComp report accuracy; Doc2Repo reports test pass rate.

<p align="center">
  <a href="assets/readme/results.svg"><img src="assets/readme/results.svg" alt="Base, Vanilla SFT and AutoMaster results for Qwen3.5-4B and 9B across Terminal-Bench 2.1, BrowseComp and Doc2Repo. Bars show mean scores with sample SD." width="100%"></a>
</p>

Vanilla SFT trains on 512 selected unguided demonstrations from the same Teacher. AutoMaster also uses 512 training examples. The selected skill library illustrates interventions explored during research; it is not the full training recipe for each checkpoint.

## Key Insights

- **Task success ≠ a good demonstration.** Even successful trajectories can contain unsupported assumptions, unproductive exploration, or superficial verification. Training on them can reinforce these habits alongside useful behaviors.

- **Better teaching without a stronger teacher.** Shaping how a fixed Teacher executes tasks can improve its demonstrations. AutoMaster improves mean Student performance by **1.42–8.99 percentage points** over Vanilla SFT, with the Teacher, task pool, training set size, and SFT recipe held fixed.

- **Generation and selection are complementary.** Skills shape the behaviors demonstrated; selection identifies valuable training examples. Removing either component lowers mean performance in all six evaluated settings, supporting their joint optimization.

- **Skill context helps behavioral internalization.** Keeping skill instructions during SFT improves mean performance by **2.15–4.01 percentage points** over removing them, with identical trajectories and supervised outputs—and no generated skills at evaluation. Explicit behavioral rules and their conditions of application offer a possible explanation.

- **Autonomous post-training benefits from exploration.** Rollout evidence and Student evaluation guide further skill design and data selection. Continued experimentation can uncover better candidates after limited progress; individual rounds need not improve monotonically.

## Explore the skills

Each skill is a self-contained folder with a `SKILL.md` entrypoint.

| Domain | A representative intervention | Start here |
|---|---|---|
| Terminal | Make a numerical requirement an executed acceptance decision | [execute-numeric-decision](skills/tb2.1/execute-numeric-decision/SKILL.md) |
| Search | Recover a stalled query by revisiting its unsupported assumption | [recover-search-anchor](skills/bc/recover-search-anchor/SKILL.md) |
| SWE | Exercise the real public call chain and observe its external effects | [run-observed-public-call](skills/doc2repo/run-observed-public-call/SKILL.md) |

Browse [all nine skills](skills/README.md). Select by the task's behavior and interfaces; there is no need to inject the entire library. Released Student inference does **not** require these skills in the prompt.

## Quick start

### 1. Get AutoMaster and the inference dependency

```bash
git clone --recurse-submodules https://github.com/RUCAIBox/AutoMaster.git
cd AutoMaster
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e './third_party/AweAgent[search]'
```

Use Python 3.11 or newer. Already cloned without submodules? Run `git submodule update --init --recursive`.

### 2. Serve a checkpoint

In a separate environment with a Qwen3.5-compatible SGLang installation:

```bash
export MODEL_PATH='/path/to/checkpoint'  # A Hugging Face model ID also works.
export SERVED_MODEL_NAME=automaster
bash recipes/inference/serve_qwen35.sh
```

Set `TP` for tensor parallelism. Keep the checkpoint's tokenizer and chat template with its weights. An existing OpenAI-compatible endpoint can also be used directly.

### 3. Run a benchmark

Configure the task assets and any required external services using the [inference guide](recipes/inference/README.md), then run one task:

```bash
awe-agent run --config recipes/inference/doc2repo.yaml --max-instances 1
```

Each domain has a YAML recipe and supports `--num-rollouts 3`. See [inference guide](recipes/inference/README.md) for time budgets, sampling and search/Judge configuration.

## Repository

```text
AutoMaster/
├── skills/                # Nine original skills, grouped by domain
├── recipes/inference/     # HF/local-model serving and evaluation configurations
├── third_party/AweAgent/  # Public inference harness, pinned Git submodule
├── docs/                  # Method and behavioral examples
└── assets/                # Project artwork and manuscript figures
```

## Acknowledgments and license

Built with [AweAgent](https://github.com/AweAI-Team/AweAgent) and Qwen3.5, evaluated on Terminal-Bench 2.1, BrowseComp and Doc2Repo. We thank the developers of these models, benchmarks and tools.

AutoMaster-authored code, documentation and skills use the [MIT License](LICENSE). AweAgent retains its [Apache-2.0 license](third_party/AweAgent/LICENSE); model weights, datasets and benchmark assets retain their own licenses.

For changes or bug reports, see [Contributing](CONTRIBUTING.md).

## Citation

<!-- Add BibTeX when the arXiv identifier is available. -->
