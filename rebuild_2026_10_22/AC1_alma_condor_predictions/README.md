# AC1: pre-data predictions for the ALMA release of 2026-11-06

Criteria `FROZEN_CRITERIA.md`, committed alone first (57d3ac6b64). `ac1_predict.py`: all checks PASS, under 1 GB, under a minute, one process. MUTATE (R31 x 10) fails K7 and exits 1.

κ = ½ FITTED. Footings never pooled. One disc excludes no model. Not theory closed. Nothing here says the data favour the framework. These are predictions; no pixel of this MOUS has been read.

**Deposited 2026-11-01 as PAPER66 v1.0, DOI 10.5281/zenodo.23865084, before the release.** **v1.1, DOI 10.5281/zenodo.23867238, corrects the 3D forecast.** **v1.2, DOI 10.5281/zenodo.23868979, reverses the detection forecast from measured noise.**

## Findings
1. **The release's target is U4_28473 (z 2.52), not U4_27928.** Phase centre offset 0.002″ against 7.361″. CFG570 matched U4_27928 inside the field of view. CFG806 and every seal are unchanged, but the record's wording "U4_27928's ALMA data" should be read as a serendipitous off-axis reading.
2. **U4_27928 will probably score nothing.** At its empirical gas (log M_gas 10.51) the frozen aperture reads S/N 0.16. The 3σ limit is log M_gas 11.79 (α_CO 4.36) or 11.15 (α_CO 1), against framework requirements at most 11.33 across the Hα V_c cases (F-DESI, F-flat, every kernel and gas row). So the α 4.36 limit lies above every requirement; the α 1 limit lies below only the fastest case (V_c 373). Same class as D4's forecast.
3. **U4_28473 tests its mass budget, not a₀(z).** With the published CO flux, log M_gas is 11.33 (α 4.36) or 10.69 (α 1). At 3 kpc, Newtonian baryons alone reach 431 to 846 km/s across the input branches (the commit message of 02ffa20dd8 says 827, from the printed subset; 846 is the JSON's maximum). Readings differ by far less: at lg M★ 11.11, S2, α 1, n = 1 flat a₀ reads 441, F-DESI 439, R-H 463, route N 432.
4. **My expectation "G1 passes" is not supported as frozen.** A moment-0 aperture over ±500 km/s peaks at S/N 1.86 for a smooth disc. A rotation-matched 3D statistic reads 9.6. G1's frozen wording cites CFG806 A-U13, a moment-0 mask. Changing that needs a dated owner addendum before data.

## Disclosed changes after the criteria, before any data
- K2's first run failed on a cell-count threshold (n > 100) I wrote into the script, which is not in the criteria; 82 non-FLOOR cells matched exactly. The threshold was replaced by matching all cells plus FLOOR flags (0 of 168 differ), and the tolerance tightened to the criteria's 1e-12.
- Added as information, no frozen weight: route N on U4_27928 and α_CO,req at V_c 430 km/s, R 3 kpc for U4_28473; moment-0 aperture scan and matched 3D forecast.
- In MUTATE, K6 also fails (C 0.736): S3's library reads the same `--mutate` flag and mutates its solver. Harmless to the lane's normal outputs.

## Scoring harness
`ac1_score.py`, tested on MOCK only: selftest 10 of 10 (`ac1_score_selftest.out`), seeds at archive noise in `ac1_score_power.out`. Smooth disc: G1-3D passes 1 of 7, moment-0 0 of 7. Compact: 6 of 7. No line: 0 of 7. Quoted V_c errors understate the MOCK scatter. `ADDENDUM_G1.md` is filed (owner, 2026-11-01): G1-3D decides on real cubes. Not tested on a real pipeline cube; at finer real pixels memory may exceed the 1.06 GB seen here. A cube of tens of GB may not fit: 27 GB free on 2026-11-01. C1 injection starts at the truth, so it flatters recovery.

## Validation on a real cube (2026-11-01, owner's yes; scores no prediction)
Public cube of the same galaxy: 2021.1.01291.S (Tadaki), spw25, 6.52 GB, sha256 e047f98d…, beam 0.48″ x 0.43″, deleted after the run. `ac1_score_VALIDATION*`, `ac1_noise_check.py`.
- **Code works on a pipeline product:** 50 s, 0.52 GB. MUTATE bites (S/N 0). G1 frozen S/N 50.8, G1-3D 14.2.
- **Known answer recovered:** 1″ aperture 0.92 ± 0.12 and ±500 km/s integrated 0.89 Jy km/s against published 0.79 ± 0.08; line centroid z 2.52365 against z_CO 2.523 ± 0.004. The 3D mask holds 0.53 (ratio 0.67, flagged): a thresholded mask misses faint flux, so its flux check runs low.
- **Fit not usable as a speed:** beam 3.9 kpc against R_d 0.93 kpc. σ0 193–207 and P-B 706–711 are beam-inflated, and the Tadaki-inclination branch hits the V_f bound. The validity gate passed the other branch, so the gate alone does not catch this; a warning now prints. The integrated line's half-max width is 788 km/s, which is an unframed look, not a measurement or a score.
- **Archive sensitivity is not the cube's noise:** measured 0.355 mJy/beam per 10 km/s, flat to 120 km/s bins, against the listed 1.30: 3.7 x. Every forecast in this lane uses the listed 0.434 for the Nov 6 unit. Same class of error as CFG970's K2.
- **MOCK at lower noise, smooth disc, 4 seeds each:** noise/2: G1-3D 4 of 4, moment-0 0 of 4, V_c 418–456 of 430. Noise/3.7: G1-3D 4 of 4, moment-0 4 of 4, V_c 428–445. No line: 0 of 4 at both. So the "likely non-detection" in PAPER66 v1.1 holds only at the listed noise. The real noise of the Nov 6 unit is unknown until release. Radiometer scaling from this cube by exposure gives about 0.17, not a measurement.

## Same-programme noise check (2026-11-01, owner's yes; 2 GB streamed, deleted)
Public CONDOR unit uid://A001/X3788/Xbfce, UDS17159, spw23, first 30 channels (`ac1_condor_noise.py`, `.out`, `_results.json`). Measured 0.162 mJy/beam per 10 km/s against listed 0.411: 2.54 x. Real beam 0.21″ x 0.16″ against the listed 0.126″. Channel edges may read a little high, so 2.54 may be low.

**MOCK with those two ratios applied to the Nov 6 unit** (noise 0.171, beam 0.109″ x 0.085″, 6 seeds, `ac1_score_power_div2.54_condorbeam*`):
| disc | moment-0 G1 | G1-3D | fit scored | V_c of 430 |
|---|---|---|---|---|
| smooth, R_e 1.56 kpc | 6 of 6 | 6 of 6 | 6 of 6 | 408–444 |
| compact, R_e 0.8 kpc | 6 of 6 | 6 of 6 | 6 of 6 | 413–438 |
| no line | 0 of 6 | 0 of 6 | none | |

**This reverses PAPER66 v1.1's "likely non-detection".** Detection and a usable V_c are now the expected outcome, if the Nov 6 unit resembles its sister. That is an inference from one sister unit, not the unit's own noise. Smooth 90 % radii are 3.2–5.1 kpc, so G2 passes there. Hand scaling for U4_27928: aperture noise falls by about 2.54 x 1.5, so S/N about 0.6 at log M_gas 10.51; G1 still fails, Prediction A stands. Sister cube is 31 GB per spw at 0.025″ pixels; at about 0.013″ pixels the Nov 6 cube would be near 115 GB per spw, an estimate.

## Not done
No z rule for route N; its reading is an extrapolation. Masses and fluxes keep the authors' reductions. E, E-CCBH, BH-k3 are not recomputed at z 2.52.

## Files
`FROZEN_CRITERIA.md`, `ac1_predict.py`, `ac1_predict.out`, `ac1_results.json`, `ac1_predict_MUTATE.out`, `ac1_MUTATE_results.json`.
