# MUTATE — A33 proof that the checks have teeth

Each mutation alters **one coefficient or one term** of the master action (or of its TT reduction) and must
break at least one check. All six do; each run exits 1. Captured output: `a33_MUTATE_<name>.out`.

```
python3 a33_checks.py --mutate <name>
```

| mutation | what it changes | checks that break | captured output |
|---|---|---|---|
| `clock2` | clock coefficient `P^iD_i\ln N` → `2·P^iD_i\ln N` | **K1, K2, K5** | `a33_MUTATE_clock2.out` |
| `nocharge` | clock coefficient → `0` (the clock term deleted from the lapse source) | **K1, K2, K5** | `a33_MUTATE_nocharge.out` |
| `wquad` | `W = (a₀²/K)[−u/a₀ − \ln(1−u/a₀)]` → `u²/(2K)` | **K3, K4** | `a33_MUTATE_wquad.out` |
| `gamma0` | `γ → 0` (both gradient terms removed) | **K11b** | `a33_MUTATE_gamma0.out` |
| `beta0` | `(1+β)θ² → θ²` (the ADM deformation removed) | **K10** | `a33_MUTATE_beta0.out` |
| `ricciP` | TT kinetic coefficient `1 → 1/(1+2ξP²)`, i.e. what a `ξR_{ij}P^iP^j` coupling does: `c_T² = 1/(1+2KξP²)` | **K6** | `a33_MUTATE_ricciP.out` |

## Measured failures (from the captured files)

```
clock2    K5_clock_coefficient_is_one   FAIL  resid(xi=2)=a0*g*(-3*a0-2*g)/(a0^2+3*a0*g+2*g^2)
          K1_lapse_eq_is_hamiltonian_constraint  FAIL  (FP*PV*r/2+FV*PP*r+2*FV*PV)/(sqrt(FV)*r)
nocharge  K5  FAIL  resid(xi=0)=a0*g/(a0+g)          K1, K2 FAIL
wquad     K3  FAIL  -g^2/(a0+g)                       K4 FAIL  g^2/(a0+g)
gamma0    K11b FAIL (no switch-off exists: the pressure force is identically zero)
beta0     K10 FAIL  value=Lambda/3   threshold=2*Lambda/(3*(3*beta+2))
ricciP    K6  FAIL  value=1+2*xiP2   threshold=1
```

Each of the six exits with status 1 and prints
`A33 COMPLETE: n/28 checks PASS.` with `n < 28`.

## Notes on the two that break three checks

`clock2` and `nocharge` are the strongest mutations available, because the clock term is the only `O(ε)` lapse
source in the whole action. Deleting it (`nocharge`) is literally A12's counterexample class — it turns the P
sector into a stress sector and the slip becomes `O(1)`. Doubling it (`clock2`) deforms the law into
`g_N = g(a₀+2g−4a₀)/(a₀+2g)`, which is not `g²/(g+a₀)`; K5 reports the deviation analytically (0.55 at
`g = a₀/2`), while K1 and K2 report the reduced-action inconsistency.

## What the mutations do *not* touch

The `--mutate` flag never touches the numbers in §4's table (Λ, a₀, L\*, ς, y_t); it only changes the action.
That is deliberate: the point is that the *derivations* depend on the terms, not that the arithmetic can be
broken by changing an input.