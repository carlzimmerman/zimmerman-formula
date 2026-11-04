# KT32_tidal_rule_rz_scatter — FROZEN CRITERIA (before any script; only the hand reasoning below)

Owner, 2026-11-04: after KT31 (ξ varying in (R, z), gather smoothing: 0 MW cells pass, K_z 77-80, but gather added 12-44 %
mass and the ladder was coarse), freeze the mass-conserving **scatter** form with a finer ladder.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download. Post hoc: same two rules (F = KT28's Frobenius norm, 4/√3; TF = KT30's trace-free norm, √6), same ξ field as KT31
(each solver cell's own plain-QUMOND tidal tensor, KT31's `tidal_xi`), clipped at 200 kpc. Only the smoothing changes.
Cassini, dwarfs and SPARC carry over from KT28 / KT30.

## Scatter smoothing
ρ_s(x) = ∫ K_{ξ(x')}(x − x') ρ(x') d³x': each source spreads its own mass over a 3D Gaussian of the width set **at the source**.
That conserves mass (up to the mesh edge). Built by ladder: ξ_k = 0 and 0.005 × 1.25^k kpc up to ≥ 200 kpc. Each source's
mass is split between its two neighbouring widths, linearly in ln ξ (linearly in ξ below 0.005 kpc), so
ρ_s = Σ_k S_k[a_k ρ]. Here S_k is a fixed-width Gaussian smoothing of an arbitrary axisymmetric field.

S_k acts on a cylindrical (R, z) mesh, separably: the exact 3D Gaussian in axisymmetry is an I0 kernel in R times a Gaussian
in z (KT29's `radial_matrix` and `gauss` forms). The mesh is non-uniform: fine near the plane and the centre, geometric
outward, reaching ≥ 150 kpc in R and ±80 kpc in z. Kernel columns are normalised so each source ring's mass is kept exactly.
Widths below 1.5× the local mesh spacing are taken as identity. The mesh field comes from the solver cells by
interpolation, and goes back by `rho_axisym` of the mesh interpolant. Phantom source as KT29/KT31:
Φ = Φ_N + QUMOND(Φ_N[ρ_s]) − Φ_N[ρ_s]. Lines L1, L2a, L2b, L3 are graded unchanged on all 1375 in-prior cells.

## Labels, per footing, per rule
- **PASSES MW** if ≥ 1 in-prior cell passes L1, L2a, L2b and L3; **FAILS MW** otherwise.
- **NOT EVALUABLE (numerics)** if S1, S2, S3 or N2 fails.
- **NUMERICS-DEPENDENT** if R5 changes the label.
A rule survives all four tests on a footing only with PASSES MW here and its earlier Cassini, dwarf and SPARC passes; alt
had those for both rules, canonical for neither.

## Expectation on record, not blind
Scatter puts each source's mass at the source's ξ. Disc sources sit where ξ is 0.005-3 kpc (KT31's map), so the phantom
source stays a disc. Removing KT31's off-plane mass excess should bring K_z down a little. I don't expect it to fall from
77-80 to ≤ 70.8: KT13's local kernels missed the same way (75-76) with no mass error. **Lean: FAILS MW on both footings, both
rules; K_z still the failing line.**

## Checks (tolerances set here)
- **S1 (mass):** Σ ρ_s vol / Σ ρ vol − 1 within ±1e-2 on every cell (the scatter form must conserve; mesh-edge loss only).
- **S2 (smoother vs exact):** a constant ξ field through S_k (no ladder blend) vs KT29's exact `rho_xi` at ξ 1 and 9 kpc, on
  the lightest and heaviest cells: |Δv_c| ≤ 0.5 km/s, |ΔK(R0)| ≤ 0.5.
- **S3 (ladder):** a constant ξ at the geometric midpoint of two ladder widths near 1 and 9 kpc, blended vs exact: same lines.
- **N2 (Hessian; replaces KT31's N1, which had a wrong premise):** grid τ_F at the cell nearest (R0, 0) vs KT29's τ: median
  ratio in [0.9, 1.1]. (KT31 measured 1.02 as a beside; this is chosen after KT31 and stated so.)
- **R1:** ξ 0 reproduces UX5's form Q (1e-6). **MUTATE (ν = 1):** Q = N on two cells (1e-6).
- **R5 (τ noise):** ln τ smoothed by one cell in both indices, rerun on up to 2 passing (or the best-D) cells; label change
  means NUMERICS-DEPENDENT.

## Beside, not graded
- KT31's gather result next to this one for the same best-D cell (v_c, K).
- K_z vs mass split: K(R0) with the phantom alone versus plain QUMOND for the best cell.

## Compute
Single thread, nice 15, ≤ 1 GB. Ladder loop outermost, checkpointed after each width (SIGTERM-safe); checkpoints deleted after
the run. Expect about an hour.
