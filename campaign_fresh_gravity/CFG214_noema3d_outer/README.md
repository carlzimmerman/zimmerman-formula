# CFG214 — NOEMA3D outer-radius test: GATE-LIMITED, NON-DIAGNOSTIC AS FROZEN

- **Criteria:** `FROZEN_CRITERIA.md` (8340f3750 + addendum 1, 68916b51e), committed before any curve value. **κ = ½ FITTED, NOT DERIVED.**
- **Inputs:** the data chat's digitised Fig. 5 (paper 1; `data_assembly/noema3d/curves/`, commit fb41406a1). Hashes are checked in the script (C3a).
- **Run:** `python3 campaign_fresh_gravity/CFG214_noema3d_outer/cfg214_outer.py`, under 1 s. The main run passes 4/4 checks. `MUTATE=1` (every digitised model V × 1.1) passes 5/5.

## Bottom line

**Only 1 of 10 galaxies passes the frozen 5% gate, so no median δ with a bootstrap CI can be formed and no law verdict is given.** Nine galaxies are excluded, as frozen.

| galaxy | model V(R_e,disk)/sin i | Table 3 V_c | deviation | gate |
|---|---|---|---|---|
| G4_38065 | 320 | 299 | +7.1% | FAIL |
| **G4_38232** | 236 (sides 143, 329) | 234 | +0.9% | PASS |
| G4_20371 | 202 | 263 | −23.1% | FAIL |
| G4_23011 | 214 | 295 | −27.5% | FAIL |
| GN4_24517 | 246 | 333 | −26.1% | FAIL |
| GN4_18574 | 142 | 197 | −28.1% | FAIL |
| G4_24078 | 189 | 339 | −44.3% | FAIL |
| GN4_32842 | 316 | 379 | −16.6% | FAIL |
| G4_17555 | 135 | 249 | −45.6% | FAIL |
| G4_37375 | 193 | 248 | −22.0% | FAIL |

- The gate recomputed here agrees with the data chat's V2 for every galaxy (C3b).
- **The one passing galaxy passes by cancellation.** G4_38232's model line has strongly asymmetric sides (143 and 329 km/s after /sin i). The data chat lists its three overlapping series as the least reliable trace.
- **Why the gate fails (as read from the data chat's README).**
  - The printed curve is the observed line-of-sight velocity.
  - The drawn model line is the best-fit 3D cube read out like the data, i.e. the BEAM-SMEARED projection.
  - Table 3's V_c is the intrinsic circular velocity. Comparing the two at R_e,disk, where smearing matters most, mostly gives negative deviations.
  - The data chat's post-hoc diagnostic finds the largest deviations where R_e,disk/beam is small. That is consistent with beam smearing but not proven.
- **So the frozen test as designed cannot be evaluated with these data.** The gate excludes galaxies for reasons of resolution, not of physics.

## What would be needed (not run here)

- A beam-aware comparison needs a NEW frozen criterion. The proper form forward-models each law's predicted rotation curve through the same beam and compares it with the data markers.
- The gate outcome is now known to me, so any relaxation would be post hoc. It would be reported beside this result and never substituted for it.

## Controls and disclosure

- **C1, C2:** the disc's Keplerian check and the on-law δ = 0 check pass.
- **C3a:** the digitised files match the hashes the data chat sent.
- **First-run fix, kept:** the first run's C3a compared the outermost-radius file with a hash that SHA256SUMS does not list, and failed. The check now uses the hashes from the data chat's message. The first run is kept as `*_firstrun*`.
- **C4** (the raster control) was carried out by the data chat: rms dV 0.15–0.18 km/s, and axis calibration residuals under 0.3%. These are far below 5% of the median V_c, so the result is not digitisation-limited.
