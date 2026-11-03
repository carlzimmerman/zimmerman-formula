# KT12_compact_kernel_milky_way: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep going". KT11 left the compact kernel with one open question on rho_DE: SPARC asked for stars 41 percent heavier (disc 0.705) than its tolerance allowed. This lane asks the one galaxy whose stellar mass comes from star counts, not rotation: the Milky Way. κ = 1/2 FITTED and held fixed, so this tests a kernel, not κ. Footings canonical 9.3603e-11 (about rho_DE) and alt 1.1312e-10 (about rho_crit), both reported, never pooled. Not theory closed. No cold component, no particle. No download.

**Not blind.** Read before this freeze: UX5's README, criteria, `ux5_core.py`, `ux5_grid.py`, `ux5_read.py`, `ux5_checks.py`, the timing line, and the first row of `cache/canonical_1.0.jsonl` (Newton v_c 232.6, K(R0) 65.4 for Sigma_b 40.3, M_bb 1.64e10, R_d 1.93). RF1's README. By hand: at R0 the observed g is about 2.2 a0 canonical and 1.8 a0 alt, where the compact kernel is exactly or nearly Newtonian, so I expect v_c to need a Newtonian disc near 229 km/s, which the box reaches only at short R_d, and I expect K_z to sit near Newton's and pass. My expectation: v_c fails in priors on both footings. Any other result is reported as found.

## Kernel
mu(x) = x - x^2/4 for x <= 2, mu = 1 above, x = g/a0 (KT11's mu = 2Y - Y^2, Y = g/s, s = 2 a0). QUMOND nu(y), y = g_N/a0: nu = 1 for y >= 2; below, x solves x^2 (1 - x/4) = y on (0, 2], nu = x/y. Deep limit nu -> y^(-1/2), the same a0 as the law.

## Solve and gate (UX5's, unchanged)
Form Q only: lap Phi = div[nu(|grad Phi_N|) grad Phi_N] on UX5's grid, face fluxes and LU, via `ux5_core` with nu swapped. Form A isn't rerun; UX5 found Q and A within 0.13 percent in K for the law. Boxes B175, BV, BV2 exactly as UX5. Lines L1 v_c, L2a chi2_Kz <= 67.459, L2b |K(R0) - 66.4| <= 4.4, L3 Ou chi2 <= 59.89. Classes FEASIBLE IN PRIORS (UX5's R_d tag 2.38-2.90 and M* tag 3.80-8.36e10), FEASIBLE (WIDE PRIORS ONLY), V+K ONLY, INFEASIBLE. Strict count (|h - 2.72| <= 0.30) reported beside, no class change. Nothing moved.

## Labels, per footing
- **MW PASSES IN PRIORS:** class FEASIBLE IN PRIORS on B175, BV or BV2. Said with the box.
- **MW WIDE PRIORS ONLY:** FEASIBLE (WIDE PRIORS ONLY) in every box that has cells, none in priors.
- **MW FAILS:** V+K ONLY or INFEASIBLE in every box. The line that fails is named (L1, L2, L3) from the in-prior best cell.

What it means, stated now. No joint pass is possible from this lane: canonical failed SPARC's stellar scale and alt failed Cassini in KT11. On canonical, a pass in priors would be independent evidence that the heavier stars SPARC asked for are allowed in the one galaxy with star-count masses; a fail adds a second fail to that footing. Reported with the best in-prior cell's M*, so the stellar mass the Milky Way asks for can be set beside SPARC's f.

Any pass gets the stress a fail gets: Q5 convergence on the best in-prior cell (doubled grid, |dK| > 1 tags [GRID-DEPENDENT]), strict count, where in the box it sits.

## Checks
- C1: the law's nu through this lane's code reproduces UX5's stored form Q v_c and K(R0) on all 175 B175 cells per footing, max relative 1e-6.
- C2: inversion x mu(x) = y to 1e-12 relative on y from 1e-6 to 10.
- C3: Plummer, form Q with the compact nu against nu(g_N) g_N, 1-30 scale radii, at most 1 percent (UX5's Q1 geometry).
- C4: Kuzmin thin sheet, K at z 1.1, R 4-12, at most 2 percent (UX5's Q2).
- MUTATE: nu = 1 must return Newton and leave the class unchanged only if Newton's own class is the same; it is reported and the lane exits 1 by design. Outputs `_MUTATE`.

Comparison row, no label: KT11's mu_2, mu = 1 - (1 + x/2)^(-2), on B175, so the compact kernel sits beside the record's own kernel. Register row after the result. Single thread, under 1 GB, minutes.
