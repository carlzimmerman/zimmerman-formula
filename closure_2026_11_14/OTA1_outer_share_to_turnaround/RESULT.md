# OTA1_outer_share_to_turnaround: STILL FAILS / STILL FAILS (canonical / alt). OTHER KEYS: NONE BROKEN / NONE BROKEN

Criteria: `FROZEN_CRITERIA.md` (008b366f76, committed alone before any script or number). Driver `ota1_grade.py` (4767bb49f2, committed before any run), read-out `ota1_read.py`; numbers in `ota1_grade.out`, `ota1.out`, `ota1_results.json`, `cache_jobs/`. Not blind. kappa = 1/2 and X = 5.41 are FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework over LCDM. No amendment.

## Frozen words
- **canonical: STILL FAILS. OTHER KEYS: NONE BROKEN.**
- **alt: STILL FAILS. OTHER KEYS: NONE BROKEN.**

Counting the cold share X x M_b(< r_ta) once, out to turnaround, with the share beyond the fair-share R200c in the record's own layout, lowers G-OUT-M3 by 0.74 to 0.77 in Z in every cell. It stays above 2 in all four cells on both footings.

| G-OUT-M3, gas +0.005 | f* 0.034, h 0.672 / 0.686 | f* 0.0615, h 0.672 / 0.686 |
|---|---|---|
| record (BASE), canonical / alt | +4.41 / +4.07 ; +4.41 / +4.07 | +4.13 / +3.81 ; +4.13 / +3.81 |
| **OTA1 rule**, canonical / alt | **+3.64 / +3.31 ; +3.64 / +3.31** | **+3.39 / +3.08 ; +3.39 / +3.07** |
| pred (canonical, h 0.672) | 1.040 -> 1.131 (A 1.560) | 1.058 -> 1.143 (A 1.537) |
| reach (Z_base - Z) / (Z_base - 2), canonical | 0.32 / 0.37 | 0.35 / 0.41 |

Keys passing, both footings, both f*: 12 of 15 before and after. The same three fail: G-MID-T3, G-OUT-M3, G-OUT-Mall. None moves in, none breaks. X-COP is unchanged: +0.013, 0.075 at f* 0.034 and +0.005, 0.074 at f* 0.0615 (PASS). Its measured radii lie inside the fair-share R200, where the rule leaves the mass unchanged.

Other keys under the rule (canonical; alt equal to 0.01):
- G-OUT-Mall: +3.36 / +3.64 -> +2.63 / +2.89 at f* 0.034, and +3.15 / +3.43 -> +2.41 / +2.67 at f* 0.0615. It still fails.
- G-OUT-M2: +1.90 / +1.99 -> +1.13 / +1.30. M3A1's extended randoms had taken it to +2.20 / +2.26.
- G-MID-T3 moves the wrong way: +2.17 / +2.54 -> +2.23 / +2.60.
- G-OUT-all: +0.82 -> +0.33.

## What the record does (the trap)
The record's shear chain does not cut the cold share at R200c. In ZN4 / M3A1 the chain is ZN1's `zn1_fn` with ZN3's shapes, on X73's GC2 baryons, where the gas has slope 2.777 beyond R500 out to the self-consistent r_ta. That chain:
- ties the cold amount to the baryons only at the fair-share R200 (f_c M2 = X M_b(< R2));
- beyond R2, uses the zoom's own normalised profile, cut at r_ta for most clusters, or a solved closing tail where x_edge R2 < r_ta.

So the R200c cut is in the normalisation, not in the radius. In the record the cold mass inside r_ta is only **0.717** of X M_b(< r_ta) for the median KiDS cluster (X-COP 0.772). R2 holds 0.261 of it (median R2 0.90 Mpc, r_ta 6.03 Mpc). The rule rescales the beyond-R2 part by lambda, median **1.69** (16 to 84 %: 1.00 to 2.18; X-COP 1.51). Lambda is 1 where the record's tail already hits X M_b(< r_ta).

