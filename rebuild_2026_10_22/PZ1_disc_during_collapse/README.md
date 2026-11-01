# PZ1_disc_during_collapse: STRONG; BLUMENTHAL HOLDS; SHIFT UP (small). A disc started at turnaround contracts slightly more than LC1's, not less

Criteria: `FROZEN_CRITERIA.md` (81c8d83d90), `AMENDMENT_A1.md` (908c641abb). `pz1_disc.py`, `pz1_read.py`, `pz1_sparc.py`, `pz1.out`, `pz1_results.json`, `pz1_checks.out`, `pz1_sparc.out`. κ = ½ FITTED, unused; not theory closed. Nothing here says the data favour the framework. Newtonian, gravity only, no feedback.

## Frozen grade, 10¹², ng 64, z = 0, 8 of 9 seeds
M_d 6.72e10, R_d 3.565 kpc, as LC1. Linear in time from each seed's measured turnaround to z = 0.

| | PZ1, 8 seeds | LC1, same 8 | LC1, 9 |
|---|---|---|---|
| R_live | 2.126 [1.90, 2.50], STRONG | 2.075 | 2.154 |
| f_Q | 0.946 [0.78, 1.08], BLUMENTHAL HOLDS | 0.873 | 0.872 |

Same-seed pairs: **ρ = R_live ratio, median 1.058 [0.998, 1.092]**, 6 of 8 above 1; **Δf_Q, median +0.037 [+0.007, +0.100]**, 7 of 8 above 0. Δf's interval excludes 0, so the frozen label is **SHIFT UP**. It is small and the class doesn't change.

| seed | t_ta Gyr | t_ta/t_f | M_d(z_f)/M_d | R_live PZ1 / LC1 | f_Q PZ1 / LC1 |
|---|---|---|---|---|---|
| 1 | 2.97 | 0.49 | 0.29 | 1.99 / 2.00 | 0.87 / 0.87 |
| 2 | 3.06 | 0.50 | 0.28 | 1.90 / 1.79 | 0.86 / 0.79 |
| 4 | 3.98 | 0.65 | 0.22 | 2.08 / 1.90 | 0.97 / 0.87 |
| 5 | 4.63 | 0.76 | 0.16 | 2.39 / 2.27 | 0.95 / 0.94 |
| 6 | 5.67 | 0.93 | 0.05 | 2.17 / 2.15 | 1.00 / 0.98 |
| 7 | 3.26 | 0.54 | 0.27 | 2.30 / 2.16 | 0.94 / 0.85 |
| 8 | 2.76 | 0.45 | 0.30 | 1.91 / 1.65 | 0.78 / 0.54 |
| 9 | 3.62 | 0.60 | 0.24 | 2.50 / 2.52 | 1.08 / 1.07 |

**The other read-outs.** At z_f, with 5–30 % of M_d in place, R_live is already 1.38 and f_Q 0.854. The response follows the disc through collapse, as Blumenthal says. At z = 0.5 and 0.25: R_live 1.70, 2.02, f_Q 0.94, 0.99; these have more disc mass than LC1's at the same z, so they aren't same-mass comparisons. Q(r) at z = 0 for r/R_d 1, 2, 3, 4, 6, 8, 10: live 3.56, 2.24, 1.92, 1.71, 1.52, 1.45, 1.36; Blumenthal 3.74, 2.45, 1.96, 1.72, 1.45, 1.34, 1.27.

**The expectation on record was little change.** That held for R_live. The f_Q shift is small and goes the wrong way for a relief: violent relaxation doesn't erase the disc's pull. The expectation's reason, that the disc holds little mass early, is only partly right here: under this law it holds up to 30 % at z_f.

## How firm the shift is (after the result, not frozen)
Wilcoxon signed-rank on Δf p 0.016, on ρ p 0.039; sign test on Δf 7 of 8, p 0.07. Dropping any one seed leaves median Δf between +0.011 and +0.063, always positive. Without the two seeds with large centre jumps (1, 8): +0.037, ρ 1.058. The bootstrap on 8 seeds is coarse, and the lower end of Δf (+0.007) is close to 0. I'd call it a small rise, not a measured law.

## SPARC, SCALING ONLY (LC1's route: rule with floor, CE1's ng 64 table, one 10¹² number carried across SPARC's masses; not version N, no run of SPARC with this disc)
f_Q 0.946: **Υ 0.31 / 0.31, rms 0.0733 / 0.0746** canonical; alt 0.30 / 0.30. LC1 at 0.872: 0.32 / 0.32. Without contraction: 0.50 / 0.49. Line FAIL, as with LC1. No relief.

## Limits
- **Turnaround isn't sharp for this region.** Frozen mean-radius t_ta runs 2.76 to 5.67 Gyr, t_ta/t_f 0.45 to 0.93, median 0.57. Seed 3 has no maximum before z_f and isn't in the pairs (A1): it's a selection on the seeds. Seed 6 turns at 0.93 t_f and is nearly LC1. The median-radius side check often disagrees (seed 1 1.76 against 2.97 Gyr; seed 5 1.75 against 4.63). No other definition was run.
- **Centre jumps.** Seeds 1 and 8 jump up to 81 and 42 kpc, and 15 and 17 updates exceed R_d, while the shrinking-sphere centre moves between clumps. Others stay under 5 kpc. Not graded, disc mass is small then, but the disc teleports in those two.
- A smooth analytic disc, fixed physical size from the first moment, no clumps, outflows or back-reaction. Real early discs are smaller and clumpier, and gas in collapse isn't smooth. Linear growth is a stated choice, not derived, not scanned. One mass. Axis taken from LC1's z_f state.
- The "chaos floor" in the criteria turned out not to be one: the null run is the same engine, numerically nearly identical to X48 and ZN1. It tests the path, not how far a real perturbation decorrelates a pair. So seed-to-seed scatter in Δf is the only noise estimate here.

## Checks
K1 zero-mass disc through the disc's force call against `x48_fast` main, 60 steps: 0.0. K2 force 3.7e-7. K3 turnaround finder against the shell ODE 0.37 %. K4 LC1's reader on LC1's nine runs against `lc1_results.json`: 0.0. K5 preemption across both phases: 0.0. K6 whole-path null against X48's `snap_zf`: Q 1.000 at every radius, S ratio 1.000, stronger than its line (largest particle shift 5e-10 Mpc; I had expected chaos and exact equality didn't fail); at z = 0 against ZN1 Q within 0.002, same 2496 steps. K7 scaling route reproduces LC1 at 0.872: 0.0. MUTATE M_d × 2, seed 1: Q(3 R_d) − 1 from 0.931 to 1.606, +72 %, BITES.

**Wall time.** All runs 12:54 to 17:53, about 5 hours, on a machine shared at load 40 to 70. The nine-seed set finished by about 17:25, about 4.5 hours; MUTATE took the rest.
