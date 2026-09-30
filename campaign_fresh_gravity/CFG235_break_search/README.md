# CFG235 -- a pre-registered per-galaxy "break" search at z > 3.5, scored symmetrically for LambdaCDM and for the framework

- **Criteria:** `CFG235_FROZEN_CRITERIA.md` (sha256 `d70dad70f0964a645ae5963bb55db762a607ace212a4a404dac31b261137d9ba`, committed as "CFG235: frozen criteria", bfc86d36d), before any per-galaxy value was opened. No frozen line was changed. Wrong or ambiguous frozen lines are reported below and kept as written.
- **Standing rules:** kappa = 1/2 is FITTED. a0(z) FLAT is the framework's law; the rival a0 x E(z) is reported only and never bears a label. Nothing here says the data favour any theory, and nothing says any theory is closed. No network; the repo was not touched (scripts import repo modules read-only with bytecode writing disabled; outputs sit next to the scripts).
- **Re-run:** `ZF_REPO=<repo> bash CFG235_run_all.sh` from the directory that holds the scripts (about 7 to 12 minutes). Order: `00_sample` (prints the sample table first; exit 2 on a count or hash mismatch) -> `01_controls` (exit 1 = a control failed) -> `02_main` (refuses unless the controls file exists and passes; with failed controls only `CFG235_GATE_OVERRIDE=1`, set by `run_all.sh`, passes the gate and every output then carries a banner) -> `MUTATE=1..8 python3 CFG235_MUTATE.py` (exit 1 = the control bites) -> `03_report`.

## Bottom line (read this first)

- **This is a gross-outlier search, not a sensitive test of either law.** With the frozen systematics (M* 0.25 dex, dynamical 0.15 dex, 'wide' cell 0.30 / 0.25) a 3 sigma flag needs R_obs = M_dyn/M_bar(stars) below its floor by about a factor 20 to 100. A per-galaxy 3 sigma flag at N about 60 is not a detection without the trials correction: the chance count at m = 62 is 0.084 per criterion.
- **Flagged at T0 (z_rob > 3 in every frozen cell): ONE galaxy of 62, Danhaive 1082948, a KNOWN case.** F1 z_rob = 3.01 (cell GS / wide / P2 / canonical), L1 z_rob = 2.87. Label at T0: "breaks the framework only"; this is a threshold straddle (L1 2.87 vs F1 3.01, 0.14 sigma apart), not a row with 1 <= R_obs < nu: its separability index is 0.05 and its R_obs is about 0.02. It is a mass-estimate outlier (M_dyn much below M*), and with L1 at 2.87 it is not a LambdaCDM break either. It fails Bonferroni (z_B = 3.154; 3.01 < 3.154) and the permutation tier (adjusted p = 0.98). **Nothing survives the trials correction. No galaxy breaks LambdaCDM at T0 through L1 or L2.**
- **Outcome class, frozen wording applied literally: INCONCLUSIVE.** The conditions met: (a) T0 flags exist but no T2 (the permutation tier cannot fire, see failed controls), and (c) no row has a separability index S_i >= 3, so the two theories are indistinguishable at 3 sigma in this sample. (b) is not met (L2 is defined for 42 rows). Sub-statements: "framework survives (this test)" = true and "LambdaCDM survives (this test)" = true, but both are nearly guaranteed by the design (below), so they are not evidence for either.
- **Answer to the owner's question ("a z ~ 5 galaxy where a LambdaCDM dark-matter fit breaks"):** at the frozen 3 sigma, trials-corrected standard, none. Every L2 candidate by the owner's LITERAL wording (needed M200 above the mass where fewer than one halo is expected in 2 deg^2 x dz 1, at central values) is listed in `CFG235_02_main.out` (TABLE L2): 15 rows, z from 3.63 to 4.91 (for example Danhaive 1025101 at z = 4.91 needs log M200 = 14.6 at r = 1.2 kpc; 1090054 at z = 4.82 needs 13.8). None is a 3 sigma statement: the weakest frozen cell gives z_rob(L2) <= 0.8 for all of them, and the best primary-cell value is 2.24 (D_1090891). These need large NFW halos because r_e is about 1 kpc and the NFW cusp holds little mass there; no halo contraction or feedback core is modelled. They are reported, not claimed.

## Sample (frozen section 2; printed by `CFG235_00_sample.py` before any statistic)

