# SRJ1 RESULT: JOINT FAILS ON CLUSTERS, FRAGILE (R500 aperture) / JOINT FAILS ON CLUSTERS, FRAGILE (R500 aperture)

**Canonical / alt.** The settled-radius joint at f = 1 fails RB1's X-COP shape gate on both footings. It puts 30 to 36 % less
cold dark energy than the reference at 0.1 R500, so the model is too light in the cluster cores. Inner bins: +0.153 / +0.144 dex
against a line of 0.10. The reference passes the same gate (-0.007). f = 0.75, f = 1.25 and gas-only sourcing fail it too.
The amount rows do not decide it. At the last radius they are CONSISTENT, as they are for the reference. At R500 they are above
the line, as the reference already is. The FRAGILE tag names only that R500 bracket. The shape fail does not depend on it.

TEST lane. Criteria f21be18fd6 (committed alone, before any script or number). Scripts and outputs 46e480051f. No amendment.
The joint is post hoc to the forest row's fail (FRZ1, FZS1). This lane could only have given it a one-sided hold, which would
have needed a blind re-grade. It gives a fail on clusters instead, and an open forest window would not rescue the joint at
f = 1 (or 0.75 or 1.25). SRF1 and SRF1R were not opened. Footings never pooled. Cold dark energy is a gravitating field
component; no particle.

## The rule as run (criteria section 1)

- Reference = RB1's ZN4-native cold, anchored at R x M_b,obs at the aperture.
- Law's layout = FRZ1's cluster-regime form-B rule, transposed:
  - fc ~ 0.48 of the cold follows the reference shape;
  - the rest is the law's phantom of the observed gas + stars, capped at (1 - fc) x the cold inside R200;
  - the remainder is spread linearly to r_ta.
- R_set = f x R_fold. R_fold comes from FLD1's runs at each system's own z (X-COP 0.056 to 0.091) and M_b,fold = M200/(1+R)
  (log 13.99 to 14.41). That is extrapolated about 2 dex above FLD1's last mass as M_b^(1/3), which is FZS1's rule.
- R_set comes out at 2.0 to 2.7 Mpc: 1.16-1.17 R200 and 1.5-2.0 R500. In groups it is 1.2 to 1.6 R500.
- The junction factor is s = 1.000 in every cluster at f = 1. Beyond R200 the phantom has reached its cap, so the two layouts
  agree there. **f = 1.25 therefore gives exactly the f = 1 numbers.**

## Gates (RB1's statistics and lines, unchanged)

| row | canonical f 1.00 / 0.75 / 1.25 | alt f 1.00 / 0.75 / 1.25 | reference (joint off) |
|---|---|---|---|
| (a) X-COP q at r_last, median [95 %] | 1.171 [0.890, 1.237] / 1.122 [0.885, 1.235] / = f 1: CONSISTENT | 1.194 [0.890, 1.237] / 1.143 [0.885, 1.235] / = f 1: CONSISTENT | 1.095 [0.885, 1.259] |
| (a) bracket: at R500 (anchor R500) | 1.076 [1.012, 1.119] FAILS / 1.030 [0.966, 1.069] CONS. | 1.137 [1.067, 1.183] FAILS / 1.088 [1.018, 1.130] FAILS | 1.057 [1.046, 1.072] FAILS |
| (a) bracket: M_NFW at r_last | 1.050 [0.931, 1.176] CONS. | 1.050 [0.931, 1.176] CONS. | 1.032 [0.931, 1.174] |
| (a) reported: M_NFW at R500 | 0.995 [0.915, 1.047] | 1.053 [0.968, 1.104] | 0.959 [0.877, 1.094] |
| **(b) X-COP shape, bins 0-0.25 / -0.5 / -0.75 / -1 / 1-2 R500** | **+0.153 / +0.137 / +0.074 / -0.007 / -0.050 FAILS** | **+0.144 / +0.123 / +0.056 / -0.025 / -0.062 FAILS** | -0.007 / +0.033 / +0.006 / -0.030 / -0.041 |
| (b) at f 0.75 | +0.169 / +0.154 / +0.090 / +0.009 / -0.033 FAILS | +0.160 / +0.140 / +0.073 / -0.008 / -0.046 FAILS | |
| (b) gas alone sources the law | +0.165 / +0.142 / ... FAILS | +0.156 / +0.128 / ... FAILS | |
| (c) groups q at R500 | 0.651 [0.592, 0.710] / 0.619 [0.566, 0.672]: CONSISTENT, 0 of 20 above 1 | 0.654 [0.593, 0.714] / 0.620: CONSISTENT | 0.597 [0.556, 0.637] |
| (d) Bullet | not graded (criteria 2d) | not graded | |

