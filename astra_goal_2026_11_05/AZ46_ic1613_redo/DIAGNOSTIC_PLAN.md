# AZ46 preliminary diagnosis — not a newly graded cube result

Lane12 explicitly requires investigating the two FN4a stage0 mismatches
before freezing a new cube test. This document freezes only that
investigation's operations; FROZEN_CRITERIA for a new physical test will
follow the diagnosis. Old labels, files and tolerances remain untouched.
Kappa=1/2 FITTED; not theory closed.

Read the local natural/robust FITS headers, the natural moment maps,
the saved FN4a mask/geometry and local authenticated Oh2015 tables.
Independently sum the natural moment0 map in32/64-row chunks, preserving
signed and positive-only sums. Parse each CLEAN beam from its own header;
do not apply the natural beam to the robust cube. Verify the moment-map
primary-beam correction from HISTORY. Use both the exact Gaussian beam
area and old1.1331 convention to separate rounding from real differences.
Check chunk agreement to1e-10 relative and raw float decoding against a
small independent astropy section. These are I/O checks, not physics gates.

Recompute the old moment-ring Vrot, sigma and surface-density profile
from its saved mask and original maps, matching its fixed geometry and
13.2arcsec rings. Reproduce its sm3 finite-difference drift calculation
and compare directly with archived S0b. Then diagnose the impact of
Oh2015 Eq4's smooth q=Sigma*sigma^2 parametrization on these SAME moment
profiles. Fit log q within the published Rmax, unweighted because profile
uncertainties were not supplied, with a positive three-parameter model;
this is a stated exploratory choice, not the paper's unpublished fit.
Do not tune fit range or weights toward16.9km/s. Report residuals and
parameters, not a new pass. The original moment1 is an intensity-weighted
velocity field, whereas Oh2015 derives its principal curves from bulk
velocity fields. Equality is not established by smoothing alone.

Primary-source browser readings (no files downloaded):

- https://arxiv.org/html/1208.5834, Hunter2012 sectionsIV.1/IV.2 and
  Table4: robust map conversion4.61, log summed map flux6.86,
  log HI mass7.53 for IC1613; mean natural/robust mass difference11%.
- https://arxiv.org/html/1502.01281, Oh2015 sectionsIII.1.2/III.2,
  Eqs3-5 and Table2: smoothed drift, gas factor1.4, Mgas5.93e7,
  Rmax2.71kpc and corrected velocity16.9km/s.

The full origin of a remaining table-to-map discrepancy is UNKNOWN
unless these operations identify it. An approximate numerical factor
alone is not proof of a helium, inclination or calibration error. Missing
bulk-field products, numeric fitted profiles, or robust moment maps
needed for a new benchmark go to NEEDS_OWNER; no acquisition here.
