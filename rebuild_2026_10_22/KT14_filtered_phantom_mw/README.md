# KT14_filtered_phantom_mw: FILTER PASSES MW at xi = 2.0 kpc on alt (7 cells, all at box corners); NO XI PASSES on canonical, best D 1.15 at xi 2.0. A lead, post hoc, and owed dwarf spheroidals, SPARC and wide binaries before any claim

Criteria: `FROZEN_CRITERIA.md` (e496e39b6d), alone first, confirmed landed before any script, **not blind**. `kt14.py`, `kt14.out`, `kt14.json`, `kt14_MUTATE.out`, `kt14_MUTATE.json`, `run.log`. No download. κ = 1/2 FITTED and held fixed. Footings never pooled. Not theory closed. Register K825.

Field equation: Phi = Phi_N[rho] + QUMOND[rho_xi] - Phi_N[rho_xi], rho_xi a 3D Gaussian (sigma xi) of rho, the board law's simple nu, UX5's grid and lines, KT13's 1375 in-prior cells per footing.

| xi, kpc | canonical: L1 / all four, lowest K with v_c in line, best D (v_c, K, Ou) | alt: L1 / all four, lowest K, best D (v_c, K, Ou) |
|---|---|---|
| 0 (plain QUMOND) | 433 / 0, 76.0, 2.37 (220.2, 76.4, 142) | 701 / 0, 76.3, 1.94 (219.4, 74.9, 116) |
| 0.25 | 426 / 0, 75.8, 2.38 | 693 / 0, 76.7, 1.96 |
| 0.5 | 415 / 0, 75.5, 2.29 | 680 / 0, 76.1, 1.95 |
| 1.0 | 396 / 0, 72.5, 1.57 (224.0, 73.3, 85) | 665 / 0, 71.8, 1.31 (222.1, 72.1, 78) |
| 2.0 | 357 / 0, 67.6, 1.15 (225.3, 71.3, 69) | 623 / **7**, 66.4, 0.83 (225.0, 69.8, 50) |
| **Label** | **NO XI PASSES** | **FILTER PASSES MW at xi = 2.0 kpc** |

## Reading
- **The mechanism works as the hand estimate said.** Smoothing the phantom's source over about 1-2 kpc pulls the lowest K with v_c in line from 76 down to 66-68, close to the measured 66.4, while v_c barely moves (v_c max 236.7 -> 235.3). This is the first time on star-count baryons that the Milky Way's v_c and K_z are both reachable. The expected pass at 1-2 kpc appeared at 2.
- **It's thin.** Every one of the 7 alt cells is in BV2 (thick R_d 2.0) at the box's largest thick-disc height (1.08 kpc), 6 of 7 at the largest thick share 0.35 (star counts: 12 +- 4 percent, RF1 A4), and K(R0) 69.8-70.7 against a line top of 70.8. Canonical misses on Ou (69 vs 59.9) and K (71.3).
- **The K_z scale length fails everywhere:** strict h count 0 at every xi on both footings, h 3.35-3.40 at the passing cells against 2.72 +- 0.15. Smoothing spreads the phantom radially as well as vertically, so K falls off more slowly with R. Newton alone gives h 2.98 (MUTATE), passing strict in 53 cells. The strict line isn't in the frozen class, but it's a real measurement and it fails.
- **xi = 2 kpc is a new number, fitted to this galaxy.** The record's heat filter has xi >= 0.03 pc, set by Cassini. Nothing fixes 2 kpc.

## What it's owed, as frozen
1. **Dwarf spheroidals.** With a universal xi = 2 kpc, a dwarf with r_half 0.3-0.7 kpc has its own phantom smeared over a volume about 30-300 times larger. By hand, the internal boost at r_half falls by about (r_half / xi)^1.5, a factor of 10-20. They'd be nearly Newtonian inside, far below their measured dispersions. **I expect this to kill a universal xi.** It's the next lane.
2. **SPARC:** inner points of small discs (R_d under 2 kpc) lose their boost the same way.
3. **Wide binaries:** a binary's own phantom is gone, so the internal motion is Newtonian plus the external field.
4. Cassini and lensing.

A scale that grows with the system, for example xi proportional to the MOND radius sqrt(G M / a0) (about 9 kpc for the Milky Way, 0.16 kpc for Fornax), would keep dwarfs and still give 2 kpc here. That's a different, non-linear field equation, not tested, and the factor would be fitted.

## Checks
C1: xi = 0 reproduces UX5's form Q on all 1375 cells per footing, max relative 0. C2: smoothed mass on the solver grid within 1.6e-4 of the original, bulge fine grid within 7.1e-5, every xi. C3: radial 2D Gaussian smoothing to 1.4e-4, vertical to 5e-9. Q5: doubled grid on the best passing cell, dK +0.05, dv +0.08: converged. MUTATE (phantom off, xi 1): returns Newton, v_c max 200.0, L1 passes in no cell, exit 1.

**Disclosed.** The first launch crashed (numpy here has no `trapezoid`; replaced by `trapz`) and used 1.45 GB building the smoothing matrix in one piece; I made it chunked and reran. **Peak RSS of the full run was still 1.8 GB, above the 1 GB the criteria set**, while another multi-process job was live. No swap was recorded. Runtime 14.6 minutes, nice 15. Matmul RuntimeWarnings from this machine's BLAS were suppressed; every check output is finite and passes.
