# CFG186 — does SPARC's acceleration scale depend on a galaxy's speed through the CMB frame? (frozen 2026-09-29, before any script or number)

**Why.** Door 11, variant 11C (`campaign_fresh_gravity/closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`): the owner's flow read as a cosmic time-flow field (aether / khronon) whose rest frame is, in practice, the CMB frame. Gate **G7**: a₀ must not change by more than 10% for galaxies moving at 0–600 km/s relative to the flow's rest frame. The record's KM1 (`real_research/khronon_momentum_2026/README.md`, check C7) found that in linearised khronometric gravity (λ = 1 + ε, L280's equal-speed locus) the aether acceleration the MOND sector reads is distorted by D cos²θ, D = 2w²/(εc²), sphere average D/3 = 0.11–0.29 at 620 km/s across the record's c14 window: a₀ would track each galaxy's speed w through the CMB frame unless c₂ ≫ 10⁻⁴. The literature file (`data_assembly/DOOR11_LITERATURE_2026-09-29.md`, G7) found no published test of a₀, RAR or BTFR residuals against a galaxy's speed relative to the CMB. This lane runs that test on the repo's copy of SPARC. A null or a non-diagnostic result is valid. κ = ½ stays FITTED; a₀ is fitted here (ā₀ free), so κ enters no pass line.

## 1. The observable (declared honestly)
- **Frame conversion.** Heliocentric velocity cz_hel → CMB frame with the solar dipole **v_sun = 369.8 km/s toward (l, b) = (264.0°, 48.3°)** (Planck 2018; the literature file quotes 369.82 ± 0.11 toward (264.021°, 48.253°); the rounded values are used): 1 + z_CMB = (1 + z_hel)/(1 − v_sun·n̂/c), i.e. cz_CMB ≈ cz_hel + v_sun·n̂.
- **What a galaxy's speed through the flow frame means.** A galaxy at rest in the Hubble flow is at rest in the local CMB (aether) frame, so the speed w is the **peculiar** velocity, not cz. Line of sight: **u = c (z_CMB − z_cos(D))/(1 + z_cos(D))**, z_cos from the distance D in flat ΛCDM (Ω_m = 0.311, declared; the second-order term is ≤ 1% of H₀D below 30 Mpc). **H₀ = 67.66 km/s/Mpc primary; 73 variant** (SPARC's Hubble-flow convention and the ladder scale of TRGB/Cepheid distances; with ladder distances, 67.66 adds ≈ +5.3 D km/s to u, D in Mpc).
- **The 3D speed is not measurable.** Only u (one component) is observed; the transverse components are not. Two proxies:
  - **W1 (PRIMARY): w² → u².** If the three components are independent and isotropic, E[w² | u] = u² + const, so a fit in u² returns the same β (the transverse part goes into ā₀ and scatter).
  - **W2 (reported): the Local Group's coherent motion.** w² = u² + |V_LG|² − (V_LG·n̂)², i.e. the galaxy shares the LG's transverse motion; **V_LG = 627 km/s toward (276°, 30°)** (Kogut et al. 1993, FROM MEMORY, UNVERIFIED; printed next to v_sun,CMB − v_sun,LG with v_sun,LG = 318 km/s toward (106°, −6°), Tully et al. 2008, also from memory).
  - **The common term, stated plainly.** The LG moves at ~620 km/s through the CMB frame and the Local Volume moves with it (the Local Sheet is cold). If every nearby galaxy moves at ≈ 620 km/s, the effect is the same for all of them and is absorbed into the fitted ā₀ (itself degenerate with the fitted a₀ / κ). SPARC alone cannot see that common term. What W1 then measures is a sky quadrupole of a₀ aligned with the LG motion (u² ≈ (V_LG·n̂)²), which a pure speed effect does not predict. Any W1 result is therefore conditional on independent velocity components, and W2 shows how much leverage is left if the flow is coherent.
- **Error on u from the distance.** σ_u ≈ H₀ e_D. With SPARC's e_D this is ~10–60 km/s for TRGB (e_D/D ≈ 5%), ≈ 170 km/s for Ursa Major (18.0 ± 2.5 Mpc) and 400–2600 km/s for Hubble-flow distances (e_D/D ≈ 30%). Script A tabulates it per method. The distance is **not** fixed: it is a per-galaxy nuisance shared between the rotation curve (a₀ ∝ D⁻² in the deep regime) and the velocity (u = cz_CMB − H₀D), so the correlated error is inside the likelihood (section 3).

