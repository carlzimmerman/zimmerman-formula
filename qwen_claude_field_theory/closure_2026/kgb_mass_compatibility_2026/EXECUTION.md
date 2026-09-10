# Execution and handoff record

2026-09-10. This is a research checkpoint, **not a complete theory certificate**.

## Final fresh verification

- `run_002`: exit **0**, runtime **119.196583 seconds**.
- **151 unittest cases** passed: 63 new and 88 earlier closure regressions.
- All **19 top-level commands** exited 0.
- **Eight new conditional Lean theorems**, in two files, compiled. Their axiom
  reports list only standard Lean/mathlib foundations; no sorry-based proof.
- Seven current evidence manifests validated against current source hashes,
  each exit0. Exact commands, cwd, inputs and statuses are in
  [COMMANDS.json](COMMANDS.json), [run_002/manifest.json](run_002/manifest.json),
  and the nested CASE records in [run_002/stdout.txt](run_002/stdout.txt).
- Four older `--require-closure` controls deliberately return **2**, and their
  parent suites verify that refusal. They are not physics passes in disguise.
- The initial complete pre-runner-hardening suite exited0. The final formal
  evidence supersedes it and records the updated combined test set.

### Important commands and exit status

| Executed case | Exit |
|---|---:|
| triple_seed.py | 0 |
| triple_flow.py | 0 |
| conformal_dictionary.py | 0 |
| conformal_inverse.py | 0 |
| gradient_inverse.py | 0 |
| conformal_flow.py | 0 |
| l119_scope.py | 0 |
| root regressions | 0 |
| structure/test_structure.py | 0 |
| structure/test_derivative_curvature_variation.py | 0 |
| structure/test_conformal_inverse_structure.py | 0 |
| extension/conformal_extension.py | 0 |
| extension/test_extension.py | 0 |
| extension/ef_principal.py | 0 |
| extension/inverse_audit.py | 0 |
| structure/CompatibilityAlgebra.lean | 0 |
| structure/ConformalInverseAlgebra.lean | 0 |
| previous closure regressions | 0 |
| concurrent L119 literal checks | 0 |

