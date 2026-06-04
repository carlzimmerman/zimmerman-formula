# Comprehensive Analysis of Geometric Candidates for the MOND Coefficient

**C. Zimmerman, June 2026.** *The coefficient Z = cH/a₀ is not forced (deep geometry; pin-q; the escape). So the
honest question is: of the **principled** geometric constructions — each with a derivation, never a number chosen
to fit — which ones fulfil the requirements, and which fail? Numbers: `reviews/project_geometric_candidates.py`.*

---

## The requirements a candidate must fulfil

| # | requirement | test |
|---|---|---|
| **R1** | **Normalization** | gives a₀ ≈ 1.0–1.25×10⁻¹⁰ for H₀ ∈ [67, 73] |
| **R2** | **Sign** (deep-MOND √-law) | *common to all* — it comes from the flat-center DOS (`project_center_vs_edge.py`), not the coefficient |
| **R3** | **Evolution** | a₀ **rises** with z — MUSE-DARK III favours the apparent/Hubble horizon over constant Λ |
| **R4** | **Clean principle** | Z from a single geometric/thermodynamic derivation, *not* a fitted coincidence |
| **R5** | **H₀ consistency** | the H₀ needed for a₀ = 1.2 (H₀ = Z·a₀/c) lies in [67, 75] (the Hubble-tension range) |

R2 and R4 are entry conditions (only principled, MOND-producing constructions are admitted); R1, R3, R5 do the
discriminating.

## The scorecard

| candidate (principle) | Z | a₀@67 | a₀@73 | H₀ need | evol | R1 | R3 | R5 |
|---|---|---|---|---|---|---|---|---|
| dS surface gravity κ=cH | 1.00 | 6.51 | 7.09 | 12.4 | rise | ✗ | ✓ | ✗ |
| surface gravity at R_H (c²/2R_H) | 2.00 | 3.25 | 3.55 | 24.7 | rise | ✗ | ✓ | ✗ |
| UV/IR self-dual point | 2.00 | 3.25 | 3.55 | 24.7 | rise | ✗ | ✓ | ✗ |
| **Friedmann free-fall (c/2)√(Gρ_crit)** | **5.79** | **1.12** | **1.23** | **71.5** | **rise** | **✓** | **✓** | **✓** |
| **holographic equipartition (Padmanabhan)** | **5.79** | **1.12** | **1.23** | **71.5** | **rise** | **✓** | **✓** | **✓** |
| Verlinde volume-law (3D) | 6.00 | 1.08 | 1.18 | 74.1 | rise | ✓ | ✓ | ✓ |
| two-horizon geom mean √(H·H_Λ) | 6.36 | 1.02 | 1.11 | 78.6 | mild | ✓ | ~ | ~ |
| Milgrom thermal/Compton 2π | 6.28 | 1.04 | 1.13 | 77.6 | rise | ✓ | ✓ | ~ |
| event-horizon free-fall (c/2)√(Gρ_Λ) | 6.99 | 0.93 | 1.01 | 86.4 | const | ✓ | ✗ | ✗ |

## What the scorecard shows

**Excluded outright:**
- **Bare-horizon scales (Z = 1, 2)** — the de Sitter surface gravity (cH), the Schwarzschild surface gravity at
  the Hubble radius (cH/2), and the UV/IR self-dual point — all fail **R1**: they predict a₀ that is 2.7–5.4×
  too large, and would need H₀ ≈ 12–25 to match. The simplest horizon geometry is *not enough*.
- **The event-horizon (Λ-tracking) candidate (Z = 6.99)** — fails **R3** (it gives a *constant* a₀, which MUSE
  disfavours) and **R5** (needs H₀ ≈ 86). The cleanest *identity* (a₀ = the cosmological curvature) is the
  data-disfavoured branch — the central tension noted in the deep geometry.

