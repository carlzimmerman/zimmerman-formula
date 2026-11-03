# KT17_mond_radius_filter: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep pushing". KT16: a filter scale xi = eps sqrt(G M / a0) passes Cassini for eps >= 0.45 (canonical) / 0.50 (alt). **eps = 1, the phantom's source smoothed over the system's own MOND radius, has no fitted number.** This lane tests it on the Milky Way and the dwarfs, both footings. κ = 1/2 FITTED and held fixed. Never pooled. Not theory closed. No cold component, no particle. No download.

**Not blind.** KT14 (MW at xi 0-2 kpc), KT15 (dwarfs), KT16 (Cassini) are known. eps = 1 gives xi about 9-10 kpc for the Milky Way, beyond KT14's range, so the MW result isn't known. I don't know which way it goes: larger xi lowers K_z further, but smears the phantom inside R0 and may cut v_c. Dwarfs: xi 0.02-0.5 kpc, expected near plain QUMOND, mildly lower.

## Field equation
KT14's filtered QUMOND, simple nu: Phi = Phi_N[rho] + QUMOND[rho_xi] - Phi_N[rho_xi], rho_xi = 3D Gaussian of rho with sigma xi, **xi = eps sqrt(G M_b / a0)**, M_b the system's total baryonic mass (MW cell: its M* plus the held gas mass, integrated from UX5's gas profiles; dwarf: Upsilon L + 1.33 M_HI; Sun: 1 solar mass). The definition of "the system" is not a local field, stated as an open problem.

## Arms
- **E1: eps = 1** (primary, nothing fitted).
- **E2: eps = 0.55** (the smallest round value above both Cassini thresholds; set by KT16, not by any galaxy).

## Tests, gates unchanged from their lanes
1. **Milky Way:** KT13/KT14's 1375 in-prior cells per footing, UX5's form Q and lines L1, L2a, L2b, L3; strict h reported beside. xi per cell quantised to 0.5 percent in log for caching (stated). Pass = an in-prior cell passing all four; doubled-grid Q5 on the best passing cell.
2. **Dwarfs:** KT15's 24 rows, model, external-field case and gate. Label against plain QUMOND on the same footing: KILLED (at most half), SURVIVES (at least plain minus 2), HURT between.
3. **Cassini:** KT16's integral at xi/r_M = eps, both footings, ceiling 5.2e-27.

## Labels, per arm and footing
- **PASSES ALL THREE:** MW in priors, dwarfs SURVIVES (external-field case), Cassini PASS. **A lead, owed SPARC, wide binaries, lensing, clusters before any claim.**
- Otherwise each test's label, with the failing one named.

## Checks
C1: at eps -> 0 (xi = 0) the MW code reproduces UX5's form Q on all in-prior cells, 1e-6. C2: smoothed mass within 2e-3 of the original on the solver grid at the largest xi used (the larger xi spreads mass to the grid edges; the tolerance is wider than KT14's 1e-3 for that reason, stated before running). C3: M_gas integral reported against a direct sum on the solver grid, 1e-2. MUTATE: phantom off returns Newton, fails L1 everywhere; separate output, exit 1.

Register row after the result. Single thread, nice 15; RSS may exceed 1 GB as KT14's did (1.8 GB); reported. About 30 minutes.
