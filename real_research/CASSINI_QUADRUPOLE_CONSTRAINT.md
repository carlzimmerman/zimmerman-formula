# The Cassini solar-system quadrupole — a real, strengthening exposure the framework inherits via AeST

*C. Zimmerman, 2026-06-05. The empirical stress-test flagged this as a hardened caveat but called it "shared,
evadable by modified-inertia, AeST quadrupole uncomputed." Pursued here to its honest end — and it is sharper than
that: the framework cannot freely claim the modified-inertia escape, because its covariant realization is modified
gravity. Companion: `reviews/cassini_quadrupole_framework.py` (every number reproduced).*

## The constraint (real, recent, and getting worse)

- **Desmond, Hees & Famaey 2024** (MNRAS **530**, 1781; arXiv:2401.04796): classical **modified-gravity** MOND —
  AQUAL and QUMOND — **cannot simultaneously** fit the SPARC radial-acceleration relation (RAR) and the Cassini
  measurement of the Solar-System quadrupole. **8.7σ** under fiducial assumptions. The RAR prefers a *gradual*
  Newton↔MOND transition; the quadrupole demands a *sharp* one. They are incompatible.
- **Improved 2026** (arXiv:2602.17884): `Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻²` (40 % tighter) ⟹ the MOND boost to the
  galactic radial acceleration at the solar position is bounded to **≤ 2 % (95 %)** — against the **~30 %** the RAR
  requires. Tension now **3–15σ** depending on the Milky-Way mass model. Cassini is now a *stronger* MOND constraint
  than wide binaries.

## Why this touches *this* framework (it is not just "generic MOND")

The framework's distinctive content is `a₀ = c²√(Λ/32π)`; its **covariant, CMB-safe, ghost-free, c_GW = c**
realization is **AeST** (Skordis–Złošnik). AeST's quasi-static weak-field limit is **QUMOND-like** — it lives in the
very class Desmond constrains. So the framework, *in its preferred realization*, is exposed to the 3–15σ tension.

**Grounding** (order-of-magnitude; the full quadrupole integral is in the cited papers). The Milky Way's external
field at the Sun is `g_ext = V²/R ≈ 2.15×10⁻¹⁰ m/s² ≈ 1.8 a₀`. The standard interpolating functions that fit the RAR
give there:

| a₀ | g_ext/a₀ | boost ν−1 (RAR) | boost (simple) | vs Cassini ≤ 2 % |
|---|---|---|---|---|
| canonical 1.20e-10 | 1.79 | **36 %** | 40 % | ✗ in tension |
| **framework 0.936e-10** | 2.29 | **28 %** | 33 % | ✗ in tension |

The framework's a₀ is ~22 % *lower* (the footing-corrected value), which pushes the Sun marginally deeper into the
Newtonian regime and shaves the boost 36 %→28 %. **It helps a little; it does not clear a multi-σ tension.**

## The realization dilemma (the honest core)

The framework cannot have it both ways:

- **Modified inertia** (Milgrom 1994/1999) — the framework's working "Layer 0" (de Sitter–Unruh, fits SPARC at 0.105
  dex) — has a *different* solar-system phenomenology and **can evade** the Desmond constraint (Desmond explicitly
  bounds modified *gravity*). **But there is no covariant, CMB-safe modified-inertia completion** — that is a famous
  open problem, and it is *not* AeST.
- **AeST** (modified gravity) gives the framework its covariance, its CMB-safety (the `Ȳ=0` saddle-blindness), its
  GW speed and ghost-freedom — **but it is the constrained class**, so it inherits the 3–15σ quadrupole tension.

The two desiderata pull apart: the property that makes the framework CMB-safe and covariant (AeST/modified gravity)
is the property that exposes it to Cassini; the property that would evade Cassini (modified inertia) has no covariant
completion. **This is a genuine tension in the framework's realization story, not a cosmetic one.**

## Is it a kill? No — but the escape is uncomputed, not free

AeST carries a free function `K(𝒬)`. In principle a `K(𝒬)` with a sharp-enough feature can **screen** the
solar-system fifth force (suppress the quadrupole) — AeST has the freedom. The question is whether the **same**
`K(𝒬)` that reproduces the gradual RAR transition *also* satisfies the sharp Cassini quadrupole. That is precisely
the Desmond tension transplanted from phenomenological MOND into AeST — and **it has not been computed**. Skordis–
Złošnik checked PPN consistency, but not the joint RAR+Cassini-quadrupole fit under the 2026 bound. So:

- **Not excluded** — AeST's `K(𝒬)` freedom is a real, untested escape hatch.
- **Not safe** — the casual "modified inertia evades it" line is *not* available to the framework, and the tension is
  strengthening with data (8.7σ → 3–15σ in two years).

## Disposition — a SECOND framework-relevant exposure

The framework now has **two** real, non-fatal, framework-relevant exposures, and they point at the **same** missing
calculation:

1. **Declining `a₀(z)`** (the distinctive claim) — undecided-leaning-unfavorable; needs AeST's quasi-static limit at
   **high z**.
2. **The Cassini quadrupole** (this note) — a 3–15σ shared-but-inherited tension; needs AeST's quasi-static limit in
   the **solar system** (does the RAR-fitting `K(𝒬)` screen `Q₂`?).

Both are honest liabilities of the *realization*, not of the core idea `a₀ = c²√(Λ/32π)` (which is a statement about
the *scale*, agnostic to inertia-vs-gravity). The clean way to state the framework's standing: **the scale-from-Λ
claim is intact; the covariant realization (AeST) that makes it CMB-safe also owes a solar-system-quadrupole
calculation it has not paid, and the bill is rising.** This belongs in `FRAMEWORK_EMPIRICAL_STANDING.md` §4 as a
hardened caveat, and in `FALSIFICATION_MATRIX.md` as a near-term, data-driven (not telescope-limited) test —
the one place the framework could be pressured *without* waiting for z~3.

**Sources:** [Desmond, Hees, Famaey 2024, MNRAS 530, 1781 (arXiv:2401.04796)](https://arxiv.org/abs/2401.04796) ·
[Improved Cassini constraints 2026 (arXiv:2602.17884)](https://arxiv.org/abs/2602.17884) ·
Skordis & Złošnik 2021, PRL 127, 161302 (AeST).
