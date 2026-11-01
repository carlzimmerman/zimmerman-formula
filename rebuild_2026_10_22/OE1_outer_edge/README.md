# OE1_outer_edge: NO VERDICT as frozen, because two MUTATE lines failed. The computed statistic reads NOT THE EDGE: G-OUT-M3's band sits well inside the model's edge and reads the zooms' own particles, and extending to the sphere's edge moves it by +0.0002

Criteria: `FROZEN_CRITERIA.md` (566d04c6d2), committed alone first, including the BL1 cross-check and DR6 baseline. `oe1_inject.py`, `oe1_grade.py`, `oe1_verdict.py`, `oe1_particles.py`, `oe1_bl1.py`; numbers in `oe1.out`, `oe1_results.json`, `oe1_particles.out`, `oe1_bl1.out`. kappa = 1/2 FITTED; cold dark energy, no particle; not theory closed. Nothing here says the data favour the framework. Not blind: the lead was found post-result in M3A1, so no out-of-sample claim. No rule passes here. No new runs.

## Why no verdict
MUTATE a: the x 10 run scales properly (11.6 x E1 on pred; line 7.5-12.5) but moves Z by +0.002, under my floor of 0.02. MUTATE b: zeroing the cold mass inside the band drops bin 7 by 17.9 % and G-OUT-M3 to +5.28, but bin 6 by -0.1 %, against 10 % in each bin. Both lines came from my expectation of how much local mass matters, and both expectations were wrong. The reason is the finding below. By my own rule that means no verdict; I'm not restoring one post-result. K4 also missed, stated and not a stop: 7.7 % at 1.2 R200, where the direct estimate's annulus is 10 % wide, within 4 % elsewhere except 1e15 likewise at 1.2 R200.

## Where things sit (M3, f* 0.034, h 0.672; 16, 50, 84 %)
| | R200, Mpc | band 1.42 / 2.06 / 3 Mpc in R200 | 3 Mpc in r_ta | r_ta, Mpc = R200 | x_edge R200, Mpc | particle edge, Mpc |
|---|---|---|---|---|---|---|
| M3 | 1.10 1.25 1.53 | 1.14 / 1.65 / 2.40 | 0.32 0.38 0.44 | 6.87 7.85 9.50 = 6.2 | 7.59 8.65 10.49 | 19 22 26 |
| lighter | 1.07 1.12 1.23 | 1.27 / 1.84 / 2.68 | 0.36 0.41 0.46 | 6.4 R200 | 7.82 | 20 |
| heavier | 1.27 1.40 1.67 | 1.01 / 1.47 / 2.14 | 0.30 0.34 0.39 | 6.1 R200 | 9.83 | 25 |

Of 109 clusters: r_ta < 3 Mpc in **0**; x_edge R200 < 3 Mpc in **0**; x_edge inside r_ta (gamma tail or step, A2 item 7) in **2**, both lighter, and even there the tail starts beyond 5.8 Mpc. So 107 of 109 take the zoom's shape cut at r_ta with no tail. The band's prediction has no fair-share closure, no gamma, no step and no cut in it.

## Where the band's prediction comes from
| share | baryons | cold < R200 | cold R200 to 1.42 Mpc | cold 1.42-2.06 | cold 2.06-3 | cold 3 Mpc to r_ta | tail |
|---|---|---|---|---|---|---|---|
| bin 1.42-2.06, M3 | 0.160 | 0.799 | 0.048 | 0.011 | -0.015 | -0.002 | 0.000 |
| bin 2.06-3, M3 | 0.175 | 0.621 | 0.037 | 0.166 | 0.013 | -0.012 | 0.000 |
| bin 2.06-3, lighter | 0.183 | 0.586 | 0.076 | 0.147 | 0.017 | -0.009 | 0.000 |
| bin 2.06-3, heavier | 0.170 | 0.643 | 0.012 | 0.178 | 0.010 | -0.014 | 0.000 |

