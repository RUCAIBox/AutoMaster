# Checkpoint inference

Run a Hugging Face checkpoint or local model directory with the public AweAgent harness. Choose the domain recipe, supply its task assets, and point it at an OpenAI-compatible model endpoint. No generated skill is added to the evaluated Student.

## 1. Install the harness

From the AutoMaster repository root:

```bash
git submodule update --init --recursive
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e './third_party/AweAgent[search]'
```

Python 3.11+ is required. The submodule is pinned to the public version listed in the [resource index](../../docs/resources.md).

## 2. Set local configuration

```bash
cp recipes/inference/.env.example .env
# Edit .env for your model, task assets and services.
set -a
source .env
set +a
```

`.env` is ignored by Git. The harness reads exported environment variables; it does not automatically load this file. Set only the variables needed by the domain you are running.

## 3. Serve the model

Use a separate environment with SGLang, PyTorch and CUDA configured for your GPU and Qwen3.5. From the repository root in that environment:

```bash
export MODEL_PATH='/path/to/checkpoint'  # or a Hugging Face model ID
export SERVED_MODEL_NAME=automaster
bash recipes/inference/serve_qwen35.sh
```

Set `TP` for tensor parallelism, `PORT` for the listen port, and `HOST` if a remote evaluation client needs access. Defaults are TP=1, port=30000 and host=127.0.0.1. Additional arguments are passed to SGLang. For example:

```bash
TP=4 bash recipes/inference/serve_qwen35.sh --mem-fraction-static 0.85
```

Keep the checkpoint's tokenizer and chat template beside its weights. The recipes send `enable_history_reasoning=true` and `enable_thinking=true`; use a template that supports these settings so follow-up user reminders retain historical reasoning.

Alternatively, use an existing endpoint by setting `MODEL_BASE_URL`, `MODEL_API_KEY` and `SERVED_MODEL_NAME`. For BrowseComp, `MODEL_PATH` must still identify the matching tokenizer for context counting.

## 4. Prepare domain assets

| Domain | Required variables | Asset preparation |
|---|---|---|
| Terminal-Bench 2.1 | `TB_TASK_DIR`, `TB_TASK_IDS` | [AweAgent terminal recipe](../../third_party/AweAgent/recipes/terminal_bench_v2/README.md) |
| BrowseComp | `BROWSECOMP_DATA_FILE`, `MODEL_PATH`, search/summary/Judge settings below | [AweAgent search recipe](../../third_party/AweAgent/recipes/deepsearch/README.md) |
| Doc2Repo | `DOC2REPO_DATA_FILE`, `DOC2REPO_TEST_SUITE_DIR` | [AweAgent BeyondSWE recipe](../../third_party/AweAgent/recipes/beyond_swe/README.md) |

`TB_TASK_IDS` is the path to a JSON file containing an array of task IDs. `DOC2REPO_DATA_FILE` must contain the intended Doc2Repo subset, rather than all BeyondSWE task types. Terminal and Doc2Repo need Docker and accessible task images. BrowseComp does not create a task container.

### BrowseComp services

The public recipe uses SerpAPI for search and Jina for reading webpages:

- `SERPAPI_API_KEY`, `JINA_API_KEY`.
- `SUMMARY_MODEL`, `SUMMARY_BASE_URL`, `SUMMARY_API_KEY` for webpage summarization.
- `JUDGE_MODEL`, `JUDGE_BASE_URL`, `JUDGE_API_KEY` for answer grading.

Summary and Judge are separate from the Student under evaluation and accept OpenAI-compatible services. To run without grading, export `AWE_AGENT__EVAL__ENABLED=false`; search and summary services are still needed.

## 5. Execute

In the evaluation environment, from the repository root:

```bash
# Check the selected task and configuration.
awe-agent run --config recipes/inference/doc2repo.yaml --max-instances 1 --dry-run

# Execute one task.
awe-agent run --config recipes/inference/doc2repo.yaml --max-instances 1 \
  --output ./results/doc2repo-smoke

# Evaluate the supplied task set three times.
awe-agent run --config recipes/inference/doc2repo.yaml \
  --num-rollouts 3 --max-concurrent 4 --output ./results/doc2repo
```

Use `terminal.yaml` or `browsecomp.yaml` for the other domains. Choose concurrency for your resources. Results and trajectories are written beneath the output directory; preserve all repeats when computing the mean and SD.

[Evaluation settings](../../docs/evaluation.md) describe the recipe budgets and sampling parameters. These recipes use public backends; changing search providers or task assets can change evaluation results.
