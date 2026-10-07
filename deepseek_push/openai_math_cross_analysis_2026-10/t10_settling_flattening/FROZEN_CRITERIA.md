# T10 — FROZEN CRITERIA: the settling-flattening theorem

**Claim to test (novel synthesis of the campaign's own results):**

For the framework's point-baryon host with phantom target ρ_ph:

  (S1)  The JKO settling reduces EXACTLY to the pure heat equation in
        μ-space,  μ(r) := r²ρ(r):   ∂ₜμ = ∂²μ/∂r²  (drift terms cancel
        identically for the deep target ∇logρ_ph = −2 r̂/r). [T3 claimed
        this; this lane verifies the substitution symbolically and
        numerically, and documents the sub-leading residual for the FULL
        kernel target.]

  (S2)  Kinematic identity (sphericity, Newton's integral):
        v²(r) = (4πG/r)·∫₀^r μ(s) ds — the rotation curve is the running
        μ-average;  EXACTLY FLAT ⇔ μ ≡ const.

  (S3)  Deep-MOND is the uniform μ-state: μ_ph = √(GMa₀)/(4πG) — from the
        certified 4πGr²ρ_ph = √(GMa₀). Hence v_flat² = 4πGμ_ph and
        v_flat⁴ = GMa₀ (the cancellation 16π²G²·(GMa₀/16π²G²) is exact).

  (S4)  The enclosed-phantom "area law": deep μ-constancy ⇒
        M_ph(<r) = 4π·μ_ph·r — the phantom halo behaves as a 2-D-gauge
        screen (mass ∝ radius, not radius³).

  (S5)  Diffusive relaxation falsifier: a local baryonic perturbation
        (μ-bump of width ℓ) relaxes with τ ∝ ℓ² (heat kernel; first mode
        e^{−π²Dt/r_out²}); the RAR-scatter bumps are predicted to decay
        diffusively, NOT exponentially in radius or as a power law.

  (S6)  P3-radius corollary: the kernel-exact mass law M_ph(<r) = M_b/(e^{r_t/r}−1)
        puts the cosmic cold share 5.36 M_b at r_supply = r_t/ln(1 + 1/5.36)
        = 5.848 r_t (71.4 kpc MW canonical; ~714 kpc for a 1e13 M_b cluster,
        INSIDE R500 — consistency with P4, "clusters hold their full share").

**Screens (frozen):** Q1: derives the SETTLING/FLATNESS structure from the
fitted-a₀ framework (a₀ enters only through the unit r_t and μ_ph); κ = ½
stays FITTED. Q2: no inserted rational; S1 is an exact substitution, S2-S4
exact algebraic identities, S5-S6 corollaries of the closed forms. Q3:
functional/equational, not a constant search — n/a.

**Checks that can fail (exit 1):**
  C1  S1 symbolic: sympy substitution of μ = r²ρ into ∂ₜρ = ρ″ + 4ρ′/r +
      2ρ/r² (equivalently the deep-target JKO RHS) yields EXACTLY μ″
      (residual ≡ 0 to 1e-12 over a symbolic parameter sweep).
  C2  S1 numeric: finite-difference solve of the deep-target JKO PDE vs
      the heat equation on μ on r ∈ [r_in, r_out]: max |Δ| < 1e-4 × scale.
  C3  S2: for 200 random smooth μ profiles (log-normal bumps), |v² − 4πG·Āμ|
      < 1e-9 relative (trapezoid, exact identity test).
  C4  S2 flat: μ ≡ const ⇒ v ≡ const at 1e-12; and a 10% tilted μ ⇒
      v varies by > 1% (equivalence bites both ways).
  C5  S3 cancellation: v² = 4πGμ_ph ⇒ v⁴ − GMa₀ ≡ 0 symbolically.
  C6  S5: heat-bump relaxation timescale exponent ∈ [1.9, 2.1] (fitted
      τ vs ℓ over bumps of width 1,2,4 kpc at fixed amplitude).
  C7  S6: r_supply/r_t = 5.8457 ± 0.002 computed from ln(1 + 1/5.36);
      [CORRECTED 2026-10-07: frozen 5.8480 was a hand-arithmetic slip;
      the exact 1/ln(1 + 1/5.36) = 5.8457.]
      MW r_supply = 71.4 ± 0.5 kpc canonical, 65.0 ± 0.5 alt.
  C8  MUTATE (T10_MUTATE=1: drift coefficient halved in the PDE — the
      substitution no longer cancels): C1 must FAIL (residual ≫ 1e-12),
      C2 must FAIL, C5 must still pass (pure algebra), C3/C4/C6/C7
      unchanged (C6 is a pure-heat bump experiment and never sees the
      drift).  [CORRECTED 2026-10-07: the original wording declared C6
      would fail under MUTATE — wrong: the bump relaxation is pure heat
      by construction; the drift enters only C1/C2. Verified empirically:
      MUTATE flips exactly C1+C2 as corrected above.]

**Deliverables:** this freeze (committed ALONE); t10_settling_flattening.py
+ .out ×2 + results ×2; README (the theorem, the falsifier, the P3-radius
corollary); Lean certificate (S2's area law M_ph = 4πμ_ph·r from the
certified deep closed form; the S3 cancellation v⁴ = GMa₀; the closed-form
mass law instances 1/(e^s−1) at the supply and half-mass radii — algebra
payload; S1's calculus substitution stays in the sympy lane, house pattern).
Language: no "theory closed"; κ stays fitted; both footings separate.