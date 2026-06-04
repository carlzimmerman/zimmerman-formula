# The Deep Geometry of a₀ = cH/Z

**C. Zimmerman, June 2026.** *What the MOND scale* is *geometrically; a geometric principle that selects it; and
the honest status of the coefficient Z. Numbers: `reviews/project_deep_geometry.py`.*

---

## The result in one screen

1. **a₀ is a horizon surface gravity.** a₀ = c²/(2R\*) is the surface gravity κ = c²/2R of a horizon at R\* =
   c/√(Gρ). Per object, the MOND radius is the **geometric mean of the Schwarzschild radius and the cosmic
   horizon**: r_M = √(GM/a₀) = (8π/3)^{1/4}·√(r_s R_H) — exact.
2. **A geometric *principle* selects the MOND scale (the new piece).** The inversion **r → r_s R_H / r** swaps an
   object's gravitational scale r_s and the cosmic horizon R_H — a UV/IR duality. Its **self-dual fixed point**
   r_sd = √(r_s R_H) is where the acceleration equals exactly **cH/2**. So **MOND is the regime where an object's
   gravity (UV) and the cosmic horizon (IR) are in geometric balance** — the self-dual radius. The *scaling*
   a₀ ~ cH is *forced* by this balance.
3. **The coefficient Z is a geometric O(1), not uniquely forced.** Simple horizon criteria give Z = 1 or 2 —
   2.7–5.4× too big against the observed Z ≈ 5.4. Matching the data needs an extra ~2.7–2.9 factor: √(8π/3) =
   2.894 (the framework's Friedmann packaging) or π/2π (Milgrom). Both fit to 6–14%; neither is forced.
   The microscopic theory (DSSYK) ties Z to its coupling (q\* ≈ 0.926), but that *predicts the coupling given Z*,
   it does not derive Z independently.

## (i) What a₀ is

The single-density form a₀ = (c/2)√(Gρ) rewrites as a₀ = **c²/(2R\*)**, R\* = c/√(Gρ): the **surface gravity of a
horizon** at R\*. Choosing ρ = ρ_crit gives a₀ = cH/Z, Z = 2√(8π/3) (the Friedmann conversion). So a₀ is, exactly,
the surface gravity of a cosmic horizon, packaged through the critical density.

The cleanest geometric expression is **per object**. The MOND radius r_M (where a galaxy/binary's internal
acceleration crosses a₀) satisfies

>  **r_M² = (Z/2)·r_s·R_H  ⟹  r_M = (8π/3)^{1/4}·√(r_s R_H)**,  r_s = 2GM/c², R_H = c/H.

For 1 M⊙: r_M ≈ 7000 AU = the geometric mean of r_s = 3 km and R_H = 14.6 Gly. The MOND scale is literally the
**geometric bridge between the smallest (gravitational) and largest (cosmological) length scales**. That a₀ ~ cH
*is* this geometric-mean statement; the two are the same fact in different variables.

## (ii) The geometric principle — MOND as the UV/IR self-dual radius

The geometric-mean structure is not just an identity; it is the fixed point of a duality. Consider the inversion

>  **r ⟼ r_s R_H / r.**

It maps the object's near-field (r_s) to the cosmic horizon (R_H) and vice versa — a **UV ↔ IR exchange**. Its
*self-dual fixed point* is r_sd = √(r_s R_H), at which the Newtonian acceleration is exactly **a(r_sd) = GM/r_sd²
= cH/2**, independent of the mass M. So there is a **mass-independent acceleration scale, ~cH, marking the radius
where an object's own gravity and the cosmic horizon are in geometric balance** — and that is precisely the MOND
regime. The MOND radius sits at (8π/3)^{1/4} ≈ 1.70× the self-dual radius (i.e. MOND switches on just *outside*
the exact balance point).

This reframes "why does MOND happen at a₀ ~ cH" from a numerical coincidence into a **balance/duality principle**:
gravity transitions where the UV (object) and IR (horizon) influences are self-dual. It is the kind of statement
that can connect to holographic UV/IR relations and dS static-patch holography — and it makes the *scaling*
geometrically inevitable. (Honest caveat: it is content-equivalent to a₀ ~ cH; its value is the *reframing*, and
the hint that the right setting is the dS static patch, not a fundamental new prediction.)

## (iii) Is the coefficient Z forced? — honest answer: no (geometrically); conditionally (microscopically)

| Geometric criterion | Z | a₀ (10⁻¹⁰) | vs observed 1.2 |
|---|---|---|---|
| Unruh T(a₀)=T_dS / de Sitter surface gravity cH | 1.00 | 6.5 | +442% |
| **self-dual point** / surface gravity c²/2R_H | 2.00 | 3.3 | +171% |
| **framework**: free-fall at ρ_crit, 2√(8π/3) | **5.79** | **1.12** | **−6%** |
| Milgrom 2π | 6.28 | 1.04 | −14% |
| event-horizon variant 2√(8π/3)/√Ω_Λ | 6.99 | 0.93 | −22% |
| **observed** (H₀=67) | **5.42** | 1.2 | — |

The honest reading:

- **The scaling is forced; the coefficient is not.** The simplest, cleanest horizon criteria give Z = 1 (Unruh /
  de Sitter surface gravity) or Z = 2 (the self-dual point) — both **2.7–5.4× too large** versus the observed
  a₀. The data demand an **extra factor ≈ 2.7–2.9** on top of the self-dual point. The framework supplies it as
  **√(8π/3) (the Friedmann density factor)**; Milgrom supplies it as **π** (his 2π). Both land within 6–14%, and
  the data (Z ≈ 5.4) cannot yet distinguish them.
- **The microscopics give Z conditionally.** In the DSSYK / Narovlansky–Verlinde reading (de Sitter = the
  spectral centre), the deep-MOND freezing slope must equal Z, tying it to the q-Gaussian band edge via Z =
  4·ρ₀(q)/√(1−q); this is reproduced at **q\* ≈ 0.926**. But q is a *free* double-scaling coupling, so this
  **predicts the coupling given Z — it does not derive Z from below.** And the identification it rests on is
  contested (the center-vs-edge dispute).
- **This is the field-wide situation, not a special failing.** The independent literature review found that *no*
  emergent-gravity framework (Jacobson, Padmanabhan, Verlinde) derives a₀'s coefficient from below — each
  *reproduces* it by fixing a horizon-DOF prefactor to general relativity. Our Z = 2√(8π/3) is one such natural
  packaging.

## What would pin Z (and is therefore the real next step)

1. **A ~6% absolute a₀ measurement** separates the candidates: 2√(8π/3) = 5.79 (a₀ = 1.12), 2π = 6.28 (a₀ =
   1.04), self-dual 2 (a₀ = 3.3). The gas-rich SPARC normalization already prefers ~1.0–1.12 over 3.3, killing
   the bare self-dual value and favouring the Friedmann/2π family — but 5.79 vs 6.28 needs better M/L control.
   (Note the H₀ dependence: with H₀ = 73, Z_obs = 5.9, nudging toward 2π.)
2. **Settling de Sitter = spectral centre** (the DSSYK center-vs-edge question) would turn the conditional Z =
   2√(8π/3) (q\* ≈ 0.926) into a derivation — or break it.

## Part II — the geometric-mean *unification*, a₀ as curvature, and the two-horizon question

Pushing further surfaces a coherent structure (numbers: `reviews/project_geometric_unification.py`).

**The geometric-mean theme runs at two levels, not one.** Not only is the *scale* a geometric mean (r_M =
(8π/3)^{1/4}√(r_s R_H)); the deep-MOND *law* is too:

>  **g_obs = √(g_N · a₀)**  (deep-MOND)  —  the observed gravity is the **geometric mean of the local (baryonic)
>  acceleration g_N and the cosmic acceleration a₀**.

So MOND is a UV/IR geometric-mean structure in *both* its scale and its dynamics. Note the law g = √(g_N a₀) is
**coefficient-clean** — Z enters *only* through a₀ = cH/Z, never the deep-MOND relation itself.

**a₀ is the cosmological curvature.** Since a₀/c² = 1/(Z R_H) is an inverse length — a curvature — the
event-horizon reading is literally

>  **a₀ = c²√(Λ/32π)   ⟺   Λ = 32π (a₀/c²)²**,

i.e. the MOND acceleration is the de Sitter curvature scale √Λ expressed as an acceleration. The galactic-dynamics
scale and the cosmological constant are **one geometric quantity** (this is Milgrom's a₀ ~ c²√Λ, made exact with
the framework's coefficient).

**Where Z² = 32π/3 legitimately lives.** The a₀–Λ conversion factor is 32π = 3Z², with Z² = 32π/3. So the
project's old number **Z² = 32π/3 — once misused to "derive the Standard Model" (numerology) — has a real home**:
it is the geometric conversion between the cosmological constant and the MOND acceleration, Λ = 3Z²(a₀/c²)².
Reclaimed from numerology to its honest geometric role.

**The sharpened two-horizon question (the payoff).** There are two horizons, giving two a₀'s that *diverge into
the past* and *converge in the de Sitter future*:

| | horizon | a₀ | evolution | status |
|---|---|---|---|---|
| **event** (global / de Sitter / DSSYK) | c/H_Λ | c²√(Λ/32π) = 0.93 | constant | the **cleanest identity** |
| **apparent** (local / Hubble / Padmanabhan) | c/H(z) | cH(z)/Z, today 1.12 | rising | what **MUSE favors** |

The high-z a₀(z) measurement sits exactly where they diverge, so it *discriminates* them — and MUSE picks the
**apparent (local)** horizon. So geometry offers the more elegant identity (a₀ = the cosmological curvature,
constant), but the **data select the local horizon** (a₀ tracks the evolving H, not the fixed Λ). The consequence
is sharp: **the framework should ground in *local* apparent-horizon emergent gravity (Padmanabhan/Jacobson), and
the DSSYK *event*-horizon derivation — though microscopically more rigorous — is tied to the constant/Λ branch the
data argue against.** Geometry sharpens the question; only the a₀(z) data answer it. This is the same conclusion
the empirical work reached, now forced by the geometric structure itself.

## Bottom line

The deep geometry we can *claim*, cleanly, is the **self-dual bridge**: a₀ is a cosmic-horizon surface gravity,
and the MOND scale is the UV/IR self-dual radius where an object's gravity and the horizon balance — making
a₀ ~ cH geometrically inevitable and tying the smallest and largest length scales through r_M = (8π/3)^{1/4}
√(r_s R_H). What we *cannot* yet claim is the **coefficient**: Z is a geometric O(1) that the simplest principles
under-shoot, fixed in the framework by the Friedmann factor but not uniquely forced — exactly as the whole
emergent-gravity literature finds. The geometry is real and elegant; the number is honest and open, and a 6% a₀
measurement or the de Sitter-centre question decides it.
