# QX11: on the action's exact field, FG1's tilt row FAILS on the canonical footing (+0.170 vs |t| <= 0.15); passes alt

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings never pooled. Criteria: FROZEN_CRITERIA.md
(610ce3a4ef), committed alone before any script. Script: qx11.py. It reuses QX8's loader, fitter and solved parts
read-only, and takes about 1 minute on one thread.

## Plainly

The a0 law as an algebraic law passes FG1's tilt row (+0.020 / -0.020). The action's exact AQUAL solution FAILS that
row on the canonical footing: t = +0.170 against FG1's line |t| <= 0.15. It passes alt at +0.090.

The miss is narrow and noisy. The bootstrap sd of t is 0.127 (exact field) and 0.100 (law), and 63% of the
canonical exact-field draws exceed the line. The label uses FG1's line as FG1 used it, with no error, and the line is
not moved.

Mechanism: the exact field lowers predicted accelerations most in low-surface-brightness, slow discs (QX8). Their
refit Upsilon rises. On the exact field, median U is 0.71 at Vflat < 100 (n 47) against 0.54 at Vflat > 150 (n 53),
canonical.

## FG1's C4 (the law alone) on the exact field

| Line | canonical | alt |
|---|---|---|
| S SPARC (rms <= 0.110, U in 0.50-0.80) | PASS rms 0.0560, U 0.58 (law 0.0541, 0.52) | **PASS** rms 0.0558, U 0.52 (law FAILED at U 0.44) |
| Tl tilt (|t| <= 0.15) | **FAIL +0.170** (boot sd 0.127; law +0.020) | PASS +0.090 (boot sd 0.097; law -0.020) |
| LT LITTLE THINGS | PASS -0.025 (exact = law) | PASS -0.064 (exact = law) |
| G, K, X, Ln, Dw, MW, DM, IC | carried from FG1: K, Dw, MW, IC FAIL; G, Ln PASS; X, DM NOT GRADED | same, alt cells |
| **C4 on the exact field** | **FAILS: Tl, K, Dw, MW, IC** (law: K, Dw, MW, IC) | **FAILS: K, Dw, MW, IC** (law: S, K, Dw, MW, IC) |

So moving the flagship from the law to the action's exact field trades the alt footing's S failure for the
canonical footing's Tl failure. Neither footing passes FG1's full gate set either way; the cluster, dwarf, Milky Way
and IC 1613 lines fail regardless.

Median U by speed bin on the exact field (FG1's bins), canonical: 20-60 0.495, 60-100 0.800, 100-150 0.710,
150-200 0.460, 200-250 0.560, 250-400 0.700. Alt figures are in qx11.out.

## Why the other rows carry

In spherical symmetry the AQUAL equation integrates exactly to mu(g/a0) g = g_N, so the exact field equals the law.
FG1's LT, G, K, Ln and Dw statistics use point or spherical models. MW is already X5's AQUAL row. IC is carried by
argument: QX8's largest low-surface-brightness correction (about -0.20 dex) cannot close E -0.59 (Z -7.9). A
disc-modelled exact field for LT, Dw or IC would be a new statistic and is not graded.

## Known answers and controls

- KA1: law mode reproduces FG1's tilt (+0.020 / -0.020) and U (0.52 / 0.44) exactly.
- KA2: law LT from SL1's cache matches FG1 (|d| 0).
- KA3: exact S matches QX8 exactly.
- KA4: exact t matches QX9 exactly.
- MUTATE (g_obs x1.5 at 0 < Vflat < 100, separate outputs qx11_MUTATE.*): exact-field t reaches +0.66 canonical
  and +0.69 alt, so the control bites (exit 1).
- Rerun: qx11.json byte-identical (sha1 fb6e19bb5cb9).

## Not shown

No new data are used. There is no disc-modelled exact field for LITTLE THINGS, the dwarfs or IC 1613, no error model
on FG1's line, and no change to PAPER67 (its tilt statement is about the law, which still passes).
