# Reconstructed NGC5023 spiral profiles

Use `run002/profiles.json`; `run001` is preserved and superseded.
This is a Figure11 reconstruction, not the recovered preferred TiRiFiC file.
All files belong to checkpoint `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`.

The exact arXiv1306.5312v1 archive supplies Figure11 and Table4. Twenty
plotted radial nodes span approximately0–6arcmin. Their image locations
are modeled as uniform0–360arcsec nodes; radius uncertainty is declared
as±1arcsec. Linear interpolation is the baseline reconstruction, not a
recovered `INTY` card. Preserve the decreasing **unwrapped phases** during
interpolation; wrap angular differences only when evaluating brightness.

Black dashed is Arm1: central width13arcsec, phase390.8degrees,
height14±9arcsec, nominal mass4.9e7Msun. Red solid is Arm2: central
width10arcsec, phase497.9degrees, height9±6arcsec, mass4.3e7Msun.
The disk height is9.1±3arcsec. Both arms share the disk rotation and
orientation. The final lag is−9.4±3.8km/s/kpc; the10km/s dispersion
includes instrumental effects. Do not add the full channel broadening
again to a10km/s effective Gaussian without identifying that duplication.

Table4's width deviations23/25arcsec and phase deviation7.5degrees are
visual one-parameter estimates, not independent per-ring Gaussian priors.
Digitization envelopes are separate: width±0.4arcsec, phase±2degrees,
amplitude±1e-5Jy km/s/arcsec². These deliberately cover line thickness,
axis/endpoint blending and low-amplitude truncation; they are not standard
errors. Raw readings and exact central anchors remain in the JSON.

## Documented TiRiFiC dictionary

[Official author documentation](https://gigjozsa.github.io/tirific/model_geometry.html),
exact response pinned in `TIRIFIC_SOURCE.json`, describes arc-length
Gaussian width `GAkD=w` in arcsec, phase `GAkP` in degrees and peak
`GAkA=A` in Jy km/s/arcsec²:

`B_arm(R,psi)=A(R)exp[-delta(psi,phase)^2/(2(w(R)/R)^2)]`.

Phase zero is the approaching major axis. For the root renderer's
receding-major azimuth and specified basis, matrix multiplication of
the documented inclination and PA rotations gives

`phi_root=psi_TiRiFiC+pi`, `Z_root=-Z_TiRiFiC`.

The line-of-sight velocity is consequently
`V_los=+Vrot*sin(i)*cos(phi_root)`. The height sign cancels for even
vertical profiles and a lag depending on absolute height.

Documented `LTYPE=3` means `H(Z)=exp(-abs(Z)/h)/(2h)`. The related
recovered author base model uses3; that supports an exponential
reconstruction but does not authenticate the missing preferred file.
The documented default radial interpolation is linear; the first node
is0. The documentation is current and response-pinned, not certified
as the exact2013 executable version.

## Normalization cross-check

The integrated minimal-wrapped Gaussian over a complete ring is
`sqrt(2pi)*w*erf(pi*R/(sqrt(2)*w))`. Piecewise adaptive radial integration
of the digitized amplitudes yields4.78037 and4.15813Jy km/s. With the
paper's6.6Mpc distance and standard HI flux conversion these correspond
to4.90597e7 and4.26738e7Msun, within0.13% and0.76% of Table4. No
renormalization or fitted parameter was used. The distance enters only
this source-consistency benchmark.

`flux_run001` also compares direct angular quadrature and a20001-point
radial trapezoid, with all declared checks passing. A centered90degree
wedge is an optional structural diagnostic, not a recovered azimuth-card
restriction. Its small nominal flux difference cannot settle the missing
card by itself. The current data do not supply a joint arm-profile
covariance or exact component-independent uncertainty distribution.
