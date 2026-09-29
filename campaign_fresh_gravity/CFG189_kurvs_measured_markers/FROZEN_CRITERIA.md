# CFG189 — the KURVS a₀(z) test re-run with the MEASURED outer rotation markers in place of the model velocity, for three laws. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any value in `kurvs_rc_points.csv` was read. Only its README (column meanings) and the control file (model against table) have been read.

## Forking paths (stated first)

- **Every earlier KURVS lane used the paper's Table B1 col 3,** which is the authors' fitted Freeman-disc model at R_max, not a measured point (the provenance correction 27bcce5a4). The model-velocity results are known:
  - the decision cell, flat +0.144 and rival −0.006;
  - CFG175's T at +0.323;
  - the break-evens and fit points;
  - CFG184's beam-smearing fractions.
- **One earlier glimpse of the markers, disclosed:** my groundwork agent's indicative, unreconciled probe of the figure geometry found the outermost plotted points differ from V sin i_SFR by −15% to +10% across seven discs.
- **Hand expectation:** the pooled Δ′ moves by a few hundredths of a dex, in either direction. Whatever the numbers show is reported.

## The outer point (declared)

- **PRIMARY: the farthest measured point.**
  - On each side, find the outermost UNCLIPPED marker (largest |R|).
  - The disc's outer point is the one on the side that reaches the larger |R|, at radius R_out.
  - V_out = |v_obs|/sin i_SFR. Its error is the mean of the plotted up and down bars, divided by sin i_SFR.
  - This is the measured analogue of "the velocity at the maximal extent".
- **Variants (reported):**
  - V-a, outer three: the error-weighted mean of the outermost three unclipped markers on the farther side, at their weighted-mean radius. It mirrors CFG141's σ treatment and smooths correlated neighbouring points.
  - V-b, both sides: the average of |v| on the two sides, interpolated at the shorter side's outermost unclipped radius. This cancels any residual centring or systemic offset, at a smaller radius.
  - V-c, clipped included: the primary, with the 18 clipped markers allowed.
  - V-d, i*: the primary, deprojected with inc_star_deg instead of inc_sfr_deg.
- **Clipped markers:** the authors clipped them for sky lines or broad components. They are EXCLUDED in the primary and in V-a, V-b and V-d; included only in V-c.
- **σ at the same radius and side:**
  - interpolated from the unclipped σ-profile points on that side at R_out, with its error from the plotted bars;
  - if R_out lies beyond that side's σ points, the outermost σ point on that side is used;
  - for V-b, the average of the two sides at the common radius.
- **Inclination error:** ±5°, as before, now around i_SFR (i* for V-d).
- **Everything else is unchanged from CFG141/CFG160:** M*, the gas at μ, R_d = R_eff/1.68, z, the SPARC anchor, δ = 0, the canonical footing, Kretschmer's α with x = R_out/R_eff − 1 and the s-axis {0, 1, 1.42, 1.62, 1.69, 3.00}.

## Beam smearing (tie to CFG184)

- The markers are observed line-of-sight values, NOT corrected for beam smearing.
- **The primary uses the observed σ,** as CFG141/160 did.
- **Variant BS:** σ_int = σ√(1 − f_bs), with f_bs from CFG184's primary forward model evaluated at R_out on the same side (CFG184's functions, exec'd read-only).
- The small beam-smearing bias of V itself at R ≥ 2 FWHM is not corrected (declared).

## The laws, and what is computed

- **Laws:** flat; a₀ ∝ H(z) (the rival); a₀ ∝ t(z)/t₀ (T, CFG175).
- **Computed:**
  1. A per-disc table: R_max against R_out, the model V (table) against the measured V_out, and σ at R_out against CFG141's σ_out.
  2. The decision cell (μ = 0.67, s = 1) and P0 (s = 0) for the three laws: Δ′ ± σ and z.
     - CFG160's lean class at the decision cell: lean flat, lean rival, both or neither.
     - The shift of each law's Δ′ from the model-velocity value.
  3. The break-evens μ_be (1σ) per law at each placed s; CFG175's gas status against the ceiling of 3.47; the fit points s₀ at μ = 0.67.
  4. The same for every variant, reported.
- **HEADLINE (declared form):**
  - "UNCHANGED" if the lean class at the decision cell equals the model-velocity class (lean rival), and every law's z moves by less than 1.
  - "CHANGED" otherwise, stating how.
  - Stated in the primary, and in how many of the variants the class matches.

## Controls and MUTATE

- **C1:** with V set to the table's col 3 at R_max and σ to CFG141's σ_out, the pipeline reproduces CFG160's cell (+0.1441 / −0.0060) and CFG175's T cell (+0.3227), to 10⁻⁴.
- **C2:** the marker radii used match the σ-profile radii within 0.02 kpc wherever both exist.
- **MUTATE=1:** the measured V × 10^0.3. The decision-cell class must change from the main run's. Exits 0 when it does.

## Readings (declared)

- **This replaces a model value by a measured one.** It does not remove the pressure, gas or calibration dependences found in CFG160–168, 170, 175 and 184.
- **Untested:**
  - the beam-smearing bias of V;
  - correlated neighbouring points;
  - the centring for the one-sided variants;
  - non-circular motions;
  - the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.
