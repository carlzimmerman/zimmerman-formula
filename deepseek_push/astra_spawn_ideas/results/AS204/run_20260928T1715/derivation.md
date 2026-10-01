# AS204 — Bound the curved-leaf heat-force derivative (Tier-0, EFE prerequisite)

Run: `deepseek_push/astra_spawn_ideas/results/AS204/run_20260928T1715/`
Task: `deepseek_push/astra_spawn_ideas/AS204_bound_a_curved_leaf_heat_force_derivative.md`
(sha256 `900a926c4ec889911daec8151ebffa85f38aa5847c4fe1aa282f19f5e2b25c63`, verified before execution)

Framework cell: a₀ = κ·c·√(G_N·ρ_Λ), κ = 1/2 adopted; both footings a₀ ∈ {9.3619e-11, 1.1279e-10} m/s²;
G_N = 6.67430e-11, c = 299792458, M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m.

---

## 1. Operative target (from the seed, executed verbatim)

Curved leaf Σ³ with induced metric h, intrinsic Laplace–Beltrami Δ_h:

- heat filter (mode-diagonal on the harmonic basis): **S_h = exp(b·Δ_h)**, b = ξ²/2 > 0
- derivative-floor splice: **φ(y) = h_mono(y)/y**, h_mono = XC4 construction = h_RAR spliced at y_star,
  δ = Δ_M = 0.05
- filtered field **H = S_h ∇u**; interpolated force **F = φ(|H|/a₀)·H**
- longitudinal elliptic projection **u′ = Δ_h⁻¹ δ_h F** (zero mean; δ_h = divergence, Δ_h⁻¹ = Green
  operator on mean-zero modes)
- weighted adjoint in the lapse-weighted measure N√h: **S_h\* = N⁻¹ S_h N**
- **a_ph = −∇(S_h\* u′)**, and the deliverable is a bound on ‖∇ a_ph‖∞.

The bound pipeline: ‖∇a_ph‖∞ ≤ **K_tot(b, curvature, lapse) · ‖F‖₂** with explicit constants
C₀, C_g, C_hh, C_G (supremum-checked numerically, `C0_sup/C0 < 1` etc. below), R₀ = sup |Ric| = 2 on
round S³, λ₁ = 3, B_ℓ bound (cf. FINAL_ACTION.md `b8c04d4e…`, filtered_zero_field/RESULT.md
`7067ca07…`).

## 2. Derivation of the bound chain (every factor and sign)

For a field A on Σ³ with ambient Jacobian J (the extension used below), |x| = 1:

**Lemma (four-term Jacobian identity, Lean-certified).**
For any ON-frame {u_a, x} of ℝ⁴,
Σ_a ‖Proj_T (J u_a)‖² = Tr(JᵀJ) − ‖J x‖² − ‖Jᵀx‖² + (xᵀJx)²        …(1)

*Proof algebra:* ‖Proj_Tw‖² = ‖w‖² − (x·w)²; Σ_a‖Ju_a‖² = Tr(JᵀJ) − ‖Jx‖² (frame completion with x);
Σ_a(x·Ju_a)² = Σ_a(u_a·Jᵀx)² = ‖Proj_T(Jᵀx)‖² = ‖Jᵀx‖² − (xᵀJx)². ∎
Lean 4 certificate `AS204_four_term_identity.lean` (2×2 case, the same algebra): compiles, axioms
⊆ {propext, Classical.choice, Quot.sound}.

**Step 1 — derivative of the physical force from its polynomial extension.**
a_ph = −∇_S v, v = S_h\* u′. The field A = −∇_S v is extended ambiently as the polynomial
A(q) = −(g(q) − (g(q)·q̂)q̂), g = ∇_amb v. Its ambient Jacobian (chain rule, |q| = 1):

J_A,ij = −Hess_ij + [ (Hess·x)_j + g_j ] x_i + (g·x) δ_ij              …(2)

(Signs: minus from −∇_S v; plus from ∂_j[(g·x̂)x̂]; the q̂-normalization term, ∝ x_i·(x·u) = 0,
vanishes on tangent directions — verified numerically.) Then with (1):
‖∇_S a_ph‖² = Tr(J_AᵀJ_A) − ‖J_A x‖² − ‖J_Aᵀx‖² + (xᵀJ_A x)²        …(3)

