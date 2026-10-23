# C8_instantaneous — FROZEN CRITERIA (written before any script or number)

Question. C5 found that the only healthy covariant parent is C4's literal Khronon + P theory (β = η = γ_F = 0,
BS K(Q) dust, stiffness γ_L = K L★²/2, capped W). There P and the lapse (the khronon acceleration A_i = ∂_i ln N) obey
elliptic equations on each leaf: they respond instantaneously. (1) Is that leaf problem well posed? (2) Does the
instantaneous response have consequences that existing data already constrain? (3) What, physically, does
"fails criterion A" mean here?

## Record checked before freezing

- `covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
- C4 README (action; static Lagrangian −|∇Φ|²/2K + P·∇Φ − W(K|P|) − (γ_L/2)(∇·P)²; ξ = 1), C5 README + script
  (theory family; DOF table: C4-literal = 2 tensor + ω = 0 pair; tensor ω² = k²; "nonlinear well-posedness" OPEN).
- CFG292 README (khronon principal symbol; the bare k² leaf-elliptic factor; Cauchy problem must be posed on khronon
  leaves; criterion B = global time allowed, USER DECISIONS 09-26), WT-02 README (CFG938 medium: elliptic χ/λ on static
  media, ill-posed heat pair on FRW — a different parent, not this one).
- DSF-21 A22 report (α₁ = α₂ = 0 at PPN order; a_P = GM/L★²; D5 "isotropic (1+2w²)"; P stress inventory D3),
  A82 VERDICT (α̂₁(internal) = 3.0e-24 vs 3.5e-5).
- External bounds already transcribed in the record (no new downloads): Kramer et al. 2021 PRX 11 041050 double pulsar
  Ṗ_b(obs)/Ṗ_b(GR) = 0.999963 ± 0.000063 and Weisberg & Huang 2016 ApJ 829 55 Hulse–Taylor 0.9983 ± 0.0016
  (`real_research/reviews/mi_pulsar_pta_precision_ledger_2026.py` L182–186); Shao & Wex 2012 |α̂₁| < 3.5e-5,
  Shao et al. 2013 |α̂₂| < 1.6e-9, Nordtvedt 1987 |α₂| < 2.4e-7 (secondary), LLR α₁ (`data_assembly/DOOR11_LITERATURE_2026-09-29.md`
  L32–39); GW170817 |c_T − 1| < 1e-15 (`EMPIRICAL_TESTS.md` A6). These are record transcriptions, not re-verified
  against the papers in this lane (no downloads); labelled as such.

## Scope (fixed now)

The leaf problem is studied at the order the screened theory is used: weak-field metric (Φ = lapse potential = ψ),
**fully nonlinear in P and W**, with γ_L > 0, γ_F = 0, η = β = 0, ξ = 1, μ_K⁻¹ ≥ 100 kpc (K(Q) term dropped where
μ_K² r² ≪ 1; stated). Energy functional E[Φ, P] = ∫ |∇Φ − K P|²/2K + g(K|P|) + (γ_L/2)(∇·P)² + ρΦ, with
g(u) = W(u) − u²/2K, W = (a₀²/K)[−u/a₀ − ln(1 − u/a₀)]. Strong-field (NS) leaf problems, the coupled
hyperbolic–elliptic evolution with GR's tensor sector, and khronon-dust caustics are OUT of scope and will be stated
as OPEN.

## Checks (pass lines)

- **K1 symbol positivity.** Linearise the leaf Euler–Lagrange system at any state with u ∈ [0, a₀) and any angle
  between ξ and P. Its Fourier symbol M(ξ) on (δΦ, δP) is positive definite for every ξ ≠ 0, and its Schur complement
  is ≥ min(K, γ_L|ξ|²) (sympy closed form + numeric grid: u/a₀ ∈ {0, 1e-6, 0.1, 0.5, 0.9, 0.999, 1−1e-9},
  |ξ|L★ ∈ 1e-4…1e4, ≥ 7 angles). PASS iff all eigenvalues > 0 and the bound holds (rel. tol 1e-10).
- **K2 convexity.** sympy: the static Lagrangian equals −[|a − Kp|²/2K + g(K|p|)] identically (residual 0);
  g′ ≥ 0 and g″ ≥ 0 on [0, a₀); W → +∞ as u → a₀⁻. PASS iff all hold.
- **K3 uniqueness kernel.** The conditions for E to be affine along a segment between two solutions
  (iξδΦ = KδP, ξ·δP = 0) have only the trivial solution for ξ ≠ 0 when γ_L > 0 (rank 4). PASS iff rank 4.
- **K4 spherical boundary-value problem** (scaled units a₀ = L★ = 1; r_M/L★ = 3 and 0.3). (i) Two different initial
  guesses converge to the same solution, max rel. difference < 1e-6; (ii) max u/a₀ < 1; (iii) inner hedgehog
  u → GM/L★² (A22's a_P) within 2 % at r = 0.01 L★; (iv) far field u/√(a₀ g_N) within 2 % of 1 at the outer edge
  of the AQUAL region (r = 30 max(r_M, L★²/r_M)); (v) domain doubling changes the inner solution by < 1e-3.
  PASS iff all.
- **K5 3D non-symmetric solve** (two unequal masses, small grid ≤ 32³, Dirichlet Φ = 0 at the box, natural BC for P,
  W extended convexly above 0.99 a₀). (i) Two initial guesses agree, max rel. difference of (∇Φ, P) < 1e-4;
  (ii) max u/a₀ < 0.99 (the extension is inactive, so the solution is that of the capped problem);
  (iii) discrete gradient norm < 1e-6 of its initial value. PASS iff all.
- **K6 (by construction, no weight)** — the β = η = 0 ADM Lagrangian contains no Ṅ and no Ṗ: their momenta vanish,
  so they are constraints. Reported, not scored toward the verdict.
- **K7 binary pulsars.** (a) Radiative: the instantaneous sector has no propagating mode (C5 DOF) and its leaf
  equations are T-even with no ∂_t, so the force it mediates is −∂E_min/∂x of the instantaneous configuration —
  zero secular work per orbit. (b) Conservative: leading fractional correction ε = (a/L★)² (screened hedgehog,
  separation a ≪ L★), and the nonlinear piece ε·(GM/L★²)/a₀ on both footings; L★ = 20, 24, 90 pc; systems PSR
  J0737−3039 and B1913+16. PASS iff ε / (fractional Ṗ_b precision) < 1 for all rows (UNCONSTRAINED).
- **K8 preferred frame.** sympy: a field obeying a ∂_t-free leaf equation, sourced by a body moving at w, is
  f(x′_∥/γ_w, x′_⊥) in the body frame. For the P potential Φ_c = (GM/L★²) r this is a (w·n̂)² anisotropy with
  coefficient −1/2. Report its α₂-equivalent (r/L★)² at 1 AU (vs 2.4e-7) and at a NS radius 12 km (vs α̂₂ < 1.6e-9),
  and compare with A22 D5. PASS iff all ratios < 1. A disagreement with A22's "isotropic" statement is recorded as a
  finding, not a fail.
- **K9 GW170817.** Tensor principal speed = 1 exactly at β = 0 (C5 H1). sympy: the P background's W term gives the
  tensor mode at most a mass m² = c_m u²; Δv/c = m²/2k² at 100 Hz with u ≤ a₀ (both footings) vs 1e-15.
  PASS iff < 1e-15.
- **K10 lensing vs dynamics (estimate only, not scored).** Φ = ψ at O(ρ) with time dependence (P anisotropic stress
  is O(ρ²), A22 D3). Instantaneous-vs-retarded size max(v²/c², a r/c²) for illustrative systems (Jupiter's P part,
  a merging cluster). Reported as ILLUSTRATIVE.

## Mutation

`C8_MUTATE=1` flips the sign of γ_L. K1, K3 must fail; K4/K5 should lose uniqueness or convergence. Outputs
`*_MUTATE.out`, `*_results_MUTATE.json`.

## Verdict lines

- **WELL-POSED + UNCONSTRAINED**: K1–K5 PASS and K7–K9 PASS.
- **WELL-POSED + CONSTRAINED (name the bound)**: K1–K5 PASS and any of K7–K9 FAIL.
- **ILL-POSED (where)**: K1 or K3 FAIL at some u < a₀, or K4/K5 non-unique; name the state.
- Any verdict is scoped to the weak-field, nonlinear-in-P leaf problem; full nonlinear Einstein + khronon evolution stays OPEN.

## Logical status (item 3) — written in the README as prose, with no score

State: what is instantaneous (P and the khronon lapse on τ-leaves), why it is physical and not gauge (τ is a field; the
leaf cannot be changed — CFG292 T7), how it differs from GR's constraints (gauge + conserved charges, curvature
propagates at c), whether it is a usable signal channel (size of the effect), and what criterion A vs B means for it.

Settings: κ = ½ FITTED; footings 9.36e-11 / 1.13e-10 m/s², never pooled; no dark-matter particle; not "theory closed";
nothing here says the data favour the framework.
