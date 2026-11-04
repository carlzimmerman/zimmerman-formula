# KT29_tidal_rule_mw_full_tensor — FROZEN CRITERIA (before any script; only the rough hand estimate below)

Owner, 2026-11-03: KT28's tidal rule survives all four tests on alt, but its Milky Way arm used the in-plane spherical form
from the rotation curve and left out the vertical tidal component. Redo the MW with the full tidal tensor, both footings.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download. This is a stress test of KT28's win, graded as hard as a fail.

## The rule, unchanged from KT28, now with the 3D tensor
ξ_tid = (4/√3) τ³ / (|∇τ|² g*), g* = a0/κ, τ = Frobenius norm of T = ∇∇Φ. This is KT28's rule exactly: for a spherical field
the 3D Frobenius norm is sqrt(g'² + 2(g/r)²) and |∇τ| = |dτ/dr|, so the 4/√3 calibration carries over unchanged.

## Evaluation, per in-prior cell, at the midplane at R0 (where v_c is measured)
In axisymmetry at z = 0, T is diagonal: T_RR = d(V²/R)/dR, T_φφ = V²/R², T_zz = ∇²Φ - T_RR - T_φφ.
- V(R) is the cell's own **unfiltered plain-QUMOND** circular speed (`vc_plane` on LU.qumond(Φ_N)).
- ∇²Φ = ν(|g_N|/a0) 4πG ρ_b(R, 0): QUMOND's source, with |g_N| = V_N²/R from `vc_plane` on Φ_N and ρ_b from `rho_struct`.
  The g_N·∇ν term is dropped (stated; it's the radial gradient of ν, small next to the disc density term).
- ∂_z τ = 0 at the midplane by symmetry, so |∇τ| = |∂_R τ|, by central difference at R0 ± 0.25 kpc.
- One ξ per cell (the cell's own structure sets it), quantised as KT17 does (log step 0.005), clipped at 200 kpc.
Then the cell is solved with the filter at that ξ (KT26/KT28's MW code), and lines L1, L2a, L2b, L3 are graded unchanged.

**Label per footing: FULL-TENSOR TIDAL RULE PASSES MW** if at least one in-prior cell passes all four;
**FAILS MW** otherwise. If alt FAILS here, KT28's alt survival is recorded as **dependent on dropping the vertical term**.

## Expectation on record, not blind
Rough hand estimate: at R0, T_zz ≈ ν 4πGρ_b with ρ_b about 0.09 Msun/pc³ is about 7x the in-plane components, and it falls
radially roughly as e^(-R/R_d), so ξ_tid ≈ (4/√3) τ R_d² / g*, i.e. about 15-25 kpc. KT17's ε = 1 (about 10-11 kpc) already failed
the MW's v_c. So **I expect FAILS MW on both footings.**

## Beside, not graded
- ξ_tid per cell (range, median); the in-plane-only value (KT28's form) on the cell's own V(R) for comparison.
- ξ_tid at (R0, z = 1.1 kpc), where K_z is measured: there ∂_z τ isn't zero, and the value shows how position-dependent the
  rule is inside a disc.

## Checks
- C1 (KT17's): plain solves reproduce UX5's Q lines, 1e-6.
- T1: the in-plane-only value on the observed-curve inputs reproduces KT28's ξ_tid(R0) (8.78 / 7.26 kpc) to 0.01 kpc.
- T2: ∇²Φ from the formula vs the solver's discrete Laplacian of the plain-QUMOND Φ at (R0, 0), printed (not graded; the grid
  is coarse in z).
- KT17's C3 half-space factor is a known failure, disclosed if it recurs. MUTATE: KT17's own path, not rerun.
