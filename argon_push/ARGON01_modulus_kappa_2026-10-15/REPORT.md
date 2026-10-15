# ARGON01 — The dynamical-modulus route to κ is closed: no local (ε, W) can fix (C, λ) = (64πa₀²/α, 2)

**Date:** 2026-10-15. **Home:** `argon_push/ARGON01_modulus_kappa_2026-10-15/`.
**Pre-registration:** `FROZEN_CRITERIA.md` (committed alone, `2a938996e`, before any script).
**Run:** `OMP_NUM_THREADS=1 timeout 120 python3 modulus_lambda.py` → `modulus_lambda.out`, `modulus_results.json`.
**Spec executed:** `deepseek_push/astra_spawn_ideas/branches/AS069/AS069.C01.md` ("ready; not dispatched") — the
dynamical-modulus extension of the parent AS069 rank/calibration result. **0 FAIL, exit 0, wall 0.2 s, 1 thread,
max RSS 112 MB** (T1x 1024³ envelope respected).

## What was asked (verbatim in spirit of AS069.C01)
Promote the kernel parameter λ of the MU_λ response family to a dynamical modulus,

  S_λ = S + ε·∫√−g [(∇λ)² + W(λ)] d⁴x,    ε ≠ 0, W ≥ 0 bounded,

and test whether δS_λ/δλ = 0 fixes the primitive zero C and λ JOINTLY at (C, λ) = (64πa₀²/α, 2) with
ρ_vac = ρ_L > 0, while the static force equations remain exactly MU_λ. Pass ⇒ a scoped gate-13 derivation of
κ = ½; else a restricted no-go quantified over (ε, W).

## The answer: NO-GO, with five theorems (all machine-checked, 21/21)

**N1 — C-invisibility (the load-bearing theorem).** In the extended action the primitive's additive constant
C(λ) enters **no** Euler–Lagrange equation except as C′(λ) in the modulus equation:

  EL(λ):  −2ε λ″ + εW′(λ) − α·∂J/∂λ(Y;λ) − α·C′(λ) = 0          (α = 2−K_B, static 1D, k01 realization)

  EL(φ), EL(Ψ): unchanged, contain only J′ (sympy-verified for generic J(Y;λ) + C(λ)).

Hence C(λ) = C₀ + ∫C′(λ)dλ with **C₀ a free integration constant of every solution**. The vacuum energy
ρ_vac = αC(λ)/(16πGc²) is therefore **never fixed by any equation of the extended class** — the Friedmann
equation observes ρ_L and sets C₀ by *calibration* (parent S4), exactly as before. **A local modulus cannot
derive the vacuum offset; there is no coupling (ε, W) under which ρ_vac = ρ_L is an output.**

**N2 — there is no static halo with λ = const (for any ε ≠ 0, any W).** The modulus source is strictly
monotone in Y:

  ∂/∂Y [∂J/∂λ] = (1+Y)^{−λ} ln(1+Y) > 0   (verified for λ = ½, 1, 2, 3;  dJ/dλ ~ Y²/2 − (λ+1)Y³/6 + … deep)

so on any non-trivial halo (Y varies; e.g. the framework's own log branch Φ = C ln r gives
residuals −0.464 / −0.081 / −0.0075 at 5/10/20 kpc at λ ≡ 2 — can't vanish) the constant-λ ansatz fails.
An *active* modulus is **position-dependent**: the force law becomes μ_{λ(x)} — **not a member of the MU_λ
family** — so requirement (ii) of the claim fails by construction. In the ε = 0 corner the modulus equation is a
constraint C′(λ(x)) = −∂J/∂λ(Y(x)) slaving λ to the profile — same conclusion (no global MU_λ member).

**N3 — the background is free.** At Y = 0 (FLRW, Theorem A: vacuum-blind response) the modulus equation
reduces to C′(λ) = εW′(λ)/α: it fixes only C′ at the background value of λ. λ_bg sits at any critical point
of W, and W's shape is a **new function/constant** — the number 2 appears only as the chosen minimum of W.
Nothing in the equations knows λ = 2 (or any λ).

**N4 — the counterexample control fails exactly as required.** Construct the claimed winner: W = 1 − cos(2π(λ−2))
(minimum at λ* = 2 by construction) plus a compensating C′(λ). It fails on three legs:
(i) λ* is a free parameter of W — 2 is input, not output;
(ii) C₀ survives (N1) — ρ_vac stays free no matter what W does;
(iii) one C′ function cannot compensate two different halos: dJ/dλ = 0.232 (M_b = 1e11 at 5 kpc) vs 0.0004
(M_b = 3e10 at 20 kpc) at the same λ — a single C′(λ) cannot cancel both, so the "compensating" construction
is inconsistent across the halo population.

**N5 — the mutation survives.** Replace MU_λ by the degenerate shift family J = J₀(Y) + λC₀ (λ a pure label,
∂F/∂λ ≡ 0): EL(λ) = −α[C₀ + C′(λ)] − 2ελ″ + εW′ = 0 — C₀ enters only as an initial value, still free; the
modulus fixes nothing. The no-go is family-stable.

**C-compensability (why every local route dies, restated).** In the extended parameter pair (λ, C₀) the parent's
observables' Jacobian is unchanged in structure: ∂F/∂C₀ = 0 exactly and ∂V/∂C₀ = α/64π ≠ 0 — rank 2 generically.
The modulus extension is **C-compensable**: it only relabels C → C₀ + ∫C′dλ. The parent's theorem (the vacuum
datum is λ-blind) survives the dynamical extension unchanged — the C zero-mode is structural, not a parameter
choice. *Any* derivation of κ = ½ must therefore come from a structure in which the observable rank actually
drops — i.e. nonlocal/global (k02/sequestering-class), never a local field λ.

