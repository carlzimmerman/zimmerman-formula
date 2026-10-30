# GH4_tsz_two_halo_compensated: FROZEN CRITERIA (committed alone, before any y-map pixel is read for this lane)

**Question.** GH3 (4cba03defe) stacked ACT DR6.02 NILC Compton-y on the 88k KiDS isolated lenses in bins 3–4. On the
CIB-deprojected map it came out NOT DECIDED: gas to 3 R_vir had χ² 4.7, gas to R_vir had 8.7, Δχ² = 4.0 exactly at
threshold. That lean was unprotected against two effects:
- the two-halo tSZ from neighbouring structure, which mimics extended gas;
- large-scale offsets, such as the uniform −1.1e-7 seen in GH3's z ≤ 0.25 deprojected stack.

**Does the extended-gas lean survive** once those are handled by (i) a compensated aperture and (ii) an empirical,
data-built two-halo template with a free non-negative amplitude?

## Data (as GH3; nothing new fetched)

- **Maps:** ACT DR6.02 NILC y strips in `_external_data/act_dr6_nilc/`.
  - PRIMARY: CIB-deprojected (`ComptonY_deproj_cib_1.0_10.7`). GH3 showed the standard map is CIB-dominated
    (CIB-SENSITIVE).
  - Reported: the standard ILC.
- **Geometry and beam:** as GH3 (CAR 0.5′, 1.6′ Gaussian).
- **Lenses:** the KiDS isolated sample (`lr_lenses.npz`), bins 3–4 (log M★,70 10.6–11.0) = PRIMARY. A lens is used only
  if its ±40′ stamp is finite and non-zero, and only if 20 R_vir fits inside 39′.
  - Reported, ungraded: bins 1–2 (log M★,70 8.5–10.6, 92,570 lenses). Zhang+24 has no hot-CGM measurement there, so
    there is no gas model. Their compensated stack is reported as a check on the two-halo amplitude.
- **Two-halo tracer:** the KiDS DR4 bright sample on disk (`KiDS_DR4_brightsample.fits` + `_LePhare.fits`, IDs
  matched). Use galaxies with `masked == 0` and MASS_MED > 0.

## Measurement

- **Annuli:** x = R/R_vir edges [0, 0.5, 1, 1.8, 3, 5, 8, 12, 20]. R_vir from Zhang Table 1 (log M★ 9–11.5 rows,
  interpolated, flat outside). Native D_A as GH3.
- **Compensated aperture (PRIMARY data vector):** per lens, the mean y in [12, 20) is subtracted from each of the
  seven inner annuli. The same operation is applied to every model and to the template, giving 7 data points. Randoms
  (3 per lens, as GH3) are subtracted after compensation.
- **Covariance:** 50 jackknife patches (equal-count RA slices), Hartlap-corrected.

## Two-halo template (empirical; no ΛCDM power spectrum, no halo model)

- **Recipe:** for each lens, count bright-sample neighbours with |z_ph − z_lens| < 0.06 and M★,nb > 0.1 M★,lens (the
  massive neighbours that carry the pressure) in the same x annuli. Self-matches within 2″ are excluded.
- **Subtraction:** the identical count around the 3 random positions per lens (lens z and lm carried) is subtracted,
  giving an excess surface density of neighbours per annulus.
- **PRIMARY template T_n:** number-weighted.
- **Systematic template T_m:** each neighbour weighted by (M★,nb / M★,lens)^{5/3}, as a pressure proxy.
- The template is compensated in the same way as the data, and stacked over lenses with the same weights.
- It is a SHAPE only: its amplitude b ≥ 0 is free in every fit. It is not beam-convolved, because it is smooth on
  scales ≳ 1′ by construction of the isolation hole; that is checked by reporting T.

## Predictions

- **Gas:** Zhang's MW-mass gas as GH3 (β 0.43, r_c 6 kpc, M_hot(<R_vir) = 1.84 M★, 0.22 keV, μ_e 1.14), cut at
  k = 1, 1.8, 3 R_vir.
- **Processing:** beam-convolved on the 0.05′ grid (now to 40′), averaged over the same annuli per (z, lm) cell, then
  compensated.
- **PRIMARY fit:** model = gas(k) at A = 1 (no free gas amplitude) + b·T_n with b ≥ 0 free. χ² has 6 dof.

## Verdict (frozen; PRIMARY = CIB-deprojected, bins 3–4, T_n)

- **EXTENDED GAS PREFERRED:** χ²(k = 3) < χ²(k = 1) − 4 and p(k = 3) > 0.01.
- **MEASURED EXTENT PREFERRED:** χ²(k = 1) < χ²(k = 3) − 4 and p(k = 1) > 0.01.
- **NEITHER FITS:** p < 0.01 for all k.
- **NOT DECIDED:** otherwise.

**Reported:**
- the fit with b ≡ 0 (compensation only);
- the T_m template;
- the standard ILC map;
- free gas amplitude A per k, with b free;
- the bins 1–2 stack, fit by b·T_n alone (no gas model);
- the uncompensated 8-annulus profile, for comparison with GH3.

**Interpretation lock:** an EXTENDED verdict here is a necessary condition for route E's KiDS lensing need (GH2
k* ≈ 1.8). It does not show route E beats the law, which GH2 found fits KiDS better at its measured-gas best.

## Checks

- **K1:** GH3's K1 (β = 2/3 projection closed form within 1e-4).
- **K2:** GH4's stacking code run with GH3's stamp (±12′), annuli and validity rule reproduces GH3's committed
  CIB-deprojected Y within 1e-6 relative. Same lenses, randoms and seed.
- **K3:** pixel geometry vs astropy WCS within 0.01 px.
- **K4:** the template recipe applied to random positions treated as lenses gives an excess consistent with zero
  (|T|/σ < 3 in every annulus).
- **MUTATE:** random positions stacked as lenses give a compensated y profile consistent with zero (p > 0.01).

**Scope.**
- The template is a tracer shape, not a predicted amplitude; b absorbs bias and pressure weighting.
- If the two-halo signal has a shape unlike massive-neighbour counts, it is not fully removed. The compensated aperture
  limits this to gradients across 0–12 R_vir.
- κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed;
  nothing here says the data favour the framework.
- Compute: one thread, nice 15, RSS < 2 GB, strip read in chunks.
