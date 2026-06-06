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

## Is it a kill? No — but the escape narrowed sharply (update, see `AEST_MASS_SCALE_two_doors.md`)

AeST's natural screening structure is its **mass term `μ²Φ`** (the feature absent in TeVeS/QUMOND). One would hope it
suppresses the solar-system quadrupole. **It cannot, by scale:** the AeST mass is `μ ≲ 1 Mpc⁻¹` (`1/μ ≳ 1 Mpc`,
pinned by the CMB/stability fit), so at 50 AU `(μr)² ~ 6×10⁻²⁰` — the `μ²Φ` term is ~40 orders down and AeST reduces
to **pure QUMOND** in the Solar System. The earlier hope ("AeST `K(𝒬)`/`μ` could screen — uncomputed, could go either
way") is **excluded** for the μ-channel.

The remaining escape narrows to the interpolation/screening parameter `β₀` (or the `χ`-field) doing something special
in the external-field configuration. But `β₀` **sets the RAR transition sharpness** — exactly the quantity Desmond
shows is too gradual for Cassini. So the Desmond tension transplants into `β₀` essentially intact. So:

- **Now computed, and it fails** (update, 2026-06-05 agent sweep): the RAR-fitting AeST interpolation β₀≈0.99 yields a
  solar-system EFE quadrupole **Q2 ≈ 1.8×10⁻²⁶ s⁻² ≈ 11× the 2026 Cassini bound** (1.6×10⁻²⁷). The β₀ that fits SPARC
  does **not** thread Cassini — so this is no longer "uncomputed, maybe evadable"; the AeST realization, at its
  RAR-fitting parameters, is **directly excluded at ~11×** unless χ/EFE subtleties (uncomputed) rescue it.
- **But the optimism is gone** — AeST's one *natural* screening scale (1/μ ~ Mpc) is ~10 orders too large to help the
  Solar System, and the surviving knob (`β₀`) is the one the RAR already pins. The casual "modified inertia evades it"
  line is *not* available to the framework, and the tension is strengthening (8.7σ → 3–15σ in two years).

## Is it generic? Yes — and it exposes a concept/realization mismatch (update)

Can the framework escape by swapping AeST for a *different* CMB-safe relativistic MOND? **Checked — no.** Two facts
from the relativistic-MOND literature settle it:

1. **Every full-fledged relativistic MOND is *modified gravity*** (AeST, RMOND, BIMOND, Khronon-Tensor). They all
   reduce to a QUMOND/AQUAL-like equation in the *stationary* weak field, so they **all** source the EFE quadrupole —
   Hees+2014 already noted Cassini "excludes a large part of relativistic MOND theories." Swapping realization does
   not swap out the quadrupole.
2. **The khronon doesn't help.** Khronon-Tensor MOND gives "order-unity corrections in *non-stationary* systems" while
   "stationary solutions remain stable to khronon perturbations" (arXiv:2302.14846) — but the Solar-System EFE is
   *quasi-stationary*, so the khronon's distinctive physics is absent exactly where Cassini bites. Same QUMOND
   quadrupole.
3. **The only escape — modified *inertia* — has no covariant completion.** It exists solely as "preliminary
   suggestions in the non-relativistic regime." There is no CMB-safe, relativistic modified-inertia theory.

**The deeper point (and it's honest, not a dodge).** The framework's *own conceptual basis* — `a₀` = the surface
gravity of the free-fall horizon, `a₀ ~ where t_dyn ~ t_cosmic` — is a **modified-*inertia*** idea (it is about the
*inertial/dynamical clock*, not the gravitational field). Modified inertia is *exactly* the class that **evades**
Cassini. But because modified inertia has no covariant, CMB-safe completion, the framework is **forced** into a
modified-*gravity* realization (AeST) that (i) doesn't match its own concept and (ii) carries the Cassini quadrupole.
**The exposure is a symptom of that forced mismatch** — the framework's natural home (modified inertia) is Cassini-safe
but doesn't exist covariantly; its available home (AeST) is covariant but Cassini-exposed. The genuine resolution is
not a better `β₀` — it is **a covariant modified-inertia theory that realizes the free-fall-clock idea directly**,
which is an open problem in the whole field, not just here. *That* is the framework's real theoretical frontier on
this front.

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
