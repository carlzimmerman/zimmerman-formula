# AN2_aest_3d_fold: NO VERDICT, numbers only. All 16 S1 rows ran. At mu 56.6, shapes fold earlier than the engine's own sphere by about what the dust ellipsoid predicts. At mu 0.1, no row folds by z = 0, spheres included.

**Plain statement.** The 3D engine misses five frozen checks (KZ, KE2, KT, KB, KE), and KG misses too, so nothing here earns a label. At mu 56.6, an elongated peak folds 8-19 % earlier than a spherical peak on the same grid, close to S0's dust-ellipsoid shifts. The engine's spherical peak, though, folds 16-18 % **later** than AN1's 1D reference, and KG shows the 3D fold time still moving with N. At mu 0.1 nothing folds by today at either mass, shape or footing, spheres included, while AN1's 1D rows fold just before z = 0 (z 0.004-0.009). **The well read is broken at 1e15:** every 1e15 row has M_d >= M_ph inside R_test at its very first step, z = 20, because a physical R_test of 1350 kpc then holds the dense early background, about 5 times M_ph. That's the starting field, not capture. Taken literally, section 9 would call all eight 1e15 rows WELL CANDIDATE. I found this after the rows ran, and no label is applied anyway. At 1e12 no step meets it. At the last step M_d / M_ph is at most 0.83 (a sphere) and at most 0.04 at mu 0.1.

Criteria `FROZEN_CRITERIA.md` (cfc462ec68), alone first. Amendments A1 (post-miss), A2 (new reference, TSC kernel, rows for numbers on the owner's instruction, 1c0004c588), A3 (eta after KT). The earlier report is `README_V1.md`. Not blind. kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. No LCDM input. S2 and S3 don't run. Not theory closed. Nothing here says the data favour the framework.

## Checks, TSC engine (A2)
| Id | Result | Line | |
|---|---|---|---|
| KC | 3.4e-4 to 7.9e-3, both footings | 0.01 | pass |
| **KZ** 64^3 | **+3.54 %**; at 128^3 +0.64 % (read) | 5e-3 | **FAIL**, as A2 expected |
| **KE2** 96^3 | **+7.3 %**; at 128^3 +3.5 % (read) | 3 % | **FAIL** |
| KR | 0 | 1e-10 | pass |
| KM | MUTATE fails KC and KD | | pass |
| **KT** | T1 (1e12, mu 0.1, B) NO FOLD at eta 0.05, 0.025, 0.0125; T2 (1e15, mu 56.6, B) 5.704, 5.707, 5.706 Gyr, moves 0.05 % | 1 % | **FAIL**: T1 has no t_q. Rows at eta 0.05 (A3) |
| **KB** | NO FOLD at (64, L) and at (128, 2L) | 3 % | **FAIL**: no time to compare |
| **KE** e = 0, 128^3 | 1e12 mu 56.6: 6.216 vs 5.277 Gyr, **+17.8 %**; 1e15 mu 56.6: 5.443 vs 4.701, **+15.8 %**; 1e15 mu 0.1 NO FOLD (t_ref 13.783); 1e12 mu 0.1 NO FOLD (13.709). Shapes "point" | 5 % | **FAIL** |
| **KG** | G1 (1e12, mu 0.1, A) NO FOLD at 64, 96, 128. G2 (1e15, mu 56.6, A) 6.023, 5.312, 5.028 Gyr: 96 to 64 −11.8 %, 128 to 96 **−5.3 %** | 5 % | **MISS**, both rows |

KG's G2 trend is still moving, and in the earlier direction. So the 128^3 times are probably upper bounds, and the sphere's lag behind AN1 may be partly resolution. Not shown.

## S1 rows, eta 0.05, N 128 (t_q in Gyr, z)
Canonical and alt agree to the printed digits at mu 56.6; shape labels differ only at 1e12 B (canonical filament, alt sheet).
| Mass, mu | Shape | t_q | z | Fold shape | vs AN1 t_ref | vs own e = 0 | S0 dust shift | M_d / M_ph |
|---|---|---|---|---|---|---|---|---|
| 1e12, 56.6 | e = 0 | 6.216 | 0.918 | point | +17.8 % | | | 0.47 |
| | A | 5.401 | 1.122 | filament | +2.3 % | −13.1 % | −12.5 % | 0.17, 0.18 |
| | B | 5.039 | 1.230 | filament / sheet | −4.5 % | −18.9 % | −21.1 % | 0.13, 0.15 |
| 1e15, 56.6 | e = 0 | 5.443 | 1.111 | point | +15.8 % | | | 0.83 |
| | A | 5.028 | 1.233 | filament | **+7.0 %** | −7.6 % | −5.4 % | 0.66, 0.73 |
| | B | 4.765 | 1.319 | filament | +1.4 % | −12.5 % | −10.1 % | 0.61, 0.67 |
| 1e12, 0.1 | e = 0, A, B | NO FOLD | | | t_ref 13.709 | | | 0.00 |
| 1e15, 0.1 | e = 0, A, B | NO FOLD | | | t_ref 13.783 | | | 0.03, 0.04 |

M_d / M_ph is at the last step read (alt, canonical where they differ). At 1e15 every row meets M_d >= M_ph at z = 20 only (see above); at 1e12 none does. No solver warnings, no transient inversions, no row UNRESOLVED. t_any = t_q in every folding row.

**What the frozen comparison would say, if labels applied (they don't).** 1e15 shape A is LATER than AN1 by 7.0 %, but earlier than its own grid's sphere, which section 9 reads as grid bias. All eight mu 0.1 rows are NO FOLD, so LATER, and so are their spheres. Low mu would read NOT RESOLVED by KG's G1. A2 said in advance that at mu 0.1 the AN1 reference sits within 3 % of today, so these rows say little.

## What this does and doesn't show
- **Shows:** with the engine's own sphere as baseline, the shape shifts at mu 56.6 track the dust ellipsoid within 3 points, at both masses. That's the one consistent read.
- **Doesn't show:** whether 3D folds no later than AN1's 1D fold. The engine's sphere is 16-18 % behind AN1 and still moving with N. Either 3D needs more than 128^3, or AN1's reference is early, or the TSC kernel adds lag. Not separated.
- **Well read:** section 9's WELL test, M_d >= M_ph inside a fixed physical R_test at any step, is met trivially at early times at 1e15. A rerun would need the test restricted to the field's own excess, or to times after turnaround. That's a criteria change, not made here.
- **At mu 0.1:** nothing folds in 3D by z = 0 at 64, 96 or 128 (G1), in either box (KB). AN1 folds at z < 0.01 there, so the gap is a few percent of t. A no-fold this close to today isn't a stable result.

## Compute
40 rows in all. 128^3 rows took 1240-1765 CPU s, none near the 67.5 min cap; RSS 1.6-1.7 GB at 128^3, 2.3 GB at 96^3, **over the 1 GB target**. Free disk dipped to 14 GB before the rows; they started once it was back over 15 GB. A KB row at eta 0.0125 was stopped by SIGTERM at 56 CPU min, unread (A3).

## Files
`an2.py` (TSC engine), `an2_checks.py`, `run_a2_rows.py`, `run_a2_checks.sh`, `an2_rows.jsonl` (every row, KT's included), `an2_checks.jsonl`, `an2_checks_MUTATE.jsonl`, `*_v1_CIC.jsonl` (the CIC engine's checks), `an2_shapes.json`, `diag_a2/kz1d.py`.
