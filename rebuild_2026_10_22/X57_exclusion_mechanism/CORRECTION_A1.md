# Post-result correction A1: R4b band entry and shear positivity

Authorized 2026-10-27 after `reviews/claude_closure_audit_2026_10_27/REPORT.md`.
The frozen criteria, assumption ledger, original script and original outputs are
historical and remain unchanged. This correction supersedes their general R4b
inference; it does not rerun or strengthen M1–M4's independent calculations.

For every footing and h cell, the downward change needed to enter the inclusive
two-sigma band is `max(0, pred - (meas + 2*s))`, not `1-meas`. Its fractional
version is this change divided by `pred`. The inherited `D` is described as a
fractional response bound, so the diagnostic compares it with that fractional
quantity. If D is large enough, the result is only “bound does not exclude.”
An achievable, conserving deficit profile and its exact projected response have
not thereby been demonstrated. The D proxy is retained conditionally, not
upgraded into a validated projection bound.

Nonnegative three-dimensional density alone does not imply nonnegative
`DeltaSigma = meanSigma(<R)-Sigma(R)`. A positive spherical shell gives negative
DeltaSigma inside its edge. A nonincreasing projected surface density is a
sufficient additional hypothesis for nonnegative DeltaSigma; a spherical,
nonnegative, radially nonincreasing density is a familiar sufficient subclass.
Thus the law-only lower bound applies conditionally to additions whose projected
shear is nonnegative, with no compensating deficit. General radial profiles
remain unresolved. The shell counterexample establishes no equilibrium or fit.

`x57_r4b_correction.py` recomputes the four band boundaries from the historical
JSON, marks the general R4b line ND, preserves every other gate, and recomputes
the class verdicts. All corrected outputs and run manifests are separately
named under `closure_program_2026_10_27/gate_fixes/`; see that directory's README
for the run commands and numerical result. Kappa remains fitted.
