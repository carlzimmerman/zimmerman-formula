# ECLIPSE DR1 key catalogue (v20261103)

Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) D: photometric redshifts and physical
properties of the lens galaxies of the Euclid DR1 galaxy-scale strong lenses.

This is the **key catalogue**: identifiers, positions, photometric redshifts, the main physical properties,
Galactic E(B-V), lens-model values, inspection results and the selection flags. The full catalogue
(`eclipse_dr1_catalogue_v20261103.fits`) has the same rows and adds every Prospector parameter, rest-frame UVJ colours,
fit diagnostics and the individual vote counts.

Version: v20261103. Rows: 15,072 (all grade A and B lenses of the Euclid DR1 strong-lens catalogue, one row per lens).
Columns: 77. Formats: FITS binary table (`eclipse_dr1_catalogue_key_v20261103.fits`) and CSV (`eclipse_dr1_catalogue_key_v20261103.csv`), identical content.

## How the values were derived

1. **Deblended lens photometry.** The lens light was separated from the lensed source with Sersic models fitted to the
   VIS image with PyAutoLens; the Sersic structural parameters were then held fixed and applied to all Euclid
   (VIS, Y, J, H) and ground-based bands (e.g. DECam, HSC, CFHT MegaCam, Pan-STARRS). Photometric errors are the MER
   4 x FWHM aperture errors plus an empirical lens-modelling term added in quadrature.
2. **Photometric redshifts** with Phosphoros (COSMOS-based template library, luminosity prior), from the lens flux in
   4 x FWHM apertures. The photo-z is the median of the zPDF.
3. **Physical properties** with Prospector (FSPS with MILES + MIST, Salpeter IMF, 8-bin non-parametric continuity SFH,
   Charlot & Fall two-component dust with a free Kriek & Conroy slope, dynesty sampling) from the total lens flux,
   with the redshift fixed to the Phosphoros photo-z. A Chabrier or Kroupa IMF would give stellar masses about
   0.2-0.25 dex lower.

Full details are in the paper (see "Citation").

## Conventions

- Every quantity measured in this work starts with `eclipse_`. Columns without the prefix are identifiers, values from
  external catalogues, votes, flags and cuts.
- Prospector quantities ending in `_med` are posterior medians. `_low` and `_upp` (and `_err_low`, `_err_upp` for colours) are
  **errors**, not bounds: `_low` = median - 16th percentile and `_upp` = 84th percentile - median.
  The same quantity without a suffix (e.g. `eclipse_logmass`) is the best-fit (maximum-posterior) value.
- Lens-model quantities have `_lower_1_sigma` and `_upper_1_sigma` columns. These are the 1-sigma **bounds** (values), not errors.
- **The stellar mass used in the paper is `eclipse_log_survived_mass_med`** (surviving mass of living stars and remnants).
  `eclipse_logmass` is the total mass formed and is larger.
- SFRs are linear (Msun/yr); stellar masses are log10(Msun).
- **Missing values are -99** in all numerical columns (for example no SED fit, no lens model or no MER match).
- Coordinates are ICRS degrees.

## Rows without an SED fit

14,281 lenses have a photometric redshift (`has_phosphoros_fit`) and 14,255 have a Prospector fit (`has_prospector_fit`).
The 791 without any SED fit have identifiers, lens-model values and votes where available, and the reason in `not_fitted_reason`:

| `not_fitted_reason` | N |
|---|---|
| fewer than 6 bands | 500 |
| no MER source at catalogue position | 170 |
| no lens model | 56 |
| lens model, multiband lens-light fits never converged | 39 |
| not fitted (lens-model consensus fails cut ii) | 26 |

## Sample selection

The paper's final sample is the set of lenses with `final_sample = True`: 9,538 DR1 lenses in this file
(9,813 in the paper together with 275 Euclid Q1 lenses, which are not in this file). Each cut has its own column.
The numbers are cumulative (each row applies all cuts above it):

| Cut | Column | DR1 lenses left |
|---|---|---|
| All grade A/B DR1 lenses | | 15,072 |
| With deblended photometry | `has_phosphoros_fit` | 14,281 |
| (i) MER `DET_QUALITY_FLAG` < 4 | `cut_i_det_quality` | 13,766 |
| (ii) lens model Success, No Consensus or not inspected (75% rule) | `cut_ii_lens_model` | 11,500 |
| (iii) at least 6 bands | `cut_iii_nbands` | 10,683 |
| (iv) OU-PHZ `PHZ_FLAGS` = 0 (lenses without an OU-PHZ entry are kept) | `cut_iv_phz_flags` | 10,594 |
| (v) Phosphoros 70% interval narrower than 1 | `cut_v_zpdf` | 10,557 |
| (vi) Prospector fit not flagged | `cut_vi_prospector_fit` | 9,700 |
| (vii) log10(M*/Msun) >= 10 | `cut_vii_mass` | **9,538** |

