# KQ1 RESULT: K(Q) dust in the law's field at X-COP CANNOT FORM the cored cluster profile, on either footing

**Label line:** canonical: CANNOT FORM CORE | alt: CANNOT FORM CORE | overall: **CANNOT FORM CORE** (secondary
concentration band 0.21-0.30 too). No mu_K in 0.1-1e4 Mpc^-1 (28 grid values + 4 refined, per footing) passes L1-L5.
Closest profile: mu_K 19.05 Mpc^-1 (lambda_0 0.33 Mpc) on both footings, failing L3 (c = 1.000 vs 0.2475-0.2665) and
L4 (per-bin rms 0.784 / 0.758 vs 0.10, inner bin -1.08 / -1.04).

Criteria `FROZEN_CRITERIA.md` (07534f282b, committed alone before any script or number); amendment A1 `AMENDMENT_A1.md`
(ce3033f48b, POST-FREEZE, after a partial first run, before the rerun). Script `kq1.py`. Outputs `kq1.json` / `kq1.out`
/ `run_main.txt` and `kq1_MUTATE.json` / `kq1_MUTATE.out` / `run_mutate.txt`. The first run's partial log is kept
unedited as `kq1_FIRSTRUN_preA1.out`. TEST lane on the F1-CONFIRMED branch. Adopts nothing. Kappa = 1/2 FITTED; not
theory closed. The component is cold dark energy (v3s's K(Q) dust); there is no particle.

## What was solved

The record's own host-hydrostatic n = 1 solver (QX7 iter_5 `profile`, executed read-only through NA2's prefix):
d rho/dr = -(mu_K^2 / 4 pi G) g_law(G (M_b + M_d)/r^2). That is K(Q)'s pressure with Jeans wavenumber mu_K, in the a0
law's field of the X-COP gas + stars plus the dust itself. The static spherical interior of the blend reduces to that
law (BL3, scoped). The total per cluster is KD1's X-COP need, F_X = 4.1786 / 3.7833 times M_b at the last data radius.
All 7 clusters were run at every mu_K, on both footings.

## Known answers and MUTATE (all PASS / bite / hold before grading)

| Check | canonical | alt |
|---|---|---|
| KA1 law alone, X-COP mean (mine = NA2 x_eval = GB1 g_xcop) | 0.467499 | 0.434523 |
| KA2 KD1 f-table / capture | 4.1786 / 4.1110 | 3.7833 / 4.1121 |
| KA2 KD1 KD at mu* through GB1 G2 | -0.702864 / 0.802677 (= kd1.json) | -0.714392 / 0.809485 (=) |
| KA3 solver: isolated sinc r_s; iter_5 lambda_0 3.162 X-COP | 3.6e-7; +0.0334 / 0.2293 (= record) | -0.0019 / 0.2249 (=) |
| KA4 calculators, analytic r_c 100 | r_1/2 100.000, slope(20 kpc) -0.0769 | |
| KA5 (A1) calculators on solver grid, sinc mu 5 | r_1/2 379.097 vs 379.099 kpc; slope 0.00333 vs 0.00334 | |
| M1 mu_K -> inf (mu* 8.89e6 and 1e9) | enclosed fraction 1 at all X-COP radii; G2 -0.702864 = KD1's cusp; r_1/2 2e-4 / 2e-6 kpc, L1 FAILS: BITES | same, -0.714392: BITES |
| M2 law alone | mean 0.4675, rms 0.476, L4 FAILS: BITES | 0.4345, 0.444: BITES |
| M3 planted cored isothermal r_c 100 at need | r_1/2 100.0, slope 0.077, c 0.2485-0.2663, rms 0.0908, bins +0.010 / -0.007 / -0.077: L1-L4 PASS, HOLDS | rms 0.0907: HOLDS |

## The scan (canonical; alt reads the same within 0.03 dex)