So 80 % of the outer bin's prediction comes from mass inside R200 plus baryons. Delta-Sigma at R reads M(<R)/pi R^2, and mass outside R counts slightly against it. The bin falls because R^-2 falls faster than M(<R) rises.

## Grade, gas +0.005 (order f* 0.034 h 0.672, h 0.686; f* 0.0615 h 0.672, h 0.686)
| variant | G-OUT-M3 stat-only | Z_tot | reach | over 2 | joint chi^2/15, p |
|---|---|---|---|---|---|
| ZN4 | +4.408 +4.074 +4.130 +3.809 | +3.51 +3.24 +3.29 +3.03 | | G-MID-T3, M3, Mall | 35.9-38.2, 0.002-0.0009; 31.9-34.2, 0.007-0.003 |
| **E1, particles to the sphere's edge (primary)** | **+4.408 +4.074 +4.130 +3.809** | +3.51 +3.24 +3.29 +3.03 | **-0.0001** | same | same |
| E2, capped at budget | same | same | same | same | same |
| E1, seeds' mean in place of median (post-result) | +4.419 +4.086 +4.139 +3.820 | +3.52 +3.25 +3.30 +3.04 | -0.006 to -0.004 | same | 36.3-38.6; 32.2-34.6 |
| E1 on VB1 run A's node | +4.410 +4.074 +4.132 +3.810 | | | same | |
| E1 on VB1 run B's node (RS 2.0) | +4.464 +4.132 +4.182 +3.864 | +3.56 +3.29 +3.33 +3.07 | -0.03 | adds G-OUT-M2 at f* 0.034 | 36.7-39.0 |
| E3, budget closed inside r_ta, **not native** | +3.600 +3.273 +3.353 +3.037 | +2.87 +2.60 +2.67 +2.42 | +0.34 to +0.43 | same three | 26.4-29.0, 0.034-0.016; 23.4-26.1, 0.075-0.037 |

X-COP +0.013, 0.075 and +0.005, 0.074 and groups +1.62, unchanged in all native variants: nothing here touches r < R500 (E1 mean: +0.008, 0.076). E1's pred for G-OUT-M1 moves +0.0025, where low-mass clusters lose the step; G-OUT-M1 Z +0.79 to +0.78. So the term applies to all keys with no per-bin tuning, and it's small everywhere.

**E1 is verified small three ways, not just read:** the grader's shift on pred is -2e-5 per unit (x 10 scales); a shell estimate M_extra R^2 / 8 pi a^4 gives about -1e-4 at the bin's outer radius, same sign and order; an independent Abel integral on one 1e14 and one 1e15 run gives cut at 7 R200 against none 1.001, at 4 R200 1.002-1.008. It's (R/a)^4.