Quantities for lenses outside the final sample are given for completeness and should be used with care,
in particular when `flag_unreliable`, `flag_flat_zpdf` is set or `eclipse_number_of_bands` < 6.

## Columns

### Identifiers and position

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 1 | `sed_fitting_id` | string |  | Unique row identifier: `DR1_B<batch>_<n>` (batch = internal processing batch) for lenses with a Prospector fit, `DR1_B<batch>_noprospector_<unique_identifier>` for lenses with a photo-z only, `DR1_nofit_<unique_identifier>` for lenses with no SED fit |
| 2 | `lens_name` | string |  | Name of the lens-modelling cutout |
| 3 | `unique_identifier` | string |  | Identifier in the Euclid DR1 strong-lens catalogue (`EUCL-DR1-Lnnnnnn`); use this to cross-match |
| 4 | `id_str_for_cutout` | string |  | Cutout identifier in the DR1 strong-lens catalogue (encodes MER tile, RA and Dec) |
| 5 | `lens_model_tile_id` | string |  | Cutout on which the final lens model was fitted |
| 6 | `ra` | float64 | deg | Right ascension of the lens (ICRS), from the DR1 strong-lens catalogue |
| 7 | `dec` | float64 | deg | Declination of the lens (ICRS), from the DR1 strong-lens catalogue |

### Values from external catalogues (DR1 strong-lens catalogue, Euclid MER and OU-PHZ)

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 8 | `lens_grade` | string |  | Visual-inspection lens grade from the DR1 strong-lens catalogue (A or B) |
| 9 | `lens_grade_score` | float64 |  | Visual-inspection lens score from the DR1 strong-lens catalogue |
| 10 | `planck_gal_ebv` | float64 | mag | Galactic colour excess E(B-V) at the lens position (Planck dust map), as used to correct the photometry |
| 11 | `mer_det_quality_flag` | float64 |  | `DET_QUALITY_FLAG` bitmask of the matched source in the Euclid MER catalogue. -99 = no MER match. Cut (i) keeps values 0-3 |
| 12 | `mer_spurious_flag` | float64 |  | `SPURIOUS_FLAG` of the matched source in the Euclid MER catalogue (1 = likely spurious). -99 = no MER match |

### Visual inspection of the lens models

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 59 | `lens_model_votes` | int64 |  | Number of expert votes in the visual inspection of the lens model (0 = not inspected) |
| 60 | `lens_model_success_fraction` | float64 |  | Fraction of the votes that are Success (-99 if not inspected) |
| 61 | `lens_model_consensus_50` | string |  | Consensus label at the 50% level: the most-voted label if it holds at least 50% of the votes and is not tied, otherwise `No Consensus`; `N/A` = not inspected |
| 62 | `lens_model_consensus_75` | string |  | Consensus label at the 75% level: the most-voted label if it holds at least 75% of the votes and is not tied, otherwise `No Consensus`; `N/A` = not inspected **(adopted in the paper)** |
| 63 | `lens_model_consensus_100` | string |  | Consensus label at the 100% level: the most-voted label if it holds at least 100% of the votes and is not tied, otherwise `No Consensus`; `N/A` = not inspected |
| 64 | `lens_model_success` | bool |  | True if `lens_model_consensus_75` = Success |

### Photometric redshift (Phosphoros)

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 13 | `eclipse_median_phz` | float64 |  | Photometric redshift of the lens: median of the Phosphoros zPDF, from the deblended lens photometry in 4 x FWHM apertures with the luminosity prior. Grid 0.1 <= z <= 2.0, step 0.01 |
| 14 | `eclipse_min70_phz` | float64 |  | Lower bound of the 70% credible interval of the Phosphoros zPDF |
| 15 | `eclipse_max70_phz` | float64 |  | Upper bound of the 70% credible interval of the Phosphoros zPDF |

