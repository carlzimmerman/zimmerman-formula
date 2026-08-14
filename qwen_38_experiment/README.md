# qwen_38_experiment — the grunt-work autoresearch kit

A self-contained harness for a local worker model (Qwen-class) to run 100 pre-scoped,
falsifiable experiments on the Zimmerman programme, HRM-style: plan at the task level,
execute as deterministic scripts, grade against pre-stated criteria, remember everything
in an append-only ledger, and consolidate every 10 tasks. Honesty machinery is built in:
FDR pre-registration for every search, a DO-NOT-CITE linter, refutation duties for every
confirmed result, and negative results treated as first-class output.

## Files

| file | purpose |
|---|---|
| `PROTOCOL.md` | **The operating loop.** Read before every task. Hard rules R1–R10. |
| `SYSTEM_PROMPT.md` | Paste-in system prompt for the worker model. |
| `TASKS.md` | The 100 tasks: hypothesis · method · PASS · KILL, ranked by breakthrough potential. |
| `qwenlib.py` | Single source of constants + the framework kernel + `check()/finish()`. Regression-pinned. |
| `runs/_template.py` | Task-script template. One script per task: `runs/tNNN_<slug>.py`. |
| `harness.py` | Runner: executes a task script, enforces exit-code truth, appends a ledger row skeleton. |
| `LEDGER.md` | Append-only results memory (schema in PROTOCOL.md). |
| `REGISTRY_FDR.md` | Pre-registered trial counts for every search. No entry → search invalid. |
| `ESCALATE.md` | Decisions reserved for Carl (amendments, publications, retractions). |
| `OPEN_THREADS.md` | The living top-3 threads, refreshed at each consolidation task. |

## Quick start (for the worker model)

1. Read `PROTOCOL.md` fully. 2. `python harness.py runs/t085_kernel_regression.py "qwenlib pins"` —
build T085 first (the canary), then T081–T084 (infrastructure), then go in order or by
Carl's pick. 3. Every session ends with the ledger current and nothing outside this
folder touched.

## Boundaries (absolute)

Work only inside `qwen_38_experiment/`. Never push. Never touch `PREREGISTRATION_DR4.md`
or any `*_HASH.txt`. Never publish. Carl reviews, commits, and decides escalations.
