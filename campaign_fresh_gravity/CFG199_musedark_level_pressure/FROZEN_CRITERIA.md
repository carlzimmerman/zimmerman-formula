# CFG199 — MUSE-DARK: is CFG198's a₀ level real? a₀ at R_e from the model's own rotation profile, bracketing the pressure term. FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, before any CFG199 number. **κ = ½ FITTED, NOT DERIVED.**

## Why

CFG198 (e9a92352d) reported against interest that the implied a₀ at z ≈ 0.5 is 0.25–0.65 dex above both footings in every mass route. That level is set by CFG198's own reconstruction: g_obs = D × g_bar, with D = 1/(1 − fDM) from the model and g_bar from a thin exponential disc of mine. Two things in CFG198 make the level suspect:
- In its v22 variant, g_obs from v22 was a median 0.44 of the fDM-route value, where a flat curve would give 0.76.
- The model's circular velocity includes a Dalcanton–Stilp pressure term, inferred (unverified) to be about half of v_c² for many of these galaxies.

The #1 rule applies: verify a fail as hard as a win. This lane replaces my geometry's absolute scale with the model's own rotation profile.

## What was known when this was written

- CFG198's numbers: its sample, levels and slopes, all committed.
- The data chat's notes:
  - `true_Vrot.dat` has 25 slit rows per galaxy: `dx_arcsec`, `rad_Re`, `flux_slit`, `v_kms`, `sig_kms`.
  - The papers' text says v_⊥ is deprojected and instrument-corrected, and v_c² = v_⊥² + v_AD².
  - The file's v against v22 had a median ratio of 0.69 and correlated with sin i (r = 0.57). The data chat first read this as projection, then as v_⊥ before the drift term; neither is established.
- Values I have seen: the ID0003 pilot note (v to ±154 km/s, σ 49 → 38 km/s, v22 149.4, fDM 0.76), from which I computed its fDM-route v_c(R_e) ≈ 151.5 km/s by hand; and the first two rows of ID0011's file (v ≈ 158 km/s at 3.9–4.3 R_e, σ ≈ 29). Nothing else from the 126 files.
- **Hand expectation, disclosed:** CFG198's level comes down, by roughly the v22 discrepancy (~0.24 dex) plus the pressure share. The excess over the footings may shrink to within them. I do not know by how much.

## Inputs

- `data_assembly/musedark_catalogues/musedark_numeric.csv`, the same sample S as CFG198: 109 disc-only galaxies with 0 < fDM < 1.
- The 126 `DC14_<n>_true_Vrot.dat` files, stored outside the repo in `_external_data/muse_dark/numeric/` (a sibling of the repo).
- Each file's sha256 is checked against `data_assembly/musedark_catalogues/numeric_manifest_sha256.txt`. Any mismatch or missing file aborts the run.

## Quantities, per galaxy in S

- **v_f(R_e):** the file's |v_kms| at |rad_Re| = 1, linearly interpolated on each side of the centre and averaged over the two sides.
  - If only one side reaches 1 R_e, that side alone is used. If neither does, the galaxy is excluded and counted.
  - σ_f(R_e) is taken the same way (reported).
- **Two readings of v_f, never pooled:**
  - (a) v_⊥ = v_f: the text reading, deprojected, before the drift term.
  - (b) v_⊥ = v_f / sin i: the projected reading, with i = `incl_deg`.
- **g_⊥ = v_⊥²/R_e.** For a non-negative pressure term this is a lower bound on the model's total at R_e.
- **Route (i), the model's own decomposition:**
  - g_bar,i = (1 − fDM) g_⊥, with D = 1/(1 − fDM).
  - a₀,i = g_bar,i / y*(D), with ν_mono, as in CFG198.
  - With fDM as given, this is a LOWER bound on route (i)'s a₀.
- **Routes (ii) SED + H₂ and (iii) SED stars only:**
  - g_bar,r = g_bar,i × [g_disc(M_r) + g_HI] / [g_disc(M_fit) + g_HI]. These are CFG198's route-to-route baryon ratios, placed on the file's absolute scale.
  - D_r = g_⊥ / g_bar,r and a₀,r = g_bar,r / y*(D_r). They are defined only for D_r > 1.05, as in CFG198.
- **Pressure-plus-geometry share (reported):** s = 1 − g_⊥ / g_obs,CFG198. This mixes the model's pressure term with any scale error in CFG198's disc geometry.

## Decision rows

- **L1, the level (route i, reading a).** Take the median log₁₀ a₀,i in the lowest-z third, using CFG198's z-thirds of the route-(i) galaxies. Its 95% CI comes from 10,000 bootstrap resamples of that third (seed 199).
  - If the CI's lower end is above log₁₀(1.131 × 10⁻¹⁰) (the higher footing): **the level excess survives even the no-pressure lower bound.** This is against interest, and robust.
  - If the CI contains either footing: **the level is consistent with the footings at the lower bound.** CFG198's excess then depends on the pressure term and the geometry.
  - If the CI's upper end is below log₁₀(9.36 × 10⁻¹¹): **below both footings at the lower bound.**
- **L1b.** The same rule for reading (b).
- **L2, slopes (reported).** Recompute b_i, b_ii and Δb (Theil–Sen, 10,000 bootstrap resamples, seed 199), and CFG198's rows R0–R2 with this g_obs, for each reading. Does the CFG198 finding survive: route (i) rises, route (ii) is not significantly rising, and Δb < 0?
- **L3, readings (reported, not graded).** Spearman ρ of v_⊥ / v_c,CFG198 against sin i, for each reading. The weaker |ρ| is noted as the better-supported reading. The share s: median and 16–84%.

## Controls

- **C1:** every `true_Vrot.dat` sha256 matches the manifest.
- **C2, interpolation:** on a synthetic antisymmetric linear profile, v_f(R_e) is recovered to 1e-12.
- **C3, route identity:** with M*_SED := M_fit and μ_mol := 0, routes (ii) and (iii) equal route (i) to 1e-12.
- **MUTATE=1:** v_f → 0.8 v_f. The route-(i) level must shift by 2 log₁₀ 0.8 = −0.1938 ± 0.001 dex, because a₀ ∝ g_⊥ at fixed fDM. Outputs are written separately (`*_MUTATE`).