N per source: Danhaive gold 41, CRISTAL (modelled) 14, Roman-Oliveira 4, Amvrosiadis (z >= 3.5) 2, ALPAKA ID 28 1; total 62, m = 62. Columns below are inputs (central values) and the final z_rob values (negative = R_obs far above the floor; positive = toward a break); `S` tier: stars-only floor; `G` tier: gas-only floor (Roman-Oliveira). UNDEF(z>5) = L2 outside the c-M calibration; UNDEF(floor) = no stellar floor; UNDEF(range) = solved M200 outside 1e10-1e15.

| id | z | tier | log M* | log M_dyn,enc | log M_b floor | flags | L1 z_rob | F1 z_rob | L2 |
|---|---|---|---|---|---|---|---|---|---|
| D_1028887 | 5.19 | S | 9.56 | 9.63 | 9.56 | V/s<1 | -1.14 | -0.96 | UNDEF(z>5) |
| D_1002030 | 5.18 | S | 9.48 | 10.24 | 9.48 | V/s<1 | -2.88 | -2.94 | UNDEF(z>5) |
| D_191250 | 5.39 | S | 10.17 | 10.54 | 10.17 |  | -2.70 | -2.65 | UNDEF(z>5) |
| D_1002222 | 5.29 | S | 9.47 | 9.65 | 9.47 | V/s<1 | -0.96 | -0.89 | UNDEF(z>5) |
| D_214966 | 5.54 | S | 9.54 | 10.15 | 9.54 | V/s<1 | -2.66 | -2.66 | UNDEF(z>5) |
| D_1025527 | 5.30 | S | 9.39 | 10.34 | 9.39 |  | -1.94 | -2.05 | UNDEF(z>5) |
| D_1001674 | 5.18 | S | 9.92 | 10.74 | 9.92 | V/s<1 | -3.77 | -3.85 | UNDEF(z>5) |
| D_201125 | 5.82 | S | 9.96 | 10.54 | 9.96 | V/s<1 | -3.07 | -3.14 | UNDEF(z>5) |
| D_1094616 | 4.06 | S | 9.40 | 10.75 | 9.40 |  | -3.85 | -4.48 | UNDEF(range) |
| D_1000989 | 3.97 | S | 9.07 | 9.51 | 9.07 |  | -2.06 | -1.98 | -2.76 |
| D_1088814 | 4.41 | S | 10.60 | 10.35 | 10.60 |  | -0.10 | 0.01 | -3.35 |
| D_1087148 | 4.38 | S | 8.24 | 9.57 | 8.24 |  | -1.97 | -1.47 | -0.80 |
| D_1015956 | 4.02 | S | 9.54 | 8.82 | 9.54 | KNOWN | 0.61 | 0.92 | not needed |
| D_1085659 | 4.06 | S | 10.17 | 9.50 | 10.17 | KNOWN, V/s<1 | 0.59 | 0.75 | not needed |
| D_1083165 | 4.15 | S | 9.78 | 10.04 | 9.78 | V/s<1 | -2.07 | -2.02 | -1.58 |
| D_1065488 | 4.15 | S | 8.01 | 9.68 | 8.01 |  | -5.90 | -5.12 | -2.14 |
| D_1025101 | 4.91 | S | 8.99 | 10.54 | 8.99 |  | -5.13 | -5.42 | 0.77 |
| D_1090526 | 3.96 | S | 9.93 | 9.84 | 9.93 |  | -0.44 | -0.12 | -2.68 |
| D_1077545 | 4.42 | S | 9.27 | 9.61 | 9.27 |  | -1.34 | -1.26 | -1.76 |
| D_1089583 | 3.93 | S | 9.01 | 10.04 | 9.01 |  | -2.92 | -3.08 | -0.80 |
| D_1077261 | 3.92 | S | 9.36 | 9.75 | 9.36 | V/s<1 | -1.99 | -1.85 | -2.30 |
| D_1095186 | 4.02 | S | 9.37 | 10.05 | 9.37 |  | -2.55 | -2.27 | -2.49 |
| D_1091580 | 4.80 | S | 8.09 | 9.19 | 8.09 |  | -2.89 | -2.29 | -2.45 |
| D_1086992 | 4.04 | S | 9.37 | 9.58 | 9.37 |  | -0.84 | -0.12 | -4.18 |
| D_1090054 | 4.82 | S | 9.62 | 10.35 | 9.62 |  | -4.30 | -4.49 | -0.26 |
| D_1014130 | 4.38 | S | 8.49 | 9.53 | 8.49 |  | -2.21 | -1.63 | -1.71 |
| D_1082948 | 3.91 | S | 10.68 | 8.61 | 10.68 | KNOWN | 2.87 | 3.01 | not needed |
| D_1000110 | 4.06 | S | 9.52 | 10.55 | 9.52 |  | -5.47 | -5.95 | 0.01 |
| D_1091153 | 4.07 | S | 10.37 | 10.04 | 10.37 |  | 0.05 | 0.15 | not needed |
| D_1094903 | 3.87 | S | 10.34 | 10.55 | 10.34 | V/s<1 | -1.53 | -1.49 | -1.70 |
| D_1079264 | 4.05 | S | 8.73 | 8.98 | 8.73 |  | -0.96 | 0.03 | UNDEF(range) |
| D_1086406 | 4.41 | S | 9.46 | 9.23 | 9.46 |  | -0.14 | 0.05 | UNDEF(range) |
| D_1013488 | 3.80 | S | 9.57 | 10.24 | 9.57 |  | -2.39 | -2.53 | 0.16 |
| D_1028072 | 4.40 | S | 9.17 | 9.50 | 9.17 |  | -1.40 | -0.85 | -2.72 |
| D_1090742 | 4.62 | S | 9.37 | 9.35 | 9.37 |  | -0.60 | -0.28 | -3.00 |
| D_1091236 | 4.17 | S | 9.34 | 9.74 | 9.34 | V/s<1 | -1.27 | -1.27 | -1.79 |
| D_1009935 | 4.89 | S | 9.65 | 8.73 | 9.65 | KNOWN | 0.98 | 1.16 | not needed |
| D_1085494 | 4.06 | S | 8.90 | 9.59 | 8.90 |  | -3.34 | -3.19 | -3.30 |
| D_1090891 | 3.92 | S | 9.74 | 10.64 | 9.74 |  | -3.80 | -4.17 | 0.55 |
| D_1008197 | 4.40 | S | 8.76 | 9.51 | 8.76 |  | -2.20 | -1.79 | -1.88 |
| D_1029814 | 4.16 | S | 8.38 | 9.95 | 8.38 |  | -4.39 | -3.64 | -1.06 |
| C_02 | 5.29 | S | 10.30 | 10.32 | 10.30 | KNOWN, dust-det | -1.16 | -0.92 | UNDEF(z>5) |
| C_03 | 5.69 | S | 10.40 | 10.25 | 10.40 | KNOWN, dust-det | -0.40 | -0.32 | UNDEF(z>5) |
| C_06b | 4.56 | S | 9.19 | 10.25 | 9.19 |  | -4.27 | -4.58 | -1.45 |
| C_07a | 5.15 | S | 10.00 | 10.36 | 10.00 | dust-det | -2.16 | -1.91 | UNDEF(z>5) |
| C_08 | 4.43 | S | 9.85 | 10.59 | 9.85 |  | -3.39 | -3.17 | -2.33 |
| C_09 | 5.58 | S | 9.84 | 10.22 | 9.84 | known-seen, mapping-assumption, table-vs-figure-mismatch | -2.05 | -1.97 | UNDEF(z>5) |
| C_10a-E | 5.67 | S | n/a | 10.04 | nan |  | n/a | n/a | UNDEF(floor) |
| C_11 | 4.44 | S | 9.68 | 10.38 | 9.68 | dust-det | -3.18 | -3.41 | -0.47 |
| C_12 | 5.57 | S | 9.30 | 9.71 | 9.30 |  | -2.16 | -1.70 | UNDEF(z>5) |
| C_15 | 4.58 | S | 9.69 | 10.31 | 9.69 | known-seen, table-vs-figure-mismatch | -3.10 | -2.93 | -1.27 |
| C_19 | 5.23 | S | 9.51 | 10.37 | 9.51 | dust-det | -3.91 | -3.66 | UNDEF(z>5) |
| C_20 | 5.54 | S | 10.11 | 10.29 | 10.11 | dust-det | -1.64 | -1.21 | UNDEF(z>5) |
| C_23b | 4.56 | S | 10.46 | 9.90 | 10.46 | KNOWN, same-system-pair | 0.64 | 0.72 | not needed |
| C_23c | 4.57 | S | n/a | 9.36 | nan | same-system-pair | n/a | n/a | UNDEF(floor) |
| R_BRI1335-0417 | 4.41 | G | n/a | 10.42 | 10.52 | known-seen, tier-G(gas-only) | 0.25 | 0.46 | not needed |
| R_J081740 | 4.26 | G | n/a | 10.62 | 10.47 | tier-G(gas-only) | -0.52 | -0.41 | -2.22 |
| R_SGP38326-1 | 4.42 | G | n/a | 11.40 | 10.80 | same-system-pair, tier-G(gas-only) | -1.56 | -1.57 | 0.14 |
| R_SGP38326-2 | 4.43 | G | n/a | 10.82 | 10.40 | same-system-pair, tier-G(gas-only) | -1.09 | -1.08 | 0.06 |
| A_065.1 | 4.45 | S | 10.48 | 10.96 | 10.48 |  | -1.75 | -1.71 | -0.67 |
| A_071.1 | 3.71 | S | 12.31 | 11.38 | 12.31 | SED-AGN-suspect | 2.16 | 2.19 | not needed |
| P_28 | 3.63 | S | 11.11 | 11.27 | 11.12 |  | -1.27 | -1.24 | -1.14 |

