# CFG184 — how much of the KURVS outer σ can be beam-smeared rotation, and what pressure-support scale the data then allow. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's request, before any CFG184 number.

## What was known when this was written

- **The data chat's methods note** (093fa9733) and my groundwork agent's read of the paper's TeX and the repo files (read-only):
  - the KURVS σ(R) is the OBSERVED Hα width, corrected only for instrumental broadening;
  - beam smearing is corrected only for σ₀ (within 3.4 R_D); the authors assume it is negligible in the outer disc;
  - seeing is sample-wide: FWHM 0.57″, 1σ spread 0.25″; the PSF shape is not stated;
  - spaxels are 0.1″ (resampled from 0.2″), with adaptive binning from 3×3 to 9×9 (0.3″–0.9″) to S/N ≥ 5; the per-spaxel bin size is not published;
  - the 1D profiles are medians over a ±0.3″ pseudo-slit along the major axis;
  - R_max is 1.9–2.6 FWHM.
- **CFG141's σ_out used the outer three points for 8 of the 10 discs,** spanning about 1.7 kpc. Only KURVS-8 and KURVS-21 are interpolated at R_max.
  - For KURVS-3, 16 and 17 the R_max points are clipped, so σ comes from about 8.4–10.1, 8.3–10.0 and 6.6–8.2 kpc.
  - KURVS-15's three points mix both sides.
  - The smearing is therefore evaluated at the radii CFG141 actually used, not at R_max.
- **The data chat's finding, as relayed** (5e8617c81): the tabulated outer velocity (Table B1 col 3, which CFG140's loader reads as `v_at_last_point_kms`) is the authors' fitted exponential-disc MODEL at R_max, not a data marker.
- **Not read before or in this lane:** the measured V(R) markers (`kurvs_rc_points.csv`). They are reserved for a later frozen re-run with measured outer velocities (proposed as CFG189).
- **Read after this commit, as declared below:** the authors' model curves (`kurvs_rc_model_curves.csv`) and the control file (`kurvs_rc_control_vs_table.csv`).
- **The Girard+2021 result, as relayed by the data chat** (arXiv:2101.04122): molecular σ lower than ionised σ by 2.45 ± 0.38 at z ≈ 0.5–2.5. It enters only as a declared scenario (below).

## The forward model (declared)

- **A thin disc on the sky.** Major axis along x; inclination i; R = √(x² + (y/cos i)²); cos φ = x/R.
  - Line-of-sight velocity: V_los = V(R) sin i cos φ.
  - Hα surface brightness: I ∝ exp(−R/R_d).
- **The intrinsic rotation curve:**
  - PRIMARY: the authors' best-fit exponential-disc model curve (`kurvs_rc_model_curves.csv`), deprojected by sin i_SFR. i_SFR is the inclination the paper used for its velocities. The two sides are folded by |R| (the average of |V| at ±R).
  - VARIANT: a Freeman exponential disc, with R_d = R_eff/1.68, normalised to the tabulated V(R_max).
  - If the authors' model was fitted to the smeared curve without a PSF, treating it as intrinsic under-estimates the inner gradient. In that case σ_bs here is biased LOW (declared).
- **The kernel:**
  - PSF: Gaussian, FWHM 0.57″ (primary), with 0.32″ and 0.82″ (the 1σ spread) as variants.
  - Spaxel bin: a box of 0.3″, 0.6″ (primary) or 0.9″.
  - The profile value at (x_s, 0) is the median over y_s ∈ [−0.3″, +0.3″] of the per-spaxel values (the pseudo-slit).
  - Angular scale from the paper's cosmology (H₀ = 70, Ω_m = 0.3).
- **The smeared dispersion.** For a spaxel, σ_bs² is the intensity- and kernel-weighted variance of V_los:
  - σ_obs² = σ_int² + σ_bs², assuming a Gaussian intrinsic line with σ_int uniform within the kernel (declared approximation);
  - the instrumental width has already been removed by the authors.