**Survivors (pass R1, R3, R5):** the **Friedmann free-fall / holographic-equipartition family (Z = 2√(8π/3) =
5.79)** and the same-family **Verlinde volume-law (~6)**. Milgrom's 2π (6.28) and the two-horizon geometric mean
(6.36) pass the normalization and (mostly) the evolution but need H₀ ≈ 77–79 — marginally above the observed
range.

## The unifying structure (the real geometric content)

Every survivor has the same form:

>  **Z = 2 × (a "3D / density" factor ≈ 2.9–3.1)**,  with the factor = √(8π/3) = 2.894 (Friedmann), π = 3.142
>  (Milgrom), ≈ 3 (Verlinde volume).

Equivalently, **a₀ = (horizon surface gravity) / (3D factor)**. The bare horizon surface gravity gives Z = 1–2
(too big by ~3×); the **extra ≈ 3× is the three-dimensional density / equipartition content of the horizon**, and
*that* is why the coefficient is ≈ 5.8 rather than 1–2. The three principled versions of this factor — the exact
Friedmann density↔rate conversion √(8π/3), the thermal/Compton π, and the volume 3 — **agree to ~10%**. They are
not independent coincidences; they are three derivations of the *same* 3D structure.

## Best-fulfilling candidate

The **Friedmann free-fall (apparent-horizon) construction**,

>  **a₀ = (c/2)√(Gρ_crit) = cH(z)/Z,  Z = 2√(8π/3) = 5.789**,

is the best-fulfilling of all candidates:
- **R1** — a₀ = 1.12 (H₀ = 67), and **exactly 1.2 at H₀ = 71.5**, squarely inside the Hubble tension;
- **R3** — it ties a₀ to ρ_crit ∝ H(z)², so a₀ **rises** with z, the MUSE-favoured behaviour;
- **R4** — it is the *exact* Friedmann density↔rate conversion, the cleanest available principle (and it is what
  holographic equipartition reproduces);
- **R5** — it is the *only* survivor whose required H₀ (71.5) sits squarely in the observed range.

Notably, it ties the MOND normalization to **H₀ ≈ 71.5** — a *prediction* that lands between Planck (67) and
SH0ES (73), i.e. compatible with the Hubble tension rather than aggravating it.

## Honest limits — best-fulfilling is not forced

- The survivors are **not decisively separated by current data.** With the real uncertainties — a₀ = 1.2 ± 0.26
  (~20% M/L systematic) and H₀ = 67–73 (~10%) — the observed Z spans roughly [4.4, 7.6], which *contains every
  survivor*. The scorecard's discrimination comes from the *central values* and the evolution sign, not from a
  decisive measurement.
- So the honest status is: the requirements **decisively exclude** the bare-horizon (Z = 1, 2) and the constant
  (event-horizon) candidates, and they **single out the density/equipartition family** with Friedmann as the
  best-scoring member — but they do **not force** 2√(8π/3) over 2π or the volume-3 at the ~10% level.
- **The decider is empirical:** a ~6% absolute a₀ measurement (controlled M/L) with a pinned H₀ separates
  Friedmann (5.79, H₀ = 71.5) from Milgrom (6.28, H₀ = 77.6) from the bare values. The same ~6% a₀ measurement
  the deep geometry, the pin-q, and the escape all converged on.

## Bottom line

A geometric candidate fulfils the requirements **iff** it builds a₀ from the **apparent-horizon surface gravity
reduced by the three-dimensional density/equipartition factor** — which excludes the bare-horizon scales (too
big) and the constant-Λ event horizon (wrong evolution), and selects the Friedmann free-fall / holographic-
equipartition family, Z = 2√(8π/3) = 5.789. That is the best-fulfilling candidate on every requirement, it
predicts H₀ ≈ 71.5, and it is the cleanest principle — *and it is not forced*: the volume-law and thermal
versions agree to ~10%, and only a 6% a₀ measurement with a pinned H₀ separates them. The geometry says **which
family**; the data, when sharp enough, will say **which member**.
