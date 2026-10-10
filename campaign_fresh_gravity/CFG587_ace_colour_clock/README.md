# CFG587: ACE first test — one colour clock or a class step? UNDECIDED as frozen

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (a15bbe272). Model: `../MODEL_accumulating_cold_energy_2026-10-10.md`.
- **Script:** `cfg587_clock.py` → `cfg587_clock.out`, `cfg587_results.json`; MUTATE `CFG587_MUTATE=1` (colour shuffled within class × mass) → `_MUTATE`.
- **Machinery:** cfg585_age.py's head executed unedited (CFG531 estimator, CFG529 validated environment). All f30 lenses (57,265).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Bins (equal count, colour residual at fixed mass over all f30 lenses)
| bin | N | median δc | early fraction | median log M* | ε K9 (A canonical) |
|---|---|---|---|---|---|
| 0 | 9,537 | −0.457 | 0.00 | 10.76 | −0.32 |
| 1 | 9,539 | −0.264 | 0.08 | 10.69 | −0.02 |
| 2 | 9,534 | −0.089 | 0.35 | 10.60 | +0.16 |
| 3 | 9,563 | +0.082 | 0.63 | 10.76 | +0.35 |
| 4 | 9,530 | +0.198 | 0.84 | 10.80 | +1.12 |
| 5 | 9,562 | +0.363 | 0.88 | 10.58 | +0.56 |

## Result (K9 primary; GLS on 6 bins with jackknife covariance)
| cell | χ² ACE (colour) | χ² STEP (class) | χ² BOTH | colour slope b (per mag) |
|---|---|---|---|---|
| A canonical | 8.22 | 5.19 | 3.87 | +1.52 ± 0.31 |
| A alt | 8.21 | 5.18 | 3.85 | +1.39 ± 0.28 |
| B canonical | 8.24 | 5.22 | 3.89 | +1.51 ± 0.31 |
| B alt | 8.23 | 5.21 | 3.88 | +1.38 ± 0.28 |

- **Verdict as frozen: UNDECIDED** in all four cells: the class step fits 3 better (< 4), adding the step to ACE gains 4.3–4.4
  but ACE never beats STEP by 4. K-in is flatter and noisier (χ² ≈ 5–6 for all models).
- P3(i): the colour slope predicts OLD−YOUNG +0.37–0.40 vs CFG586's measured +0.88–0.97 ± 0.33–0.36 → consistent within 2σ (low side).
- Declared log-age variant (τ ∝ 10^(δc/1 mag), PROVISIONAL): χ² 12.1, worse than both.
- Controls 2/2: C1 partition (min N 9,530); C2 all-f30 ε(K9) +0.3850 reproduces CFG531 exactly.
- MUTATE (colour shuffled within class × mass): ACE not favoured (passes). Its binned slope is still +0.9–1.0/mag because the
  bins sort by class composition — so this binned design cannot separate a clock from a step; the real slope (+1.4–1.5) and
  within-bin contrast exceed the shuffled version, consistent with CFG585/586's within-class age signal.

## Reading (not a verdict)
- The excess rises strongly with colour at fixed mass (slope ≈ 5σ), but six mixed bins cannot tell a continuous clock from a
  class step: the class and colour axes are too collinear. The red-end dip (bin 5, lower median mass 10.58) shows mass is
  not perfectly matched across colour bins.
- ACE is neither supported over a class step nor ruled out. Its strongest evidence remains the within-class OLD/YOUNG
  difference (CFG585/586). A decisive clock test needs colour contrast INSIDE each class at matched mass (as CFG585) in
  more than two bins, or an independent clock (specific SFR), not mixed-class bins.
