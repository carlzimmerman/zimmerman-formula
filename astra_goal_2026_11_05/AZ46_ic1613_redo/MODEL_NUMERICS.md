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

## A2 — border normalization arithmetic, after failed fixture, before production

The original fallback leaves two known-answer checks failing: maximum
absolute cube error1.6379172323999214e-12 at channel14,y20,x40 of the41x41
extended-source fixture, against the unchanged1e-12 line. This pixel lies
in the fixed24arcsec zeroed border. Its masked model sum is4.2285969605e-7
of the maximum, above sqrt(epsilon)=1.4901161194e-8, so the old fallback
does not run there. Interior error is7.78e-16. Direct positive summation
of the same full periodic kernel at this pixel gives8.68e-19 maximum error.

Before editing the model, extend the fallback to the union of the original
weak-sum set and every fixed-border pixel with positive observed masked
intensity. This is a categorical treatment of the already-declared zeroed
border, not a newly tuned leakage threshold, intensity cut or acceptance
line. The beam, border size, convolution, mask and local normalization are
unchanged. Report cost/use and rerun the original failed tests without
changing their tolerances. This amendment is explicitly post-fixture-result;
it does not repair the separate robust6arcsec beam-moment failure or prove
production accuracy across all fitted geometries. Downstream mock/fit
evidence whose model hash changes must be regenerated before reuse.
