# CFG600 FROZEN CRITERIA: KiDS catchment from the lensing profile itself (CFG594 audit rank 2, KiDS half)

Written 2026-10-10 before any CFG600 script exists or any CFG600 number is computed. Inputs read so far are committed results only (CFG529 / CFG531 READMEs, JSON and scripts; CFG594 audit).

Standing settings: a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are scored separately and NEVER pooled. nu_mono. Candidate B. The cold energy's mass is still required. No knob is fitted beyond the one declared calibration below. Not "theory closed". Compute: nice 10, 1 thread per process, at most 4 processes, no PM runs, nothing downloaded. Verdicts use RAW data (KiDS f30 ESD) against framework-native predictions only; ΛCDM is not a yardstick.

## 1. Question
CFG529/531 set each lens's settled-supply edge from the census f_ret, which is measured relative to LCDM halo masses (audit L06/L07). What if each system's catchment (edge x = r_edge / r_ta,law, with r_ta,law from the law and the baryons, no SHMR) is taken from the lensing profile BEYOND the edge instead? How far do the inner-bin shortfall and the early-type split move?

## 2. Machinery (read-only)
CFG531's cfg531_kids.py executed up to its line `EARLY = TYP == 1` (which loads CFG529's data, f30-matched environment, constructions A and B, cached law tables). Node own profiles come from CFG529's node tables (x = 0.20 ... 1.00, 17 nodes): own_x = (1 - fo) full_x + fo tr_x (W30), stacked with the f30 weights; model = E + own_x with CFG529's covariance C/hart(n) + delta delta^T (delta = behroozi - moster). Both constructions A, B, both footings.

## 3. The calibration (one declared rule, no other freedom)
- **x\* = the node x that minimises chi2 over the six OUTER bins (bins 0-5, R > about 445 kpc) with eps = 0**, per class, construction and footing. The outer bins are beyond the census edge for every f30 group, so they set the catchment; the inner nine (K9: bins 6-14) are held out of the calibration.
- The scored quantity is eps (CFG531's GLS amplitude, Delta M / M_pred) in K-in (bins 12-14), K-mid (9-11) and K9 at x\*, with the E and own mixing unchanged.
- Reference rows: CENSUS edge (CFG531 base) and LAW_RTA (law to r_ta).

## 4. Labels (per footing; both constructions must agree, else MIXED)
Let d = eps_K9(x\*) - eps_K9(census) and s = sigma of eps_K9(census).
- **CLOSED:** Z_K9(x\*) < 2.
- **REDUCED:** not closed and d <= -1 s.
- **UNCHANGED:** |d| < 1 s.
- **WORSE:** d >= +1 s.
Early-type split: repeat for early (typ 1) and late (typ 0) f30 lenses, x\* calibrated per class, and report CFG531's early-minus-late difference (jackknife-or-quadrature, CFG531's rule) for K9 at census and at x\*. Label the split MOVED if the difference changes by >= 1 of its sigma, else UNCHANGED.
Also reported (no verdict weight): x\* itself, chi2 outer and inner at x\*, the node chi2 curve.

## 5. Controls and MUTATE (must flip)
- K1: the CENSUS own path reproduces CFG531's committed BASE eps (K-in, K9, 1e-6) for A/B, both footings.
- K2: node x = 1.00 own profile equals LAW_RTA (reported if not an identity; the identity or its measured difference is stated).
- K3: calibration on a noiseless mock (data := model at x = 0.50 node) recovers x\* = 0.50 and eps = 0.
- **MU1 (circular calibration):** calibrate x on the inner nine bins themselves. The label must change to CLOSED-by-construction on at least one footing, which shows why the held-out outer-bin rule is needed; if it does not, the estimator is void.
- **MU2 (broken edge):** x fixed at 0.20 (edge pushed to the inner radius) must be rejected: chi2_outer >= 2 x the x\* value on both footings, else void.

## 6. Scope
KiDS only. The group half of audit rank 2 (CFG543 P2) is NOT in this lane: the on-disk group data are Tian+2026 sigma_los and Re only, so a dynamical catchment mass from sigma would be circular with the BFJR statistic, and no independent zero-velocity or lensing mass is on disk. A download needs the owner's yes.
