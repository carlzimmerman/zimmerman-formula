# CFG940: faint gas-rich rotators (McQuinn+2022): above, on or below the law at low g_bar?

**Bottom line.**
- **LANE CLASS: NOT DIAGNOSTIC (DATA)**, both footings, every enclosed-mass estimator. **None of the 25 rotators reaches
  g_bar < 1e-12 at its measured radius.** The lowest is 10^−11.71 with total baryons (A, DDO154) and 10^−11.96 with
  exponential-disc enclosed baryons (B, DDO154). McQuinn+22 measure one speed at R_max = 0.35–5.8 kpc, and at those radii
  these dwarfs sit at 10^−12 to 10^−10.7. The dSph excess (+0.37 to +0.44 dex) lives below 10^−12, so this sample cannot
  test it. That is the same wall CFG931 hit with SPARC.
- **Secondary (all 25, labelled secondary, no lane-class weight):**
  - **A (total M_bary): S-BELOW.** Mean E = −0.304 ± 0.068 dex canonical (z −4.5), −0.340 ± 0.067 alt (z −5.0). No declared
    single systematic moves it.
  - **B (enclosed exponential discs): S-ON.** −0.083 ± 0.064 canonical, −0.121 ± 0.064 alt.
  - So the secondary class is **BRACKET-DEPENDENT**. B3 and B4 also give S-ON, B2 gives S-BELOW, and B5 (thin disc) and
    B6 split by footing.
  - **The C-UP corner reaches the law** (+0.117 / +0.079 dex): B plus doubled asymmetric drift, i − 1σ and distance −10 %.
- **Not ABOVE.** At their own g_bar no estimator puts the faint rotators above the law. Where dSphs exist at the same g_bar
  (cell [10^−12, 10^−11.5), 6 dwarfs at +0.240 / +0.201 dex), **the dSphs sit above the rotators**: D = +0.438 ± 0.122
  (A, z 3.6) and +0.318 ± 0.108 (B, z 2.9). With CFG880's 83 dwarfs: +0.374 (A), +0.253 (B). This is the pattern of the
  kinematic picture, but it is measured at g_bar ≳ 1e-12, where the dSph excess is only about +0.2 dex.
- **The deficit under A is not established as a problem for the law.** On the 7 galaxies also in SPARC (INFO I4):
  - McQuinn's V at R_max runs 13 % below SPARC's resolved curve at the same angular radius (median);
  - g_bar^A is 0.10 dex above SPARC's own mass model there, and B is 0.17 dex below it (so A is the closer end);
  - McQuinn E under A sits 0.18 dex below SPARC's own E at that radius. Under B it matches (+0.00).
  - So part of the A deficit belongs to the single-point estimator (lower edge speeds, total mass), not to the galaxies.
  - INFO only. It is a 7-galaxy check, and it is not in the frozen variant list.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. Cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

| | |
|---|---|
| Kind | DATA TEST (pre-registered), block CFG940–949 |
| Criteria | `FROZEN_CRITERIA.md`, **798e98d78**, committed alone before any script or number |
| Amendment | `AMENDMENT_A1.md`, **bda93d8db**, POST HOC: the frozen K3 failed on its own tolerance (D_PV's integer-arcsec rounding was left out; AGC111164 0.053 vs 0.051 kpc). Fixed before any residual; failed outputs kept as `*_preA1` |
| Results | **7c7fc125e**: `cfg940.py` and all outputs (K, MUTATE plant, MUTATE shuffle, main) |
| Not blind | McQuinn+22's published BTFR turn-down was known. Before freezing I had estimated by hand that AGC110482 sits below Newton under A, and written down the expectation that W1 might be empty under A. Criteria section 10 |

## The test

- **Data:** McQuinn+2022 Tables 1–2 (on disk, 64cee36d7), parsed by MRT byte positions with `python3 -I`, sha256 checked.
  - 25 dwarfs: 7 SHIELD, 12 VLA-ANGST, 6 LITTLE THINGS.
  - log M_bary 6.96–9.06; six have M* < 1e7.
- **g_obs** = V_cor²/R_max, with R_max = (D_PV/2) × Dist recomputed, unrounded.
- **g_bar:**
  - A = G·M_bary/R_max² (primary; an upper bound on the spherical enclosed value). Helium is included in the tabulated
    M_bary: K2's best factor is 1.36.
  - B = enclosed exponential discs: gas from Wang+16 with CFG873/874's extended root; stars from a SPARC-fitted size
    relation, log R_d = −2.945 + 0.360 log M* (66 galaxies, rms 0.24 dex).
  - Bracket variants B2–B6: compact root, R_HI := R_max, R_d × 2, Freeman thin disc, R_d ÷ 2.
- **Residual:** E = log10(g_obs/g_law), with g_law = g_bar ν_e(g_bar/a0).
  - σ_E propagates e_Vcor, e_Rmax (R enters g_obs and g_bar together) and the mass errors.
  - K4 found that e_Vcor already contains the inclination error, so it is not added again.
- **Comparison groups:** CFG828's 29 dSphs (primary; V10 uses CFG880's 83) and SPARC (Q ≤ 2, Inc ≥ 30°, errV/V < 0.1, the 8
  overlap galaxies removed), matched in 0.5-dex g_bar cells. Systematic floor 0.05 dex per group mean.
