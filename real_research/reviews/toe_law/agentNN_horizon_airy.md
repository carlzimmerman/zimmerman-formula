# agentNN — Banking memo: the heat-kernel / turning-point Airy mechanism for Link 5's generator

**Question.** MM (fb0ff706) proved the GENERIC/FREE pump fluctuation operator at the edge b→c_χ lands
NON-Airy (simple-pole / Rayleigh-Jeans, forward slope −1, not −1/4). Link 5 needs the negative-argument
Airy (index-1/3) normal form so that σ_req ~ e^{−ζ̃ u^{−1/4}} is FORCED rather than transcribed. Two
routes asked: can a turning-point / caustic mechanism on the pump's own fluctuation kernel Ψ promote the
free non-Airy edge to the Airy class — and if so, naming exactly the operator the pump must carry?

**Coefficient quarantine held throughout.** ζ̃, (16π/3)^{1/4} never entered any route; the q=1/4 ⟺
index-1/3 agreement is the QUARANTINED requirement-match (LL/V), never an independent consistency check.

---

## The two routes, each counted at its VERIFIED grade

### Route 1 — WKB / Langer turning point on the khronon sound-mode equation → **CONFIRMED / DIRECTION-NARROWED**

- Cast the khronon worldline pullback (W_b ∝ 1/sinh²(κτ/2)) into Schrödinger form: reduced sound-mode
  equation is hyperbolic Pöschl–Teller −ψ″+[s(s−1)κ²/(4sinh²ξ)]ψ = ν²ψ (s=2 conformal khronon).
- A LINEAR turning point IS present in the FREE khronon (simple zero of V−ν², (V−ν²)′(ξ*) ≠ 0), but its
  GLOBAL connection across the symmetric two-sided 1/sinh² barrier is the Γ-function THERMAL S-matrix
  |Γ(iν/κ)|² = π/(ν sinh(πν/κ)), tail d/dν log = −π/κ ⇒ **index 1 (Rayleigh-Jeans / KMS), slope −1** —
  machine-confirmed, **reproducing MM independently**. Sonic-edge family measure A(b) ∝ 1/(c_χ−b) is a
  simple pole (q=0).
- The free group velocity dω/dk = c_χ is CONSTANT (never zero) ⇒ the free theory has **NO turning-point
  degeneracy and NO fold** — the index-1/3 Airy is gated behind a named, unbanked input the free operator
  genuinely lacks.
- **Verifier (CONFIRMED):** free-vs-pump distinction holds and is load-bearing, not a relabel. One LOOSE
  non-load-bearing prose mislabel ("z(w)~w^{2/3}") flagged, no verdict impact; q=1/4 left honestly OPEN.

### Route 2 — Heat-kernel / proper-time (Schwinger) on Ψ → **CONFIRMED / MECHANISM-CANDIDATE**

- Edge class = saddle type of the worldline phase Φ(z;w) = w·z − S(z). FREE = Gaussian/quadratic
  (K_free ~ s^{−1/2}; sinh^{−2} = double-pole Matsubara tower, Boltzmann tail index 1) ⇒ simple-pole /
  Rayleigh-Jeans edge = **MM, reproduced three independent ways**.
- A FOLD (Φ′=Φ″=0, Φ‴≠0) gives the cubic normal form = Airy turning point, index 1/3. The b→c_χ edge is a
  PARAMETER pole 1/(c_χ²−b²) (a wrong-variable coalescence) — it multiplies the kernel and CANNOT be the
  caustic by itself.
- **Verifier (CONFIRMED):** firewall holds at full generality — the most general 2-derivative dispersion
  ω=√(a+b k²) has ω″ = a·b/(a+b k²)^{3/2} > 0, strictly convex, NO inflection; the luminal line ω=c₀k has
  ω″≡0 (degenerate cone → simple-pole edge); the sinh^{−2} Matsubara double pole fits a SIMPLE exponential,
  provably not a fold. So the Airy is genuinely pump-specific, NOT MM's free turning point smuggled back.

---

## Independent reproduction this round (compute-first; all clean)

| object | claim | independent check | status |
|---|---|---|---|
| Airy cubic integral | (1/π)∫₀^∞ cos(k³/3+wk)dk = Ai(w) | proper oscillatory quadrature, w=±1,±2,0 | rel ~1e-36 ✓ (NN: ~1e-31) |
| index ↔ measure map | 2q/(2q+1)=1/3 ⟺ q=1/4 EXACTLY | sympy solve | exact 1/4 ✓ |
| turning-point index law | m/(m+2): m=1→1/3 | sympy | exact ✓ |
| FREE firewall | massive/general-2-deriv ω″ > 0, no real inflection | sympy: ω″=a·b/(a+b k²)^{3/2}, roots=∅ | convex, no fold ✓ |
| luminal degeneracy | massless ω=c k has ω″≡0 (cone, not isolated turning point) | sympy | ≡0 everywhere ✓ |
| ROTON fold exists | ω=√(c²k²−αk⁴+βk⁶) has ω″(k*)=0, ω‴≠0 | sympy+mpmath findroot | k*≈3.286, ω‴≈38.7 ≠0 ✓ |

