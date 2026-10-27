# X55_one_halo_mass_for_both: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED. Footings never pooled (canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s²). No dark-matter particle. Route E's
clumping w ≈ 0 component is "cold dark energy" (not matter, not a particle). ΛCDM is the external rival. Not "theory
closed". Nothing here may say the data favour the framework; results are phrased as "this test …".

## Question

X53 found that KiDS-1000 isolated lenses want route-E halos about 0.35–0.5 dex heavier than EM1's SPARC relation gives.
**Is there one halo-mass relation log M200 = a + b (log M_b − 10.5) that fits BOTH the SPARC rotation curves (route E at
the a₀/(2πG) Burkert floor, X38's machinery and line) AND the B21 KiDS isolated-lens ΔΣ (route E exactly as X53's (H2H))?**

Pivot 10.5 (not EM1's 10.0) is chosen to sit between the SPARC and lens mass ranges; EM1's (a, b) = (11.18, 0.90) at pivot
10 is (11.63, 0.90) at pivot 10.5. Grids and outputs use pivot 10.5.

## 1. SPARC side (framework-native; no c(M), no abundance matching)

- EM1's SPARC loader, mask, weights, Υ grid 0.30–1.20 (step 0.01, per galaxy free, as X38) and `fit_one`/`pooled`/`line`,
  executed read-only (EM1 code up to its backgrounds block, as X38 does).
- M_b = 0.5 L[3.6] + 1.33 M_HI (EM1's definition; fixed, not the fitted Υ). M200 w.r.t. 200 ρ_crit,0, background A's h
  (X38). Burkert at Σ_core = a₀/(2πG) per footing, X38 A1 compact root, saturation at M_max counted (X38 rule). **Primary:
  pure floor (X38).** Reported variant: X43 rule max(floor, η Σ_coll), c_f = 4 (as the lensing side).
- Per galaxy, the halo depends only on M200, so each galaxy's best-Υ weighted squared residual wr2, weight ws and Υ index
  are tabulated on log M200 = 8.00–15.00 (step 0.01, linear interpolation in log M200). The statistic is EM1/X38's pooled
  rms = sqrt(Σ wr2 / Σ ws); median Υ = median of the per-galaxy best Υ.
- **SPARC region in (a, b):** best fit (a_S, b_S) = minimum pooled rms on the grid a 10.0–14.0, b −0.5–2.5 (step 0.02).
  Uncertainty by galaxy bootstrap: B = 1000 resamples of the 175 galaxies (numpy default_rng seed 55), each refit on the
  same grid. Δχ²_S(a, b) = Mahalanobis distance² from (a_S, b_S) with the bootstrap covariance of (a, b) (2 dof).
  Reported alongside: bootstrap fraction at the grid edge; a Birge-type point Δχ² (Σwr2 rescaled so its minimum equals
  N_pts − 2), which ignores the per-galaxy systematics and is reported only.
- **SPARC line (X38):** rms ≤ 0.110 and median Υ in [0.50, 0.80].

## 2. KiDS side (exactly X53's (H2H); framework-native masses)

- X53's code executed read-only up to its scoring loop (as X53 A1 does): B21 Fig. 3 isolated sample, released covariance,
  native background (h 0.679), F2 inventory (LePhare + 0.15 dex M★, B21 cold gas, hot CGM 0.5 M★ inside 100 kpc), Newtonian
  baryons, Burkert halo with Σ_core = max(a₀/(2πG), η Σ_coll), **c_f = 4**, sharp truncation at R200 (200 ρ_crit,0, bg A
  h), CFG805's two-halo term with b_eff ≥ 0 per bin profiled (exact non-negative LS). Relation variable M_b = M★ + M_cold
  (X53 A6).
- ΔΣ is linear in the mass profile, so per bin: stacked model = stacked baryons + lens-weighted interpolation of a halo ΔΣ
  table on log M200 (8.0–15.0, step 0.01). K_TAB requires this to reproduce X53's `stack_H` χ² at EM1's relation within 0.1.
- χ²_K(a, b) on the same (a, b) grid, all radii (60 points, graded) and R ≤ 0.31 Mpc (28 points, reported).
- **KiDS region:** Δχ²_K = (χ²_K − χ²_K,min) / s_K with **s_K = max(1, χ²_K,min / (n − 4 − 2))** (Birge scaling: (H2H)
  fits badly in absolute terms, so its regions are widened; this favours route E, i.e. finding one relation).
  The unscaled region (s_K = 1) is reported.

## 3. Separation statistic and verdict (per footing)

- nσ(Δχ²) for 2 dof: p = chi2.sf(Δχ², 2), nσ = norm.isf(p/2) (1σ ↔ 2.30, 2σ ↔ 6.18, 3σ ↔ 11.83).
- **Separation n_sep = min over grid nodes of max(nσ_S, nσ_K)**, the smallest n at which the two n-σ regions share a
  point. **Graded n_sep is taken over nodes that pass X38's SPARC line** (the question asks for sensible Υ). Unrestricted
  n_sep is reported. The node attaining it is the **joint relation**; for it I report SPARC rms / median Υ / saturations,
  KiDS χ² (all radii, with 2h) and b_eff, and the law's SPARC rms (EM1 LAW) and KiDS χ² (X53 L2H) for comparison.
- **Informativeness (coordinator, frozen):** SPARC's bootstrap 68 % interval (16th–84th percentile) of log M200 evaluated
  at each lens bin's lens-weighted mean log M_b must be ≤ 0.30 dex wide in all four bins. If not, a would-be ONE RELATION
  verdict becomes **NOT INFORMATIVE** ("SPARC cannot tell"). SPARC's bootstrap widths on (a, b) and on M200 at the four
  lens-bin masses are reported regardless.
- Classes:
  - **ONE RELATION FITS BOTH**: n_sep ≤ 2 and the informativeness condition holds.
  - **NOT INFORMATIVE**: n_sep ≤ 2 but the condition fails.
  - **TENSION**: 2 < n_sep < 3.
  - **CONTRADICTION**: n_sep ≥ 3.
  - **UNDECIDED**: step 0 fails (no grading), or no line-passing node exists on the grid.
- Lane verdict: the same class on both footings → that class; otherwise UNDECIDED (both reported).

## 4. Step 0 (stop rule)

1. X53's χ²: L, H, L2H, H2H on primary and all radii, both footings, recomputed via X53's own code (read-only) and equal
   to `x53_outer_lensing_results.json` within 0.05.
2. X53 A1: the best common shift (truncated, c_f 4) on A1's 0.05-dex grid, recomputed with my halo table, equals A1's
   shift exactly and its χ² within 0.2 (primary and all radii, both footings).
3. EM1: `em1_emergent.py` rerun unchanged in a scratch copy (outputs only there) returns (a, b) = (11.18, 0.90) for bg A
   (11.20, 0.90 bg B) and R1 rms 0.0656 within 1e-4.
4. X38: my SPARC table at EM1's relation reproduces X38's SPARC row (bg A): rms 0.0795 / 0.0729 within 2e-4, median Υ
   0.77 / 0.60, 0 saturated.

## 5. Reported (not graded)

- Lens stellar-mass systematic: lens M★ shifted −0.15 and +0.15 dex (baryons and relation variable together); regions,
  n_sep and class.
- Primary radial range (R ≤ 0.31 Mpc) KiDS region and n_sep; untruncated halos (100 R200) variant; SPARC with the X43 rule.
- **Restricted overlap:** the M_b range where SPARC and the lenses overlap (lens-weighted 5th–95th percentile of log M_b,
  all bins pooled); SPARC refit (with its own bootstrap) on galaxies inside it; n_sep against KiDS; plus SPARC's
  bootstrap log M200 at each lens bin's mean M_b against the KiDS log M200 there.
- **Isolation leakage:** (i) KiDS on R ≤ 0.31 Mpc only (one-halo, not exposed); (ii) outer data (B21 labels > 0.4 Mpc)
  scaled by F2's committed GAMA / KiDS isolated ratio 0.64 (covariance rows/columns scaled alike). Does either close the gap?
- **Saturation (coordinator):** number of SPARC galaxies at M_max, and lens weight fraction per bin at M_max, at the SPARC
  best fit, the KiDS best fit and the joint relation; number of nodes inside each 2σ region with any saturation.

## 6. Checks and MUTATE

- K0: step 0. K_TAB: halo-table stack = X53 `stack_H` (χ² within 0.1). K_NNLS: my vectorised b_eff ≥ 0 fit equals X53's
  `fit` within 1e-6 in χ² at one node. K_BOOT: bootstrap seed reproducible (two draws identical). K_R: peak RSS < 1 GB.
- **MUTATE** (`X55_MUTATE=1`, separate `_MUTATE` outputs): lens stellar masses shifted +1 dex. Step 0 items 1 and 2
  (named K0_X53 and K0_A1) must FAIL and the run must exit 1.

## 7. Resources

One thread (OMP_NUM_THREADS=1), `nice -n 15`, PYTHONHASHSEED=0, < 1 GB. No downloads. `compute_queue/` untouched. Nothing
written outside this lane except the EM1 scratch copy in a temporary directory, removed afterwards.