The full final reproduction command from repository root is:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/run_suite.py
```

The exact bounded wrapper command, including all 123 explicit input paths, is
saved in COMMANDS.json; it uses a 450-second limit, 4MiB log cap, and one
numerical-library thread. These are computation bounds, not mathematical bounds.

## Development failures and evidence revisions

Failures are not removed or presented as physics certification.

- The initial `test_triple` import check failed before its implementation.
- `python3 -B -m unittest test_conformal_inverse` first exited1 because the
  requested continuation module did not exist. After implementation, its
  finite-difference pressure-preservation check exposed cancellation at step
  1e-11. A recorded scan from 1e-8 to 1e-12 located the converged 1e-10 window;
  independent complex-step, real derivatives and 80-digit checks also agree.
- `python3 -B -m unittest test_gradient_inverse` initially exited1 because
  the gradient-chart implementation did not yet exist, then passed.
- `python3 -B l119_scope.py` initially passed all three algebraic checks but
  exited1 while serializing a symbolic dictionary key. Explicit string keys
  fixed the output; its complete command now exits0.
- The first `test_runner` check exited1 before run_case existed. Its standalone
  tests subsequently passed, but the **combined** formal `run_001` exposed a
  different bug: prior physics imports changed sys.path and selected an older
  sibling run_suite.py. The test now imports its target by exact filename.
  All 21 root tests pass together, not just in isolation.
- The failed `run_001` is retained unchanged. Validation against current
  sources correctly exits1 because its old test_runner.py hash is superseded.
  This is a historical failed record, not a current valid mathematical certificate.
- A b=.05 triple-seed exploratory call failed to solve its equations. The scan
  records such unresolved attempts; optimizer status does not replace residuals.
- An optional asymptotic-analysis agent hit its model usage limit and supplied
  no result. No claim depends on that agent and no usage reset was consumed.

The final read-only review found no blocking issue. Its one minor suggestion
was to record timeout/launch errors before exiting; this was implemented and
tested (statuses124/127) before the final successful run. Those wrapper status
tests are distinguished from the physical calculations.

## Mathematical result and scope

The improved triple-mass KGB seed agrees through more derivatives but still
fails the next preservation equation under one common action. The conformal
extension is a distinct action whose metric/current equations were varied and
independently tested. Its actual 3x3 inverse has

```
det M3 = 4 F_X X' (2X+U)/(B p r).
```

The pressure fold is removable; the clock-norm-gradient zero is not: under the
listed finite-coefficient regularity assumptions it forces zero geometric
density, whereas the exponential target density is strictly positive at every
finite positive y and r. SymPy checks the explicit reduction, and Lean checks
the conditional algebra, invertibility and positivity—not the entire theory.

A selected particle-free clock action remains locally EF-healthy over a bounded
deep-MOND exterior interval. Refinement gives the inward angular boundary near
y=.14041695259 and the outward boundary near y=.00014074400653. Of the 30 retained
continuation attempts, 6 reached their requested finite target, 22 stopped at
a health boundary, and 2 failed their initial health gate. Repeated refinement
runs are included in those counts; they are not 30 independent theories.

**Candidate family: OPEN. Selected branch: does not pass the full acceleration
range. Complete gravitational closure: NOT ACHIEVED.**

The next unavoidable calculation is a mass-universal, preserved F,P,G trajectory
through the Newtonian transition, using the actual enlarged equations (and
retaining the gradient chart). It then needs interior baryon matching and the
full Dirac/PPN/cosmological/stability calculations listed in REPORT.md. No
particle dark matter is added; the physical scalar clock must remain explicitly
counted and healthy.

## Exact files added in this checkpoint

All 67 listed files are under `qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/`. No pre-existing
research source or Fable file was edited. Ignored local primary-paper copies
and every unrelated dirty file are excluded.

```text
COMMANDS.json
EXECUTION.md
REPORT.md
audit_contract.json
conformal_dictionary.py
conformal_flow.py
conformal_inverse.py
extension/.gitignore
extension/EF_PRINCIPAL.md
extension/INVERSE_AUDIT.md
extension/REPORT.md
extension/SOURCES.md
extension/audit_contract.json
extension/conformal_extension.py
extension/ef_contract.json
extension/ef_principal.py
extension/ef_run_001/manifest.json
extension/ef_run_001/results.json
extension/ef_run_001/stderr.txt
extension/ef_run_001/stdout.txt
extension/inverse_audit.py
extension/inverse_audit_contract.json
extension/inverse_audit_run_001/manifest.json
extension/inverse_audit_run_001/results.json
extension/inverse_audit_run_001/stderr.txt
extension/inverse_audit_run_001/stdout.txt
extension/run_001/manifest.json
extension/run_001/results.json
extension/run_001/stderr.txt
extension/run_001/stdout.txt
extension/test_extension.py
gradient_inverse.py
l119_scope.py
run_001/manifest.json
run_001/stderr.txt
run_001/stdout.txt
run_002/manifest.json
run_002/stderr.txt
run_002/stdout.txt
run_suite.py
structure/CONFORMAL_INVERSE_STRUCTURE.md
structure/CompatibilityAlgebra.lean
structure/ConformalInverseAlgebra.lean
structure/DERIVATIVE_CURVATURE_VARIATION.md
structure/STRUCTURE.md
structure/contract.json
structure/inverse_contract.json
structure/inverse_run_001/manifest.json
structure/inverse_run_001/stderr.txt
structure/inverse_run_001/stdout.txt
structure/run_001/manifest.json
structure/run_001/stderr.txt
structure/run_001/stdout.txt
structure/test_conformal_inverse_structure.py
structure/test_derivative_curvature_variation.py
structure/test_structure.py
structure/variation_contract.json
structure/variation_run_001/manifest.json
structure/variation_run_001/stderr.txt
structure/variation_run_001/stdout.txt
test_conformal_inverse.py
test_dictionary.py
test_gradient_inverse.py
test_runner.py
test_triple.py
triple_flow.py
triple_seed.py
```
