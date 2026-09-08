# Reproduction and test exits

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Python 3.13.9, SymPy 1.13.1; existing g03j uses NumPy 1.26.4.
No installation, new data download, or large dynamics run was required.

## Important commands actually executed

```bash
git status --short
git log -6 --oneline
git remote -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/g03j_scalar_carrier_kernel.py
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol.py --require-causal-conserved-source-response
```

| Command | Observed exit | Meaning |
|---|---:|---|
| New tests, before implementation | 5 | Expected red: assertion that implementation was missing; no tests ran |
| New tests, final implementation | 0 | 8 regression tests passed; not 8 full-theory gates |
| Existing g03j | 0 | Its four checks reproduce under its assumed carrier dictionary |
| Existing cluster audit | 0 | 9 regression tests passed |
| Existing metric causal symbol | 0 | 10 algebraic consistency checks passed |
| Same causal symbol, finite-speed requirement enabled | **2** | Physical acceptance gate rejected its exponential principal system; not an execution crash |
| Bounded Gate 1 computation below | 0 | Exact identities and static bracket computation completed |
| Manifest validator below | 0 | Recorded hashes/provenance valid; not a mathematical proof |

g03j's exit zero does not independently connect its source equation to the
full action. The causality run's ten successful internal checks are precisely
what establish its conditional failure of the physical acceptance criterion.
The unmodified metric causality files were used without `--output`, so no
archived evidence was overwritten. Its imported dependency is
`../g03_global_kernel_bridge_2026/metric_constraint.py`.

## Exact bounded-run command used

```bash
OPENBLAS_NUM_THREADS=1 python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/contract.json --input qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/constitutive_gate.py --input qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/test_constitutive_gate.py --input qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md --input qwen_claude_field_theory/closure_2026/g03t_flrw_linear_from_action.py --input hunt_2026/f33b_ppn_k4_clock_host_healthy.py --input qwen_claude_field_theory/closure_2026/g03j_scalar_carrier_kernel.py --output qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/run_001 --result qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/run_001/result.json --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- python -B qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/constitutive_gate.py --output qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/run_001/result.json
OPENBLAS_NUM_THREADS=1 python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

`run_001` must not already exist for the bounded runner. To reproduce without
writing any results, run the child command with no `--output`; it prints a
summary and derives everything again. For a new provenance run, choose a
fresh output directory and replace ALL three occurrences of `run_001`.
The runner is optional tooling; the computation itself depends only on SymPy
and Python. The command never loads or executes the theory source files;
their correspondence to the reduced density is independently reviewed and
their literal versions are pinned as provenance inputs.

## Exact files newly created in this change

All under `qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/`:

- `constitutive_gate.py`
- `test_constitutive_gate.py`
- `CONSTITUTIVE_DECISION.md`
- `REPRODUCE.md`
- `contract.json`
- `run_001/result.json`
- `run_001/manifest.json`
- `run_001/stdout.txt`
- `run_001/stderr.txt` (empty, recorded and hashed)

No original action, simulation, preregistration or unrelated dirty file was
modified. The mathematical result is scoped to the explicit static actions
and limits in the decision note. Full-theory status remains **OPEN**.
