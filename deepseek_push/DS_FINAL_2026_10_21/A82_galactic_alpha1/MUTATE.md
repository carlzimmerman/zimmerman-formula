# A82 — mutations, and what each one proves the checks can see

Every mutation changes **one** physical input or one **solver relation** in the BVP, is applied
by `A82_MUTATE=<name>` (equivalent: `--mutate <name>`), and is required to make the run exit 1.
All runs below were executed from a cold start in this directory with

```bash
A82_MUTATE=<name> python3 a82_checks.py --quiet ; echo $?
```

Recorded exit codes and the checks that failed (from the `FAIL` lines of that run):

| mutation | what changes, exactly | exit | checks broken | n |
|---|---|---|---|---|
| `drop_boost` | the clock source factor `(1+2w²)` is set to 1: the galaxy is at rest w.r.t. the CMB frame | **1** | B1 B2 B3 B5 B7 B8 B9 C8 E3 | 9 |
| `boost_half` | `2w² → w²` (wrong coefficient in the tilted-foliation lapse) | **1** | B5 B7 B9 C8 E3 | 5 |
| `linear_response` | the exact nonlinear response `C = u(2a₀−u)/(a₀−u)²` is replaced by its small-`u` (Newtonian) value `2u/a₀` | **1** | B2 B4 B5 B6 B7 B9 C7 E1 E2 E3 | 10 |
| `sign_flip` | the boost source `−2w²g` is given the wrong sign (`+2w²g`) | **1** | B3 B5 B7 B9 C7 E3 | 6 |
| `no_gradient` | `γ = 0`: the P-gradient operator `−(γ/2)(D·P)²` is removed from the action sector | **1** | A1 A7 | 2 |
| `a0_off` | physical input: `a₀ → 1.05 a₀` | **1** | B7 B9 | 2 |
| `Lstar_off` | physical input: `L★ → 2 L★` (the P coherence length) | **1** | B5 | 1 |
| `spurious_dipole` | an `l = 1` source `0.7 cos θ` is added to the P equation (a preferred-direction term the action does not contain) | **1** | C1 C4 | 2 |
| `w_quad` | the Langmuir gate `W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)]` is replaced by a quadratic `W' = 2u/K`, i.e. `u²/(a₀−u) → 2u²/a₀` | **1** | A1 A3 B2 B5 B7 B8 B9 | 7 |
| `lapse_half` | the `w²` coefficient of the tilted-foliation lapse `2w²Φ` is halved to `w²Φ` | **1** | C2 C3 C5 | 3 |
| `no_phi2` | the post-Newtonian `−Φ²` term is deleted from the exact lapse | **1** | C6 | 1 |
| `pulsar_wide` | physical input: the pulsar–WD orbital period `5.85 h → 100 d` | **1** | D1 D2 D3 D6 | 4 |

`lapse_half` is the sharpest of the set: it changes nothing in the numerical BVP (which uses the
clock factor directly) and is caught **only** by the angular-projection checks C2/C3 and by the
symbolic ADM check C5 — i.e. the "no dipole" result is tied to the coefficient 2 in the lapse and
not to a number typed into the solver.

`no_phi2` is caught only by C6, which is the point of C6: the `−Φ²` term must **not** cancel, and
deleting it is detectable.

## Coverage: every check has at least one mutation that breaks it

