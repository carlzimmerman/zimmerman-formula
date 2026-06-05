# The one calculation that matters next: AeST's quasi-static limit, worked out explicitly

*C. Zimmerman, 2026-06-05. After this verification pass, the framework's two genuine, framework-relevant exposures —
the **declining `a₀(z)`** (distinctive, telescope-limited) and the **Cassini Solar-System quadrupole** (near-term,
3–15σ, inherited via AeST) — point at the **same missing computation.** This note states it precisely, so the next
push is a defined calculation, not a hunt. Honest upfront: this is a research program (Skordis–Złošnik-level), not a
session's work — but it is *bounded and concrete*, which the coefficient hunt was not.*

## Why one calculation resolves both exposures

The framework's distinctive content (`a₀ = c²√(Λ/32π)`) is a statement about a **scale**, agnostic to whether
gravity or inertia is modified. Its **covariant, CMB-safe, ghost-free, c_GW=c** realization is **AeST**
(Skordis–Złošnik 2021): metric `g_μν`, unit-timelike vector `A_μ` (`A_μA^μ=−1`), scalar `φ`, with

```
  𝒬 = A^μ ∂_μ φ ,   Y = q^μν ∂_μφ ∂_νφ   (q^μν = g^μν + A^μA^ν) ,   F(Y,𝒬) = −K(𝒬) + (2/ℓ²)·Y·𝒥(Y) + …
```

and the deep-MOND force coming from the **`Y^{3/2}`** piece of `F`, normalized by `a₀`. Both exposures are
properties of **the same quasi-static weak-field reduction of `F`**:

- **Solar-system quadrupole.** In the quasi-static limit AeST reduces to a **QUMOND-type** equation
  `∇·[μ(|∇φ|/a₀)∇φ] ∝ ρ`, with `μ` fixed by `F`. The Milky Way's external field `g_ext ≈ 1.8 a₀` at the Sun, fed
  through this nonlinearity, sources an anomalous quadrupole `Q₂ ∝ a₀·𝒢(μ; g_ext/a₀)`. Cassini bounds `Q₂`.
- **Evolution `a₀(z)`.** `a₀` enters as the normalization of the same `Y^{3/2}` term, and is set by `K(𝒬)`
  evaluated on the **cosmological** `A_μ` (the Hubble flow). Whether `a₀ ∝ √ρ_DE` (the framework's claim) or
  `∝ √ρ_total` (the disfavored branch) is a property of how `K(𝒬)` carries the de Sitter background.

**Both are `μ`/`K(𝒬)`.** Compute the quasi-static `μ(x)` once, and you can ask both questions of the *same*
function — they stop being independent guesses.

## The calculation, in three defined steps

1. **Reduce.** Take AeST's field equations (Skordis–Złošnik 2021, Eqs. for `φ`, `A_μ`, `g_μν`) to the quasi-static,
   weak-field, low-velocity limit. Output: the explicit `μ(x)` (with `x = |∇φ|/a₀`) as a functional of `K(𝒬)` and
   the `Y^{3/2}` coefficient. *(Skordis–Złošnik sketch this; the explicit `μ(x)` for a chosen `K` is what's needed.)*
2. **Solar system → Cassini.** With the `μ(x)` that reproduces the SPARC RAR (the constraint), solve the
   external-field-perturbed two-body problem (Sun in the Galactic field) and extract `Q₂`. **Test:** is
   `Q₂ ≤ 1.6×10⁻²⁷ s⁻²` (2026 Cassini) achievable *simultaneously* with the RAR fit? If yes → the 3–15σ tension is
   an artifact of assuming a *phenomenological* `μ`; AeST's `K(𝒬)` screens it. If no → the framework's covariant
   realization is in real, quantified trouble (and would need a different completion).
3. **Cosmology → `a₀(z)`.** Evaluate `K(𝒬)` on the FRW background `A_μ = (a(t),0,0,0)`-aligned Hubble flow and read
   off how the `Y^{3/2}` normalization (hence `a₀`) depends on the background density. **Test:** does
   `a₀(z) ∝ √ρ_DE` *come out*, or must it be *imposed*? This is the difference between the distinctive claim being a
   prediction vs a parameterization.

## What each outcome would mean (stated in advance, so it can't be rationalized after)

| step 2 (Cassini) | step 3 (a₀(z)) | verdict |
|---|---|---|
| `K(𝒬)` screens `Q₂` at RAR fit | `√ρ_DE` comes out | **strong** — both exposures dissolve into one consistent `K(𝒬)`; the framework becomes a genuine *prediction* machine |
| `K(𝒬)` screens `Q₂` | `√ρ_DE` must be imposed | **viable** — Cassini-safe, but `a₀(z)` stays a parameterization (DESI still arbitrates) |
| no `K(𝒬)` screens `Q₂` at RAR fit | either | **serious** — AeST realization quantifiably fails Solar-System gravity; the *scale* idea survives but needs a non-AeST (e.g. modified-inertia) completion that doesn't yet exist covariantly |

## Honest status of *this* note

- It is **not** a result — it is a **well-posed problem**, which is the honest output of the verification work: the
  framework's open questions have collapsed from "derive the coefficient / find the TOE / which √ρ" to a **single,
  bounded `μ(x)`-from-`K(𝒬)` computation** with three defined steps and pre-registered outcomes.
- It needs tools this repo does **not** have run here: AeST's full field equations symbolically reduced, and a
  two-body EFE-perturbation solver. That is a real project — but a *defined* one, and **not** the numerology trap
  (the coefficient) we proved closed.
- Until it is done, the standing is unchanged: **not refuted; distinctive claim undecided-leaning-unfavorable; a
  near-term Cassini pressure on the realization; verdict belongs to DESI DR3 + z~3 (~2027).**

**The productive frontier is no longer a search. It is this calculation.**

**Sources:** Skordis & Złošnik 2021, *PRL* 127, 161302 (AeST) · Desmond+2024, *MNRAS* 530, 1781 (Cassini–RAR
tension) · arXiv:2602.17884 (2026 Cassini update) · `CASSINI_QUADRUPOLE_CONSTRAINT.md`,
`THE_DARK_ENERGY_TRACKING_READING.md`, `FRAMEWORK_EMPIRICAL_STANDING.md`.
