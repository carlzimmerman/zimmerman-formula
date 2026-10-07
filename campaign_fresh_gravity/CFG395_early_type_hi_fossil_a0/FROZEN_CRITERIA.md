# CFG395 — FROZEN CRITERIA: "fossil a0" in early-type HI discs

Frozen 2026-10-06, before any script or residual was computed. Committed alone.

## Disclosure of what was seen before freezing

A data inventory was done first (no residuals, no RAR quantities computed):
- VizieR has **no** catalogue for den Heijer+2015 (J/A+A/581/A98 not found), nor for Serra+2016 (J/MNRAS/460/1382) or Lelli+2017 (J/ApJ/836/152).
- den Heijer+2015 (arXiv:1509.05236) gives **one** outer HI circular velocity per galaxy (no rotation curves); the radius is not tabulated there. Its Table 1 is already on disk (`real_research/data/denheijer2015_etg_hi_tfr.tsv`, CFG37).
- Serra+2016 (MNRAS 460, 1382; arXiv:1604.07902) Table 1 gives, for the same 16 galaxies, R_HI (arcsec) and V_HI, plus R_eff and the JAM peak.
- Lelli+2017 (ApJ 836, 152; arXiv:1610.08981) Table (TableETG.tex) gives [3.6] luminosity, distance, R_eff, and the exponential-disc R_d and Σ_d for the same 16 rotating ETGs, and adopts Υ_[3.6] = 0.8 for rotating ETGs (Chabrier).
- So the ETG sample is **16 points, one per galaxy**, at 3.4–13.7 R_eff. These are not "rotation curves"; the task's "outermost points" clause applies.
- On-disk CFG41/CFG53: Di Teodoro+2023, 15 massive HI discs, four with RC3 T ≤ 0 (NGC 1167, NGC 5790, UGC 12591, UGC 12811); 216 figure-recovered points, point-mass WISE stellar masses, a selection bias of +0.076 ± 0.030 dex (CFG41).

## Prediction under test

Slow settling: a galaxy keeps the a0 of its settling epoch. a0 tracks dark-energy density (a0(z) = κ c √(G ρ_DE(z)), κ = ½ FITTED). With DESI-like evolving DE, ETGs settled at z ≈ 2 → a0 ≈ 0.87 × local; late types settled late → a0 ≈ 1.00–1.06 × local. Deep-limit residual offset 0.5 log10(0.87/1.00..1.06) = −0.030 to −0.043 dex. Fast settling: 0.

The **expected signal at the actual g_bar of the points** is also computed (not only the deep limit): shift(f) = log ν(g_bar/(f a0)) − log ν(g_bar/a0) with ν = ν_mono; Δ_pred = median_ETG shift(0.87) − median_late shift(f_late), f_late = 1.00 and 1.06. Reported, not used to set thresholds.

## Data and models (headline)

- **ETG points (16):** g_obs = V_HI² / R_HI, R_HI = θ_HI × D. D = Lelli+2017 distances (consistent with their L_[3.6]).
- **ETG baryons:** Υ_[3.6] = 0.8 (Lelli+2017 fiducial for rotating ETGs).
  - disc: L_d = 2π Σ_d R_d², razor-thin exponential (Freeman exact radial force);
  - bulge: L_b = L − L_d, spherical Hernquist with half-light radius = the galaxy's R_eff (declared approximation; the bulge R_eff is not tabulated), a = R_eff / 1.8153;
  - gas: 1.33 M_HI (den Heijer/Serra 2012 M_HI, rescaled by (D_Lelli/D_C11)²) as a point mass with enclosed fraction 0.5 at R_HI (bracket 0 and 1).
- **Late types:** SPARC (Lelli+2016 rotmod + master table), Q ≤ 2, T ≥ 8, Υ_disk 0.5, Υ_bul 0.7, every point with g_bar inside [min, max] of the headline ETG g_bar.
- **Kernel:** ν_mono (FP1's committed kernel via CFG4_common, read-only). **Both footings:** a0 = 9.3603e-11 and 1.1312e-10 m/s².
- **Residual:** r = log10 g_obs − log10[ν_mono(g_bar/a0) g_bar].

## Statistic

Δ = median(r_ETG) − median(r_late). Uncertainty:
- σ_boot: bootstrap by galaxy (ETG galaxies and late galaxies resampled independently, 4000 draws, seed 395);
- σ_ML,ETG: ETG Υ × 10^(±0.1) applied coherently to all 16 → half the spread of Δ;
- σ_ML,late: SPARC Υ_disk and Υ_bul × 10^(±0.1) coherently → half the spread (the window is re-used, not re-selected);
- σ_gas: ETG gas enclosed fraction 0 vs 1 → half the spread;
- σ_bulge: Hernquist bulge vs a point-mass bulge → half the spread;
- σ_Δ = quadrature sum.

## Verdicts (per footing)

1. **NON-DISCRIMINATING** if σ_Δ > 0.02 dex (cannot see a −0.04 signal at 2σ). This takes precedence.
2. else **SLOW-SETTLING HINT** if Δ < −0.02 and (Δ + 0.02)/σ_Δ < −2.
3. else **FAST / NO FOSSIL** if Δ > −0.02 and (Δ + 0.02)/σ_Δ > 2.
4. else **INCONCLUSIVE**.

Power is reported as |Δ_pred| / σ_Δ and as 0.04/σ_Δ.

## Controls

- **C1:** Serra+2016 V_HI equals den Heijer+2015 v_circ for all 16 galaxies (names matched).
- **C2:** R_HI in kpc at the Cappellari+2011 distances (den Heijer's D column) reproduces den Heijer's stated range 8–28 kpc (mean 15) and R_HI/R_eff 3.4–13.7 (mean 7.3): endpoints and means within 0.6 kpc and 0.15.
- **C3:** L − L_d ≥ 0 for all 16 (the Lelli decomposition is self-consistent).
- **C4:** the session-06 SPARC late-type count is reproduced (27 T ≥ 8 galaxies with ≥ 3 gas-dominated deep points at Q ≤ 2) through the same loader.
- **MUTATE:** −0.04 dex added to every ETG residual; the canonical Δ must shift by −0.040 ± 0.005. The MUTATE run writes `_MUTATE` outputs and exits 1 when the shift is detected.
- A failed control is kept and reported; the verdict is not re-run with changed tolerances.

## Secondary arms (reported, NOT verdict-bearing)

- **S1:** SPARC T ≤ 1 (S0–Sa), Q ≤ 2, points with g_bar < 10^-10.5, against the late arm in the S1 window (same machinery).
- **S2:** Di Teodoro+2023 T ≤ 0 (four S0/S0a): recovered points with g_bar < 10^-10.5, point-mass baryons (WISE M_*, Υ as in CFG41, plus 1.36 M_HI as given in the tsv), minus CFG41's selection bias 0.076 dex; against the late arm in the S2 window. Stellar mass systematic ±0.2 dex (CFG41's).
- **S3 (sensitivities of the headline):** Cappellari+2011 distances; ATLAS3D r-band L × (M/L)_SFH × 10^(−0.25) (Salpeter→Chabrier) as point mass; Υ_[3.6] 0.6 and 1.0.

## What this lane cannot do

ETG outer points are star-dominated, so the residual moves by ~0.5 × δlogΥ in the deep limit: a −0.04 dex fossil signal is degenerate with an 0.08 dex lower ETG M/L. Nothing here can separate a fossil a0 from a stellar-population M/L offset unless σ_Δ (which includes ±0.1 dex Υ) is below 0.02.