- **Classes:**
  - **W1 (g_bar < 1e-12; lane class):** DATA if N < 5. BELOW if mean E ≤ −2 se. ABOVE if mean E ≥ +0.20 and |D| < 2σ_D.
    ON if |mean E| < 2 se and D ≥ 3σ_D. Otherwise NOT DIAGNOSTIC.
  - **WS (all g_bar; secondary):** S-BELOW / S-ON / S-ABOVE at 2 se.

## Main result (dex)

| window | estimator | canonical | alt | class |
|---|---|---|---|---|
| **W1 g_bar < 1e-12** | A, B, B2–B6 | N 0 | N 0 | **NOT DIAGNOSTIC (DATA)** |
| WS (secondary) | **A** | −0.304 ± 0.068 (N 25) | −0.340 ± 0.067 | **S-BELOW** |
| WS | **B** | −0.083 ± 0.064 | −0.121 ± 0.064 | **S-ON** |
| WS | B2 compact gas root | −0.168 ± 0.064 | −0.205 ± 0.064 | S-BELOW |
| WS | B3 R_HI := R_max | −0.044 ± 0.064 | −0.082 ± 0.064 | S-ON |
| WS | B4 R_d × 2 | −0.023 ± 0.063 | −0.061 ± 0.063 | S-ON |
| WS | B5 Freeman thin disc | −0.123 ± 0.064 | −0.161 ± 0.064 | SPLIT BY FOOTING |
| WS | B6 R_d ÷ 2 | −0.122 ± 0.065 | −0.159 ± 0.065 | SPLIT BY FOOTING |
| WS | C-UP (B + AD×2 + i−1σ + D−10 %) | +0.117 ± 0.064 | +0.079 ± 0.064 | S-ON (INFO) |

**Matched comparisons (WS, canonical):**
- dSphs exist only in cell [−12, −11.5): 6 dwarfs at +0.240 (alt +0.201).
  - A: D = +0.438 ± 0.122 (5 rotators in the cell).
  - B: D = +0.318 ± 0.108 (18 rotators).
- SPARC at matched g_bar: D_SP = −0.327 ± 0.085 (A), −0.091 ± 0.086 (B).

**Post-hoc reading (no class weight):** if the frozen W1 rules were applied to all 25, A would give BELOW, and B would give
NOT DIAGNOSTIC (UNRESOLVED): |z| 1.3 / 1.9 < 2, and D z 2.9 < 3.

## Systematics, declared (WS; mean E canonical / alt)

