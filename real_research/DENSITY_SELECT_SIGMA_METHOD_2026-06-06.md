# A new way to measure a₀(z): select deep-MOND galaxies by DENSITY, then use the velocity dispersion

*C. Zimmerman, 2026-06-06. Carl's idea — "can we not calculate the density of the early galaxies?" — turned out to be
the right reframe, and it opens a genuinely **unoccupied** method. Worked the math + verified the pieces with a
data-gathering agent. Honest verdict: a real new method, the best route yet for using *existing* JWST data, with one
hard systematic that is the make-or-break. Script: `early_galaxy_density_deepMOND.py`.*

## The reframe (why it's new)

Every a₀(z) attempt so far chased **resolved rotation curves** V(r) — sparse, and biased to bright, compact,
**high-acceleration** galaxies that can't probe a₀. But the acceleration *regime* is set by **density**, not the
rotation curve: `g_bar = G·M_bar/R²`. Density (mass + size) is exactly what JWST photometry gives for *hundreds of
thousands* of galaxies. So:

> **Calculate the density to SELECT the deep-MOND galaxies (g_bar < a₀), then measure a₀ from the abundant INTEGRATED
> velocity dispersion σ via the deep-MOND pressure-supported relation `σ⁴ = (4/9)·G·M_bar·a₀`.**

This needs only σ + M_bar + size — *line widths and photometry*, not resolved curves. The density calculation is the
key that unlocks a much larger sample.

## The density calculation — where the deep-MOND galaxies are

Using the UNCOVER/CEERS JWST size–mass relation (R_e sub-kpc to ~2 kpc) + high gas fractions:

| z | deep-MOND threshold `logM*_dM` (deep-MOND if below) | predicted σ at threshold |
|---|---|---|
| 1 | 10.8 | 152 km/s |
| **2** | **9.6** | **85 km/s** |
| **3** | **9.0** | **60 km/s** |
| 4 | 8.5 | 46 km/s |
| 6 | 7.8 | 31 km/s |

**The sweet spot is z=2–3:** the deep-MOND population reaches `logM* ≈ 9–9.6` (the extended low-mass tail, R_e~1–2 kpc),
with predicted **σ ≈ 60–85 km/s — well above the NIRSpec grating resolution floor (~25–30 km/s) and measurable.** At
z≥6 only `logM* ≲ 7.8` is deep-MOND (σ~30, at the floor). *The method correctly rejects the massive disks that fail the
kinematic test:* de Graaff+2024's logM*~9–10 z>6 galaxies compute to g/a₀ ~ 2–10 (Newtonian), exactly their measured
high-acceleration regime.

## Two pieces verified by the data agent
- **The relation is real and calibrated.** The deep-MOND M–σ coefficient `9/4` (for σ_3D) matches the **June-2026 local
  Baryonic Faber–Jackson measurement** (arXiv:2605.26965, a₀=1.2×10⁻¹⁰, scatter 0.11 dex). Not a guess.
- **The method is genuinely unoccupied.** *Nobody has tested a₀ — let alone a₀(z) — from the high-z pressure-supported
  M–σ / Faber–Jackson relation.* Every existing a₀(z) test is rotation-curve based. This is a real, novel niche.
- **The targets exist.** KLASS lensed dwarfs (σ=18–35 km/s at logM*~8, z~1–1.5); de Graaff JADES (logM*~8, z>6);
  UNCOVER/GLASS/CANUCS lensed low-mass samples. Abundance is *ample* — JADES+lensed clusters supply hundreds of
  logM*~8–9 photometric targets.

## The binding systematic (the honest make-or-break)
At z≥2 the integrated σ is **not clean pressure support** — and σ⁴ amplifies every error:
- **Gas turbulence** adds σ_turb ~ 30–80 km/s (not gravity).
- **Partial rotation**: KLASS finds v/σ ~ 2.5; only ~16% are dispersion-dominated; `V_circ² = v_rot² + 3.4σ²`, so σ
  alone undercounts support and *misattributing* rotation to pressure biases a₀.
- **Outflows/feedback** inflate line widths (AURORA).
- Net: measured M_dyn/M_bar ~ 3–4 even where MOND predicts a modest boost, and **a 30% σ error → 2.7× error in a₀**.

To get a *clean* a₀ you must isolate genuinely pressure-supported, deep-MOND systems and correct turbulence/rotation —
which **partially reintroduces** the resolved-kinematics requirement the method was meant to avoid. So the method does
**not fully escape** the kinematics problem; it *broadens the sample* and gets the *regime selection right* (by density,
the genuinely new and correct first step), but the dispersion measurement is contaminated and must be modeled.

## Forecast and verdict
With per-galaxy a₀ error ~95% (σ⁴ amplification of a 20% turbulence-corrected σ error), the statistical reach is:

| N deep-MOND galaxies / z-bin | a₀(z) error | vs the 26% decline at z=3 |
|---|---|---|
| 30 | ~15% | marginal |
| 100 | ~8% | **decisive** |

So **~30–100 density-selected deep-MOND galaxies per z-bin with grating σ would test a₀(z=3)~0.74 vs constant** — *if*
the turbulence/rotation systematic is controlled. It's **exposure-limited (deep G395H/G235M σ), not abundance-limited**,
and it uses data JWST is *already taking* (NIRSpec gratings of lensed fields: UNCOVER, GLASS, CANUCS).

**Honest bottom line:** Carl's "calculate the density" instinct is the right move and opens a **real, novel, partially-
viable** path — the best route found yet for attacking a₀(z) with *existing/near-term* JWST data, and the first to use
density-selection + integrated σ instead of sparse resolved curves. It is *not* a free lunch: the high-z σ contamination
(turbulence + rotation) is the genuine wall, and beating it cleanly partially re-imposes the resolved-kinematics need.
But it converts "the test needs a dedicated future rotation-curve campaign" into "the test may be reachable now via a
density-selected dispersion sample, if the σ systematic can be modeled" — a meaningful upgrade, and a concrete program
(stack/forward-model σ for logM*~8.5–9, z=2–3 lensed deep-MOND galaxies). The door Carl found is genuinely **ajar**.

**Sources (verified):** UNCOVER size–mass [2412.06957]; CEERS size–mass [ApJ ad20ed]; de Graaff JADES kinematics
[2308.09742]; KLASS lensed dwarfs [MNRAS 497:173]; local Baryonic Faber–Jackson / deep-MOND M–σ coefficient
[2605.26965]; feedback-inflated σ [2501.17145].
