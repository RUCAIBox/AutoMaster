# Evaluation recipes

The recipes evaluate the Student without generated skills. These are the settings in the checked-in public YAML files; paper scores are reported separately on the repository homepage.

## Budgets and execution

| Setting | Terminal-Bench 2.1 | BrowseComp | Doc2Repo |
|---|---|---|---|
| Scaffold | `calibforge` | `fold_search` | `search_swe`, search disabled |
| Agent wall-clock budget | 10,800 s / 3 h | Step and context budget | 14,400 s / 4 h |
| Maximum steps | 500 | 600 | 400 |
| Evaluator timeout | 3,600 s | 3,600 s | 7,200 s |
| Bash default / maximum timeout | 1,800 / 3,600 s | Not applicable | 3,600 / 3,600 s |
| Bash output limit | 65,536 characters | Not applicable | 32,000 characters |
| Model request timeout | 1,200 s | 1,200 s | 1,200 s |
| Default concurrent tasks | 1 | 1 | 1 |
| Default rollouts per task | 1 | 1 | 1 |

Use `--num-rollouts 3` for three evaluations. `execution.max_retries=1` means one task attempt in this harness. LLM and search-service request retries are separate settings.

The 12-hour runtime timeout is a container setting, not an additional model-generation budget. Verifier execution is separate from the agent wall-clock budget.

## Model sampling

| Parameter | Terminal | BrowseComp | Doc2Repo |
|---|---|---|---|
| Temperature | 1.0 | 1.0 | 1.0 |
| Top-p | 0.95 | 0.95 | 0.95 |
| Completion budget | `max_completion_tokens=16384` | Dynamic `max_tokens`, capped at 65,500 | `max_completion_tokens=16384` |
| Presence penalty | Server default | 1.5 | Server default |
| Top-k / min-p / repetition penalty | Server defaults | 20 / 0.0 / 1.0 | Server defaults |
| Preserve historical reasoning | Enabled | Enabled | Enabled |

BrowseComp uses the matching tokenizer and a 261,120-token context budget. It folds older tool observations when their combined content exceeds 32,000 tokens, targeting 5,000 while retaining the two most recent tool observations. It requests a final answer when remaining context falls below 8,192 tokens. Full observations remain in saved interaction records.

The summary and Judge requests use temperature 0 and `max_completion_tokens=8192`. Configure their model names and endpoints in your environment.

## Reading results

Terminal and BrowseComp use task accuracy. Doc2Repo uses a test-pass fraction per task, averaged over the task set. For repeated evaluation, compute a score for each complete repeat, then report the mean and sample SD of those repeat scores. Keep the task set, checkpoint and inference settings fixed across repeats.

Record the model revision, AweAgent commit, task IDs, task images, server configuration and auxiliary search/Judge models with each evaluation. The public BrowseComp recipe uses SerpAPI/Jina; the choice of search and reader backend affects retrieved evidence.

## Common setup issues

- **Missing submodule:** run `git submodule update --init --recursive` from the repository root.
- **Model not found at the endpoint:** match `SERVED_MODEL_NAME` to the server's served name; include `/v1` in `MODEL_BASE_URL` for an OpenAI-compatible chat endpoint.
- **Earlier reasoning disappears:** use the model's history-reasoning-aware template and keep the recipe's `chat_template_kwargs`.
- **BrowseComp cannot load a tokenizer:** set `MODEL_PATH` to the same model/tokenizer revision as the serving endpoint and install AweAgent's `[search]` extra.
- **Search or grading fails:** check the search, reader, summary and Judge settings separately; they are not the evaluated Student endpoint.
- **Code tasks cannot start:** verify Docker access and the availability of the dataset's task images and test assets.
