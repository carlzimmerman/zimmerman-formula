# X33 AMENDMENT A1 (POST-RESULT: written after the first run's step 0 fired the stop rule; before any finding was computed)

κ = ½ FITTED. Footings never pooled. Not "theory closed".

## What happened

The first run (no findings written; stop rule) passed S0a, S0b, S0d, S0e, S0f, S0g, K_rows, K_ident and K_size, and
**FAILED S0c**: plain medians of X1's per-system iso Delta against X1's printed class values, tolerance 0.03.

| class | plain median can / alt | X1 printed can / alt | d can / alt |
|---|---|---|---|
| LG field | +0.036 / +0.007 | +0.05 / +0.02 | −0.014 / −0.013 |
| MW classical | +0.243 / +0.200 | +0.28 / +0.24 | **−0.037 / −0.040** |
| MW ultra-faint | +0.596 / +0.539 | +0.63 / +0.59 | **−0.034 / −0.051** |
| bright M31 | +0.220 / +0.185 | +0.25 / +0.21 | −0.030 / −0.025 |
| M31 others (N 5) | +0.777 / +0.697 | +0.64 / +0.59 | **+0.137 / +0.107** |
| Crater II, Antlia II | equal to 0.003 | | |

## Mechanism (checked, not assumed)

X1's class value (`class_stats[...].median`) is not a median of the per-system central values. It is the median, over
bootstraps, of the median over systems **and Monte-Carlo measurement draws** (`boot_median(X[idx, col])` in
`x1_hosted_recount.py`, where `col` indexes the draws). The draws of log(g_obs) ∝ log σ² are asymmetric, so the
draw-inclusive median shifts from the central-value median. A quick check (scratch, not committed as a result): resampling
the per-system central values alone returns the plain median exactly (0.036, 0.243, 0.596, 0.220, 0.777 canonical);
adding Gaussian draws of width sdMC moves it to 0.056, 0.281, 0.630, 0.268, 0.684, within 0.004–0.04 of the record. The
residual gap is the non-Gaussian draw shape, which only X1's draws carry. X19 met the same thing: its K1 printed these plain
medians as "K1-reported" and graded the JSON values against the printed digits instead.

So S0c as frozen compared two different estimators; the per-object values themselves are the record's (K_ident: Crater II,
Antlia II, Bootes I equal X1's CSV to 1e-9).

## Change (check code only; no threshold, residual definition, class, property or analysis line changes)

- **S0c (graded, replaces the frozen line):** X1's JSON `class_stats[f|cls|primary|iso AQUAL L*0].median` equals X1's
  printed `.out` value within half the last printed digit (0.005), for the 7 classes, both footings. This is the record
  consistency X19's K0 graded.
- **S0c-plain (reported, not graded):** the plain per-system medians above, with the difference to the record.
- **Disclosure carried to the README:** the atlas stores per-object central values. Class medians computed from the atlas
  therefore sit 0.01–0.05 dex below X1's printed class values for LG field, MW classical, MW ultra-faint and bright M31,
  and 0.11–0.14 dex above for M31 others (N 5). Any comparison with X1/X19 class numbers must use X1's own values.

The stop rule is otherwise unchanged; the rerun recomputes everything from scratch.
