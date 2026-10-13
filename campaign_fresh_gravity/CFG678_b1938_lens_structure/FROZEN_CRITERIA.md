# CFG678 FROZEN CRITERIA: blind predictions for B1938+666's own mass structure (sealed while the stage-2 fit is running)

Date: 2026-10-12. Block CFG670–679. Committed ALONE while CFG674 Part 4 stage 2 (PyAutoLens: PowerLaw + shear + m=3,4 multipoles
+ adaptive Delaunay source on GO 8281 F115W) is running and **before any stage-2 number is read**. Seen: stage 1 only (light:
two Sérsics; mass: PowerLaw θE 0.443″, slope at its 1.5 prior edge, q from ell_comps (−0.081, −0.026); shear γ ≈ 0.048).
κ = ½ FITTED; footings separate; cold energy mass required; no particle species; not "theory closed".

## Predictions (computed from the stage-1 LIGHT only + the law; no mass information except θE for normalisation)
- P1 slope: stars = the two stage-1 Sérsics (shapes fixed, one M/L), deprojected spherically (circularised R), baryonic field g_N(r),
  law g = ν_mono(g_N/a0) g_N, total 3D mass, projected; M/L set so the projected mass inside θE = Σ_cr π θE² (Planck18 distances
  z_l 0.881, z_s 2.059; the framework's background = ΛCDM's at percent level). Predicted γ_eff = 1 − dlnκ/dlnR at θE (ρ ∝ r^−γ
  convention, 2 = isothermal), and also the mass-weighted slope over 0.5–1.5 θE. Both footings; gas neglected (stated).
- P2 alignment: mass position angle = light position angle (luminosity-weighted of the two Sérsics) within the stated tolerance
  |Δφ| ≤ 10° if the light axis ratio q_L ≤ 0.9; mass axis ratio q_M ∈ [q_L, q_L + 0.1] (the phantom is slightly rounder; at
  g/a0 ≳ 10 it is ≲ 10 % of the mass). If q_L > 0.9 the PA test is NOT DIAGNOSTIC.
- P3 multipole: the m=4 mass multipole amplitude ≤ 0.02 θE-normalised unless the light shows a comparable a4 (stage-1 Sérsics carry
  no a4, so the prediction is "small"); m=3 small (≤ 0.02).
- g/a0 at θE is reported (sanity: the framework's prediction is Newtonian-dominated there).

## Scoring (applied to the stage-2 maximum-likelihood + posterior, once available)
- P1 CONSISTENT if |γ_meas − γ_pred| ≤ max(2σ_meas, 0.10); TENSION ≤ 0.25; INCONSISTENT beyond. NOT DIAGNOSTIC if the stage-2 slope
  posterior sits on a prior edge.
- P2/P3 CONSISTENT / INCONSISTENT by the tolerances above, with 2σ from the posterior. External shear is a separate component and
  is not counted as misalignment.
- Context only: ΛCDM halos allow misalignment and slopes near 2 from bulge–halo conspiracy; not scored.
Seal: `cfg678_predictions.json`, sha256 in `cfg678_PREDICTIONS_HASH.txt`. MUTATE (`CFG678_MUTATE=1`): a0 → 0 (pure stars) must
change γ_pred by > 0.05 (exit 1 iff it bites).
