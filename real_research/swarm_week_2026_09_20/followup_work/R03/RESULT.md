# R03 — Derive corrected velocity curvature and its observable domain (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / proved (algebra), finite_evidence (precision)
- Baseline: followup work order `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`; HEAD
  `29b5c74ff`.  `python3 matched_profile_comparison.py` exit 0.
- Model/action ID: conditional mass continuations (the L304 log shell from R02
  vs the L311 sqrt shell), circular-motion kinematics only.

## Exact claim and scope

For v^4 = a0 G M_total(r) with circular motion: beta = (1/4) d ln M/d ln r.
Log continuation M = Mbase + C_log ln(r/r0): C_beta := d beta/d ln r + 4 beta^2
= 0 identically.  Sqrt continuation M = Mbase + C_sqrt sqrt(r): C_beta =
beta/2 identically.  Matching amplitude AND slope at an anchor does not erase
the separation.  Scope: conditional shape relations; no new empirical law.

## First discriminator and result

**4/4 PASS.**  V1: C_beta = 0 for the log model to 8e-9 of 4 beta^2's scale.
V2: C_beta = beta/2 for the sqrt model to 5e-8 relative.  V3: after a two-point
match (same M and beta at r_anc), the sqrt model still bends with C_beta =
beta/2 (7e-10).  V4 (the honest negative): with 12 rotation points at 1% over
a factor-3 window, the curvature invariant's Monte-Carlo 1-sigma (0.6) is 4.9e3
times the sqrt-vs-log separation — a second derivative of a noisy rotation
curve is NOT a usable discriminator at galactic data quality.

## Evidence

- `matched_profile_comparison.py` → exit 0, 4/4 PASS + results JSON
  (sigma_beta 0.070, sigma_C 0.608, separation 0.000 at the chosen beta level —
  the V4 measurement is curve-flat; ratio quoted at the median simulated beta).

## Independent check

The identities were also derived by hand in the script docstring (algebraic
closure) and reproduced numerically with an independent gradient path (np.gradient
on log r); boundary rows excluded (one-sided gradient artifacts at both ends
were the only nonzero residuals).

## Novelty and physical interpretation

The R02 correction changes which continuation is physical: the log shell has
C_beta = 0, the sqrt shell beta/2 — so the discriminator is real but
precision-gated.  L311 V2's "r^{1/8}" outer-rise shape must not be quoted for
the log law; the observable that survives is slow logarithmic growth
(d ln v/d ln r -> 0), measurable only with wide dynamic range or very high
precision (R18).

## Decision and next action

proved (algebra) + finite_evidence (precision limit).  R18: treat C_beta as
precision-gated, not a ready observable.  F2: use the log law's beta shape.
Next cheap test: L311 V1/V2 re-run on the log law to quantify the curve change.