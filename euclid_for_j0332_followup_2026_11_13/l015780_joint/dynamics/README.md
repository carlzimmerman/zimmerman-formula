# L015780 aperture-corrected spherical dynamics fixture

The independent dynamics leave room for increased stellar mass: at the aperture-corrected SED median, the nine requested spherical scenarios predict **243.72–263.19 km/s**, compared with DESI v2.1 **289.09094 ± 45.77872 km/s**. This is a conditional spherical calculation, not an oblate/rotating model or a combined lensing fit. The lensing-required mass versus source redshift must be compared separately before a joint conclusion.

## Stellar normalization

The actual selected-pixel aperture contains **0.586873907843197** of the adopted infinite COOLEST-point Sérsic profile. Thus the finite-aperture SED median 11.695423687535316 becomes total-mass median **11.926878886134908**, a **+0.23145519859959318 dex** change at fixed shape and constant stellar M/L. The conditional lower/upper mass offsets remain 0.0824999179365555 / 0.055947521539581 dex. No mandatory photo-z transport was applied.

This is an analytic-profile normalization convention, not an observation of unmeasured stellar wings. ECLIPSE-D uses finite modelling-mask unconvolved flux for its SED physical properties; see the [primary paper](https://eceb.astro.uni-bonn.de/public/dr1/nersesian.pdf), §§3.1–3.2 and 6.1, and the neighboring observational/input audit.

The adopted light has n=7.1487323518099215, circularized radius 3.5931186871430794 arcsec, q=0.6670958152224268, major-axis radius 4.399237967210424 arcsec. Its mask radius 6.913007224867312 arcsec extends well beyond the 10-arcsec cutout; 9983 of 10000 pixels are selected. The recommended factor integrates the adopted profile over that actual pixel union. It is **not** the full untruncated circle fraction.

Released-map/infinite-COOLEST-flux ratio 0.5626791623480932 would instead add 0.249739167740633 dex. This is a separate export/profile-normalization sensitivity, with a 0.01828397-dex difference; the discrepancy is not uniquely attributed to a sampling mechanism. Using it shifts the central SED-plus-v2.1 dynamics median from 11.94315 to 11.95982. The exact-profile fraction is primary because it normalizes the spatial model actually used in the calculation.

## Dynamics and conditional mass scan

Geometry is flat H0=67.74 km/s/Mpc, Omega_m=0.3089, lens z=0.428270373960303, scale 5.768111134526029 kpc/arcsec. The spherical fixture uses the geometric-mean effective radius, 20.72550790698354 kpc, exact Abel deprojection, constant mass-to-light ratio, constant velocity anisotropy beta, simple-mu AQUAL with a0=9.3603e-11 m/s², a 0.75-arcsec fiber radius and Gaussian seeing. Seeing and beta are scenarios rather than measured or marginalized priors.

| beta | Seeing FWHM (arcsec) | Dispersion at SED median (km/s) | Dynamics-only best log10 Mtotal | SED + v2.1 median log10 Mtotal |
|---:|---:|---:|---:|---:|
| -0.3 | 0.8 | 248.58 | 12.06526 | 11.94443 |
| 0 | 0.8 | 254.49 | 12.04439 | 11.94233 |
| 0.3 | 0.8 | 263.19 | 12.01419 | 11.93908 |
| -0.3 | 1.2 | 246.36 | 12.07423 | 11.94509 |
| 0 | 1.2 | 251.92 | 12.05442 | 11.94315 |
| 0.3 | 1.2 | 260.09 | 12.02575 | 11.94016 |
| -0.3 | 1.6 | 243.72 | 12.08522 | 11.94583 |
| 0 | 1.6 | 248.84 | 12.06675 | 11.94409 |
| 0.3 | 1.6 | 256.36 | 12.04004 | 11.94141 |

For beta=0 and 1.2-arcsec seeing, the conditional SED-plus-v2.1 mass quantiles at [2.5,16,50,84,97.5]% are [11.80310,11.87655,11.94315,11.99475,12.04530]. The SED prior is an explicitly declared two-half-normal surrogate with equal probability on each side of the catalogue median, using the stated asymmetric offsets. The mass scan has 1301 points separated by 0.002 dex. These are conditional quantiles under that surrogate and the spherical fixture; they do not include shape, IMF, M/L gradients, covariance calibration, rotation, environment or source-redshift uncertainty.

DESI v3.0 gives 295.30569 ± 30.47236 km/s and is treated as an alternative reduction, never multiplied with v2.1 as independent data. The central SED-plus-v3.0 quantiles are [11.84570,11.91117,11.96204,12.01043,12.05767]. The measured fiber/light center offset is 0.048659 arcsec; explicitly averaging the off-center Gaussian aperture changes central sigma by only -0.00826%, from 251.9229 to 251.9021 km/s.

The spherical luminosity fractions entering the fiber are 0.18263475, 0.14338426 and 0.11040925 for 0.8, 1.2 and 1.6 arcsec seeing. Without seeing, the fraction 0.21422181 agrees with the analytic incomplete-gamma Sérsic aperture fraction to 3.51e-6 relatively. These fractions refer to the infinite spherical tracer profile; they are distinct from the elliptical SED modelling aperture fraction above.

## Numerical evidence and reuse

- [Primary contract](contract.json), [script](joint_diagnostic.py), [central values](run_01/central.json), [full result](run_01/result.json), [scan CSV](run_01/mass_scan.csv), [figure](run_01/mass_dynamics.png), [bounded v2 manifest](run_01/manifest.json).
- [Independent aperture contract](independent_contract.json), [script](independent_aperture_check.py), [result](independent_01/result.json), [bounded v2 manifest](independent_01/manifest.json).
- Both runs completed and passed the installed computation-audit manifest validator. All input hashes, versions, executable arguments and limits are recorded. Neither run modifies input files.
- Independent integration of the entire square by adaptive angular/radial-gamma quadrature, minus 17 rejected pixels by adaptive two-dimensional quadrature, gives fraction 0.5868739078431986. It agrees with the renderer by 1.55e-15; baseline/fine renderer difference is 1.82e-11.
- Abel density integrates to 0.999999999918; reprojection versus analytic Sérsic brightness differs by at most 6.63e-7 relatively at five tested radii.
- Exchanging the Jeans and aperture integration order gives a linear acceleration kernel. Its predictions agree with an independent pressure-to-LOS-to-aperture quadrature to at most 2.68e-7 relatively in sigma across all nine scenarios.
- Doubling radial, Abel, angular and luminosity resolution changes sigma by at most 8.58e-6 relatively at three tested masses in every scenario. Analytic Newtonian Plummer pressure/projection/aperture benchmarks and the independent exchanged-kernel Plummer aperture benchmark pass.

The outcome is **finite numerical implementation verified over the stated fixtures**, conditional on the physical assumptions and catalogue summary distributions. No full-model theory confirmation or exclusion follows.
