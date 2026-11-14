# AGB2R — blind re-grade of AGB2: my reading of the frozen rules (written and committed before any measured magnitude is read)

2026-11-14. A second implementation of lane AGB2 from two files only:
`closure_2026_11_14/AGB2_host_mass_step_redshift/FROZEN_CRITERIA.md` and `AMENDMENT_1.md`.
Also used, as Part J of the criteria prescribes: AGB1's `agb1_run.py` and `agb1_template.py` (imported unchanged) and
its committed `agb1_A_full.json`, `agb1_A_des_only.json`, `agb1_results.json`.
Not read: any other file of the AGB2 folder, its commits, or the write-ups of AGB1 and of the later AGB lanes.

What I had seen when this was written: the two files above; AGB1's fitter, template and the three JSON files
(AGB1's own amplitudes, profiles and fork values, which the criteria use as inputs); and, from the Pantheon+ table,
the non-magnitude columns only, to confirm the sample counts (1,563 = 716 low + 847 high; `measured` 1,251 = 542 + 709;
`k1` 1,590; all match the criteria), that duplicate light curves of one supernova share zHD and host mass exactly
(97 duplicate groups in `all`, 1,446 distinct CIDs), and the survey codes present. No magnitude column (mB, m_b_corr)
has been read, and nothing has been fitted. The amendment quotes two constant steps (K2) and K1's Ω_m; I saw those
there and nothing else of AGB2's numbers.

## What I will build (my reading)

### The galaxy model (`agb2r_galaxy.py`)
- Cosmic time from flat Ω_m = 0.30, H0 = 70, no radiation, by numerical integration.
- One common absolute time grid of 4 Myr steps. 541 formation times at lookback 13.000, 12.976, …, 0.040 Gyr
  (every 24 Myr, i.e. every 6 steps). Each galaxy starts as a 10⁶ M⊙ seed at its formation time.
- In each step the rate dM/dt = Ψ(M, z) p_Q(M, z) with Ψ = 2.00 e^{1.33 z} (M/10¹⁰)^0.7 M⊙/yr and
  p_Q = ½[1 − erf((log M − log M_Q(z))/1.5)], log M_Q = 10.43 + 0.9 log₁₀(1+z) (z ≤ 1.5), 8.56 + 5.6 log₁₀(1+z) above.
  **Reading:** z and p_Q are held at their step-start values and the growth is integrated exactly in M^0.3:
  M_end^0.3 = M^0.3 + 0.3 × 2.00 e^{1.33 z} p_Q × 10^{−7} × Δt[yr]; the mass formed in the step is M_end − M.
  M is the **surviving** stellar mass, the sum over all earlier steps of mass formed × (1 − f_ml(age)), with
  f_ml(t) = 0.046 ln(t/0.276 Myr + 1) and age measured from the middle of the forming step; the seed counts as a
  population born at the formation time and loses mass by the same law.
- **Reading:** the seed is part of the mass but not of the star-formation history; the progenitor-age distribution
  at time t weights each earlier step j by its formed mass × the delay-time distribution integrated over that step
  (Φ is averaged over the 4 Myr step on a sub-grid, because Φ rises as τ^20 below 0.3 Gyr):
  Φ(τ) ∝ (τ/0.3)^20/((τ/0.3)^21 + 1) (t_p = 0.3 Gyr, s = −1, α = 20). Mean and median of that distribution.
- Table: at each z = 0, 0.02, …, 1.6 (time rounded to the nearest step boundary), every track that exists gives
  (log M, mean τ, median τ); mean and median are interpolated linearly in log M onto log M = 7.5 … 12.4 (step 0.05).
  If no track reaches a grid mass at that z (the top of the grid at high z), the value of the most massive track is
  used (flat), and I report where that happens. Catalogue masses are clipped to [7.5, 12.4]; values in between by
  bilinear interpolation.
- The criteria print a table of mean ages at log M = 8 … 12 and z = 0, 0.5, 1.0, the median at z = 0, and the
  step-run gaps Δτ(z) for `all`. I compare my model with them and report the differences; they are AGB2's numbers,
  not checks, and I do not tune to them.

### Templates
- Redshift of a supernova = zHD (bins, templates, D_M); zHEL only in the (1 + z) factor of μ_fid.
- L_i = 1 if HOST_LOGMASS < 10, else 0 (the catalogue mass, not clipped).
- **Step run:** D_i = 0.030 Δτ(z_i)(L_i − ½); Δτ(z) on z = 0, 0.01, …, 1.00 = mean over the sample's high-mass rows
  of τ(M_j, z) minus the mean over its low-mass rows (rows, so duplicate light curves count once each — the sample is
  a set of rows; this is my reading), then linear in z.
- **Per host:** D_i = −0.030 τ(M_i, z_i).
- τ = mean (primary) or median (fork). The sample in use defines its own groups (`measured` recomputes Δτ).

### Part H
- Data: the Pantheon+ table and the STAT+SYS covariance, symmetrised (C + Cᵀ)/2; a sub-sample takes its sub-block.
- μ_fid = 5 log₁₀[(1 + zHEL) D_M(zHD)] with D_M in c/H0 for flat Ω_m = 0.334 (constants go into the bin offsets).
- Bins: 20 (or 40) equal-count bins in zHD of the sample in use. Edges at the zHD values of sorted positions
  round(kN/n_bins); a row goes to the bin by `searchsorted(edges, z, side="right")`, so the duplicate light curves of
  one supernova (identical zHD) never straddle an edge. Counts are then equal to within the ties.
- Design: one indicator per bin, (L − ½), D (and x1, c in reading R). Reading R: y = mB − μ_fid. Reading P:
  y = m_b_corr − μ_fid.
- Weights: **as frozen**, the inverse of the full (sub-block) covariance; **as amended**, diag(1/C_ii) of the same
  block. In both the parameter covariance is (XᵀWX)⁻¹, not rescaled by χ². Δχ²(A = a) = (Â − a)²/σ_A².
- Words H1 (step run) and H2 (per host) by the six W1 rules; second word ROBUST if each single fork (reading P;
  median; 40 bins; `measured`) gives the same first word. Under the amendment the forks use diagonal weights too.

### Checks
- **KG** (i) log M_Q(0.35) within 0.01 of 10.55, branches equal at z = 1.5 to 0.005; (ii) at z = 0,
  [τ(11.5) − τ(10.0)]/[τ(12) − τ(8)] ≥ 0.5 for the mean age; (iii) for the z = 0 track of log M = 11.5 (linear in
  log M between the two bracketing tracks), the lookback by which half of its **formed** mass had formed lies in
  [8, 11.5] Gyr and the lookbacks of 25 % and 75 % lie within 2 Gyr of each other; (iv) rebuilding the whole table with
  a 2 Myr step moves no tabulated mean **or** median age by more than 0.05 Gyr (I require both).
- **K1** flat ΛCDM on `k1` with m_b_corr, the full covariance, the offset profiled analytically, Ω_m by a bounded
  one-dimensional minimisation; pass |Ω_m − 0.334| ≤ 0.009. The amendment keeps K1 on the full covariance.
- **K2** reading R on `all`, 20 bins, the constant step with no template: g in [0.02, 0.09] mag. As amended: diagonal
  weights. As frozen: full covariance. Both reported; each reading's own K2 governs that reading.
- **K3** eight twins per weighting: y = model prediction with bin offsets o_b = 24 + 0.01 b, g = 0.05, (a, b) = (−0.15,
  3.1) in reading R only, plus A_true D, A_true ∈ {1, 0}, both templates, readings R and P, primary sample and bins.
  Pass each: |Â − A_true| ≤ 10⁻⁶ and χ²_min ≤ 10⁻⁸. The twin script exits 3 if all pass, 4 otherwise. No measured
  magnitude is read.
- **K4** primary configuration, reading R, both templates. One generator `numpy.random.default_rng(20261114)`; per
  draw, for bins 0 … 19 in order, one permutation of that bin's distinct CIDs, each CID taking the host mass of the CID
  it is mapped to (all its rows). L and both templates are recomputed from the shuffled masses (Δτ(z) included,
  though it cannot change: the masses of the sample are the same multiset). The same 400 shuffles serve both
  templates and both weightings. σ_A = the claimed error of the unshuffled real-data fit in that weighting.
  Pass: |mean Â| ≤ 0.2 σ_A and std(Â) (ddof 1) in [0.8, 1.25] σ_A. **As amended** also the sandwich error,
  V = B⁻¹ (Σ_CID s_g s_gᵀ) B⁻¹ with B = XᵀWX and s_g = X_gᵀ W_g e_g from the real-data residuals, no small-sample factor
  (CR0; I also print it with the G/(G−1) factor), in [0.8, 1.25] σ_A.
- Evaluability, per reading: as frozen, H1/H2 need KG, K1, K3 (full) and K4 (frozen form) to pass; as amended, KG, K1,
  K3 (diagonal) and K4 (amended form). If K2 fails in a reading, reading R is not evaluable there, the words are taken on
  reading P and the second word is FRAGILE (no R).

### Part J
- f(A): the committed AGB1 profile on `full` (and `des_only`) for A = −1.0 … 2.0 (31 of the 41 committed points),
  cubic spline (scipy CubicSpline, not-a-knot); every minimum is taken on a grid of 0.001 over [−1, 2].
- χ²_J(A) = f(A) + (A − Â_H1)²/σ_H1². J1 by the W1 rules on Δχ²_J(0), Δχ²_J(1) from the joint minimum; second word
  ROBUST if `des_only`, H1's reading-P amplitude, and both together, give the same first word. Edge minima flagged.
- t(A), n(A): AGB1's fitter (`Fitter("A", SN(sample), BAO("all"))`, template T_S), at A fixed on −1.0 … 2.0 step 0.1
  (q0 = 0) and −1.0 … 2.0 step 0.25 (never accelerated), started as AGB1's forks start them: fixed starts plus the
  committed profile point at that A (and, for never, also the q0 = 0 fit at that A). Cubic splines, minima on 0.001.
- Δχ²_today = min[t + prior] − min[f + prior]; Δχ²_never = min[n + prior] − min[f + prior].
  q0_J = the committed profile's q0, linear in A, at the minimum of f + prior.
- J2 and J3 by their rules, judged on (`full`, H1 primary); printed for (`full`, H1 reading P), (`des_only`, primary),
  (`des_only`, reading P).
- KJ with no prior: Δχ²(0), Δχ²(1) from my spline vs `agb1_results.json` to 0.02; my re-fitted f at A = 0 and 1
  (fixed starts plus the neighbouring committed point and AGB1's A-free fit as extra starts, as AGB1's profile did)
  vs the committed profile to 10⁻³; t − f and n − f at A = 0 and 1 vs AGB1's fork D_today, D_never to 0.01.
- Part J is run twice: with the amended H1 (diagonal) and with the as-frozen H1 (full covariance), the latter labelled
  NOT EVALUABLE if the frozen K4 fails.

### Reported only
- Band-by-band step: one fit with the 20 primary bin offsets, five band steps g_k (L − ½)[band k] for zHD in 0.01–0.05,
  0.05–0.15, 0.15–0.30, 0.30–0.50, 0.50–1.00, and global a, b in reading R; both readings, both weightings. Beside each,
  the step the slope predicts at A = 1: the mean of 0.030 Δτ(z_i) over the band's rows. A straight line through the
  five (generalised least squares with the five steps' joint covariance against the band's mean zHD), and the same
  line through the five predicted steps.
- Reading R with g fixed at 0, both templates.
- Model forks: alternate quenching mass log M_Q = 10.077 + 0.636 z at all z; the T_W delay-time distribution
  (τ^−1.13 for τ ≥ 40 Myr, 0 below); τ evaluated at catalogue mass ± 0.2 dex (L unchanged).
- Sample forks: zHD ≤ 0.7; drop SDSS (1), SNLS (4), PS1 (15), DES (10), Foundation (150), and "the other low-z sets
  together" = codes 5, 18, 50, 51, 56, 57, 61–66. **Reading:** the HST code 100 (5 rows at z ≈ 0.85) is not a low-z set
  and is never dropped.
- The joint amplitude with H2 in place of H1; (Â_H1 − Â_AGB1) over the combined error, AGB1's side of its 68 %
  interval that faces Â_H1 taken as its error.
- Not computed: the C14 mass-function-weighted median age today (the criteria do not give the mass function).

## Ambiguities resolved (summary)
1. Galaxy-integration details (step-start p_Q and z; mid-step ages for mass loss; seed in mass but not in the age
   distribution; Φ averaged over each step) — not written in the criteria; mine as above.
2. Masses above the most massive track at high z: flat. Masses below 7.5: clipped (criteria).
3. Δτ averages over rows, not distinct supernovae.
4. Equal-count bins keep ties together.
5. K4: shuffle by distinct CID within bins; the same draws for both templates; σ_A of the real fit; sandwich CR0.
6. "The other low-z sets": HST code 100 not included.
7. q0_J from the committed profile's q0; f in J2/J3 is the committed profile, not refitted (KJ checks they agree).
8. The power forecasts in the criteria (σ_A 0.40 / 0.10 full covariance; 0.41 / 0.12 diagonal) are compared, not
   used as checks.

kappa = 1/2 FITTED; not theory closed.