Problems in the sample found and kept (phase 2 readings, none changes a frozen line):
- **CRISTAL ID mapping:** dynamics id 09 joins sample row 09a (frozen rule X, else X+'a'). Under it CRISTAL-09 HAS a finite SED M*, while the data note says it has none. Not resolved by hand; flagged `mapping-assumption`. 10a-E and 23c have no finite M* (L1, F1 and L2 UNDEFINED, counted in m).
- **Duplicate check (frozen rule |dz| <= 0.02, same field, one side without coordinates):** the rule finds FOUR possible pairs, not the one the frozen text quoted (that text used |dz| <= 0.01): CRISTAL-08 with Danhaive 1088814, 1077545 and 1086406, and Amvrosiadis ALESS 065.1 with CRISTAL-08 (the ALESS field, ECDFS, is from memory, unverified). All stay in the sample; m stays 62. No flag was affected.
- CRISTAL M* has no error column: stat error 0 (the 0.25 dex systematic stands in). Roman-Oliveira SGP38326-1/-2 have no gas error: 0.3 dex (as CFG197). Amvrosiadis V_circ(2 r_e) is used as tabulated, without an added sigma term. ALPAKA ID 28 uses the frozen f_enc = 0.5 at R_ext although a digitised optical R_e exists on disk (R_ext/R_e = 2.34 there): not used; it is a post-hoc variant only, not computed.

