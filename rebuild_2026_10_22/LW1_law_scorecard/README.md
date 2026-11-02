# LW1_law_scorecard: the a0 law fails K, X, Dw, DM and IC on both footings, S on alt too, and MW depends on a vertical form the law doesn't supply

Criteria: `FROZEN_CRITERIA.md` (e9694d20a9), committed alone first. `lw1_keys.py`, `lw1_xcop.py`, `lw1_dwarfs.py`, `lw1_dm.py`, `lw1_mw.py`, `lw1_read.py`; post-result `lw1_mw_stress.py`. Numbers in `lw1.out`, `lw1_results.json` and each part's `.out`, `.json`. **A law scorecard, not a claim of a theory:** kappa = 1/2 FITTED, no action, CMB and cluster cores not accounted for. Footings never pooled. Not blind. No line moved. Nothing here says the data favour the framework. Not theory closed. FG1's files aren't edited; corrections to its C4 column are listed below.

## Scorecard
| Line | canonical | alt | Source |
|---|---|---|---|
| S SPARC | PASS U 0.52, rms 0.0541 | **FAIL** U 0.44, rms 0.0537 | READ FG1 |
| Tl tilt | PASS +0.02 | PASS -0.02 | READ FG1 |
| LT LITTLE THINGS | PASS -0.025 | PASS -0.064 | READ FG1 |
| G groups | PASS Z +0.31 | PASS Z -0.31 | reproduced |
| **K** 15 keys, gas +0.005 | **FAIL** 10 of 15 at both f* | **FAIL** 10 of 15 at both f* | computed |
| **X** X-COP | **FAIL** +0.467, 0.476 | **FAIL** +0.434, 0.444 | computed |
| Ln KiDS isolated | PASS (first term zero by construction) | PASS | READ FG1 |
| **Dw** dwarfs, with EFE | **FAIL** | **FAIL** | computed |
| **MW** | form A **FAIL** INFEASIBLE; form R PASS, 1 in-prior cell | form A **FAIL** INFEASIBLE; form R PASS, 6 | computed |
| **DM** | form R **FAIL** r 1.239; form A NO LABEL, r 1.477 | form R **FAIL** r 1.204; form A NO LABEL, r 1.477 | computed |
| IC IC 1613 | **FAIL** E -0.593 (Z -7.9) | **FAIL** | READ FG1 |

UL1's measured-Upsilon gate already fails the law; carried, not redone. No line is NOT COMPUTABLE, though CFG577's exact Jeans factor for this nu wasn't recomputed.

## 1. Keys on the measured chain
Same five keys fail in all 8 cells of gas, f*, footing: G-MID-T2, G-MID-T3, G-MID-b, G-OUT-M3, G-OUT-b. FG1's 9 of 15 was the old template; on the measured chain it's 10 of 15, a different set. Gas +0 changes no label.

| Cell, gas +0.005 | M3 h 0.672, 0.686 | Z_tot | worst key | joint chi^2 / 15, p |
|---|---|---|---|---|
| canonical f* 0.034 | +4.76, +4.26 | +3.80, +3.39 | G-MID-T3 +4.86 | 65.0, 3e-8; 64.5, 4e-8 |
| canonical f* 0.0615 | +4.63, +4.14 | +3.70, +3.30 | G-MID-T3 +4.80 | 63.3, 7e-8; 63.0, 8e-8 |
| alt f* 0.034 | +3.99, +3.51 | +3.08, +2.71 | G-MID-T3 +4.54 | 56.0, 1e-6; 56.4, 1e-6 |
| alt f* 0.0615 | +3.85, +3.38 | +2.97, +2.60 | G-MID-T3 +4.48 | 54.6, 2e-6; 55.2, 2e-6 |

**Worse than the retired native profile on this statistic:** ZN4 reads G-OUT-M3 +4.41, Z_tot +3.51, joint p 0.002 in M3A1's cell, against the law's +4.76, +3.80, 3e-8 in the same cell. JOINT FAIL everywhere, and without G-OUT-M3 p stays 2e-5 to 5e-7. Jackknife R is harsher. M3A1's budget exists only for G-OUT-M3, so G-MID-T3 is stat-only. Its terms were built on canonical and are carried to alt. The law's seed term is 0; its gas term is its own. R is BA1's, recomputed on each run; it equals BA1's stored R to 0.

