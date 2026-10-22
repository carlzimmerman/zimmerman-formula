# C6_literal_cassini — FROZEN CRITERIA (written and committed before any script or number)

## Question

C5 found that the only healthy covariant parent is the **C4-literal Khronon + P** theory: β = 0, η = 0, BS K(Q) dust,
longitudinal stiffness γ_L = K L★²/2 > 0 and **no curl stiffness (γ_F = 0)**. D7d's Cassini pass used γ_F = γ_L
(vector Laplacian). Does the healthy literal form (γ_F = 0) still pass the Solar-System tests?

## The theory tested (FRAMEWORK-NATIVE, no new posit)

Static, weak field, O(ε), f = 1, p = K P, Φ = ln N, C4-literal static Lagrangian (A33 at η = 0 with γ_F = 0):

    L = −|∇Φ|²/2K + P·∇Φ − W(K|P|) − (γ_L/2)(∇·P)² − ρΦ,   W = (a₀²/K)[−u/a₀ − ln(1 − u/a₀)],  γ_L = K L★²/2.

Expected Euler–Lagrange equations (to be confirmed by sympy in C1, not assumed):
(L) ∇²Φ = Kρ + ∇·p;  (P_L) ∇Φ + (L★²/2)∇(∇·p) = a₀p/(a₀ − |p|).
D7d's (P) had (L★²/2)∇²p (γ_F = γ_L). The only change is ∇² → ∇∇· (grad-div).

## Methods

- **Route F** (linear Fourier response about the Galactic background, exact to O(GM/L★²/u_e)): D7d's formula with
  A = (κ²/2)[r_F(I − k̂k̂) + k̂k̂] + J − k̂k̂, r_F = γ_F/γ_L; r_F = 1 is D7d, r_F = 0 is this lane.
  Q₂ = −(2GM/5πL★³) I₂ (BN11/Hees sign, as D7d), I₂ = ∫κ²χ₂dκ with the analytic large-κ tail of the r_F = 0 kernel.
- **Route N** (nonlinear axisymmetric grid): D7d's (ln r, θ) machinery imported read-only (`d7d_solver.py`: Grid, dP,
  q2_raw, regrid), with this lane's own build in which the stiffness is r_F·(vector Laplacian) + (1 − r_F)·(grad-div),
  grad-div written as the discrete gradient of the discrete divergence. Memory < 1 GB RSS, single thread, nice.
- Inputs read-only from the record: GM, a₀ footings, E0–E3 fields (D7b json), Hees 2014 (3 ± 3)e-27 s⁻²,
  Park 2026 (1.6 ± 1.8)e-27 s⁻² (`prep_2026/planetary_doors/BOUNDS.md`), planet bounds (Earth 8.7e-15, Mars 1.4e-15,
  Saturn 7.0e-15 m/s²), BN11 μ₁ 3.8e-26, E2 AQUAL canonical E0–E3, D7d json for comparison.

## Checks (script prints `Cn PASS/FAIL value threshold`; exit 0 iff all pass)

- **C1** sympy: the Euler–Lagrange equations of L above are (L) and (P_L); (P_L) makes h(p) an exact gradient
  ∇χ, χ = Φ + (L★²/2)∇·p; and the linear kernel with r_F = 0 equals m/(1 − m + κ²m/2), m = k̂·J⁻¹·k̂. All residuals 0.
- **C2** Route F validation: r_F = 1 reproduces D7d's `chi` to < 1e-12 (max abs over a κ, c grid); at κ = 0 the
  r_F = 0 kernel equals linear AQUAL, 1 + χ = 1/(μ(1 + L₀c²)), to < 1e-12; at x_e = 0 (isolated) r_F = 0 equals r_F = 1
  to < 1e-12 (the monopole/hedgehog is curl-free, so γ_F cannot matter there).
- **C3** Route N validation against D7d: this lane's build at r_F = 1 equals D7d's `build` matrix exactly
  (max |ΔA| = 0, same rhs) at Λ = 30.
- **C4** AQUAL anchor (L★ = 0, Route N, Richardson over two grids): BN11 μ₁ point within 10 % of 3.8e-26, and
  E2 canonical E0–E3 AQUAL values (2.200 / 3.127 / 3.557 / 4.097e-26) each within 3 %.
- **C5** Route N (r_F = 0) vs Route F (r_F = 0) at Λ = L★/r_M = 30 and 100, canonical E0 and E3: max |N/F − 1| < 5e-2,
  same sign.
- **C6** small-L★ continuity: Route N r_F = 0 at Λ = 0.01 vs Λ = 0 (E2 canonical): |ratio − 1| < 2e-2.
- **C7** Route F numerics: quadrature refinement changes I₂ by < 1e-6 (relative); the analytic tail coefficient
  matches the kernel at κ = 1e3 to < 1e-4 relative.
- **C8** linear validity at 24 pc (both footings, all E): max (GM/L★²)(1 + x_e)²/(a₀x_e) < 1e-4
  (the r_F = 0 hedgehog in v-space is bounded by (GM/L★²)/m ≤ (GM/L★²)(1 + x_e)²).

`--mutate`: Route N's grad-div drops the 2q_r/r term of the divergence. It must break at least one of C4/C5/C6.
Outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## Results (verdict lines)

- **R1** Cassini Q₂ (Route F, r_F = 0) at L★ = 24, 50, 90 pc, both footings, E0–E3 (24 cells), against the two-sided
  2σ bands Hees [−3.0e-27, 9.0e-27] and Park [−2.0e-27, 5.2e-27]. Also the ratio to D7d (r_F = 1).
- **R2** inner-planet anomalous radial acceleration (Earth, Mars, Saturn; Route F monopole) vs the bounds above.
- **R3** wide binary 1.5 M☉ at 20 kAU: γ_v − 1 (Route F monopole in the field), both footings, E0–E3.
- **R4** mechanism: leading large-κ anisotropy of the potential kernel (P₂ coefficient of the 1/κ⁴ term) for r_F = 0
  vs r_F = 1; transverse/longitudinal size of δp near the Sun.
- **R5** (reported, not a verdict line) Route N scan for the Cassini lower bound L★_C at r_F = 0 on one coarse grid.

## Verdict

- **PASSES** iff C1–C8 all PASS and every R1 cell lies inside both 2σ bands and every R2 ratio < 1 at all three L★.
  The margin reported is min over cells of 9.0e-27/|Q₂| (Hees) and 5.2e-27/|Q₂| (Park).
- **FAILS** iff C1–C8 all PASS and any R1 cell or R2 ratio is outside: name the test, cell and factor.
- **UNDECIDED** iff any of C2–C6 fails (the solve is not validated): say which and why.

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework.
