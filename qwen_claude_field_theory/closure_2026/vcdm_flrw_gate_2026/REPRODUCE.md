# Reproduce the FLRW rejection

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Reviewed base: `89588dd6f76c1996d8deee5cf6084eec41c2e614`.
Environment: Python 3.13.9, SymPy 1.13.1, SciPy 1.14.1, NumPy 1.26.4.
No new packages or observational datasets were required.

## Commands and observed exit status

```bash
git status --short
git log -4 --oneline
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py --require-healthy-flrw
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_causal_symbol.py --require-causal-conserved-source-response
git diff --check
```

| Test/run | Exit | What it establishes |
|---|---:|---|
| New test suite | 0 | 10 regression/control tests pass |
| New calculation, default mode | 0 | Derivation completed; printed physical verdict is FAILED |
| New calculation, `--require-healthy-flrw` | **2** | Physical acceptance requirement fails; not a crash |
| Prior Gate 1 suite | 0 | 8 tests pass |
| Cluster measurement suite | 0 | 9 tests pass |
| Prior metric causal acceptance gate | **2** | Its 10 algebraic checks pass, finite-speed criterion fails in its stated scope |
| Manifest validation below | 0 | Input/output hashes and execution record validate |
| Diff whitespace check | 0 | No whitespace errors |

Development red tests failed as intended before missing computations were
implemented (exit 1). One intermediate control test omitted the canonical
fixture D=Z=1 after generalizing the code to P(X); it correctly returned D
rather than 1. The fixture was specified explicitly, and a separate radiation
control now verifies D=6, Z=2 gives speed squared 1/3. No production sign was
changed to manufacture a positive or negative physical result.

## Exact provenance-run command executed

```bash
OPENBLAS_NUM_THREADS=1 python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/contract.json --input qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py --input qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/test_vcdm_flrw.py --input qwen_claude_field_theory/closure_2026/gate1_constitutive_2026/CONSTITUTIVE_DECISION.md --output qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/run_001 --result qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/run_001/result.json --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- python -B qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py --output qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/run_001/result.json
OPENBLAS_NUM_THREADS=1 python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The runner output directory must be fresh. For a new recorded reproduction,
replace all three occurrences of `run_001` with a new directory name. To
recompute without writing any file, use the standalone script with no
`--output`. Archived results are never overwritten; output creation is
exclusive. The runner's exit 0 records successful computation, not a healthy
theory. The saved result has `acceptance: false`.

The script derives the quadratic action, the full six-constraint scalar Poisson matrix,
preservation equations, homogeneous constraints, vacuum rank change and exact
control solutions. No expected ranks, determinants, PPN values or mode counts
are supplied to the calculation. Finite coefficient comparisons and tests are
separate from the analytic all-positive-coefficient sign proof in the report.

## Exact new-file inventory

All nine new files are under
`qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/`:

- `vcdm_flrw.py`
- `test_vcdm_flrw.py`
- `FLRW_OBSTRUCTION.md`
- `REPRODUCE.md`
- `contract.json`
- `run_001/result.json`
- `run_001/manifest.json`
- `run_001/stdout.txt`
- `run_001/stderr.txt` (empty, hashed)

No original theory, simulation, preregistration or unrelated dirty file was
modified. The framework's full-theory goal remains OPEN. The proposed
VCDM+exponential-lapse completion is rejected for the specified healthy
matter-filled FLRW branch; a different kinetic/constraint structure is needed.
