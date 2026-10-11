# CFG631: what besides the law sets a galaxy's cold energy? One multiplicity-corrected multi-property search

Commits: step 0 (residual-free inventory and pre-flight) defe92ee8. Frozen criteria 06ca28e0d, committed alone. κ = ½ is fitted. The
footings (9.36e-11 / 1.13e-10) are never pooled. Kernel: repaired ν_mono. Cold energy's mass is still required. This is not a closed theory.

## Step 0: what is on disk (no downloads)
| sample | properties on disk | missing |
|---|---|---|
| SPARC (128 with an outer band) | f_gas (HI only), bulge (17 with f_bul > 5%), Σ_* / R_d, T, inclination, distance method, RC3 B−[3.6] colour (78), 2M++ density (109) | metallicity, H₂, ages; SFR only 23 (ALFALFA overlap) |
| WALLABY DR2 (85, CFG537 build) | f_gas, Σ_* (2MASS K), RC3 T, inclination, AllWISE W1−W2 (84) | SFR, H₂, bulges, environment; RC3 colour only 13; Hubble-flow distances only |
| KiDS f30 early types (26,568) | u−r, r−Ks, LePhare sSFR, photo-z, CFG509 companion count | sizes, Sérsic index, surface brightness, metallicity, gas |

Nothing needed a download for the frozen design. Optional small downloads that would add properties (owner approval needed; none
fetched): (1) AllWISE W1–W4 cone matches for the 175 SPARC positions (IRSA, ~50 kB). That gives SPARC a W1−W2 colour matching
WALLABY's and a W2−W3 sSFR proxy, plus W3 for WALLABY (~100 kB). (2) S4G/z0MGS-type SFR and H₂ compilations for SPARC (VizieR,
< 1 MB each). (3) KiDS lens sizes would need KiDS DR4 multi-band catalogue tiles (hundreds of GB). Not recommended.

## Results (`cfg631_discs.out`, `cfg631_kids.out`)
**Discs.** OLS of the CFG537 outer residual (R ≥ 3 R_d) on all properties jointly with log M_b as control. Effects are in dex across
each property's 16–84 range [95% interval]; p_fw comes from a 5000-draw permutation max-T over 26 t's. Canonical footing shown; alt
agrees to ≤ 0.004 dex.

| sample | property | effect | p_fw |
|---|---|---|---|
| SPARC | f_gas | +0.119 [−0.006, +0.244] | 0.58 |
| SPARC | bulge | −0.008 [−0.087, +0.070] | 1.00 |
| SPARC | log Σ_* | +0.107 [+0.004, +0.210] | 0.45 |
| SPARC | T | −0.147 [−0.264, −0.030] | 0.20 |
| SPARC | inclination | +0.024 [−0.027, +0.076] | 1.00 |
| SPARC | Hubble-flow distance | +0.024 [−0.029, +0.076] | 1.00 |
| SPARC | colour B−[3.6] | −0.030 [−0.166, +0.107] | 1.00 |
| SPARC | 2M++ density | −0.027 [−0.073, +0.019] | 0.97 |
| SPARC | log M_b (per 0.5 dex) | −0.015 [−0.040, +0.011] | control |
| WALLABY | f_gas | +0.001 [−0.085, +0.087] | 1.00 |
| WALLABY | log Σ_* | +0.009 [−0.091, +0.109] | 1.00 |
| WALLABY | T | −0.012 [−0.072, +0.049] | 1.00 |
| WALLABY | inclination | +0.087 [+0.005, +0.168] | 0.41 |
| WALLABY | W1−W2 | −0.091 [−0.154, −0.027] | 0.09 |
| WALLABY | log M_b (per 0.5 dex) | −0.042 [−0.088, +0.005] | control |

- Omnibus F (all core terms beyond mass): SPARC p 0.031 / 0.029, WALLABY p 0.24 / 0.25.
- **VERDICT (discs, frozen): INCONCLUSIVE.** No property is discovered in either sample, but SPARC's omnibus is < 0.05. The SPARC
  joint signal lies along one collinear "early type / dense / gas-poor" axis: T −0.15, Σ_* +0.11 and f_gas +0.12 partly cancel,
  with |r| 0.8–0.87 between them at fixed mass. That is CFG534's early-type outer excess again, and it does not separate into one
  property. WALLABY, which has the power for 0.1 dex T and f_gas effects, shows none of it: T −0.012 ± 0.03, f_gas +0.001 ± 0.04.
- Upper limits (WALLABY 95%): T, f_gas and Σ_* effects are each ≤ 0.07–0.11 dex across their ranges.
- Disc age reading: SPARC colour −0.03 dex, wrong sign for "older carries more" (one-sided p 0.65). It is uninformative
  (forecast MDE80 0.31 dex).
