# Action-derived variance closure checkpoint

Base: `48ab93de3` (shared main, PAPER20), following `d2301db52`.
Target: the unchanged same-action gravity requirements; full theory **OPEN**.
No coefficient functions, couplings, or existing scientific records are edited.

The new missing implication is not another root of the L194 proxy: it is the
derivation of gradient-variance dynamics and nonlinear feedback from the action.
PAPER20 is audited as a local source, not authenticated as an external publication.

## Independent work packages

- `geometry/`: derive the physical clock-frame observable, its covariance
  transport, and admissible same-variance/different-rate witnesses.
- `evolution/`: retain the actual sourced expansion and constitutive rates in
  the original six-state system; integrate covariance and modes independently,
  and test instantaneous balance against the actual acceleration equation.
- `review/`: independently locate the exact action-to-attractor implication in
  PAPER20 and identify the first missing nonlinear action order.
- `VarianceClosure.lean`: certify exact real-algebra implications, with the
  action-to-algebra map explicitly remaining a separate symbolic/numerical audit.

A same-variance/different-rate pair refutes an **exact universal** scalar
closure, not a possible late-time attractor on a restricted basin. Linear
covariance evolution has no nonlinear finite-variance feedback. A useful next
step must expose the actual interaction vertex and mode couplings, not replace
them with a new fitted variance-rate function.

## Completed checkpoint

All four packages completed. A further `vertices/` calculation expanded the
unchanged P+sW action through quartic scalar order on fixed metric/clock,
varied its spatial sector independently, and checked generated 3k harmonics
against the exact constitutive flux. It did not eliminate nonlinear constraints.

Result: exact universal variance-only closure is excluded on the stated
regular linear branch; the full nonlinear statistical state remains open.
Numerical equal-variance witnesses, nonzero balanced-state accelerations,
and the bare nonlinear vertex are in `REPORT.md`. Seven conditional algebraic
lemmas compile in Lean. Four bounded v2 manifests validate; 92 fresh tests
include 17 new tests and 75 regressions. No active delegated run remains.

Concurrent L195 commit `08281ae25` was reviewed without rewriting its source.
It prescribes effective-fluid inputs rather than deriving nonlinear response
from this action, so it does not supersede the missing implication.

Next distinct route: derive the constrained cubic/quartic interaction,
including mean/2k backreaction and generated 3k modes. This is needed before
asserting a nonlinear cold attractor or feeding its stress into one common
CMB/late-time transfer history. Do not rerun only the old scalar proxy roots.
