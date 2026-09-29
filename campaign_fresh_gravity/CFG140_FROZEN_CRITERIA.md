# CFG140 — a₀ at z ≈ 1.4 from KURVS-CDFS's outermost measured rotation points: flat a₀ against a₀ ∝ H(z). FROZEN CRITERIA

Written 2026-09-29, before any acceleration, g_obs, g_bar or offset number of this lane. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. The orchestrator approved the lane and assigned the number.

## Why

The adopted STANDING names a₀ at z ≈ 2.5 as one of the two decisive tests; B predicts a flat a₀. CFG52, CFG54 and CFG99 found no usable disc on disk.

KURVS-CDFS (Puglisi et al. 2023, arXiv:2305.04382) is the first on-disk z > 1 sample whose outermost observed rotation points plausibly reach low accelerations. That is the data chat's rough arithmetic, which is NOT used here.

**Stated up front:**
- **The gas is unmeasured.** It enters as a declared bracket, not as data.
- **V²/R at the last point is a rough surrogate for g_obs.**
- **CFG52's correlated mass-scale systematic caps any such test near 2.3σ** against a₀ ∝ H(z).
- **A non-diagnostic answer is valid.**

## Data (in the repo; nothing fetched)

- **KURVS-CDFS**, `data_assembly/arxiv_tables/kurvs2023_{integrated,kinematics,velocities_at_radii,fdm}.csv`, with definitions per `KURVS_DEFINITIONS_NOTE.md`:
  - z_Hα, log M* (MAGPHYS), R_eff, σ₀ (with error);
  - R_max, the maximal extent of the observed curve (kpc);
  - v_last, the inclination-corrected OBSERVED velocity at R_max (with error).
  - The R'_3D and R'_6D velocities are read off the paper's exponential-disc model fit, so they are a reported variant only.
