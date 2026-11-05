# Results and next steps — AzTEC/C159

Status: completed conditional forecast, 2026-11-04. No further computation is needed before new independent inputs arrive.

## Results

- At 7.5 kpc: canonical FDESI 374.4 km/s; matched MOND 382.2 km/s; the published illustrative baryons+NFW model 443.6 km/s.
- Outer values extrapolate the measured inner mass profiles. They are not measured outer velocities or unconditional predictions.
- A 4.1% gas-mass reduction and 3.4% stellar-mass increase let MOND track the nominal FDESI curve within 3.5 km/s over 1–7.5 kpc.
- Approximate simulated-cube sensitivity does not support a decisive FDESI/MOND separation with the currently listed July data quality. Particular NFW halos are more testable, but halo and baryonic freedom matter.
- F-flat and matched MOND remain identical under the adopted law.

## Next steps, in priority order

1. Obtain the independent JWST stellar mass map and gas conversion-factor constraints when available. Do not use a gravity-dependent dynamical mass as an independent baryonic prior.
2. Recheck ALMA release metadata around July 20, 2027 for 2023.1.00835.S. Fit the released [CII] visibilities/cube jointly for inclination, surface brightness, rotation, dispersion and noncircular motions. Establish the actual usable outer radius before interpreting a 7.5-kpc prediction.
3. Recheck the September 24, 2027 release of 2025.1.00827.S. Incorporate CO excitation constraints and propagate gas conversion-factor uncertainties; percent-level mass precision is not currently guaranteed.
4. Compare FDESI, matched MOND and a stated halo family using identical nuisance parameters and priors. Calibrate discrimination with injection/recovery through the actual sampling and noise, not the present approximate cube-distance statistic.
5. Proceed to a strong model-selection claim only if the differences survive those uncertainties. The single-bin 7.5-kpc MOND benchmark is a combined error below 2.6 km/s for a nominal three-sigma distinction; it is not an achieved precision forecast.

No monitoring or automated downloads have been scheduled. Dates are public-release metadata, not guaranteed observing dates.

## Saved evidence

- `REPORT.md`: interpretation, sources, limits and observing context.
- `calculate.py` and `contract.json`: deterministic computation and declared scope.
- `inputs/archive_metadata.csv`: retrieved archive metadata.
- `run01/predictions.csv`, `mass_size_grid.csv`, `sensitivity.csv`, `results.json`: numerical results.
- `run01/manifest.json`: bounded-run provenance and hashes. Validate using the computation-audit skill's `validate_manifest.py` with this repository as `--root`.