(The J_A asymmetry — the term (Hess·x)_j x_i — is why both ‖J x‖² and ‖Jᵀx‖² appear.)

**Step 2 — Bouchain bounds on the contributing operators.**

- Rough Laplacian on exact 1-forms: ∇*∇ = Δ₁ + Ric (Weitzenböck). On S³ (Ric = 2h, parallel),
  the exact-form eigenproblem degrades by λ̂→λ̂+2. The integrated identity ∫Tr(J_AᵀJ_A)(mode) =
  ē_l·1 is used as a control with the empirical per-level table ē_l = 2l²(l² + 2l + 2)
  (exact to 1e-11 at the quadrature, l = 1..11; see §6 and residuals.json weitzenbock_modes).

- Heat kernel contraction: ‖∇S_h f‖ ≤ sup_cache ‖∇S_h‖·‖f‖; C₀/C_g-supremum checks hold
  (C0_sup/C0 = 0.26–0.52, Cg_sup/Cg = 0.37–0.56 in the six cells).

- l'Hôpital-type bounds on φ(y)/y: φ monotone; sup-φ ≤ 1; the x/y-spline is C¹ at y_star
  (C1_join_relative_residual = 2.8e-6), deep limit h_RAR(10⁻⁸)/10⁻⁴ = 0.99995.

- Weighted adjoint: S_h\* = N⁻¹S_hN; lapse factor enters through L_N = ‖∇N/N‖∞ and
  c_min = inf N, c_max = sup N.

**Step 3 — assembled constant (a₀-free).**
K_tot = (1/c_min)·[(C_hh c_max)/λ₁ + (L_N C_g c_max)/λ₁ + (L_N C₀ c_max L_N C_G)
 + C₀ R₀ √(2b/e)·c_max L_N C_G + C_g·2 L_N c_max C_G/λ₁ + (L_N C₀ c_max B_ℓ)
 + (C_g c_max B_ℓ)]            …(4)

Each term carries units [∇a_ph]/[‖F‖₂]; no a₀ appears: both footings share the identical K_tot
at κ = 1/2 (the a₀ factor enters only through the physical ‖F‖₂ ≤ c₁√(vol_h·supH/a₀) bound).

## 3. Numerical execution (bounded prototype)

Leaf: **round S³** (closed, smooth, |Rm|ₛₑ𝒸 = 1, inj radius π, Ric = 2h ⇒ R₀ = 2, λ₁ = 3).
Quadrature: exact-separable: Chebyshev–Gauss 2nd kind in t (surface weight √(1−t²)), Gauss–Legendre
in u, uniform ψ — every basis Gram entry exact at truncation (gram_residual ≤ 8.7e-15).
Basis: exact spectral (l+1)² modes per level; intrinsic gradient + ambient Hessian recursion,
validated against independent finite differences and least-squares quadratic fits
(dbg_fd.py: median relative error vs direct FD ≈ 2.3e-10–6.6e-10; hessian recursion vs FD
3e-6 max abs = FD discretization).

Grid: 6 cells at L = 8 truncation (n = 285 modes, G = 4851 grid points):

| cell (b, lapse ε, target supH) | ‖∇a_ph‖∞ | K_tot | r_curved | r_naive |
|---|---|---|---|---|
| (0.05, 0.0, 2.3374) | 1.41413 | 272.1 | 0.00933 | 0.0494 |
| (0.05, 0.3, 2.3374) | 1.71691 | 1735.3 | 0.00178 | 0.0601 |
| (0.2, 0.0, 2.3374) | 0.73512 | 19.28 | 0.06453 | 0.1369 |
| (0.2, 0.3, 2.3374) | 1.20240 | 175.6 | 0.01127 | 0.2179 |
| (0.2, 0.3, 1.2) | 1.60006 | 175.6 | 0.01688 | 0.3263 |
| (0.2, 0.3, 4.0) | 1.72460 | 175.6 | 0.01541 | 0.2979 |

