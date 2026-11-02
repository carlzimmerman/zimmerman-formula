# UX3_cluster_gas_term: no rule passes. The gas term takes canonical keys from 10 to 14 of 15 with k fitted on X-COP, and to 12 of 15 at pi^2, and G-OUT-M3 falls under 2, but G-OUT-all stays over 2 and alt reads 10. No measured switch is separated from "not a cluster"; every rule is FITTED

Criteria: `FROZEN_CRITERIA.md` (5935a4fc9e), committed alone first. `AMENDMENT_A1.md` (72cc6bd9d8) added C5 before any switched holdout was graded. Scripts `ux3_common.py`, `ux3_a.py`, `ux3_b.py`, `ux3_ok.py`, `ux3_grade.py`, `ux3_read.py`; numbers in `ux3_a.out`, `ux3_b.out`, `ux3_read.out`, their JSON and `_MUTATE` twins. **Not blind.** A description: no action, no field equation, nothing derived. The cold sector stays retired and nothing here reinstates it. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Labels (rule g = law x (1 + theta k g_gas/a0))
All rules have theta = 1 in clusters, so **keys and X-COP are the same row for C0, C1, C1b, C4, C5**.

| Rule | canonical, k pi^2 | canonical, k fit 13.29 | alt, k pi^2 | alt, k fit 14.25 |
|---|---|---|---|---|
| C1, C1b, C0, C4 | discs pass, X-COP all 7 fails: **no frozen label fits**, reads discs only | **KEYS FAIL** | discs pass, X-COP fails: no frozen label fits | **KEYS FAIL** |
| C5 gas-dominated | discs pass by a hair (even rms 0.195 at line 0.195), X-COP fails: no label | **DISC BREAK** | **DISC BREAK** | **DISC BREAK** |
| unswitched | **DISC BREAK** | **DISC BREAK** | **DISC BREAK** | **DISC BREAK** |

The frozen labels didn't cover discs passing with X-COP failing and keys failing. I say so and don't add a label. **DISCS AND CLUSTERS: none.**

## Keys, through LW1's path, gas +0.005. The law alone: 10 of 15, M3 +4.76, chi^2 65, p 3e-8
| | keys | over 2 | G-OUT-M3, h 0.672, 0.686 | chi^2/15, p boot, p jack (h 0.672) | X-COP unseen; all 7 |
|---|---|---|---|---|---|
| canonical, pi^2 | **12** | MID-T3, MID-b, OUT-all | +1.65, +1.36 | 22.2, 0.10, 0.02 | +0.040, 0.078; **+0.065, 0.106 FAIL** |
| **canonical, k fit** | **14** | **OUT-all -2.71, -2.77** | +0.58, +0.35 | 16.1, 0.38, 0.20 | -0.044, 0.081; -0.016, 0.089 |
| alt, pi^2 | 12 | MID-T3, MID-b, OUT-all | +1.19, +0.89 | 23.3, 0.08, 0.02 | **+0.056, 0.088 FAIL**; **+0.080 FAIL** |
| **alt, k fit** | **10** | OUT-all -3.23, OUT-M2, Mall, T1, T2 | -0.06, -0.27 | 18.5, 0.24, 0.14 | -0.042, 0.079; -0.015, 0.087 |

Same keys at f* 0.0615 and gas +0, except alt pi^2 at f* 0.0615 (11, adds OUT-M2). Canonical k fit stays 14, OUT-all -2.65 to -2.88. h 0.686 joint at pi^2 is p 0.045 canonical, 0.033 alt.

k scan, canonical (alt): 0.59 pi^2 12 (11), M3 +2.93; 0.7 pi^2 12 (11), M3 +2.59; 1.3 pi^2 13 (11), M3 +0.72; 1.7 pi^2 11 (10), OUT-all -3.17. **So M3 wants k above about 0.8 pi^2, OUT-all wants it below about pi^2, and no k clears both.** MID-T3 and OUT-all pull apart at the same k: at pi^2 it is +2.37 and -2.27. The miss is a shape in mass, temperature and radius, not a level. HSC's factor 1.7 on k fails more keys, on the KiDS-based keys.

**Read this as hard as a win.**
- It is the first measured-gas row here with M3 under 2 and X-COP passing and joint p above 0.05. FR1's H reached 14 at M3 +3.48. That is real, and it's still a fail.
- k came from 4 hydrostatic clusters and the keys are out of sample, so a one-number transfer from chi^2 65 to 16 is notable. **But it isn't independent of the record:** BF1's family came from X-COP after LM1 and GM1 had shown KiDS's gas ratio predicting X-COP. This is GM1's T2a in a different form.
- If HSE is 0.12 dex high (LF1), k fit overshoots X-COP at -0.136, and the k that fits drops to where M3 fails again.
- Post-result, no label: a plain multiplier fitted to X-COP (H 2.95, 2.73) reads **2 of 15, M3 -12.4, chi^2 428**. So the gas tie does real work in shape against that. A M500-tied term was not run, and GM1 found gas and M500 not separated, so "gas" isn't earned.
- pi^2 isn't supported. With A = 1 the fit wants 13.29, 14.25, which is 1.35-1.44 pi^2, different per footing. BF1's pi^2 leaned on its constant A. Say k is about 10-14, fitted.

