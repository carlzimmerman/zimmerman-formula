# Independent Draco proper-motion screen

Use public Vitral et al.2024 DRACO_BINS.dat, Zenodo11111113, downloaded intact and checked against published MD5. Use ONLY its five PM rows (radial/tangential dispersions and errors in mas/yr); do not add its overlapping Walker LOS bins as independent data. These binned PM constraints are not a reconstructed star-level/covariance likelihood. Report an uncorrelated error-weighted squared-residual diagnostic, NOT an exclusion significance.

Keep LVD81.55kpc distance and fixed inferred physical envelopes from fit_002/core_fraction_001/core_001; no refit to PM, no inconsistent free distance rescaling. Convert modeled km/s to mas/yr by4.74047 D_kpc. Angular projected radii are tested both as circular R=D alpha and using LVD ellipticity/PA with each tabulated sky angle. This bracketing is a geometry sensitivity, not a correct axisymmetric PM projection. A spherical Plummer tracer and fixed beta cannot capture Draco's rotation/flattening or full observed distribution function. No DF-viability inference.

Spherical projected weights for beta constant: LOS=1-beta R²/r², PMR=1-beta+beta R²/r², PMT=1-beta. Integrate the SAME Jeans pressure against each weight, with observed number-density projection as denominator. At beta0 all three agree. Test beta=-.5,0 from the previous fits only; do not use the unphysical positive-constant-beta cored moment as an accepted model.

Screen free Plummer, half-supply Plummer, best-grid compact-cut plus extended halo, full measured cut plus fitted halo, and resolved full Draco snapshot. Count gravity once. An apparent LOS fit is not called data-accepted unless this held-out check is also understood. Final four-dwarf closure remains open even if these ten component values are reproduced.
