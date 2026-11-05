# VC875 results and next steps

Status: conditional forecast completed 2026-11-04. The detailed analysis supersedes the optimistic initial shortlist.

## Results

- At 3.84 kpc, nominal FDESI predicts 245.8 km/s versus matched MOND 251.6 km/s; at 5 kpc, 248.7 versus 255.8 km/s.
- Small baryonic normalization changes let MOND match within 2.0 km/s, and a constrained NFW example within 4.64 km/s over the fitted radial range.
- The high-resolution release does not have a demonstrated ability to distinguish these models after nuisance uncertainties. Native angular resolution alone does not ensure diffuse-emission sensitivity.
- Older measured rotation velocities remain below the fiducial mass-based forecast even under the report's illustrative pressure corrections. The nominal mass model is not validated by those data.
- run02 is the completed calculation; run01 is a retained serialization failure, not a successful final result.

## Next steps

1. Recheck the high-resolution observing unit uid://A001/X2d1f/X33a, listed for November 13, 2026 at 19:00 EST (November 14 at 00:00 UTC). This is a public-release date, not an observing date.
2. Combine the new data with the existing compact-array observations, checking weighting, recovered flux, actual beam/noise and outer-radius coverage.
3. Obtain an independent stellar mass map and gas-conversion constraints. Replace the provisional UV stellar-size proxy; investigate the existing mass/kinematic tension before claiming model preference.
4. Fit geometry, beam smearing, pressure support and noncircular motions consistently across FDESI, MOND and a stated halo family. Calibrate discrimination with injection/recovery using the actual data sampling.
5. Only upgrade this to a discriminating test if the remaining model difference exceeds the full propagated observational and baryonic uncertainty.

No monitoring is scheduled. REPORT.md contains source links and detailed assumptions; calculate_v2.py, contract_v2.json and run02 preserve the final computation.
