# AZ46 numerical implementation contract, before new fits

This records numerical choices before any new optimization or mock verdict.
It does not change FROZEN_CRITERIA.md or the prepared data identities.

The extended-source known answer failed at the corners in commit
8a18286e8e. Its intrinsic emission is removed by the inherited border;
local normalization divides by tiny beam leakage and amplifies FFT
cancellation. The compact-source test passes at unchanged tolerance.

Retain the full pixel-integrated beam kernel and circular convolution
convention. After FFT convolution, at spatial pixels with positive observed
masked intensity and computed masked model sum no greater than
sqrt(machine epsilon) times the maximum absolute masked model sum,
recompute every channel by direct nonnegative summation of the SAME full
periodic kernel. This is an arithmetic fallback, not a new beam, intensity
cut, data mask, fit parameter or physical acceptance line. A zero result
keeps the original zero-normalization behavior. Report fallback use in fit
diagnostics. Its cost must be included in the fit pilot, not assumed free.
Keep the original failed tests and their tolerances; rerun them after the
repair and retain the earlier failures in git history.

For the two current 8x8 pilots at reference geometry (centre zero, PA73.7,
inclination35, systemic velocity -232.2, sigma9 and rotation min(R/20,20)),
neither cube has selected border pixels or requires this fallback. This
single evaluation does not prove safety across geometry or dispersion fits.

Physical numerical domains are 24 arcsec for the border, +/-1000 arcsec
for the force plane and 960 arcsec for its radial range. Preserve the
original pressure-support smoothing's physical 30 arcsec width (five
6-arcsec cells). On a different regular radial grid, integrate a centred
30-arcsec top-hat over the piecewise-constant cell values with reflected
boundary extension. At 6 arcsec it is exactly the original five-cell
uniform filter; at 3 arcsec the end cells have half weights. The model's
stated pressure-support form, clipping and six dispersion nodes remain.

Use dense finite-difference Jacobians: the old fixed-start ring sparsity
does not establish zero derivatives under moving geometry and beam
convolution. Production optimizer budgets remain the frozen 100/200.
Tiny-budget implementation pilots must be labelled ungraded.

Kappa = 1/2 FITTED; not theory closed.
