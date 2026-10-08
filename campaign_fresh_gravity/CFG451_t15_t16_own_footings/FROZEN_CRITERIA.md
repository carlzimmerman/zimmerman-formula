# CFG451 FROZEN CRITERIA: T15 (cold budget) and T16 (coupling gradient) re-run on the framework's own a0

Frozen before any CFG451 script exists. kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10) are
reported separately, never pooled. No dark-matter particle; the cold fluid's mass is still required. Read-only on
deepseek_push (T15, T16) and CFG450: no file there is edited.

## Why
T15 and T16 compute the kernel supply S(<R)/M_b = 1/(exp(r_t/R) - 1), r_t = sqrt(G M_b / a0), with a0 = 1.2e-10, which is
neither footing (found in CFG450). Their deficits came from the canonical audit. This lane puts every a0-dependent piece on one
footing at a time.

## What changes and what is held
- **On the footing:** a0 in S for the MW 30-kpc point, groups and clusters; the group/cluster deficits from CFG450's
  `cfg450_results.json` (unrounded medians, gas at R500, b = 0 and 0.3) at the same footing.
- **Held (a0-independent, as on disk):** lambda = 0.028 (CFG382: fixed by the MW floor e = 0.14 at 30 kpc with
  rho = V^2/(4 pi G r^2), no a0); tau = 10.3 Gyr; rho_R500 = 1.55e-24; f_law(R500) = 0.286; the MW deficits (V^2 r/G vs M_b,
  M_b 7e10 and 1e11); the group/cluster M_b and R500 conventions (6e12 / 554 kpc; 2.8e13 / 985 kpc); T12's lambda range
  [0.029, 0.066].
- T15/T16's formulas are copied verbatim; only a0 and the deficits change.

## Verdict items (each footing separately, read off the declared numbers)
- **V1 cluster budget:** T15 M_cold/M_b for clusters < 0 at b = 0 and b = 0.3 -> "clusters overdraft" stands; any >= 0 -> it breaks.
- **V2 group knife-edge:** sign of groups b = 0.3 M_cold/M_b (reported; |value| < 0.15 = knife-edge as T15 declared).
- **V3 MW-30:** the V (km/s, M_b = 7e10) at which the MW budget turns infeasible (x > S), found by bisection on [150, 300].
- **V4 floor bind (T16 C3):** lambda_floor 0.028 / upper cluster window >= 1.5 -> "floor and clusters cannot share one lambda"
  stands; 1.0-1.5 -> WEAKENED; < 1.0 -> the floor fits the cluster window (the bind breaks).
- **V5 three-way intersection** of the MW (M_b 7e10, feasible V of 188/200/230), group and cluster lambda windows:
  nonempty or empty, and its bounds.
- **V6 T15 C5:** T12's lower lambda 0.029 / cluster lambda_max (reported).

## Controls
- **C1:** with a0 = 1.2e-10 and the original rounded deficits (0.79/1.76, 0.41/0.91), the copied code reproduces the
  committed t15_results.json (rows, ceil, res, viol) and t16_results.json (mw lam_max/feasible, others, windows, inter,
  gap_floor_cl) to 1e-9.
- **C2:** the CFG450 deficits read in are its committed medians (canonical clusters 0.4135/0.9054 to 1e-3).
- **MUTATE (CFG451_MUTATE=1):** T15's own planted misread f_law := deficit; V1 must flip (cluster M_cold >= 0) on both
  footings. Outputs go to *_MUTATE files.

A failed control is reported and kept, never silently fixed.
