# VS2_rotation_vs_central: UNDECIDED, narrowly. At fixed mass, slow rotators keep their excess whatever the central label; being central adds little. Only one slow non-central in the graded sample

Criteria: `FROZEN_CRITERIA.md` (354f5ac0b5), alone first, **not blind**. `vs2.py`, `vs2.out`, `vs2.json`, `vs2_MUTATE.out`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

Central means no brighter 2MRS neighbour inside the window. VS1's "four centrals" were a narrow list: many fast rotators pass this rule too.

| Window | Slow coefficient, canonical | Central coefficient, canonical | Slow, alt | Central, alt |
|---|---|---|---|---|
| **500 kpc, 500 km/s, primary** | +0.121 +- 0.047 | **+0.041 +- 0.035** | +0.118 +- 0.046 | +0.042 +- 0.035 |
| 300 kpc, 500 km/s | +0.130 +- 0.049 | -0.031 +- 0.048 | +0.128 +- 0.048 | -0.030 +- 0.048 |
| 1000 kpc, 1000 km/s | +0.134 +- 0.050 | +0.026 +- 0.037 | +0.133 +- 0.049 | +0.027 +- 0.037 |

Frozen rule for ROTATION needs the central term within 1 sigma of 0. At primary it is 1.2 sigma, so the label is UNDECIDED. Both reported windows would read ROTATION, but they aren't the graded row and I don't regrade.

Quadrants at primary, canonical: slow central +0.176 (3), slow non-central +0.199 (1, NGC 4374), fast central +0.089 (6), fast non-central +0.035 (6).

## Limits
- One slow non-central. Its central status flips with the window. Errors are scatter only, with no shared systematic.
- The rule misses high-velocity satellites and doesn't handle Virgo well.
- **NGC 3608 row not obtained.** Relaxing CFG330's quality filter still excludes it, so the second slow non-central is missing. I stopped there; `vs2_cfg330_relaxed.py` records the attempt.
- Primary window was picked after listing labels, as the criteria say.
- MUTATE, central labels shuffled: central term +0.007 and +0.045 in the two runs on the mass-tercile shuffle, slow stays +0.13. The control does not clearly isolate the term at this sample size.
- An offset is not a ZN4 halo. No mechanism, no field equation.
