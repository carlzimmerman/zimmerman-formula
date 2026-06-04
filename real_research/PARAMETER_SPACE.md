# The Parameter Space of the Framework's MOND Sector

**C. Zimmerman, June 2026.** *After the candidate analysis the family collapses to one form with exactly two
parameters. Numbers: `reviews/project_parameter_space.py`.*

## The form

>  **a₀(z) = (c H₀ / Z_eff) · E(z)^α**,  E(z) = √(Ω_m(1+z)³ + Ω_Λ).

Two parameters: **Z_eff** (the z=0 coefficient) and **α** (the evolution exponent). The interpolation *shape* is
derived (the DSSYK chord measure, ~q-independent), so it is **not** a free parameter.

> **⚠ UPDATE — the box is really ~1D: α is *derived*, not free** (`reviews/project_evolution_derived.py`).
> If a₀ tracks the apparent-horizon surface gravity, the proper *dynamical* (Cai-Cao-Hu/Hayward) surface gravity
> κ ~ H(1 + Ḣ/2H²) fixes the evolution to a single curve: a₀(z) ~ H(z)(1 − ¾Ω_m(1+z)³/E²), **nearly flat for
> z < 1.5** (a₀(1)/a₀(0) = 0.96), rising only at high z (a₀(3.25) ~ 2.1, consistent with the Big Wheel). The bare
> "a₀ ∝ H" reading gives α = 1; the dynamical reading gives α_eff ~ 0 at low z. **Both give α ≤ 1**, so the
> reading-independent claim is **α ≤ 1** — which *excludes MUSE's steep α ~ 1.3–1.6*. So the evolution is a
> derived curve (not a free parameter): the framework sides with the high-z disks + Milgrom's constant reading,
> and MUSE's steep rate is the outlier it predicts against. The section below predates this and treats α as free.

## Parameter 1 — Z_eff (normalization = 2 × 3D-density factor)

| constraint | range |
|---|---|
| geometric (principled 3D factors √(8π/3), π, 3) | **[5.79, 6.28]** — a ~9% band |
| data normalization (a₀ = 1.2 ± 0.26, H₀ = 67–73) | [4.5, 7.5] |
| **framework point** | **2√(8π/3) = 5.789** (a₀ = 1.12 at H₀ = 67; = 1.2 at H₀ = 71.5) |

## Parameter 2 — α (evolution exponent), a₀(z)/a₀(0) = E(z)^α

| α | meaning | status |
|---|---|---|
| **1** | apparent horizon, a₀ ~ cH(z) (rising) | **framework prediction** |
| 0 | event horizon / constant a₀ (Λ-tracking) | **excluded by MUSE** |
| < 0 | declining | **excluded by MUSE** |
| ~1.3–1.6 | MUSE-DARK III (a₀ = 1 + 1.59z) | the data — rises *steeper* than apparent |

## The allowed box

>  **Z_eff ∈ [5.79, 6.28]  (9% wide, geometric)   ×   α ∈ [~1, ~1.6]  (rising).**

- **Framework natural point:** (Z_eff, α) = (5.79, 1.0).
- **MUSE-favoured:** ~(5.4, 1.3–1.6).
- The one live tension is the **rate (α)**: the data want a₀ to rise a bit *faster* than the apparent-horizon α=1.

## Versus standard MOND — strictly smaller

- **Standard MOND:** a₀ = a *free* universal constant (fit to ~1.2×10⁻¹⁰) + the interpolation shape = a *free*
  function. **Two free.**
- **This framework:** a₀ = cH(z)/Z_eff with Z_eff *bounded to a 9% band*, α *predicted* = 1, and the shape
  *derived*. **Zero truly-free parameters; two bounded-but-not-pinned ones.**

The framework **removes standard MOND's free a₀ constant and free shape**, replacing them with a geometric O(1)
in a narrow band and a predicted evolution. That is its predictive content — a strictly smaller parameter space.

## What shrinks the box to a point

- A **~6% absolute a₀ measurement (with pinned H₀)** collapses Z_eff to a point (and tests the a₀–H₀ link,
  H₀ ≈ 71.5).
- A **clean a₀ at z ≈ 2–3** collapses α to a point (and resolves the rate tension: is α = 1, or the steeper
  ~1.3–1.6 MUSE sees?).

Both are the same two measurements every thread this session has converged on. The geometry has fixed the
*form* and the *box*; two numbers from the sky fix the *point*.