Convergence (L = 10, same machinery, probe_run10.py): ‖∇a_ph‖∞ = 1.41458 vs 1.41413 at L = 8
(≤ 0.04% truncation drift).

## 4. Controls (each capable of failing; all fixed at machine precision)

| control | observed | expectation |
|---|---|---|
| NC1 DS = SD on the curved leaf: ⟨(1−e^{-2b})∇(S_hf)⟩²/‖∇S_hf‖² | 9.0559e-3 (b=0.05), 1.0869e-1 (b=0.2) | (1−e^{-2b})²: 9.0559e-3, 1.0869e-1 — match ≤ 3.9e-16 |
| flat torus twin (T³, FFT): commutator ‖D S − S D‖∞ | 0.2746 (b=0.05) | flat identity D S = S D fails only on the curved geometry; on T³ the same check is the model-precision floor |
| b→0 limit: ∇(cstar0) vs P_F (round-trip of the projection solve) | ≤ 1.3e-14 max | 0 |
| weighted-adjoint identity ⟨S_h\*(u′), W⟩ vs ⟨u′, S_h\*W⟩-form | ≤ 3.1e-14 rel | 0 |
| Hessian integrated identity ∫Tr(J_AᵀJ_A) vs Σ_l e_l‖cₗ‖² | ≤ 3.7e-15 rel | 0 |
| Weitzenböck modal: ∫|Hess_amb Y_l,α|² = e_l table | 0.0 resid (48.0, 48.0, 288.0, 288.0) | 0 |
| splice C¹-join residual at y_star | 2.8e-6 | 0 |
| enforcement: wall ≤ 120 s, RSS ≤ 512 MiB, 1 thread | 89.8 s, 509 MB, OMP/OPENBLAS forced to 1 | enforced via SystemExit above 115 s / 512 MiB |

## 5. Footings

a₀_canonical = 9.3619e-11, a₀_alternative = 1.1279e-10 m/s²; κ = 1/2; ρ_Λ ratios and
‖F‖₂ ≤ c₁√(vol_h·supH/a₀) bounds tabulated (F2_bound_canonical 1.1188e6, alternative 1.0193e6,
ratio 0.911). Both footings give r_curved ≪ 1.

## 6. Weakest claim and domain

**Claim (scoped to the prototype):** on the round S³ leaf with the mode-truncated spectral basis
(L = 8), for b ∈ {0.05, 0.2}, lapse ε ∈ {0, 0.3}, target supH ∈ {1.2, 2.3374, 4.0} (per-unit leaf
scale, seed rng 204), ‖∇a_ph‖∞ ≤ K_tot·‖F‖₂ holds with margin r_curved ≤ 0.0645; ‖∇a_ph‖∞ itself
is ≤ 1.73 (dimensionless, leaf-normalized).

**Limitations:** the S³ round leaf is a model; the physical curved leaf has |Rm| ~ (lapse-scaled)
and possibly noncompact source support; the bound constants are proven only at the sampled
parameter box and the two footings; the supremum checks C0_sup/C0 etc. are numerical, not
analytic proofs. These feed forward to the EFE prerequisite (AS245) and the convergence
of the Green/heat-spectral truncations on the actual leaf.

## 7. Next unresolved implication

Whether the accumulated K_tot bound (which is crude: r_curved ≤ 0.065 with several
supremum-to-L¹ gaps) survives the passage to the physical leaf — the lapse coupling
(grad N)/N and the φ(y) spline at genuine a₀-scale y, where |H|/a₀ ~ 1, is the first bridge
not tested here (all cells sit at H-scale ~ 1.a₀ on the physical leaf the argument needs
y = O(1) behavior, which is exactly where h_mono saturates).

## 8. Files in this run directory

- `as204_curved_heat_force.py` — bounded prototype (all six cells, controls, enforcement)
- `residuals.json` — full machine-readable result grid (residuals, controls, constants, footings)
- `AS204_four_term_identity.lean` — Lean 4 certificate of the four-term Jacobian identity
  (compiles under `lake env lean`; axioms {propext, Classical.choice, Quot.sound})
- `raw_output.txt` — raw stdout of the grid run
- `probe_*.py`, `dbg_*.py` — validation probes (basis, FD, LS, memory, controls)