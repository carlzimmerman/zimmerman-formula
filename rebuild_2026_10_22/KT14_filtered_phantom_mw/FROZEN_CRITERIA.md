# KT14_filtered_phantom_mw: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep pushing, the answer must lie somewhere". KT13: every local QUMOND kernel that reaches the Milky Way's v_c lands at K(R0) 75-76 against 70.8, because the phantom in the plane is about (nu - 1) rho_b, so the extra pull comes as a disc. This lane tests the one field-equation change that KT13 names: **the phantom is sourced by a smoothed copy of the mass**, so the extra pull comes out rounder than the disc. κ = 1/2 FITTED and held fixed. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. No cold component, no particle. No download.

**Not blind.** KT13's numbers are known. The record's chassis already has a heat filter (STANDING, L340), with xi >= 0.03 pc set by Cassini; nothing in the record fixes xi at kpc. **Any xi that passes here is post hoc and a new number**, labelled so.

## Field equation (filtered QUMOND)
lap Phi_N = 4 pi G rho; rho_xi = G_xi * rho (3D Gaussian, sigma = xi, mass conserved); lap Phi_N,xi = 4 pi G rho_xi;
lap Phi = 4 pi G rho + div[ (nu(|grad Phi_N,xi| / a0) - 1) grad Phi_N,xi ].
So Phi = Phi_N[rho] + (QUMOND[rho_xi] - Phi_N[rho_xi]). xi -> 0 is plain QUMOND. It follows from the QUMOND action with the auxiliary potential coupled to the smoothed density. Kernel: the board law's simple nu, no other.

Hand estimate before running: if the phantom column spreads over about xi, the share inside |z| < 1.1 kpc falls roughly like erf(1.1 / (sqrt 2 xi)). Removing about 5 of the phantom's roughly 24 units of K needs that share under about 0.8, so xi of about 0.9 kpc or more. v_c should barely move. **Expectation: passes appear at xi 1-2 kpc, likely failing the K_z scale length or Ou somewhere.** Reported as found.

## Frozen list and cells
xi in {0, 0.25, 0.5, 1, 2} kpc. xi = 0 must reproduce KT13's simple-kernel rows. Cells: KT13's 1375 in-prior cells per footing (B175, BV, BV2 within LN16's R_d tag and M* tag), UX5's form Q grid and LU, gas and bulge shapes as UX5's `rho_struct`. Smoothing is done component by component: discs and gas are separable (radial 2D Gaussian via the I0 kernel, vertical 1D Gaussian); the bulge on a 2D (R, z) grid.

## Gate, unchanged
UX5's L1 v_c, L2a chi2_Kz <= 67.459, L2b |K(R0) - 66.4| <= 4.4, L3 Ou chi2 <= 59.89; strict h line |h - 2.72| <= 0.30 reported beside. Nothing moves.

## Labels, per footing
- **FILTER PASSES MW at xi = X:** an in-prior cell passes all four lines at that xi; the smallest such xi is named. Stressed like a fail: doubled grid on the best passing cell, |dK| > 1 tags [GRID-DEPENDENT]; strict h count stated. **It's a lead, not a pass of the theory.** It is owed, before any claim: dwarf spheroidals (r_half below xi lose their own boost), SPARC (inner points of small discs), wide binaries (a binary's own phantom is smoothed away, so the prediction is Newtonian internal motion plus the external field), lensing and Cassini. These predictions are written here so they can't be chosen later.
- **NO XI PASSES:** none in the list does. The line that fails at the best cell is named.

## Checks
C1: xi = 0 reproduces KT13's simple rows on all in-prior cells, max relative 1e-6. C2: mass of rho_xi on the solver grid equals rho's within 1e-3 for every xi on McMillan-like and the shortest-disc cell. C3: the radial smoothing of a 2D Gaussian of width w returns width sqrt(w^2 + xi^2) to 1e-3; the vertical one likewise. MUTATE: replace rho_xi by rho_xi scaled by 0 in the phantom (phantom off): must return Newton and fail L1 everywhere; separate `_MUTATE` output, exit 1.

Register row after the result. Single thread, under 1 GB, about 15-25 minutes at nice 15. A large multi-process job is live on this machine, so this stays small.
