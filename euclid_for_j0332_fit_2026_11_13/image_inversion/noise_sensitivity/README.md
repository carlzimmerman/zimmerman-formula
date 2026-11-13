# Correlated-noise sensitivity adapter (paused pending corrected inversion)

run.py subclasses the root inversion, without editing it. It applies a separable AR(1) innovation stencil to FULL standardized data and design matrices, then retains only output pixels whose full2x2 stencil lies within original likelihood mask. This avoids contaminant/mask bleeding. For correlation r=.23:

w(i,j)=[z(i,j)-r*z(i-1,j)-r*z(i,j-1)+r²*z(i-1,j-1)]/(1-r²).

The stationary separable covariance model has unit diagonal, C(dx,dy)=r^(|dx|+|dy|). A second optionalstress uses standardized amplitudes divided by .674. This .674scale was measured in maskedbackground and is NOT a physical estimate of fullnoise including sourcePoisson or modelresiduals. Retainedmask6420pixels,vs6711original. The stencil is a sensitivity model; it is not asserted to be true detector covariance. Missing boundary innovations are conditioned/excluded; this does not calculate the exact marginal covariance determinant for an arbitrary perforatedmask. The constant normalizer correction uses triangular innovationdiagonal1/[(1-r²)*scale]. Compare AQUAL/SIE under identical adaptermask only; do not compare absolute evidence numbers to differentlymasked diagonalrun.

Proper source and nuisance priors unchanged. SIEbaseline sourceprecision is reoptimized, then AQUAL mass/shear/sourceprecision is reoptimized with same mass/shear priors as rootstellarpriorrun. Heldoutcounterimage test uses diagonal originalRMS and fixes mass/shear to rootbest while reoptimizing sourceprecision after removing49counterimagepixels. Covariance/regularization hyperparameters are not jointlymarginalized.

adapter_zero_correlation_test.json verifies r=0,scale1 exactly reproduces parent diagonal solver's score,chi²,priorpenalty,sky,lens amplitude at an identical6420pixelmask.

## Invalidated pre-correction run

Initial optimization stopped on rootnotification that parent's bilinear sourcewindow used a discontinuous hardcut at edge nodecentres. STOPPED_INVALID_HARDCUT.json records oldmodulehash and UTC. No AQUALsensitivity solution completed; initialSIE stdout and any partialoutputs MUST NOT be used as finalfit evidence. Rerun after root supplies corrected inversion and rootreferencefit. Inputs and parentmodules were untouched.
