# 2000 Astra spawn ideas for DeepSeek

**2000 individual research work orders, AS001–AS2000, in 20 groups of 100.** Their purpose is to build and rigorously test the missing links from Zimmerman's core framework to a closed theory of gravity with an explicit first-principles input budget. These are authored task specifications; the package does not claim the tasks have run or the theory is closed.

Start with the [complete 2000-task index](INDEX.md). Each linked task is a separate Markdown file directly in this folder, with its principle, equations, source hashes, explicit assumptions, inputs, ordered steps, falsifiable controls, completion criterion and output instructions. The [machine-readable manifest](manifest.json) carries the same task content and explicit dependencies.

Each task can pursue first-principles closure and branch on useful findings. The [first-principles and branching protocol](FIRST_PRINCIPLES_AND_BRANCHING.md) defines child tasks, duplicate checks, continued derivation and the conditions for a complete closure submission. Strong closure must distinguish genuinely derived inputs from adopted constitutive assumptions.

## Run the work

1. Read the [framework contract](FRAMEWORK_CONTRACT.md), which fixes the scale relation, both normalization footings and distinct gravity branches.
2. Use the [orchestration guide](ORCHESTRATOR.md) to select ready tasks, claim ownership, paste a single-task prompt into the actual DeepSeek runner and reconcile results.
3. Require the [result contract](RESULT_CONTRACT.json), source provenance and a separate mathematical review before accepting a claim.

The catalog concentrates on common-action variation, gravitational mode counting, zero-field behavior, finite-wavelength stability, source/force consistency, cosmology, transport, and calibrated observations. It also targets specific gaps in historical coefficient, entropy and equilibrium arguments. A static identity or a numerical pass remains scoped evidence until the missing dynamical and observational bridges are supplied.

The [thirteen-requirement closure map](ORCHESTRATOR.md#closure-gates-preserve-the-amended-thirteen-requirements) defines success. Results must belong to one explicit theory and an overlapping parameter domain. The adopted coefficient may remain an input as the canonical specification permits; if so, final claims must say so. Optional comparison branches are not allowed to silently replace the operative filtered-MONO target.

See [review notes](REVIEW_NOTES.md) for the cross-catalog overlap and mathematical-instruction corrections. Before dispatch, [reuse existing campaign results](REUSE_BEFORE_DISPATCH.md).

## What is in the folder

| File or area | Purpose |
|---|---|
| `AS001_*.md` … `AS2000_*.md` | Exactly 2000 individual task prompts |
| [INDEX.md](INDEX.md) | Human-readable complete task list |
| [manifest.json](manifest.json) | Structured task descriptions, dependencies and prompt hashes |
| [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) | Actual source hashes and Git provenance, including uncommitted sources |
| [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) | Equations, branch definitions, assumptions and evidence rules |
| [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md) | First-principles route, child-task protocol and full-closure escalation |
| [ORCHESTRATOR.md](ORCHESTRATOR.md) | Dispatch prompt, resource bounds, review protocol and closure gates |
| [RESULT_CONTRACT.json](RESULT_CONTRACT.json) | Required worker return fields |
| `_catalog/` | Authored source records and the renderer; these do not execute science |
| [validate_catalog.py](validate_catalog.py) | Read-only structural validator; no physics certification |
| `claims/`, `results/`, `reviews/` | Created by the actual dispatcher as work begins |

The separate [fresh-gravity follow-up namespace](fresh_gravity_followups/README.md) is owned by another campaign and linked to avoid duplicate work. Its FGF task files and research results are additional; they are not counted among these 2000 AS work orders. Preserve its ownership and original execution identities.

Validate the delivered package from the repository root:

```bash
python3 deepseek_push/astra_spawn_ideas/validate_catalog.py
```

A source change will deliberately make freshness validation fail until an orchestrator reviews the new base. Validation checks counts, schema content, links, prompt/source hashes and dependency cycles. It does not prove task novelty, feasibility of every conjecture, mathematical correctness of future results, or empirical closure. No DeepSeek API key, runner or background execution is installed by this catalog.

## Additional measurement-decade catalog

The [2017–2026 extension](measurement_decade_2017_2026/README.md) adds **2,500 individual work orders, 250 per year**, for **4,500 seeds combined**. See its [index](measurement_decade_2017_2026/INDEX.md), [100-source chronology ledger](measurement_decade_2017_2026/SOURCES.md), [single launch prompt](measurement_decade_2017_2026/LAUNCH_PROMPT.md) and the [catalog registry](CATALOG_REGISTRY.json). Original AS manifests, source pins, task files and execution ownership remain intact. The extension has its own validator and result adapter.
