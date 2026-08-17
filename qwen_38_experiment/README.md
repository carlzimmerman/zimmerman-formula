# qwen_38_experiment — the grunt-work autoresearch kit

A self-contained harness for a local worker model (Qwen-class) to run 100 pre-scoped,
falsifiable experiments on the Zimmerman programme, HRM-style: plan at the task level,
execute as deterministic scripts, grade against pre-stated criteria, remember everything
in an append-only ledger, and consolidate every 10 tasks. Honesty machinery is built in:
FDR pre-registration for every search, a DO-NOT-CITE linter, refutation duties for every
confirmed result, and negative results treated as first-class output.


## ⭐ CURRENT PRIORITY: the dust front (open problem 2d)

As of 2026-08-17 the dispatcher's top task tier is `DUST_TASKS.md` (D001–D012) — the
framework's #1 open problem. **Run `python dust_filters.py --explain` at the start of every
dust session.** It implements five free filters, three of them parameter-free, each fatal
alone; two of them (F4 the calibration-independent barotropic violation at Γ = 4/3, and F5
the parameter-free 0.194 gate-sign crossover) are new, and either one alone would have killed
a construction the corpus spent real time on. Screen candidates with
`python dust_filters.py --screen spec.json` (exit 0 = screened, exit 2 = dead) *before*
spending a session. A candidate that passes is **SCREENED, never VIABLE**.

`python dust_filters.py --selftest` gates every number against a committed result (14/14).


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

## Reading the rest of the repository — encouraged; writing it — forbidden

**READ freely from every folder in zimmerman-formula.** That is where the committed
physics lives, and tasks are expected to pull from it:

- `nbody_2026/stage*.py` — the committed results record (stages 1–64); import their
  numbers by re-deriving or copying WITH a provenance comment naming the stage.
- `opus_48_extended_research/papers/` — THE_COMPLETION.md (the field theory),
  PINNING_Q0_IN_AEST.md (the Q₀ pin), DR4_TARGET_UNDER_LOCAL_A0.md, and the rest.
- `real_research/bridge1_aest_equations.md` — the exact SZ21 perturbation equations,
  verbatim-verified; the ONLY approved source for AeST linear theory.
- `real_research/`, `prep_2026/` — pipelines, data loaders, SPARC/KiDS machinery
  (you may import their functions read-only or copy them into `runs/` with attribution).
- `STANDING.md`, `RETRACTIONS.md` — check BEFORE citing any verdict; if a claim you
  need appears in RETRACTIONS.md, it is dead — do not resurrect it.

**WRITE only inside `qwen_38_experiment/`.** Never modify, move, or delete anything
outside this folder — not even a typo fix (note it in ESCALATE.md instead). Never touch
`PREREGISTRATION_DR4.md` or any `*_HASH.txt` (hash-frozen; verify with T082, never edit).
Never `git push`, never publish. If a task needs data that only exists outside the repo,
mark it BLOCKED and name the dataset. Carl reviews, commits, and decides escalations.