## 2. X-COP: the two numbers
**There's no sign difference.** Both are log10(M_HSE / M_model), positive where the model is short. The brief's "different sign convention" doesn't hold. **They are different models.** CS2's -0.151, 0.205 is its Burkert core rule with cold mass normalised to M_HSE - M_b at R500, rebuilt here to -0.1510, 0.2051. It isn't the a0 law, so FG1's C4 X cell shows another rule's row. The law's own number is DR1's.

| | canonical | alt |
|---|---|---|
| mean, rms | +0.467, 0.476 | +0.434, 0.444 |
| M_HSE / M_law, geometric | **2.93** | 2.72 |
| x 0.1, 0.2, 0.3, 0.5, 0.7 factor | 3.51, 3.39, 3.18, 2.66, 2.16 | 3.27, 3.15, 2.94, 2.46, 2.00 |
| median deficit at 0.5 R500 | 2.3e14 Msun, 61 % of M_HSE | 2.2e14, 58 % |
| median deficit at 0.7 R500 | 2.9e14 Msun, 54 % | 2.8e14, 50 % |

All 7 clusters are short, +0.42 to +0.55 canonical. The law multiplies the baryons by about 3.5 at 0.5 R500 and still lacks about 60 % of the hydrostatic mass. Bracket, not a grade: taking LF1's 0.12 dex off M_HSE leaves factors 2.23, 2.06.

## 3. Dwarfs with the external field
E1 is the record's solver (D10, S1's grid, Z2's host field), checked to 2e-13 against Z2's table. Median E (Z):

| Class | plain, canonical | **E1, canonical** | plain, alt | **E1, alt** |
|---|---|---|---|---|
| MW ultra-faint | +0.59 (+5.22) | **+1.30 (+6.76)** | +0.55 (+4.87) | **+1.26 (+6.59)** |
| bright M31 | +0.23 (+2.20) | **+0.55 (+3.97)** | +0.19 (+1.81) | **+0.52 (+3.66)** |
| M31 others | +0.75 (+2.29) | **+0.97 (+2.71)** | +0.71 (+2.12) | **+0.94 (+2.55)** |
| MW classical | +0.24 (+1.69) | +0.31 (+1.24) | +0.21 (+1.42) | +0.27 (+1.08) |
| LG field | +0.05 (+0.57) | +0.04 (+0.53) | +0.01 (+0.08) | +0.00 (+0.05) |

**The field makes it worse, as FG1 expected, and by more than was stated:** the ultra-faint deficit goes from a factor 3.9 to 20 in acceleration. Alt's bright M31 passes plain and fails with it. E_lo, E_hi and the algebraic E2 all fail too. Plain and E1 agree on the label, so leaving the term out isn't what fails the line, and including it doesn't help.

**Tides, READ Z2, not recomputed:** not implicated for any flavour; the AQUAL + EFE clean subset is still +0.693 +- 0.150 (N 7). **Against E1 itself:** at fixed M_V the data are flat in host field, -0.05 +- 0.19 dex per dex, where AQUAL with its EFE predicts -0.76. So neither plain nor EFE describes these satellites; T1 has them failing at every EFE strength.

## 4. DiskMass and the Milky Way
**The law only gives the in-plane force.** With no action, the vertical force needs a form: A is the field equation (AQUAL, QUMOND one-zone), R is the round rule, which has no field equation behind it.

**DiskMass** (line r 0.90-1.10, n >= 27). Form R r 1.239 [1.192, 1.271], Y_K 0.438 canonical; 1.204 [1.156, 1.246], 0.394 alt, n 30: FAIL. 2.2 h_R 1.158, 1.126: FAIL. Form A r 1.477, both: outside the line, but a0 x 1.5 barely moves r (0.0015, 0.011), so it gets NO LABEL as frozen. FG1's 1.250, 1.342 used a different nu, not this law's. CFG577's Jeans integral, 5-7 % upward on its nu, would move these further out; not recomputed. OD1 (read): old-star dispersions take the round rule's r to 0.82-0.88 at its frozen c, under the line, and it says the answer turns on a correction known only to 1.2-1.9. So this cell depends on sigma_z's tracer.