- q is the joint's minimum cold over the measured cold. With the joint off it equals RB1's f_ret exactly.
- Per cluster at r_last, f 1 canonical: q_ref -> q (factor C_S/C_R):
  - A1795 0.885 -> 0.890 (1.005); A2029 0.934 -> 0.934 (1.000); A2142 1.235 -> 1.237 (1.002); A2319 1.259 -> 1.171 (0.930);
  - A644 2.216 -> 2.216 (1.000); A85 1.095 -> 1.181 (1.078); ZW1215 0.511 -> 0.511 (1.000).
  - Most last radii sit near R200, where the joint changes almost nothing.
- Predicted over measured hydrostatic mass at r_last: 0.91, 0.94, 1.19, 1.14, 1.86, 1.15, 0.55.
- Joint factor C_S/C_R inside X-COP, anchored at r_last, canonical: 0.63-0.70 at 0.1 R500, 0.68-0.75 at 0.25 R500,
  0.76-0.84 at 0.5 R500 and 0.89-1.06 at R500. Inside R500 the phantom of the cored gas is too small to replace the reference's
  central cusp.
- Groups: factor 1.003 to 1.149 at R500 (median 1.09). The joint adds cold at R500 there, so q rises by about 9 % and stays
  far below 1.
- Reported gate-2 ladder slope with q at R500: +0.133 [+0.056, +0.199] canonical, +0.146 alt; the reference gives +0.160.

## Checks and twins (all pass or bite)

- K1: with the joint off, RB1's committed numbers are reproduced to 4e-13: C-X at r_last and at R500, the two M_NFW rows, per
  cluster, G-H, gate 3's bins, both footings.
- K2: my transposed rule fed FRZ1's own halo (z 2.2, 1e13) equals FRZ1's layout to 8e-15. FZS1's fractions are reproduced:
  law 0.1282 / 0.3732 against 0.128 / 0.373, reference 0.1749 / 0.4580 against 0.175 / 0.458. R_set 0.4106, s 1.0582.
- K3: FLD1's radii are reproduced to 0.043 kpc. K4: the junction holds to 2e-16 and C_S never decreases. K5: 20 / 12 / 7.
- TW-N, no phantom inside R_set: moves the shape bins 0.160 / 0.157 dex rms (line 0.05) and exits 1.
- TW-0, f = 0: returns the reference to 0 and exits 1.

## Against the estimates

- **The lead's** (less cold inside half of R_set, then a fail at R500 or on shape): right on direction and right on the word.
  The fail is on shape, in the inner bins. At R500 the amount moves by under 10 %, and the reference already crosses the line
  there.
- **Mine** (the phantom reaches its cap inside R500, so the layout is cuspier): wrong for clusters. The law's layout is
  lighter than the reference everywhere inside R500 there and catches up only near R200. My 50 % on a shape fail was right in
  word and wrong in sign.

## What is not verified

- R_fold for clusters is FLD1's spherical, law-dominated shell result, extrapolated 2 dex in mass. f = 0.75 to 1.25 all fail.
  A much smaller R_set would shrink the region the joint changes, but it was not run, because the brief allows no scan.
- The transposition is a choice made before any number: the reference shape in place of FRZ1's NFW, the fc split, and the
  cap at the cold inside R200. A different shape inside R_set (pure phantom, say) is a different joint and was not graded.
- Group baryon profiles are FRZ1's bar_cum shapes normalised at R500, not measured profiles.
- The X-COP baryons are extended as M proportional to r from the last point to R200. This sets the phantom there, and so s,
  which scales the inner bins. s = 1.000 at f = 1; the f = 0.75 bracket, with s below 1, fails by more. A different
  extension was not run.
- The Bullet was not graded: RB1's graded row never uses the reference layout.
- One diagnostic print (the phantom unit cross-check, not in the criteria) had a unit slip in its ratio. It was fixed before
  the committed run. Gates, statistics and labels were untouched; the committed run reads 2e-15.

## Files

`FROZEN_CRITERIA.md` (f21be18fd6); `srj1.py` -> `srj1.out` / `.json`, `srj1_MUTATE_newton.*`, `srj1_MUTATE_f0.*` (46e480051f);
this file. The run takes 2 s on one thread, peak RSS 0.63 GB. RB1's and FZS1's code is copied; `fzs1_hm.py` is executed
read-only for K2 only. Nothing was fetched and nothing was pushed.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
