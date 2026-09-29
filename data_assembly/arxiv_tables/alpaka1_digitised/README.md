# ALPAKA I rotation curves digitised from the paper's figure

`digitise.py` reads the raster figure `vrot_2303.16227.png` (the paper's `figures/vrot.png`, arXiv:2303.16227, sha256
`bc03fa1107cff2ef816c2e0b032893f6e54c6f625ee17335af0918996cd824b6`) and recovers, for the 19 secure disks, the radius and
value of every plotted ring (velocity and dispersion), the plotted 1-sigma band at each ring, and the dashed optical R_e
line where the paper drew one. No author was contacted. Nothing is fitted.

## Method
- Axis label VALUES were transcribed by eye from 2.6x crops (an OCR attempt was unreliable and was abandoned); label
  POSITIONS are detected automatically; each axis is a linear map fitted to its ticks with a residual check (x axes start at 0
  at the left frame edge, y axes at 0 at the bottom frame edge). Both the arcsec axis (bottom) and the kpc axis (top) are
  calibrated independently.
- Rings are found by colour (pink velocity, teal dispersion); a closing step recovers markers crossed by the dashed R_e line.

## Validation (in `checks.txt`, `alpaka1_vrot_validation.csv`)
- 118 markers on 19 disks; every disk has the same number of velocity and dispersion rings.
- Digitised max V against the paper's table V_max: median 0.7%, max 1.6%. Digitised mean of the last two rings against the
  table's V_ext: median 0.8%, max 1.3%. Dispersion at the outer rings agrees with the table's sigma_ext to the printed digits.
- kpc per arcsec from the two independent axes against the angular scale at each galaxy's redshift (flat LCDM, H0 = 70,
  Om = 0.3; the paper's own cosmology was not checked): median 1.6%, max 2.0%.
These checks would expose a mis-transcribed label; none fails.

## Outputs
- `alpaka1_vrot_digitised.csv`: every ring (id, ring, panel V or sigma, R in arcsec and kpc, value, plotted band edges, pixels).
- `alpaka1_outer_summary.csv`: per disk, the outermost ring radius R_ext (arcsec and kpc), V_ext (the paper's table value), R_e where
  drawn, R_ext/R_e, and V_ext^2 / R_ext in units of a0 = 1.2e-10 m/s^2.
- `debug_overlay.png`: the figure with every detected marker circled, for a visual check.

## Results and what they do not say
- R_ext runs from 1.4 to 6.3 kpc (0.18 to 0.84 arcsec). The outermost ring is the outermost radius at which the rotation velocity
  was measured in the paper (footnote to its dynamical-time estimate).
- **R_e is available for only 7 disks** (ID 1, 6, 8, 9, 18, 20, 28): the paper drew it only for galaxies with HST data whose R_e is
  comparable to or smaller than the CO/[CI] extent. R_ext/R_e is 1.23, 1.00, 1.63, 0.79, 3.50, 0.94 and 2.34 for those. For the other 12
  disks the figure does not say whether R_e is missing (no HST data) or larger than the CO extent.
- **V_ext^2/R_ext / a0** is a rough estimate of the total centripetal acceleration at the outermost ring (deprojected velocity, spherical
  shortcut, no baryon model); it is NOT g_bar. It ranges from 2.0 (ID 1, z = 0.56, R_ext = 1.23 R_e) through 3.7-4.7 (ID 12, 7, 13) to 31.8
  (ID 22); ID 18 (3.5 R_e) is 11.8 and ID 28 (2.3 R_e) is 9.8.
- ID 1 is the lowest. My rough order-of-magnitude for its baryons (M* = 1.1e10 Msun plus a CO-derived gas mass of 1e9-8e9 Msun
  depending on the conversion factor, none applied in the repo) puts g_bar at R_ext of order 0.5-0.8 a0, i.e. possibly below a0. That is
  arithmetic in the margin of a README, not a calculation; the gas conversion and the geometry need the calculation thread.
- Band edges are read from anti-aliased colour and are approximate.