## The ε-dilemma (new falsifier for the whole position-dependent-kernel class)
An active modulus (small ε) produces λ(x)-structure in every halo: excursion Δλ ~ α⟨∂J/∂λ⟩R²/(2ε) ≈
0.153·α·R²/ε at the transition. Keeping Δλ inside the measured per-galaxy band (F3 λ_eff = 2.15 ± 0.35, i.e.
κ = 0.465 ± 0.076; environment slope −0.010 ± 0.015, canonical S1) at R = 10 kpc forces ε ≳ 4.2×10⁴⁰ (SI,
4D-action units) — the modulus frozen. A frozen modulus selects nothing (κ stays a parameter). An active
modulus is excluded by κ_eff universality. **Kill test for this class: κ_eff per galaxy measured below the
current band.** Either limb — the derivation fails.

## k02 scale check (preliminary; saves the next lane a wrong turn)
The no-go leaves global/sequestering (k02) as the only open class. A preliminary scale check: a sequestering
constraint on any *local functional of the static sector* gives ρ_vac/ρ_c ≈ α/16π = 0.0398 (dust rest
Lagrangian — the dominant functional) or ~(v/c)² ≈ 1.6×10⁻⁷ (binding/response functionals), against the
required Ω_DE/Ω_c = 0.686/0.265 = 2.59 that the framework's own vacuum offset needs. That is a factor 65
(dust) to 1.6×10⁷ (binding) short. Any O(1) coefficient engineered to reach 2.59 is a new constant (CFG-D G6).
**Preliminary, not a theorem**: a complete k02 construction with a tuned measure could evade; the cost is then
counted as knobs. Recommendation: do not dispatch a naive k02 lane; dispatch one that quantifies its measure.

## Numerology guard (recorded, NOT a claim)
Ω_c/Ω_b = 5.364 is 0.57% from 16/3, and Z²/2π = (32π/3)/(2π) = 16/3 exactly. 16/3 = 4/(3κ²) at κ = ½ is the
π-free rational in the framework's own bookkeeping. This is **recorded so that no agent adopts it without a
mechanism** (k01 K6 spirit). If a mechanism ever produces Ω_c/Ω_b = 16/3, it simultaneously gives the cosmic
cold abundance AND (via GF2's static closure) the vacuum-ladder cross-step — the conjoint target of
CFG635 G7 / CFG723 E1 / GF2 STATE door 2. Until then it is numerology.

## What this does NOT establish
- No statement about Q/RAR/EXP/MONO kernels or other response families beyond MU_λ (the generic-J pieces —
  C-invisibility and the zero-mode lemma — hold for any J; the monotonicity legs are MU_λ-specific but hold
  for every member tested).
- No claim about criterion B, DOF counts, PPN, lensing or stability of the framework itself (untouched).
- No empirical test; nothing here falsifies the framework — it closes an attempt to *derive* κ = ½.
- The framework's own static-branch closure (GF2: κ = ½ from σ² = C/2, self-sourced log branch) is untouched
  and remains the standing derivation, pending referee. This push closes the *vacuum-coupling* side: no local
  completion of the MU_λ action can promote that static ½ to the vacuum ½.

## Verdict (loud)
**κ = ½ stays FITTED, not derived.** The registered AS069.C01 route — the only local mechanism left on the
record — is **CLOSED with a theorem over the declared (ε, W) class.** The C zero-mode is structural:
a local dynamical field cannot reduce the observables' rank; only a global/sequestering structure (k02-class)
can, and its naive scale is 65×–1.6×10⁷× short of the framework's own vacuum offset. Not "theory closed".
The remaining open obligation is unchanged in content and sharper in shape: *a κ-derivation must output the
absolute primitive zero C₀ = 64πa₀²/α from a source that is not a local functional of the static fields.*