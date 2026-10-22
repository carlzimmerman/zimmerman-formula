# A46 mutations

Two deliberate falsifications of the A46 pipeline, each `exit 1`, each logged to
`a46_MUTATE_<name>.out`. Both are run with the same data, same priors and same three-parameter
fits as the production run; only the named assumption changes. They exist to prove that the
passes in `a46.out` are not vacuous — that the checks *would* fail if the physics were wrong.

## `beta0` — take "β = 0" literally (A42's own premise)

A42's title case is "β = 0, Λ_bare = 3H₀²/c²". Taken literally in (F1), β = 0 gives
`H² = Λ_bare c²/3 = H₀²`, i.e. pure de Sitter with **no matter term at all**: `Ω_m = 0`,
`H(z) = H₀` for every z. The mutation sets the model's `E(z) ≡ 1`.

Result: **12/17 PASS, exit 1.** The five failures are exactly the checks that test whether the
model is a cosmology at all:

| check | production | `beta0` | why it fails |
|---|---|---|---|
| K5 | 0.0033 | **341.45** | `D_M/r_d`, `D_H/r_d`, `R`, `l_A` are off by 340×; `Δχ²_SN = 660` |
| K17 | 4.5e−5 | **0.99996** | `E_model/E_ΛCDM − 1 ≈ −1` — the model has no matter |
| K7 | 0.065 | **1.42e9** | `Δχ²(model − ΛCDM)` is 10⁹, not ~0 |
| K8 | 1.007 | **2.68** | the fit runs to `Ω_b h² = 0.060` (the box edge), trying to fake the matter |
| K16 | 0.962 | **0.525** | the fit lands at `H0 = 30`, because there is no `(1+z)³` to fit |

The best fit is `χ² = 2.18×10⁹` at `Ω_m = 0.02, h = 0.30` (both box edges). This is the
mutation that reproduces A42's §1 conclusion — β = 0 is not a cosmology — and shows the
pipeline detects it as a 10⁹ χ², not as a 10σ parameter shift.

## `fixed_rd` — assume the ΛCDM ruler instead of computing it

The production model computes `r_d` and `r_*` from its **own** `H(z)` (Hu–Sugiyama `z_*`,
Eisenstein–Hu `z_drag`, one-point calibrated at Planck). The mutation instead **fixes**
`r_d = 147.09 Mpc` and `r_* = 144.43 Mpc` — the Planck/ΛCDM values — for the model as well,
so the model is never allowed to have a different sound horizon.

This is the single most important mutation, because the whole A46 result is that the model's
`r_d` is 20% larger at fixed physical densities. If that were an artefact of the ruler
calculation, fixing the ruler would restore agreement. It does not.

Result: **11/17 PASS, exit 1.** Six failures:

| check | production | `fixed_rd` | meaning |
|---|---|---|---|
| K5 | 0.0033 | **0.1999** | the degeneracy is broken at 20% once `r_d` is pinned |
| K6 | 1.2009 | **0.9978** | the model's ruler collapses to ΛCDM's by construction |
| K9 | 0.842 | **1.018** | `a0` from the best-fit `H0 = 68.61` is `1.152e-10`, i.e. the *alt* footing, not canonical |
| K10 | 58.8 | **14.2** | fixing `H0 = 67.40` now costs only `Δχ² = 14.2`, not 58.8 |
| K12 | 1.155 | **1.000** | `r_d` at the `a0` branch is exactly the BAO value — no tension left |
| K16 | 0.962 | **1.201** | `H0`(fit)/`H0`(map) is 1.20, not `√(1−Ω_m) = 0.835` |

The interesting failure is **K9**: with the ruler pinned, the fit prefers `H0 = 68.61`, which gives
`a0 = 1.152×10⁻¹⁰` — closer to A42's `1.1312e-10` than to the canonical `9.36e-11`. That is the
one configuration in which A42's `a0` survives, and it survives by **discarding the model's own
sound horizon** — i.e. by not being the model. It is recorded here so the reader can see that
the `a0 = 1.1312e-10` branch is reachable only at the price of the theory's own prediction for
`r_d`, and that the honest fit (production) selects the canonical footing instead.

## What the mutations establish

1. **The 17/17 in `a46.out` is not a tautology.** Both mutations fail loudly and in the checks
   that are supposed to catch them, not in unrelated ones.
2. **The two branches are distinguishable.** `beta0` (no matter) fails by 10⁹ in χ²; `fixed_rd`
   (ΛCDM ruler) fails by 20% in the distance ratios and drifts `H0` to 68.6. Neither is a
   small perturbation of the production fit.
3. **The production result is the model's own**, computed with its own `E(z)` and its own
   `r_d`, not with ΛCDM's pasted in.
