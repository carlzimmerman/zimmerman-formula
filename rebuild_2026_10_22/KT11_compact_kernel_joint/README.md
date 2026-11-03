# KT11_compact_kernel_joint: TWO NEAR MISSES, NO JOINT PASS. The compact kernel fits SPARC better than mu_2 at its own fitted scale, passes Cassini on rho_DE (0.376x) and nearly on rho_crit (1.024x), but rho_DE needs stars 41 percent heavier than the tolerance allows and rho_crit just fails Cassini

Criteria: `FROZEN_CRITERIA.md` (ebfa88ad99), alone first, confirmed landed before the run, **not blind**. `kt11.py`, `kt11.out`, `kt11.json`, `kt11_MUTATE.out`, `kt11_res.py`, `kt11_res.out`. No download. kappa = 1/2 FITTED and held fixed: this tests a kernel, not κ. Footings never pooled. Not theory closed. No register row.

Kernel: mu = 2Y - Y^2 for Y <= 1, mu = 1 above (Argon's u' = chi(1-chi)^2), exactly Newtonian above g = s. One float f on all stellar Upsilon.

| Gate | rho_DE | rho_crit |
|---|---|---|
| f, 95 percent | 1.41 [1.29, 1.54]: disc 0.705, bulge 0.987 | 1.26 [1.16, 1.38]: disc 0.630, bulge 0.882 |
| G1 stellar scale, [0.79, 1.26] | **FAIL** | PASS, at the edge |
| G2 fit | rms 0.1693, median +0.018: PASS | rms 0.1682, median +0.016: PASS |
| G3 Cassini | 0.376x: PASS | **1.024x: FAIL** |
| G4 trend, bulgeless | -0.005 [-0.041, +0.035]: PASS | +0.023 [-0.012, +0.061]: PASS |
| **Label** | **FAILS G1** | **FAILS G3** |

## Reading
- **Neither footing passes.** Each fails one gate, by a narrow margin on rho_crit. I'm not moving the tolerances after the result.
- rho_crit's Cassini miss is resolved, not noise: 1.0244x at two grid resolutions. It is 2.4 percent over.
- rho_crit's bulge, 0.882, is close to Sani's independent median 0.862 (by eye; Sani's own error and kappa_virial dependence apply). That links KT9 and this lane: the sharp kernel asks for the bulge mass Sani measures. It isn't a gate, and it's on the footing that fails Cassini.
- **The trend in all galaxies grows:** -0.068 on rho_DE, -0.035 on rho_crit, against mu_2's -0.032 and -0.017. It sits in bulge galaxies, as before. G4 tested bulgeless only, so it passing doesn't mean the trend is solved.
- G2 compares with mu_2 at f = 1. With f fitted for both, mu_2 is slightly better on rho_DE (0.1680 at f 1.15) and the same on rho_crit (0.1684 at 1.03). So this kernel doesn't fit better; it fits as well with heavier stars.

## What would turn this into a pass, not run
- On rho_crit, a slightly sharper corner above g = s would pull Cassini below 1. That's a new shape choice and would need its own frozen lane.
- On rho_DE, independent evidence that 3.6 micron disc M/L is near 0.7 would reopen G1. The stellar-population values on record sit near 0.5 to 0.6.
- Even a pass would owe clusters, lensing, LITTLE THINGS and wide binaries, and it would derive nothing.

## Controls
Planted f = 1.2 recovered 1.20. Exponential Cassini control 3.761x. MUTATE: exponential fails Cassini at 3.761x; shuffled SPARC rms 0.712. Exit 1.
