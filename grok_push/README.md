# grok_push — the two-branch Einstein theory

Write-only folder for this track. Reads the rest of the repo; does not modify it.

## The theory (K001)

Gravity is Einstein's. The dark sector is L247's constitutive fluid
`p = P(a)`, `a^μ = u^ν ∇_ν u^μ`, with `P` matched to the SPARC-selected
kernel `μ₂`. Lean `medium_branch_dichotomy` splits the self-consistency
identity into exactly two branches:

| branch | kinematics | what it carries |
|---|---|---|
| **(F) free fall** | `a = 0`, `p = 0` | CMB third peak, clusters, forest, KiDS lensing, `Ω_dm` |
| **(S) supported** | `a' = −K ρ` hydrostatic | the RAR, SPARC discs; Cassini-inert because the Sun is not at rest here |

L248 killed (S) as the *source* of the KiDS weak-lensing RAR. Under two
branches that kill is a **prediction**: the MW cap sits at 5.8 kpc and
KiDS begins at 35 kpc (L248 `v6_frac = 0`).

## What K001 measured (7/7, 155 SPARC curves, both `a₀` footings)

- Median `M_S / M_bar` = 2.95 / 3.34 (canonical / alt). Pre-registered
  halo-kill was median > 20. Does not fire. Disc-scale, not a halo.
- Cosmic split: `f_S = Ω_(S)/Ω_dm ∈ [0.027, 0.064]`. Kill was `≥ 0.10`.
  (S) is a **trace** of `Ω_dm`, not a cosmological component.
- 153/155 SPARC last-points sit outside `r_M` (median `r_M/r_last = 0.25`).
  (S) is in the rotation-curve window.
- MW identification total / `M(<100 kpc)` = 0.060 (16.8× shortfall) —
  PAPER29's one-component failure is this theory's local split.
- L248 cap 5.80 kpc vs first KiDS bin 35 kpc, factor 6 inside, frac = 0.

## Lean (`lean/K001_two_branch.lean`)

8 theorems, `lake env lean` exit 0, zero sorry, axioms
`{propext, Classical.choice, Quot.sound}` only:

`branch_dichotomy`, `free_fall_pressureless`, `supported_mass_formula`,
`truncation_is_supported`, `cap_inside_lensing` (the L248 escape as an
inequality), `measured_point_outside_cap`, `cosmic_trace`,
`truncation_acceleration`.

Lean certifies the algebra. Physical verdicts are the Python lane's.

## Tagged, not inflated

| tag | what |
|---|---|
| DERIVED | two-branch dichotomy, matched `P`, `p=0` on (F), truncation formula |
| MEASURED | `n=2`, `a₀ = s/2`, `Ω_dm` amplitude (charge initial condition) |
| POSTULATED | kinematics selects the branch (stars on (F), disc medium on (S)) |
| OPEN | covariant action whose Euler-Lagrange equation *is* `p = P(a)`, constraint algebra, ghosts |

PAPER29's audit of the equilibrium track stands: do not upgrade a
postulate to DERIVED. G028's action-level gap is restated, not closed.

## Kills going forward

1. `f_S ≥ 0.10` from a volume-limited census → L166 double-count.
2. KiDS-like lensing that *turns* at `a₀/(1+B)²` inside 35 kpc → (F) is not carrying lensing.
3. A stripped dwarf with Newtonian `σ` (L247 V7) → (S) does not survive ram pressure.
4. DR4 wide binaries in Arm A (`γ_v ~ 1.17`) → the Sun is not on (F).
