# NR4_low_mass_requirement: NOT DECIDED as frozen (K2, K3 missed 1e-6 at 5.6e-6, 2.6e-6). The map reads REGION ONLY BELOW f 0.87 [ABOVE EVERY SEED]: one cell of 36 clears the SPARC side, no net response and low-mass η × 1.5

Criteria: `FROZEN_CRITERIA.md`, committed alone first. `nr4.py`, `nr4_tail_add.py`, `nr4.out`, `nr4_results.json`, `nr4_m*_results.json`. A requirement map: m and f are FITTED, never a rule. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. Not blind.

**Why no verdict.** The frozen K2 and K3 compare f 0 on the response path with the true off path, and miss 1e-6. DR5's amendment traced the same size of miss to the response grid (300 points), which I haven't separately confirmed here. I'm not amending the line after seeing the map. The clearing cell's gates are read directly on the off path in NR3's HIGH row (Υ 0.52 / 0.54, tilt −0.10 / −0.08, LITTLE THINGS +0.093 / +0.085, groups +1.47), so that cell doesn't rest on the mismatch.

## Map, gates failed (Υ A shown)
| m \ f | 0 | 0.25 | 0.5 | 0.87 | 1 |
|---|---|---|---|---|---|
| 1 (measured) | 0.75 tilt, LT | 0.60 tilt, LT | 0.50 tilt, LT | 0.39 line, tilt, LT | 0.35 line, tilt, LT |
| 1.15 | 0.66 tilt, LT | 0.54 tilt, LT | 0.45 line, tilt, LT | 0.35 line, LT | 0.32 line |
| 1.3 | 0.61 tilt, LT | 0.48 line, LT | 0.39 line | 0.30 line | 0.30 line |
| **1.5** | **0.52 CLEARS** | 0.43 line, tilt | 0.36 line | 0.30 line | 0.30 line |
| 1.7 | 0.49 line, tilt | 0.39 line, tilt | 0.32 line | 0.30 line | 0.30 line |
| 2 | 0.44 line, tilt | 0.34 line, tilt | 0.30 line | 0.30 line | 0.30 line |

f 0.75 is in `nr4.out`; it clears nothing either. Groups stay CONSISTENT everywhere (Z +1.47 to +1.50), rms 0.063–0.079.

## What it says
- **At gravity's measured strength, f 0.87, no m ≥ 1 reaches Υ 0.50.** Best is 0.39, at measured η. Corrected after audit: the commit message's "no m" was too broad, because the grid starts at m 1. NR3's LOW, about m 0.67 / 0.60 at f 1, reads Υ 0.51 / 0.52, and fails tilt +0.55 and LITTLE THINGS +0.173 there. The 150–250 km/s bins read 0.30–0.39 regardless of m, since m doesn't touch them.
- **What clears needs both:** net response near 0 at 150–250 km/s (those bins go below 0.50 by f 0.25), and η(10¹⁰), η(10¹¹) about 40 and 37, above every seed (36.1, 33.8) and against medians 26.7, 24.7. On this coarse grid m is bracketed by 1.3 and 1.7. One cell on a 6 by 6 grid isn't a measured region.
- **The two asks pull apart at low mass:** with no response, tilt needs η up; a response of any size then pushes dwarfs to the floor.
- **Doesn't address clusters.** The clearing cell's own row, NR3 HIGH's EM1 off, is N's cluster path: 12 of 15, inner keys over, G-OUT-M3 +0.10, X-COP −0.160 FAIL. ZN4's native profile is a different path (X-COP passes, G-OUT-M3 +4.41 on measured gas), and the two aren't comparable: the difference is the profile, not the gas. The criteria's "as ZN4" was loose.
- f is one number per cell. A response that varies with mass isn't mapped.

My expectation (f_max about 0.25, m 1.3–1.7, [ABOVE EVERY SEED]) held on the tag, and was too generous on f_max.

## Independent audit
Rerun at 1200 response points: K2 3.9e-7, K3 2.0e-7, so the miss is the grid. The frozen label stays NOT DECIDED; I'm not amending after seeing the map. Interpolating, LITTLE THINGS needs m about 1.43 at f 0, η about 38.2, 35.3, so the [ABOVE EVERY SEED] reading holds off-grid. m 1.5, f 0.25's tilt fail is −0.15 on the line. Keys on this path aren't at gas +0.005; rerun there, key sets are unchanged. Grid floor and cap don't make the clearing cell (bins 0.51–0.77).

κ = ½ FITTED. Not theory closed.