### Lens model (PyAutoLens)

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 45 | `eclipse_einstein_radius` | float64 | arcsec | Einstein radius of the SIE mass model (PyAutoLens), posterior median |
| 46 | `eclipse_einstein_radius_lower_1_sigma` | float64 | arcsec | Lower 1-sigma bound of `eclipse_einstein_radius` (a value, not an error) |
| 47 | `eclipse_einstein_radius_upper_1_sigma` | float64 | arcsec | Upper 1-sigma bound of `eclipse_einstein_radius` (a value, not an error) |
| 48 | `eclipse_effective_einstein_radius` | float64 | arcsec | Effective Einstein radius from the area within the tangential critical curve, posterior median |
| 49 | `eclipse_effective_einstein_radius_lower_1_sigma` | float64 | arcsec | Lower 1-sigma bound of `eclipse_effective_einstein_radius` (a value, not an error) |
| 50 | `eclipse_effective_einstein_radius_upper_1_sigma` | float64 | arcsec | Upper 1-sigma bound of `eclipse_effective_einstein_radius` (a value, not an error) |
| 51 | `eclipse_effective_radius` | float64 | arcsec | Half-light radius (not circularised) of the Sersic fit to the lens light in VIS, posterior median |
| 52 | `eclipse_effective_radius_lower_1_sigma` | float64 | arcsec | Lower 1-sigma bound of `eclipse_effective_radius` (a value, not an error) |
| 53 | `eclipse_effective_radius_upper_1_sigma` | float64 | arcsec | Upper 1-sigma bound of `eclipse_effective_radius` (a value, not an error) |
| 54 | `eclipse_sersic_index` | float64 |  | Sersic index of the lens light in VIS, posterior median |
| 55 | `eclipse_sersic_index_lower_1_sigma` | float64 |  | Lower 1-sigma bound of `eclipse_sersic_index` (a value, not an error) |
| 56 | `eclipse_sersic_index_upper_1_sigma` | float64 |  | Upper 1-sigma bound of `eclipse_sersic_index` (a value, not an error) |
| 57 | `eclipse_vis_ratio_ls_l` | float64 |  | Ratio of lensed-source flux to lens flux in VIS, from the lens model. -99 = not available |
| 58 | `eclipse_number_of_bands` | int64 |  | Number of bands with deblended lens photometry used in the SED fits. -99 = no SED fit |

### Prospector derived properties

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 16 | `eclipse_log_survived_mass_med` | float64 | log10(Msun) | **Stellar mass M* used in the paper**: surviving mass (living stars + remnants): posterior median |
| 17 | `eclipse_log_survived_mass_low` | float64 | log10(Msun) | Lower error on `eclipse_log_survived_mass_med` (median minus 16th percentile) |
| 18 | `eclipse_log_survived_mass_upp` | float64 | log10(Msun) | Upper error on `eclipse_log_survived_mass_med` (84th percentile minus median) |
| 19 | `eclipse_sfr_med` | float64 | Msun/yr | Present-day star-formation rate (linear, not log): posterior median |
| 20 | `eclipse_sfr_low` | float64 | Msun/yr | Lower error on `eclipse_sfr_med` (median minus 16th percentile) |
| 21 | `eclipse_sfr_upp` | float64 | Msun/yr | Upper error on `eclipse_sfr_med` (84th percentile minus median) |
| 22 | `eclipse_mw_age_med` | float64 | Gyr | Mass-weighted stellar age: posterior median |
| 23 | `eclipse_mw_age_low` | float64 | Gyr | Lower error on `eclipse_mw_age_med` (median minus 16th percentile) |
| 24 | `eclipse_mw_age_upp` | float64 | Gyr | Upper error on `eclipse_mw_age_med` (84th percentile minus median) |
| 25 | `eclipse_lw_age_rband_med` | float64 | Gyr | Light-weighted stellar age, weighted by rest-frame r-band luminosity: posterior median |
| 26 | `eclipse_lw_age_rband_low` | float64 | Gyr | Lower error on `eclipse_lw_age_rband_med` (median minus 16th percentile) |
| 27 | `eclipse_lw_age_rband_upp` | float64 | Gyr | Upper error on `eclipse_lw_age_rband_med` (84th percentile minus median) |
| 28 | `eclipse_lw_age_lbol_med` | float64 | Gyr | Light-weighted stellar age, weighted by bolometric luminosity: posterior median |
| 29 | `eclipse_lw_age_lbol_low` | float64 | Gyr | Lower error on `eclipse_lw_age_lbol_med` (median minus 16th percentile) |
| 30 | `eclipse_lw_age_lbol_upp` | float64 | Gyr | Upper error on `eclipse_lw_age_lbol_med` (84th percentile minus median) |
| 31 | `eclipse_luminosity_rband_med` | float64 | Lsun | Rest-frame r-band luminosity: posterior median |
| 32 | `eclipse_luminosity_rband_low` | float64 | Lsun | Lower error on `eclipse_luminosity_rband_med` (median minus 16th percentile) |
| 33 | `eclipse_luminosity_rband_upp` | float64 | Lsun | Upper error on `eclipse_luminosity_rband_med` (84th percentile minus median) |
| 34 | `eclipse_luminosity_hband_med` | float64 | Lsun | Rest-frame H-band luminosity: posterior median |
| 35 | `eclipse_luminosity_hband_low` | float64 | Lsun | Lower error on `eclipse_luminosity_hband_med` (median minus 16th percentile) |
| 36 | `eclipse_luminosity_hband_upp` | float64 | Lsun | Upper error on `eclipse_luminosity_hband_med` (84th percentile minus median) |
| 37 | `eclipse_mass_to_light_rband_med` | float64 | Msun/Lsun | Rest-frame r-band stellar mass-to-light ratio (surviving mass): posterior median |
| 38 | `eclipse_mass_to_light_rband_low` | float64 | Msun/Lsun | Lower error on `eclipse_mass_to_light_rband_med` (median minus 16th percentile) |
| 39 | `eclipse_mass_to_light_rband_upp` | float64 | Msun/Lsun | Upper error on `eclipse_mass_to_light_rband_med` (84th percentile minus median) |
| 40 | `eclipse_mass_to_light_hband_med` | float64 | Msun/Lsun | Rest-frame H-band stellar mass-to-light ratio (surviving mass): posterior median |
| 41 | `eclipse_mass_to_light_hband_low` | float64 | Msun/Lsun | Lower error on `eclipse_mass_to_light_hband_med` (median minus 16th percentile) |
| 42 | `eclipse_mass_to_light_hband_upp` | float64 | Msun/Lsun | Upper error on `eclipse_mass_to_light_hband_med` (84th percentile minus median) |
| 43 | `eclipse_sfr_100Myr` | float64 | Msun/yr | Star-formation rate averaged over the last 100 Myr (linear) |
| 44 | `eclipse_sfr_100Myr_err` | float64 | Msun/yr | Uncertainty on `eclipse_sfr_100Myr` |

