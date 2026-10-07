# CFG382: one dimensionless fluid-lapse coupling. Does it pay for itself?

Criteria: `FROZEN_CRITERIA.md` (1f66028cc), Amendment 1 (97307dde9, before any script: clusters scored at R500 against 0.430).

**Verdict: PARTIAL** (primary: V = 200 km/s, tau since z = 2). Settling rate Gamma = lambda sqrt(4 pi G rho_tot). lambda = 0.028, fixed once by the MW floor (0.14 at 30 kpc).

| prediction (no further freedom) | predicted | measured | |
|---|---|---|---|
| P1 groups (Lovisari, R500) | 0.722 | 0.60 +- 0.15 | PASS |
| P2 clusters (X-COP, R500) | 0.714 | 0.430 +- 0.15 (like-for-like) | FAIL (would PASS against the 1-Mpc 0.576) |
| P3 pincer | Gamma MW 3.35 H_L >= 1.73; cluster 0.57 H_L <= 1.93 (and <= 1.04 central) | | PASS |
| P4 UFD direction | e = 3e-30 (fully settled) | large excess | FAIL (conflict) |

The brackets (V 180-230, tau since z = 1/2/4) give the same picture: PARTIAL, or FAILS at V = 230.

**Two structural lessons (they hold for ANY local-density-keyed rate):**
1. **Groups and clusters cannot be separated.** R500 is DEFINED by mean density, so local rho(R500) is the same for both (1.5e-24 vs 1.6e-24 kg/m^3). Their measured levels differ at R500 (0.60 vs 0.43), so any rate keyed to local density predicts one number for both.
2. **The UFD conflict.** Ultra-faints are the DENSEST systems (6.7e-20 kg/m^3), so a dynamical rate settles them completely. They show the LARGEST excess. Their excess must come from history (pre-reionisation collapse, CFG338/344), not from the settling rate.

**Reading.** One dimensionless constant does three things right: the galaxy floor (by construction), groups (no freedom), and CFG245's pincer, the galaxy/cluster rate window that sank the vacuum-rate lane. It cannot do clusters at R500 or UFDs. Those need something beyond a local rate (history, or a reservoir inside R500, as CFG379 found).

Controls: C1 calibration and C2 pass. MUTATE (lambda x 3) moves groups 0.72 -> 0.38, rc 1. The growth / sigma8 consequence was not run (it needs the PM engine).

## Post-run target audit (labelled; `cfg382_target_audit.py`; the frozen PARTIAL stands)
The targets above mixed definitions: the group 0.60 is cm03's definition B with a weak-lensing bias, while the cluster 0.430 is definition A with no bias. Here both are on definition A with the SAME hydrostatic bias b (groups: stars := 0.10 M_gas placeholder, which leans high, disclosed):

| b | groups (Lovisari 20) | clusters (X-COP 7) |
|---|---|---|
| 0.0 | 0.79 [0.53-1.40] | 0.41 [0.36-0.50] |
| 0.1 | 1.04 [0.75-1.72] | 0.54 [0.48-0.63] |
| 0.2 | 1.35 [1.02-2.11] | 0.70 [0.63-0.79] |
| 0.3 | 1.76 [1.38-2.61] | 0.91 [0.83-0.99] |

**Reading.**
- (1) The levels move by about x2 across plausible hydrostatic bias, which is more than the differences any mechanism test here is trying to resolve. **Retention-level fitting cannot discriminate mechanisms until group and cluster masses are lensing-calibrated on one footing.**
- (2) The ordering that survives every b: groups need about TWICE the excess-per-present-baryon of clusters. A local-density-keyed rate predicts equality (CFG382). The ordering instead follows BARYON DEPLETION (groups are gas-poorer), as the original-baryon reservoir reading expects (CFG365).
