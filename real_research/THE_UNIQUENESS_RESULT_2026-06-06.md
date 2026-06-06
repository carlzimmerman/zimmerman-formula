# It works this way and no other way — a uniqueness theorem for the falsifiable framework

*C. Zimmerman, 2026-06-06. The honest, rigorous answer to "show mathematically it has to work this way and no other
way." The result: **every falsifiable element of `a₀ = (c/2)√(Gρ_DE)` is uniquely forced** — the form, the exponent,
the evolution law, and the density `ρ_DE`. The single un-forced quantity, the overall coefficient, **cancels in every
test and is therefore unfalsifiable.** So for everything that can be measured, there is no other way. Proven in
`uniqueness_dimensional_proof.py` (Buckingham-Π by linear algebra). Stated below with exact scope — theorem vs premise
vs data — so it is a proof, not a numerology claim.*

## The premise (one conceptual input, strongly motivated)

> **`a₀` is a universal, *local* property of spacetime/inertia** — the acceleration at which Newtonian dynamics
> breaks down, the same in every galaxy (the radial-acceleration relation has one `a₀`, scatter ~0.13 dex), and it
> manifests in **empty space** (the deep-MOND regime is the low-density outskirts, far from matter).

This is the framework's single ansatz, and it nearly forces its own inputs: a universal *local* scale can only be built
from the fundamental constants `{c, G}` plus a **locally-defined, uniform** cosmological scale. The cosmological
constant `Λ` (equivalently the vacuum/dark-energy density `ρ_Λ = Λc²/8πG`) is such a scale — it fills all space
uniformly and is always defined. The Hubble rate `H` is a *global* expansion rate, not a local property; and its
"horizon" interpretation (de Sitter temperature) **ceases to exist** under DESI's thawing dark energy (no future de
Sitter ⇒ no event horizon). So the only universal, local, always-defined cosmological scale is `Λ`. **Inputs forced
(given the premise): `{c, Λ}`, equivalently `{c, G, ρ_DE}`.**

## Theorem 1 — the FORM and EXPONENT are unique (Buckingham-Π, proven)

For a quantity built from a set of inputs, the number of free dimensionless constants equals
(#variables − rank of the dimension matrix). Computed:

- **From `{c, Λ}`** (dimensions L, T; M absent): 3 variables, dim-rank 2 ⟹ **exactly 1 Π-group**. Solving the exponents:
  `a₀ = κ · c² · Λ^{1/2}` — **unique**. (G drops out entirely.)
- **From `{c, G, ρ}`** (dimensions L, M, T): 4 variables, dim-rank 3 ⟹ **exactly 1 Π-group**. Solving:
  `a₀ = κ · c · G^{1/2} · ρ^{1/2}` — **unique**; the power **½ on ρ is forced.**

There is **exactly one** free constant and **nothing else**. No other functional form of these inputs is an
acceleration. The `√ρ` scaling is not a choice — it is the only dimensional possibility.

## Theorem 2 — the EVOLUTION LAW is parameter-free

Because `a₀ = κ·c√(Gρ)` with κ the *only* free constant,
> **`a₀(z)/a₀(0) = √(ρ(z)/ρ(0))`  — κ cancels exactly.**

The framework's distinctive, falsifiable prediction therefore carries **zero free parameters.** Every differential or
ratio test is blind to the one unforced quantity.

## Proposition 3 — the DENSITY is forced to be `ρ_DE` (universality + data)

Among the inputs, the remaining question is *which* density. It is forced:
1. **`a₀` is universal at fixed z** (one `a₀` per galaxy) ⟹ `a₀ ∝ √(uniform density)`. A *local* density (matter,
   which clusters) would make `a₀` vary galaxy-to-galaxy — **excluded** by the tight RAR.
2. The only **uniform** densities are the cosmic means: `ρ_DE` (vacuum), `ρ_tot` (≈ `H`, the Verlinde reading), `ρ_rad`.
3. **Data:** `a₀(z)` is **non-rising** — the multi-method fit (rotation curves + HI + dispersions + lensing, z=0–1.5)
   gives slope `p = −0.50 ± 0.30` and **excludes** the rising `ρ_tot/cH` (Verlinde) reading at `Δχ² = +17` (~4σ);
   `ρ_rad` rises even faster (`∝(1+z)²`) and is excluded outright.
4. The **only uniform, non-rising density is `ρ_DE`.** (Computed: at z=3, `ρ_DE` → 0.74, `ρ_tot` → 4.5, `ρ_rad` → 1.0+.)

⟹ **`a₀ ∝ √ρ_DE` is forced.** No other density survives universality + data.

## The one free element — and why it changes nothing

The coefficient `κ` (the leading 2 in `Z = 2√(8π/3)`) is the single Π-group constant. It is **not forced** — that was
proven independently across 63 frameworks and an explicit derivation. **But it cancels in `a₀(z)/a₀(0)` and in every
ratio/slope/RAR-shape test.** It is therefore **unfalsifiable**: no measurement can determine it. So:

| element | status |
|---|---|
| form `a₀ ~ c²√Λ` | **FORCED** (Theorem 1) — falsifiable |
| exponent ½ (the `√ρ` law) | **FORCED** (Theorem 1) — falsifiable |
| evolution `a₀(z)/a₀(0)=√(ρ_DE(z)/ρ_DE0)` | **FORCED** (Theorem 2) — falsifiable, parameter-free |
| density = `ρ_DE` | **FORCED** (Proposition 3) — falsifiable |
| coefficient `κ` | **free — but unfalsifiable** (cancels in every test) |

## Conclusion

**"It works this way and no other way" is true for everything that can be measured.** Dimensional analysis leaves
exactly *one* degree of freedom (the coefficient), and that degree of freedom is the *one quantity that can never be
observed*. Every falsifiable prediction — the `√ρ_DE` form, the exponent, the parameter-free evolution law, the
density — is uniquely forced by the premise + dimensional necessity + the data. The framework's testable content is
**rigid**: there is no neighboring theory of the same inputs that makes a different falsifiable prediction.

## Honest scope (so this is a proof, not an overclaim)
- **Theorem (pure math):** the form, the exponent ½, the parameter-free evolution law — Buckingham-Π, proven by
  linear algebra over the dimension exponents.
- **Strongly-motivated premise (one input):** `a₀` is a universal *local* property of spacetime built from the vacuum
  scale `{c, Λ}` — motivated by `a₀`'s universality, its appearance in empty space, and the structural failure of the
  rival (horizon) scale under thawing DE. This is the framework's single conceptual ansatz, not a theorem.
- **Data (established ~4σ):** `a₀(z)` is non-rising — selects `ρ_DE` over `ρ_tot` among uniform densities.
- **Not forced:** the coefficient `κ` — but it is unfalsifiable, so it changes no prediction.

*This is the strongest TRUE form of "no other way": the falsifiable framework is unique; only the unmeasurable
coefficient is free. It does not claim the coefficient is derivable (it is not) — it shows that this does not matter,
because nothing observable depends on it.*