## Planted-galaxy controls and MUTATE (run BEFORE the real statistics; `CFG235_01_controls.out`)

The control sample is 62 generic synthetic background rows (a phase-2 choice; frozen text does not fix it) plus plants; it never touches a real value. Exit 1: **four frozen expectations FAILED, kept, not repaired**:

1. **C5b (T2 fires on a planted 5 sigma residual) and P1 "T2 fired": FAILED.** The frozen Westfall-Young permutation holds sigma_i fixed and permutes the residuals. With sigma set by shared systematics, the permuted maximum equals the observed one for almost any pairing, so the test has no power unless the row's sigma is among the smallest (C5c, informational: with the smallest sigma the adjusted p is 0.017; with the median sigma 0.52; on the planted P1 0.97). **The T2 tier therefore cannot confirm anything in this design: a frozen design flaw, found before any real statistic was read.**
2. **P3 (L2 fired at M200,need = 1e14) and the label "LambdaCDM only": FAILED.** With the frozen conservative L2 cells (c-M +1 sigma, -0.3 dex in M200, 10 V_ref, wide sigma) z_rob(L2) is -0.08 at that halo mass. The noise-free scan (C6, reported) reaches 3.06 only at M200,need = 3e14 with zero noise. So L2 cannot fire inside its frozen range with the frozen sigmas, and "breaks LambdaCDM only" is unreachable.
3. Everything else passes: C0 (counts), C1 (analytic vs MC L1 z, 0.006), C2 (P2 closed form exact; nu_mono identical to CFG5_common), C3 (lemma: gas only raises the floor, both kernels), C4 (HMF within 2e-4 of the on-disk Eisenstein-Hu + Sheth-Tormen; DM14 c-M within 2e-4 dex), C5a (T2 false-positive rate 1.5% on null), P1 L1 and F1 fire (z_rob 3.84 / 4.18), P2 (framework-only) fires on F1 only (6.77, L1 0), P4 and P5 silent, P6 (z_rob 3.05) T0 yes and T1 no (z_B 3.205), P7 tier S silent while the S+G cell reports z = 10.9, P8 lists the duplicate, P9 not testable, P10 (f_DM-inconsistent row) silent, P11 (fragile) silent, structural L1 => F1 holds, background silent.
Added in phase 2 (declared): P10 (for M5), P11 (for M6), P3b (for M7), C6, and the planted values of P5, P6, P11 found by bisection on the pipeline's own z.

