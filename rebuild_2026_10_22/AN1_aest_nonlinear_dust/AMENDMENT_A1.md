# AN1 AMENDMENT A1: numerics and code faults found in first runs, before the production grid

Committed before any production row. Labels, pass lines, mu list, rows, tolerances: unchanged. **Disclosure: while debugging I ran about 20 development rows at N 1500 and saw their fold redshifts. They came from code with the faults below, and they are why I can no longer say the hand expectation was untouched; section 9 stands as written, and it was written first.**

| # | What failed | Change | Effect on frozen text |
|---|---|---|---|
| 1 | K1, K2, K5, K6 failed at the frozen eta 0.1: Hubble flow itself had truncation error larger than the signal (`an1_checks_RUN1.json`; K1 err -0.024, K2 slope 1.53) | **eta 0.005**; K7's eta test uses 0.0025 | section 4, K7. Tolerances unchanged |
| 2 | K5 energy drift 0.75, then 0.018 that did not change with N or eta. Traced: an isolated Neumann outer shell needs a boundary force, and a pinned wall opens a vacuum cell | K5: wall at 1500 kpc, filler density 1e-4 of centre, outer node pinned. Force was checked against numerical -dU/dr first | K5 setup only; line unchanged. Production uses Dirichlet, not this boundary |
| 3 | K3 F/g 0.028 at the first node only: self-similar centre error | Node spacing from cell second moment, exact for a quadratic density. rho_c 1e11 Msun/kpc^3, a math test (K3 didn't freeze rho_c) | Production too |
| 4 | K6 at eps 1e-4 was truncation noise | eps 1e-2, x still 7e-4 | K6's setup only |
| 5 | Bug: baryon stop `rb <= rf` was true for rf = infinity: all baryons pinned at z 20 | Fixed | none |
| 6 | Baryons on field nodes with a step M_b: force flicker, false fold at about z 3.7 | Baryons at q cell centres; M_b(<r) continuous | section 3 said same q; now half a cell off |
| 7 | Bug: shells with rf above their current r stopped at once at z 20; cluster gas was placed at its final radius | A shell stops only when falling (v <= 0): at r_f, or at turnaround if that is below r_f | section 3 stop rule made explicit |
| 8 | Outer shell had E = 0 with Dirichlet | One-sided E; folds in the outer 5 % of cells flagged `edge_artefact` | added flag; such a row is reported, and counts as UNRESOLVED if it's the row's fold |

Also: frozen R500 1.35 Mpc was written before I read that the median of all 12 X-COP systems is 1.24 Mpc. Kept at 1.35 as frozen; disclosed. Gas shells: only baryon charge up to M_gas(<R500) follows the beta model.
kappa = 1/2 FITTED. Reinstates nothing. Not theory closed.
