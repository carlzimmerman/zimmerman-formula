# CFG927 sealed forecast table (criteria 8791d53c3; sealed 2026-10-20)

Fisher Δχ² between each run's own Limber C_L^φφ and its same-pipeline control (Gaussian covariance, fiducial = control, no data).
Class: D = DISCRIMINATING (≥ 9), M = MARGINAL (4–9), B = BLIND (< 4), NC = NOT COMPUTABLE. `r` = ROBUST across ZHOLD/ZREL/KCUT/KLOW/BG,
`d` = RULE-DEPENDENT (member range in the JSON). L_sup per pair: T1x ≥ 3000, T2x ≥ 3000, NC1x ≥ 3000, P1 ≥ 3000 (max k > 7.98 h/Mpc share at L 8–3000: S0 0.0013, F − S0 0.0014; threshold 0.10).

| pair | footing / inputs | model | L ≤ 400 | L ≤ 763 | L ≤ 1000 | L ≤ 2000 | L ≤ 3000 | L_9 |
|---|---|---|---|---|---|---|---|---|
| T1x | canonical / inherited | ACT-DR6-like (L_min 40) | 0.07 Br | 0.45 Br | 0.79 Br | 1.86 Br | 1.97 Br | none ≤ 3000 |
| T1x | canonical / inherited | SO-baseline-like (L_min 30) | 0.29 Br | 2.53 Bd | 4.58 Md | 11.03 Dd | 12.77 Dd | 1590 |
| T1x | canonical / inherited | S4-like (L_min 30) | 0.68 Br | 12.41 Dd | 31.70 Dr | 143.11 Dr | 200.71 Dr | 703 |
| T1x | canonical / inherited | CV-limited (context) (L_min 30) | 0.89 Br | 24.40 Dr | 87.74 Dr | 1768 Dr | 8032 Dr | 623 |
| T2x | alt / inherited | ACT-DR6-like (L_min 40) | 0.06 Br | 0.42 Br | 0.73 Br | 1.73 Br | 1.83 Br | none ≤ 3000 |
| T2x | alt / inherited | SO-baseline-like (L_min 30) | 0.26 Br | 2.34 Br | 4.25 Md | 10.23 Dd | 11.84 Dd | 1712 |
| T2x | alt / inherited | S4-like (L_min 30) | 0.63 Br | 11.50 Dd | 29.42 Dr | 132.79 Dr | 186.05 Dr | 717 |
| T2x | alt / inherited | CV-limited (context) (L_min 30) | 0.82 Br | 22.62 Dr | 81.45 Dr | 1639 Dr | 7428 Dr | 633 |
| NC1x | canonical / native_cmb | ACT-DR6-like (L_min 40) | 0.08 Br | 0.53 Br | 0.91 Br | 2.11 Br | 2.22 Br | none ≤ 3000 |
| NC1x | canonical / native_cmb | SO-baseline-like (L_min 30) | 0.33 Br | 2.93 Bd | 5.25 Md | 12.40 Dd | 14.30 Dd | 1431 |
| NC1x | canonical / native_cmb | S4-like (L_min 30) | 0.77 Br | 14.03 Dd | 35.44 Dr | 156.83 Dr | 219.14 Dr | 682 |
| NC1x | canonical / native_cmb | CV-limited (context) (L_min 30) | 1.00 Bd | 27.15 Dr | 95.59 Dr | 1819 Dr | 8044 Dr | 609 |
| P1 | canonical / inherited | ACT-DR6-like (L_min 40) | 4.07 Md | 21.37 Dr | 32.31 Dr | 57.53 Dr | 59.37 Dr | 518 |
| P1 | canonical / inherited | SO-baseline-like (L_min 30) | 17.32 Dr | 117.30 Dr | 183.44 Dr | 334.25 Dr | 363.67 Dr | 339 |
| P1 | canonical / inherited | S4-like (L_min 30) | 40.68 Dr | 546.67 Dr | 1165 Dr | 3713 Dr | 4669 Dr | 295 |
| P1 | canonical / inherited | CV-limited (context) (L_min 30) | 53.38 Dr | 1050 Dr | 3061 Dr | 38930 Dr | 138034 Dr | 285 |

| pair | noise scan Δχ² at L 30–3000, f_sky 0.4, beam 1.4′ (Δ_T in μK-arcmin) | Δ_T for Δχ² = 9 | PR4 8–400 Asimov | CFG917 realised PR4 Δχ² | gate K / MUTATE |
|---|---|---|---|---|---|
| T1x | 20: 2.69, 10: 6.92, 6: 12.77, 3: 33.88, 2: 64.46, 1: 200.71, 0.5: 591.07, 0: 8032 | 8.03 | 0.018 | -0.088 | PASS / bites |
| T2x | 20: 2.49, 10: 6.42, 6: 11.84, 3: 31.42, 2: 59.78, 1: 186.05, 0.5: 547.46, 0: 7428 | 7.54 | 0.017 | -0.085 | PASS / bites |
| NC1x | 20: 3.02, 10: 7.77, 6: 14.30, 3: 37.71, 2: 71.31, 1: 219.14, 0.5: 635.90, 0: 8044 | 8.84 | 0.021 | -0.276 | PASS / bites |
| P1 | 20: 76.85, 10: 196.40, 6: 363.67, 3: 935.58, 2: 1691, 1: 4669, 0.5: 12214, 0: 138034 | > 20 | 1.034 | +1.881 | PASS / bites |

Noise models: ACT-DR6-like Δ_T 15.0, beam 1.4′, CMB ℓ T 600–3000 / P 600–3000, f_sky 0.25 (L_min 40 and baseline 40-763 from on-disk files (CFG649, CFG363); dT, beam, CMB l range, f_sky ILLUSTRATIVE); SO-baseline-like Δ_T 6.0, beam 1.4′, CMB ℓ T 30–3000 / P 30–5000, f_sky 0.4 (f_sky 0.40 from on-disk quote (SO lensing map over 40% sky); the rest ILLUSTRATIVE); S4-like Δ_T 1.0, beam 1.4′, CMB ℓ T 30–3000 / P 30–5000, f_sky 0.4 (all ILLUSTRATIVE round values); Planck-like-anchor Δ_T 30.0, beam 5.0′, CMB ℓ T 100–2048 / P 100–2048, f_sky 0.65 (ILLUSTRATIVE; K7 only).
K7 anchors (reported): Planck-like-anchor σ(A) 0.0190 vs on-disk 0.028 (ratio 0.68); ACT-DR6-like σ(A) 0.0127 vs on-disk 0.023 (ratio 0.55); SO-baseline-like σ(A) 0.0058; S4-like σ(A) 0.0026.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed. A forecast is not a measurement.
