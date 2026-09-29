# KURVS-CDFS observed Hα rotation curves v_obs(R), all 22 galaxies, from the paper's vector figures

Built 2026-09-29 by `extract_rc.py`, from the same four figure PDFs and with the same method as `../kurvs_sigma_profiles/` (byte-for-byte source copies and their sha256 are there). Files already on disk only; no download, no contact.
Requested by the "Complete gravity theory" chat for the calc thread's CFG184. Data only: no physics, no pressure or beam-smearing correction, no inclination correction.

## Files
| file | rows | content |
|---|---|---|
| `kurvs_rc_points.csv` | 511 | one row per plotted marker: `kurvs_id`, `R_kpc` (signed, both sides), `v_obs_kms`, `err_up_kms`, `err_lo_kms`, `clipped_white_marker`, `errbar_touches_axis_edge`, `errbar_extends_beyond_axis`, `has_errbar`, `source_pdf` |
| `kurvs_rc_model_curves.csv` | ~34 vertices per galaxy | the authors' best-fit exponential-disc (Freeman) model curve as polyline vertices inside the panel: `R_kpc`, `v_model_obs_kms` |
| `kurvs_rc_reference_lines.csv` | | R50 dotted verticals (kpc) |
| `kurvs_rc_control_vs_table.csv` | 22 | the control against Table B1 (below) |
| `qa_replot.png`, `checks.txt` (171 PASS), `manifest.json` | | replot compared with the paper's figures by eye; checks; axis calibrations |

## Meaning of the columns (the paper's own caption)
- **Radius:** kpc, signed; both sides of the kinematic centre; the plot convention is that "rotation curves are plotted such that the velocity gradient is always positive", so the sign of R is a plotting convention.
- **Velocity:** the OBSERVED line-of-sight velocity along the kinematic major axis: **not** inclination-corrected, **not** beam-smearing corrected, no pressure-support correction. Divide by sin i (Table 1, `../kurvs2023_integrated.csv`, `inc_sfr_deg` from HST-F814W) for the deprojected value.
- **Error bars:** the plotted 1σ vertical bars, exact geometry (31 touch the panel edge and 30 extend beyond it: the PDF geometry is complete, the figure clips them visually). Every marker has a bar.
- **Clipped markers:** white circles (18) are pixels the authors clipped for sky-line contamination or broad components (paper caption); they are kept in the CSV and flagged.
- **Model curve:** the black solid curve of the figure (the paper's best-fit exponential-disc model to the data, used to interpolate the observed velocities at R′₃D and R′₆D); the polyline is the figure's own vertices within the plotted range (about ±15 kpc).

## The control (data-driven, not by eye)
The model curve at |R| = R_Hα,max (Table B1 column 2, `../kurvs2023_velocities_at_radii.csv`), divided by sin i_SFR, reproduces the tabulated "velocity at the maximal extent" (column 3): median ratio 1.001, range 0.994–1.009 over the 20 galaxies with V > 15 km/s, and KURVS-4 (V = 8.0) gives 8.02. KURVS-10 could not be checked because its R_max (15.2 kpc) lies beyond the plotted axis. This confirms both the axis calibration and that the tabulated last-point velocity is the model evaluated at R_max, not the last data marker (my reading of the agreement). The velocities at R′₃D and R′₆D could not be checked the same way because the per-galaxy R′ in kpc are not tabulated; only the R_max control is available.
Also: marker radii equal those of the σ(R) extraction to within 0.013 kpc for 21 of 22 galaxies (same panel rows, separate axis calibration); KURVS-3 has two extra rotation-curve markers (R = −9.4 and −8.6 kpc) that are absent from its σ panel, presumably because their σ falls outside the plotted range.

## Limits
- The plotted points are a 1D cut along the major axis sampled about once per pixel, after adaptive binning to S/N ≥ 5 (blocks up to 9 × 9 spaxels); successive points are correlated.
- Extrapolated parts of the model curve (beyond the data) are the exponential-disc fit, not measurements; the paper notes "measurements of the rotation velocity are extrapolated from the best-fitting model when the observed data do not extend far out" (TeX l. 386).
- Inclination correction uses `inc_sfr_deg`; the paper's own choice and the star-formation inclination uncertainty are not propagated here.
