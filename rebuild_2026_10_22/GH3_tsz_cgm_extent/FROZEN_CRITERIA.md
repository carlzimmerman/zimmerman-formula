# GH3_tsz_cgm_extent: FROZEN CRITERIA (committed alone, before any y-map pixel is read)

**Question.** GH2 found that on KiDS isolated lenses, the lensing preference flips from the isolated law to route E
when the hot CGM extends beyond k* ≈ 1.8 R_vir. Zhang+24 detect it only to R_vir, the measured case, where the law wins
by +372.

**Does the hot gas around these same lenses extend past R_vir?** Measure the stacked thermal-SZ Compton-y around them
with ACT DR6, and compare with beam-convolved predictions for the gas cut at k = 1, 1.8 and 3 R_vir.

## Data (fetched 2026-10-29 with the owner's OK)

- **Maps:** ACT DR6.02 needlet-ILC Compton-y, `act-planck_dr6.02_nilc_ComptonY.fits` (PRIMARY), and the
  CIB-deprojected `..._ComptonY_deproj_cib_1.0_10.7.fits` (systematic). From LAMBDA, via byte ranges.
  - Only rows 3239–8040 (Dec −36° to +4°) are taken, as raw big-endian float32 strips with their 2880-byte headers.
  - Location: `_external_data/act_dr6_nilc/` (geometry and sha256 logged).
- **Geometry:** CAR at 0.5′; col0 = 21600 − 120·RA (RA wrapped to ±180°); row0 = 7559.5 + 120·Dec.
- **Beam:** 1.6′ FWHM Gaussian (LAMBDA info page).
- **Lenses:** the KiDS isolated sample of X53/F2/GH2 (`real_research/data/lensing_rar/lr_lenses.npz`), bins 3–4
  (log M★,70 10.6–11.0; 88,861 lenses).
  - PRIMARY: all of them.
  - Reported: z ≤ 0.25 (7,440 lenses) and GAMA G09 centrals bins 3–4 (GH1/X75 hosts).
  - A lens is used only if its ±12′ stamp is finite and non-zero; zero marks outside the footprint.

## Measurement

- **Stack:** the y-map is stacked in annuli of x = R/R_vir per lens: [0, 0.5), [0.5, 1), [1, 1.8), [1.8, 3), [3, 5).
  - R_vir(lm) is Zhang's Table 1, interpolated in log M★ (flat outside).
  - Angular radii use native D_A (h 0.679, Ω_m 0.3085).
- **Background:** the same stack on 3 random positions per lens (same z and lm, uniform over each lens's 1° box with
  non-zero map) is subtracted.
- **Covariance:** 30 jackknife patches (equal-count RA slices), Hartlap-corrected.

## Predictions (no free parameter in PRIMARY)

- **Gas:** Zhang+24 MW-mass hot gas, ρ ∝ [1 + (r/r_c)²]^{−3β/2} with β 0.43 and r_c 6 kpc, normalised to
  M_hot(<R_vir) = 1.84 M★ and cut at k R_vir.
- **Pressure:** isothermal at T = 0.22 keV (Zhang's T_vir), with μ_e = 1.14.
- **Signal:** y(R) = (σ_T / m_e c²) ∫ n_e kT dl, converted to angle with native D_A and convolved with the 1.6′ beam.
- **Stacking:** averaged over the same annuli. Lenses are grouped on a (z, lm) grid with Δz = 0.025 and Δlm = 0.1.
- **k grid:** 1, 1.8, 3.

## Verdict (frozen)

χ² over the five annuli (jackknife covariance) for each k:
- **EXTENDED GAS PREFERRED:** χ²(k = 3) < χ²(k = 1) − 4 and p(k = 3) > 0.01.
- **MEASURED EXTENT PREFERRED:** χ²(k = 1) < χ²(k = 3) − 4 and p(k = 1) > 0.01.
- **NEITHER FITS:** p < 0.01 for all k.
- **NOT DECIDED:** otherwise.

**Reported:**
- free-amplitude fits per k: a shape-only test, which absorbs T and normalisation;
- the CIB-deprojected map (CIB-SENSITIVE if the class differs);
- the z ≤ 0.25 subset and the G09 centrals;
- the raw stacked profile and the random-stack profile.

## Checks

- **K1:** the projection integral reproduces the β = 2/3 closed form within 1e-4.
- **K2:** a synthetic point source of known Y injected into a blank copy of the strip, then stacked, returns its beam
  profile and Y within 2 %.
- **K3:** the pixel geometry maps the strip's own header CRPIX/CDELT back to (RA, Dec) within 0.01 pixel.
- **MUTATE:** random positions treated as lenses must give a stacked profile consistent with zero (p > 0.01).

**Scope.**
- The two-halo tSZ from correlated large-scale structure is not modelled. It adds to the outer annuli and would favour
  "extended" spuriously, so the verdict is conservative only against MEASURED EXTENT.
- Residual CIB is checked with the deprojected map.
- κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed;
  nothing here says the data favour the framework. One thread, nice 15, RSS < 1 GB (the strips are memory-mapped).
