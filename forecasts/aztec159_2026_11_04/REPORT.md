# AzTEC/C159: conditional prerelease gravity comparison

Calculated 2026-11-04. The 2027 datasets could test particular dark-halo models, but the available information does not support promising a decisive test of FDESI versus MOND. Numbers below are conditional predictions from published mass profiles, not measurements of the outer rotation curve.

## Model and inputs

Use the current law-only PAPER66 canonical footing: gN=g²/(g+a0), local a0=9.3603e-11 m/s². FDESI uses w0=-0.838, wa=-0.62 and a0(z)/a0(0)=sqrt[a^(-3(1+w0+wa)) exp(-3wa(1-a))]. At z=4.5668 this ratio is 0.659339. Matched MOND holds the same local normalization and interpolation law fixed. F-flat is identical to this matched MOND comparator; this galaxy cannot distinguish those two descriptions. No retired cold-sector halo rule is added.

Published inputs: Mstar=4.5e10 Msun, Mgas=1.5e11 Msun, stellar effective-radius proxy 0.460×1.4=0.644 kpc, gas exponential SCALE length 1.3 kpc, inclination40 degrees, integrated [CII] flux4.6 Jy km/s. These follow [Fraternali et al. 2021](https://arxiv.org/abs/2011.05340), Table1 and section3.2. The stellar size is inferred from FIR size, not an observed stellar mass map. Gas mass assumes alphaCO=4.3. The published inner rotation estimate is 506 +151/-76 km/s, with inclination dominating its uncertainty; the two rings are not fully independent. No independent outer curve is available in that analysis.

[Jiménez-Andrade et al. 2018](https://arxiv.org/abs/1710.10181) supplies the CO-based mass estimate. Its approximately20% quoted gas-mass uncertainty does not exhaust conversion-factor systematics. A conversion factor inferred using a dynamical mass cannot be treated as an independent prior when testing that same gravity law.

## Calculated circular speeds

Two razor-thin exponential discs; gas and stellar radii held fixed. NFW column reproduces the illustrative halo choice in Fraternali2021: M200=2e12 Msun, c200=3.4. This is one halo prescription, not a unique dark-matter prediction. Here M200 normalizes the dark profile directly; its radius uses H0=68.56427, Omega_m=0.2976016 flat cosmology. The published-profile extrapolation beyond3 kpc is unverified.

| Radius kpc | Baryons/Newton | FDESI | Matched MOND | Baryons+published NFW |
|---:|---:|---:|---:|---:|
| 1 |547.3|549.0|549.9|559.3|
| 2 |542.8|546.3|548.0|565.3|
| 3 |512.5|518.0|520.7|545.8|
| 5 |438.4|448.7|453.6|494.9|
| 7.5 |356.6|374.4|382.2|443.6|
| 10, exploratory |301.6|327.3|337.7|416.6|

All speeds km/s, intrinsic circular speeds before pressure support and beam convolution. The planned extended-emission motivation mentions15 kpc DIAMETER, not15 kpc radius. Even7.5 kpc is a conditional reach, not an assured detected ring. At7.5 kpc the major-axis line-of-sight FDESI–MOND gap is only5.0 km/s at inclination40 degrees. Standard a0=1.2e-10 MOND gives388.1 km/s there, but that changes the local calibration as well as redshift evolution. It must not be presented as a pure evolution test.

## Nuisance degeneracies and required precision

An equal-weight fractional fit over27 radii from1 to7.5 kpc shows that matched MOND with stellar mass increased3.38% and gas mass reduced4.08% approximates the nominal FDESI curve to RMS1.92 and maximum3.46 km/s. These are small changes relative to present mass uncertainty. This is a curve-mimicry calculation, not a fit to observed data or a posterior probability.

An NFW alternative with stellar mass increased11.68%, gas mass reduced14.69%, c=2, and dark mass about9.57e11 Msun gives RMS6.67 and maximum12.05 km/s residuals. Its halo mass is at the imposed baryon-budget floor Mdark=Mb×0.843/0.157, and concentration is at the allowed lower bound2. This is a favorable baryon-rich, low-concentration example, not evidence that such a halo is preferred. Wider halo/profile freedom was not searched. Rejecting the published2e12/c3.4 curve would not reject all dark matter.

For a single7.5 kpc bin, the fixed-model7.80 km/s MOND gap corresponds to a total uncertainty budget below2.60 km/s for a nominal3-sigma separation. If each acted alone, inclination uncertainty would need to be below0.334 degrees, or gas normalization uncertainty below1.91%. These limits cannot all be saturated simultaneously: velocity measurement, inclination, gas and stellar profiles, distance, pressure support, warps and systematics share the budget. Joint shape fits can change these requirements; they are transparent single-bin benchmarks, not universal observing specifications.

## What the 2027 releases provide

[ALMA Science Archive](https://almascience.eso.org/aq/), TAP metadata retrieved2026-11-04 and preserved in inputs/archive_metadata.csv:

* 2023.1.00835.S, uid://A001/X3621/X205e: release2027-07-20 16:28:27 UTC (12:28 EDT). Outer-disc [CII]; metadata resolution0.1794 arcsec, about1.20 kpc with the paper's6.70 kpc/arcsec scale, maximum recoverable scale3.19 arcsec. Listed noise near the line0.686–0.8093 mJy/beam per10 km/s. These are archive metadata values, not measurements from the proprietary cube. Repeated spectral entries are not assumed independent observations.
* 2025.1.00827.S, uid://A001/X3833/X2514: release2027-09-24 18:08:58 UTC (14:08 EDT). CO excitation/gas-mass project, beam1.80 arcsec. This complements resolved [CII] rather than directly supplying an equally resolved rotation curve. The proposal describes JWST mass-distribution data, but this calculation does not use a new published JWST mass map. No achieved percent-level alphaCO precision is specified.
* Additional carbon-line project2026.1.00461.S is listed with placeholder release3000-01-01; it has no verified2027 release date and is excluded from the2027 sensitivity claim.

These are scheduled public-release dates, not necessarily dates of future observations, and can change.

## Conditional sensitivity calculation

Forward-model an inclined exponential [CII] disc with the published flux and scale length, Gaussian local line dispersions16 and30 km/s, the0.1794-arcsec beam and listed noise. Compare cubes with one independent noise sample per Gaussian beam area. The resulting square-root weighted squared differences are approximate model distances, NOT injection-calibrated detection significances. They assume known geometry, no uv filtering, Gaussian beam/noise, fixed surface brightness and no noncircular motions. Spatial noise covariance and actual reduction/taper sensitivity require the released visibilities. The velocity grid is10 km/s; channel width alone is not a velocity-error floor.

| Comparison with nominal FDESI | Approximate full-cube model distance | Image pixels assigned deprojected R>5 kpc |
|---|---:|---:|
| Same-mass MOND |0.35–0.73|0.13–0.29|
| Adjusted-mass MOND example |0.28–0.55|0.03–0.07|
| Same-mass published NFW |3.53–7.27|1.12–2.32|
| Adjusted-mass NFW example |0.96–1.93|0.10–0.26|

The full-cube comparison gets much of its information from bright inner emission. The outer-only statistic masks image pixels after beam convolution; it is not a clean isolated annular likelihood. These mass-adjusted examples were fitted to intrinsic curves, not optimized to minimize cube differences, so they do not give the best possible competitor fit.

An extended component brighter than the extrapolated exponential could improve outer kinematics; its actual flux, rotation and mass contribution must be measured. A taper may help surface brightness but cannot be assigned a new sensitivity without the visibility weighting. The present calculation therefore does not prove the July dataset cannot succeed, but does show there is no supported claim that it will resolve the small MOND gap.

## Decision

At the assumed masses and profiles, an outer speed near374 rather than444 km/s would challenge the paper's illustrative NFW halo. It would not favor FDESI over MOND unless independent baryonic and geometric constraints also exclude MOND's neighboring predictions. July's outer kinematics plus September's gas information make this a useful conditional halo test. A decisive FDESI-versus-MOND test remains unsupported by current precision information. Existing inner data do not select among these alternatives.

## Reproduction and scope

calculate.py, contract.json, and run01 contain the bounded computation, predictions, sensitivity scenarios and checksummed manifest. Validation passed; point-mass and zero-a0 limits, prediction ordering, deep-MOND bound and optimizer convergence checks passed. The finite grid varies gas mass1.2–1.8e11 and gas scale length0.9–1.7 kpc; it is not a posterior. All original forecasts and sealed predictions remain untouched.
