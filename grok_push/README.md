# grok_push — the two-branch Einstein theory

Write-only folder for this track. Reads the rest of the repo; does not modify it.
This repository is public: this file is written for a hostile referee.

## The answer (K001 + K002)

A complete relativistic **force-law** theory of gravity on these equations
is not available on this evidence. What survives is Einstein gravity plus
one constitutive dark-sector fluid on two branches.

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

## Force-law pincer, now including the screened AeST host (K002)

| completion | death | instrument |
|---|---|---|
| modified gravity | Cassini quadrupole | L243, G004/G005 |
| modified inertia | lensing | L241 |
| disformal / vector | preferred frame | L244 |
| bimetric | lensing sum | G007 Lean |
| H004 screened AeST + `(D²φ)²` | `α₁` **grows** as `XI2`, 12 orders over the Will bound | f31 |
| Hessian-squared `|D_m D_n φ|²` | same growth | f31c B |
| coherent `J_Y → J_Y(1+XI2)` | suppresses, but is **not a local action** | f31c A |

H005 pre-registered both readings of f31. The FAIL reading is the result.
K002 did not re-run the ladder; it read the committed artifact.

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

## Lean

- `lean/K001_two_branch.lean` — 8 theorems, exit 0, zero sorry, standard axioms.
- `lean/K002_alpha1_closed_form.lean` — 4 theorems: `drag_at_zero`,
  `drag_grows_linear`, `drag_slope_pos`, `lock_is_ghost`. Exit 0, zero sorry,
  axioms `{propext, Classical.choice, Quot.sound}`. Certifies that f31's
  closed form **grows** in `XI2` for `0 < K_B < 2`, `J_Y > 0`, and that the
  AeST lock value of `c_14` is a ghost.

Lean certifies the algebra. Physical verdicts are the Python lanes'.

## Tagged, not inflated

| tag | what |
|---|---|
| DERIVED | two-branch dichotomy, matched `P`, `p=0` on (F), truncation formula, f31 closed-form growth |
| MEASURED | `n=2`, `a₀ = s/2`, `Ω_dm` amplitude, `f_S ∈ [0.027, 0.064]` |
| POSTULATED | kinematics selects the branch (stars on (F), disc medium on (S)) |
| OPEN | a **fluid** action in GR whose stress is `T = ρ u u + p(a) Δ` with healthy constraints — not a modified-gravity action |
| DEAD | every local force-law completion, including H004 |

## Kills going forward

1. `f_S ≥ 0.10` from a volume-limited census → L166 double-count.
2. KiDS-like lensing that *turns* at `a₀/(1+B)²` inside 35 kpc → (F) is not carrying lensing.
3. A stripped dwarf with Newtonian `σ` (L247 V7) → (S) does not survive ram pressure.
4. DR4 wide binaries in Arm A (`γ_v ~ 1.17`) → the Sun is not on (F).
5. A local covariant operator that reproduces f31c-(A) (`J_Y → J_Y(1+XI2)`) would reopen the force-law door. Two fourth-order candidates already failed.
