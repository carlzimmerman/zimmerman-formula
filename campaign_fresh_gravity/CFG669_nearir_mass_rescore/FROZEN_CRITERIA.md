# CFG669 FROZEN CRITERIA: the KiDS age signal and early-type excess on near-IR (Ks) stellar masses

Date: 2026-10-12. Written and committed ALONE, before any CFG669 code or score. Block CFG660–669 (last number). Nothing below may be
edited after this commit.

Raw lensing only (owner's 10-10 rule); no ΛCDM ingredient; CFG529/531's ε not used. The only framework statement is
morphology-blindness (the law reads baryons only). Not "theory closed". Nothing will be phrased as "the data favour the framework".

## 0. What has been seen (stated before any choice below)

- CFG667: early-type OLD vs YOUNG raw K9 amplitude +0.166 (LePhare M*) → +0.032 ± 0.080 at fixed Taylor+11 mass.
- CFG668: early vs late at matched baryonic mass: LePhare +0.308 (Z 3.4; +0.249, Z 2.4 with 40-bin matching), Taylor +0.185 / +0.181
  (Z 1.7); the frozen decile matching failed its 0.02-dex control. CFG668 named a non-optical-colour mass estimator as the decider.
- LePhare's MAG_ABS_Ks: finite for every bright-sample galaxy, from the measured Ks band (MABS_FILTKs = 9); median −21.91; the
  implied median log M/L_K against LePhare masses is −0.675 with an assumed M_sun,Ks = 5.08 (likely a Vega/AB zero-point issue). No
  lensing score with Ks masses has been computed.
- **Author's expectation, before any score:** Ks masses sit between LePhare and Taylor; both signals likely shrink. A constant M/L_K
  ignores the mild age dependence of near-IR M/L (older → higher M/L_K), which biases toward keeping an age signal.

## 1. Estimator K

log M*_K = 0.4 (5.08 − MAG_ABS_Ks) + c, with one global constant c fixed so that the median of log M*_K over the f30 lenses equals the
median of LePhare log M* over the same lenses. c does not change any ranking or matching; it sets only the absolute scale used by the
gas term. Baryonic mass M_b,K = M*_K (1 + f_cold,type(log M*_K)), with CFG668's per-type f_cold relation (0.1-dex bins of the table's
f_cold against log M*, linear interpolation, clamped).

## 2. Tests (CFG585's head and CFG531's `esd_loo`, executed unedited; K9 = bins 6–14, inner = 9–14; patch jackknife)

- **T1 (age signal, early types):** CFG589-style tertiles of the u−r residual within 10 deciles of log M*_K (early f30 types). K9
  amplitude A_K.
  - **M\* BIAS EXPLAINS** if A_K ≤ 0.05 and |Z| < 1; **SIGNAL PERSISTS** if A_K ≥ 0.12 and Z ≥ 2; **PARTIAL** otherwise.
- **T2 (early-type excess):** early vs late f30 types matched in log M_b,K with **40 bins** (deciles of 40 of the early types' M_b,K),
  bins with fewer than 100 lenses of either type dropped; late types re-weighted per bin to the early counts (WG and WW scaled). K9
  amplitude A_K. Matching control: the mean over used bins of (median log M_b early − late) within ±0.01 dex (max reported).
  - **EXCESS NOT SIGNIFICANT** if A_K < 2σ; **EXCESS PERSISTS** if A_K ≥ 0.15 with Z ≥ 3; **INTERMEDIATE** otherwise. If the matching
    control fails, the T2 class is reported as **NOT CLEAN**.
- Reported: the same T1/T2 numbers for LePhare and Taylor recomputed in this script (consistency with CFG667/CFG668), and the median
  log M*_K − log M*_L for OLD − YOUNG and early − late.

## 3. Combined statement

Three estimators (LePhare SED fit, Taylor optical colour–M/L, Ks light) side by side. The record's tensions are called
**ESTIMATOR-ROBUST** only if both T1 and T2 keep Z ≥ 2 on all three; **NOT ROBUST** if either falls below 2σ on Ks.

## 4. MUTATE (`CFG669_MUTATE=1 CFG669_M=M1|M2`, each exits 1 iff its tooth bites)

- M1 (null): early/late labels shuffled within each M_b,K bin (T2) → |A_K| < 2σ.
- M2 (linearity): OLD weights × 0.8 in T1 → A_K shifts by log10(0.8) within 0.002.

## 5. Machine rules

Light: one process, `nice -n 10`; precomputed per-lens stacks; allowed while the 1024³ run is live.
