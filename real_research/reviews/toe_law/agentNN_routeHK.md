# agentNN — Route 2: Heat-kernel / proper-time. Does the pump operator's proper-time exponent go CUBIC at b → c_χ?

**Question (pre-registered):** The Airy function arises in heat-kernel/proper-time expansions
when the s-integral (or its momentum partner) has a **cubic degeneracy** — a coalescing-saddle /
caustic — instead of the usual Gaussian (quadratic) saddle. Determine whether the pump fluctuation
operator Ψ's proper-time exponent presents such a cubic degeneracy at the edge b → c_χ. Show the
FREE case lands quadratic/Gaussian (= MM's non-Airy, Watson/Rayleigh-Jeans edge). Then name the
EXACT active-pump operator term that promotes quadratic → cubic.

**Standing kill to beat (agentMM, fb0ff706):** the GENERIC/FREE pump fluctuation operator at the
edge lands NON-Airy — simple-pole / Rayleigh-Jeans, forward slope −1 not −1/4. A generic turning
point already present in the free theory CANNOT be the answer. The active pump must supply something
the free operator lacks.

**Coefficient quarantine:** ζ̃, (16π/3)^{1/4} never appear. Pure structure / pure numbers only.

---

## NN-1 — The free worldline kernel is GAUSSIAN/quadratic (reproduces MM)

Free pullback (EE STEP 3 / LL S4 banked): G_b(τ) = −H²/[16π² c_χ (c_χ²−b²) sinh²(κτ/2)].

- **[NN-1a]** Heat kernel of the free quadratic dispersion ω² = c_χ² k²:
  K_free(s) = ∫dk/2π e^{−s c_χ² k²} = 1/(2√π c_χ √s) — a **half-integer power s^{−1/2}**,
  the signature of a **Gaussian (quadratic) saddle** in the momentum integral. Standard heat-kernel
  short-time class.
- **[NN-1b]** The thermal worldline kernel sinh^{−2}(κτ/2) is the Mittag-Leffler **double-pole
  Matsubara tower** Σ_n 1/(κτ/2 − iπn)² (machine: rel.diff ~1e-30 at x=0.7). Its frequency transform
  is w/(e^{2πw/κ}−1): **Boltzmann tail e^{−2πw/κ}, index 1, Gevrey-1.** This is exactly MM's /
  LL-3(iii)'s kill object — a quadratic-saddle / Rayleigh-Jeans edge.

**Free = quadratic, confirmed.** No cubic degeneracy anywhere in the free proper-time exponent.

---

## NN-2/3 — The caustic condition, built and verified

**The hierarchy (catastrophe-optics applied to the in-medium dispersion):** the spectral edge
class is set by the saddle structure of the worldline phase / proper-time integral
Φ(z;w) = w·z − S(z), saddles at Φ′(z*)=0:

| saddle structure at the dominant z* | normal form | edge class | index | machine |
|---|---|---|---|---|
| nondegenerate Φ″≠0 (Gaussian) | quadratic | van Hove √-edge / simple pole | **1/2** (or pole) | DOS slope **−0.500000** [NN-3a]; K_free ~ s^{−1/2} [NN-1a] |
| **TWO saddles coalesce: Φ′=Φ″=0, Φ‴≠0 (FOLD)** | **cubic** | **Airy turning point** | **1/3** | (1/π)∫cos(k³/3+wk)dk = Ai(w) to **rel 1e-31** [NN-3b] |

- **[NN-3b]** The cubic stationary point IS the Airy integral, machine-exact (rel ~1e-31 at
  w=±1,2, w=0). Negative-argument Airy amplitude index −1/4 confirmed [NN-3c].
- **[NN-6]** Honesty tie (exact arithmetic, robust — no fragile improper quadrature): the cubic
  fold's split-cubic exponent Φ = w s² − iβ/s has the **cube-root saddle triad**; the two
  admissible (Re>0) saddles carry **Im/Re = ±1.7320508076 = ±√3 EXACTLY** (match=True), the third
  (growing, phase π) is one-sidedness-excluded. **This is LL-1e's √3 ⟺ k=1/2 ⟺ index-1/3 lock,
  reproduced from the fold.** (The Laplace-image closed form 2·3^{1/3}e^{−w^{1/3}/2}cos((√3/2)w^{1/3})
  is LL-2.2, banked; not re-claimed here — the saddle lock is the robust statement.)

## NN-4 — The MM discriminator: the edge b→c_χ CANNOT be the caustic by itself

The kill to beat is precise: the generic edge is already-present and non-Airy. NN-4 confirms WHY,
and where the real degree of freedom is:

- **[NN-4a]** The edge b→c_χ is a **PARAMETER pole** in the Deser–Levin amplitude 1/(c_χ²−b²) — a
  simple pole in the b-parameter (slope −1, MM's machine −1.000000). It **multiplies** the kernel;
  it does **not** alter the saddle structure of the τ/k integral. **A coalescence in the wrong
  variable** — it cannot be an Airy turning point.
- **[NN-4b]** An Airy edge needs a **coalescing saddle in τ/k**, i.e. an **inflection of the
  in-medium dispersion** ω″(k*)=0 at the dominant saddle. Machine-checked: **neither the massless
  ω=c_χk nor the massive ω=√(c²k²+m²) has any real finite inflection** (ω″ = c²m²/(...)^{3/2} > 0,
  convex everywhere). **The free/massive operator has only Gaussian saddles → Watson/Rayleigh-Jeans
  simple-pole edge. MM holds, reproduced from the saddle side.**

## NN-5 — WHAT THE PUMP MUST ADD (named, exact)

The free operator lacks exactly one thing: a dispersion **inflection** to coalesce two saddles into
a fold. The pump must supply it.

- **[NN-5a]** A convex-bending quartic ω=√(c²k²+αk⁴) (α>0) still has **no inflection** — a positive
  k⁴ does not bend the dispersion the right way.
- **[NN-5b]** A **sign-indefinite (roton) dispersion** ω=√(c²k²−αk⁴+βk⁶) (the k⁴ term with the
  **bending sign**, k⁶ stabilizing) **DOES have a real inflection** — machine: ω″(k*)=0 at
  **k*≈3.29** for the test case. **This dispersion can host an Airy turning point.**

**THE NAMED OPERATOR:** the active pump must add to Ψ a **sign-indefinite higher-derivative kinetic
term** that bends the in-medium khronon dispersion **non-monotonically (roton-type)** — concretely a
quartic-momentum operator of schematic form **−α (∂_iχ)∂²(∂^iχ)** (a k⁴ contribution with the
dispersion-bending sign), stabilized by a **+β k⁶** (sextic) floor — **TUNED so that the in-medium
dispersion's inflection ω″(k*)=0 (with ω‴(k*)≠0) sits exactly at the dominant worldline saddle for
the edge frequency** (the fold/caustic-coincidence condition).

This is precisely the object EE-3.2's Bogoliubov lemma already demanded — **a dynamics modifier
(in-medium dispersion/gain), not a state filler** — now pinned to its exact analytic shape: a
**roton inflection coincident with the spectral edge.** Two conditions, not one:
1. **Existence** of the inflection: the sign-indefinite k⁴ (+k⁶ floor) — a higher-derivative kinetic
   operator absent from the free khronon action.
2. **Coincidence** (tuning): ω″(k*)=0 at the edge resonance — an untuned k⁴ gives a generic fold at
   the wrong frequency, not the edge. This second condition is the unbanked physical input (what sets
   the inflection scale to the edge); it is where a dS-bath / horizon-heat-kernel mechanism would have
   to act.

---

## VERDICT

**turning_point_class found at the FREE level: QUADRATIC (Gaussian saddle) → simple-pole /
Rayleigh-Jeans edge.** Machine-confirmed three independent ways: K_free ~ s^{−1/2} [NN-1a]; sinh^{−2}
= double-pole Matsubara tower, Boltzmann tail index 1 [NN-1b]; massless & massive dispersions have
**no inflection** [NN-4b]. **This is MM's kill, reproduced on the heat-kernel/proper-time side.**

**A LINEAR (Airy / index-1/3) turning point IS available structurally — [NN-3b] machine-exact, [NN-6]
√3 lock exact — but ONLY if the pump supplies a dispersion inflection.** It is NOT already present in
the free theory (so it does not fall to MM's "generic turning point" objection), and the b→c_χ edge
pole is the **wrong-variable** coalescence [NN-4a] that cannot supply it.

**MECHANISM-CANDIDATE, conditional and named:** the route gives a CONCRETE, falsifiable operator
requirement — a sign-indefinite higher-derivative (roton) kinetic term, fold-tuned to the edge — that
the free operator provably lacks. The route does NOT derive that this term is present or so tuned; the
**coincidence condition** (ω″(k*)=0 at the edge resonance) remains the named unbanked physical input,
consistent with the standing fb0ff706 ledger (a banked dS-bath/horizon-heat-kernel mechanism must
force it). The firewall held: ζ̃, (16π/3)^{1/4} never entered; the q=1/4↔index-1/3 agreement is the
quarantined REQUIREMENT match (LL), not re-used here.
