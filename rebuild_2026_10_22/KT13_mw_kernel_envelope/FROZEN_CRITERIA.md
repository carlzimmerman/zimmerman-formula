# KT13_mw_kernel_envelope: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep working", "we gotta figure it out". KT12 left the Milky Way between two shapes: mu_2 reaches v_c but over-forces K_z; the compact kernel gets K_z but not v_c. Question: does ANY standard QUMOND kernel pass the Milky Way on star-count baryons, or is the miss set by the baryons whatever the kernel? κ = 1/2 FITTED and held fixed; a0 is each footing's, canonical 9.3603e-11 and alt 1.1312e-10, never pooled. Not theory closed. No cold component, no particle. No download.

**Not blind.** I've read KT12's and UX5's outputs. Hand argument, stated before running: in QUMOND, phantom density in the disc plane is about (nu - 1) rho_b, so a local kernel lifts K(R0) and v_c(R0)^2 by about the same factor nu(R0). Then K at the v_c line is roughly K_N (229 / v_N)^2. The in-prior best cells give 64.1 (200/229 lift) to 55 (175), so about 84-94 against a line top of 70.8. Gradient terms (g_N . grad nu) can change this, which is what the full solve tests. **Expectation: NO KERNEL IN FAMILY on both footings.** Any other result is reported as found.

## Kernels, frozen list, as nu(y), y = g_N / a0
1. simple (the board law, UX5's): nu = 1/2 + sqrt(1/4 + 1/y)
2. nu_2, 3. nu_3, 4. nu_6: nu_n = [ (1 + sqrt(1 + 4 y^-n)) / 2 ]^(1/n) (Milgrom's mu_n = x / (1 + x^n)^(1/n); n = 1 is the simple)
5. sharp: nu = max(1, y^(-1/2))
6. RAR: nu = 1 / (1 - exp(-sqrt(y)))
7. OR mu_2 (KT11's): mu = 1 - (1 + x/2)^(-2), inverted numerically
8. compact (KT12's): mu = x - x^2/4 for x <= 2, 1 above
All share the deep limit nu -> y^(-1/2), so a0 is the same; they differ only in the transition. No member is added after the result.

## Solve and gate
UX5's form Q, grid, LU and lines, unchanged: L1 v_c, L2a chi2_Kz <= 67.459, L2b |K(R0) - 66.4| <= 4.4, L3 Ou chi2 <= 59.89. **Cells: the in-prior cells of B175, BV and BV2 only** (R_d tag 2.38-2.90, M* tag 3.80-8.36e10), 25 + 675 + 675 = 1375 per footing, from UX5's boxes. Wide-prior cells are not run. Per kernel and footing: count passing all four, and each line; best cell by UX5's D; lowest K(R0) among cells passing L1; and the diagnostic K_proj = K(R0) (229.1 / v_c)^2 at the in-prior best cell.

## Labels, per footing
- **KERNEL FOUND:** any listed kernel has an in-prior cell passing all four lines. That kernel is then owed SPARC, Cassini and the rest; it's a lead, not a pass. Stressed like a fail: doubled grid on that cell, |dK| > 1 tags [GRID-DEPENDENT].
- **NO KERNEL IN FAMILY:** none does. Then, reading, not label: if every kernel's lowest K(R0) with v_c in line is above 70.8, the miss is set by the baryons for this family, and the Milky Way needs either K_z's measurement or the star-count disc to move. Scope: eight kernels, local QUMOND only. It isn't a theorem for all kernels or for non-local or AQUAL forms (UX5: A and Q within 0.13 percent for the simple kernel).

## Checks
C1: simple nu reproduces UX5's stored form Q on these cells, max relative 1e-6. C2: compact reproduces KT12's in-prior best cell per box, 1e-6. C3: each kernel's nu satisfies y = x mu(x) for its mu, 1e-8, y from 1e-4 to 100 (RAR and nu_n via their closed mu where one exists, else by the stated nu). MUTATE: nu = 1 (Newton) must fail L1 in every in-prior cell; separate `_MUTATE` output, exit 1.

Register row after the result. Single thread, under 1 GB, about 15 minutes, nice 15.
