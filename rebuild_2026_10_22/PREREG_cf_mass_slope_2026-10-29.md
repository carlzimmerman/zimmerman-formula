# PRE-REGISTRATION: an external prediction for native c_f(M), locked before the X48 A4 zooms report (2026-10-29)

**Source.** The external model's Q2, relayed by the owner in chat on 10-29. It is committed here before any A4 number is
read. A4 was launched 10-29 06:40 (criteria fc22ce369d). Its 18 ng64 seeds at 1e13 / 1e14 M☉ were still running when this
file was written.

## Prediction (verbatim in substance)

c_f(M) = 4.0 (Σ_coll(M)/Σ_coll(10¹² M☉))^(1/3) ≈ 4.0 (M / 10¹² M☉)^0.077

| M (M☉) | predicted c_f |
|---|---|
| 1e12 | 4.0 |
| 1e13 | 4.78 |
| 1e14 | 5.69 |
| 10^14.5 | 6.22 |

**Sign:** c_f rises with mass. The source's derivation (a binding-energy form factor α_W(c_f) for the smooth core, with
α_W ∝ Σ_coll^0.15) is asserted, not derived. It is recorded as a falsifiable prediction, not a result.

## How it will be scored (fixed now)

Use the c_f definition X48 already uses, with `x48_analyze.py --ng 64 --tag A4` and the A3 1e12 runs.
- **SLOPE TEST (primary):** the sign of d ln c_f / d ln M between 1e12 and 1e14 from the ng64 seed medians. The
  prediction passes if the slope is positive and its 68 % seed-bootstrap interval contains 0.077, and fails if the slope
  is ≤ 0 at 68 %.
- **LEVEL (reported):** c_f(1e12) against 4.0.

## Context already in the record (disclosed, so the test is not blind to it)

- X48 ng48 medians were 7.2 / 7.0 / 5.6 at 1e12 / 1e13 / 1e14, a falling trend. They were not converged.
- X48 A3 ng64 at 1e12 gave 7.74.
- So the level is already above 4 at 1e12, and the earlier slope was negative. A4 decides the slope at converged
  resolution.

κ = ½ FITTED; c_f EXTERNAL; not theory closed.
