# FN4a_ic1613_cube_model: NOT EVALUABLE by the frozen rule (two stage-0 checks fail, and the free model misses its χ² line). Read post-result, the law fails IC 1613's cube at every inclination from 15° to 60°; the cube's own kinematics prefer 53.5°

Criteria `FROZEN_CRITERIA.md` (a616530a1a, committed alone before any download); fetch log, script and `AMENDMENTS.md` (A1–A9) committed before any number. Data: 7 of the 8 owner-approved files (`fn4a_fetch.json`). κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Label (frozen): NOT EVALUABLE
| Check | Result | Line |
|---|---|---|
| **S0a** HI mass from moment 0, D 0.7 Mpc | **FAIL**: 3.04e7 M☉ against Oh+15's 4.24e7 (M_gas / 1.4), ratio 0.716 | 10 % |
| **S0b** V(R_max = 2.71 kpc), drift-corrected (A2) | **FAIL**: 20.85 km/s against 16.9; uncorrected 16.10 | 2 km/s |
| **M_free** χ²_red on the beam grid | **FAIL**: 4.053 (318,102 on 78,568 voxels) | 1.5 |
| KA1 law mock at i 35° | PASS: LAW FITS THE CUBE, best i 35° (Δχ² +77), mock M_free χ²_red 0.885 | |
| KA2 mock at 0.505 × the law | PASS: GENUINE OVER-PREDICTION | |
| KA3 Newtonian baryons | PASS: Δχ² +65,165 (best at 55°) | > 83.7 |
| MUTATE, channels shuffled | BITES: M_free χ²_red 11.6, NOT EVALUABLE | |
| Rerun | `fn4a_s0.json`, `fit_free.json`, `fit_law_canonical.json` byte-identical | |

**The failures checked:**
- **S0a:** the cube agrees with its own moment map (244 Jy km/s inside the mask, 277 with an approximate primary-beam correction, against the map's 263). The 30 % gap is to Oh+15's quoted gas mass, not a reading error. The record's E −0.593 used Oh+15's mass. The cube's mass would make the law's prediction about 0.05 dex smaller, which does not reverse the row.
- **S0b:** the plain ring velocity, 16.10 km/s, matches Oh+15 within 0.8 km/s. My drift correction (A2: azimuthal means of moments 0 and 2, finite differences) adds 4.7 km/s at the steep HI edge, where Oh+15's smoothed profiles add about 1. The check was frozen on the corrected value, and it fails.
- **M_free:** IC 1613's HI is holed and turbulent. A thin rotating disc with 64 free rings leaves residuals four times the noise. KA1's mocks reach 0.885, so the excess is the galaxy, not the code.

## Post-result reading of the fits (no label; `fn4a.out`, `fits/`)
Δχ² of the law against M_free, by inclination (line χ²₀.₉₅(64) = 83.7):

| i (°) | 15 | 20 | 22.5 | 25 | 30 | 35 | 37.5 | 40 | 45 | 50 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M_law canonical | +14,798 | +74,743 | | +136,241 | +208,741 | +280,423 | | +352,606 | +417,821 | +436,964 | +420,033 |
| M_law+nc canonical | +993 | | +91,245 | | +181,790 | | +249,155 | | +294,051 | | +347,177 |
| M_law alt | +19,466 | +92,789 | | +159,002 | +235,917 | +311,211 | | +386,340 | +452,158 | +471,429 | +454,613 |
| M_law+nc alt | +5,606 | | +102,984 | | +205,565 | | +300,209 | | +370,303 | | +386,987 |

- **The law fits nowhere from 15° to 60°**, with or without non-circular terms, on either footing. Without the M_free line, the frozen rule reads GENUINE OVER-PREDICTION on both footings. Dividing every Δχ² by M_free's χ²_red of 4.05 still leaves the best case at +245, above the line.
- **The law's χ² keeps falling toward the 15° edge.** It wants an inclination below 15°, under every geometric and stellar measure on record (RF2 24.5–45.8°; MUSE 32 ± 11 and 36 ± 11).
- **The cube's own kinematics prefer i 53.5°** (M_free; PA 75.6°, centre 21″ from Oh+15's). That is the opposite direction from the one the law needs.
- **KA2 shows the cube can tell.** A galaxy rotating at 0.505 × the law (the record's E −0.593) is labelled GENUINE OVER-PREDICTION. The law does not hide in a low-inclination fit, as IN1's 1D band allowed.

So the inclination lever that UX4 called the only data route for IC 1613 does not rescue the law in the cube. The label stays NOT EVALUABLE, because the frozen stage-0 lines and the free model's χ² line were not met.

## Departures and limits
- `ic1613_ubvcalib.txt` was not obtainable (HTML page at every URL), so stars are V light at constant M/L (A1). The 1.9e8 M★ bracket at the best inclination is in `fits/fit_law_*.json`.
- **A code bug, found and fixed before any fit:** R_out first came out 0, because IC 1613's central HI hole broke a count from the centre. It is now the edge of the last ring with ≥ 50 % coverage (845″, 64 rings). The stage-0 numbers did not change.
- The robust-cube resolution check (reported, no line, in the criteria) was not run. Its beam differs, and the code carries the NA beam.
- **Memory:** stage 0 peaked at 1.13 GB RSS (the V-image coordinate grid), and the KA mocks at 1.4–1.8 GB, over the 1 GB guidance. One thread throughout.
- Pressure support uses azimuthal-mean profiles. It is large at the HI edge (A7). The non-circular terms use 6 radial nodes.

## Files
`fn4a_fetch.py`/`.json` (download), `fn4a_core.py` (model), `fn4a_prep.py` and `fn4a_s0.out`/`.json` (stage 0), `fn4a_fit.py` and `fits/fit_<stage>.json` (fits, copied from the gitignored `cache/`), `fn4a_report.py` and `fn4a.out`/`.json`. Run order: prep, `fit free`, then `law_canonical`, `law_alt`, `nc_canonical`, `nc_alt`, `newton`, `mutate`, `ka1`, `ka2`, then report. One thread each, about 1–8 minutes per stage.

κ = ½ FITTED. Not theory closed.
