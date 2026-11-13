# FOR J0332 aperture normalization and independent light checks

The recommended aperture fraction for the **fixed COOLEST-point, unit-total stellar mass library** is **0.8038930178016896**. Under that same infinite Sérsic model and spatially constant stellar mass-to-light ratio,

\[
M_{\rm aperture}=f_{\rm aperture}M_{\infty},\qquad
\log_{10}M_{\infty}=\log_{10}M_{\rm aperture}+0.09480174337819178.
\]

Thus the catalogue Salpeter median 11.831087312562882 becomes **11.925889055941074**. At fixed shape this shifts the location of the adopted mass prior; its published asymmetric conditional offsets remain 0.10419238776391282 below and 0.08637886769182401 above. This is a model normalization correction, not an independent observation of stellar mass in the outer wings.

## Why an aperture correction is needed

ECLIPSE-D defines its lens total flux as the unconvolved model summed over pixels within the circular modelling mask (§3.1), and uses this flux for the physical-property SED fit (§3.2). Its limitations section explicitly discusses omitted Sérsic wings and possibly underestimated stellar masses (§6.1). The effective radius is the circularized/geometric-mean radius. These definitions are in the [primary paper](https://eceb.astro.uni-bonn.de/public/dr1/nersesian.pdf), with a checksum-pinned local copy in the experiment manifest.

The adopted model has geometric-mean radius 1.139181788743383 arcsec, major-axis radius 1.263125483214478 arcsec, n=5.868719099803722 and q=0.8133792204448107. The circle is centered at (west,north)=(-0.25,-0.35) arcsec with radius 4.770086090372511 arcsec. Its 7128 selected pixel centers lie in the 100-by-100 cutout. The circle extends south of the cutout edge: its minimum north coordinate is -5.120086 arcsec, whereas the image ends at -5.0 arcsec. Consequently a full continuous circle covers slightly more area than the released pixel selection.

| Normalization | Enclosed fraction | Addition to log10 mass |
|---|---:|---:|
| Exact adopted profile integrated over selected pixel union; recommended | 0.8038930178016896 | 0.09480174337819178 dex |
| Full offset geometric circle; geometry comparison | 0.8041991534587496 | 0.0946363883934997 dex |
| Released VIS pre-PSF map divided by analytic COOLEST infinite flux; normalization sensitivity | 0.7984475942238776 | 0.09775358332797784 dex |

The first row is appropriate to the fixed mass library because it integrates the very profile whose infinite mass the library parameterizes, over the actual catalogue aperture pixels. The released-map alternative retains a small export/profile-normalization mismatch rather than silently identifying the map with an exact pixel integral. It changes the correction by 0.00295184 dex. The origin of this mismatch is not uniquely diagnosed here.

The released VIS unconvolved circle sum is 16.38420045765792 native units; the analytic infinite flux of its COOLEST point model is 20.52006991590225. All released galaxy maps are zero outside the circle. NIR H/J/Y full-circle sums agree with maximum-likelihood catalogue fluxes to about 6e-5 fractionally after AB conversion; VIS differs by 1.11%, so exact all-band map/table identity is not claimed. Removing artefact pixels does not match the NIR catalogue fluxes as closely as the full circle does.

## Evidence and interpretation limits

- [Aperture contract](aperture_contract.json), [script](aperture_audit.py), [central values](aperture_audit_01/central.json), [full results](aperture_audit_01/result.json), and [bounded-run manifest](aperture_audit_01/manifest.json) preserve inputs, hashes, versions and command. The completed run passed the computation-audit manifest validator.
- Use `central.json["fraction_pixel_integrated_circle"]` for the recommended fixed-library correction. The key `fraction_released_map_over_COoLEST_infinite_flux` is the explicitly separate map sensitivity. The spelling is preserved in the recorded output.
- The continuous integral uses an exact incomplete-gamma radial primitive and angular quadrature. Doubling angular nodes from 256 to 512 changes the fraction by 1.6e-15, and independent adaptive angular quadrature differs by 6.7e-16. Pixel integrals use the independently benchmarked renderer described below.
- The catalogue median light shape gives a full-circle correction of 0.0858711 dex. Synthetic marginal-summary draws under three assumed n/radius correlations produce different spreads; they are recorded as covariance sensitivity only. They are **not a native joint shape posterior**. A different light shape also changes the deflection field, so varying this fraction alone is not complete shape-uncertainty propagation for the image fit.
- The correction assumes constant stellar M/L and infinite single-Sérsic continuation. No SED refit, IMF change, actual outer-wing measurement, M/L gradient measurement, redshift transport, or environmental correction is included.

## Independent raw VIS/NIR shape fits

The raw-band test is recorded in [its contract](contract.json), [script](fit_light_shapes.py), [results](run_01/result.json), [model arrays](run_01/models_masks.npz), and [bounded manifest](run_01/manifest.json). It fits a PSF-convolved elliptical Sérsic lens plus constant sky to VIS and NIR Y/J/H, with free center, n, major-axis radius, axis ratio, position angle, intensity and sky. Published parameters supply starting points only. Released source and artefact masks are dilated by 1–3 pixels; stronger PSF-overlap masks and conditional subtraction of the released source template provide controls. The fit aperture is a separate 4.5-arcsec circle centered on the lens, and must not be confused with the catalogue SED aperture above.

**These masked fits do not establish a precise independent NIR stellar profile.** One-to-three-pixel dilation is smaller than the 0.51–0.59 arcsec NIR PSF FWHM and leaves source-wing sensitivity. Conservative PSF-overlap masks remove nearly all NIR data within one arcsec; full-support exclusion removes all within two arcsec. Fits then become unstable or hit n/radius bounds. This is a limitation on identifiability, not evidence for a preferred extreme profile. The source-subtraction alternative is conditional on a published source model.

At the two-pixel mask, exploratory (n, major-axis radius in arcsec) values are VIS (4.902,0.967), Y (4.775,0.678), J (5.059,0.752), H (4.193,0.640). Their strong variation under mask controls precludes treating them as independent precise mass-profile measurements or a measured M/L gradient. Supplied diagonal-RMS chi-square per pixel is about 0.46 in VIS and 0.06–0.08 in NIR; noise calibration and resampling correlations also limit nominal error interpretation.

Numerical checks passed: an analytic Gaussian-profile/Gaussian-PSF benchmark has peak-normalized maximum discrepancy 5.42e-10; noiseless known-Sérsic recovery uses each actual band PSF and a finer renderer; numerical refinement at fitted models changes predictions by at most 0.00073 supplied-RMS units per pixel. Central pixels use radial incomplete-gamma integration, not sampling the Sérsic cusp. Fixed-n=4 controls and full 7-by-7 joint n/radius profile grids with nuisance refits are included. The profile grids, local covariances and strong n/radius correlations are conditional diagnostics, not calibrated posterior regions; coarse interpolation in the plot should not be read as precise contour structure.

Figures: [raw data/model/residuals](run_01/raw_band_fits.png) and [mask dependence and profile grids](run_01/shape_profiles.png).
