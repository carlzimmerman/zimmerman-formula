# ARGON01 FROZEN CRITERIA — the dynamical-modulus route to κ (AS069.C01 executed)

Written and committed ALONE, before any script. Date 2026-10-15.
Home: `argon_push/ARGON01_modulus_kappa_2026-10-15/`. κ = ½ is FITTED, not derived. The two
footings are never pooled. Nothing here adds a particle species or a new force to the framework;
the modulus term under test is a *declared extension* (the registered AS069.C01 child of
`deepseek_push/astra_spawn_ideas/branches/AS069/AS069.C01.md`, state "ready; not dispatched").
Not "theory closed".

## Question (from AS069.C01, verbatim in content)
Does promoting the dimensionless kernel parameter λ of the MU_λ response family to a dynamical
modulus,

    S_λ = S + ε · ∫√−g [ (∇λ)² + W(λ) ] d⁴x,      ε ≠ 0 declared, W ≥ 0 bounded, λ → λ(x),

fix the primitive zero C and the kernel parameter JOINTLY at the κ = 1/2 footing — i.e. at
(C, λ) = (64π a₀²/α, 2) with ρ_vac = ρ_L > 0 — while the static force equations remain exactly
those of some MU_λ member?

## Class and conventions (pinned)
- Corpus A1-class local action, g03t convention (k01 `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py`, pinned
  8df5a3ab…): L = √−g [R − 2Λ − (2−K_B)J(Y;λ) − K(Q) + 2(2−K_B)J^μ∂_μφ + …]/(16πG), α = 2−K_B ∈ [7/4, 2].
- Static 1D reduction (k01 K1): L = −2Ψ′² + 2αΨ′φ′ − αJ(φ′²;λ) − ρ(Ψ+φ); the J^μ∂_μφ term is the λ-independent 2αΨ′φ′.
- MU_λ (parent AS069): μ_λ(Y) = 1 − (1+Y)^{−λ}, J_λ(Y) = ∫₀^Y μ_λ dy, Y = g/s, s = c√(Gρ_L), κ = a0/s = 1/λ; the
  primitive's additive constant C(λ) is free (J(0) = 0 convention); ρ_vac = α(J(0;λ)+C(λ))/(16πGc²) = αC(λ)/(16πGc²).
- Parent theorem (AS069, Lean-certified): observables' Jacobian ∂(F,V)/∂(λ,C) is rank 2, ∂F/∂C ≡ 0, ∂V/∂C = α/64π ≠ 0;
  the vacuum datum is λ-blind (C compensates); κ = 1/2 ⇔ λ = 2 is adoption, never a consequence.
- Sources: AS069 parent result (provisional), AS067 zero-mode lemma (provisional), k01 K1–K6 (committed). No Q/RAR/EXP/MONO
  import. No new observation, no download.

## Verdict rules (pre-registered)
- **PASS-EXACT (a)**: an explicit (ε, W), W ≥ 0 bounded, ε ≠ 0, with no constant beyond (ε, W) themselves, whose on-shell
  system (force + modulus + Friedmann) fixes C with NO remaining integration constant AND λ = 2, with ρ_vac = ρ_L > 0 and
  exact MU_λ forces.
- **NO-GO (b)**: a theorem over the declared (ε, W) class showing δS_λ/δλ cannot remove both independent freedoms
  (C-zero-mode + λ), with the obstruction exhibited and the parent's rank theorem shown to survive the extension. The
  surviving positive statement MUST quantify over (ε, W).
- **FAIL**: any individual proof step that does not close.

## Gates and controls (all required; any miss ⇒ INADMISSIBLE, not scored)
- G1 C-invisibility: EL(φ), EL(Ψ) contain C only through J′ (parent zero-mode lemma, re-checked under λ(x)); EL(λ) contains
  C(λ) only through C′(λ); hence C₀ = C(λ₀) − ∫… is a free integration constant of every solution. Check: sympy EL of the
  extended L for generic J(Y;λ) + C(λ).
- G2 No constant-modulus halo: for ε ≠ 0 the modulus equation on a non-trivial static halo admits NO solution with λ ≡ const,
  because ∂J/∂λ(Y) is strictly increasing in Y (∂²J/∂Y∂λ = (1+Y)^{−λ}ln(1+Y) > 0) and Y varies. Thus an active modulus is
  position-dependent ⇒ the force law is μ_{λ(x)} — not a member of MU_λ (claim (ii) fails) — unless ε freezes it.
- G3 ε-dilemma: ε small ⇒ λ(x) varies ⇒ κ_eff environmental/radial variation, bounded by the record (environment slope
  −0.010 ± 0.015, canonical S1; per-galaxy λ_eff spread F3 2.15 ± 0.35); ε large ⇒ modulus frozen ⇒ no selection. Either
  limb kills the derivation claim; quantify with the recorded numbers.
- G4 FLRW background: at Y = 0 the modulus equation reduces to C′(λ) = εW′(λ)/α — fixes only C′ at the background; λ_bg and
  C₀ remain free. Check symbolically in minisuperspace.
- G5 Negative control (must be capable of failing): construct the claimed counterexample — W with a minimum at λ* = 2 and a
  compensating C′(λ). It must FAIL the claim: (i) λ* is a free parameter of W (the number 2 is input, not output);
  (ii) C₀ survives ⇒ ρ_vac unconstrained (calibration, parent S4, not derivation); (iii) cross-halo consistency: one C′
  function must serve every halo, whose Y-profiles differ — exhibit the contradiction for two halos.
- G6 Mutation (must still fail): replace MU_λ by the degenerate shift family J = J₀(Y) + λC₀ (λ a pure label, ∂F/∂λ ≡ 0).
  The modulus equation must still fail to fix C.
- K1 numerology guard: record 5.364 ≈ 16/3 (0.6%) with Z²/2π = 16/3 exactly as a non-claim, so it is never adopted without
  a mechanism (mirrors k01 K6).
- K2 k02 scale check (preliminary, stated as check not theorem): a global/sequestering constraint on any local functional of
  the static sector gives ρ_vac/ρ_c either ~α/16π ≈ 0.04 (dust rest Lagrangian) or (v/c)²-suppressed (binding/response
  functionals) against the required Ω_DE/Ω_c = 0.686/0.265 ≈ 2.6; any O(1) coefficient needed to evade is a new constant
  (G6 of CFG-D). Quantified in the script.

## Kill / close
- If the no-go closes (b): κ stays FITTED; the local modulus class is closed; the k02/sequestering (global) route is the
  only remaining class; the sharpened obligation is restated (§8 of the report). Never write "κ derived".