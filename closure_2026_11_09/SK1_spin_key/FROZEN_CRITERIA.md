# SK1 (spin key): FROZEN CRITERIA, committed alone before any script or number

TEST lane, quarantined. Owner decision `closure_2026_11_09/OWNER_DECISION_2026-11-09_SK1_TR1_LAUNCH.md` ("Launch both").
kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. Footings graded separately, never pooled.
No download: every input below is already on disk.

## Question

At fixed baryonic (stellar) mass and fixed Newtonian acceleration, does the a0 law's residual rise as the measured spin
parameter lambda_Re falls? Rotation is the one selector class the closure register still lists with no verdict
(VS4 NO VERDICT; LAM2, LAM3, LAM4 could not build or apply a spin estimator).

## Kill stated in advance

The hot-system amplitude spans two orders of magnitude across classes (dSphs about +0.2 dex, groups and clusters +0.19 to
+0.45, Coma UDGs +1.1 to +1.4 dex). A spin switch cannot carry that amount alone. **A detected spin trend is graded as a
SELECTOR HIT, not a completion**, and needs a second variable for the amount. **A FAIL closes the selector catalog.**

## What the record already says (not blind; read before freezing)

- **KU1 / KU2** (`rebuild_2026_10_22/KU1_*`, `KU2_*`) used this same DynPop file. KU2 matched slow and fast rotators in
  cells of M* and **Sigma_Re** and found D = +0.023 +- 0.023 ln (canonical, hosted footing 9.3603e-11), about +0.01 dex:
  UNIVERSAL. NC3 (`closure_2026_11_07/NC3_*`) found cluster members vs field early types +0.011 dex at fixed M* x sigma.
- **Why SK1 is not a rerun of KU2.** At fixed M* and fixed size, g_dyn scales as Sigma_Re^2 / R up to the virial
  coefficient. Matching on Sigma_Re therefore fixes most of g_dyn and pulls any class difference in the residual toward
  zero by construction. The owner's question fixes the **baryonic** side (M*, g_N), so SK1 matches on g_N, not on
  Sigma_Re. KU2's statistic is replayed as a known answer and reused as control (b).