| variant | A | class A | B | class B |
|---|---|---|---|---|
| V1 V = V_rot (no asymmetric drift) | −0.406 / −0.442 | S-BELOW | −0.185 / −0.223 | S-BELOW |
| V2 asymmetric drift × 2 | −0.229 / −0.266 | S-BELOW | −0.009 / −0.047 | S-ON |
| V3 inclination − 1σ (8°) | −0.217 / −0.253 | S-BELOW | +0.004 / −0.034 | S-ON |
| V4 inclination + 1σ | −0.365 / −0.401 | S-BELOW | −0.144 / −0.182 | S-BELOW |
| V5 i ≥ 40° only (N 21) | −0.302 / −0.338 | S-BELOW | −0.093 / −0.131 | S-ON |
| V6 distance −10 % | −0.258 / −0.294 | S-BELOW | −0.035 / −0.073 | S-ON |
| V7 distance +10 % | −0.346 / −0.382 | S-BELOW | −0.127 / −0.165 | S-ON / S-BELOW |
| V9 kernel ν_simple (g_N = g²/(g+a0)) | −0.305 / −0.341 | S-BELOW | −0.084 / −0.122 | S-ON |
| V10 dSphs = CFG880's 83 | (D +0.374) | S-BELOW | (D +0.253) | S-ON |
| V11 floor 0 (canonical z) | z −6.7 | S-BELOW | z −2.1 (alt −3.1) | S-BELOW |
| V12 floor 0.10 (canonical z) | z −2.8 | S-BELOW | z −0.8 (alt −1.1) | S-ON |
| V13 plateau only (N 6) | −0.171 / −0.207 | S-ON / S-BELOW | +0.023 / −0.015 | S-ON |
| V14 rising only (N 19) | −0.346 / −0.382 | S-BELOW | −0.117 / −0.155 | S-ON / S-BELOW |
| V15 D_PV ≥ 100″ (beam proxy, N 16) | −0.300 / −0.336 | S-BELOW | −0.105 / −0.143 | S-ON |
| V16 tabulated R_max | −0.303 / −0.339 | S-BELOW | −0.088 / −0.126 | S-ON |

- **A's S-BELOW is not FRAGILE.** No non-subset variant changes it; only the plateau-only subset (V13, canonical, z −1.99)
  does, and subsets carry no FRAGILE weight.
- **B's S-ON is fragile in the other direction.** V1 (no asymmetric drift), V4 (i + 1σ), V11 (no floor) and V7 (alt) push
  it to S-BELOW.
- **The enclosed-mass bracket is the dominant systematic.** A → B moves E by +0.22 dex. Inclination (+0.09 / −0.06),
  asymmetric drift (+0.08 / −0.10) and distance (±0.04) are each smaller, and together (C-UP) they cover the rest of the gap.
- **Rising vs plateau (I1):** rising curves sit 0.18 (A) / 0.14 (B) dex below plateau curves. Under B the six plateau
  galaxies sit on the law (+0.023 / −0.015).
  - Under A, rising curves are pushed down most, because mass beyond R_max is counted.
  - For the BTFR, a rising V(R_max) is only a lower bound on V_flat. Part of a published turn-down can be built this way.
  - The point test here is not the BTFR statistic, and this lane does not decide the turn-down.

## INFO lines (no class weight)

- **I2, M* < 1e7 (N 6: AGC111164, AGC229053, AGC742601, UGC04483, UGC08833, UGCA292):** A −0.371 ± 0.098 / −0.406;
  B −0.080 ± 0.079 / −0.118. None is in W1.
- **I3, Newtonian reading (CFG936):** mean log10(g_obs/g_bar) is +0.347 ± 0.081 (A) and +0.744 ± 0.067 (B): **ABOVE
  NEWTON** on every estimator. These are not Newtonian systems like CFG936's tidal dwarfs.
  - Individually, 5 galaxies sit below Newton under A: AGC110482 −0.32, UGCA292 −0.14, UGC04483 −0.09, DDO53 −0.07,
    DDO125 −0.01.
  - None sits below Newton under B.
- **I4, overlap calibration (SPARC rotmod without the point cut, at R_SP = R_max·D_SPARC/D_McQ, canonical):**

| galaxy (SPARC) | Q | V_McQ / V_SPARC | E_McQ A | E_McQ B | E_SPARC | log g_SP/g_A | log g_SP/g_B |
|---|---|---|---|---|---|---|---|
| DDO154 | 2 | 55 / 46.7 | +0.077 | +0.215 | −0.016 | −0.090 | +0.169 |
| NGC3109 | 1 | 58 / 66.5 | −0.016 | +0.117 | +0.162 | −0.102 | +0.143 |
| NGC3741 | 1 | 31 / 41.1 | −0.316 | −0.108 | +0.114 | −0.339 | +0.048 |
| Ho II (UGC04305) | 3 | 43 / 34.5 | −0.373 | −0.154 | −0.561 | +0.000 | +0.392 |
| UGC04483 | 2 | 18 / 20.8 | −0.528 | −0.085 | −0.126 | −0.431 | +0.343 |
| DDO125 (UGC07577) | 2 | 16 / 17.6 | −0.694 | −0.568 | −0.483 | −0.230 | −0.000 |
| WLM (UGCA444) | 2 | 29 / 35.5 | −0.191 | −0.058 | −0.060 | +0.071 | +0.318 |
| DDO126 (UGC07559) | 2 | out of SPARC's radial range | | | | | |

  - Medians: log g_SP/g_A −0.102, log g_SP/g_B +0.169. By the frozen reading rule, **A is the better-calibrated end**.
  - V_McQ/V_SP median 0.873. E_McQ(A) − E_SP −0.177; E_McQ(B) − E_SP +0.002.
  - SPARC's own E for these seven at that radius has median −0.06.
