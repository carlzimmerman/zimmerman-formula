# Verified results and handoff

2026-09-10. Full theory: **OPEN**, not Lean-certified as a law of nature.
No particle dark matter was added. One explicitly dynamical clock remains.

## Strongest result

An action-derived differential system constructs common numerical P(X),G(X)
for two different mass-parametrized exponential-MOND exterior patches.
Preserving their equality forces P_X; differentiating it forces P_XX.
The scalar principal coefficients are recomputed afterward, not tuned to pass.
At the selected seed, independent 60/80-digit calculations confirm positive
local static-time energy and strict scalar cone containment for both masses.
Both short continuations to t=±.05 pass at all 51 output points each.
Maximum relative stress residual is below 9.5e-16 on those sampled intervals;
shared h=G_X/P_X mismatch is below 1.5e-15. This is numerical local evidence,
not a continuum-validated existence proof or an empirical prediction.

The same branch reaches a light-cone boundary at t=+0.07985070533895 and an
angular-gradient boundary at t=-0.13302238646506. The two solver tolerances
return identical displayed endpoints (maximum-step control can dominate;
this agreement is not an independent proof of convergence).
A selected third mass matches the local action jet but needs a 14.6992%
change in P_XX to preserve the next derivative. With the actual shared value,
its literal h_XX mismatch is 14.2545%, independently reproduced at 60 digits.
This excludes that extension, not all actions or all third-mass roots.

A separate metric derivation establishes Phi'=g and Psi'=g-rP/(2m) at first
weak-field order. Pressure/rho alone is not the lensing diagnostic. The actual
local pressure-induced Weyl-slope correction rP/(4mg) stays below 1.38e-8 in
the short two-mass intervals, but full integrated lensing/PPN remain unproved.

## Tests and exact execution

Base at execution: `ce9b690dfa213dae2ac002910399afe3d0828a40` (dirty worktree).
The source files were unchanged during the run. Runtime: 91.534654 seconds.
88 Python unit tests passed (30 new + 58 previous), plus four new
conditional Lean theorems and the prior suite's formal checks. All 11 top-level
commands exited zero. Fable L118's six mixed documentary/algebra checks also
exit zero but are NOT counted as physical closure or as these unit tests.
Five provenance records validate with input/output hash checks.

The initial test-first run of test_joint.py exited 1 because joint_static.py
did not exist yet; after implementation and review all eight tests pass.
Two exploratory reads used filenames that did not exist (exit 1, then corrected);
a process-list diagnostic was sandbox-denied (exit 1). Neither affected results.
These are environment/read failures, not mathematical counterexamples.

Main reproduction from repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/run_suite.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The suite's exact successful command vectors and working directories follow:

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B joint_static.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B third_mass.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B -m unittest -v test_joint.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B test_independent_audit.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/audit`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B lensing.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/lensing`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B test_lensing.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/lensing`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B precision_check.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/precision`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B test_precision.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/precision`.

- Exit 0: `lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/audit/SharedPreservationFormal.lean`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B run_suite.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_shared_pressure_2026`.

- Exit 0: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B fable_independent_2026/L118_gate_spec_and_transition_pathology.py`
  Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.

The bounded runner used run_experiment.py, the local audit_contract.json,
all 100 execution_artifacts as repeated --input arguments, output run_001,
--timeout 450 --max-output-bytes 4194304 --max-threads 1, followed by the
main reproduction command above. No memory or CPU-time hard cap was imposed;
thread limiting is cooperative. Full child commands, raw numerical results,
exceptions, input hashes and execution status are preserved in run_001.
Independent audit, Lean, lensing and precision subdirectories additionally
retain their own earlier validated runs.

## Exact new files

All paths below are relative to `qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/`.
Only this new directory is intended for this commit; no existing or concurrent
Fable source is changed. RESULTS.md is this post-run summary, not an execution
input. The other reports/source inputs are hash-pinned by the main manifest.

- `REPORT.md`
- `RESULTS.md`
- `audit/AUDIT.md`
- `audit/SharedPreservationFormal.lean`
- `audit/lean_contract.json`
- `audit/python_contract.json`
- `audit/run_lean_001/manifest.json`
- `audit/run_lean_001/stderr.txt`
- `audit/run_lean_001/stdout.txt`
- `audit/run_python_001/manifest.json`
- `audit/run_python_001/stderr.txt`
- `audit/run_python_001/stdout.txt`
- `audit/test_independent_audit.py`
- `audit_contract.json`
- `joint_static.py`
- `lensing/REPORT.md`
- `lensing/audit_contract.json`
- `lensing/lensing.py`
- `lensing/run_001/manifest.json`
- `lensing/run_001/results.json`
- `lensing/run_001/stderr.txt`
- `lensing/run_001/stdout.txt`
- `lensing/test_lensing.py`
- `precision/REPORT.md`
- `precision/audit_contract.json`
- `precision/precision_check.py`
- `precision/run_001/manifest.json`
- `precision/run_001/results.json`
- `precision/run_001/stderr.txt`
- `precision/run_001/stdout.txt`
- `precision/test_precision.py`
- `run_001/manifest.json`
- `run_001/stderr.txt`
- `run_001/stdout.txt`
- `run_suite.py`
- `test_joint.py`
- `third_mass.py`

## Next unavoidable construction

Enforce three-mass, then continuum-of-masses derivative compatibility inside
the inverse differential-algebraic system; vary shared initial data or a
justified higher-order metric completion, not independent per-halo stability
coefficients. Test continuation through the transition and source/cosmological
matching only using the resulting same functions. A local pressure-window
repair is no substitute for these functional conditions.

Unresolved: full nonlinear Dirac closure/propagating count, full PPN and measured
G, all-sector/global stability and strong coupling, FLRW with these same
functions, k=0/y=0, complete lensing and baryonic interior matching. The fitted
kappa=1/2 has not been derived. No previous model's cosmology is imported here.
The selected two-mass branch does not meet the global target; the wider action
construction problem remains OPEN. The parent research goal is not complete.

## Review provenance

Independent reviews checked the source principal expression, both matching
signs, the total chain rule, numerical cancellation, and third-derivative
compatibility. They prompted a stronger static-Hamiltonian test and a corrected
label distinguishing logarithmic-derivative residual from literal h_XX mismatch.
Legacy false-empty wording is explicitly qualified without changing old evidence.
Mathbox's computation audit set these evidence boundaries. Mathematical
self-proofreading covered the new reports and equations; explicit spacing now
distinguishes products G_X X' and P_X X' from second derivatives. No unresolved
typographical issue changes the results. This is not a formal proof of nature.
