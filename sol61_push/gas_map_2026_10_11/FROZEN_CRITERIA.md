# Gas-only map normalization audit, frozen before pixel calculations

Observed before freeze: authors' public Dropbox V1 release has gas-only
xray_alpha1_dsdls1.fits, xray_alpha2_dsdls1.fits and xray_kappa_dsdls1.fits.
Downloaded all three (529920,529920,267840 bytes). Headers only inspected:
256x256, TAN WCS, CDELT=(-,+)5.4666666667e-4 degrees, no BUNIT or RADESYS.
Parameter metadata declares profile17 map inputs at lens redshift .296;
release states Dls/Ds=1 normalization. No pixel-derived quantity seen yet.

Audit scope: source authentication, array integrity, angular coordinates,
deflection convention and differential consistency. No fitted dark halo map,
physical mass conversion, arbitrary gas renormalization, repaired-kernel fit,
cold-mass verdict or a0-footing prediction.

Use float64 arrays. Freeze coordinate convention x=west, y=north, with both
pixel axes increasing. Test all eight signed permutations of supplied alpha
components; primary expected convention is (+alpha1,+alpha2). For each compute
D=(d ax/dx+d ay/dy)/2 and curl=(d ay/dx-d ax/dy)/2 using second- and fourth-
order centred differences. Compare with kappa after excluding an eight-pixel
border. Report best affine D=s*kappa+b, relative RMS residual, curl RMS and
raw D-kappa RMS. This is a convention DIAGNOSTIC, not permission to rescale.
Tight differential-consistency gate: |abs(s)-1|<.02, residual RMS<.02 times
std(kappa), curl RMS<.02 times std(kappa), same preferred convention up to
global sign for both derivative orders. A nonzero b requires a documented
boundary/zero-mode explanation, not automatic subtraction from measured gas.
If gates fail, label map normalization UNRESOLVED and preserve results.

Require finite matching arrays, positive angular pixel size, all 135 gold
image positions within WCS bounds (if not, report which; no extrapolation).
Test both ICRS and FK5(J2000) interpretations of missing RADESYS, report pixel
coordinate displacement, but do not choose a frame solely from convenience.
Do not evaluate gas deflections at image positions until convention gate passes.

Controls: analytic quadratic potential gives D=kappa and zero curl with both
difference orders to 1e-10 relative; a constant added deflection leaves D/curl
unchanged; MUTATE component sign and degrees-vs-arcseconds scaling must fail
the analytic control. Independent finite-difference orders must be reported.
One thread, CPU20s/wall30s, expected memory<150MB; no PM. Pin code, files,
source URLs/hashes, metadata, Python/astropy/numpy/scipy versions and outputs.
Commit this file ALONE before running. No theory-level pass/fail or novelty.
