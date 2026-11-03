# LAM2_gas_poor_lambda_estimator: STAGE 0 PASS. 2546 gas-poor galaxies pass the quality cut, 428 of them slow rotators; 95 % of all slow rotators in the cut are gas-poor. Stage 1 waits on wave 1 (spectra and pPXF, owner yes per item)

Criteria `FROZEN_CRITERIA.md` (fa14da563a), amendment A1 in `AMENDMENTS.md`, written before any count. Files: `lam2_fetch.py` (query), `lam2_stage0.py`, `.out`, `.json`. Not a gravity test. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

| gate | gas-poor (graded) | gas-bearing (row) |
|---|---|---|
| N after quality cut | 2546 | 778 |
| slow / fast | 428 / 2118 (0.168) | 23 / 755 (0.030) |
| F1 (>= 1000, >= 100 slow) | PASS | FAIL |
| F2 sigma(AUC) at 0.75, need <= 0.0167 | 0.0143, PASS | 0.0596, FAIL |

Counts: 5811 matched rows give 5732 galaxies after one row per mangaid. 49 have no galSpecLine row. The quality cut passes 3365. Gas-poor EW bins: [<1 A) 1633 with 340 slow, [1, 2) 678 with 68, [2, 3) 235 with 20.

## Reading
- The gas-poor sample is where the question can be asked at all. Almost every slow rotator in the cut is gas-poor, which is why the paper's H-alpha input cannot reach them.
- F2 passes with little margin (0.0143 against 0.0167). E3's 0.05 gain is about 3.5 sigma of one model's AUC, and E4's 0.03 is about 2 sigma.
- The gas-bearing comparison will be weak: 23 slow rotators. Its rows are reported, not graded, as frozen, and should be read as indicative.
- The first run crashed on parsing specobjid, which overflows int64; the fix only reads the ids as text. No count had printed.

## Wave 1, for the owner
- DR17 spec-lite for the 3324 quality galaxies with a line row, about 0.17 MB each, about 570 MB.
- `pip install ppxf` and its bundled templates.
- ATLAS3D positions (Cappellari+2011 table 3, VizieR, tens of kB) and an SDSS SpecObj query at those positions.
