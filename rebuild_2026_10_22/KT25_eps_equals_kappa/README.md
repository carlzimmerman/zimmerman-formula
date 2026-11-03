# KT25_eps_equals_kappa: canonical ε = κ SURVIVES (Cassini 0.48x ceiling, dwarfs 15/24, 9 MW cells, SPARC +0.0021); alt FAILS on Cassini by 6 percent (1.06x), as predicted. With ξ = r_M / 2 the filter's two numbers become one on the canonical footing

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `kt25.py` (KT17's code, EPS [0.5]), `kt25.log`, `kt25.out`, `kt25.json`, `kt25.time`; `kt25_sparc.py` (KT19's code, EPS 0.5), `kt25_sparc.log`, `kt25_sparc.out`, `kt25_sparc.json`, `kt25_sparc_MUTATE.*`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K837. MW run 12 minutes, 0.64 GB.

| test | canonical | alt |
|---|---|---|
| Cassini Q2 / ceiling | **0.481, PASS** | **1.06, FAIL** |
| dwarfs, MW field (plain 15/24) | 15/24 | 15/24 |
| MW in-prior cells passing all four | 9 (7 at share 0.35, 2 at 0.26) | 78 (stored 30: 20 at 0.35, 10 at 0.26) |
| SPARC d rms, median | +0.0021, +0.041 | -0.0006, +0.014 |
| **Label** | **ε = κ SURVIVES** | **ε = κ FAILS: Cassini** |

## Reading
- **On canonical, one number does both jobs.** κ = 1/2 sets a0, and the same 1/2 sets the smoothing length ξ = r_M / 2 = sqrt(G M_b / (4 a0)). Every test KT17 passed at 0.55 still passes at 0.50, and canonical's MW now passes at thick share 0.26 (2 cells), which KT17's 0.55 didn't. 0.26 is Lian+22's APOGEE chemical thick-disc share (provisional lookup).
- **On alt it fails Cassini, narrowly.** 0.5 r_M sits below alt's Cassini threshold 0.504. This was predicted from KT16 before running.
- **As hard as a fail:** canonical's MW passes are all corner cells: Sigma_b 53.9 (+2 sigma), M_bb 2.0-2.12e10 (top), thick height 1.08 kpc (box top, except one at 0.90), R_d 2.6, thick R_d 2.0. The two at share 0.26 pass K by 0.1 and Ou by 1.3. None passes at the star-count share 0.12. Strict h fails everywhere (3.21-3.25). Cassini passes by a factor 2, not 10. The dwarfs are no better than plain QUMOND (15/24). SPARC's canonical median +0.041 is near the 0.05 line.
- **What it is:** a reduction, two fitted numbers to one, on one footing. It doesn't explain why 1/2, and it doesn't define "system mass" locally.

## Checks
KT17's C3 gas-mass check fails again on both footings (half-space grid factor 2, known from KT17; not fixed, as frozen). KT19's C3 envelope check fails again (exit 1, known). C1 and C2 pass in both; Q5 doubled grid dK +0.06, dv +0.08. SPARC MUTATE (Newton): rms 0.573, FAILS. KT17's MUTATE path (EPS [1.0], nu = 1) wasn't rerun; it's unchanged code.
