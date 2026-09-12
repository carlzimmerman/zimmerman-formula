# Recorded geometry commands and results

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Source/test edits were confined to this new `geometry` directory. No frozen
action code was edited and no Git mutation was performed. The requested
bounded provenance runner read the actual repository revision/status.

## Exploratory checks

```bash
python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry -p 'test_*.py' -v
```

Exit 0: initial seven tests passed. This preceded the direct frozen-action
map check and was not a test-first red phase.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry -p 'test_*.py' -v
```

Exit 0: eight tests passed in 2.640 seconds after adding the action-map test.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/derive_geometry.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/result.json
```

Exit 0: 23 exact symbolic assertions passed in 2.632 seconds. This exploratory
artifact predates the combined `--run-tests` CLI; use `run_001/result.json`
and its manifest as the canonical evidence.

## Canonical bounded run

```bash
PYTHONDONTWRITEBYTECODE=1 python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/contract.json \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/derive_geometry.py \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/test_geometry.py \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/transfer_evolve.py \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py \
  --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/run_001 \
  --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/run_001/result.json \
  --timeout 60 --max-output-bytes 1048576 --max-cpu-seconds 30 --max-threads 1 \
  -- python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/derive_geometry.py \
  --run-tests \
  --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/run_001/result.json
```

Exit 0; status `completed`; 23 exact symbolic assertions and eight unit tests
passed. Wall time 6.370614 seconds; tests took 4.330 seconds. All pinned input
hashes remained unchanged and the declared result was present. Software:
runner Python 3.11.16, computation Python 3.9.6, SymPy 1.14.0. Platform:
macOS 26.5.2 arm64. Enforced bounds: 60 seconds wall time, 30 seconds CPU per
process, 1 MiB combined log output. The one-thread environment cap is
cooperative. No memory or CPU-affinity cap was requested.

The actual revision recorded by the runner was
`08281ae2582ef39f853ad85405f3c56cb25dcc37`, dirty. It differs from the parent's
initial supplied baseline `48ab93de3`; all three frozen scientific source
hashes match the earlier exploratory read. Source identity is pinned by those
hashes rather than inferred from the earlier revision label.

```bash
PYTHONDONTWRITEBYTECODE=1 python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Exit 0: `valid evidence record; mathematical interpretation requires review`.

Regeneration requires a fresh runner output directory and the corresponding
changed `--result-file`; do not overwrite this archived evidence.

## Deliberate negative controls

After the canonical run, two isolated processes mutated only an in-memory
symbolic result. No source or evidence artifact was changed. These show test
sensitivity and are not represented as a test-first development history.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry python3 -c 'import unittest; import derive_geometry as d; import test_geometry as t; d.projected_geometry()["expression"] *= 2; result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([t.ClockGeometryTests("test_unitary_gauge_preserves_all_three_spatial_components")])); assert len(result.failures) == 1 and not result.errors, "normalization mutation escaped detection"; print("Expected normalization-mutation failure detected")'
```

Exit 0: the targeted unit test failed exactly once as required, detecting the
incorrect factor of two. No unexpected errors occurred.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/geometry python3 -c 'import unittest; import sympy as s; import derive_geometry as d; import test_geometry as t; result = d.projected_geometry(); result["expression"] = result["expression"].subs({s.Symbol("pi_"+axis, real=True): -s.Symbol("pi_"+axis,real=True) for axis in "xyz"}, simultaneous=True); check = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([t.ClockGeometryTests("test_comoving_fields_have_zero_projected_gradient")])); assert len(check.failures) == 1 and not check.errors, "gauge-sign mutation escaped detection"; print("Expected gauge-sign mutation failure detected")'
```

Exit 0: the targeted unit test failed exactly once as required, detecting the
incorrect clock-gauge sign. No unexpected errors occurred.

## Final self-review

The `mathbox:proofread-math` skill was applied to all new mathematical prose
in `DERIVATION.md`: definitions, signs, mode normalization, conditional
nondegeneracy and the limit on the closure conclusion. Routine edits covered
provenance and canonical-result cross-references. Explicit definitions were
added for the already-used frozen-source symbols \(C_r,q_r,\rho_b,j,j_r,R,
R_v,R_\sigma\); no sign, coefficient or proof step was changed. No unresolved
notation or LaTeX issue was found. This was source review, not a rendered
document build.