## Part A: why discs break, odd SPARC names
Labels: **WHOLE DISC** on all graded rows but two; canonical's sqrt(.5)(1+f) and 1.5/(2-f) read INNER DISCS at 0.52 and 0.50, on the line. Not gas-rich dwarfs.

F1, A = 1, canonical (alt within 0.05 in shares): rms 0.217 against law 0.166.

| Bin | excess share | median d (law) |
|---|---|---|
| f < 0.25, 1110 points | 0.60 | -0.041 (+0.010) |
| Vflat > 120 | 0.59 | -0.044 (+0.005) |
| y high tercile | 0.52 | -0.043 (-0.011) |
| R < 1/3 R_last | 0.45 | -0.029 (-0.005) |
| gas-rich f > 0.5, Vflat < 120, 178 points | 0.27 | -0.197 (-0.054) |
| Vflat < 60, 66 points | 0.17 | -0.280 (-0.109) |

- **Most of the damage is in ordinary massive discs, in their stellar inner parts,** where y is large, so a small gas share still gives pi^2 g_gas/a0 of order 1. No single bin reset gets back near the law: best rms 0.188.
- **Gas-rich dwarfs miss worst per point,** over-predicted by 0.14-0.17 dex beyond the law, but they are few.
- **BF1's members also break on their constant.** Constant alone: rms 0.19-0.21, median +0.07 to +0.11, since A is about 0.75 at low f. Term alone 0.217. In a member the two partly cancel in the median, not in the scatter.
- Separation, AUC clusters above SPARC: ell 1.000, Sigma_gas and g_gas/a0 0.990, f 0.982; y 0.415, gas slope 0.416, rho_gas 0.260. **y and density don't separate them.** g_gas/a0 nearly does, which is why the family is close at all: X-COP 0.094-0.23, SPARC median 0.018, 95 % 0.068. Any threshold there would be read off this table, so FITTED.

## Part B: is there a switch?
| Rule | even SPARC rms (law 0.186, 0.187) | V < 60 shift | LT canonical, alt | FG1 path rms, U canonical |
|---|---|---|---|---|
| C1 random-motion share, sigma 10 | 0.188, 0.189 | -0.004, -0.003 | -0.028, -0.067 | 0.0544, 0.52 |
| C1b | 0.190, 0.192 | -0.020, -0.017 | -0.038, -0.075 | 0.0549, 0.49 |
| C0 control | 0.186, 0.187 | 0 | -0.025, -0.064 | 0.0541, 0.52 |
| C4 control ("clusters are big") | 0.186, 0.187 | 0 | -0.025, -0.064 | 0.0543, 0.52 |
| C5 gas-dominated | 0.195, 0.197 | -0.054, -0.046 | -0.073, **-0.106** | 0.0639, 0.52 |
| unswitched | **0.208, 0.213** | -0.075, -0.066 | -0.073, **-0.106** | 0.0765, 0.33 |

k pi^2 shown; k fit is in `ux3_b.out` and worse for C5.

**Answer: C1 is physically stated and passes discs, and that pass carries no evidence.** Discs pass largely by construction: V_rot >> 10 km/s shuts it off. It is measured-local in form, but sigma 10 km/s is an adopted, PROVISIONAL value, and clusters' V_rot = 0 is idealised. Its one separating prediction, a lift in slow discs, is -0.002 to -0.010 dex, unmeasurable. **It can't be told from the "clusters are big" control on any line here.** C5, the switch that doesn't pass by construction, is damaged exactly by gas-rich dwarfs: the term doesn't follow gas share. So what's on the table is "hot gas counts, cold gas doesn't", stated, not tested. Alt's SPARC U 0.43 sits under the S line as the law's does. Gas-free systems (dSph, MW's stars) can't test it, and those failures of the law stay as they are. Groups: the grader's table has no gas, term unapplied, not a pass.

M/Mg at R500, z 0.1, Mg 1e12, 1e13, 1e14, 1e15, canonical: law 8.4, 5.1, 3.2, 2.2; pi^2 10.2, 8.0, 7.4, 8.1; k fit 10.8, 8.8, 8.5, 9.6. Read against GM1's tables, no grade: Sun and Lovisari+15 12.9 at lg M 13.6-14, so the rule runs **low in groups**; Lovisari+20 6.8 at lg M 14.9-15.5, so k fit runs **high at the top**. M/Mg rising above 1e14 is a sharp check with pointed gas and lensing.

