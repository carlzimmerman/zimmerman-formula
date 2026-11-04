# KT31_tidal_rule_rz_solve — FROZEN CRITERIA (before any script; only the hand reasoning below)

Owner, 2026-11-04: after KT29 (full-norm tidal rule) and KT30 (trace-free) failed the Milky Way with one ξ per cell at the
midplane, freeze the test KT29 said was still missing: **a Milky Way solve where ξ varies with (R, z)**, set at every solver
cell by that cell's own tidal field.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download. Post hoc: same two rules as KT28 and KT30, now with a position-dependent width; the register counts it as one more
attempt on each rule. Cassini, dwarfs and SPARC are already position-dependent (row-wise in r) in KT28/KT30 and aren't rerun;
their results carry over.

## Rules (both graded, each labelled on its own; no "either passes")
- **F** (KT28): τ = Frobenius norm of T = ∇∇Φ, ξ = (4/√3) τ³ / (|∇τ|² g*).
- **TF** (KT30): τ = Frobenius norm of T − (tr T/3) I, ξ = √6 τ³ / (|∇τ|² g*).
g* = a0/κ; clipped at 200 kpc. Φ is the cell's own **plain-QUMOND** potential (the MW is isolated; no external field).

## Building ξ(r, θ) on the solver grid (KT14's spherical (r, θ) half-space grid, 9456 cells)
In spherical coordinates, with Φ on the cell centres (mirror-even across the plane θ = π/2, mirror at the axis):
T_rr = ∂²Φ/∂r², T_θθ = (1/r²) ∂²Φ/∂θ² + (1/r) ∂Φ/∂r, T_rθ = ∂_r((1/r) ∂_θ Φ), T_φφ = (1/r) ∂Φ/∂r + (cot θ / r²) ∂_θ Φ;
|T|² = T_rr² + T_θθ² + 2 T_rθ² + T_φφ², tr T = T_rr + T_θθ + T_φφ. Then |∇τ|² = (∂_r τ)² + ((1/r) ∂_θ τ)².
Derivatives by `np.gradient` on the non-uniform centres. No smoothing of τ in the graded run.

## Position-dependent smoothing (gather form, as KT27/KT28's row-wise smoothing)
ρ_s(x) = ρ smoothed with a 3D Gaussian of width ξ(x), evaluated at x. Built by a width ladder: ξ_k = 0 and 0.005 × 1.5^k kpc
up to ≥ 200 kpc. ρ at each ladder width uses KT29's exact `rho_xi` (cell averages via `rho_axisym`). Each cell blends its two
neighbouring ladder widths linearly in ln ξ, or linearly in ξ between 0 and 0.005 kpc. Then the phantom source is KT29's:
Φ = Φ_N + QUMOND(Φ_N[ρ_s]) − Φ_N[ρ_s]. Lines L1, L2a, L2b, L3 are graded unchanged on all in-prior cells.

Gather form doesn't conserve mass. C2 prints the ratio of smoothed to true mass per cell, and the label carries it (below).

## Labels, per footing, per rule
- **PASSES MW** if ≥ 1 in-prior cell passes L1, L2a, L2b and L3. If every passing cell has a mass deficit > 10 %:
  **PASSES MW, MASS-CONDITIONAL**.
- **FAILS MW** otherwise.
- **NOT EVALUABLE (numerics)** if check N1 fails.
- **NUMERICS-DEPENDENT** if R5 changes the label.
A rule survives all four tests on a footing only if it passes MW here **and** already passed Cassini, dwarfs and SPARC on
that footing (KT28 / KT30). On alt both rules did; on canonical neither did.

## Expectation on record, not blind
Inside the disc the rule gives ~33-53 kpc at the midplane (KT29/KT30) but ~0.003-0.04 kpc at z ≈ 1 kpc. With gather
smoothing, the midplane layers lose most of their density from the phantom source, while the gas and thin disc just off the
plane keep theirs almost untouched. Which wins for v_c at R0 isn't clear by hand. A large mass deficit is likely (the thin
disc's mass sits where ξ is large), which would cut the phantom. **Lean: FAILS MW on both footings, both rules; low
confidence.**

## Checks (tolerances set here)
- **N1 (Hessian):** at the grid cell nearest (R0, 0), the grid-built ξ_F reproduces KT29's per-cell full-tensor ξ, median
  ratio over cells in [0.8, 1.25]. It's a different method (KT29 used vc_plane and ν 4πGρ_b). Failure means NOT EVALUABLE.
- **R1:** with ξ set to 0 everywhere, the solves reproduce UX5's form-Q lines (1e-6, KT17's C1).
- **R4 (ladder blend):** on the lightest and heaviest in-prior cells, a constant field ξ = 0.005 × 1.5^(k+½) for k at 1 kpc and
  10 kpc, blended from the ladder, vs direct `rho_xi` at that ξ: |Δv_c| ≤ 0.5 km/s and |ΔK(R0)| ≤ 0.5.
- **R5 (τ noise):** rerun the passing (or best-D) cells with ln τ smoothed by a 1-cell Gaussian in both grid indices; print
  the change in ξ at (R0, 0) and in v_c, K; NUMERICS-DEPENDENT if the label changes.
- **C2:** mass ratio printed for all cells (min/median/max).
- **MUTATE (ν = 1):** must give Q = N (no phantom) on two cells.
- KT17's C3 half-space factor is a known failure; disclosed if it recurs.

## Beside, not graded
ξ(R, z) maps for the best-D cell (both rules, both footings), as a table at R = 4, 8, 12, 20 kpc and z = 0, 0.1, 0.3, 1, 3 kpc.

## Compute
Single thread, nice 15, ≤ 1 GB. Width loop outermost; accumulators are checkpointed to disk after each width (SIGTERM-safe,
resume skips done widths). Expect ~1 hour.
