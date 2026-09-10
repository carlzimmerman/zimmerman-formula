# Execution and handoff

The authoritative commands, argv, working directories, observed statuses and
numerical summary are in `COMMANDS.json`; raw complete output and pinned input
hashes are in `run_001/manifest.json`, `stdout.txt`, and `stderr.txt`.
Successful execution is distinct from a successful gravity theory.

## Main verification

From the repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/run_suite.py
```

This command was executed inside the Mathbox bounded runner with a 450-second
limit, 4 MiB output limit and one numerical-library thread. The wrapper's exact
143 input paths and argv are in `COMMANDS.json`. Runtime: 137.280773 seconds.

| Important check | Observed status |
|---|---|
| Four new root numerical programs | Exit 0; model successes/failures separately recorded. |
| Root regression tests | 10/10; exit 0. |
| Exact arbitrary-F variation tests | 14/14; exit 0. |
| Independent EF dictionary tests | 10/10; exit 0. |
| Same-action cosmology tests | 8/8; exit 0. |
| New NonaffineAlgebra Lean file | Seven conditional theorems; exit 0. |
| New ConeWindow Lean file | Two equivalences; exit 0. |
| New CosmologyGates Lean file | Five conditional lemmas; exit 0. |
| Previous closure suite, run after new work | 151 tests; enclosing command exit 0. |
| Earlier require-closure negative controls | Expected exit 2, retained by the preceding suite. |
| Concurrent L121 literal program | Exit 0; six labels do NOT establish its CMB interpretations. |
| Concurrent Fable full Lean file | Exit 1: conflicting cached Mathlib Asymptotics declarations. |
| Entire enclosing root suite | **Exit 1**, solely because that concurrent-file compilation failed. |
| Main manifest validation with current root | Exit 0: valid evidence of the recorded run, not a mathematical PASS. |

Thus all 193 Python tests passed and all 14 NEW Lean theorems compiled. The
full suite is not reported green: the external Lean recompilation remains
blocked by the available environment. No failed output was erased or counted
as a proof. No result from that blocked compilation is used as new evidence.

The exact error is:

```text
import Mathlib.Analysis.Asymptotics.AsymptoticEquivalent failed,
environment already contains 'Asymptotics.IsEquivalent'
from Mathlib.Analysis.Asymptotics.Defs
```

Trying the concurrent file in its own saved project also exited 1: Mathlib was
not materialized there, and dependency lookup failed DNS. The unmodified
`concurrent_snapshot/ConcurrentMondlean.lean` preserves the tested source at
commit `293b4e70a`; recompiling the snapshot reproduced the same cached-module
conflict. These are environment failures, not a proof that its arithmetic or
inequalities are false. No dependency installation or old source edit was
used to conceal them.

## Numerical outcomes

- 144 quadratic-F local jets: 55 meet the local EF criteria.
- 11 fixed-quadratic continuations: one seed fails, ten hit a health boundary,
  none reaches y=100.
- 105 background points with analytic full-real-j elimination: 93 constructible,
  12 excluded. Maximum actual-principal correlation residual: 8.09e-14.
- Controlled nonquadratic trajectory stops at y=2.498186927381134 with step
  .005 and at 2.4981867909551614 with half step; both use the 1e-8 relative
  window guard. A 1e-7 guard gives 2.4981869007627. These are approximate
  guarded endpoints, not exact universal boundaries.
- Accepted nodes and interpolation midpoints pass the stated local checks.
  X is monotonic. Maximum recorded metric/current scaled residuals are below
  8e-16 and 3e-16 respectively in the formal run. These do not bound global
  ODE error or prove physical nonlinear stability.

## Independent evidence

- `variation/run_001`: 14 exact tests + nine Lean theorems, exit 0; validator 0.
- `dictionary/run_001`: ten independent tests, including 70-digit controls,
  exit 0; validator 0.
- `cosmology/run_002`: eight tests + five Lean lemmas + literal L121 run,
  exit 0; validator 0. Its `run_001` is retained but superseded after a
  documentation correction; do not present its old document hashes as current.
- Independent read-only review approved the final curvature selection,
  cancellation-resistant flow, and claim limits. A separate source audit
  confirmed the missing epsilon-to-baryonic-mass/measured-G normalization.

## Late L123 counterclaim supplement

After the main run, the newly committed L123 universal stiff-tail claim was
audited rather than folded into the theory as an established exclusion.
`run_supplement.py` ran under its separate pinned `supplement_contract.json`
in 3.501478 seconds and exited 0. `SUPPLEMENT_COMMANDS.json` records every
argv/status. Nine new exact tests and three new conditional Lean lemmas pass;
the unchanged L123 program also exits 0, without validating its prose.
Ten root and eight cosmology tests were rerun AFTER this addition and passed.
`supplement_001/manifest.json` validates with exit 0.

The combined evidence therefore covers **202 distinct Python tests and 17 new
conditional Lean theorems**, with 18 regression repeats in the supplement.
The earlier legacy-file Lean compilation remains failed/environment-blocked;
the supplement does not convert the original full suite to a PASS.

## Development failures and reproducibility scope

Test-first imports of `curvature_window` and `controlled_flow` initially exited
1 before those modules existed. Final tests above pass. Earlier new-package
root inverse/quadratic tests, main scans and controlled-flow refinements were
run before the pinned suite and reproduced its qualitative outcomes. A first
unguarded endpoint ran into cancellation near a zero-width window; the final
implementation explicitly stops before that region and compares two guards.
The source agent records its initial Lean parser/import attempts separately;
only its final compiled files support the present claims.

No unrelated dirty work was staged. All new checkpoint files are under this
directory; `FILES.json` inventories them. The full-theory goal remains OPEN:
common universal functions and physical sourcing must precede a meaningful
joint galaxy/CMB parameter fit. The background equations are now available,
but no CMB spectra or all-gates physical certificate has been produced.
