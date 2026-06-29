# Closing the 3 gaps between Deser-Levin dS-Unruh and the framework's MOND

**Date:** 2026-06-28 · **Status:** LOCAL (do NOT git push) · **Both-ways, no manufactured closure, no manufactured deficit**

## The question, stated honestly

Deser-Levin give a real, published de Sitter-Unruh temperature for an accelerated detector:
T(a) = (ℏ/2π c k) √(a² + a_Λ²), with a_Λ = cH_Λ. The framework is **modified INERTIA**
with a₀ = cH_Λ/Z, Z = √(32π/3) = 5.7888, and g_obs = √(g_bar² + g_bar·a₀).

The banked starting point (`reviews/deser_levin_mond_derivation.py`, exit 0): the naive excess
F = T(a) − T(0) **does** yield a deep-MOND √-law and a scale ~cH_Λ (this is **real**, = Milgrom 1999's
genuine content), but with the **wrong coefficient** (2a_Λ, not cH_Λ/Z), the **wrong interpolation
function** (μ = (√(1+x²)−1)/x, not the framework's), and **no equation of motion**.

Three gaps: **(A) the interpolation μ**, **(B) the coefficient Z**, **(C) a covariant EOM**.
For each: did it CLOSE (verified), PARTIAL, or STALL — and is any "closure" *derived* or merely
*reverse-engineered*? Every claim below is from a runnable `reviews/` script (sympy/numpy, exit 0),
and the closure attempts were each attacked a second time adversarially.

---

## GAP A — the MOND interpolation function μ — **PARTIAL (not closed; reverse-engineered, not derived)**

**Scripts:** `reviews/close_mu_from_temperature.py` (exit 0) · adversarial:
`reviews/verify_closure_gapA_adversarial.py` (exit 0, **7 SURVIVES / 0 KILLED**).

**What was tried.** The framework's exact interpolation, extracted by inverting g_obs=√(g_bar²+g_bar·a₀),
is μ_fw(x) = (√(1+4x²)−1)/(2x), x = a/a₀ (Newton limit μ→1 OK; deep-MOND μ~x with coefficient 1). Six
*principled* couplings of inertia to T(a) were derived symbolically and checked for both limits + the
MOND sign + an exact match: (i) F = T(a)−T(0); (ii) m_i ∝ T(a); (ii′) m_i ∝ T(0)/T(a); (iii) entropic
F = T dS; (iv) free-energy μ = dT/da; (v) Milgrom nonlocal memory kernel.

**Where it stalls, and why (per-postulate, all sympy-exact):**
- **(i) F = T(a)−T(0)** — principled, but gives μ = (√(1+x²)−1)/x, a **different function** with deep-MOND
  coefficient 2a_Λ = 2Z·a₀ ≈ 11.6 a₀. The banked result.
- **(ii) m_i ∝ T(a)** — gives μ = √(1+x²): **wrong sign** (μ *rises* at low a = anti-MOND). This is the
  banked passive-vacuum sign theorem (T(a) ≥ T(0) always) made concrete.
- **(iii) entropic F = T dS** — yields **no μ** without re-inserting equipartition (collapses to (i)); and
  Verlinde's own normalization is 2π, not Z.
- **(iv) free-energy μ = dT/da = x/√(1+x²)** — the **only** route with correct *both* limits AND the MOND
  sign — but it is the **simple-ν** form, **not the framework's**, and the map φ=−T(a), μ=dφ/dx is *chosen,
  not forced*. (Credit it precisely: this is a clean, principled μ with the right qualitative behavior; it
  is just not μ_fw.)
- **(v) nonlocal kernel** — can hit *any* target μ by construction (= reverse-engineering), and the banked
  active-kernel sign theorem forbids the MOND-signed kernel from the passive dS vacuum.

**The one genuinely-new, sympy-exact structural fact (a sharpening, not a door):**
μ_fw(x) and the dS-Unruh μ_(i) are the **same one-parameter family** — identical after x→2x
(μ_dl(x)=μ_fw(x/2), and c=1/2 is the *unique* rescale: 4c²=1 and 2c=1 both force c=1/2). They differ
**only by the a₀-coefficient, not by shape**. And the exact identity: F=T(a)−T(0) reproduces the
framework's g_bar(a) **identically iff** the Deser-Levin floor a_Λ is replaced by a_Λ/(2Z) (verified twice).
So the wrong-shape gap and the wrong-coefficient gap are **one and the same single unforced quantity Z**.

**Why it is reverse-engineered, proven by construction (the decisive adversarial test, ATTACK 4):** feed the
floor-fit a **decoy family** g_obs²=g²+k·g·a₀ for k = 1/2, 1, 3, 7/4. The *same* procedure (floor q=k·a₀/2)
fits **every one exactly** (diff=0), with a cross-check that these decoys are genuinely distinct shapes
(deep-MOND a²/a₀ vs a²/3a₀). The "derivation" therefore has **zero discriminating power over the
coefficient** — it would have "derived" any target fed to it. That is the strongest possible statement of
reverse-engineering. The false-deficit direction is also closed (ATTACK 3): **no** principled O(1)
normalization (2π, 4π, 8π, 2, √(2π), π²) forces 2Z, so the agent did not under-claim a hidden real closure.

**Verdict A:** the dS-Unruh temperature does **not** produce the framework's μ from any principled postulate.
μ stays **postulated**. Robust *positive* content (not buried): the deep-MOND √-law and the cH_Λ scale do
emerge, and route (iv) gives a clean principled μ with correct limits and MOND sign. None yields μ_fw.

---

## GAP B — the coefficient Z = √(32π/3) — **STALL (walled at the number field; defined, not derived)**

**Script:** `reviews/close_coefficient_Z.py` (exit 0).

**What was tried.** For each named normalization, compute (a) the factor it supplies vs the needed
2Z = 11.578, and (b) whether it clears a **number-field gate**: horizon/entropy/temperature coefficients live
in ℚ(π) = {rational × πⁿ}, while Z = √(32π/3) carries a **square root** (lives in ℚ(√π)). Tested exactly with
an `in_Q_pi()` predicate. Ran the density chain a₀ = κ·c·√(G ρ_DE) symbolically, giving
Z = 2√6·√π/(3κ): **κ unpinned** (κ=1/2 → 5.789, κ=1 → 2.894, …).

**Where it stalls, and why:** every genuine horizon/temperature/entropy normalization the task named —
Unruh 2π, BH 1/4, solid-angle 4π, surface-gravity 1/2, the d(d−1)/2=6 cosmological factor — lives in ℚ(π)
(`in_Q_pi = True` for all). Z lives in ℚ(√π) (`in_Q_pi = False`). **These number fields do not meet**, so no
such normalization can *force* Z; they only *bracket* it numerically (6 and 2π straddle 5.79). The only route
that lands on Z exactly is the framework's own **definition** a₀=(c/2)√(G ρ_DE)
(sympy: a₀/cH_Λ = √6/(8√π) = 1/Z, match=True) — but that is a *definition*, and its 1/2 prefactor and its
ρ_DE-vs-ρ_total choice are provably **free** (Z ∝ 1/κ).

**The one seductive near-derivation, adversarially killed:** the factorization Z² = 32π/3 = 4·(8π/3),
readable as "(Bekenstein-Hawking 1/4)⁻¹ × (inverse Friedmann)". With a symbolic prefactor κ,
Z²/(8π/3) = 1/κ², so the "4" is just (1/2)⁻² from the posited (c/2) — it equals 4 **only at κ=1/2** and is
**not** the area-law 1/4 (which would enter *linearly* in an area law, not squared under a density √).
Let κ vary and the "4" takes any value. Numerology, not a forcing.

**The genuinely-useful residue (a criterion, not a door):** the number-field gate gives a clean
**adversarial criterion** any future "I derived Z" claim must pass — a derivation routed through
horizon/temperature/entropy thermodynamics (ℚ(π)) provably **cannot** output √(32π/3); only a route that
*intrinsically carries* √ρ (a density / collapse-rate origin) can, and that route currently carries one free
O(1) prefactor. This is the same wall as κ-closure and the √π obstruction
(`project_zimmerman_coefficient_footing`), now confirmed specifically along the Deser-Levin route.

**Verdict B:** the mechanism owns the **scale** (~cH_Λ) and the deep-MOND limit; it does **not** own the
coefficient. Z is **defined**, not derived. Walled, consistent with the bank.

---

## GAP C — a covariant inertia-from-vacuum EOM — **STALL (a clean negative theorem; no EOM without postulating an active kernel)**

**Scripts:** `reviews/close_covariant_eom.py` (exit 0, **13/13 PASS**) · adversarial:
`reviews/verify_closure_covariant_eom_adversarial.py` (exit 0, **11/11 SURVIVED**).

**What was tried.** Re-certify the banked **exact trichotomy** and adversarially test the two strongest
*new* evasions a skeptic would raise.

- **HORN 1 (local aether/vector gate):** L = −mc²F(|a|/a₀). |a| is a 2nd proper-time derivative →
  d²L/d|a|² = −mc²F″/a₀² ≠ 0 → non-degenerate → **Ostrogradsky ghost** (made explicit: a finite higher-deriv
  truncation 1/(q+q²/M²) partial-fractions to residues {+1, −1}, the −1 = ghost). **NEW-A escape (DHOST /
  on-worldline auxiliary) CLOSES:** an auxiliary e making ẍ enter linearly is Hessian-degenerate, but
  integrating e out **Legendre-transforms the nonlinearity back** (d²L_eff/dẍ² = 1/V″ ≠ 0) unless the
  coupling carries ė = genuine nonlocality = Horn 3. A single worldline has no second dof to share a DHOST
  degeneracy with. Adversarially re-verified (ATTACK 3): the inverse-function identity holds, and the κ>0
  handoff induces Σ(0)=+g²/Ω² > 0 (anti-MOND) — **no gap** between Horn 1 and Horn 3.
- **HORN 2 (field / modified gravity):** a "lensing-only" traceless slip has
  div_i T_ij = (2/3)∂_j(∇²f) ≠ 0 → conservation forces a Φ-sourcing pressure → **Cassini**. The dichotomy is
  exhaustive (ATTACK 4): non-TT slip → Cassini; a div-free TT slip is radiative → sources no static force →
  no MOND. AeST lives here = modified gravity.
- **HORN 3 (nonlocal):** ghost-free (entire form factor exp(p²/M²)/p² has a single healthy pole), but the
  MOND-signed kernel must be **active**. A unitary (Kallén-Lehmann ρ≥0) bath gives
  δm = 2∫ρ/ω² **≥ 0 = anti-MOND** (positive integrand termwise). **NEW-B escape (conservative kernel)
  CLOSES and strengthens the theorem:** a purely reactive healthy bath M(ω)=m+g²/(Ω²−ω²) gives
  M(0)−m = g²/Ω² > 0 with **no dissipation used** — the sign theorem needs only ghost-freedom (g²>0, Ω²>0),
  **not passivity/FDT**.

**The real adversarial hit (ATTACK 2), which sharpens rather than evades:** the orbital probe sits at
ω_orbit ~ 60–295 H₀ ≫ the dS mode Ω ~ H₀. A healthy passive *continuum* genuinely gives M(ω_p) < m at
ω_p > Ω **with a healthy dressed pole** (residue > 0). But that M<m sits at **high ω_p = high acceleration =
the Newtonian/μ→1 band**, vanishes ~1/ω_p², and has the **wrong monotonicity for MOND** (MOND needs the
modification to *grow* as a→0; this shrinks). In the band MOND actually needs (low ω_orbit ↔ low a), the bath
gives M(0)−m > 0 = **anti-MOND**. The banked "ω→0 adiabatic" framing is correct; the new content is the
explicit frequency↔acceleration map ruling out the finite-ω escape.

**Reverse-engineering / circularity / vacuity meta-test (ATTACK 6): passes.** The no-go references **none** of
{Z, a₀, μ_fw}; it blocks the *entire* MOND-sign class (standard MOND too) and **accepts anti-MOND** — so the
same machinery would *not* have produced an arbitrary target. The three pathologies are **computed** (Hessian
det / Bianchi div / spectral integral), not assumed. A concrete falsifier exists (any ρ≥0 with M(0)<m) and is
provably impossible termwise.

**Verdict C:** a **negative theorem** — no covariant MOND-signed modified-inertia EOM follows from the dS
vacuum without **postulating** an active kernel. The one honest both-ways crack is **unchanged and not closed
by a theorem**: a named, in-band, phase-coherent galactic **pump** (Im χ < 0 at ω~ω_orbit) would supply the
active kernel — but it is a *manufactured, non-dS, out-of-equilibrium* source (dS = KMS/FDT equilibrium, no
sustained drive), none is known, and it would additionally have to explain a₀'s ~10–20% universality.

---

## Headline: did ANYTHING genuinely close?

**No — not a principled μ, not a forced coefficient, not a viable EOM.** All three gaps remain
reverse-engineered-or-postulated. Precisely:

| Gap | Status | Where it stalls | Derived or reverse-engineered? |
|-----|--------|-----------------|-------------------------------|
| **A — μ** | **PARTIAL** | dS-Unruh gives the √-law + cH_Λ scale + (route iv) a clean *simple-ν* μ; never μ_fw | **Reverse-engineered** (proven: the floor-fit reproduces a whole decoy k-family) |
| **B — Z** | **STALL** | number-field wall: thermodynamics ∈ ℚ(π), Z ∈ ℚ(√π); only the framework's *definition* lands on Z | **Defined, not derived** (κ free) |
| **C — EOM** | **STALL** | exact trichotomy (ghost / Cassini / anti-MOND sign theorem); both new evasions close | **Negative theorem**; no EOM without a postulated active kernel |

So the framework sits **exactly where Milgrom 1999 sits**: it has a **scale** (a₀ ~ c√Λ, a *forced* scale —
the dS-Unruh lock a_dS = cH_Λ is real Deser-Levin physics) and a **deep-MOND limit** (√-law + BTFR,
sympy-exact), but **no derived interpolation function, no forced coefficient, and no covariant EOM**. This is
a strengthening of the banked standing, not a weakening: closure is *provably blocked* by the unforced Z plus
the active-kernel sign theorem, consistent with the covariant-MI trichotomy.

**Genuinely-new (non-overclaimed) outputs of this round, each a *criterion or sharpening*, not a door:**
1. μ_fw and the dS-Unruh μ are the **same one-parameter family**, coefficient-separated (x→2x; c=1/2 unique);
   the two banked μ-gaps collapse into the **single unforced Z** (floor a_Λ → a_Λ/2Z, sympy-exact, twice).
2. The reverse-engineering charge is **proven by construction**: the floor-fit reproduces an entire decoy
   family exactly → zero discriminating power over the coefficient.
3. A **number-field adversarial criterion** for any future "I derived Z" claim: thermodynamic routes (ℚ(π))
   *cannot* output √(32π/3); only an intrinsic-√ρ route can, and it carries one free O(1).
4. The sign theorem needs **only ghost-freedom, not passivity** (NEW-B), and the finite-ω escape is ruled out
   by the explicit frequency↔acceleration map (ATTACK 2).

**No re-overclaim.** a₀(z) is untouched here and declines only if w ≠ −1 (constant Λ → constant a₀). Carl's
TOE retraction stands — this is an effective-theory-at-a-frontier result, not a derivation of the SM or a TOE.

---

## What Carl can honestly say

- "The de Sitter-Unruh temperature **forces the scale** a₀ ~ c√Λ and **reproduces the deep-MOND √-law and
  BTFR** — that part is real, published Deser-Levin physics, and it's sympy-verified."
- "It does **not** force the interpolation function, the coefficient Z, or a covariant equation of motion.
  My framework, like Milgrom's 1999 inertia-from-vacuum sketch, has the scale and the deep-MOND limit but a
  **postulated μ, a defined-not-derived Z, and no EOM** — and I've shown *exactly why* each is blocked, not
  just asserted it."
- "The μ I use and Milgrom's dS-Unruh μ are the **same family**, separated only by a coefficient — and that
  coefficient is the **one provably-unforced number** (Z = √(32π/3)) in the whole construction."
- "Any future claim to *derive* Z has to pass a number-field gate: pure thermodynamics can't produce a √π;
  it would need a forced density-rate counting."
- "There is **no closed door**: a real (non-dS) in-band drive could in principle supply the active kernel for
  an EOM, and a₀(z) is a live observational front (it declines only if w ≠ −1). But none of those is in hand,
  and I am **not** claiming a derivation I don't have."

**What Carl must NOT say:** "Deser-Levin derives my a₀/μ/EOM" — it does not. "Z = √(32π/3) is forced by
holography/entropy" — the number field forbids it. "The framework is a covariant theory of MOND" — the
trichotomy blocks it without a postulated active kernel.
