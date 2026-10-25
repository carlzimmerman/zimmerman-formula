# X37_orbit_conversion: cold dark energy converting to dark energy with orbits fails the clusters

Criteria: `FROZEN_CRITERIA.md` (204001f8ad, committed alone). `AMENDMENT_A1.md`: A1 is pre-result (MUTATE bites K1);
A2 is post-result and implementation only (an edge weighting fixed for K1's N★ → ∞ limit; graded numbers are identical
to RUN1). κ = ½ FITTED. Footings never pooled. Raw eRASS1 × KiDS bands, graded with X30's machinery read-only. Cold dark
energy is not matter. Not "theory closed". Nothing here says the data favour the framework.

**Hypothesis OC.** Cold dark energy converts to dark energy as f = exp(−N_orb/N★). N★ is set from SPARC alone:
6.87 canonical, 2.78 alt. That clears the least-orbited sixth of SPARC (N₁₆ = 9.3).

## Verdict: OC FAILS CLUSTERS (both footings)

| key | measured (canonical h 0.672) | OC predicted | Z | |
|---|---|---|---|---|
| MID all-KT (reported) | 1.67 | 1.66 | — | the level comes out right |
| MID slope b with KT | +2.24 ± 0.74 | **−0.29** | +3.4 | WRONG SIGN |
| MID T3 | 2.13 ± 0.25 | 1.60 | +2.1 | UNDER |
| OUTER all-KT | 0.72 ± 0.14 | **1.67** | −6.7 | OVER |
| OUTER terciles | 0.39 / 0.62 / 1.03 | 1.73 / 1.68 / 1.61 | −4.2 / −4.6 / −2.7 | OVER |
| OUTER all 326 (X7 CAL) | 0.93 ± 0.10 | 1.68 | −7.6 | OVER |

Alt is the same picture: OUTER 0.66 measured vs 1.34 predicted (Z −5.3), MID slope −0.21 vs +2.07, and MID all 1.20 vs
1.53. Every reported variant fails the same way: the r^−2 profile, N★ × ½ and N★ × 2.

**Checks 4/4** (K0 X30's bands and C* reproduced; K1 both limits; K2 quadrature; K3 0.59 GB). `--mutate` fails K1, exit 1.

## Why it fails (the mechanism, from the profile numbers)

- **Orbit counts are highest at the centre,** so conversion empties the core. Only 0.2–0.3 % of the retained cold dark
  energy lies inside 0.15 Mpc, and about 5 % inside 0.5 Mpc. The rest (73 % of the fair share retained, canonical) stays
  in the outskirts and overshoots OUTER, which the data put **below** the law.
- **Hotter clusters are older in orbits at fixed radius,** so they convert more. That makes the MID trend with KT
  negative, while the data rise with KT.
- Both failures are generic to any conversion or loss keyed to dynamical age. The clusters need the opposite: cold mass
  concentrated toward the centre and growing with KT, and less than the law far out.

## What it adds to the cold-sector problem

This is the same wall as X30. A mechanism that removes cold dark energy where things are most evolved (galaxies) also
removes it from cluster centres, where the data want it most. Any successful exclusion has to remove it from galaxies
while concentrating it in cluster cores. A depletion rule keyed to orbits, density, temperature or time cannot do both.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x37_orbit_conversion.py`, `.out` / `_results.json`, `_RUN1` (before A2),
`_MUTATE`, `x37_x30_machinery*.log` (X30's own prints).

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x37_orbit_conversion.py            # exit 0, 4/4
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x37_orbit_conversion.py --mutate   # exit 1, K1 fails
