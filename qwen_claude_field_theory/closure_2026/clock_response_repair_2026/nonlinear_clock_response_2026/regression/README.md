# Existing regression archive

All **92 existing tests** and the four existing MOND-completion checks passed.
Every job exited zero; no timeout, skipped test, test failure, or test error
was reported. The bounded run completed in **9.680608 seconds**.

| Existing suite | Tests |
|---|---:|
| variance_closure_2026/geometry | 8 |
| variance_closure_2026/evolution | 4 |
| variance_closure_2026/vertices | 5 |
| cosmological_bridge_2026 | 35 |
| inhomogeneous_charge_2026/exterior | 5 |
| inhomogeneous_charge_2026/current | 9 |
| inhomogeneous_charge_2026/constraints | 5 |
| inhomogeneous_charge_2026/tracking | 5 |
| finite_gradient_metric_2026, root test files only | 4 |
| finite_gradient_metric_2026/cubic | 6 |
| finite_gradient_background_2026 | 6 |
| Total | 92 |

`mond_braiding_completion` has no test*.py suite. Its existing `run_checks.py`
identifies four relevant checks, all rerun here: its symbolic `derive.py`,
`CubicRelations.lean` (two statements), the earlier `dirac_operator/ellipticity.py`,
and `dirac_operator/lapse_source.py`. The three Python outputs are retained
as `mond_derivation.json`, `prior_ellipticity.json`, and `prior_lapse.json`.
The Lean invocation uses `-j1` and the existing pinned project/toolchain.

`run_001/result.json` records every exact child argv, cwd, exit code, elapsed
time, stdout, stderr, and test counts. Individual execution JSON records also
inventory actual project file reads. All observed project Python sources,
test modules, and input JSON dependencies were present in the 68 declared
inputs; no unpinned project input was found. The Python audit hook rejects
project writes outside the new run directory, and `-B` prevents bytecode writes.
External Python libraries are recorded by actual software version. Lean's
toolchain and package lockfiles are pinned rather than tracing every compiled
library read.

The v2 `run_001/manifest.json` validates with the computation-audit validator
and `--root /Users/carlzimmerman/new_physics/zimmerman-formula`. It pins the
actual execution inputs and all 18 declared result files; no input changed
during execution. `runner_argv.json` preserves the exact bounding invocation;
the manifest's `command` array preserves the scientific supervisor command.
No command was copied from an untrusted prior manifest.

Limits: at most four simultaneous jobs, one cooperative numerical-library
thread per job, 150-second per-job wall limit, 180-second outer wall limit,
150-second inherited per-process CPU limit, and a 2 MiB outer log limit.
No memory or CPU-affinity cap is claimed. The outer runner's process-group
bound remains the backstop if an individual timed-out job has descendants.

Only this new regression directory was edited. Previous source/test/result
files and the frozen nonlinear clock calculation were untouched. The runner
performed read-only revision/provenance checks; no git mutation was performed.
Regression success is not a new physical derivation, a solved source, or a
nonlinear hyperbolicity/stability certificate.