**Milky Way**, X5's 175 cells, UR3's gate (v_c, chi2_Kz, K_z(R0), Ou):

| | canonical | alt |
|---|---|---|
| Form A, AQUAL L* = 0 | **INFEASIBLE**, 0 cells, best D 2.33 | **INFEASIBLE**, 0 cells, D 2.34 |
| Passing X5's weaker gate | 7, K(R0) 76.7-77.8 | 4, K(R0) 76.9-80.9 |
| Form R | **FEASIBLE IN PRIORS**, 10, 1 in priors, D 0.78 | **FEASIBLE IN PRIORS**, 17, 6 in priors, D 0.60 |

**FG1's cell was generous on form A.** "FEASIBLE (wide priors only), 7 of 175" passed X5's gate; on the gate UR3 used for C1 and C2, it's INFEASIBLE. X5's scored row was L* 24 pc, v3 rather than the law; at L* = 0 the count is the same, 7 and 4, so that was a label problem only.

**Form R's pass, tested as a win (post-result, `lw1_mw_stress.py`; no grade changed):**
- It doesn't bite on a0: at a0 x 1.5 form R is still FEASIBLE IN PRIORS, 18 and 12 cells. The box can absorb that change, so this gate doesn't test the law's a0.
- Canonical rests on one in-prior cell, at the box's corner: Sigma_b 53.9 (+2 sigma), M_bb 2.12e10 (+2 sigma), R_d 2.60, K(R0) 70.1 (+1.7 sigma).
- Every in-prior cell misses the K_z scale length: h 3.30-3.38 against 2.72 +- 0.15, +3.9 to +4.4 sigma. That's X5's reported number, not in UR3's gate, so no label changes.
- Moving g_c from R to r changes no in-prior count.
- UL1's c correction concerns NFW starts. No halo here, so it doesn't apply.

**No single form clears both weighings.** Form R: MW passes, DiskMass fails. Form A: MW fails, DiskMass is at 1.477 with no label.

## Corrections to FG1's C4 column, as statements
K: 9 of 15 on the old template becomes 10 of 15 on the measured chain. X: NOT GRADED, showing another rule, becomes FAIL, factor 2.93. Dw: FAIL stands, larger. DM: NOT GRADED becomes FAIL by form R, on the law's own nu. MW: FAIL by X5's gate becomes FAIL on form A, PASS on form R. C4's failed lines grow from K, Dw, MW, IC to K, X, Dw, DM, IC, with MW form-dependent.

## Checks
K1 plain dwarfs vs FG1 |d| 0. K2 keys and preds vs DR1 |d| 0, groups 0. K3 X-COP vs DR1 0; CS2 rebuilt; FITS rows vs cached 3.9e-5, from G and Msun constants. K4 solver vs Z2 2.1e-13, xe 0. K5 UR3's no-extra and CFG576's RM, PD |d| 4.9e-4, to its 3 printed places. K6 AQUAL vs X5's L0 relative 0; Newton McMillan vs GD3's 3-place literal 4.7e-4. K7 R = I exact. **K8 not run:** M3A1 doesn't store its R. Rerun of the read byte-identical.

MUTATE a0 x 1.5: keys move up to 1.91, 2.11 in Z; canonical stays 10 of 15, alt falls to 5. X-COP to +0.396, +0.362. Dwarfs up to 0.085. DiskMass R to 1.162, 1.132. MW both forms move in D. Exceptions stated above: form A r on DiskMass, and form R's class on MW. The numeric thresholds for "moves" in `lw1_read.py` were set by me after the freeze, which only said "must move". No line flips to PASS under it that wasn't one already.

## Expectation against result
K, X, Dw, DiskMass R, MW form A: held. Z_tot +3.80 against my +3.5, and the ultra-faint rise was what Z2 implied. **Wrong:** I said form R on MW was unknown, and it passes on the frozen gate.

## Limits
Carried lines aren't recomputed. Form R's g_c uses in-plane g_b, one reading of a rule with no field equation. DiskMass is one-zone. X-COP masses are hydrostatic. K_V and h_z are DiskMass's adopted values. The freeze didn't say which MW form is primary, so I don't pick one. kappa = 1/2 FITTED. Not theory closed.