## 2. Data and sample (on disk; no network)
- Rotation curves, baryonic components and the master table (D, e_D, f_D, Inc, e_Inc, Q): read as `CFG4_common.load_sparc()` reads them (read-only import; ν_mono from FP1 through CFG4_common). Positions: `real_research/data/sparc_lelli2016_table1_pos.tsv` (VizieR J/AJ/152/157) → Galactic with astropy.
- **Heliocentric velocities, first available source used:** (1) `cz_kms` of `real_research/data/sparc_cosmicweb_match.csv` (NED heliocentric redshifts via `sparc_ned_positions.json`, built by `prep_2026/a0_line/cosmicweb_match.py`; 126 of 175 galaxies); (2) HRV of the Updated Nearby Galaxy Catalog (`ungc_karachentsev2013.tsv`, Karachentsev et al. 2013); (3) HRV of Kourkchi & Tully 2017 (`kt2017_galaxies.tsv`; used as a per-galaxy velocity only if members of one group carry different values, a check the script prints; otherwise dropped); (4) cz of 2MRS (`2mrs_huchra2012.tsv`). Sources (2)–(4) are matched to the SPARC position (nearest within 1.5′). Where sources overlap, the median |Δ| is reported and every |Δ| > 50 km/s is listed; the primary fit is rerun without those galaxies (reported). Galaxies with no velocity are listed and dropped.
- **PRIMARY sample:** clean (Q ≤ 2, Inc ≥ 30°, ≥ 5 usable points; CFG182's cuts) with a **redshift-independent distance**, f_D ∈ {2 TRGB, 3 Cepheid, 4 Ursa Major, 5 SNIa}, and a velocity.
- **Hubble-flow galaxies (f_D = 1) are EXCLUDED from the primary.** Their D was computed from their own redshift (H₀ = 73 plus flow corrections), so u is a function of sky position and the flow model, not a measurement of the galaxy's motion. Their naive β, and the β of the whole clean sample, are reported only as a bound on what including them would do, labelled CIRCULAR.
- **SECONDARY:** `real_research/data/sparc_a0_environment_table.csv` (122 galaxies). Provenance: `real_research/reviews/project_sparc_a0_vs_cosmicweb.py`, `fit_a0_per_galaxy()` and `write_outputs()`: log₁₀ a₀ = median over deep points (g_bar < 1.2 × 10⁻¹⁰/3) of 2 log g_obs − log g_bar, fixed Υ_disk = 0.5 and Υ_bul = 0.7, catalogue distance and inclination, no errors. It is refitted on its f_D ≠ 1 galaxies with u at the catalogue distance, unweighted, with bootstrap and permutation, and is labelled SECONDARY everywhere.

## 3. Per-galaxy likelihood and the statistic
- **Law:** g_obs = ν_mono(g_bar/a₀) g_bar (the 09-26 kernel decision; with a₀ fitted the kernel only shapes the transition). Only the primary kernel is run.
- **Nuisances (CFG182's model, re-implemented in this lane, not imported):** Υ_disk and Υ_bul log-normal about 0.5 and 0.7 with σ = 0.1 dex; inclination Gaussian (e_Inc; predicted velocity × sin i′/sin i); distance Gaussian (e_D; g_bar invariant, predicted velocity × √(D′/D)). χ² in velocity space with the published e_V, plus the prior terms.
- **2D profile curves.** For every clean galaxy, C_i(x, t) on x = log₁₀ a₀ ∈ [−11.30, −9.00] (step 0.02) × t = (D − D_SPARC)/e_D ∈ [−4, 4] (step 0.25), with D ≥ 0.3 D_SPARC (infeasible cells masked). At each cell Υ_disk, Υ_bul and i are profiled (least squares, warm-started along x). The t prior is inside C. A cubic spline along t maps the curves onto step 0.05 for the fit. Checks: warm-start vs cold starts; min_t C_i reproduces a 1D distance-profiled curve (reported cross-check against CFG182's committed-or-not `cfg182_a_profiles.npz`, read only).
- **Weights.** Birge scaling s_i = max(1, χ²_min,i/(N_i − 1)) (CFG182's convention). Intrinsic-scatter inflation q_i = 1/(1 + τ²/σ_i²): σ_i is the Δχ² = 1 half-width of the scaled, distance-profiled curve p_i(x) = min_t C_i(x, t)/s_i, and τ is the maximum-likelihood extra scatter of the preferred values x̂_i at β = 0 (Gaussian approximation; it uses no speed information). Reported variants: q_i = 1, and no Birge scaling.
- **Model:** log₁₀ a₀,i = L + log₁₀(1 + β z_i), with z_i = (w_i/w_ref)², **w_ref = 600 km/s**, so β = 0.10 is the G7 line (10% at 600 km/s).
- **Global statistic:** F(L, β) = Σ_i q_i min_t [C_i(L + log₁₀(1 + β z_i(t)), t)/s_i], where z_i(t) uses u_i at D = D_SPARC + e_D t. **The distance is shared by the curve and the speed.** 1 + β z_i ≥ 0.05 is enforced as in CFG182. β̂ and L̂ come from the minimum. Errors: 2000 galaxy bootstrap resamples (primary); the Δχ² = 1 profile interval is reported.

## 4. Power row (script A, BEFORE any β fit on the real speeds)
- (P1) Fisher: σ_β,F = ln 10 / √(Σ_i v_i (z_i − z̄_v)²), with v_i = 1/(σ_i² + τ²) and z_i at the catalogue distance.
- (P2) Curve-level mocks at β = 0 (N = 500): each galaxy's curve is shifted in x so its preferred value sits at L₀ + ε_i, with ε_i ~ N(0, σ_i² + τ²). β̂ is fitted with the real speeds; σ_β,mock = half the 16–84% width.
- **β_det = 2 max(σ_β,F, σ_β,mock)**, the smallest β detectable at 2σ (50% power). The 80%-power value 2.84σ is also reported.
- **If β_det > 0.10 the test is declared NON-DIAGNOSTIC for G7 before the fit is looked at.** No G7 verdict is then issued from SPARC; β̂, its errors and the upper limits are reported as a bound only. The row is also computed for W2 and for H₀ = 73 (reported). Script A writes the verdict to its results JSON; script B prints it first.

## 5. Nulls (script B)
- **Speed shuffle (N = 2000):** the catalogue-distance velocities (u_j(0), plus the transverse term for W2) are permuted among the primary galaxies. Each galaxy keeps its own distance lever: u_i′(t) = u_π(i)(0) + [u_i(t) − u_i(0)]. p_perm = (1 + #{|β̂_perm| ≥ |β̂_obs|})/(N + 1). Variant (reported): permutation within distance-method groups.
- **Noise injection (N = 1000):** the P2 mocks (β = 0, real speeds, extra scatter τ), giving p_noise the same way.

## 6. Systematics
- **Distance-method split:** I = f_D ∈ {2, 3, 5} (individual TRGB/Cepheid/SNIa distances) versus UMa = f_D = 4 (one cluster distance; its internal velocity spread is measured with no distance error but spans little speed). β in each, with a bootstrap difference test.
- **H₀ = 73** variant; the **W2** proxy; velocity-source disagreements dropped.
- **Sky split:** the hemispheres n̂·V̂_LG > 0 and < 0 (both keep leverage in u²); Galactic b > 0 / b < 0 (reported if both halves have ≥ 10 galaxies).
- **β with a free sky dipole** (a₀,i ∝ (1 + β z_i)(1 + D·n̂_i), D a free 3-vector; reported). This guards against the uneven sky coverage leaking a sky dipole (the claims CFG182 re-tests) into β.
- **β with a distance term** γ log₁₀(D_SPARC/10 Mpc) (reported).
- **The CIRCULAR rows:** β on the Hubble-flow galaxies alone, and on all clean galaxies (reported only as a bound).

## 7. Pass lines (declared before data)
- **SIGNAL** ("a₀ tracks CMB-frame speed") requires ALL of:
  - S1: p < 0.003 against both nulls.
  - S2: β̂_I has the same sign at ≥ 2σ, and I and UMa agree (p > 0.05).
  - S3: the H₀ = 73 value lies within 1σ_boot of the primary.
  - S4: the two LG-apex hemispheres agree (p > 0.05).
- **G7 PASS** (only if DIAGNOSTIC): the two-sided 95% Neyman interval for β lies inside [−0.10, +0.10].
- **G7 FAIL:** SIGNAL declared with |β̂| > 0.10.
- **Otherwise:** a NULL (or NON-DIAGNOSTIC) result, reported with its limits.
- **Limits by Neyman construction (curve level):** β_inj on a grid (−0.90 to 3.00, step 0.05), 200 trials each (the P2 mocks plus the shift log₁₀(1 + β_inj z_i(0)) at the catalogue distance). F(β_inj) = P(β̂ ≥ β̂_obs | β_inj). Outputs: the one-sided 95% upper limit β₉₅ (F = 0.95), the two-sided 95% interval (F = 0.025, 0.975), and the recovery bias ⟨β̂⟩ versus β_inj.

## 8. Translation to the khronon parameter (conditional on KM1's model, stated as such)
- KM1: D = 2w²/(εc²) and sphere average D/3. Read as a₀ → a₀(1 + D/3) (the deep-regime equivalent of scaling the MOND input), this gives **β = 2 w_ref²/(3εc²) = 2.670 × 10⁻⁶/ε**, so the data require ε ≥ 2.670 × 10⁻⁶/β₉₅ (and |β| from the two-sided interval for either sign).
- On L280's locus, ε = c₂ = c14/(1 − 2c14). KM1's window c14 ∈ [1, 2.5] × 10⁻⁵ corresponds to β ∈ [0.107, 0.267]; G7's line β = 0.10 is ε = 2.67 × 10⁻⁵.
- **Caveats:** KM1's distortion is anisotropic (cos²θ relative to the motion) and only its sphere average is used; W1 is conditional on independent velocity components (section 1); KM1 is linear order only.

## 9. MUTATE control (must bite)
- **MUTATE=1 (scripts A and B) injects β = 0.30 at the point level before the curves are built:** V_obs → V_obs √(ν(y′)/ν(y)), with y = g_bar,fid/a₀,ref, y′ = y/(1 + 0.30 z_i(0)), z_i(0) = (u_i(D_SPARC)/600)² (W1, H₀ = 67.66), a₀,ref = 1.2 × 10⁻¹⁰ m/s² (declared), and e_V unchanged. Outputs are named `*_MUTATE.*`.
- **M1 (load-bearing):** β̂_mut − β̂_obs ∈ [0.24, 0.36].
- **M2 (reported):** the mutated data's p values. They are required to be < 0.003 only if 0.30 ≥ 4σ_β; otherwise they are a statement of power.
- **M0 (load-bearing, both modes):** synthetic noiseless curves C = (x − L₀ − log₁₀(1 + 0.30 z_i(t)))²/σ_i² + t² must return β = 0.300 ± 0.005 (fitter exactness).

## 10. Expectations (hand estimates, written down so they can be wrong)
- CFG182's curves have per-galaxy half-widths of median ~0.26 dex. With ~60 primary galaxies whose z = (u/600)² spreads by ~0.3 (TRGB galaxies at |u| up to ~600 km/s; Ursa Major bunched near z ≈ 0.05), the hand estimate is σ_β ≈ 0.25 and β_det ≈ 0.5. That is 5× the G7 line, so **NON-DIAGNOSTIC (P ≈ 0.9)**.
- β̂ consistent with 0 at < 2σ (P ≈ 0.85).
- W2 has almost no leverage (σ_β > 1).
- β₉₅ ≈ 0.4–0.7, i.e. ε ≳ (4–7) × 10⁻⁶. That does not reach KM1's window (β 0.11–0.27) (P ≈ 0.75).

## Scripts (each < 10 min; outputs named by mode)
- `cfg186_common.py` (shared).
- `cfg186_a_curves_power.py` (velocities, sample, 2D curves, power row).
- `cfg186_b_fit.py` (fit, nulls, systematics, limits, KM1, G7).
- `cfg186_c_pergalaxy_table.py` (SECONDARY).
- Rules: nothing edited outside this directory; no personal names; declared control failures are kept; a null or a non-diagnostic result is valid.

## Addendum 1 (after part A's first run; before any β fit on the real speeds)
Part A's first run is kept as `cfg186_a_curves_power_firstrun.out` / `cfg186_a_curves_power_results_firstrun.json`. It built the curves (149 clean galaxies, 0 non-finite cells, optimizer check 0.0000, CFG182 cross-check 95% |Δχ²| = 0.027) and found three problems. None of them involves the speeds.
1. **A bug, found by the power-row mocks.** Beyond the x-grid, the curves were continued linearly with the edge derivative (CFG182's convention). That makes the objective unbounded below when a curve's minimum lies at a grid edge. Three primary TRGB galaxies prefer log₁₀ a₀ ≤ −11.30, the grid's lower edge: CamB, NGC2976 and UGC07577. The β = 0 mocks then ran away: mean β̂ = +5.6 and σ = 5.4, against the Fisher 0.47.
   - **Fix:** one linear ghost point at each end, so Catmull-Rom covers the whole grid, and a **non-decreasing outward continuation**: a curve whose minimum lies at an edge is flat beyond it. The grid, the model and every pass line are unchanged. The fix applies identically to the real fit, the nulls and MUTATE.
2. **The spline check (SPL) failed as written.** Its max |Δχ²| was 0.69 over 24 random cells (median 0.0000). A follow-up over 60 cells found the large errors only in cells 65–1800 above the galaxy's minimum, with relative error ≤ 0.5%, where the fit never goes.
   - **Redefinition:** the load-bearing check now uses cells within Δχ² ≤ 25 (unscaled) of each galaxy's minimum, which must agree to 0.1. The relative error over all cells (≤ 1%) is reported. The first-run failure stays on record in the firstrun files.
3. **τ.** τ = 0.353 dex, the Gaussian ML value as declared, is inflated by the same three edge galaxies. The declared τ is kept; τ without them is reported as a sensitivity. The Fisher row alone (σ_β = 0.47, so β_det = 0.94) already puts the primary test at ~9× the G7 line.

## Addendum 2 (after part A's second run; still before any β fit on the real speeds)
The second run (`cfg186_a_curves_power_secondrun.*`) applied Addendum 1's fix. The β = 0 mocks still ran away: median β̂ ≈ 4, against the Fisher σ = 0.47.
- **Diagnosis** (curve-level mocks only, no real speeds fitted):
  - Idealised parabolic curves give β̂ 16–84% = [−0.54, 1.09] with z(t) coupled, and [−0.45, 0.63] with z frozen at the catalogue distance, matching the Fisher value.
  - The real curves with z frozen give [−0.44, 1.67].
  - Only real curves with z(t) coupled run away.
- **Cause:** the declared weighting multiplied the WHOLE 2D curve, including the distance prior t², by 1/s_i (Birge) and by q_i (τ-softening; median q = 0.19). The distance prior was thereby weakened to ≈ 0.19 t²/1.4, i.e. e_D inflated ~2.7×. Through the speed–distance coupling u(t) = cz_CMB − H₀(D_SPARC + e_D t), a large β then buys a cheap per-galaxy degree of freedom: each galaxy slides along its a₀–distance valley until the model crosses it. That is an artefact of scaling the prior, not a property of the data.
- **Fix (the statistic's weighting only):** Birge scaling and τ-softening act on the data part at fixed distance, and the distance prior is never scaled:
  - C_eff(x, t) = t² + m(t) + q_i(t) [d(x, t) − m(t)]
  - d = (C − t²)/s_i
  - m(t) = min_x d(x, t)
  - q_i(t) = σ_x(t)²/(σ_x(t)² + τ²), with σ_x(t) the Δ = 1 half-width of d(·, t) − m(t) along x at fixed distance (the Gaussian convolution of the data likelihood with the intrinsic a₀ scatter).
- **What is unchanged:** τ is still the Gaussian ML scatter of the preferred values x̂_i about L₀, using the distance-profiled widths σ_i of min_t [t² + d]; the mocks still draw ε_i ~ N(0, σ_i² + τ²). The variants "no τ" (q = 1) and "no Birge" (s = 1) keep the same structure.
- Everything else (grid, model, nulls, pass lines, MUTATE) is unchanged. Part A is rerun from scratch.

## Addendum 3 (after part A's final run; before part B, i.e. before any β fit on the real speeds)
Part A (`cfg186_a_curves_power.out`) gives a power row of Fisher σ_β = 0.45 and mock σ_β = 2.25, so β_det = 4.5 against the G7 line of 0.10. **The test is NON-DIAGNOSTIC for G7**, as expected. The β = 0 mocks are skewed and biased positive: median β̂ = +1.46, 16–84% [+0.04, +4.54].
- **Where the skew comes from.** Idealised parabolic curves give a nearly symmetric distribution. The skew comes from two sources:
  - the real curves' asymmetry: a galaxy's χ² flattens toward low a₀ (Newtonian) and rises steeply toward high a₀;
  - the concave model log₁₀(1 + βz), bounded below at β ≈ −1/z_max.
  The estimator is therefore biased, and it is **calibrated, not corrected**: p values come from the two nulls, and limits from the Neyman construction with the same estimator.
- **Changes before part B:**
  - The Neyman grid is extended to β_inj ≤ 10: step 0.05 on [−0.90, 1.00], 0.10 on (1.00, 3.00], 0.25 on (3.00, 10.00]. Part A's mocks show a sampling width of ~2–4 at β = 0, so the declared ceiling of 3.00 could be too low.
  - One reported variant is added, **z frozen at the catalogue distance** (no speed–distance coupling in the fit), to show how much the coupling contributes.
  - The failed reported MOCK check stays on record.
  - Nothing else changes.

## Addendum 4 (AFTER part B's first run, kept as `cfg186_b_fit_firstrun.*`; calibration only)
- **First run:**
  - β̂ = +0.89. Bootstrap σ = 0.67. Speed shuffle p = 0.079. Noise injection p = 0.56.
  - Declared Neyman β₉₅ = 1.80. No SIGNAL; G7 NON-DIAGNOSTIC.
- **Two calibration problems surfaced.** Neither touches the primary estimator, the pass lines or the verdict.
  1. **The noise-injection mocks misrepresent the estimator's response on the real curves.**
     - Noiseless injections on the real curves are recovered 1:1: 0.004, 0.309 and 1.031 for β_inj = 0, 0.3 and 1.0.
     - With the declared noise, the mocks give median β̂ = +1.07 at β_inj = 0 and +3.6 at β_inj = 1.
     - The speed shuffle on the real curves is centred: median −0.02, 16–84% ±0.50.
     - Diagnosis: the Gaussian redistribution of preferred values (homoscedastic τ = 0.34 dex) moves each curve's asymmetric shape away from the a₀ where it is physically anchored. The concave model log₁₀(1 + βz) then biases β̂ up, and the bias grows with the noise: median 0.06 / 0.25 / 1.04 at 0.25 / 0.5 / 1.0 × the declared noise.
     - Consequence: the declared Neyman limit (built on those mocks) is anti-conservative.
     - **Added:** a Neyman construction on speed-shuffled real data, with the same grid and 200 trials per value. It uses the real curves and preferred values, with the speeds permuted (destroying any real β) plus the injected shift log₁₀(1 + β_inj z_π(i)(0)). The bootstrap 95th percentile is also reported. **The quoted β₉₅ is the LARGEST of the declared Neyman, the shuffle Neyman and the bootstrap value**, the conservative choice. The declared noise null and its p stay reported as declared.
  2. **W2 and the small subsets sit near the model's pole β → −1/z_max, where the bootstrap σ collapses.** W2 has σ_boot = 0.13, but its own speed shuffle gives p = 0.56 (29% of shuffles reach β < −0.4). **Added:** every reported row carries its own speed-shuffle p (500 permutations) next to its bootstrap σ.

## Addendum 5 (AFTER the MUTATE run; the declared control failure is kept)
- **M1 as declared FAILS:** β̂_mut − β̂_obs = +0.542 against the window [0.24, 0.36]. The MUTATE output keeps rc = 1. The first MUTATE run is kept as `cfg186_b_fit_MUTATE_firstrun.*`.
- **Why the window was wrong.** It assumed the injected β adds to β̂_obs. The model is multiplicative: (1 + β_obs z)(1 + 0.30 z) = 1 + (β_obs + 0.30 + 0.30 β_obs z) z. With β̂_obs = +0.89, and the β leverage carried by the high-z galaxies (z up to ~1.1), the expected shift is 0.30 (1 + β_obs z_eff) ≈ 0.43–0.57, not 0.30.
- **Two reported diagnostics were added to part B's MUTATE branch.** They show the miss is the composition, not the pipeline:
  - **M1b:** the same injection applied at the curve level to the REAL curves moves β̂ by +0.567, against +0.542 from the point-level run.
  - **M1c:** on the MUTATE curves, with the real-data factor (1 + β̂_obs z) held fixed, the extra factor recovers γ = +0.335 against the injected 0.30.
- The noiseless synthetic checks (FIT0 / M0) recover 0.3000 exactly.
