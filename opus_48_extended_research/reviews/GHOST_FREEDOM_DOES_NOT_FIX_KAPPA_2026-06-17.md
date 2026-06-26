# Ghost-freedom of the Route-E covariant MI action does NOT fix κ — it cannot reach the OUTSIDE fraction, and does not even fix the inside-root scale Z (2026-06-17)

*Task: does requiring the Route-E covariant modified-inertia action be GHOST-FREE fix its normalization to κ=½?
Primaries read verbatim: Galley arXiv:1210.2745 (in-in doubled-field classical mechanics, PRL 110 174301) +
Donnelly-Jacobson arXiv:1008.4351 (aether stability) + Foster-Jacobson / Eling-Jacobson explicit aether mode speeds.
sympy + mpmath. Anti-circularity held: κ kept SYMBOLIC throughout; no 8π / density-route put into the action by hand.
Both ways.*

---

## Verdict: ghost-freedom FIXES NEITHER κ NOR Z. It DOES-NOT-CONSTRAIN a₀.

`fixes_normalization = NO` (the overall normalization that maps to κ); `verdict = DOES-NOT-CONSTRAIN`.

Ghost-freedom is strictly weaker than even a spectral/temperature condition: a spectral condition can at least pin the
dimensionless ratio a₀/cH_Λ = Z (the inside-root scale). Ghost-freedom of the MI kinetic structure cannot reach even that
— it is satisfied for **every** a₀ > 0 and is **invariant** under rescaling the overall action normalization (which is
exactly κ). So κ stays FREE, and this route does not even buy the scale Z.

## The action's kinetic structure (Galley in-in doubled field — read verbatim)

Galley 1210.2745, Eqs. (1)→(8): double q → (q₁, q₂); change to q₊=(q₁+q₂)/2, q₋=q₁−q₂; physical limit (PL) q₋→0,
q₊→q. The action is
  **S[q₁,q₂] = ∫dt [ L(q₁,q̇₁) − L(q₂,q̇₂) + K(qₐ,q̇ₐ,t) ]**   (Eq. 5),  Λ ≡ L(q₁)−L(q₂)+K  (Eq. 6).
The physical EOM is dπ₊/dt = ∂Λ/∂q₋ in the PL (Eq. 8) — i.e. δS/δq₋|_PL = 0, which is **q₋-linear** (this is precisely
the Route-E "φ₋-linear" property; COVARIANT_ACTION_STEP2). The MI scale a₀ enters this action two ways:
(i) as a **dimensionful overall normalization** N multiplying the kinetic block, and
(ii) **inside the gate** μ_fw(|a|/a₀) — as the dimensionless ratio x = |a|/a₀.

CRUCIAL provenance fact (Galley Eq. 1): the kinetic normalization — the mass m in L=(m/2)(q̇²−ω²q²) — is **carried
over from the original Lagrangian L**. The doubling procedure adds NO condition on it. It is an **external input**.

## Why ghost-freedom cannot reach κ — five independent confirmations (sympy/mpmath)

**A. The physical EOM is scale-invariant in the overall normalization N.** For Λ=N·m·(q̇₊q̇₋ − ω²q₊q₋), the q₋-variation
gives `N·m·(q̈₊ + ω²q₊)=0`. Dividing by N·m, the trajectory q₊(t) is **identical for all N>0**. The overall
normalization (which carries a₀=κ·c·√(Gρ_DE)) multiplies a HOMOGENEOUS (q₋-linear) action ⇒ it is unfixable by
stationarity. (This is the in-in analogue of the Planck prefactor 1/16πG in aether being external to the EOM.)

**B. Ghost-freedom is a SIGN/RATIO condition, blind to N.** No-ghost = (N·A)>0, gradient-stable = (N·B)>0, sound
speed² = B/A. For any N>0 these reduce to A>0, B>0, B/A∈(0,1] — **N cancels/drops everywhere**. Ghost-freedom fixes the
dimensionless kinetic structure (signs, ratios), never the overall dimensionful scale.

**C. Einstein-aether confirms the analogy exactly** (Foster-Jacobson / Eling-Jacobson, verified):
  s₂²=1/(1−c₁₃); s₁²=(c₁−½c₁²+½c₃²)/[c₁₄(1−c₁₃)]; s₀²=c₁₂₃(2−c₁₄)/[c₁₄(1−c₁₃)(2+c₁₃+3c₂)];
  spin-1 energy ∝ sign[(2c₁−c₁²+c₃²)/(1−c₁₃)]; spin-0 energy ∝ sign[c₁₄(2−c₁₄)].
