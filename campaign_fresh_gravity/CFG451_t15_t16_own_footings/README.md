# CFG451: T15 and T16 on the framework's own a0

Criteria: `FROZEN_CRITERIA.md` (d070de4c1, committed alone before the script). Script: `cfg451_own_footings.py`.
Outputs: `cfg451_own_footings.out`, `cfg451_results.json` (MUTATE: `*_MUTATE.*`).

**Verdict: this does not rescue the budget. The cluster overdraft stands on both footings.**
- On the canonical footing the floor-vs-cluster bind weakens (1.63× → 1.40×), and the group knife-edge turns positive.
- But the Milky Way 30-kpc budget becomes infeasible at its measured speed, and T16's single-λ window closes.
- On the alt footing the picture is close to the committed T15/T16.

The lower a0 makes the kernel supply S smaller everywhere. That helps the R500 budgets and hurts the MW point.

## Key numbers (M_cold/M_b; λ windows; footings never pooled)

| item | T15/T16 as committed (1.2e-10) | canonical 9.3603e-11 | alt 1.1312e-10 |
|---|---|---|---|
| S/M_b: MW30 / groups / clusters | 2.85 / 6.15 / 4.98 | 2.47 / 5.38 / 4.34 | 2.76 / 5.96 / 4.82 |
| V1 clusters b = 0 / 0.3 | −0.98 / −0.48 | **−0.80 / −0.31** | −1.00 / −0.51 |
| V2 groups b = 0.3 | +0.04 (knife-edge) | **+0.26 (positive)** | −0.04 (knife-edge) |
| MW-30 at V 188 / 200 / 230 | −0.97 / −0.65 / +0.25 | −0.64 / −0.32 / +0.58 | −0.89 / −0.57 / +0.33 |
| V3 MW-30 infeasible above (M_b 7e10) | 196.6 km/s | **186.5 km/s** (below 188) | 194.2 km/s |
| cluster λ window | [0.0073, 0.0172] | [0.0085, 0.0200] | [0.0064, 0.0164] |
| V4 floor 0.028 / cluster upper | 1.63× STANDS | **1.40× WEAKENED** | 1.71× STANDS |
| V5 intersection, MW M_b 7e10 (frozen) | EMPTY | EMPTY (no feasible MW point) | EMPTY |
| intersection, T16 verbatim (both M_b) | [0.0152, 0.0172] | **EMPTY** ([0.0201, 0.0200]) | [0.0162, 0.0164] |
| V6 T12 λ / cluster λ_max | 3.95× | 3.40× | 4.50× |

## Reading
- **Clusters are negative everywhere.** Your own a0 shrinks the overdraft from about −1.0 to −0.8 at b = 0, but it does not
  close it.
- **The canonical footing moves trouble rather than removing it.** The groups stop overdrafting at b = 0.3, and the floor
  needs only 1.4× more λ than clusters allow. But with M_b = 7e10 the MW 30-kpc deficit exceeds the kernel supply above
  186.5 km/s, which is below the measured 188. Even T16's verbatim window (which also admits the M_b = 1e11 MW points) misses
  by 0.0001.
- **T16's "nonempty intersection" depends on the M_b = 1e11 MW convention.** With M_b = 7e10 alone, the MW window is a single
  point (V188) or nothing, and the intersection is empty on every row, including the committed 1.2e-10 baseline.

## Disclosures
- **T15's stated f_law(R500) = 0.286 is 0.280 in its own code.** The rounding is the docstring's. C1 reproduces the
  committed JSON with 0.280.
- **The frozen MUTATE was ill-posed and FAILED as frozen. It is kept.** T15's planted misread f_law := deficit gives
  x(1 − S) with S ≈ 4–6, which makes the clusters MORE negative (−1.3 to −3.6), so V1 cannot flip. The mutation does change
  every row by more than 0.1, so the code is sensitive to it, but the frozen flip test is wrong. It is not replaced post hoc.
- λ = 0.028 is held because its MW-floor calibration uses ρ = V²/(4πGr²), which has no a0 in it.

## Controls
- C1 reproduces the committed T15 and T16 JSON at 1.2e-10 to 1e-9.
- C2 reads CFG450's deficits correctly.
- MUTATE failed as frozen (see above).