- **I5, by survey (A / B, canonical):** SHIELD −0.31 / −0.05; VLA-ANGST −0.34 / −0.13; LITTLE THINGS −0.23 / −0.03.

## Per-galaxy table

E in dex. A = total M_bary at R_max; B = exponential-disc enclosed baryons. log g in m/s². σ_E is canonical.

| galaxy | survey | R/P | i (deg) | R_max (kpc) | V_cor (km/s) | log M* | log M_bary | log g_obs | log g_bar A | log g_bar B | E_A can / alt | E_B can / alt | σ_E A / B | log(g_obs/g_bar) A / B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AGC110482 | SHIELD | R | 55 | 0.61 | 13 ± 2 | 7.39 | 7.70 | −11.04 | −10.72 | −11.33 | −0.763 / −0.796 | −0.412 / −0.449 | 0.140 / 0.145 | −0.32 / +0.29 |
| AGC111164 | SHIELD | R | 50 | 0.35 | 15 ± 2 | 6.57 | 6.96 | −10.68 | −10.98 | −11.52 | −0.246 / −0.281 | +0.058 / +0.020 | 0.122 / 0.147 | +0.30 / +0.84 |
| AGC229053 | SHIELD | R | 50 | 1.82 | 22 ± 3 | 6.91 | 7.66 | −11.06 | −11.71 | −11.93 | −0.223 / −0.261 | −0.111 / −0.150 | 0.120 / 0.123 | +0.65 / +0.86 |
| AGC731921 | SHIELD | R | 40 | 1.79 | 38 ± 6 | 7.71 | 8.02 | −10.58 | −11.34 | −11.57 | +0.055 / +0.018 | +0.182 / +0.144 | 0.142 / 0.143 | +0.76 / +0.99 |
| AGC739005 | SHIELD | R | 55 | 0.75 | 22 ± 2 | 7.17 | 7.62 | −10.68 | −10.99 | −11.47 | −0.242 / −0.277 | +0.029 / −0.009 | 0.086 / 0.108 | +0.31 / +0.79 |
| AGC742601 | SHIELD | R | 45 | 0.48 | 15 ± 2 | 6.63 | 7.25 | −10.81 | −10.96 | −11.54 | −0.392 / −0.427 | −0.067 / −0.105 | 0.120 / 0.131 | +0.15 / +0.73 |
| AGC749237 | SHIELD | R | 54 | 0.99 | 26 ± 3 | 7.62 | 8.07 | −10.65 | −10.77 | −11.35 | −0.341 / −0.374 | −0.012 / −0.049 | 0.104 / 0.107 | +0.12 / +0.69 |
| DDO99 | VLA-ANGST | R | 90 | 2.16 | 22 ± 1 | 7.30 | 7.96 | −11.14 | −11.57 | −11.81 | −0.379 / −0.417 | −0.249 / −0.288 | 0.048 / 0.046 | +0.43 / +0.67 |
| DDO125 | VLA-ANGST | R | 66 | 1.68 | 16 ± 2 | 7.76 | 8.01 | −11.31 | −11.29 | −11.52 | −0.694 / −0.730 | −0.568 / −0.605 | 0.116 / 0.114 | −0.01 / +0.22 |
| DDO181 | VLA-ANGST | R | 65 | 1.76 | 22 ± 3 | 7.31 | 7.76 | −11.05 | −11.59 | −11.77 | −0.278 / −0.316 | −0.179 / −0.217 | 0.122 / 0.122 | +0.54 / +0.72 |
| DDO183 | VLA-ANGST | R | 90 | 1.38 | 16 ± 2 | 7.36 | 7.77 | −11.22 | −11.36 | −11.63 | −0.570 / −0.607 | −0.424 / −0.463 | 0.114 / 0.113 | +0.14 / +0.41 |
| NGC3109 | VLA-ANGST | P | 83 | 5.82 | 58 ± 1 | 8.28 | 8.91 | −10.73 | −11.48 | −11.72 | −0.016 / −0.053 | +0.117 / +0.078 | 0.031 / 0.030 | +0.75 / +0.99 |
| NGC3741 | VLA-ANGST | P | 67 | 3.21 | 31 ± 2 | 7.24 | 8.42 | −11.01 | −11.45 | −11.84 | −0.316 / −0.354 | −0.108 / −0.147 | 0.062 / 0.058 | +0.44 / +0.82 |
| SextansA | VLA-ANGST | P | 38 | 1.28 | 32 ± 6 | 7.43 | 8.18 | −10.59 | −10.89 | −11.48 | −0.205 / −0.239 | +0.129 / +0.092 | 0.168 / 0.167 | +0.30 / +0.90 |
| SextansB | VLA-ANGST | R | 53 | 1.74 | 34 ± 4 | 7.55 | 8.03 | −10.67 | −11.31 | −11.60 | −0.048 / −0.085 | +0.114 / +0.076 | 0.106 / 0.107 | +0.64 / +0.94 |
| UGC04483 | VLA-ANGST | R | 64 | 0.66 | 18 ± 2 | 6.92 | 7.79 | −10.80 | −10.70 | −11.48 | −0.528 / −0.560 | −0.085 / −0.122 | 0.103 / 0.108 | −0.09 / +0.68 |
| UGC08508 | VLA-ANGST | R | 63 | 1.16 | 24 ± 2 | 7.30 | 7.78 | −10.80 | −11.21 | −11.57 | −0.231 / −0.268 | −0.034 / −0.072 | 0.078 / 0.079 | +0.41 / +0.77 |
| UGC08833 | VLA-ANGST | R | 30 | 0.78 | 22 ± 5 | 6.95 | 7.46 | −10.70 | −11.18 | −11.58 | −0.148 / −0.185 | +0.072 / +0.034 | 0.203 / 0.204 | +0.49 / +0.89 |
| UGCA292 | VLA-ANGST | R | 52 | 0.99 | 15 ± 2 | 6.85 | 7.85 | −11.13 | −10.99 | −11.61 | −0.689 / −0.724 | −0.344 / −0.382 | 0.120 / 0.121 | −0.14 / +0.48 |
| DDO53 | LITTLE THINGS | R | 33 | 0.99 | 21 ± 5 | 7.45 | 8.08 | −10.84 | −10.77 | −11.40 | −0.532 / −0.566 | −0.169 / −0.206 | 0.213 / 0.214 | −0.07 / +0.56 |
| DDO126 | LITTLE THINGS | R | 59 | 3.07 | 36 ± 4 | 7.81 | 8.45 | −10.86 | −11.38 | −11.68 | −0.205 / −0.242 | −0.043 / −0.082 | 0.101 / 0.100 | +0.52 / +0.81 |
| DDO154 | LITTLE THINGS | P | 49 | 5.60 | 55 ± 7 | 7.42 | 8.65 | −10.76 | −11.70 | −11.96 | +0.077 / +0.039 | +0.215 / +0.176 | 0.112 / 0.112 | +0.95 / +1.20 |
| F564v3 | LITTLE THINGS | R | 51 | 1.61 | 27 ± 3 | 7.22 | 7.80 | −10.83 | −11.47 | −11.73 | −0.125 / −0.163 | +0.019 / −0.019 | 0.101 / 0.101 | +0.63 / +0.90 |
| HoII | LITTLE THINGS | P | 34 | 4.44 | 43 ± 9 | 8.45 | 9.06 | −10.87 | −11.09 | −11.48 | −0.373 / −0.408 | −0.154 / −0.192 | 0.187 / 0.187 | +0.22 / +0.61 |
| WLM | LITTLE THINGS | P | 90 | 2.27 | 29 ± 3 | 7.46 | 8.06 | −10.92 | −11.51 | −11.75 | −0.191 / −0.229 | −0.058 / −0.097 | 0.103 / 0.095 | +0.59 / +0.83 |

