# CFG663 FROZEN CRITERIA: does the response sector have to lens? (dynamics vs lensing at the same baryonic acceleration)

Date: 2026-10-12. Written and committed ALONE, before any CFG663 code or score. Block CFG660–669. Nothing below may be edited
after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. Footings (9.3603e-11 canonical, 1.1312e-10 alt) judged separately, never pooled. The cold energy's mass is
required. No particle species. Not "theory closed". Nothing will be phrased as "the data favour the framework". Raw data only:
the published KiDS-1000 lensing RAR (Brouwer et al. 2021 release, on disk) and SPARC rotmod (the record's CFG4 harness). No ΛCDM
halo, no MOND fit, no stacked-halo model enters any prediction.

## 0. What has been seen (stated before any choice below)

- MECHANISM_JOINT_2026-10-12.md: in the two-sector picture (collisionless cold matter + a response field that makes the law),
  a conformally coupled scalar response would not lens (the lensing ⇄ stability fork).
- `prep_2026/mi_lensing_final/` (record, read only): a non-lensing force with NO cold matter is excluded by KiDS
  (g_lens ≤ g_bar vs data g_obs/g_bar ≫ 1). Its ESD → g_obs conversion is reused here (B21 eq. 7: g_obs = 4G·ESD/bias).
- Ranges only (no scores): the B21 isolated RAR files (all, and the two u−r colour bins) have 15 bins with g_bar centres from
  1.38e-15 to 3.92e-12 m/s². SPARC good points (Υ = 0.61) with g_bar in [3e-13, 3.92e-12]: 179 points in 47 galaxies; in
  [1e-13, 1e-12]: 9 points.
- **Author's expectation, written before any score:** B21's lensing RAR is known to lie near the law at these accelerations, so
  the non-lensing hypothesis should predict SPARC dynamics well above the law (EXCLUDED). The test is run to measure by how much,
  with the KiDS errors propagated.

## 1. The two hypotheses (both built from the data, no fitted constant)

At a given baryonic acceleration g_bar, the two-sector picture gives dynamics = law + cold matter: g_dyn = F(g_bar) + g_cold.
- **H-L (the response lenses):** lensing sees the same force, g_lens = F(g_bar) + g_cold. Dynamics and lensing agree.
- **H-NL (the response does not lens):** lensing sees only Newtonian mass, g_lens = g_bar + g_cold. The cold matter required
  by lensing is then fixed by the data, g_cold,req(g_bar) = g_lens,obs(g_bar) − g_bar, and dynamics must be
  g_dyn,NL = F(g_bar) + g_cold,req(g_bar).
- Under H-L, the cold matter is not fixed by lensing; its prediction for dynamics is taken as F(g_bar) (cold matter negligible
  where the law already fits SPARC; the record's law rms 0.1003 / 0.1013 dex). This is the record's law, not a new fit.

F = the law with the record's ν_mono (read only), per footing.

## 2. Data and procedure

- **Lensing (primary):** B21 `Fig-8_RAR-KiDS-isolated_Colorbin_1` (lowest u−r, i.e. the bluer, late-type-dominated half, the
  closest match to SPARC discs) with its covariance. **Secondary:** `Fig-4-5-C1_RAR-KiDS-isolated_Nobins` (all isolated lenses).
  Column 1 is g_bar (m/s²); g_obs = 4G·ESD_t/bias, error = 4G·error/bias, G in pc units as in the record's loader.
- **g_cold,req:** g_obs − g_bar at the KiDS bin centres, interpolated linearly in (log g_bar, g_cold) between centres; set to 0
  where negative (conservative: H-NL then equals H-L there).
- **Dynamics:** SPARC good points (the harness's mask and weights, Υ = 0.61) with g_bar inside [the lowest KiDS centre ≥ 3e-13,
  the highest KiDS centre 3.92e-12]. Score each hypothesis by the harness's weighted rms of log g_obs − log g_pred over those
  points, per footing. Δ = rms_NL − rms_L.
- **Error propagation:** 2000 draws of the KiDS ESD vector from its covariance (seed 663), recomputing g_cold,req and Δ for each.

## 3. Classes (per footing; the lane label needs both)

- **NOT DIAGNOSTIC** if the median over the overlap points of g_cold,req/F(g_bar) < 0.1 (H-NL and H-L nearly identical there).
- **H-NL EXCLUDED** if Δ ≥ 0.05 dex AND at least 95% of the KiDS draws give Δ ≥ 0.03 dex.
- **H-NL CONSISTENT** if Δ ≤ 0.01 dex.
- **TENSION** otherwise.
- Reported, no verdict weight: the mean signed residual of each hypothesis on the overlap points; the same with the secondary
  lensing file; KiDS lensing vs the law over all 15 bins (χ² with the covariance), as context for H-L.

Stated limits: different populations (KiDS isolated lenses vs SPARC discs); B21's g_bar recipe vs SPARC rotmod; the SIS
conversion of ESD to g_obs. These are named in the verdict, not used to soften it after the fact.

## 4. MUTATE (`CFG663_MUTATE=1`, exit 1 iff both bite)

- M1: g_cold,req forced to 0 must give Δ = 0 exactly.
- M2: lensing g_obs replaced by g_bar (Newtonian lensing) must give the NOT DIAGNOSTIC class.

## 5. Machine rules

Light: one process, `nice -n 10`; allowed while the 1024³ run is live. The B21 tar is extracted into a fresh scratch directory and
read with `python3 -I`; nothing is downloaded.
