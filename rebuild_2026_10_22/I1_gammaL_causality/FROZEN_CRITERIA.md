# I1_gammaL_causality: FROZEN CRITERIA (committed alone, before any script or number)

## Question

v4 = Skordis–Złośnik AeST (arXiv:2007.00082, eq. `Minkowski_action`, on disk) + C1's capped F (static limit = the
canonical law μ = x/(1+x)) + the stiffness term −(γ_L/2K²)(q^{μν}∇_μ∇_νφ + θQ)² (C1, C3: β_L = (2−K_B)L★²/2).
C5 defect (b): the γ_L term gives the scalar ω² ⊃ (2−K_B)L★²k⁴/(4K₂), i.e. ω ∝ k², no cone. What is v4's causal
structure, is its Cauchy problem well posed, and what is its status under the owner's criteria A (no influence faster
than c) and B (global time order: nothing backward in time, no closed signal loops)?

## What was done before this file (disclosure)

Read: both BRIEFs (+ doors BRIEF), THEORY_V3_DRAFT §1b, C1/C3/C5/C6/C8 READMEs, H1/H3 READMEs, C5's AeST code
(`sz_lagrangian`, H10), SZ21's `Minkowski_action` paragraph on disk. **No sympy or numeric computation of this lane has
been run.** Pen-and-paper expectations (not scores), stated so the test can fail them:
- E1. The γ_L term linearises to −(γ_L/2K²)(∇·V)² with V_i = ∂_iϕ + Q₀A_i, containing **no time derivative** of any
  field (the θQ piece cancels the Φ̇ terms); on FRW its background value vanishes.
- E2. In the aether frame the scalar is beam/Schrödinger-type (ω real, ω ∝ k²): Petrovskii-correct, time-reversible,
  dispersive (not diffusive), infinite group speed 2√A k.
- E3. Its symbol is aether-referenced. On a Cauchy slice tilted by w relative to the aether, the k⁴ term turns the
  dispersion quartic in the slice frequency and two roots go complex with Im ω ∝ κ/w above κ_c ≈ 1/(2√A w)
  (Hadamard ill-posed, like Schrödinger or Laplace posed on a non-characteristic "timelike" surface).
- E4. C1 says AeST reproduces AQUAL only with a **twisting** aether. If the twist is forced in v4's static solutions
  (a_T ≠ 0 with ∇×a ≠ 0 for non-symmetric sources), no slice is aether-orthogonal on an open set, so E3 applies
  there, and high-k rays (near-horizontal curves) can close loops with ∮a·dx ≠ 0 (criterion B).

## 1. Declared inputs (no fitting, no scans to a target)

- SZ21 `Minkowski_action` (on disk, `../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex`) and its
  stated dispersion relations; C5's reading of the missing operator before K_B|…|² as "+".
- Capped F response (C5 H10): λ_T = y, λ_L = (1+y)² − 1, y = g/a₀; Y = 0 (vacuum, FRW): λ = 0.
- AeST constants (not fixed by any lane; reported grid, not fitted): K_B ∈ {0.05, 1}; c_s(λ=0) ∈ {1, 0.1}, so
  K₂ = (2−K_B)/(K_B c_s²); μ⁻¹ ∈ {1, 10} Mpc; then Q₀ = μ c_s √(K_B/2), ℓ_F² = 2K_B/((2−K_B)Q₀²).
- L★ ∈ {24, 50, 90} pc (FITTED, D10/C3 window); β_L = (2−K_B)L★²/2.
- Sun-in-Galaxy background: x_e from D7d `R2_scan` (as C5/C6): canonical 1.30–2.60, alt 1.15–2.15. Footings
  a₀ = 9.36e-11 (canonical) / 1.13e-10 (alt) m/s², never pooled.