- **The z = 0 same-pipeline anchor: SPARC** (Lelli et al. 2016): `real_research/data/SPARC_Lelli2016c.mrt` and `real_research/data/sparc_data/*_rotmod.dat`.
- **The z ≈ 0.9 same-instrument control: KROSS V2** (Harrison et al. 2017), `data_assembly/high_z_tf_tables/kross_v2.csv`.
- **The kernel and a₀:** `CFG4_common` (ν_mono, the framework's committed kernel; A0 canonical and alt), imported read-only.

## Selection (declared before any number)

- **KURVS, primary:** the 10 galaxies the paper classes as rotation-supported, the rows of `kurvs2023_fdm.csv` (IDs 3, 7, 8, 9, 11, 13, 15, 16, 17, 21).
- **KURVS, variant:** every one of the 22 with v/σ₀ ≥ 1.
- **SPARC anchor:** quality Q ≤ 2, inclination ≥ 30°, log M* ≥ 9.5 with M* = 0.5 L[3.6]; the last rotmod point is used.
- **KROSS control:** kin_type RT or RT+, v/σ₀ ≥ 1 (with v the intrinsic velocity at 2 R_1/2), and finite M*, r_im and σ₀.

## The one pipeline, applied identically to all three samples

- **Radius R:**
  - KURVS: R_max, with v_last;
  - SPARC: the last point, with its V_obs;
  - KROSS: 2 R_1/2 (2 r_im), with the intrinsic vC.
- **Disc scale R_d:** R_eff/1.68 for KURVS, the tabulated R_disk for SPARC, r_im/1.68 for KROSS.
- **Pressure support, two variants carried in EVERY result:**
  - P0: V_c = V_obs.
  - P1: V_c² = V_obs² + 2σ₀²(R/R_d), the Burkert et al. (2010) exponential disc with constant σ₀.
  - σ₀ is tabulated for KURVS and KROSS. For SPARC it is a declared 10 km s⁻¹, since SPARC has no σ column.
- **g_obs** = V_c²/R, the spherical surrogate.
- **Baryons:**
  - M_b(<R) = M*(<R) + M_gas(<R). Each component is a thin exponential disc's enclosed mass, M(<R) = M[1 − e^(−y)(1 + y)], with the spherical shortcut g_bar = G M_b(<R)/R².
  - Stars use y = R/R_d. Gas uses y = R/(2R_d), so it is more extended.
  - M* is MAGPHYS for KURVS, 0.5 L[3.6] for SPARC, and mstar for KROSS.
- **Gas bracket, unmeasured for KURVS and KROSS:** μ = M_gas/M* ∈ {0.25, 0.67, 1.5, 4}.
  - 0.67 is the paper's own 40% molecular fraction (Tacconi et al. 2020); 0.25 is a low molecular case.
  - 1.5 and 4 add HI, up to the stacked z ≈ 1 M_HI ≈ 4 M* noted in the Sharma et al. 2024 table.
  - SPARC uses its measured gas (1.33 M_HI) in the same radial model, and the μ bracket as a reported variant.
- **Coherent stellar-mass bracket:** δ ∈ {−0.2, 0, +0.2} dex, applied to a whole sample.
- **Predictions:** g_pred = ν_mono(g_bar/a) g_bar.
  - Flat: a = a₀.
  - The rival: a = a₀ E(z), with E(z) = √(Ω_m(1+z)³ + Ω_Λ), Ω_m = 0.315.
  - Both a₀ footings (9.36e-11, 1.13e-10) are carried.
- **The common observable:** Δ = log10 g_obs − log10 g_pred.

## Per-object error model (declared)

Added in quadrature:
- **Velocity:** (2/ln10) e_V/V, and under P1 the σ₀ error propagated.
- **Random per-object stellar mass:** 0.15 dex (KURVS, KROSS) or 0.10 dex (SPARC), times the local slope d log g_pred/d log g_bar.
- **Inclination:** a declared ±5° for KURVS, since none is tabulated; SPARC's tabulated e_Inc; KROSS ±5°. It enters through V ∝ 1/sin i.

The pooled value is the inverse-variance weighted mean over objects. If χ²/dof > 1 about that mean, the error is inflated by √(χ²/dof), as declared.

## Checks

- **C1 CONTROL:** the SPARC anchor (measured gas, P0, δ = 0, canonical) has a median Δ_flat within ±0.10 dex of zero. The anchor offset per cell is used below whatever it is; if C1 fails, it is reported and kept.
- **C2 CONTROL:** ν_mono reproduces its two limits to 1e-6: g_pred → g_bar at y = 10⁴, and g_pred → √(g_bar a) at y = 10⁻⁴.
- **C3 CONTROL:** the 10 selected KURVS IDs are exactly the f_DM rows, and every value used is finite.
- **R0 POWER** (printed before any g_obs or Δ). Per bracket cell, the pooled expected separation log g_pred,H − log g_pred,flat (baryons only) divided by the pooled per-object error. The error is evaluated with V replaced by the flat prediction's V, so no observed velocity enters. Also printed: the number of KURVS objects with g_bar < a₀ at R.
- **H0 (feasibility; load-bearing):** in the central cell (μ = 0.67, δ = 0, P1, canonical) the expected separation is ≥ 2σ. If it fails, the lane reads NON-DIAGNOSTIC and H1 and H2 are reported only.
- **H1 [HEADLINE; MUTATE must change it]:** the framework's flat a₀ is NOT disfavoured by KURVS. It is false only if the anchor-corrected Δ′_flat = Δ_flat(KURVS) − Δ_flat(SPARC anchor, measured gas, same P and δ) exceeds +2σ in EVERY cell of the grid (4 μ × 3 δ × 2 P × 2 footings).
- **H2 (reported verdict):** the rival a₀ ∝ H(z) is disfavoured: the anchor-corrected Δ′_H < −2σ in every cell.

## Reported rows

- **R1:** the full grid of pooled Δ_flat, Δ_H and their anchor-corrected versions for KURVS; the anchor's Δ per cell; the cells favouring each reading.
- **R2:** per KURVS galaxy, g_bar/a₀ at R per cell, and Δ_flat and Δ_H in the central cell.
- **R3:** KROSS (z ≈ 0.9) through the same pipeline: pooled Δ per cell. Also the differential Δ(KURVS) − Δ(KROSS) against each reading's predicted differential (flat 0; the rival from the E(z) ratio at the two samples' median redshifts).
- **R4:** the all-22 v/σ₀ ≥ 1 variant.
- **R5:** the R'_6D model-extrapolated velocities as a variant, with R'_6D ≈ 6 R_eff/1.68 and no seeing term (declared as rough).
- **R6:** SPARC with the μ bracket instead of its measured gas: what the bracket does where a₀ is known.

## Kill lines and readings (declared)

- **The framework (flat a₀) is disfavoured** if the anchor-corrected Δ′_flat > +2σ in every cell, and killed at > +3σ in every cell.
- **The rival is disfavoured** if Δ′_H < −2σ in every cell, and killed at < −3σ in every cell.
- **Otherwise:** NON-DIAGNOSTIC over the declared brackets, and the reading lists which cells favour which reading.
- **H0 FAIL:** NON-DIAGNOSTIC. The test lacks the power to separate the readings even before the brackets.
- **What would settle it:** a measured cold-gas mass for these galaxies, and a pressure-support-free tracer at R_max.

## MUTATE

MUTATE=1 multiplies every KURVS v_last by 10^0.3 (g_obs × 4). The anchor-corrected Δ′_flat must then exceed +2σ in every cell, so H1 fails and the script exits 1.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
