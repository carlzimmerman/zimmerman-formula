# CFG765 FROZEN CRITERIA: pre-flight — can the record's z ≈ 2–2.7 KMOS3D fits tell the two formation clocks apart?

Date: 2026-10-13. Block CFG760–769. Committed ALONE before any CFG765 script or number. κ = ½ FITTED; both footings; not "theory
closed". Pre-flight only: it decides whether a test is possible, not which clock is right.

## Inputs (read only)
CFG270 `cfg270_points_stageB.csv`, the 72 headline fits (tier T1): z and y = g_bar,*/a₀ at 2.2 r_d (stars-only baryons, a lower
limit on y; using it as given is favourable to the test because a lower y means a larger boost).

## The two predictions
- Orbital clock (CFG764): t_orb at 2.2 r_d ≈ 0.1–0.3 Gyr ≪ the baryon age, so f = 1: D_orb = ν_mono(y).
- Universal clock (CFG763), at its most separable allowed value τ = 3.47 Gyr: f = 1 − e^{−a/τ}, D_uni = 1 + f(ν_mono(y) − 1). Baryon
  age a ∈ {1, 3} Gyr (framework-free bracket for z ≥ 2; 1 Gyr is the most favourable to the test).
- Separation per fit: Δ = log₁₀ D_orb − log₁₀ D_uni (dex).

## Test
- **P1. DIAGNOSTIC iff the median Δ over the 72 fits at a = 1 Gyr is ≥ 0.30 dex** (twice CFG270's committed inner baryon band of
  ±0.15 dex, a systematic shared by all fits, so it does not average down). NOT DIAGNOSTIC otherwise.
- Reported: Δ at a = 3 Gyr; the y a fit would need for Δ ≥ 0.30; the pooled statistical error for comparison (which the shared
  systematic dominates).

**MUTATE** (`CFG765_MUTATE=1`): y := 0.01 for every fit (a deep-regime sample). P1 must then be DIAGNOSTIC. Exit 1 iff it bites.