## Part C: HSC against KiDS on the 35 shared clusters
Shear to shear, no gas, no law, no deprojection. A = KiDS shear / Okabe's NFW.

| h 0.672, raw | all | 0.18-0.26 Mpc | 0.38-0.81 | 1.18-2.49 |
|---|---|---|---|---|
| Frozen A | **0.650 +- 0.075** | 0.548 | 0.646 | 0.746 |
| Post-result, unbiased A | **0.746 +- 0.091** | 0.556 +- 0.118 | 0.676 +- 0.144 | 0.826 +- 0.148 |

Eq. 17 row 0.666, 0.768. h 0.686 0.585, 0.707. Catalogue M500 in place of Okabe's 0.611, 0.708; that's partly HSC-calibrated, so no third voice. Band edges: the criteria's overlapped at bin centres, so I split into bins 0-1, 2-4, 5-7.

- **Frozen label: UNRESOLVED,** 2.8 sigma with the 0.1 systematic. **My frozen estimator is biased low:** it weights by noisy masses, and a mock with Okabe's own errors (median 47 %) returns 0.77 for true A = 1. I hadn't thought of that when freezing. The estimator weighted by the law's V returns 0.98 on the same mock, and **post-result reads NOT A SHEAR GAP, 1.9 sigma.** Not a protected label: it's 25 % low at nearly 2 sigma, and "not a gap" is the rule's wording, not a claim that they agree.
- **What is settled: the factor in dM/Mg is an amplified small mass difference.** The law holds half the mass, so 25 +- 13 % in mass gives dM/Mg 3.24 +- 1.09 from HSC's own M/Mg, on top of KiDS's 3.09. The 6.28 against 3.09 closes with no gas or deprojection problem. **So GM1's factor 1.7-2 isn't a separate disagreement.**
- It isn't a KiDS low fluctuation: Q on the 35 is 5.11 +- 2.23 at x 0.5-1, gas-matched others 3.60 +- 1.14, all 5.37.
- A rises outward, 0.56 to 0.83, under 2 sigma; inner bins are the miscentring-exposed ones.
- **Not settled: which survey is right.** No independent third mass reaches these clusters on disk. Keys at k x 1.7 fail more, but keys are KiDS, so that's no vote.

## Checks
K1 k = 0 vs LW1 per key 0. K3 BF1 lines 0.0005, to print precision (first FAIL: my typo, in `AMENDMENT_A1.md`). K5 0 relative, frozen form 1e-9. K6 law path vs FG1: rms and U match on both. K7 asserted. **K4 FAILS its frozen 1e-6:** grader gas over catalogue gas is 1.0003, constant, sd 0; a constant-unit level, 3e-4. Gas share is right; f = 1/(1 + f*) holds. Not a verdict check.
**MUTATE:** k x 3 X-COP -0.25 to -0.42, FAILS, M3 moves 6.21, 7 of 15. Okabe masses shuffled: frozen A 0.019. **IV A moves only to 0.80, so IV's level is barely sensitive to which cluster holds which mass;** it tests the mean mass, as a ratio of sums must. f shuffled in Part A: inner share 0.88 on the shuffled rows, labels move. Rerun byte-identical: keys (g005 f* cells), A, B, read.

## Errors, disclosed
First grader run crashed at the dump, `CL` undefined; rows unaffected. First K4 used R500 in Mpc against a metre grid and read 0; found from the 0, fixed. First bootstrap gave nan; masked. K4's check in code had been written at 0.05, tightened to the frozen 1e-6, so it now fails. Part A printed unseen rows, disclosed in A1. The constant-multiplier row, IV estimator, mocks and M/Mg table are post-result. MUTATE's f shuffle was only read for labels.

## Expectation against result
WHOLE DISC 60 %: mostly, two on the line. C1 passes discs 75 %: yes. Keys 15: no. X-COP stays passing at A = 1, 60 %: wrong at pi^2, right at k fit. UNRESOLVED 55 %: as frozen. I expected failures at G-IN and low-mass terciles: wrong, G-IN is fine; it's OUT-all and MID-T3.

## Limits, unfinished
No action or field equation; the enclosed-mass form means nothing in a merger, and **the Bullet's gas-lens offset is untested and is the obvious threat to any gas-tied term.** Hydrostatic X-COP. M500-tied rival not run. DiskMass, Milky Way, IC 1613, dwarfs: law's rows unchanged by a hot-gas term, so those failures stand. Needs, not on disk: a third mass on the 35 clusters; pointed gas with lensing at Mg near 1e15. BF1's deeper run still going, untouched.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