| mu_K (Mpc^-1) | lambda_0 (Mpc) | r_1/2 (kpc) | L2 slope <=20 kpc | c | per-bin rms; bins 0-0.25 / 0.25-0.5 / 0.5-0.75 | fails | KD1 model P SPARC G1 at this mu_K | iter_5 host-held G5/G6/G7 |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 62.8 | 2334-3087 | 0.020 | 0.051 | 0.472; +0.54 / +0.50 / +0.37 | 3 | PASS (0 captured) | P/P/P |
| 1.0 | 6.28 | 860-1059 | 0.026 | 0.060-0.063 | 0.324; +0.44 / +0.31 / +0.06 | 3 | PASS (0) | P/F/P |
| 2.51 (best rms) | 2.50 | 494-577 | 0.026 | 0.101-0.136 | **0.226**; +0.16 / -0.07 / -0.28 | 3 | PASS (0) | P/F/P |
| 3.98 (c crosses 0.25) | 1.58 | 360-406 | 0.025 | 0.238-0.341 | 0.297; -0.10 / -0.34 / -0.35 | 3 | PASS (0) | P/F/P |
| 6.31 | 1.00 | 254-276 | 0.025 | 0.58-0.78 | 0.456 | 3 | PASS (0) | P/F/P |
| 10 | 0.63 | 173-182 | 0.029 | 0.997-1.000 | 0.619 | 3 | PASS (711/2696 pts) | P/F/P |
| **19.05 (closest)** | 0.33 | **96-98** | 0.059 | **1.000** | **0.784**; -1.08 / -0.61 / -0.35 | 2 (L3, L4) | PASS (1599/2696) | P/F/P |
| 25.1 (r_1/2 ~ 75) | 0.25 | 74-75 | 0.094 | 1.000 | 0.808; -1.11 / -0.61 / -0.35 | 2 | PASS (1925) | F/F/P |
| 33.1 | 0.19 | 56-57 | 0.157 | 1.000 | 0.808 | 2 | | |
| 39.8 | 0.16 | 47 | 0.226 | 1.000 | 0.808 | 3 | FAIL (Z -0.011, rms 0.153) | F/F/F |
| 79.43 (galaxy bound) | 0.079 | 24 | 1.03 | 1.000 | 0.808 | 4 | FAIL (Z -0.082, rms 0.208) | F/F/F |
| >= 158 | <= 0.04 | <= 12 | surface inside 20 kpc | 1.000 | 0.808 = KD1's cusp | 4 | FAIL, toward KD1's -0.72 | F/F/F |

The dust is retained (r_s < r_ta0) in every cell, so L5 passes everywhere.

**Why it cannot.** Everything follows from one fact. In the law's field g ~ 1/r, the n = 1 equilibrium has
rho = rho_c - (mu_K^2 / 4 pi G) * integral of g dr, which falls like ln(r_s / r), not like r^-2. It has a hard surface
r_s.
- The core size and the extent are tied by the single Jeans length. When r_1/2 is 50-100 kpc (mu_K 19-33), the surface
  sits at r_s ~ 160 kpc. All of KD1's amount is then inside 0.25 R500: c = 1.000, the inner bin is over-filled by
  1.1 dex, and the outer bins are short by 0.35-0.6.
- When the dust reaches 0.7 R500 with c near 0.25 (mu_K ~ 4), the core is 360-400 kpc, 4-8 times the target. The
  profile is still log-flat, so the inner bin is over (-0.10) and the middle bins over (-0.34).