- **Evaluation radii:** exactly those CFG141 used per disc (the outer three points, or R_max for KURVS-8 and 21), averaged as CFG141 averaged σ.
- **Hα scale:** R_d = R_eff/1.68 from the stellar R_eff (primary), with × 0.7 and × 1.5 as variants. The Hα profiles are not published.
- **Inclination:** i_SFR (primary), with i* as a variant.

## What is computed

1. **Per disc,** at CFG141's radii: σ_bs, and the fraction f_bs = σ_bs²/σ_out² of the observed outer σ² that beam-smeared rotation can supply. Given for the primary model and as the range over the declared variants.
2. **The pressure-support scale the data allow.**
   - Replacing σ_out by σ_int = √(max(σ_out² − σ_bs², 0)) in the pressure term reduces it by the factor (1 − f_bs).
   - The sample-effective scale s_eff(s) is the uniform s that gives the same Δ′_flat at the decision cell (μ = 0.67, δ = 0, canonical) as the σ_int pipeline at nominal s. It is reported at s = 1 (Kretschmer) and at each placed prescription (1.42, 1.62, 1.69, 3.00).
   - This is given for the primary model and for the maximal-smearing variant (the variant that maximises the sample f_bs), which sets the lower bound on s_eff.
3. **Placement against the laws.** Take P0 (s = 0), s = 1 and the published prescriptions, re-evaluated with σ_int.
   - Report the three laws' decision-cell Δ′ ± σ (z): flat, a₀ ∝ H(z) and a₀ ∝ t(z)/t₀ (CFG175).
   - Report their KURVS break-evens, and their fit points s₀ at μ = 0.67.
   - Compare with CFG162's crossing s_mid = 0.67 and CFG175's fit points (flat 0.39, rival 1.03, T < 0).
   - KROSS is unchanged: its σ₀ is the survey's own, beam-smearing-corrected value. This is declared, not tested.
4. **A declared scenario, reported and not scored:** the pressure-bearing dispersion is the molecular layer's, σ_mol = σ_Hα/2.45 (Girard+2021), so s_eff = s/6.0. Where K21 then lands, and the laws' cells there.
   - Default reading: the Hα velocities need the Hα gas's own pressure support. The molecular scenario is not the default.

## Readings (declared forms)

- **"Beam smearing is minor":** the primary sample f_bs ≤ 0.10, and s_eff(1) ≥ 0.9. K21 stays where CFG162 placed it.
- **"Beam smearing can move K21 across the crossing":** the maximal-smearing variant gives s_eff(1) < 0.67 = s_mid.
- **"Non-diagnostic":** anything in between, reported as the range.
- **Stated plainly:** turbulent pressure support cannot be separated, from these data, from unresolved bulk or non-circular motion or from outflow broadening. A σ_int that survives beam-smearing removal is an upper bound on the pressure-bearing dispersion, not a measurement of it.

## Controls and MUTATE

- **C1:** reproduce CFG141's σ_out per disc from the σ-profile file (exact).
- **C2:** with a flat V(R) at i = 0 (face-on), σ_bs = 0 to 10⁻⁶ km/s.
- **C3:** σ_bs → 0 as FWHM → 0 and bin → 0.1″ with a flat V(R), to 0.5 km/s.
- **C4:** with σ_int = σ_out (no smearing removed), the pipeline reproduces CFG160's decision cell (+0.1441 / −0.0060) and CFG175's T cell (+0.3227), to 10⁻⁴.
- **MUTATE=1:** FWHM × 3. The primary f_bs must rise and s_eff(1) must fall.
- **MUTATE=2:** FWHM → 0.01″ and bin → 0.1″. f_bs → about 0 and s_eff(1) → about 1, so the headline must change if the main run finds any non-negligible smearing.
- Each MUTATE run exits 0 when its direction holds.

## Untested (declared)

- the Hα surface-brightness profile;
- the PSF shape;
- the per-spaxel bin size;
- disc thickness;
- non-circular motions;
- the model-velocity provenance of the tabulated outer V (the CFG189 re-run with measured markers addresses it);
- the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.
