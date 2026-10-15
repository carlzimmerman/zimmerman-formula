# CFG798: Herschel/HIFI as an archival dish antenna at 541.7 / 595.5 GHz (feasibility only)

**Verdict (frozen rule): FEASIBLE-WITH-REPROCESSING at 541.7 GHz (canonical). Below the hours threshold at 595.5 GHz (alt).
Not feasible "clean".** No archive data reach the kill line.

**What was counted.** `cfg798_query.py` sent one TAP query to the public ESA HSA (`hsa.metadata_expert_panels` ×
`v_active_observation`) and returned 2800 active HIFI band 1a/1b observations.
- Matches are in `cfg798_matches.csv` (147 rows).
- HSA `duration` is in milliseconds (checked against start and end times).
- Integration time = 0.5 × duration × coverage fraction. For spectral scans the coverage fraction is the share of the LO
  span that puts the target in a sideband. This is an accounting step and is not written in the criteria.

| target | public obs covering it | Tier A (survives std pipeline) | Tier B (needs Level-1 reprocessing) |
|---|---|---|---|
| 541.7 GHz | 95 | **0 h** | **13.1 h** (DBS/FastDBS point 7.6 h, DBS spectral scans 4.7 h, load-chop-ref scans 0.6 h) |
| 595.5 GHz | 52 | **0 h** | **5.8 h** (< 10 h threshold) |

Not a single band-1 frequency-switch-noRef or load-chop-noRef observation covers either line.
- Every match uses a sky reference.
- The signal does not depend on the target, so the OFF subtraction removes it (frozen switching rule).
- Report only: about 580 public observations (264 archive hours) touch the ±1% window around 541.7 GHz. That is a scan.

**Reach** (5σ ε_min; `cfg798.py`; S = power suppression, T_DSB = 80 | 150 K provisional; B = 1.1 MHz WBS; H+V combined):

| target, hours | S = 10 | S = 50 (primary) | S = 1000 |
|---|---|---|---|
| 541.7, 13.1 h | 2.5–3.5e-12 | **5.7–7.8e-12** | 2.5–3.5e-11 |
| 595.5, 5.8 h | 3.1–4.3e-12 | 7.0–9.6e-12 | 3.1–4.3e-11 |

- Every case covers the CFG795 converter window (4e-9) by more than 100×.
- The primary case misses the framework kill line (1e-12) by about 8×. Even S = 10 misses it.
- An archival null would therefore close the converter window. It would not test the kill line.
- K1 PASS (4.39e7/day). MUTATE ρ = 0 bites.

**Caveats that decide whether "with reprocessing" is real.** None of these is quantified here.
1. **DBS cancellation.** The chop throw is 3′. The emission spread is about σ/c ≈ 160″. ON and OFF see similar flux, so
   the cancellation is only partial and the residual is unknown. The clean route is to stop HIPE before the reference
   subtraction and calibrate each phase against the internal hot/cold loads. That keeps the full signal but leaves
   strong baselines.
2. **Geometry.** S = 50 for a parabolic primary is a literature value (provisional). The 39″ HIFI beam against the
   160″ emission spread alone is roughly 20× of mode mismatch.
3. **The radiometer limit is optimistic.** The stack mixes 95 observations at different LOs and IFs, so standing waves
   will set the floor.

**Next step** (a separate lane; downloads need approval):
- Pull Level-1 products for the 95 obsids at 541.7 GHz. The largest are 1342194493 (Mars), 1342213736 (NGC1068),
  1342246494, 1342246480/81/82 (IRC+10216), 1342210758, and the DBS spectral scans 1342250735, 1342244791 and
  1342191481. The full list is in the CSV.
- Re-run the HIFI pipeline without `doRefSubtract`.
- Undo the LSR/source Doppler correction to get the spacecraft frame, and map each spectrum to RF using its own LO and
  sideband.
- Mask LO spurs. Fit the 90–100 MHz standing waves.
- Drop LO ≈ 549.3 GHz, where the image of the 556.94 GHz H₂O line lands on the same IF (7.6 GHz) as 541.7 GHz.
- Stack, and look for a line about 1 MHz wide that is fixed in the spacecraft frame and sits in the same RF place
  across all targets.
- Test the pipeline first on a channel injected at 541.7 GHz.

κ = ½ fitted; not theory closed. External numbers are provisional.