- Galactic twist magnitude: ILLUSTRATIVE Kuzmin disc M = 6e10 M☉, a = 3 kpc, Sun at (ϖ, z) = (8.2, 0.02) kpc, law
  applied pointwise along g_N (H1's algebraic per-point form). Magnitude only; no verdict rests on it.
- C8's lab case (1000 kg moved 1 m, read at 1 km) for the criterion-A size comparison.

## 2. Checks (`i1_gammal_causality.py`, one line each; deterministic; sympy/mpmath)

- **K1 (linearisation, E1).** Covariant (q^{μν}∇_μ∇_νφ + θQ) with general h_{μν} (no gauge fixing) and A_μ
  perturbation about Minkowski: equals ∂_i(∂_iϕ + Q₀A_i) at first order, residual 0, and contains no ∂_t. On flat FRW
  with comoving aether: background value 0 (residual 0); first-order part has no ∂_t of ϕ. PASS iff all residuals 0.
- **K2 (own scalar operator).** From SZ eq. `Minkowski_action` + the stiffness term (own code, Newtonian gauge, fields
  Ψ, Φ, α, ϕ): det degree 4 in ω; non-zero branch ω² = C5 H10's closed form, residual 0. PASS iff both.
- **K3 (aether slicing: Petrovskii).** For 0 < K_B < 2, K₂ > 0, λ ≥ 0, L★ > 0: every ω² root is real and ≥ 0
  (symbolic positivity of the coefficients), and ω²/k⁴ → A = (2−K_B)L★²/(4K₂) > 0. PASS iff both; then the aether-slice
  problem is well posed (Im ω ≡ 0, time-reversible, dispersive).
- **K4 (tilted slicing, E3).** Lorentz-transform the aether-frame relation s² = A p⁴ + B p² + M² (s = −u·k,
  p² = q^{μν}k_μk_ν) to a slice whose normal has velocity w relative to the aether. (a) w = 0: all roots real.
  (b) κ ⟂ w, exact: roots complex iff κ > κ_c(w, A, B, M) (closed form). (c) mpmath roots at κ = 10³κ_c over 7
  directions: max Im ω / (κ/(γ_w w)) within 1e-2 of 1. PASS iff (a), (b), (c) hold.
- **K5 (twist forced, E4).** Static transverse equation (ℓ_F²/2)∇×∇×V_T + M_T V_T = −Π(M δV_L), a_T = V_T/Q₀:
  (a) sympy: |Π M k̂| = (1+y) y |sinθ cosθ| for M = diag(1+y, 1+y, (1+y)²); (b) the Solar-System particular solution
  Ω_V = −(1+y) y h r sinθ cosθ/(2ℓ_F²) φ̂ satisfies the toroidal ODE, residual 0. PASS iff both.
- **K6 (ray loop identity).** At linear order a vector orthogonal to u = (1, a) has e⁰ = a·ê, so along a ray moving at
  speed v relative to the aether, Δt = ℓ/v + ∮a·dx. sympy residual 0 → closed signal loop iff v > ℓ/|∮a·dx|. PASS iff 0.
- **K7 (magnitudes, reported; scored only on convergence).** Galactic twist Ω_a at the Sun and over a meridional
  loop (illustrative Kuzmin), the minimal tilt w over 100 AU and 1 kpc regions, κ_c and λ_c = 2π/κ_c, the growth rate
  at 2κ_c, the loop time Δt and the speed needed to close it, on the declared grid. PASS iff a grid refinement changes
  Ω_a at the Sun by < 10 %.
- **K8 (completions, Q3).** (a) Time-derivative partner: q^{μν} → g^{μν} in the stiffness (i.e. (□φ + …)²): static
  symbol identical to v4 (residual 0) AND report Krein signs of all roots on Minkowski. (b) Auxiliary field σ with a
  Lorentz-invariant kinetic term ε(∂σ)²/2: report Im ω and Krein at large k for ε = ±1e-2. Scored only on the sympy
  residual in (a); the health reading is reported.
- **K9 (criterion-A size).** Lab signal (Gm/L★²)(Δx/r) reproduces C8's 1.2e-46 m/s² (L★ = 24 pc) to 1e-2.

`I1_MUTATE=1`: γ_L → −γ_L (K3 must fail) and isotropic response λ_L = λ_T (K5 must fail). Outputs `*_MUTATE.*`.

## 3. Verdict rule (applied in this order)

- K1 or K2 FAIL → **UNDECIDED** (machinery).
- K3 FAIL (complex ω² on the aether slicing) → **ILL-POSED (everywhere)**.
- K3 PASS, K4 PASS, K5 PASS → **ILL-POSED (where the aether twists)**: well posed (Schrödinger-type) on twist-free
  backgrounds (Minkowski, FRW, exact spherical symmetry); Hadamard ill-posed at κ > κ_c on every slicing in any
  non-symmetric bound system. Criterion A violated everywhere; criterion B met on twist-free backgrounds and violated
  in principle where the aether twists (closed loops, K6). Sizes from K7, K9.
- K3 PASS, K4 PASS, K5 FAIL (twist not forced) → **WELL-POSED, CRITERION A VIOLATED (size K9) / B MET**.
- K3 PASS and K4 FAIL (tilted slices well posed) → **WELL-POSED, CRITERION A VIOLATED / B MET**.
- **WELL-POSED + CAUSAL** only if no ω ∝ k² branch exists (K2's branch absent).
- Q3: a completion is reported as a named, counted addition only if it keeps the static symbol, is ghost-free and has
  bounded Im ω; otherwise "none found".

Reading limits declared now: frozen-coefficient (WKB) analysis; linear only; no nonlinear theorem; an EFT cutoff above
κ_c would hide the ill-posedness but is not derived in the record and would be a new posit.

κ = ½ FITTED. Both footings, never pooled. No dark-matter particle. Never "theory closed". Nothing here says the data
favour the framework.

## AMENDMENT A1 (PRE-RESULT: written before any script of this lane was run; no pass line changed)

The illustrative Galactic model in §1 is changed from a Kuzmin disc to a **Miyamoto–Nagai** disc (M = 6e10 M☉,
a = 3 kpc, b = 0.28 kpc; Sun at (8.2, 0.02) kpc). Reason (pen and paper, while writing the script): above and below a
Kuzmin disc the field is that of a displaced point mass, |g_N| depends only on the distance to that point, so the
pointwise-law twist source ∇ν × g_N vanishes identically off the plane and its tangential part is continuous across it.
The Kuzmin case is kept as a code sanity line (its twist must come out ≈ 0, reported, not scored). K7's scored line
(grid refinement < 10 % at the Sun) now applies to the Miyamoto–Nagai disc.