- Variant residual (SPARC g_bar < a₀/3): f_gas +0.22 (t 2.9), T −0.15 (t −2.1), Σ_* +0.12. Same axis.

**KiDS f30 early types.** Partial-property tertiles (each property partialled on M* quintiles, log M* and the other four properties).
D = ε_HIGH − ε_LOW in K9, four cells. The null comes from 200 joint permutations.

| property | D(K9) A-can / A-alt | T(K9) | T(K-in) | family-wise p | label |
|---|---|---|---|---|---|
| u−r (age) | +0.928 ± 0.33 / +0.850 ± 0.30 | +2.82 | +2.27 | 0.035 | ASSOCIATED |
| r−Ks | +0.32 / +0.30 | +0.94 | +1.43 | 0.91 | not |
| log sSFR | −0.06 / −0.05 | −0.16 | +1.28 | 1.00 | not |
| photo-z | +0.12 / +0.11 | +0.33 | +0.54 | 0.995 | not |
| companion count | +1.09 / +1.01 | +3.43 | −0.11 | 0.005 | ASSOCIATED (see caveat) |

- **AGE VERDICT (frozen): AGE CONFIRMED, HOLDS.** With r−Ks, sSFR, photo-z and environment controlled, D(K9) is +0.85 to +0.93 in
  every cell (CFG585: +0.86 to +0.94), with a one-sided empirical p of 0.015 and Z_emp +2.54. It neither strengthens nor fades.
  Partialled on M*, z and environment only: +0.81 to +0.89. With own leakage (post hoc): +0.86 to +0.94, Z +2.8. Redder lenses have
  *fewer* companions (λ 0.53 vs 0.62).
- **Companion count: an estimator systematic, not a second parameter.** The signal sits only in K9's outer bins (K-in T −0.11). The
  split selects on the very counts that set the satellite term, and the frozen estimator gives both groups the f30-average leakage.
  The post-hoc own-leakage rule cannot repair it (λ_LOW −1.46 is unphysical, because the split selects on count noise). Read it as
  unmodelled environment in the lens model, not cold energy.
- Calibration: the null |Z| ≥ 2 rate per cell is 0.060 (nominal 0.046), and the null T has sd 1.0. In this split the jackknife errors
  are roughly calibrated.

## Controls and MUTATE
- C1 PASS (exponential kernel reproduces CFG584's WALLABY slope, −0.0716 / −0.0686). Kernel swap changes Δ_out by < 5e-5 dex.
- C2 PASS (medians ≤ 0.036). C5 PASS (null FWER 0.065).
- C3 PASS (CFG585 D +0.9411 reproduced). C4 PASS (Δ median log M* 0.006).
- **Disc MUTATE PASS:** a 0.20 dex Σ_* injection is recovered exactly (linearity, 1e-9) and comes out REPLICATED (t +5.8 SPARC, +4.1 WALLABY).
- **KiDS known-signal recovery FAILS (frozen rule):** raw M* tertiles give D +0.41 to +0.44, Z 1.6 (1.74 with own leakage), not ≥ 2.
  By the frozen wording the KiDS part "has no teeth" for detecting that control. The early-type mass trend in f30 is weaker than
  the CFG531 summary implied, so the control was mis-chosen and is not evidence against the estimator. The permutation null (FWER
  calibrated, sd 1.0) is the operative check. The age result is reported under this caveat.
- KiDS shuffle: 200-draw null as above.

## Reading
- Composition (f_gas, bulge, r−Ks, T) does not set the residual: no disc property survives, and WALLABY bounds composition effects
  at ≤ 0.1 dex.
- Gravity strength (Σ_*, mass) does not set it either: the mass coefficient is ~0 or slightly negative in both samples, and Σ_* is
  null in WALLABY.
- Time is the one property that survives correction and controls, but only in KiDS early-type lensing. Redder-at-fixed-mass early
  types carry about +0.9 more fractional inner mass whatever their dust/metallicity colour, sSFR, redshift or neighbours. The disc
  samples cannot test it (SPARC colour MDE 0.31 dex; WALLABY has no age proxy beyond W1−W2, which leans *negative*, p_fw 0.09).
- So the best-supported reading: cold energy in massive early types depends on formation time, not on what the galaxy is made of or
  how strongly it gravitates. In discs there is no second parameter above ~0.1 dex.
- Not established: the framework has no mechanism for time-dependent gathering (CFG586). The KiDS estimator inherits the CFG529
  environment model and SHMR-based own-profiles (lane machinery; CFG700 sees the age signal on raw ESD).

Files: `cfg631_common.py` (property builders), `cfg631_inventory.*`, `cfg631_preflight.*`, `cfg631_discs.*` (+ `_MUTATE`),
`cfg631_kids.*`, `cfg631_posthoc_leakage.*` (post hoc, no verdict weight).