**MUTATE M1-M8: all eight BITE** (exit 1; "bites" = a control that passed in the main run now fails). M1 swap floors: P2 labels break. M2 no systematics: P5, P6, P7, P11, P3b fail. M3 no trials correction: P6 "not confirmed" fails. M4 gas x3 in the primary floor: P7 fires. M5 D = 1/(1 - f_DM): P10 fires. M6 primary cell only: P11 fires; **the frozen P5 did NOT bite under M6** (P5 sits at z_primary = 1.5, so a primary-only rule still does not fire it; the fragile row P11 was added to test the rule; kept as a wrong frozen pairing). M7 actual footprint: P3b z_primary rises from 1.83 to 2.14. M8 m = 31: P6 passes Bonferroni. Because the main controls already exit 1, "bites" is scored as NEW failures relative to the main run.

## Labels (frozen section 9). Every galaxy that breaks EITHER theory at ANY tier

| galaxy | z | src | known? | criterion z_prim -> z_rob | after Bonferroni (z_B = 3.154) | after Westfall-Young | after parametric null (reported) | label T0 / T1 / T2 |
|---|---|---|---|---|---|---|---|---|
| Danhaive 1082948 | 3.91 | D | **KNOWN** (M_dyn < M*) | F1 3.31 -> 3.01 (L1 3.17 -> 2.87) | fail (-0.14) | p = 0.979 (fail) | p = 0.52 | framework only / neither / neither |

All other 61 rows: label "neither" at every tier. Known cases: Danhaive 1082948 (above), 1009935 (F1 z_rob 1.16), 1015956 (0.92), 1085659 (0.75); CRISTAL 02 (-0.92), 03 (-0.32), 23b (0.72) -- the last three are the "D_ind < 1" cases of the independent SED + gas route; under the one-sided stars-only floor they do not approach 3 sigma, and with the S+G cell (reported) the six dust detections have L1 z between -3.2 and -0.3. Known-seen rows: CRISTAL-09 (-1.97), -15 (-2.93), Roman-Oliveira BRI1335-0417 (0.46). Near misses (F1 z_rob): ALESS 071.1 2.19 (its SED is AGN-suspect), 1009935 1.16. Sample counts: L1 T0 0, F1 T0 1, L2 T0 0; T1 0; T2 0 for all three (chance expectation 0.084 each).

**Sensitivity of the one flagged row (reported, not label-bearing):** the z_rob value sits in the 'wide' sigma cell (M* 0.30, dynamical 0.25 dex); in the primary cell it is 3.31 (F1) and 3.17 (L1), in the 'narrow' cell higher. Dropping the sigma_0 pressure term from V_c (the no-pressure variant; the frozen k = 3.36 is the conservative choice) raises its primary-cell z to 6.8 (L1) / 7.0 (F1), and moves 1009935 from 1.1 to 4.6. Its M_dyn is +0.4 / -0.6 dex from the paper's model, and the Danhaive paper itself says the source shows no signs of rotation and lists possible causes in the SED and kinematic fits. The rival a0 x E(z) floor gives 3.70 (primary cell). None of this is a detection of anything about a0(z).

## Structural limits (stated in the frozen file; confirmed by the run)

- **Every L1 flag is also an F1 flag** (nu > 1): checked, true (vacuous here: no L1 T0 flag). "Breaks LambdaCDM only" cannot come from L1.
- **"Framework only" is essentially unreachable at high acceleration:** the separability index S_i = log10 nu(x_*) / sigma_tot has a maximum of 1.61 over the 60 defined rows (median about 0.3); no row reaches 3. The single "framework only" label at T0 is the straddle artefact described above (S_i = 0.05).
- **"LambdaCDM only" needs L2, which cannot fire** inside its frozen range with the frozen sigmas (failed control P3). L2 is UNDEFINED for 15 rows above z = 5 (c-M calibration), 3 rows by range, and 2 rows with no stellar floor: 20 of 62. The z-clamped L2 values for the z > 5 rows are a reported-only column and never enter a label.
- **T2 (permutation) cannot confirm anything** (failed controls C5b and P1). Only T1 (Bonferroni) is informative, and one row got within 0.14 sigma of T0 and none reached T1.

## Route-systematic dependence