- The best per-bin rms anywhere is 0.226 / 0.222 at mu_K 2.5 (iter_5's 0.225, reproduced). That is 2.3 times the line.
  There, r_1/2 ~ 500 kpc and c 0.10-0.15.
- Freeing the amount does not rescue the closest profile. On a coarse F grid 1-12, the best is F = 1 (the grid edge),
  with rms 0.369 / 0.376 and an inner bin of -0.53. The M_d(<tl) normalisation bracket is identical, because all the
  dust is inside tl.

## mu_K needed (or the closest miss) vs the record's two bounds

| | canonical | alt |
|---|---|---|
| mu_K that forms the core | **none** | **none** |
| closest (fewest failed lines) | 19.05 Mpc^-1: L3 margin -0.733 (c 1.000 vs <= 0.2665), L4 rms 0.784 (margin -0.684), worst bin -1.08 (margin -0.977); L1 r_1/2 96.2-98.2 kpc (margins +46.7 / +2.3 kpc), L2 0.059 (margin +0.441), L5 PASS | 19.05: L3 -0.733, L4 rms 0.758 (-0.658), bin -1.04 (-0.942); L1 95.5-97.9 (+46.0 / +2.6), L2 0.061 (+0.439), L5 PASS |
| BBN side (KD1 B1b, mu_K >= 8.890e6 / 8.889e6 Mpc^-1, physical; frw_dust stiff phase <= 0.067 of radiation at 0.1 MeV, Delta N_eff <= 0.5) | closest is 4.67e5 times below | same |
| galaxy side (QX3 g3 capture bound, mu_K <= 79.43 Mpc^-1; KD1 KA4) | closest is inside (0.24 of the bound) | same |
| iter_5 host-held galaxy gates (pass only at lambda_0 >= 10 Mpc, mu_K <= 0.63) | closest fails G6 (KiDS) there | same |
| X14 q_K at l 156 kpc | 3.24 (K(Q) not inert at the fold scale here) | 3.05 |

At mu_K = 8.89e6, where BBN allows the dust, the solver gives KD1's 0.35 pc cusp (M1), and X-COP is over-predicted
by 0.70 dex.

## The galaxy-capture cost (KD1 4.111 / 4.112), carried

- **The per-system captured fraction does not change.** f_cap omega_d/omega_b = 4.111 / 4.112 does not depend on mu_K,
  and it is still 13-21 times SPARC's cap of 0.3257 / 0.1937.
- **What mu_K changes is who captures, and where the dust sits.** At the closest mu_K 19.05, KD1's model P Jeans mass
  at turnaround is 1.1e11 Msun.
  - 1599 of 2696 SPARC points sit in systems that capture.
  - The isolated sinc core (pi/mu_K = 165 kpc) keeps the dust outside the discs, so KD1's own model P reads G1 PASS
    (Z +0.020 / -0.008).
  - But the record's host-hydrostatic reading (iter_5) at lambda_0 0.32 Mpc fails G6 KiDS lensing. The host squeezes
    the 4.1 M_b of dust inside a few hundred kpc.
- So the capture cost stays: it moves from SPARC (KD1, mu*) to KiDS (iter_5) but does not go away. This is reported,
  not graded. Model P's G1 passes for every mu_K <= 25, and fails from 39.8 up.

## Compute

Peak RSS 218 MB (main), 208 MB (MUTATE). One thread, nice 10-15. Main 9 min 24 s, MUTATE 45 s. SIGTERM handler
writes a `_partial` checkpoint.

## Disclosures

1. **A1 (post-freeze).** The first main run was stopped after 7 canonical rows (log kept). rho came from np.gradient on
   a solver grid that starts at M = 0, which gave a spurious slope of 1.005 on L2 at every mu_K. The calculators now
   start at grid index 2, and KA5 was added. The A1 rerun moved r_1/2 on those 7 rows by <= 0.6 % (from
   the 0.3 % rho(0) fix); c and rms are identical. Lines, grid and labels are unchanged.
2. **The grid holds mu_K 631 twice** (logspace's 630.96 and the stated 631). Both rows are identical except the L2
   slope, which there is the surface edge inside 20 kpc (large in both). No effect.
3. **L2 slopes of 10^2-10^4 at mu_K >= 158** come from the hard surface r_s < 20 kpc (rho -> 0), not from noise.
4. **The fitted-amount reading uses a coarse F grid {1, ..., 12}.** Its best value is at the lower edge (F = 1), so the
   true minimum may sit at F < 1. That is far below KD1's need, and it is reported only.
5. **The galaxy readings are reported, not graded.** KD1's model P was run through GB1's g_sparc at each mu_K.
   iter_5's host-held G5/G6/G7 are read from qx7_iter5.json at the nearest recorded lambda_0. Neither enters the
   label.
6. **Baryons beyond the last X-COP data radius are held constant** (iter_5 XPROF). The law's field is applied to the
   enclosed baryons + dust (as frozen).
7. No QX3 iter2 lensing number enters any line. GL1's mu_J = 631 is a grid point only.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
