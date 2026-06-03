# The geometric origin of a₀ — why MOND kicks in when it does

**Carl Zimmerman · June 2026 · a deep dive, honest to first principles.** *You asked for the geometric
reason the MOND acceleration switches on at its value, and a dimensional framework that brings it
together. There is one, it is real, and — following the mathematics rather than the hope — it leads to
the cosmic **horizon**, not the cubic T³. Reproducible: `reviews/geometric_origin_of_a0.py`.*

---

## The answer in one line

> **a₀ is the acceleration scale of the cosmic (de Sitter) horizon, a₀ ∼ cH.** MOND switches on when a
> particle's acceleration falls to where its own causal (Rindler) horizon swells to the size of the
> universe's horizon. The *order* of a₀ is geometrically forced; only the O(1) coefficient Z is posited.

Numerically: cH₀ = 6.5×10⁻¹⁰ m/s²; a₀ = cH₀/Z = 1.13×10⁻¹⁰ with Z = 2√(8π/3) = 5.789; observed
cH₀/a₀ ≈ 5.5. The horizon scale is right; the factor ~5.5 is the unpinned piece.

---

## Three independent geometric readings — all return cH

**Reading 1 — the horizon coincidence.** A particle of proper acceleration a has, by the equivalence
principle, a Rindler horizon a distance **d_R = c²/a** behind it. The universe has a de Sitter horizon
at **R_dS = c/H**. They coincide when

  c²/a = c/H  ⟺  **a = cH.**

For a ≫ cH the Rindler horizon is small and local → ordinary inertia. As a falls to cH, the Rindler
horizon swells to the cosmic horizon — the particle becomes *causally enclosed by the de Sitter horizon*,
and its dynamics must feel it. That geometric merger is the MOND threshold (Milgrom; McCulloch).

**Reading 2 — the Unruh temperature hitting the de Sitter floor.** A detector in de Sitter at
acceleration a sees (Deser–Levin 1997)

  T(a) = (ℏ/2πck_B)·√(a² + (cH)²).

For a ≫ cH this is the flat-space Unruh temperature T ∝ a (linear inertia → Newton). For a ≪ cH it sinks
to the **Gibbons–Hawking floor** T₀ = ℏH/2πk_B, and the inertia-giving excess ΔT = T(a)−T(0) ≈ a²/2cH
goes nonlinear → a = √(2cH·g_N): **MOND**. The crossover sits at a ∼ cH because that is where the
particle's own Unruh heat drops to the cosmic vacuum's temperature. This route *derives* the MOND
interpolation μ(a) = [√(a²+(cH)²)−cH]/a coefficient-free (`reviews/desitter_unruh_mond.py`).

**Reading 3 — the cosmic free-fall time (the Zimmerman form, read geometrically).** Write the surviving
relation as

  a₀ = (c/2)√(Gρ_crit) = **c/(2·t_ff)**,  t_ff = 1/√(Gρ_crit) = √(8π/3)/H = 2.89 Hubble times,

where t_ff is the gravitational free-fall time of the cosmic critical density. So **a₀ is the
acceleration that reaches c in two cosmic free-fall times.** MOND switches on when a particle is so
weakly accelerated that the cosmic medium would gravitationally *collapse* before the particle goes
relativistic — i.e. when cosmic gravity outpaces the particle's own dynamics.

All three are the same statement: **a₀ ∼ cH, the horizon scale.**

---

## The Z decomposition — both factors are geometry, not numerology

  **Z = 2 · √(8π/3) = 5.789**

- the **2** is the surface-gravity / "reach c" factor — a horizon of radius R has surface gravity c²/2R;
- the **√(8π/3) = 2.894** is the **Friedmann free-fall factor**, ρ_crit = 3H²/8πG — exact GR geometry.

The *order* of a₀ (∼cH) is forced by all three readings. The *exact* coefficient is the one posited
piece: Z = 5.79 (this form), 6 (Verlinde de Sitter entropy), 2π (Milgrom matching), or the bare 1
(naïve Unruh) are different O(1) placements of the transition, and the data say cH₀/a₀ ≈ 5.5. No de
Sitter mechanism derives the exact O(1) — that is the standing open coefficient
(`reviews/desitter_entropy_coefficient.py`: a number-field argument shows √(8π/3) cannot be
entropy-derived). **This is the honest seam: geometry fixes the scale; the coefficient is a posit.**

---

## The unifying dimensional framework — one 4D premise

Everything that survives flows from a **single** premise: *gravity is the low-energy thermodynamics of
the de Sitter horizon* (Jacobson 1995 → Padmanabhan → Verlinde). In order:

1. the horizon carries a temperature T₀ = ℏH/2πk_B and an acceleration cH;
2. MOND switches on at a ∼ cH (Readings 1–3); the form **and** the interpolation are *derived*;
3. a₀ = cH/Z ⟹ **a₀(z) = a₀(0)·E(z)** — the evolution is automatic, since cH(z) ∝ E(z);
4. the phantom halo ρ∝1/r², the BTFR v⁴=GMa₀, the Freeman scale a₀/2πG = 137 M⊙/pc² all follow;
5. the deep-MOND **sign** requires an entropy/DOF (not temperature) modification — the one open piece
   (`reviews/established_paths_to_mond.py`).

This is a **4D, horizon-based** framework. It needs no extra dimensions and no global topology. It is
the legitimate "bringing it all together": one premise (the horizon), one scale (cH), one evolving
prediction (E(z)).

---

## The cubic T³ — placed honestly

You like the cubic T³, so here is exactly what the mathematics says about it, with nothing forced.

A topology of size L has a natural kick-in acceleration c²/L. Setting c²/L = a₀ gives **L = c²/a₀ ≈ 24
Gpc = Z·R_dS.** But that is just a₀∼cH *re-stated* — L and R_dS both track the horizon — **not** an
independent derivation. And a 24 Gpc cell has inscribed radius R_i = 12 Gpc < χ_rec ≈ 14 Gpc → borderline
to excluded (the specific 20.6 Gpc cell is firmly excluded; `reviews/orbifold_matched_circles_rigorous.py`).

So the honest placement:
- **The horizon, not the cube, is the geometric source of a₀.** Both the cube scale and a₀ track R_dS,
  which is *why* they look related — but the causation is the horizon.
- A **super-horizon** cubic T³ (L ≳ 30 Gpc) can *coexist* with this picture as a global-shape choice —
  it doesn't conflict with evolving-a₀ — but it does not cause a₀, it does not produce Z (its eta
  invariant is size-independent and rational; Z²=32π/3 is a size-dependent irrational *volume*), and the
  observed isotropy forces it beyond our horizon, hence undetectable (`reviews/orbifold_isotropy_and_mond.py`).

---

## Bottom line

There **is** a geometric reason MOND kicks in when it does, and it is robust: **a₀ is the de Sitter
horizon's acceleration, cH, reached when a particle's causal horizon merges with the universe's.** Three
independent readings — horizon coincidence, Unruh-floor, cosmic free-fall time — give the same scale, and
the de Sitter–Unruh route even derives the interpolation. The one honest gap is the O(1) coefficient Z, a
posit. The cubic T³ is a separate, decoupled, super-horizon choice — keep it if you like the global
picture, but the *reason* a₀ has its value is the horizon, and that is the piece that survives every test
and unifies the rest.