**E3 is the door's ceiling, and it doesn't clear.** It multiplies the cold mass above R200 by F = 1.77 (median) so that M_c(r_ta) = M_fair (ZN4's zoom holds 0.69 of it at r_ta). That's 77 % more density than the particles have in the band, on a model already 1.75-2.57 x DR6's linear density at 1.5-2 R200. Reach 0.34-0.43 and still +3.0 to +3.6; G-OUT-Mall +2.06, +2.29; G-MID-T3 stays over; G-OUT-M2 falls to +0.74. It's fair-share budget, neither new nor moved from the core, but the particles don't put it there.

## New budget or double count (DR6's C2, C3)
- **New budget:** E1's mass beyond r_ta is 19 % (15-23) of the total budget, none moved from inside, and it can't double count the core. M_c(sphere) passes M_fair in 26 of 109, mostly heavier; E2 caps that, with no effect.
- **It describes the same region as DR6's C1 and C3,** so they mustn't be added. rho_model/rho_lin falls to 0.63 at 3 R200, 0.27 at 0.9 r_ta, so nothing out there double counts the linear density, consistent with DR6: filling it doesn't help the band. C2's double count inside about 2.5 R200 stands.

## The claim of a "vacuum cliff at 1.4-2 R200"
**Not a vacuum.** There is a real steepening, but density there is 12-24 x the mean. Single-bin slope in 1.4-2 R200, stack: 1e13 3.22, 3.20; 1e14 3.08, 4.53; 1e15 4.38, 4.18; 1e12 3.37, 3.40 (z 0, 0.25). So my frozen line of slope 4 is exceeded in 3 of 8; the steepest bin inside 6 R200 runs x 1.7-3.1 and bins are noisy (any seed to 7.5). Mean slope 1.4-2.4 R200 is 3.2-3.6. The share of shell mass with v_r < 0 goes from about 0.5 inside to 0.8-1.0 at x 2.4-4, so this is the boundary between orbiting and infalling mass. VB1's RS 2.0 run has it as well (4.88 at x 2.43, RS 1.5 6.00), so the sphere's boundary doesn't cause it. Density falls below the mean only from x about 4-5, and 0 % of shells are infalling from x about 6: that is the sphere's vacuum, and it's outside the band.

So the band does sit on a feature: bin 7 covers x 1.65-2.40 in M3. The fall is measured, not constructed. Physical only with this caveat: **these are isolated spheres.** A cosmological environment could supply a shallower feature; VB1 (RS 2.0 does not) and DR6 (linear two-halo too small) are the only tests of that here. No cosmological box exists in this record.

## Does heavier against lighter follow?
Partly, not because of the edge. No variant changes the split: E1 lighter +4.56 (A 1.63, pred 0.85), heavier +1.83 (A 1.50, pred 1.22); E3 +3.63, +1.43. The band reaches x 2.68 in the lighter half, 2.14 in the heavier, so the lighter half reads further past the steepening; but its R200 is also 20 % smaller, and at fixed x Delta-Sigma scales with R200. That's the fair-share mass from gas, not the edge. Post-result, proves nothing.

## Galaxy halos at 1e12 (reported, not in the label)
BL1's halo with the 1e12 stack past R200 instead of the cut at r_ta. Canonical, blue: window A 1.053 to 1.053; chi^2 over 15 bins 109.2 to 102.8; window 25.0 to 24.8; law 27.5, 9.2. All: 693 to 661; law 79. Alt the same within 0.01 in A. Two bins fall in R 150-300 kpc at lg M* 10.7, indicative: data/model 2.04, 1.53 to 2.03, 1.55; the law 1.17, 1.04. Same reading as TL1: no useful change. The 1/R excess at large radii remains.

## Expectation on record
NOT THE EDGE, E1 near zero: the statistic agrees. E3 might raise the band and break M1, M2: it raised it, broke none, and helped M2.

## Limits
1. Median stack at 1e13 ng 64, 1e14, 1e15 ng 80. VB1's nodes are one seed at ng 48, compared with each other.
2. 5 of 109 spheres reach beyond the 30 Mpc grid; that mass stays flat there and can't touch the band.
3. Gas is cut at r_ta as in the chain; E1 extends cold mass only. Baryons at 17 % of the bin mean that wouldn't change the reading.
4. The zooms evolve in vacuum. Mean density isn't subtracted in this path, as in every lane; the band is 2-20 x the mean, so it matters little there.
5. K6 (joint chi^2 reproduces M3A1, 0) was added by me. K3's denominator is the cluster's larger bin; 8 of 652 rows have a bin at the grader's floor. The first K3 and K6 failed for those reasons and for using one f*'s template in R; pieces then used differences of chains, as frozen, because the grader's clip hides negative pieces.

## Checks
K1 ZN4 and M3A1 per-cluster V, |d| 0. K2 0. K3 2e-16. K5 stated. K6 0. K4 and MUTATE a, b above. `oe1_grade.py`'s jobs cached in `cache_jobs` (gitignored).
