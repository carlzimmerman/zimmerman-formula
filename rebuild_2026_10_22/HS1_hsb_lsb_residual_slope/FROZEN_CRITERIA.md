# HS1_hsb_lsb_residual_slope: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Argon's Q6 (`../ARGON_REPLY_2026-10-31/PREDICTIONS_ON_RECORD.md`): at fixed V_flat and fixed Υ on SPARC, does the velocity residual at 2 R_d trend with surface brightness? Route E's halo is set by total baryonic mass alone (EM1's M200(M_b)) and doesn't know about surface density. The a₀ law's boost depends on g_bar, which does. So the slope may separate them, and Argon said it would.

**Argon's numbers, on record before this lane.** N1 +0.085 ± 0.020 per dex, a₀ law 0.00 ± 0.015. Its example arithmetic had r₀ 5.8 kpc where the rule gives 4.04 (`../ARGON_REPLY_2026-10-31/README.md`), which doesn't change the test.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads. I've seen NF1's and LS1's ΔV by V_flat, not this slope.

## Sample
SPARC (Lelli+ 2016), V_flat 60–120 km/s, Q ≤ 2, Inc ≥ 30°, as LS1's selection. The sample is fixed by these cuts before any slope is read. A galaxy with 2 R_d outside its measured points is dropped and counted.

## Statistic
- δ = V_model/V_obs − 1 at R = 2 R_d, at Υ 0.50 on the grader's grid, interpolated in ln R between measured points that pass the grader's `OK` mask.
- x = lg SBeff (SPARC's effective surface brightness at 3.6 μm).
- b = ordinary least-squares slope of δ on x, per dex. σ_b from 10,000 galaxy bootstrap draws, half the 16–84 % width, seed 1.
- This is a statistic with no fitted model parameter, and Υ isn't refit per galaxy.

## Models
- **N1** (headline for route E): S_cold = f_c η(M_t) 10^(0.0927 (12 − lg M_t)) Σ_coll(M_t) below 10¹². NF1's rule, NF1's table.
- **N0, N2, F:** NF1's other variants and FC1's rule with the floor. F on both footings.
- **Law:** ν = ½ + √(¼ + a₀/g_bar), the kernel used in LS1's and NF1's comparisons, on both footings.

## Verdict (per model)
- **FLAT:** |b| ≤ 2σ_b.
- **TILTED:** otherwise, with its sign.

Headline pair on background A, canonical footing for F and the law:
- **N1 TILTED, LAW FLAT:** Argon's expected outcome. Route E's version N has a surface-brightness problem that the law doesn't.
- **BOTH FLAT:** this test doesn't separate them on this sample. Argon's test does not kill N1.
- **N1 FLAT, LAW TILTED** and **BOTH TILTED:** as named.
- **[F DIFFERS]** appended if F's class differs from N1's. That's the part of Argon's claim that says the test kills N1 and not the floor.

Argon's numbers are scored separately: HIT if the measured b lies in its stated 1σ range, CLOSE if within its 2σ.

## Reported, not graded
1. Background B.
2. Υ 0.40 and 0.60. R = 1.5 and 3 R_d. V_flat 40–150.
3. Spearman ρ of δ against x, for robustness to outliers.
4. rms of δ per model.

## Checks
- **K1:** the slope code against `numpy.polyfit` on the real arrays: |d| ≤ 1e-10.
- **K2:** this path's N1 and N0 reproduce NF1's bin values in `../NF1_no_floor_rule/nf1_bins.json` (median Υ and ΔV in 60–100): Υ exact, ΔV within 1e-6.
- **MUTATE** (`--mutate`, separate outputs): δ + 0.1 x must change b by +0.1 to within 1e-9, and move a FLAT class to TILTED or say why not.
- Any K failure: no verdict, exit 1.