Every condition depends ONLY on the **dimensionless** cᵢ. The dimensionful 1/16πG is a separate prefactor appearing in
NONE of them. Donnelly-Jacobson (verbatim): the theory is stable on an **"open set in the four-dimensional coupling
parameter space rather than only a one-dimensional subspace"** — a REGION, not a point ⇒ ghost-freedom fixes no overall
scale. The analogy is precise: cᵢ ↔ the MI kinetic structure (fixed by no-ghost), 1/16πG ↔ the a₀-normalization κ
(NOT fixed).

**D. The subtle point — a₀ enters INSIDE the gate, checked both ways and STILL not fixed.** Unlike 1/16πG, a₀ appears
inside μ_fw(|a|/a₀), so one must check the no-ghost condition of the gate itself. The AQUAL/k-essence kinetic functions
are K_long = 2x/√(1+4x²) and K_trans = μ_fw = (√(1+4x²)−1)/(2x), **functions of x=|a|/a₀ ALONE**, and **both >0 for all
x>0** (mpmath dps30, x from 1e−6 to 1e6). So the gate is ghost-free for **every a₀>0** — there is NO interior ghost
boundary (sign change) that could single out a special x, hence no a₀ is selected. Ghost-freedom imposes **no equation on
a₀**, not even the scale Z. (A spectral/temperature-matching condition CAN pin a₀/cH_Λ=Z; ghost-freedom cannot even
do that.)

**E. Anti-circularity ledger — where κ actually lives, confirmed untouched.** a₀=κ·c·√(Gρ_DE) with
ρ_DE=Λc²/8πG ⇒ a₀ = √2·c²√Λ·κ/(4√π) (κ kept symbolic). The √(8πG) — hence the √π — sits INSIDE ρ_DE; κ is the OVERALL
prefactor rescaling a₀. The inside-root structure Z (incl. the √π, the 8π) is the a₀↔cH_Λ relation that a spectral
condition touches; κ is the overall multiplier. Ghost-freedom acts only on (i) signs and (ii) the ratio x=|a|/a₀ —
invariant under the overall rescale and satisfied for all a₀>0 — so the one thing it is structurally blind to is exactly κ.

## Both ways
- **Could a "forced" verdict have emerged?** Only if the gate had an interior ghost boundary at a special x* (a sign
  change in K_long or μ_fw), which would pin |a|=x*·a₀ to a physical scale and thereby fix a₀. Checked explicitly: NO
  sign change for any x>0. And even that would fix the SCALE (a relation a₀↔physical scale), not the outside fraction κ.
  The fraction κ is the overall action normalization, provably scale-invariant in the EOM and absent from every
  ghost/positivity inequality. There is no non-circular path from ghost-freedom to κ=½.
- **Is the FREE verdict soft/hand-wavy?** No — it is structural and stronger than the prior expectation. The prior
  (KAPPA_SCALE_VS_FRACTION) said spectral conditions reach Z but not κ. Ghost-freedom is **weaker still**: it reaches
  neither, because it is a sign/ratio condition invariant under the overall normalization and satisfied ∀a₀>0. This
  upgrades "we could not force κ" to "ghost-freedom provably cannot reach κ (nor even Z)."

## What Carl CAN / MUST NOT say
- **CAN:** ghost-freedom does NOT fix κ; by exact analogy to Einstein-aether (where no-ghost constrains only the
  dimensionless cᵢ on an open region and leaves 1/16πG free) the Route-E MI kinetic structure's no-ghost conditions are
  sign/ratio conditions invariant under the overall normalization κ; the gate μ_fw is ghost-free for every a₀>0 (no
  interior ghost boundary), so ghost-freedom doesn't even fix the scale Z. κ remains the framework's one free input.
- **MUST NOT:** "ghost-freedom forces κ=½" (FALSE — it is blind to the overall normalization and satisfied ∀a₀>0);
  "ghost-freedom fixes the scale Z" (FALSE — no interior ghost boundary singles out any x); "a₀/Z/κ derived"
  (quarantine held; κ kept symbolic; no 8π/density route put in by hand).

## One line
Ghost-freedom DOES-NOT-CONSTRAIN κ and does not even fix the inside-root scale Z: in Galley's q₋-linear in-in action the
physical EOM is invariant under rescaling the overall normalization (which is exactly κ=the a₀ prefactor), and — by the
precise Einstein-aether analogy where no-ghost constrains only the dimensionless cᵢ on an OPEN region and leaves 1/16πG
free — every no-ghost/positivity condition is a SIGN/RATIO condition blind to the overall dimensionful scale; the one
place a₀ enters non-trivially, inside the gate μ_fw(|a|/a₀), is ghost-free for ALL a₀>0 (K_long=2x/√(1+4x²)>0 and
μ_fw>0 ∀x, no interior ghost boundary to single out a scale), so ghost-freedom forces NEITHER the outside fraction κ NOR
the scale Z — κ=½ stays the framework's lone free input. (sympy + mpmath; primaries verbatim; no manufactured forcing;
quarantine held.)