The √3 lock (Im/Re = ±√3 exact, cube-root saddle triad) and the Pöschl-Teller Γ-function thermal S-matrix
(rate −π) are reproduced in the route+verify files (agentNN_routeHK.*, agentNN_verify_*); both are
internally consistent with the recompute above.

---

## OVERALL VERDICT — **MECHANISM-CANDIDATE (named operator), not a derivation**

Counted at verified grades: Route 1 = DIRECTION-NARROWED, Route 2 = MECHANISM-CANDIDATE. The higher of the
two governs the round only because Route 2's CONFIRMED firewall establishes the Airy is **genuinely
pump-specific** — but it is a CANDIDATE, NOT a confirmed mechanism: both routes leave the index-1/3 lock
gated behind undischarged conditions. **No Airy was wished in; no fourth-root was smuggled closed.**

**The named operator the pump must carry (the two routes' convergent shape):**
> A **sign-indefinite higher-derivative (roton) kinetic term** in Ψ — schematically **−α(∂_iχ)∂²(∂^iχ)**
> (a k⁴ contribution with the dispersion-**bending** sign), stabilized by a **+β k⁶** sextic floor — which
> creates an isolated in-medium dispersion **inflection ω″(k*)=0, ω‴(k*)≠0** (a fold/caustic). This is a
> modification of the **DISPERSION RELATION (dynamics)**, NOT a state and NOT a constant gain — exactly the
> dynamics-modifier EE-3.2/MM relocated the answer to (the active pump's own kernel Ψ). The free operator
> has only Gaussian saddles (Route 2) inside a symmetric thermal Pöschl-Teller barrier (Route 1) and
> provably cannot supply the fourth-root fold alone.

**Undischarged conditions that keep this a CANDIDATE (the verifier's three, named):**
1. **Existence** — the sign-indefinite k⁴(+k⁶) term must actually be present (absent from any free
   2-derivative action). *Genuine non-free win; uncomputed whether the pump generates it.*
2. **Edge-coincidence (tuning)** — ω″(k*)=0 must land AT the dominant worldline saddle for the b→c_χ edge
   frequency. An untuned k⁴ gives a generic fold at the *wrong* frequency, not the edge. **This is the
   named unbanked physical input** where a dS-bath / horizon-heat-kernel mechanism must act.
3. **Oscillatory-side selection** — the edge must probe the OSCILLATORY Ai(−w) side (index 1/3), not the
   decaying Ai(+w) tunneling tail; a second tuning NN compressed into the single word "coincidence"
   (sign(ω‴)=+1 fixes the allowed side).

A fourth, decisive gap: even granting existence+coincidence, that the resulting edge measure is the
SPECIFIC q=1/4 fourth-root (not another power) requires the dispersion scale to soften with a particular
edge exponent — **deriving ρ(b) is left honestly OPEN by both routes**, not asserted.

---

## Relation to MM's NEEDS-NEW-INPUT — **this SHAPES the new input (it does not just re-confirm the gap)**

MM proved a generic turning point already present in the free theory cannot be the answer. This round does
**not** overturn MM — it **reproduces MM independently on two new sides** (Route 1: free turning point is
thermal/Γ-function, rate −π; Route 2: free saddles are Gaussian, dispersion convex with no inflection) and
then **converts MM's unstructured "needs-new-input" into a SHAPED new input by naming the exact operator**:
a sign-indefinite roton k⁴(+k⁶) higher-derivative kinetic term on Ψ, fold-tuned to the edge resonance. MM
said "the pump must add *something*"; this round says "the pump must add *this dispersion-bending
higher-derivative operator*, and here are the three conditions it must satisfy." That is strict progress —
a falsifiable target — while remaining short of a derivation.

**Link-5 update (one sentence):** σ_req ~ e^{−ζ̃ u^{−1/4}} is still FREE INPUT, but its missing mechanism is
now SHAPED — the pump must carry a sign-indefinite roton higher-derivative kinetic term (−α(∂χ)∂²(∂χ)+β k⁶)
whose dispersion inflection ω″(k*)=0 is tuned to coincide with the b→c_χ edge, promoting the free
Gaussian/thermal simple-pole edge to the negative-argument Airy (index-1/3) class.

**Single next calculation:** Compute the in-medium khronon self-energy / dispersion correction from the
named dS-bath / horizon-heat-kernel mechanism and test (a) the generated k⁴ coefficient carries the
dispersion-BENDING sign with a k⁶ stabilizer (existence), AND (b) the inflection ω″(k*)=0 lands at the
b→c_χ edge resonance on the Ai(−w) oscillatory side (coincidence) — if both hold, derive ρ(b) and confirm
it is the q=1/4 fourth-root e^{−γ(c_χ−b)^{−1/4}} with γ_req; if the correction comes out convex
(positive/zero k⁴), the route lands non-Airy and MM's kill stands.
