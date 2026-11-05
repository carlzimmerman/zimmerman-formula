# AZ46 amendments

## A1 — spectral metadata, after raw prototype and before any cube fits

The first8x8 raw prototype copied FN4a's linear velocity-axis expression.
Inspection of the actual FELO-HEL header and Astropy's spectral WCS finds
that the natural cube's optical-velocity mapping is nonlinear: its values
differ from that linear expression by up to0.06207714km/s across the107
channels. This was found after raw-data inspection, not from a fitted or
graded cube result. No new cube fit or local-cube verdict exists.

For the full redo interpret “native spectral channels” as their FITS WCS
velocities, separately for each cube. Use WCS(header).spectral values in
m/s converted to km/s. Preserve and report the difference from the old
linear expression. Check those values independently with the optical-
velocity/frequency mapping implied by the header reference and increment:
if delta=(pixel+1-CRPIX3)*CDELT3 and v0=CRVAL3, then
v=v0+delta/[1-delta/(c+v0)], with c=299792458m/s. Report their numerical
agreement; this parser comparison is not an observational acceptance gate.

Keep the actual107 channels, masks/noise procedure, channel sampling,
model families, physical brackets and every acceptance/convergence line
unchanged. In particular no failed beam tolerance is relaxed. The first
raw prototype remains a local development artifact under raw_contract/;
it is not eligible as production input after the source-identity change.
A fresh-tag raw pilot and resume/convergence checks must be regenerated.

Kappa=1/2 FITTED; not theory closed.
