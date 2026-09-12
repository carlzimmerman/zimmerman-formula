# Verification and handoff

Whole-theory status: OPEN. Code execution success is not gate closure.
The action and coefficient histories were not changed. The previous checkpoint
`f59fad6c7` was pushed successfully before this continuation. Latest external
research fully audited here: `473860435`, L211/L212. A final bounded dependency
check read the new matter-coupling declaration and limitations in L214 at
`425a28355`; its entire branch and newly extended Lean module were not audited.

## Final executed checks

The final bounded wrapper command is preserved verbatim in [COMMAND.md](COMMAND.md).
It invokes `python3 -B principal_gate/verify.py --output .../run_002/checks`
from the repository root through the Mathbox provenance runner.
The actual absolute child argv and working directory for every command are
recorded in [run_002/checks/summary.json](run_002/checks/summary.json).

| Command, relative to closure_front_2026 unless noted | Final exit | Evidence scope |
|---|---:|---|
| `principal_gate/principal_gate.py` | 0 | 11 exact checks plus four automatically preserved principal constraint branches |
| `principal_gate/test_principal.py` | 0 | Constraint preservation/antisymmetry controls and a rejected linear MOND identification |
| `principal_gate/first_derivative_variation.py` | 0 | 19 invariant stress/current checks including canonical energy |
| `metric_response/derive_static_metric.py` | 0 | 68 static action, curvature, source, momentum and degeneracy checks |
| `spherical_branch/derive_spherical.py` | 0 | 26 radial/current/constitutive checks |
| `boosted/derive_boosted.py` | 0 | Existing sourced cubic principal regression |
| `boosted/test_boosted.py` | 0 | Existing independent boosted controls |
| `../mond_braiding_completion/derive.py` | 0 | Existing same-action cubic closure calculation |
| `health/pressure/audit_pressure.py` | 0 | Existing canonical pressure and clock regression |
| `lake env lean .../principal_gate/ResponseGate.lean` | 0 | Seven exact real-algebra/exponential implications |
| `lake env lean .../spherical_branch/SphericalScaling.lean` | 0 | Four coefficient-vector/radius statements |

The two Lean commands ran from the existing
`clock_constitutive_construction_2026/lean_formalization_2026` project.
All eleven final axiom lists contain only `propext`, `Classical.choice`,
and `Quot.sound`. The scalar Taylor-jet derivation is SymPy evidence;
the final spherical Lean file does NOT formalize analytic Taylor theory or
Mathlib's polynomial representation. No new dependency was installed.
General action variation, the nonlinear Dirac system, empirical agreement
and full PPN/CMB closure are NOT certified by these Lean leaves.

The final wrapper and the three current manifest validations returned 0:

- `principal_gate/run_002/manifest.json`
- `metric_response/run_001/manifest.json`
- `spherical_branch/run_002/manifest.json`

Validation command for each, executed from repo root:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py PATH_ABOVE --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

`PATH_ABOVE` here expands to the corresponding full repo-relative path under
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/`.
The manifest records actual argv, SHA-256 hashes before/after, runtime,
repository revision/dirty state and declared output. The verifier additionally
stores every child stdout/stderr and source hash. Dependency provenance is
limited to the explicitly declared local inputs and pinned library manifest,
not every transitive library file.

Resource limits: two verifier workers, one cooperative numerical-library
thread per child, 90 seconds per command and 300 seconds for the outer runner.
No memory/CPU-affinity hard cap is claimed. Python 3.9.6, SymPy 1.14.0,
existing Lean 4.34.0-rc2 environment. The tests ran on the local Mac.

## Failed checks retained

1. Before implementation, `python3 -B .../principal_gate/test_principal.py`
   exited 1 because the derivation file did not yet exist. It subsequently
   passed against the real implementation.
2. Initial ResponseGate compilation exited 1 because the broad
   `Mathlib.Tactic` import required an unavailable compiled module. Selecting
   the already installed specific tactics removed that environment dependency.
   A second compile exposed a redundant tactic after a solved goal (exit 1);
   removing that tactic preserved the theorem and produced exit 0.
3. The first common wrapper, `principal_gate/run_001`, exited 1. All Python
   jobs and the then-six ResponseGate declarations passed, but the attempted
   spherical polynomial proofs failed. Its compiler output contains Lean's
   generated `sorryAx` for those unfinished declarations; the verifier rejected
   them. The failed logs and manifest remain preserved. They are NOT evidence
   for the final changed source.
4. The final spherical formalization is explicitly weaker: coefficient-vector
   separation, with action-to-coefficient derivation left to the symbolic
   computation. The independent cubic-radius algebra theorem is retained.
5. The assertion negative control intentionally exits 1 in every successful
   suite. Child `PYTHONOPTIMIZE=0` prevents disabled assertions from yielding
   false success. Its stderr and status are recorded in the summary.

Historical spherical `run_001` predates the canonical history correction;
use `run_002` for current-code reproduction. No failed evidence was
relabelled as a proof. A superseded uncommitted standalone principal result
was removed; its reproducible current output is inside the final common run.

## Review and exact changed files

Independent read-only review reconstructed both potentials, principal Dirac
chains, variational signs, the exponential inequality and critical-source
compatibility. It identified two scope gaps, now corrected: a bounded-derivative
argument also requires zero acceleration at zero source; loss of uniform
response need not occur solely at a local `G=0` point.
Proofreading reviewed the new reports and displays; these substantive scope
corrections were proof-audit changes, not concealed typographical edits.

[FILES.md](FILES.md) lists every created path and the one modified index.
Unrelated journal/Claude working-tree edits were preserved. No coefficient
function, existing test, or Claude research file was overwritten.
