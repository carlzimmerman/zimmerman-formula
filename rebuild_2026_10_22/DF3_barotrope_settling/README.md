# DF3_barotrope_settling: NEITHER. No DF2 passer holds discs and clusters. Γ 5/3 collapses into a sub-kpc core with the whole fair share; Γ 1 and 2/3 have no equilibrium in clusters

Criteria `FROZEN_CRITERIA.md` (f5093bf4d8), committed alone first. `AMENDMENT_A1.md`, post-result. `df3_solver.py`, `df3_run.py`, `df3_controls.py`, `df3_cell_*.out`, `df3_map.out`. A requirement map: it adopts nothing, reinstates no retired sector, offers no action. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. A family statement on these inputs, not a no-go theorem.

## The five gate-1 passers, solved, canonical (alt beside in the outputs, same read)
| Γ, σ km/s | X-COP mean, rms | Keys | SPARC rms, Υ, tilt | Groups Z | M_f/M_b at R_last, median | NO EQUILIBRIUM: clusters (X-COP), SPARC, groups | Read |
|---|---|---|---|---|---|---|---|
| 5/3, 100 | −1.284, 1.357 | 2 of 15 | 0.578, 0.30, 0.00 | −8.49 | 5.36, all of it | 0, 0, 0 | settles in, FAIL |
| 5/3, 30 | −1.284, 1.357 | 2 of 15 | 0.628, 0.30, 0.00 | −8.50 | 5.36, all of it | 0, 0, 0 | settles in, FAIL |
| 1, 100 | +0.465, 0.474 | 10 of 15 | 0.0715, 0.45, +0.11 | −1.45 | 0.007 | 1.00, 0.35, 1.00 | no equilibrium, FAIL |
| 1, 30 | no equilibrium (A1) | not meaningful | 0.458, 0.30, 0.00 | −0.19 | 0.20 | 1.00 by A1, 0.69, 0.95 | no equilibrium, FAIL |
| 2/3, 30 | +0.466, 0.475 | 10 of 15 | 0.0541, 0.52, +0.03 | −4.48 | 0.0004 | 1.00, 0.29, 0.82 | no equilibrium, FAIL |

Where NO EQUILIBRIUM is 1.00 the numbers are the law's plus whatever small mass an equilibrium holds; the rest of the fair share is unaccounted for, so a pass-like row there isn't a pass. Γ 2/3's SPARC row is the law's for that reason. X-COP by x at Γ 5/3 is −2.01 at x 0.1 to −0.81 at 0.7, M_f/M_b 957 to 39: a point mass, and over-massive everywhere.

## Why
- **Γ 5/3:** the anchor makes it soft at low density. At a cluster's mean density c_s is far below V, so it compresses until c_s reaches V. Newtonian scaling from the controls gives R near 0.4 kpc at σ 100 and M 3e14 M☉, and R ∝ σ². So DF2's worry was too mild: it doesn't sit near ρ_a in a disc, it sits well above, with half its mass inside 0.03 to 0.26 R_last.
- **Γ ≤ 1:** softer as it compresses. M_max near 2.5 σ² r_ta / G, Bonnor-Ebert type, and a cluster's fair share is far above that at any σ on DF2's table (K_isothermal_max checks the coefficient: 2.518).

## Map, canonical, numbers only (`df3_map.out`)
No (Γ, σ) of 18 passes X-COP, SPARC and groups together, so nothing went to the keys or back to gate 1. Closest on X-COP: Γ 1, σ 1000, +0.182, 0.234, NO EQUILIBRIUM 1.00, groups −4.74. Γ 5/3 stays at X-COP −1.284 through σ 1000. By the scaling above, not run, a core reaching about 1 Mpc needs σ near 5000 km/s, which scales c_s at z 1100 to near c/6, far off DF2's table. Γ 2/3 at σ 300 and 1000 spreads out with an equilibrium, and reads as the law plus a thin fluid: X-COP +0.46, groups −4.7.

So the anchor forces a choice: too soft and it collapses, or stiff enough to stay out and then it does nothing for clusters.

## Bullet
The standing kill on pressure fluids (X19, MG1) stands; not re-derived. Order of magnitude: Γ ≤ 1 has no equilibrium to offset. Γ 5/3's core has a column of at least about 1e7 M☉/pc² at the grid's limit, far above anything it sweeps, so it would pass through the other cluster and stay with the galaxies. That is the right sign for the offset, but it comes from a point mass of 1e14 M☉, which X-COP's −2.01 and the keys already exclude. Bullet columns are grid bounds, not measured values, and the Mach numbers printed for the unresolved core carry no weight.

## My expectation
On record: NEITHER, Γ ≤ 1 without equilibria, Γ 5/3 settling. It held. Wrong in degree: I put Γ 5/3 near ρ_a in discs, and it goes much denser. I said σ near 1000 might help clusters at Γ 5/3; it doesn't.

## Controls
Lane-Emden ρ_c/ρ̄ 6.04 (5.991) and ξ₁ 3.664 (3.654). Isothermal limit 2.518 (2.52). K x 16 ρ_c ratio within 0.03 %. Fair share within 0.02 %, grid doubling 0.04 %. Law limit: X-COP +0.467, 0.476, SPARC 0.0541. Planted σ 3: rms 0.63, fails.

## Not verified
Static, spherical, no rotation, no infall, no time evolution: whether the fluid ever reaches these states isn't computed, and AN1's folding warning applies. Fair share is an upper bound; retention wasn't scanned. Cores are below the grid at Γ 5/3. Relativistic corrections ignored: c_s printed near 1e4 km/s at some unresolved cores, and those values carry no weight. The artefact in A1 is read, not fixed. No forest, no action, no production.
