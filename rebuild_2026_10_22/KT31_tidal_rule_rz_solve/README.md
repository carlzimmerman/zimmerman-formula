# KT31_tidal_rule_rz_solve: frozen label NOT EVALUABLE (check N1 fails, by design error); beside, with ξ varying in (R, z), 0 Milky Way cells pass on either footing or rule. v_c now reaches the line, K_z is too high

Criteria: `FROZEN_CRITERIA.md` (517840aaa4), alone first, confirmed landed. `kt31.py`, `kt31.out`, `kt31.json`, `kt31.time`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K845. 9 minutes, 0.95 GB peak. Checkpoints (`ckpt/`, 0.4 GB) deleted after the run; rerun regenerates them.

ξ is built at every solver cell from that cell's own plain-QUMOND tidal tensor. Rules: F (KT28, Frobenius, 4/√3) and TF (KT30, trace-free, √6). Gather smoothing uses a width ladder of KT29's `rho_xi`. 1375 in-prior cells.

| | canonical F | canonical TF | alt F | alt TF |
|---|---|---|---|---|
| **frozen label** | **NOT EVALUABLE** | **NOT EVALUABLE** | **NOT EVALUABLE** | **NOT EVALUABLE** |
| beside: cells passing L1, L2a, L2b, L3 | 0 | 0 | 0 | 0 |
| L1 (v_c) / L2a / **L2b (K_z at R0)** / L3 | 264 / 585 / **18** / 100 | 222 / 553 / **8** / 76 | 590 / 434 / **0** / 505 | 538 / 393 / **0** / 449 |
| v_c max (km/s) | 232.3 | 231.4 | 237.9 | 237.0 |
| best-D cell: v_c, K(R0) (line 66.4 ± 4.4) | 216.1, 79.7 | 215.2, 80.2 | 216.4, 76.8 | 215.6, 77.4 |
| smoothed / true mass, min / median / max | 1.15 / 1.29 / 1.42 | 1.12 / 1.26 / 1.39 | 1.17 / 1.33 / 1.44 | 1.13 / 1.30 / 1.42 |

## Why the frozen label is NOT EVALUABLE, and what that means
N1 compared the grid's ξ at the cell nearest (R0, 0) with KT29's exact-midplane value. It came out about 0.03, against a line of [0.8, 1.25]. The Hessian isn't what's wrong. Beside N1, added after the freeze and not graded (N1b): the grid's tidal size matches KT29's to 1.02, and the grid ξ using only the radial gradient matches KT29 to 1.05. What N1 missed is that the exponential disc has a kink in density at z = 0. That cell sits 8 pc above the plane, where the vertical gradient of τ is already large, so ξ falls from about 40 kpc to about 1.4 kpc. The check's premise (ξ continuous at the plane) was wrong; that's my design error, and the label stays as frozen.

## Reading (beside the label)
- With ξ varying in (R, z), the midplane problem of KT29/KT30 goes away. Inside the disc, ξ is only 0.005-3 kpc (the ξ map is in `kt31.out`), so the disc's mass isn't smoothed away. **v_c now reaches the line**: hundreds of cells pass L1 on both footings.
- **The vertical force fails instead.** K_z at R0 is 77-80 against 66.4 ± 4.4. On alt, no cell passes L2b at all; on canonical only 8-18 do, and none of those pass L1 too. It's the same miss as KT13's local QUMOND kernels (K 75-76 once v_c is in line): local rules put the Milky Way's extra pull into a disc.
- Gather smoothing also **adds** 12-44 % mass. Cells about 1 kpc above the disc get ξ of about 5 kpc and pull in disc density. I had only anticipated a deficit. Some of the extra K_z may be that added mass; how much isn't separated. A mass-conserving (scatter) form isn't built.
- F vs TF hardly differ (ξ within ~10 %).

## As hard as a fail
- R4 (ladder blend) FAILS: at ξ ≈ 9 kpc the blend is off from direct `rho_xi` by +0.65 to +0.77 km/s (line 0.5); at 0.8 kpc it's −0.01. The ladder step of 1.5 is too coarse at large ξ. That's under 1 km/s, small next to the K_z miss (11-14 units).
- R5 (ln τ smoothed by one cell) moves v_c and K by ≤ 0.05; no label change.
- R1 (ξ 0 reproduces UX5's form Q, max rel 0) passes on both footings, as does MUTATE (ν = 1 gives Q = N, 2e-13). R6 (added code check: cached component build = `rho_xi`, 9e-16) passes. Failed checks: N1 ×2, R4 ×2, so the script exits 1.

## Where this leaves the tidal line
- Midplane single value: fails v_c (KT29, KT30).
- Full (R, z): fails K_z.
- No tidal-rule form tested passes the Milky Way on either footing. KT28's alt "survival" rested on the in-plane approximation.
- Not tested: a mass-conserving scatter form, and a finer ladder.
