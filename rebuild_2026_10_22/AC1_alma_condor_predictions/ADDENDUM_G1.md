# AC1 addendum G1, FILED 2026-11-01 on the owner's approval ("Yes, file it"), PRE-DATA

Committed before any byte of the MOUS has been read. It governs U4_28473 only. The frozen moment-0 G1 is still printed beside it. FROZEN_CRITERIA.md is not edited. κ = ½ FITTED; one disc excludes no model; not theory closed.

## Why
At the archive sensitivity a smooth mock disc with the published flux never passes the frozen moment-0 G1 (0 of 7, S/N at most 2.2), because a ±500 km/s moment-0 adds noise across channels where a rotating disc has no line. A velocity-resolved statistic is the standard answer. This choice was made on MOCK cubes only.

## Ruling
1. **U4_28473 only.** U4_27928 stays under CFG806 and its addenda.
2. **G1 becomes G1-3D.** Smooth the continuum-subtracted cube spatially (0.15″ FWHM) and spectrally (100 km/s). Keep connected voxels ≥ 2.5σ containing a peak ≥ 4σ and touching a 0.5″ cylinder at the phase centre within ±500 km/s. Sum the unsmoothed flux. S/N = (S − null mean) / max(null sd, mask-sum noise), null = the same procedure at 200 off-source seeds. Pass at S/N ≥ 5 and z within 0.004 of 2.52455.
3. **The frozen moment-0 G1 is still printed** beside it, labelled. If the two differ, the report says so.
4. **Fit validity, new gate.** A branch is scored only if no V_f, R_t, σ0 or h sits at a bound, three starts agree within 15 %, moment-0 q is not clamped, and σ(V_c)/V_c ≤ 0.25. Otherwise "FIT NOT CONSTRAINED", no α_CO,req.
5. **G2 radius.** The 90 % flux radius of the mask, deprojected, replaces the farthest pixel, which noise components drive to tens of kpc on MOCK.
6. **V_c error.** Criteria's error is kept, and because MOCK shows it is too small (below), the report also gives the MOCK recovery scatter at the measured S/N. Readings use the larger of the two.

## What it buys, MOCK at archive noise (V_c 430 km/s, flux 0.79 Jy km/s; `ac1_score_power.out`, `ac1_score_selftest.out`)
| disc | moment-0 G1 passes | G1-3D passes | fit scored | recovered V_c |
|---|---|---|---|---|
| smooth, gas R_e 1.56 kpc | 0 of 7 | **1 of 7** | 1 of 7 | 455 ± 61 |
| compact, gas R_e 0.8 kpc | 0 of 7 | 6 of 7 | 4 of 7 | 419 ± 26, 439 ± 30, 369 ± 15, 386 ± 24 |
| no line | 0 of 7 | 0 of 7 | none | |

Selftest seed plus six power seeds in each row. Few seeds: these are rough rates.

**Read this before approving.** The addendum does not rescue a smooth disc. If Tadaki+23's R_e 1.56 kpc holds down to 0.066″, the likely result is still a non-detection, unless the emission is clumpy, which MOCK does not test. The compact recoveries scatter low, and one (369 ± 15) sits 4σ from truth, so the quoted errors understate the real spread. All compact 90 % radii lie below 3 kpc in the scored fits, so G2 fails and scoring would happen at about 2.3–2.9 kpc.

## Corrections this makes to my own earlier forecast
PAPER66 v1.0 quotes a rotation-matched 3D S/N of 9.6. That is an ideal matched filter with the true model known. A blind finder on the same disc passes 1 of 7. The paper's number is what it says, but it reads as far more promising than this.

## Alternatives considered, not taken
- **Keep the frozen G1** and accept "upper limit" as the likely result: cleanest, tests nothing.
- **Approve this:** scores if the gas is compact or clumpy.
- **Add imaging from visibilities with a taper:** not done or tested. It needs CASA, and A-U12 ruled out tapers for U4_27928.