My expectation on record had the sign wrong: I expected lambda < 1. PAPER72's "inside R200c" (open item 12) is a separate bookkeeping, the matter-power layout, and is not touched here.

## Known answers, twins, checks (all pass)
- KA1: the base reproduces G-OUT-M3 at +4.408 / +4.074 and +4.130 / +3.809 (max |d| 0.004), and X-COP to 0.0002. PASS.
- TW0, zero extra share (lambda = 1): every key's prediction, both footings, max |d| 8e-11; X-COP |d| 0. PASS.
- TW2, doubled share: G-OUT-M3 moves by 2.45 / 2.43 (line 0.10). BITES.
- K1: under the rule, M_new(r_ta) / Mfair - 1 is at most 2e-16 over 1,310 calls, and inside R2 it differs from the record by 0. PASS. 8 calls (2 gas-poor clusters x 2 h x 2 footings) have no fair-share R200 and are left unchanged, as frozen. The uniform fallback was never used.
- K2: groups Z and SPARC are unchanged, |d| 0. PASS.
- Footings: in ZN1's "fs" mode the KiDS prediction does not take the footing. Canonical and alt agree in Z to 0.004, and A differs between them by the grader's per-footing reference. Graded side by side, not pooled.

## Bracket B: outer gas slope in the count only (reported, not graded; f* 0.034)
| slope beyond R500 | G-OUT-M3 canonical (h 0.672 / 0.686) | G-OUT-Mall | keys |
|---|---|---|---|
| 2.676 (shallower) | +3.42 / +3.10 | +2.42 / +2.68 | 12 of 15 |
| 2.777 (rule) | +3.64 / +3.31 | +2.63 / +2.89 | 12 of 15 |
| 3.071 (steeper) | +4.12 / +3.79 | +3.09 / +3.38 | 12 of 15 |

Alt agrees to 0.004. Neither end of the bracket changes the word.

## Post hoc readings (not graded)
- **Doubled share (TW2, S = 2).** Its job was to show the change can reach the key. With twice X M_b counted beyond R2, G-OUT-M3 goes to +1.96 / +1.64 and G-OUT-Mall to +0.91 / +1.11, but G-MID-T2 goes over (+2.01 at h 0.686) and G-MID-T3 rises to +2.37 / +2.72 (13 of 15 keys). The outer key would want about twice the counted share beyond R200, and the MID band then breaks. This is not a rule and was not frozen.
- **Errors including systematics.** M3A1's quadrature s (0.118 -> 0.148, x 1.25) applied to the rule's numbers gives about +2.90 / +2.64 (f* 0.034) and +2.70 / +2.45 (f* 0.0615). It is still over 2. This only rescales, which is M3A1's arithmetic, not a regrade.
- **Stacking.** Combining this with FR1's measured gas-fraction line or M3A1's C4e leakage was not computed. These are different changes to different inputs, and stacking them was not frozen.

## What it does to row 20
Row 20 stays FAILS. Counting the cold share to turnaround removes about a third of the miss (reach 0.32 to 0.41) and breaks nothing: X-COP, groups and SPARC are unchanged, and no passing key fails. The remaining miss is still about +3.1 to +3.6 sigma stat-only on both footings. PAPER72's open item 12, read for the shear chain, is answered: counting the cold share to turnaround helps and does not close the row. The scorecard is not edited here.

## Limits
- The rule keeps the record's layout beyond R2, the zoom's normalised shape or ZN1's tail, and rescales it. It does not use a new infall profile. A different placement (for example, the extra mass at R2 to 3 Mpc) would move the band differently and was not frozen.
- The baryons beyond R500 are the record's GC2 extrapolation (slope 2.777) and are not measured at those radii in these clusters. The bracket brackets the count only, not the baryon lensing term.
- Gas +0.005 only (GS4). X-COP's gas scale +0.111 was not run.
