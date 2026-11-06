# QX21 frozen criteria: is QX20's hot/cold step physics or a method artefact?

Frozen before any QX21 script or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules:
SWARM_BRIEF.md.

## Question

QX20 (41d601b6ce) puts X-ray-hot systems (ellipticals, groups, X-COP) +0.32 to +0.37 dex above SPARC's cold discs, at the
same M_b, g_N, depth, r/r_M and f_gas (+0.351 / +0.345 in g_N). Its hot masses are X-ray hydrostatic; SPARC's come from
rotation curves. Is the step tied to galaxy type (real), or to the mass method (artefact)?

## Disclosure before freezing

The record has already looked at the KiDS early/late split. CFG61 found early-type lenses above the law at chi2 51.9/7,
late-type lenses near it at 12.6/7, and an early-minus-late difference at chi2 28.1/7. I have read CFG61's printed
per-bin stacks. QX21's statistic D (T1) is new: a log-amplitude of the split, compared with QX20's step. It is not
blind to CFG61's chi2.

## T1: weak lensing, no hydrostatic mass (the decisive test)

- **Data:** Brouwer+2021 Fig. 8 released ESD profiles,
  real_research/data/lensing_rar/brouwer2021_rar/Fig-8_RAR-KiDS-isolated_Colorbin_{1,2}.txt.
  - Bin 1 is u-r < 2.5 (late); bin 2 is u-r >= 2.5 (early).
  - Full 30x30 covariance from Fig-8_..._Colorbins_covmatrix.txt.
  - ESD and covariance are bias-corrected as the README says.
- **Bins:** CFG61's committed 1-halo set K1, the 7 g_bar bins with index 8-14 (1.30e-13 to 3.92e-12 m/s^2). The lens
  distribution fixed this set (median R < 0.3 Mpc for both classes), not the data values.
- **Statistic:** d_i = log10(ESD_early,i / ESD_late,i) on K1.
  - Linearised covariance C_d = (J C J^T) / ln(10)^2, with J the Jacobian of (ln E_i - ln L_i).
  - D = the GLS mean of d with C_d, and sigma_stat its GLS error.
- **The law predicts D_law ~ 0.** C4 of CFG61 shows the law's ESD at fixed g_bar is mass-independent to 4e-6. D_law is
  computed as the same log ratio of CFG61's printed lens-by-lens law columns (L) on K1, canonical, and reported.
- **Systematic:** the early class's M_* calibration is +-0.1 dex (CFG61's own term). In the deep regime that is +-0.05 on
  D: sigma_sys = 0.05 dex. sigma_tot = sqrt(sigma_stat^2 + sigma_sys^2).
- **Lines:**
  - STEP SEEN (lensing): D - D_law > 0 and (D - D_law) / sigma_tot >= 3.
  - NO STEP (lensing): |D - D_law| / sigma_tot < 2.
  - Otherwise: weak.
- **Size versus QX20's g_N step S = 0.35 dex:**
  - "same size": |(D - D_law) - S| <= 2 sigma_tot;
  - "smaller": D - D_law < S - 2 sigma_tot;
  - "larger": the reverse.
- **Footing:** D is empirical and footing-free. The law's D_law is ~0 on both footings (C4). Both footings are reported.

## T2: pressure-supported COLD systems (no X-ray mass)

- **Data:** LW1's per-system plain-law offsets, log g_obs/g_law with no EFE (rebuild_2026_10_22/LW1_law_scorecard/
  lw1_dwarfs.json, per_system[*].plain), both footings. Velocity-dispersion masses, no X-ray.
- **Classes:** MW classical dSphs and bright M31 dSphs are the test classes. MW ultra-faints and M31 others are reported
  only: they carry known tides and equilibrium questions (Z2), and the plain law already fails them for other reasons.
- **Statistic:** each class median, with a bootstrap 95% interval over systems (10,000 resamples, seed 21).
- **Line:**
  - "cold pressure-supported step present": the median exceeds SPARC's mean (QX20: +0.027 canonical, -0.001 alt) by
    >= 0.15 dex, and the interval's lower end exceeds SPARC's mean.
  - "absent": the interval contains SPARC's mean.
- **Meaning:** if present, the step tracks pressure support, not X-ray heat. That still says nothing about the method,
  since the masses are dynamical.

## T3: hot-system masses by a second method (READ, not recomputed)

- **Sources:** LF1 (22272b3b32) and RF3.
  - LF1: KiDS shear on eRASS1 clusters gives about 0.12 dex MORE mass at fixed gas than X-COP's hydrostatic share.
  - RF3: A2142, the one X-COP cluster with a lensing mass in the record, agrees with its hydrostatic mass.
- **Graded statement:** the sign of any hydrostatic bias that the record measures.
  - If lensing >= hydrostatic, correcting the bias RAISES the hot offsets. The step cannot be a hydrostatic-mass artefact
    of the usual sign: METHOD-SIGN EXCLUDED.
  - If lensing < hydrostatic: METHOD POSSIBLE.

## Overall label (scoped)

- **STEP REAL (type-keyed):** T1 is STEP SEEN, and T3 is METHOD-SIGN EXCLUDED. T2 says whether the key is pressure
  support or X-ray heat.
- **STEP METHOD:** T1 is NO STEP, and T3 is METHOD POSSIBLE.
- **NO VERDICT:** anything else.
- **Scope:** KiDS gives an early/late (colour) split of isolated lenses at log M_* <= 11. The X-ray classes are larger
  and hotter. The same SIGN and a comparable size is what is tested, not identity. The baryonic escape stays open in
  every case: CGM hot gas in early types (CFG61 R4 says the law fits the split if early types carry 1-1.5x M_gal in
  extra baryons, untested).

## Controls (separate outputs)

- **M1 (type shuffle, T1):** all 2^7 = 128 per-bin early/late swaps. The observed D must exceed the 95th percentile of
  the swap distribution. If it does not, T1 has no power to call a type step and the label is NO VERDICT. The same
  shuffle at the dSph level: classes randomly relabelled against SPARC's anchor, reported.
- **M2 (Newton, T2):** with g_law -> g_N, every dSph class offset moves by > 0.3 dex. It must move, or the T2 pipeline is
  not reading the law.
- **KA1:** reproduce CFG61's C1 early-vs-late chi2 119.9/15 (u-r, all 15 bins) to +-0.5 from the released files.
- **KA2:** reproduce LW1's MW-classical plain median +0.2445 canonical to 1e-4.

Compute: one thread, seconds.
