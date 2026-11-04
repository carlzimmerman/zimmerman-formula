# LAM7 FROZEN CRITERIA: LAM6's orbit-shape test on KU2's full sample

Frozen before any new cube is streamed. kappa = 1/2 FITTED; footings never pooled; not theory closed.

## Why
LAM6 (8483e6bd02) gave NO VERDICT: on 963 galaxies the law residual at r_half leans with integrated h4 by
E = +0.040 [-0.008, +0.093] ln (canonical), +0.042 [-0.003, +0.096] (alt). LAM7 sums the rest of KU2's sample.

## Sample and pipeline
- KU2's 6056 galaxies (`ku2.py` selection, exactly) minus the 1000 LAM4 already summed: the NEW sample.
- Each DR17 LOGCUBE streamed, summed in the half-light ellipse and deleted with LAM4's `integrate()` unchanged
  (criteria 1023fbaae9 rules); sums saved to `_external_data/lam7_integrated_2026_11_04/`.
- Each sum fitted once with LAM4's `prep()`/`run()` unchanged (pPXF + E-MILES, moments 6, degree 8; pPXF's
  standard emission-line mask, 800 km/s full width). No refits.
- Fits with sigma_int <= 0 or |h4| >= 0.3 (pPXF bound reached) are dropped and counted.

## Graded statistic (identical to LAM6)
E = OLS slope of within-(KU2 cell, KU2 class) demeaned r on demeaned h4_int, x IQR(h4_int); groups >= 3;
2000 bootstrap draws (seed 20261104). Canonical and alt separately.
**Graded on the NEW sample only** (independent of LAM6's look). LAM4's 1000 + new combined is a row.

## Checks
- C1 N in groups >= 3000. C2 KU2 D reproduced exactly. K1 median log(sigma_int / Sigma_Re) within +-0.03 and
  rms <= 0.06 on the new sample. K2: LAM4's K2 (A1 noise scaling) re-run on 200 synthetics drawn from the new sums,
  rms <= 0.03. M1 MUTATE: h4 shuffled within groups, 95 % interval includes 0.
- Any check fails: NO VERDICT (K2 fail: h4 NOT MEASURABLE).

## Labels, per footing (as LAM6)
- **TRACKS ORBIT SHAPE**: |E| >= 0.05 and the 95 % interval excludes 0.
- **NO ORBIT DEPENDENCE**: the 95 % interval lies inside +-0.05.
- otherwise **NO VERDICT**.

## Rows (ungraded)
Combined sample; within slow and within fast; galaxies with LAM2's MPA-JHU gas flag, gas-poor vs gas-bearing;
E by S/N tercile; E using KU2's second-best JAM model.
