# Reproduction and evidence inventory

Base revision: `3f564b75dc48a0a5ac995fd46165b17e1d546e19`.
Run from repository root. Python 3.13.9, SymPy 1.13.1, NumPy 1.26.4,
SciPy 1.14.1. No dependencies installed, no empirical dataset or Lean proof.

## Exact scientific commands and observed exit statuses

```bash
git status --short
git log -5 --oneline
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/conformal_action.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/braiding_gate.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/braiding_gate.py --require-two-tensor
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/transformed_lapse.py --require-two-tensor
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/anisotropic_primary.py --require-primary-consistency
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -v
git diff --check
```

| Check | Exit | Observed result |
|---|---:|---|
| Raw conformal action/map derivations | 0 | 12 symbolic identity/source residuals vanish |
| Combined braiding calculation, default | 0 | Calculation completes; extra principal scalar data reported |
| Braiding acceptance gate | **2** | Does not pass zero-scalar-pair gate |
| Transformed affine mechanism acceptance | **2** | Fixed physical MOND potential has nonzero lapse Hessian |
| Anisotropic primary consistency acceptance | **2** | Exact weak self-bracket counterexample |
| New unit suite | 0 | 32 tests pass |
| Prior expansion-switch suite | 0 | 22 tests pass |
| Prior FLRW suite | 0 | 10 tests pass |
| Prior constitutive suite | 0 | 8 tests pass |
| Prior cluster audit suite | 0 | 9 tests pass; not a new data analysis |
| Bounded provenance run | 0 | Completed in 2.079083 seconds; NOT theory certification |
| Manifest/hash validator | 0 | Valid record with current pinned inputs/outputs |
| Whitespace check | 0 | No whitespace errors |

Total: **81 passing regression tests**, with **three failed physical
acceptance gates**. A zero process exit means the computation ran, not that
the theory satisfies the full requirements. Production ranks, determinants,
and counts are obtained from differentiated matrices. Expected expressions
in independent regression assertions are not inputs to those matrices.

All four computation modules and all four test modules were executed.
The standalone transformed and anisotropic modules were also run in default
mode by their implementing reviewer (exit 0); the root ran their acceptance
modes and the combined importer independently.

## Tests-first development and review corrections

Tests were written before missing implementations. The initial missing-feature
runs exited 1. Later root tests caught a genuine mixed-primary reduction bug:
eliminating p_z through p_n/eta introduced an artificial division and the reduced
Hamiltonian had not imposed the mixed primary. Choosing a regular elimination
order and imposing both primary and secondary constraints corrected it without
changing the asserted ranks. The eta=0 fixture tests the corrected path.

New exceptional-branch/normalization/report tests subsequently failed first
(three missing features, exit 1), then passed. Two added anisotropic tests
failed first before the production rank and verdict were made dependent on
the actual Hessian and exact witness. One root combined run occurred during
that tests-first edit and saw those same two intended failures. The final
root run was made only after the edits completed.

Independent review reconstructed the canonical transformation, bracket matrix,
reduced Hamiltonian and homogeneous matter constraints. It required explicit
real-branch domains, full eta=-1/3 preservation, and vacuum irregularity.
The final report review caught a static-dust versus canonical-scalar ambiguity:
the same action now specifies both minimal sectors and their distinct
diagnostic limits, and a tests-first particle-source variation was added.
The exact torus witness's positivity and nonzero-smearing assumptions were
also made explicit. The reviewer then reported no remaining blockers within
this scope. Full nonlinear closure was not reviewed or claimed.

Mathbox research/computation/proof audits influenced the actual work: failed
routes remained visible, primary brackets were varied rather than inherited,
mode/parameter exceptions were retained, and evidence was pinned only after
the final mathematical review. Mathematical proofreading covered DECISION.md;
no additional mathematical-token correction or proof certificate was needed.

## Immutable bounded run

`run_001/manifest.json` records the child argv, commit/dirty state, software,
nine input hashes before/after, outputs, timing and resource settings.
`run_001/result.json` contains separate candidate results, computed brackets,
constraints, preservation residuals, exceptional sectors and scope limits.
No hard memory/CPU/affinity limit was requested; timeout=60 seconds,
combined log cap=1048576 bytes and cooperative numerical-library threads=1.

Set AUDIT_SCRIPTS to the installed Mathbox computation-audit `scripts`
directory. The portable equivalent of the executed runner command is below.
For reproduction use a **fresh** run directory in all occurrences; the runner
and scientific output refuse to overwrite existing results.

```bash
OPENBLAS_NUM_THREADS=1 python -B "$AUDIT_SCRIPTS/run_experiment.py" \
  --root . \
  --contract qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/contract.json \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/conformal_action.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/braiding_gate.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/transformed_lapse.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/anisotropic_primary.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/test_conformal_action.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/test_braiding_gate.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/test_transformed_lapse.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/test_anisotropic_primary.py \
  --input qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/DECISION.md \
  --output qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/run_001 \
  --result qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/run_001/result.json \
  --timeout 60 \
  --max-output-bytes 1048576 \
  --max-threads 1 \
  -- python -B qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/braiding_gate.py \
  --output qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/run_001/result.json
OPENBLAS_NUM_THREADS=1 python -B "$AUDIT_SCRIPTS/validate_manifest.py" \
  qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026/run_001/manifest.json --root .
```

## Exact new-file inventory

Only these 15 files were created for this checkpoint, all in this directory:

- `conformal_action.py`
- `test_conformal_action.py`
- `braiding_gate.py`
- `test_braiding_gate.py`
- `transformed_lapse.py`
- `test_transformed_lapse.py`
- `anisotropic_primary.py`
- `test_anisotropic_primary.py`
- `DECISION.md`
- `REPRODUCE.md`
- `contract.json`
- `run_001/manifest.json`
- `run_001/result.json`
- `run_001/stdout.txt`
- `run_001/stderr.txt` (empty, hashed)

No previous action, result, observational artifact or unrelated dirty file
was changed. Overall field-theory status: **OPEN**. See DECISION.md §6 for
the remaining calculation and precise scope of the falsifications.
