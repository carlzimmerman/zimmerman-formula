# LAM2_gas_poor_lambda_estimator: NO KINEMATIC AXIS BEYOND PHOTOMETRY. In 2352 gas-poor galaxies the SDSS fibre's line shape adds AUC +0.014 over photometry (95 % +0.005 to +0.024), real but under the frozen 0.05. h4 does track spin (Spearman -0.35), but photometry already carries most of what it knows

Criteria `FROZEN_CRITERIA.md` (fa14da563a), amendment A1 in `AMENDMENTS.md`, written before any count. Files: `lam2_fetch.py` (query), `lam2_stage0.py`, `.out`, `.json`. Not a gravity test. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

| gate | gas-poor (graded) | gas-bearing (row) |
|---|---|---|
| N after quality cut | 2546 | 778 |
| slow / fast | 428 / 2118 (0.168) | 23 / 755 (0.030) |
| F1 (>= 1000, >= 100 slow) | PASS | FAIL |
| F2 sigma(AUC) at 0.75, need <= 0.0167 | 0.0143, PASS | 0.0596, FAIL |

Counts: 5811 matched rows give 5732 galaxies after one row per mangaid. 49 have no galSpecLine row. The quality cut passes 3365. Gas-poor EW bins: [<1 A) 1633 with 340 slow, [1, 2) 678 with 68, [2, 3) 235 with 20.

## Reading
- The gas-poor sample is where the question can be asked at all. Almost every slow rotator in the cut is gas-poor, which is why the paper's H-alpha input cannot reach them.
- F2 passes with little margin (0.0143 against 0.0167). E3's 0.05 gain is about 3.5 sigma of one model's AUC, and E4's 0.03 is about 2 sigma.
- The gas-bearing comparison will be weak: 23 slow rotators. Its rows are reported, not graded, as frozen, and should be read as indicative.
- The first run crashed on parsing specobjid, which overflows int64; the fix only reads the ids as text. No count had printed.

## Stage 1-2 result (`lam2_grade.out`, `lam2_grade.json`; M1 in `lam2_grade_MUTATE.*`; K2 in `lam2_k2.*`)

| check | result | frozen bar |
|---|---|---|
| K1 sigma_pPXF vs velDisp, gas-poor n 2539 | median +0.009 dex, rms 0.022 | PASS |
| K2 h4 recovery, 599 synthetics | rms 0.0274 (S/N thirds 0.031 / 0.029 / 0.022); slope 0.80 | PASS |
| M1 MUTATE, h4/h6/sigma ratio shuffled in 27 cells | AUC(S_mut) - AUC(B) -0.005 | PASS |
| E1 rms(S) on lambda_Re | 0.178 | FAIL (<= 0.10) |
| E2 purity of predicted slow, S | 0.586 (29 predicted slow) | FAIL (>= 0.70) |
| **E3 AUC(S) - AUC(B)** | **+0.0141 [+0.0051, +0.0235]** | **FAIL (>= 0.05)** |
| E4 AUC(SP) - AUC(P) | +0.0259 [+0.0170, +0.0357] | FAIL (>= 0.03) |

AUCs, gas-poor (N 2352, 396 slow, out of fold): B 0.791, P 0.788, S 0.805, SP 0.814. 187 galaxies were dropped for missing MPA-JHU indices; 10 spectra failed the fit (empty in the fit window).

**Label: NO KINEMATIC AXIS BEYOND PHOTOMETRY.** A shuffled-label code test (DRYRUN, outputs not kept) gave E3 +0.0005 and E4 +0.006, so the code returns zero when there is nothing to find.

## Reading
- **The signal is real and small.** Both gains have 95 % intervals clear of zero, and the shuffle control kills them. h4 correlates with lambda_Re (Spearman -0.35 over all, -0.28 within fast, -0.18 within slow). Slow rotators have more peaked profiles (median h4 +0.031 +- 0.002) than fast ones (+0.014 +- 0.001), the sign expected when rotation flattens the integrated profile. But Sersic n, ellipticity, mass and velDisp already rank slow above fast at AUC 0.79, and the line shape adds 0.014 on top. Stellar populations add nothing over photometry (-0.003).
- **What this means for a lens split:** a fibre-spectrum "spin" label for gas-poor lenses would mostly re-split structure and mass, which CFG849/CFG850 already did. That route is closed at the frozen bar.
- **Reported rows, not graded, and not a result:** the gain sits in the most massive third (log M* > 11.17: +0.061) and the highest-velDisp third (+0.064), where most slow rotators are (262 and 278 of 396). Elsewhere it is +0.000 to +0.031. This was not a graded cell and was looked at after the grade. Taking it further needs its own frozen lane and a sample not used here.
- **Gas-bearing rows (23 slow, weak):** S beats photometry plus sigma_balmer (the closest catalogue match to the paper's H-alpha width) by +0.042, and sigma_balmer itself adds -0.021. Indicative only.
- **Why E1 is far off:** the paper's rms 0.08 used whole-galaxy integrated H-alpha. A 3 arcsec fibre covers 0.06-1.2 R_e here (median 0.28), where rotation is still rising. Transfer to larger apertures is not tested: the gain is flat across fibre radius over R_e (+0.017, +0.011, +0.011).
- ATLAS3D external test: NOT RUN (CDS and VizieR timed out).
