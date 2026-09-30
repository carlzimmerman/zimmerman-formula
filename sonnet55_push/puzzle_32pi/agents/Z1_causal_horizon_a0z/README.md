# Lane Z1: the causal-horizon cutoffs as a0(z) laws, and the discriminating-test table

## Bottom line (verdict: DISCRIMINATING TEST; NOTHING NEW on the derivation; kappa = 1/2 stays FITTED)
1. The five declared cutoffs (d_p, d_e, c/H(z), R*, 2R*) give only **four distinct z-shapes**: flat (R*, 2R*), H(z) (c/H), particle horizon (radius and diameter share one shape) and a mild event-horizon shape. The **particle-horizon law D = c^2/(2 d_p(z))** predicts a0(z)/a0(0) = 1.74 / 2.63 / 4.80 / 6.05 / 7.41 / 13.7 at z = 0.5 / 1 / 2 / 2.5 / 3 / 5 (**+0.78 dex at 2.5**), 1.6x steeper than the H(z) law (3.77) and 2.8x the LambdaCDM-native +0.33 dex; it equals the H(z) law only in a matter-only universe. The event-horizon law (+0.21 dex) is dead on LEVEL (5.3x SPARC).
2. **The data in hand do not exclude D at a claimable level, and do not confirm it.** Against it: Milgrom 2017's Table I recomputed (Delta chi2 = +50..+220 over flat at face value, but the observers' model-dependent zeta_obs can absorb an offset of 0.29, inside the 0.40-0.50 that halving M_b gives); the record's Jeanneau deep refit (1.9 sigma honest; needs a baryon DEFICIT); the KROSS sample (-7.2 sigma at the record's decision cell, but it fits at outer pressure scale s = 2.6). For it: MUSE-DARK III's headline a0(0.87)/a0(0) = 2.38 (D +0.05 sigma; flat -14.9, H(z) -6.2; the record's non-diagnostic datum) and KURVS at the published pressure prescriptions. Nothing here is a detection either way.
3. **Allowed a0(2.5)/a0(0)** (honest 2-sigma rows, family E(z)^p; a D-shaped family agrees to 7%): about **0.3 to 6.0 from the data rows alone; 0.3 to 1.3 if Milgrom's table is taken at face value; 0.3 to 3.8 with the 0.18 zeta offset the H(z) law itself needs**. The rising side closes at a0(2.5)/a0(0) ~ 4-6; D (6.05) sits at the edge; the falling side is open down to ~0.3.
4. **Decisive test** (z ~ 2.5, deep MOND, 0.1 dex): flat vs LambdaCDM-native / H(z) / D at 3.3 / 5.8 / 7.8 sigma, but **H(z) vs D only 2.1 sigma** (needs 0.07 dex for 3 sigma): 0.1 dex decides "flat or rising", not which rising law. No lane in hand reaches it (KMOS3D not feasible, CFG196 0.91 sigma, KURVS/KROSS nuisance-limited at z <= 1.5); only the lensed NIRSpec-IFU + ALMA rotator does, and it needs the 0.25-dex mass-scale floor cut to ~0.1.
5. **The coincidence:** R*/R_p = 1.0995 (Planck-like), H0-independent, 1.06-1.10 over the record's Omega_m values, equal to 1 only at Omega_Lambda = 0.731 (6.6 sigma away). It is a "why now" coincidence: R_p grows, R* does not, and they cross 1.07 Gyr in the FUTURE (a* = 1.075), tighter than Omega_m = Omega_Lambda (3.5 Gyr ago). Flat and D differ exactly by R*/d_p(z): 9.95% today (0.8 sigma of SPARC's analysis scatter), so **no z = 0 observable separates them**; the lowest-z separator is a0 binned over z = 0.15-0.45 (D changes by 38% across it; the record's forecast formula gives 2.2 / 3.5 / 6.7 sigma for KiDS-now / combined / LSST-Euclid).

## What I did (declared before computing; six scripts, one shared module)
Candidates and rule as in p11 (`p11_machian_cutoff_candidates.py`): a0 = c^2/R_c, proper lengths at t(z), Planck-like flat LCDM with radiation (H0 67.4, Om 0.315, Or 9.1e-5). No candidate was added to make a law fit. Each script states its expectations at the top; where an expectation failed the failure is kept in a `*_firstrun*/*_secondrun*/*_thirdrun*` output and listed below.

| script | content | checks | controls / mutations |
|---|---|---|---|
| `z01_cutoff_laws.py` | the laws, absolute levels, structure, cosmology sensitivity | 14/14 | analytic limits (EdS d_p = 2c/H, de Sitter d_e = c/H0, radiation d_p = c/H), p11 reproduction, comoving-horizon mutation |
| `z02_data_constraints.py` | laws vs MUSE-DARK III, CFG198 slopes, Jeanneau deep refit, TFR ledger, literature rows | 17/17 | CFG190/CFG198/L276/refit reproduced; look-elsewhere control; 3 mutations |
| `z03_milgrom_table.py` | Milgrom 2017 Table I recomputed law by law | 11/11 | table columns reproduced; 3 mutations |
| `z04_kurvs_pipeline.py` (+`zkurvs.py`) | the record's KURVS/KROSS pipeline with the new laws | 9/9, `MUTATE=1` 5/5, `MUTATE=2` 5/5 | CFG160/CFG170/CFG175 cells reproduced; injected-truth power checks |
| `z05_decisive_tests.py` | z ~ 2.5 outcome table, lane reach, allowed range | 16/16 | CFG52 floor and the record's forecast script reproduced; 3 mutations |
| `z06_coincidence_Rstar_Rp.py` | R*/R_p vs parameters and time; low-z separability | 15/15 | p11 reproduced; H0-cancellation and comoving mutations |

`run_all.sh` reruns everything in about 25 s, exit 0: **82 checks pass, 0 fail (+10 in the two pinned MUTATE runs); 20 controls, 14 in-script mutations.** numpy 1.26.4, scipy 1.14.1. The record is only READ (CFG141's pipeline is exec'd unmutated exactly as CFG175 does; nothing is written outside this directory).

Papers actually opened (arXiv): 1703.06110 (full text), 2405.01841 (text), 2409.11425 (tables), 2604.22613, 2603.28856, 1703.04321, 1810.07202, 2209.12199, 2409.17956, 2504.20857, 2206.04333 (abstracts). NOT opened: the McGaugh/Milgrom-group "no BTFR evolution" claims, PHIBSS gas (carried from the record), Tian+24 clusters.

## 1. The implied laws (`z01`)
a0(z)/a0(0) and, in brackets, dex. A radius vs a diameter (factor 2) or c/H vs cH/Z changes the LEVEL only.

| law | z=0.5 | z=1 | z=2 | z=2.5 | z=3 | z=5 | a0(0) level |
|---|---|---|---|---|---|---|---|
| flat: R*, 2R* | 1 | 1 | 1 | 1 | 1 | 1 | 2R*: 0.936e-10 (0.870 SPARC); R*: 1.87e-10 |
| H(z): c/H(z), cH/Z | 1.32 (+.12) | 1.79 (+.25) | 3.03 (+.48) | 3.77 (+.58) | 4.57 (+.66) | 8.30 (+.92) | cH0/Z 1.131e-10 (1.05); cH0 6.5e-10 |
| **particle horizon d_p** | **1.74 (+.24)** | **2.63 (+.42)** | **4.80 (+.68)** | **6.05 (+.78)** | **7.41 (+.87)** | **13.7 (+1.14)** | diameter 1.029e-10 (0.956); radius 2.06e-10 (1.91) |
| event horizon d_e | 1.09 (+.04) | 1.20 (+.08) | 1.47 (+.17) | 1.62 (+.21) | 1.76 (+.25) | 2.35 (+.37) | 5.70e-10 (5.29) |
| ref: LambdaCDM-native (L274) | 1.08 | 1.23 | 1.77 | 2.16 (+.33) | 2.62 | 5.32 | |
| ref: T = t/t0 (CFG175) | 0.62 | 0.42 | 0.24 | 0.19 | 0.16 | 0.09 | |
| ref: MUSE-III linear 1+1.59z | 1.80 | 2.59 | 4.18 | 4.98 | 5.77 | 8.95 | |

- **D vs H(z):** in EdS d_p = 2c/H exactly, so D = H(z) there (control C2). In this universe d_p H/c = 3.18 today, 2.16 at z = 1, 1.98 at 2.5, 1.79 at 50, so D/H(z) = 1.32 / 1.47 / 1.60 at z = 0.5 / 1 / 2.5. Slope today: d ln a0/dz = 1 + c/(H0 d_p) = 1.314 (D) against 3 Om/2 = 0.473 (H(z)): D falls at 9.1% per Gyr today, the H(z) law at 3.3%.
- **Robust:** D(2.5) = 5.91-6.09 over Om 0.28-0.34 with radiation on/off; 6.04 for a DESY5-like w0wa. H0 cancels. The horizon integral converges early as a_min/sqrt(Or); it is undefined (much larger) if inflation precedes the hot big bang, a conceptual caveat to the whole "particle horizon" reading.
- **Level:** only the diameter (0.956 SPARC) and 2R* (0.870) sit inside SPARC's ~12% analysis scatter; the level match of D is the p11 numerology-class coincidence (an 8% match among ~6 candidates happens ~55% of the time).

## 2. The laws against the data in hand (`z02`, `z03`, `z04`; honest = statistics plus the record's systematic budget; "stat-only" numbers are shown only to say they are NOT claimed)
| constraint (record lane / paper) | flat | H(z) | **D** | LCDM-native | event |
|---|---|---|---|---|---|
| **MUSE-DARK III headline** log a0(0.87)/a0(0) = +0.377 +- 0.025 (2604.22613); pull, [95%-CI reading] | -14.9 [-29.9] | -6.2 [-12.5] | **+0.05 [+0.10]** | -12.0 | -12.3 |
| MUSE-DARK III shape: chi2 vs its linear fit over z = 0.33-1.44 (5 points, 0 parameters) | 948 | 251 | **5.0** | 694 | n/a |
| CFG198 per-galaxy slopes, SED masses (95% CIs [-0.47,+0.36], [-0.23,+0.35]); law slope dex/z | 0 in | +0.258 in | **+0.342 in (edge)** | +0.123 in | +0.088 in |
| ... inside in how many of 7 SED-mass rows; and III's own fitted-mass route (+0.51..+1.07) | 7; out | 6; out | **4; out** | 7; out | n/a |
| **Jeanneau deep refit** (N = 61, z 1.06, g_bar/a0 0.16): Delta_b = +0.140 +- 0.070 +- 0.272; honest pull (stat-only) | -0.51 (-2.0) | -1.35 (-5.2) | **-1.93 (-7.5)** | -0.81 | -0.76 |
| TFR ledger, 4 baryonic rows, chi2 (4 dof), max honest pull | 2.68, 1.25 | 1.69, 1.06 | **1.73, 0.93** | 2.16, 1.19 | 2.33, 1.20 |
| **Milgrom 2017 Table I** (six discs z 0.85-2.38), zeta_1/2 chi2 (6 disc; reading U2, all six) [range over 8 readings] | 7.4 [0.5-19.6] | 55.9 [22-137] | **101.7 [50-242]** | 23.7 [5-61] | 16.5 |
| ... smallest one-sided offset on zeta_obs at which the law is accepted at p = 0.05 (a halving of M_b gives 0.40-0.50) | 0 | 0.18 | **0.29** | 0.06 | 0.03 |
| RC100 Z-slope, Z = log10 z, 17 low-g galaxies -0.2 +- 0.4 (2405.01841/2409.11425); all 100: 0.01 +- 0.2; law sigma | +0.5 / 0.0 | +2.1 / +3.2 | **+2.4 / +3.8** | +1.5 / +2.0 | n/a |
| Big Wheel z = 3.25 (2409.17956 abstract; g/a0 ~ 2.5 from the record; mass error ~0.25) | ~0 | 1.0 | **1.7** | 0.5 | 0.2 |
| **KURVS** through the record's pipeline, decision cell (Kretschmer s = 1, mu = 0.67): Delta' z | +3.3 | -0.1 | **-2.0** | +1.8 | +2.2 |
| ... P0 (no pressure correction); cells within 2 sigma of 24; fit point s0 (published prescriptions s = 1-3) | -2.3; 5; 0.39 | -4.6; 8; 1.03 | **-5.9; 12; 1.55** | -3.3; 7; 0.63 | -3.1; 5; 0.56 |
| **KROSS** (z 0.85, same pipeline, mu = 0.67, s = 1): Delta' z; fit point s0 | -0.2; 1.04 | -4.1; 1.87 | **-7.2; 2.64** | -1.5; 1.29 | -1.4; 1.27 |
| KURVS AND KROSS in one published (s, mu) cell within 2 sigma each; best common joint chi2 | no; 10.0 | yes; 5.0 | **no; 5.6** | yes; 5.4 | n/a; 6.6 |

**What each line does and does not say** (each carries the record's "non-diagnostic" caveats):
- **MUSE-DARK III** is a RAR-fitted apparent a0 from a LambdaCDM-halo decomposition with fitted stellar masses; LambdaCDM hydro gives an apparent x3 rise by z = 2 with no fundamental a0 (2206.04333); the record's CFG198 shows the rise travels with the fitted-mass route (SED masses: slope -0.04 [-0.47, +0.36]); MUSE-DARK II's bTFR (0.00 +- 0.06, 2603.28856) is inconsistent with III under any common law (CFG190). D is the only candidate within 2 sigma of the headline, but a random datum is matched by SOME of five laws 42% of the time (`z02` A1b), and I had p11's z = 0.5, 1 ratios and III's 2.38 in hand before writing the script, so "D fits" was a hand-interpolated expectation, not a blind prediction. It is a fact about the shape (D tracks III's line, chi2 = 5.0 for 5 points) and, with D's own normalisation, about the level too (a0(0) = 1.029e-10 vs III's intercept 1.00 +- 0.04, +0.7 sigma; a0(0.87) = 2.46 vs 2.38 +- 0.10, +0.8 sigma; the flat 2R* law gives 0.936 at both, -14 sigma at 0.87): not evidence for a causal-horizon origin.
- **Milgrom 2017** (1703.06110): the paper states only that ~4 a0 at z ~ 2 is "all but excluded" (no significance; masses +-50%; smaller a0 explicitly not excluded). The full table recomputed by law is the strongest data line: chi2 orders the laws by steepness in EVERY reading (flat < event < LambdaCDM-native < H(z) < D), Delta chi2 vs flat = 50-223 (D), 22-117 (H(z)), 5-41 (LambdaCDM-native). D stays > 2 sigma high in 4 of 5 galaxies (H(z) in 3 of 5) when the inclination-suspect one is dropped (reading U2). But zeta_obs is a model-dependent NFW fit and Milgrom's own footnote says larger values are likely: to keep D the fitted phantom fractions (0-0.2) must all be under-estimated by >= 0.29, and the arithmetic of a halved M_b gives 0.40-0.50. So "all but excluded at face value, not excluded once that systematic is allowed". This also shows the record's shorthand "Milgrom excludes the H(z) rival" is supported by the table (offset 0.18 needed) but NOT by the paper's ~4 a0 sentence.
- **KURVS / KROSS** (record pipeline unchanged; velocities are the authors' MODEL at R_max, CFG140 correction; CFG189/CFG194: 12 of 19 marker choices leave the class): the same law moves by 0.85 dex across the record's own (s, mu) cells, 3.7x the D-vs-flat separation (0.23 dex = 4.8 sigma stat), so the lane cannot decide D vs flat until s and mu are measured. In this pipeline the FLAT law needs LESS outer pressure support (s0 = 0.39) than every published prescription (s = 1-3); D needs the most (KURVS 1.55, KROSS 2.64). The coherent velocity change that would bring each law to zero at the decision cell: flat -29%, H(z) +1.2%, D +18%, event -19%, LambdaCDM-native -16%. CFG184's beam-smearing range (effective s 0.40-0.96) and CFG189's marker shifts (-0.02 dex) were not re-run for D. My post-hoc expectation that KROSS would push D out was wrong at a common cell (joint chi2: D 5.6 < flat 10.0).
- **Jeanneau deep refit** (record): D's -0.38 dex prediction against +0.14 needs FEWER baryons, while the gas stress (HI x0.5/x2 gives +0.09/+0.32) and the selection bias (+0.02..+0.11) push the other way. RC100 slopes are reference-only by their authors (deep-MOND formula at R_e; selection contested), in log10 z.

**Acceptance matrix** (2-sigma honest; `z05` A5; Y = not excluded):

| law | Jeanneau deep | TFR ledger | CFG198 SED | Milgrom off 0 | Milgrom off 0.18 | Milgrom off 0.30 | MUSE-III headline | KURVS&KROSS pub. cell |
|---|---|---|---|---|---|---|---|---|
| flat | Y | Y | Y | Y | Y | x | x | x |
| H(z) | Y | Y | Y | x | Y | Y | x | Y |
| **D** | Y | Y | Y | x | x | Y | Y | x |
| LCDM-native | Y | Y | Y | x | Y | Y | x | Y |

No law is accepted by all eight rows. The two rows that reject flat (MUSE-III, the KURVS&KROSS cell) are the record's fragile/method-localised ones; the row that rejects D and H(z) at face value (Milgrom) is a high-acceleration, model-dependent one.

**Allowed a0(2.5)/a0(0)** (family E(z)^p, p = 0 flat, 0.58 LambdaCDM-native, 1 H(z), 1.36 D; every listed row must hold at 2 sigma):

| rows | p | a0(2.5)/a0(0) | dex |
|---|---|---|---|
| A data only: Jeanneau deep + TFR ledger + CFG198 SED routes | -0.90..+1.35 | 0.30 - 6.0 | -0.52..+0.78 |
| B A + Milgrom at face value | -0.90..+0.20 | 0.30 - 1.3 | -0.52..+0.12 |
| C A + Milgrom with zeta offset 0.18 | -0.85..+1.00 | 0.32 - 3.8 | -0.49..+0.58 |
| D A + Milgrom with zeta offset 0.30 | +0.20..+1.35 | 1.3 - 6.0 | +0.12..+0.78 |
| E C + KURVS AND KROSS in one published cell (fragile lean) | +0.40..+1.00 | 1.7 - 3.8 | +0.23..+0.58 |
| scenario: MUSE-III at face value | +1.5..+1.9 | 7.3 - 12 | +0.86..+1.09 |

The D-shaped family a0(0) D(z)^q gives 0.37 - 3.5 for row C (upper edge within 7% of the E^p family). MUSE-III at face value lies above the upper edge of A and C: the rise cannot be both the fundamental a0 and something the other honest rows allow. The falling side: Jeanneau and the ledger do not bound it; CFG198's SED-mass CIs do, near 0.3 (the T law, 0.19, lies beyond it). The bracket is set by the systematic budgets: shrinking the Jeanneau band to its statistical value halves the allowed p range (mutation M1).

## 3. The decisive-test table (`z05`)
Predictions at z = 2.5 in Delta log10 a0 and in the BTFR mass-axis zero point (exact P2 map, y = g_bar/a0(0)):

| law | Delta log a0 | Delta_b y=0.1 | y=0.3 | y=1 |
|---|---|---|---|---|
| flat (framework; R*, 2R*) | 0.000 | 0.00 | 0.00 | 0.00 |
| LambdaCDM-native | +0.334 | -0.30 | -0.25 | -0.16 |
| H(z) tracking (cH/Z) | +0.576 | -0.54 | -0.47 | -0.33 |
| particle horizon D | +0.782 | -0.74 | -0.67 | -0.50 |

The exact map transmits MORE of a large a0 shift to the mass axis than the ledger's local linearisation x/(2+x) (D: 0.95 / 0.86 / 0.64 at y = 0.1 / 0.3 / 1 against 0.83 / 0.62 / 0.33), so linearised "diluted" numbers for steep laws under-state them; deep-MOND selection (y <~ 0.3) keeps > 85% of D's shift. A RAR-FITTED a0 (MUSE-type) is a different observable: LambdaCDM's apparent x3 at z = 2 (+0.48) equals the H(z) law's +0.48 there, so it cannot separate LambdaCDM from H(z) at all.

**What a measurement m +- 0.10 dex of Delta log a0(2.5) concludes** (2-sigma windows |m - law| <= 0.20):

| m (dex) | survives |
|---|---|
| < -0.20 | none of the four (a0 fell, or a systematic) |
| -0.20 .. +0.13 | flat only |
| +0.13 .. +0.20 | flat, LambdaCDM-native |
| +0.20 .. +0.38 | LambdaCDM-native only |
| +0.38 .. +0.53 | H(z), LambdaCDM-native |
| +0.53 .. +0.58 | H(z) only (a 0.05-dex window) |
| +0.58 .. +0.78 | H(z), D |
| +0.78 .. +0.98 | D only |
| > +0.98 | none |

Pairwise separations (sigma at 0.05 / 0.10 / 0.13 / 0.25 dex): flat-D 15.6 / 7.8 / 6.0 / 3.1; flat-H(z) 11.5 / 5.8 / 4.4 / 2.3; flat-LambdaCDM 6.7 / 3.3 / 2.6 / 1.3; H(z)-D 4.1 / 2.1 / 1.6 / 0.8; H(z)-LambdaCDM 4.8 / 2.4 / 1.9 / 1.0; D-LambdaCDM 9.0 / 4.5 / 3.4 / 1.8. The 0.25-dex column is the record's correlated mass-scale floor (CFG52; 2.3 and 1.3 reproduced); 0.13 is PAPER7's single-rotator precision. **H(z) vs D needs <= 0.07 dex for 3 sigma; nothing pre-registered reaches that.**

**Lane reach** (lever = D-vs-flat separation in dex at the lane's redshift; record numbers cited, not re-derived):

| lane | z, regime | D-vs-flat lever | what it delivers | verdict for flat/D/H(z)/LCDM |
|---|---|---|---|---|
| KROSS | 0.85; g_bar/a0 0.3-1.7 | 0.37 | pipeline 6.7 sigma stat but the law moves 0.62 dex across (s, mu) | rejects D at the decision cell unless s ~ 2.6; nuisance-limited |
| MUSE-DARK (III RAR fit; II bTFR; CFG198) | 0.3-1.4; RAR / g_bar < 0.5 a0 | 0.38 (median z) | III: apparent a0, 15 sigma vs flat at face value; II/refit: honest +-0.27; CFG198 slope CI half-width ~0.4 dex/z vs 0.34 D-flat slope | non-diagnostic (mass route decides); D at the edge |
| KURVS-CDFS | 1.5; g_bar/a0 0.06-0.67 | 0.57 | 4.8 sigma stat; nuisance spread 0.85 dex; needs measured sigma(R) and gas (dust limits CFG142/163) | non-diagnostic until s and mu are measured |
| KMOS3D | 0.7-2.7; only 2-3 of 74 clean z >= 1.9 discs reach g_bar < a0 (CFG99) | 0.74 at z 2.3 | injected discs come back 28% slow (beam smearing) | NOT feasible |
| SINS-AO + PHIBSS CO (CFG196) | 2.2; g/a0 3-17 | 0.72 (H(z) 0.52) | pre-flight 0.91 sigma vs 2 needed (flat vs H(z)) | cannot discriminate; D not run |
| z > 3.5 discs (CFG197) | > 3.5 | > 0.95 | floor bound consistent for every law (M_dyn/M* 5.1) | nothing |
| **JWST NIRSpec IFU + ALMA lensed rotator (PAPER7 pre-registered; 21 candidates, none yet passes the gates)** | 2.3-2.9; needs g_bar < 0.3 a0 and M_b to ~0.1 dex | 0.74-0.78 | +-0.13 dex single object; 0.25-dex correlated mass floor caps flat vs LCDM-native at 1.3 sigma, vs H(z) at 2.3, vs D at 3.1 | the only route to the table above |
| z-binned weak-lensing RAR (KiDS/DES/HSC/Euclid) | 0.15-0.45; deep MOND | D changes 38% across the window (H(z) 19%, LCDM-native 4%) | record's forecast formula: 2.2 / 3.5 / 6.7 sigma for D (1.1 / 1.7 / 3.4 for H(z)) with 5% / 5% / 3% gas floors | the best LOW-z discriminator of flat vs D; forecast, not data |

## 4. The coincidence R*/R_p (`z06`)
- **Exact structure.** R* = sqrt(8 pi/3) c/H_L (H_L = H0 sqrt(Omega_Lambda)), so the coincidence is "R_p = 2.63 de Sitter-Hubble radii vs R* = 2.89". Both lengths scale as c/H0, so **R*/R_p is independent of H0** (identical to 1e-12 for H0 = 55-85; a mutation freezing rho_Lambda while changing H0 in R_p moves it by 10-40%). It depends only on (Omega_m, Omega_Lambda, Omega_r, Omega_k).
- **Parameters.** R*/R_p **decreases** monotonically with Omega_Lambda: 1.42 / 1.29 / 1.18 / 1.0995 / 1.07 / 0.96 / 0.85 at Omega_Lambda = 0.55 / 0.60 / 0.65 / 0.685 / 0.70 / 0.75 / 0.80 (radiation off lowers it by 0.02). At the record's Omega_m values: Planck 1.0995, CFG174 1.091, forecast script 1.097, DESI+CMB 1.073, DESI-BAO-alone 1.061; curvature +-0.01 moves it by 1%; a DESY5-like w0wa gives 1.11. Its parameter error is ~0.015, so **it is robustly 6-10% above 1, never 1**; R* = R_p would need Omega_Lambda = 0.731 (6.6 Planck sigma away).
- **Time.** R*/d_p(z) = 0.70 / 0.83 / 0.96 / 1.03 / 1.10 / 1.91 / 2.89 / 6.66 / 15.0 at z = -0.3 / -0.2 / -0.1 / -0.05 / 0 / 0.5 / 1 / 2.5 / 5. It is a MOMENT, not a constant: R* is fixed, d_p grows, and the two cross at a* = 1.075, **1.07 Gyr from now** (8% of the age), falling 8.6% per Gyr. Comparison with the record's other coincidence: Omega_m = Omega_Lambda was at a = 0.772 (3.5 Gyr ago), |ln a| = 0.26 against 0.07. The comoving horizon crosses at a = 1.42 instead, so the closeness depends on using the proper length. The ratio is within 5 / 10 / 20% of 1 for 12 / 23 / 46% of Omega_Lambda in 0.5-0.9 (the 10% threshold was chosen after seeing 1.0995).
- **Flat vs D at low z.** With both normalised at 2x the ratio of the two laws is exactly R*/d_p(z): 1.0995 today, 1.17 at z = 0.05, 1.25 at 0.1, 1.57 at 0.3, 1.91 at 0.5. The level difference today is 9.95% = 1.8 sigma of SPARC's statistical error, 0.8 of its analysis scatter: **no z = 0 observable separates them**, and the z <~ 0.05-0.08 samples (SPARC, MIGHTEE-HI 2504.20857, 'first tentative evidence for evolution') see at most a 7-11% change (D +6.7% at z = 0.05). The lowest-z separator is the binned a0 at z = 0.15-0.45. The two laws also differ qualitatively in the future: D falls below flat after a* and decays like 1/a, flat stays constant.
- **Reading.** A 10% coincidence is generic (p11: ~55% among six candidates; here ~a quarter of the Omega_Lambda range), it is a "why now" statement of the same kind as Omega_m ~ Omega_Lambda, and it says nothing about why the FACTOR 1/2 (or 32 pi) is what it is: the record's premise 2R* is the flat law, not the horizon law.

## Errors of mine fixed openly (first-run outputs kept)
- `z01` C2 tolerance (EdS check with a_min = 1e-12: truncation 2e-6) and S7 expectation (tail a_min/sqrt(Or), not 2e-6): the claims were right, my tolerances/analytics were wrong.
- `z02`: A2 threshold 'chi2 < 5' missed at 5.015 (arbitrary; replaced by p > 0.05); **B1 declared that D lies OUTSIDE CFG198's SED-route CIs: wrong, +0.342 is inside +0.360/+0.349**; F1 threshold -30 missed at -29.9; the `E1` sentence "the H(z) law is not excluded by Milgrom" was replaced after `z03` showed the table does disfavour it.
- `z03`: **four declared expectations failed** (flat chi2 < 6; LambdaCDM-native and event ~ flat; H(z) only mild; ratio ranges): the test is sensitive at the 10-20% level and orders every law by steepness; the "offset needed" criterion (chi2 <= 6) was replaced post hoc by p = 0.05 acceptance (disclosed in the code).
- `z04`: my post-hoc expectation that flat has the best joint KURVS+KROSS chi2 was wrong (D 5.6 < flat 10.0); `z05`: D3 dilution expectation wrong, L2 control value guessed (0.155; the record's script prints 18.8%), R0 used a radiation-free E(z), M2 (offset 0.6) was a two-sided error, A5's KURVS&KROSS clause wrong for D; `z06`: **F3a claimed the ratio increases with Omega_Lambda (it decreases; my monotonicity test passed on the wrong branch)** and the 1.08-1.11 range guess.
- The tracebacks in the kept first-run files had absolute paths; they were sanitised.

## What is NOT established
- That any cutoff is physical: no Machian kernel selects R_c = c^2/a0 (X3: the Sciama integral cuts off in frequency, not acceleration, and gives a0-independent coefficients); the particle horizon is undefined if inflation precedes the hot big bang; radius vs diameter is a factor 2 the construction does not fix.
- That the data favour, or exclude, the particle-horizon law: every line above is either non-diagnostic (MUSE-III, KURVS/KROSS, RC100), model-systematic-limited (Milgrom's zeta_obs), or 1.9 sigma at best under an honest band (Jeanneau). The Milgrom-table exclusion at face value is the strongest and rests on six galaxies with model-dependent fractions.
- That flat wins anything: flat is rejected by MUSE-III's headline (-15 sigma) and by the KURVS&KROSS published cell; it is accepted by the rows the record itself calls clean. kappa = 1/2 stays FITTED; the record's DO-NOT-CITE numbers are not used; nothing here says the theory is closed.
- The KURVS re-run inherits every fragility of CFG160-194 (model velocity, gas, pressure, radius); CFG184/189/194 variants were not re-run with D; D was not run through CFG196's pre-flight or the JWST lane.
- The E(z)^p range is a proxy family (D and LambdaCDM-native are only approximately powers of E, D/E^1.36 = 1.19 at z = 0.5-1); the D-shaped family agrees on the upper edge, but neither is a model.

## Verdict
**DISCRIMINATING TEST (nothing new on the derivation).** The cutoff table turns into one clean statement: the particle-horizon reading of the record's premise is not the flat law but a steep rising one, differing from it by +0.78 dex at z = 2.5, from H(z) by 0.21 dex and from LambdaCDM-native by 0.45 dex; the data in hand leave it disfavoured-not-excluded (Milgrom's table, the Jeanneau refit, KROSS against; MUSE-III and the published-pressure KURVS cells for), and a deep-MOND z ~ 2.5 measurement at 0.1 dex decides flat against every rising law but not which one. The R*/R_p match is a robust ~10% "why now" coincidence that carries no information about the factor 1/2.
