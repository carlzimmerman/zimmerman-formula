# KURVS-CDFS observed Hα velocity-dispersion profiles σ_obs(R), all 22 galaxies

Built 2026-09-29 by `extract.py` from the four vector figures of arXiv:2305.04382 (Puglisi+2023) that show each galaxy's rotation curve
and dispersion profile (copies in `raw_small/`, sha256 in `manifest.json`). The PDFs hold every marker, error bar, reference line and tick
as exact geometry and the tick labels as text, so nothing was read by eye; axes are calibrated from the major ticks and their labels.
No g, V_c, pressure-support correction, model or verdict is computed here. Requested by the calculation thread; data only.

## Files
| file | rows | content |
|---|---|---|
| `kurvs_sigma_profiles.csv` | 509 | one row per plotted marker: `kurvs_id`, `cdfs_id`, `R_kpc` (signed), `sigma_obs_kms`, `err_up_kms`, `err_lo_kms`, `clipped_white_marker`, `errbar_touches_axis_edge`, `errbar_extends_beyond_axis`, `has_errbar`, `source_pdf` |
| `kurvs_sigma_reference_lines.csv` | 22 × (2 lines + band lo/hi + R50 verticals) | per galaxy: `sigma0_observed_line`, `sigma0_beam_corrected_line`, `sigma0_band_lo/hi` (km/s), `R50_dotted_vertical_kpc` (kpc, both signs) |
| `kurvs_sigma_coverage.csv` | 22 | radii only: outermost unclipped point on each side, all-sides, including clipped, the paper's R_Hα,max, number of unclipped points at |R| ≥ 0.5 R_Hα,max |
| `qa_replot.png` | | replot of the extracted data, compared to the paper's figures by eye |
| `checks.txt`, `manifest.json` | | 134 PASS lines; calibrations (slope, residual, ticks) |

## The six items asked for
1. **Radius axis:** kpc (the figures' x label is "Radius [kpc]"). `R_kpc` is signed: the figure plots both sides of the kinematic centre; the
   pixel-to-kpc conversion is the authors' own (the axis is drawn in kpc), read from the tick labels. The paper's TeX does not say which cosmology/scale it used
   beyond that; nothing was converted by me.
2. **Observed or corrected:** the plotted profile is **σ_obs, the OBSERVED dispersion, not beam-smearing corrected**. The paper's caption says the
   horizontal dotted line is the observed σ_0, the solid line the beam-smearing-corrected σ_0 (Johnson+18 Table B1 correction, applied to the single
   outer-disc value, not to the profile), and the grey band the 1σ error of σ_0. The corrected σ_0 lines reproduce the paper's Table σ_0 within 0.44 km/s
   and the band half-widths reproduce its errors within 0.46 km/s (checks in `checks.txt`).
3. **Error bars:** 1σ vertical bars as drawn (the paper states the map uncertainties are the 1σ errors of its χ² line-fit; the 1D bars are taken from those maps).
   `err_up/err_lo` are the exact geometric bar half-lengths in km/s. 34 bars extend beyond the plotted axis range (`errbar_extends_beyond_axis = 1`; the
   PDF geometry is complete, the figure clips them visually) and 37 touch the edge; no marker lacks a bar.
4. **Major axis, sides:** the profile is extracted from the σ_obs map along the kinematic major axis (the grey solid line in the paper's maps), both sides
   plotted as negative and positive radius; the paper says rotation curves are plotted so the velocity gradient is positive, so the sign of `R_kpc` is
   the plotting convention, not a fixed compass side.
5. **Outermost radius vs R_max:** `kurvs_sigma_coverage.csv` gives it. Including clipped markers the outermost radius equals the paper's R_Hα,max within 0.15 kpc for
   21 of 22 galaxies; KURVS-10 differs (13.5 vs 15.2 kpc) so the table's R_Hα,max there is not the extent of the plotted dispersion profile. The number of unclipped points
   at |R| ≥ 0.5 R_Hα,max ranges 4–13 per galaxy.
6. **Flagged or masked points:** white-filled circles are pixels **clipped** for large sky-line contamination or broad components (the paper's caption); 18 such markers,
   flagged in `clipped_white_marker`. They are still plotted by the authors and stay in the CSV, so drop them if you want the authors' clean set. The paper flags KURVS-21 as
   having a highly asymmetric velocity field and marks it `*` in its tables (`flag_star_in_table` column of the coverage file). Thick dotted verticals mark R50 (HST half-light radius) for reference.

## Limits
- Marker centres are exact geometry; the axis calibration uses two to five labelled major ticks per panel (residual ≤ 0.01 km/s wherever more than two ticks exist). Values are as precise as the authors' plotted figure.
- The y calibration for KURVS-11 uses only two labelled ticks (the fit is exact by construction); it is cross-checked by its σ_0 lines matching the table.
- The dispersion is the line-of-sight Hα dispersion in a seeing-limited 1D cut; beam smearing raises σ_obs where the velocity gradient is steep (the centre, and outer points with large error).
- Figure resolution: what the authors plot is a 1D cut sampled about once per KMOS pixel, so successive points are correlated.
