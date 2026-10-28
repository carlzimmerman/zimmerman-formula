# Observational recovery contract (2026-10-28)

Written before acquiring new numerical tables. Scope: four HO2 SLUGGS centrals (M87/NGC4486, NGC4365, NGC4374, NGC5846); independent IC1613 inclination; potential additional X-ray groups. Broad user authorization supersedes earlier no-download rule only for small public research sources and tables. Existing lanes stay read-only. No commits: coordinator directs this because .git is read-only.

## Tests and outcomes

1. Recover measured X-ray gas temperatures from primary published spectroscopy, retaining asymmetric uncertainties, extraction aperture, model, source version and covariance/use limitations. Virial temperatures inferred from optical dispersions do not count. A temperature without radial support is data recovery, not a clean Jeans prediction test.
2. Four-target gas prediction: if a measured kT and supported gas density slope/core/temperature profile span the GC radii, compare the hydrostatic mass/potential implied by those independent measurements with the existing GC profiles. Any extrapolation, assumed beta model or fixed core must be reported separately and cannot upgrade the original held-out grade. Recover the four-target input list even when a full test is blocked.
3. IC1613: distinguish morphology/photometric inclinations, stellar-kinematic inclination estimates, HI tilted-ring fitted inclinations, and estimates relying on equilibrium/BTFR. Quantify conditional velocity and acceleration shifts only with explicit assumptions. No inclination can repair an independent dispersion test without rechecking its mass/anisotropy/rotation support assumptions.
4. Groups: identify genuinely new X-ray sources vs existing matched systems, preserve selection and sky footprint. No sample-size or power upgrade without common schema, unique associations, matched sigma support, measurement homogeneity, and optical completeness. Published gas masses remain externally calibrated when appropriate.

## Standing assumptions

- RAW: published line-of-sight velocities, X-ray spectra and fitted spectral temperatures (measurement errors retained).
- SURVEY-CALIBRATION: distances, SPS masses, spectral plasma/abundance models, deprojection geometry, inclination estimators, selection functions.
- FRAMEWORK-NATIVE: canonical a0=9.3603e-11, alt=1.1312e-10 m/s2 reported separately when a0 matters; kappa=1/2 fitted.
- Externally calibrated: R500/HSE/NFW quantities, scaling-derived gas masses or temperatures. No hidden standard-MOND yardsticks, parameter scans, new fitted knobs or theory-closed claims.

## Reproducibility

Store public small tables/necessary extracted inputs under this directory, record URL/date/version and SHA256, and regenerate all derived numbers with a deterministic offline script and a mutation check. Primary text may be retained as authorized local source material only if useful; reports summarize rather than republish article text. Record source acquisition failures and bounds honestly.