Median R_max / R_HI(Wang+16) is 0.83, R_max / R_s(gas) 1.27 and R_max / R_d* 2.74. There were no gas-root fallbacks.

## Controls

| control | result |
|---|---|
| K0 integrity | sha256 = PROVENANCE for both tables; 25 rows each, same order; 7 SHIELD rows first |
| K1 log M_dyn | V_cor reproduces the paper's log M_dyn for 25/25 within rounding; V_rot only 17/25 (so the paper used V_cor) |
| K2 helium | f_He 1.36 passes (max 0.013 dex), 1.33 just misses (0.018): helium included, M_bary as tabulated |
| K3 V_rot, R_max | V_rot = V_PV/(2 sin i) to 0.92 km/s. R_max: FAILED the frozen 0.051 kpc (0.053, AGC111164); PASS under A1 (max dR/tol 0.84) |
| K4 inclination error | already inside e_Vcor (rms 0.33 vs 2.88 km/s): not added again |
| K5 CFG828 | reproduced exactly (max diff 0): N_in 8, D +0.051 ± 0.073, dSph out-of-range mean +0.438 (alt +0.398) |
| K6 CFG919 DW | reproduced exactly: +0.372 / +0.332 dex (83 dwarfs; CFG880 slice exec'd read-only) |
| K7 SPARC | 2696 points / 147 galaxies |
| MUTATE plant, W1 | **not recoverable at N = 0** (no rotator in the window, any estimator) |
| MUTATE plant, WS | P37 → S-ABOVE, P0 → S-ON, P−37 → S-BELOW on A and B, both footings; planted means exact (≤ 1e-9): all required controls met |
| MUTATE shuffle, WS | S1 (real data, within-cell rotator/dSph label shuffle): median D_shuf +0.012 (A) / +0.008 (B) vs bars 0.031 / 0.027; \|z\| ≥ 3 in 1.4 % / 0.0 %: PASS. S2 on P0 (required on B canonical): median +0.003 ≤ 0.117: PASS |

## What this means, and what would decide it

- **For the question as posed (g_bar < 1e-12):** these data cannot answer it. The single measured radius is the edge of the
  detected HI at each survey's depth, and it stays above 1e-12 for all 25.
- **At the g_bar they reach (1e-12 to 1e-10.7):**
  - The faint rotators show **no dSph-like excess** (not ABOVE), and they sit 0.3–0.4 dex below the matched dSphs.
  - Whether they are ON the law (B, and CFG934's cooling-floor prediction for M_b ~ 1e7–1e9) or BELOW it (A) depends on how
    much of the gas lies inside R_max.
  - The deficit under A is within reach of the declared systematics (C-UP) and of the single-point estimator's offset from
    SPARC on the same galaxies (I4). **It is not a demonstrated failure of the law.**
- **What decides it:** per-radius HI surface densities, so that g_bar(R) comes from measured gas rather than a size
  relation. Also needed are resolved, asymmetric-drift-corrected rotation curves for faint rotators that reach several
  times the R_max used here.
  - On disk: LITTLE THINGS (CFG442/449; CFG931 A2 found ≤ 4 faint rotators below 10^−11.5, offset from SPARC).
  - Not on disk: SHIELD resolved velocity fields and deeper HI. Nothing was downloaded by this lane.

## Reproduce

All runs use one core and about 0.09 GB, and take seconds. The data paths are passed as arguments:

```
D=../../real_research/data/faint_rotators_mcquinn2022
OMP_NUM_THREADS=1 nice -n 10 python3 -I cfg940.py --t1 $D/apjac9285t1_mrt.txt --t2 $D/apjac9285t2_mrt.txt --mode K        # cfg940_K.out
...                                                                                                    --mode plant    # cfg940_MUTATE_plant.out
...                                                                                                    --mode shuffle  # cfg940_MUTATE_shuffle.out
...                                                                                                    --mode main     # cfg940.out, cfg940_results.json
```

No other lane's files were edited. CFG880's input slice was exec'd read-only with writes refused. CFG827, CFG824, CFG828,
CFG919, CFG931 and SPARC were only read. The data files are untouched.

κ = ½ FITTED; footings never pooled; not theory closed.