- The floor is stars only (gas >= 0). For the six CRISTAL dust detections, adding the measured gas at the LOW end of the CFG234 bracket (x1/3) moves z by at most 0.4 toward a break (for example 19: L1 -3.31 -> -3.15; 02: -0.96 -> -0.72); the gas x1/3 to x3 bracket, the M* zero point (+/-0.2 dex; 0.29 dex in the CFG234 rival median) and the geometry (sphere / thin disc / compact) are route systematics of order 0.1 to 0.3 dex in log R_obs, which is the size of the sigma the flag must exceed. The four CRISTAL dust-limit discs (08, 12, 15, 23b) are never given a gas value.
- CRISTAL's V_c comes from one DysmalPy analysis and its R_e is a fit output with a [CII]-size prior; Danhaive's from one geko fit with k_tot = 1.8 divided out. Both are model outputs of one chain each; this lane reads those analyses, not raw kinematics. The repo holds no provenance note comparing the CRISTAL CSVs to the paper, and CRISTAL-09 and -15 disagree between table and figure (the table values are the frozen input).
- The pressure coefficient k = 3.36 is the authors' value (Danhaive and CRISTAL); CFG234 found the lower 1.68 to be mostly an artefact of how it was varied. A lower k lowers V_c and would make breaks easier; the frozen choice is the conservative one.

## Hand estimates (frozen section 16) scored against the outcome (`CFG235_03_report.out`)

H1 (L1 T0 flag, P 0.50) FALSE; H2 FALSE; H3 FALSE; H4 (F1 flags contain L1 flags) TRUE (vacuously); **H5 (any "framework only" at T0, P 0.04) TRUE: a wrong expectation, kept** (via the straddle); H6 FALSE; H7 (L2 undefined for >= 20 rows, P 0.97) TRUE (exactly 20); H8 (inconclusive or both survive) TRUE; H9 (1082948 is the known flagged case) TRUE; H10 (BRI1335-0417 flagged) FALSE; H11 (P5 and P6 pass first time) TRUE for those two, but four other frozen expectations failed.

## Things that went wrong, kept

- The first `02_main` run crashed after printing all tables, at the JSON write (a variable name was reused); fixed, re-run; the printed numbers are identical (`CFG235_02_main_firstrun.out` kept).
- The first controls run crashed while bracketing the P3b plant; P3b was redefined (M200,need = 3e14 at z = 4.5, fixed) and the noise-free L2 scan was added (C6).
- The MUTATE scripts read the planted values saved by the main controls run, so a mutation flips one cell on the same planted rows.
- The frozen P5 pairing with M6 does not bite (above). The frozen duplicate count (one pair) differs from the rule's count (four).

## What was NOT tested

The two-sided pooled tests (CFG197, CFG213/234) and any median-level claim; external-field and environment corrections for the framework; halo contraction, feedback cores, non-NFW shapes, assembly bias and the survey selection function for L2 (the survey volume is the generous COSMOS-scale V_ref; the actual Danhaive footprint of about 0.049 deg^2 would make L2 easier and is run only as MUTATE 7); any source outside the 62 (GN20, REBELS-25, SPT0418-47, J081740's GA-NIFS data, ALPINE rotators); raw kinematics; a z-dependent a0 (the rival is reported for three rows only); an alternative T2 (for example a sign-flip or parametric step-down): the parametric-null column is reported but was not frozen as a label tier, and no alternative was used to change any result.

## Files

`CFG235_FROZEN_CRITERIA.md` (copy of the committed file), `CFG235_common.py`, `CFG235_00_sample.py/.out/_results.json`, `CFG235_01_controls.py/.out/_results.json`, `CFG235_02_main.py/.out/_results.json` (+ `_firstrun.out`), `CFG235_03_report.py/.out`, `CFG235_MUTATE.py`, `CFG235_MUTATE_1..8.out/_results.json`, `CFG235_run_all.sh/.out`.

## In-place re-run (orchestrator)

`bash CFG235_run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`; about 12 minutes): `00_sample` exit 0; `01_controls` exit 1 (the four failed frozen expectations, kept; the gate passed with the documented `CFG235_GATE_OVERRIDE=1` banner); `02_main` and `03_report` exit 0; all eight MUTATE runs exit 1 (bite). Every `.out` and `_results.json` is identical to the author's apart from one timing line. `CFG235_02_main_firstrun.out` is the author's first main run (it crashed at the JSON write, a reused variable), kept as produced. The frozen criteria are `../CFG235_FROZEN_CRITERIA.md` (bfc86d36d), committed before any per-galaxy dynamical value was opened or computed with.