| check | broken by |
|---|---|
| A1 static BVP residual | `no_gradient`, `w_quad` |
| A3 slaved limit | `w_quad` |
| A7 P-gradient operator active | `no_gradient` |
| B1 boosted BVP residual | `drop_boost` |
| B2 linearised = nonlinear difference | `drop_boost`, `linear_response`, `w_quad` |
| B3 δa > 0 | `drop_boost`, `sign_flip` |
| B4 bound `δa/(w²a₀) < 1` | `linear_response` |
| B5 α₁,eff = 4u′/(1−u′) | `Lstar_off`, `boost_half`, `linear_response`, `a0_off`(via B7), `w_quad` |
| B6 α₁g ≤ 2a₀ | `linear_response` |
| B7 A36's table reproduced | `a0_off`, `boost_half`, `sign_flip`, `drop_boost`, `w_quad` |
| B8 w²-continuation | `drop_boost`, `w_quad` |
| B9 α₁(8 kpc) value | `a0_off`, `boost_half`, `sign_flip`, `drop_boost` |
| C1 l=1 projection = 0 | `spurious_dipole` |
| C2 l=2/l=0 = 2/13 | `lapse_half` |
| C3 l=0 = 13/6 | `lapse_half` |
| C4 dipole moment = 0 | `spurious_dipole` |
| C5 pure-boost ADM terms cancel | `lapse_half` |
| C6 `−Φ²` does not cancel | `no_phi2` |
| C7 2PN contamination > 10 at 1 kpc | `linear_response`, `sign_flip` |
| C8 2PN contamination < 0.05 at 30 kpc | `drop_boost`, `boost_half` |
| E1 α₁(1 pc) < 1e-6 | `linear_response` |
| E2 α₁(10 pc) < 1e-4 | `linear_response` |
| E3 α₁ = 4(a₀/g)² scaling | `drop_boost`, `boost_half`, `linear_response`, `sign_flip` |
| D1 α̂₁(internal) < 1e-20 | `pulsar_wide` |
| D2 e_F < 1e-25 | `pulsar_wide` |
| D3 Shao–Wex margin > 15 dex | `pulsar_wide` |
| D6 EFE correction < 1e-9 | `pulsar_wide` |

## Checks that were deleted because no mutation could break them

Deleted, with the reason (per the lane's rule: a check that cannot fail is not a check):

- **`A4` first integral `g = g_N + u`** — `g` is *defined* as `g_N + u` in the solver's output
  dictionary, so the residual is zero by construction (it printed `1.152e-14`). An identity, not a
  test. Retained as a printed column in `[A]`.
- **`A5` `u < a₀` and `0 < u′ < 1`** — both are algebraic properties of the slaved branch
  `u = a₀g/(g+a₀)`: `u/a₀ = g/(g+a₀) < 1` and `u′ = (a₀/(g+a₀))² ∈ (0,1)` for every positive `g`.
  No physical input can violate them; the solver's line search additionally enforces the cap, so
  even `w_quad` (which drives `u → g_N = 9.9 a₀` at the centre) cannot. Retained as a printed
  diagnostic (`u < a0 everywhere: True ; max u/a0 = 0.911607`).
- **`A6` `u′` monotone in `r`** — this is a property of the *input* `g_N(r)` (a Hernquist cusp has a
  single minimum of `g`), not of the solver or of any physical constant. Deleted.
- **`D4` `Δa < 1e-15 m/s²`** and **`D5` `δP_b/P_b < 1e-18`** — both are *theorem-bounded*: the
  external-field channel gives `Δa = ½ α₁ g_ext (V/c)(v_orb/c)` and the identity proved in B6,
  `α₁ g_ext ≤ 2a₀`, caps it at `a₀ (V/c)(v_orb/c) = 1.54e-16 m/s²` for **any** `g_ext`. No physical
  input can push it above `1e-15`; the numbers are retained as printed diagnostics.

## A mutation that was tried and is *not* claimed

`first_order` (upwind the `u′/r` term of the P operator, making the scheme first-order) changes
nothing at the reported radii: the P-gradient operator contributes `5.187e-06` of the response at
1 kpc (`(L*/r)²u′/2` column of `[B]`), so the discretisation order is invisible at 1–1000 kpc. It
is left in the script as a switch but is **not** counted as a mutation, because it breaks no check.
That fact is itself the numerical justification for the resolution used: `u(8 kpc)` moves by
`1.38e-07` between `N/4` and `N` grid points.
