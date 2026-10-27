# CFG407 AMENDMENT A1 (pre-result; committed alone before any X-COP number exists)

**What happened.** The first execution of `cfg407_xcop_outer.py` (committed in addeed8f74) stopped while loading data. It hit a FileNotFoundError on `A1644_mstar.fits`, after K1 and K2 had passed (both exact, 0.0) and before any X-COP quantity was computed. No M_HSE in the band, no X43 prediction for an X-COP cluster, and no Δ had been formed. Nothing graded exists.

**Correction to the criteria's data section.** That section said every cluster has a `*_mstar.fits`. It does not. My pre-freeze check opened only A2142's files. The on-disk inventory is:
- `*_hydro_mass.fits` and `*_fgas_profile.fits`: all 12 clusters.
- `*_mstar.fits`: **7 clusters** (A85, A644, A1795, A2029, A2142, A2319, ZW1215).
- **Missing stars for 5:** A1644, A2255, A3158, A3266, RXC1825.

This matches CS1's own note ("7 with stars; 5 more as an M★ = 0 variant").

**Effect.**
- **PRIMARY and V-NAT: unchanged.** Both use X43's recipe, stars = 0.20 × gas, and read no stellar file.
- **V-INNER: unchanged.**

**Amended V-MEAS (reported variant, not graded):**
- **V-MEAS (all 12):** measured gas as frozen. Stars are the measured MSTAR where the file exists. For the 5 clusters without one, stars = 0.20 × measured gas, X43's own stellar fraction (declared fallback).
- **V-MEAS-7 (added, reported):** the same, restricted to the 7 clusters with measured stars. Its se uses N = 7.

**Script change, implementing only this:** the loader reads `*_mstar.fits` only when it exists. `baryons(…, "MEAS")` uses the fallback when it does not. V-MEAS-7 is computed on the 7-cluster subset. No other line changes. Readings, controls, radii, statistic and cells are as frozen. The control count printed by the earlier crashed run (2/2) is superseded by the full run.

κ = ½ FITTED; not theory closed.