- **ST1 / QX26 IMF handling** (the record's IMF control): Posacki+2015, log alpha = 0.38 log(sigma_e / 200) - 0.06 vs a
  Salpeter population; Salpeter / Kroupa-Chabrier mass ratio 1 / 0.63; IMF mass factor vs Chabrier
  f_K(sigma_e) = max(alpha(sigma_e) / 0.63, 1), floored at 1. ST1 printed the X-ray elliptical offset +0.210 -> +0.093
  (canonical) and +0.189 -> +0.074 (alt), at the hosted footings 9.3603e-11 / 1.1312e-10.
- LAM6-LAM8 (orbit shape, h4) and LAM9-LAM10 (spectroscopic IMF) gave NO VERDICT / NOT MEASURABLE; nothing here uses them.

## Inputs (on disk, untracked, never committed; read with `python3 -I`, path as an argument)

1. `_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits` (MaNGA DynPop, Zhu et al. 2023; 10,296 rows).
   HDU 1: Lambda_Re, Eps_MGE, Sigma_Re, Re_arcsec_MGE, DA, z, nsa_sersic_mass, nsa_elpetro_mass, nsa_elpetro_absmag,
   obj_ra, obj_dec, Qual. HDUs 2-11: ten JAM models, each with log_Mt_rhalf (total mass inside the sphere of the 3D
   half-light radius), rhalf_arcsec, chi2_dof.
2. `real_research/data/atlas3d_fj_table.tsv` (ATLAS3D XV/XX: logsig_e, logML_JAM, logr12, logL, logML_Salp, Dist, qual)
   joined by name to `_external_data/atlas3d_emsellem11/tableb1.tsv` (Emsellem+2011, ATLAS3D III: lamRe, epse, F/S).
   The FJ table has no lambda_Re; the ATLAS3D III table on disk does. ATLAS3D is a **replication row, not graded**.
3. `campaign_fresh_gravity/_external_data/cfg393/t15_table5.tsv` (Tully 2015 2MASS groups), NC3's matching
   (10 arcsec, |cz - HV| < 300 km/s), for the environment control.
4. `real_research/data/humphrey2006_ellipticals.tsv` (ST1 / QX26's X-ray elliptical input) for the IMF known answer.

## Sample (DynPop)

Qual >= 1; finite Lambda_Re, Eps_MGE; Sigma_Re > 0; DA > 0; z > 0.005; nsa_sersic_mass and nsa_elpetro_mass finite and
> 0; log_Mt_rhalf and rhalf_arcsec finite in at least 8 of the 10 models (KU1's cut).
**Slow rotator** (Cappellari 2016): Lambda_Re < 0.08 + Eps_MGE / 4 and Eps_MGE < 0.4. **Fast**: all others.

## Conventions (fixed)

- **JAM model**: per galaxy, the model with the lowest chi2_dof (KU2's resolution of KU1's model spread). The second-best
  model is a robustness row; each of the ten models one at a time is a disclosed row.
- **Aperture**: the 3D half-light sphere of the chosen model, r_h = rhalf_arcsec x DA (DynPop's own D_A, H0 = 67.8, the
  distance its JAM masses are scaled to).
- **g_dyn** = G M_t(< r_h) / r_h^2 (sphere-enclosed JAM total mass; no further deprojection).
- **Stellar mass**: nsa_sersic_mass (primary), stored as log10 in h = 1 units (NSA convention), converted to DynPop's
  H0 = 67.8: log M* = stored + 2 log10(100 / 67.8) = stored + 0.3375. Chabrier IMF as stored. Gas ignored (stated below).
  M*(< r_h) = 0.5 M* (r_h encloses half the light; constant M/L inside the galaxy).
- **IMF control (primary residual)**: M*_IMF = M* x f_K(Sigma_Re), f_K as in QX26 / ST1 above. Sigma_Re is already the
  dispersion inside R_e, so QX26's sigma_0 -> sigma_e aperture factor 0.87 is not applied.
  Disclosed IMF brackets, not knobs: Chabrier as stored (f = 1) and Salpeter everywhere (f = 1 / 0.63).
- **g_N** = G (0.5 M*_IMF) / r_h^2.  **g_law** = g_N / 2 + sqrt(g_N^2 / 4 + a0 g_N) (the law g_N = g^2 / (g + a0)).
- **Residual** rho = log10(g_dyn / g_law), in dex.
- **Footings**: a0 = 1.2e-10 m s^-2 (canonical) and 1.1e-10 (alt), graded separately. Known-answer replays use the
  record's own hosted values (9.3603e-11 / 1.1312e-10) where the replayed lane used them.

## Primary statistic (matched, not regressed)

Cells: 0.2 dex in log M*_IMF x 0.1 dex in log g_N (at fixed M* and g_N the radius is fixed too). In each cell with at
least 2 slow and 2 fast: D_cell = median rho(slow) - median rho(fast), weight min(n_slow, n_fast).
**D = weighted mean over cells** (the QX22 / KU / NC3 cell statistic, in dex). Bootstrap: 2000 resamples over galaxies,
seed 20261109, cells rebuilt each time; 95 % percentile interval.

**Per-bin SHAPE across lambda_Re.** Bins (all galaxies, slow and fast): [0, 0.1), [0.1, 0.2), [0.2, 0.3), [0.3, 0.45),
[0.45, 0.6), [0.6, 1]. For each bin b: D_b = the same matched statistic with bin b against the fast rotators not in
bin b (cells as above), with its bootstrap interval. Shape statistic S = Spearman correlation of D_b with the bin centre.
A spin key predicts S <= -0.6 with D rising toward the low-lambda bins.

Beside, not graded: OLS slope of rho on Lambda_Re with log M*_IMF and log g_N as covariates.

## Labels, per footing

- **NO POWER** if the 95 % half-width of D exceeds 0.10 dex, or MUTATE (2) fails to recover its plant. No other label.
- **FAIL** if D < +0.10 dex or D < 0 (wrong sign).
- **PASS = SELECTOR HIT** only if all hold: D >= +0.20 dex; the 95 % interval excludes 0; SHAPE holds (S <= -0.6 and the
  two lowest-lambda bins both have D_b >= +0.10); the second-best JAM model gives D >= +0.20; and controls (a)-(d) hold.
- **UNDECIDED** otherwise (D between +0.10 and +0.20, or D >= +0.20 with a failed shape, robustness or control
  condition, which is named).
- A SELECTOR HIT is not a completion (kill above). The combined reading needs both footings.

## Controls

- **(a) environment** (so a spin trend is not a host trend). T15 match. D recomputed on (a1) T15 field singletons
  (Nmb = 1) and (a2) T15 satellites (Nmb >= 2, not the group's brightest). Holds if D >= +0.10 on each subset that is
  evaluable (at least 10 slow in at least 3 matched cells). If neither subset is evaluable the control is NOT
  EVALUABLE and a PASS becomes UNDECIDED. Reported: T15 group centrals (Nmb >= 2).
- **(b) Sigma_Re alone** (the dispersion key HX1 graded NO LADDER). KU2's statistic on SK1's footings and residual:
  slow minus fast at matched (M*_IMF, Sigma_Re) cells (0.2 dex x 0.1 dex). Holds if it is >= +0.10 dex, i.e. the spin
  split is not carried by dispersion alone. If it is below, the spin trend at fixed g_N is a dispersion difference and
  adds nothing to the key HX1 already graded.
- **(c) seeing and inclination**: D recomputed on (c1) Re_arcsec_MGE >= 4 arcsec (sigma_PSF / R_e <= 0.27 for MaNGA's
  2.5 arcsec FWHM; seeing lowers lambda_Re in small galaxies) and (c2) Eps_MGE < 0.4 for both classes (the slow line's
  own range). Holds if D >= +0.10 on both.
- **(d) gas and morphology**: D recomputed on the red sequence only (NSA elpetro u - r >= 2.5, NC3 / QX22's line), where
  gas inside r_h is negligible. Holds if D >= +0.10. Sign of the gas omission stated: gas would raise fast rotators' g_N,
  lower their residual and raise D, so ignoring it biases D low; a FAIL within 0.03 dex of the +0.10 line is flagged.

## Known answers (exit 0 only if all pass)

- **KA1** ST1 / QX26 X-ray elliptical IMF offset replayed from humphrey2006 with SK1's own f_K: D_imf +0.0930 (canonical
  hosted) and +0.0743 (alt hosted), |difference| <= 1e-4.
- **KA2** KU2 replayed with KU2's conventions (hosted footings, elpetro as stored, H0 70 D_A from z, matched M* x Sigma_Re,
  ln): D +0.023332 / +0.025383, |difference| <= 1e-5; n 6056, 536 slow, 27 cells.
- **KA3** published slow fraction: ATLAS3D III F/S column gives 36 slow of 260 (14 %, Emsellem+2011); SK1's join must
  reproduce the count exactly. DynPop's own paper is not on disk; the DynPop count is checked against the record instead
  (KU1/KU2: 536 slow, 5520 fast at their cuts).
- **KA4** the residual function returns 0 to 1e-12 when g_dyn is replaced by the law's own prediction.

## MUTATE (`sk1.py --mutate` -> sk1_MUTATE.out / .json, exit 1)

1. Shuffle Lambda_Re within 0.2 dex M*_IMF bins (seed fixed), reclassify: |D| < 0.05 and the interval contains 0, both
   footings.
2. Plant +0.2 dex on every slow rotator's g_dyn: D rises by 0.20 +- 0.03 and the interval excludes 0, both footings.
3. Swap the stellar-mass column (elpetro for sersic): the label on each footing must not flip.

The lane's power claim rests on (2); if (2) fails the label is NO POWER.

## Hand estimates (HE), before any number

- **HE-a** if the spin key is real at the size the hot rows need: slow minus fast +0.20 to +0.30 dex.
- **HE-b** if ST1's IMF reading is the whole story: about 0 (0 to +0.05) after the IMF control. Estimate: at fixed M*
  and r_h, slow rotators run about 0.15-0.2 dex higher in Sigma_Re^2, so about +0.05 to +0.10 dex before the IMF control;
  the Posacki factor adds about 0.06 dex of stellar mass to them, which removes about 0.04-0.05 dex of residual.
- **HE-c** control (b) at matched Sigma_Re near KU2's +0.01 dex.
- **HE-d** label expected: FAIL on both footings (D below +0.10).

## Limits stated in advance

Sphere-enclosed JAM mass is model output, not raw data. NSA kcorrect masses carry their own systematics; the h-unit
conversion is a constant and cancels in D to first order. r_h accelerations sit near a0 (y about 0.5-1), not deep, so
the law's boost is modest. T15 covers only the 2MASS-bright part of the sample. A pass or fail here grades rotation as a
key at r_h in early and late types at z about 0.03; it says nothing about the amount the hot rows need.

## Compute and hygiene

One thread, seconds, RSS well under 1 GB; SIGTERM exits cleanly (the run is short and rerunnable; outputs are written only
at the end). No knob scans: every number above is fixed here. Files: `sk1.py`, `sk1.out/.json`, `sk1_MUTATE.out/.json`,
`RESULT.md`. Filing and registering are the orchestrator's acts.
