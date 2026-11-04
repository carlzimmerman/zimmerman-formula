# AN2 diagnostic SG: does the grid error that delays the 3D sphere also delay the shapes? Frozen before any run. POST-RESULT, NOT BLIND

Follows SL (`SPHERE_LAG_RESULT.md`, f3f55780f6), which traced the sphere's 16-18 % lag behind AN1 to grid resolution. A diagnostic, not a grade: AN2 stays NO VERDICT and no label changes.

## Known before running
- Exact dust references, `an2_checks.ellipsoid` at d0 (1 − 0.0082) for the box mean, as SL used for the sphere (4.702 Gyr, reproduced today). Computed today, in Gyr:

| Key | e = 0 | A | B |
|---|---|---|---|
| 1e12 | 4.702 | 4.116 | 3.709 |
| 1e15 | 4.702 | 4.449 | 4.225 |

- The rows (hold on, 128^3) at 1e15, where SL found hold moves the sphere 0.15 %: A 5.028 (+13.0 % over exact dust), B 4.765 (+12.8 %), sphere 5.443 (+15.8 %). So a read before running: the shapes carry about 3 points less grid error than the sphere. This lane tests that read directly, in pure dust and at both masses.
- Caveat stated now: the reference treats the Gaussian peak's centre as a homogeneous ellipsoid. For the sphere this matched within the 3D trend; for shapes it is an assumption, and the 64 to 128 trend is the check on it.

## Runs (pure dust, no baryon stop, as SL's D0; eta 0.05, L = 8 q_t, canonical, TSC)
| Id | Shape | N |
|---|---|---|
| G0 | A, B | 64, 128, both masses (8 runs) |

Output `diag_a2/shape_grid.jsonl`. Script `shape_grid.py` (SL's `sphere_lag.py` with the shape as an argument). nice 15, one thread, two at a time, 67.5 CPU min cap. Started only when the 1-minute load average is under 16 and free plus inactive memory is over 8 GB.

## Reading rule, fixed now
- Grid error of a shape: e_s = t_q / t_exact − 1, at 128. The sphere's is 15.6 % (SL D0).
- If |e_s − 15.6 %| ≤ 3 points for every shape, AN2's shifts against its own sphere stand as measured. Otherwise each shift is restated against exact dust, and the difference is the bias of AN2's own-sphere comparison.
- Convergence order per shape from 64 to 128, against SL's 1.34 for the sphere. Orders within 0.3 of each other count as the same.
- At 1e12 the rows also carry the hold term. The hold effect on a shape is read as rows / G0 − 1 at 128 and set beside the sphere's 14.4 %. A read only.
- If the 64 to 128 trend doesn't point at the exact value (error not falling), the homogeneous reference is called unreliable for that shape and nothing is restated.

## Expectation, before any number
Shapes fold as filaments, less focused than the sphere's point, so smaller grid error: e_s about 12-13 %, as the 1e15 rows already suggest. Then AN2's shifts against its own sphere overstate the shape effect by about 2-3 points, and against exact dust the shapes still fold 5-21 % before the sphere, close to S0.

kappa = 1/2 FITTED. Canonical only, footings not pooled. A gravitating field, never a particle. The cold sector stays retired. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