### Flags and sample selection

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 65 | `has_phosphoros_fit` | bool |  | True if the lens has a Phosphoros photo-z. False = no photo-z and no SED fit (see `not_fitted_reason`) |
| 66 | `has_prospector_fit` | bool |  | True if the lens has a Prospector fit. False = all Prospector columns are -99 |
| 67 | `not_fitted_reason` | string |  | Why the lens has no SED fit (empty if fitted); values listed below |
| 68 | `flag_unreliable` | bool |  | True if the Prospector fit is flagged as poor: ppc p-value < 0.01, or a band deviates by more than 5 sigma, or ESS < 200. Also True if there is no fit |
| 69 | `flag_flat_zpdf` | bool |  | True if the 70% credible interval of the Phosphoros zPDF is wider than 1 (almost flat zPDF; the median then piles up near z = 1.05) |
| 70 | `cut_i_det_quality` | bool |  | True if the lens passes cut (i) `mer_det_quality_flag` between 0 and 3 |
| 71 | `cut_ii_lens_model` | bool |  | True if the lens passes cut (ii) `lens_model_consensus_75` is Success, No Consensus or N/A (not inspected) |
| 72 | `cut_iii_nbands` | bool |  | True if the lens passes cut (iii) `eclipse_number_of_bands` >= 6 |
| 73 | `cut_iv_phz_flags` | bool |  | True if the lens passes cut (iv) `PHZ_FLAGS` = 0 in the Euclid OU-PHZ catalogue, or no OU-PHZ entry (the flag itself is not included in this file) |
| 74 | `cut_v_zpdf` | bool |  | True if the lens passes cut (v) not `flag_flat_zpdf` |
| 75 | `cut_vi_prospector_fit` | bool |  | True if the lens passes cut (vi) has a Prospector fit and not `flag_unreliable` |
| 76 | `cut_vii_mass` | bool |  | True if the lens passes cut (vii) `eclipse_log_survived_mass_med` >= 10 |
| 77 | `final_sample` | bool |  | **True if the lens passes all seven cuts (i)-(vii): the final sample of the paper** |

## Citation

If you use this catalogue, please cite:

> Euclid Collaboration: Nersesian, A., et al., *Euclid Data Release 1 (DR1). Euclid Lens Identification Pipeline and
> Scientific Exploration (ECLIPSE) D: Photometric redshifts and the first census of strong lenses in the galaxy
> evolution framework*, [JOURNAL / arXiv:XXXX.XXXXX]

The lens sample comes from the Euclid DR1 strong-lens catalogue (Euclid Collaboration: Lines, N, et al. 2026, Euclid Collaboration: Holloway, P., et al. 2026); Lens modeling properties come from Euclid Collaboration: Nightingale, J., et al. 2026; please cite those papers too.

## Contact

Angelos Nersesian (angelos.nersesian@ugent.be)
