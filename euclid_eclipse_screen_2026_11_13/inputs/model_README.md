Euclid DR1 strong-lens catalogue: dr1_catalogue_v5
====================================================

Built 2026-10-25 on RAL by the chunked catalogue build (hpc/batch_cpu/submit_catalogue_chunked.sh, euclid_dr1 @ unknown).

Samples (tile ids are unique across samples):

- `dr1_sep1`: 15007 lens folders

Lens folders: 15007

Root files
----------

| File | Rows | What |
|------|-----:|------|
| `lens_mass.csv` | 14984 | vis_pix mass model (SIE + shear), one row per lens |
| `lens_sersic.csv` | 14968 | lens light Sersic (VIS), one row per lens |
| `source_sersic.csv` | 14968 | source light Sersic (VIS), one row per lens |
| `magnitudes.csv` | 118977 | lens / lensed-source fluxes, one row per lens x band |
| `witt_wynne.csv` | 14923 | Witt-Wynne SIEP projection, one row per lens |
| `astrometric_offsets.csv` | 104067 | band-to-VIS grid offsets (prior +/-0.5"), one row per lens x non-VIS band |
| `wcs.csv` | 0 | sky positions (lens light, source, lensed images), one row per lens x {vis_lp, vis_pix} |
| `source_clumps.csv` | 0 | vis_pix source clumps x their lensed images |
| `wcs_skipped.csv` | 0 | lenses with no wcs.csv rows, and why |
| `grades.csv` | 15007 | v5 lens-finding grade + sample of every lens |
| `lens_index.csv` | 15007 | per lens: sample, grade, which products exist, distribution part |
| `band_inventory.csv` | 15071 | QA: expected vs completed SED bands, every requested tile |
| `unresolved_manifest.csv` | 351 | QA: the band_inventory rows not fully complete |
| `excluded_tiles.csv` | 62 | QA: tiles left out of the build (no finished vis_lp + vis_pix), and why |
| `fits_deduplication_validation.csv` | 29820 | QA: per pre_psf/model.fits, HDU and duplicate-EXTNAME counts |
| `fits_deduplication_summary.json` |  | QA: summary of the above |

Per-lens folder
---------------

PNGs: vis_lp_fit, vis_pix_fit, vis_lp_image_with_positions, rgb, segmentation,
fit_sersic, fit_multi_wavelength. FITS: pre_psf / model (one HDU pair per band,
<BAND>_GALAXY_0 = lens, _1 = lensed source), convergence, potential, deflections.
JSON: coolest, coolest_sersic, wcs_vis_lp, wcs_vis_pix. CSV: this lens's rows of
every root table, plus vis_pix_source_plane_reconstruction_<i>.csv (the
pixelized source reconstruction, one row per source-plane mesh pixel).
witt_wynne.in: isit4or2or1 input.

Every Sersic product comes from the newest completed result per lens and band.
