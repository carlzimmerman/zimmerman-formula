# CFG666 FROZEN CRITERIA: the dark-energy clock (cold energy settles at the cosmic rate toward a de Sitter-scale law)

Date: 2026-10-12. Written and committed ALONE, before any CFG666 code or score. Block CFG660–669. Nothing below may be edited
after this commit. **This is a hypothesis born from a numerical coincidence; the record has been burned by dS-scale numerology
before (memory: "never cite dS-Unruh for κ = ½"; the 2π/Z coincidence). It must pass knob-free tests before anything is claimed.**

κ is fitted on the record (κ_eff = ½ canonical; 0.604 alt). Footings never pooled. The cold energy's mass is required. No particle
species. Not "theory closed". Nothing will be phrased as "the data favour the framework". Raw data only.

## 0. What has been seen (stated before any choice below)

- The anomalies motivating it: CFG623 (mergers allow only α = 0), CFG700 (old early types ×1.46 raw ESD vs young at fixed M*),
  CFG531 (KiDS late types below the law), the record's high-z lanes (s* floors, calibration-limited), CFG534 (SPARC early-type outer
  excess +0.071 dex, shuffle-calibrated ~2.1σ).
- The record excludes κ = √(8π/3) = 2.894 (de Sitter surface gravity) **as the directly measured κ**, by 5.8× (memory: P2).
- **The coincidence (computed by hand, no data fit):** if a_true = c·H_Λ (κ_true = √(8π/3)) and the settled fraction is
  f = 1 − e^(−H_Λ t) with H_Λ = H₀√Ω_Λ (H₀ = 67.4, Ω_Λ = 0.685; 1/H_Λ = 17.53 Gyr), the deep regime gives V⁴ = f² G M_b a_true,
  i.e. a₀,eff = f² a_true. κ_eff = ½ needs f = 0.4157, t = 9.42 Gyr; κ_eff = 0.604 (alt) needs f = 0.457, t = 10.7 Gyr.
- **Hand estimate of the shape (before any score):** ν_eff exceeds ν_mono(g_N/a₀,eff) by about +0.03 / +0.06 / +0.04 dex at
  y_eff = 0.1 / 1 / 10. Expectation: the shape test is at risk.
- No colour → age mapping exists on the record (CFG588/589 fit slopes only), so no KiDS amplitude test is frozen here.

## 1. The model (all choices frozen now)

- True scale a_true = c·H_Λ = c·H₀√Ω_Λ.
- Settling at the cosmic rate H_Λ toward the law's phantom at a_true, uniformly in radius: the settled phantom fraction is
  f(t_b) = 1 − exp(−H_Λ t_b), with t_b the time since the system became bound.
- Effective law for a population with typical f̄: g = g_N · ν_eff, ν_eff = 1 + f̄ [ν_mono(g_N/a_true) − 1].
- f̄ is NOT fitted: f̄ = √(κ_eff/κ_true) per footing (0.4157 canonical, 0.4568 alt), which reproduces each footing's measured a₀ in
  the deep limit exactly. The test is therefore of the SHAPE, with no free parameter.

## 2. Checks

- **C1 (arithmetic):** f̄ and the implied t_b per footing, reproduced to 1e-4.
- **D1 (primary, raw SPARC, the record's CFG4 harness, Υ = 0.61, all good points):** weighted rms of log g_obs − log g_pred for
  the clock model vs the law (ν_mono at a₀,eff), per footing; mean signed residual; rms in g_bar bins (> 1e-10, 1e-11..1e-10,
  < 1e-11).
  - **SHAPE ALLOWED** if rms_clock ≤ rms_law + 0.01 on both footings and |mean residual_clock| ≤ 0.03 dex;
  - **SHAPE DISFAVOURED** if rms_clock ≥ rms_law + 0.03 on either footing or |mean residual_clock| > 0.06 dex;
  - **SHAPE TENSION** otherwise.
- **D2 (reported, sign only):** SPARC early (Hubble T ≤ 2) vs late (T ≥ 7) discs: the clock predicts a LARGER outer boost
  (g_bar < 1e-11) for the older (earlier-type) group at fixed g_bar. Report the mean outer residual difference against the law;
  no verdict weight (CFG534 already saw +0.071 dex for early types).
- **C2 (mergers, deterministic):** α_eff = H_Λ τ_ff for cluster cores (τ_ff = 0.1–0.5 Gyr) must lie below CFG623's first excluded
  node (0.1); reported against the allowed set {0}.
- **MUTATE (`CFG666_MUTATE=1`, exit 1 iff both bite):** M1, f̄ = 1 (no dilution, a_true as the law's scale): D1 rms must rise by
  ≥ 0.1 dex (the excluded κ = 2.894); M2, f̄ doubled: mean residual must move by ≥ 0.1 dex.

## 3. What a pass would and would not mean

A SHAPE ALLOWED result means only that the clock's interpolation is not excluded by SPARC; it would not establish the clock. The
decisive tests come after: a KiDS old/young amplitude test with a colour → age mapping declared from an external stellar-population
table before any fit, and a high-z test (a₀,eff falls steeply with redshift: f at t_b = 2 Gyr is 0.108, so κ_eff(z ≈ 2) ≈ 0.03).
A SHAPE DISFAVOURED result closes the clock in this form.

## 4. Machine rules

Light: one process, `nice -n 10`; allowed while the 1024³ run is live.
