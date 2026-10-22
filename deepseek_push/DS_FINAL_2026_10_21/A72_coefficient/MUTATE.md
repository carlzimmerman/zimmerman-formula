# A72 — MUTATION CONTROL

Twelve mutations, each changing **exactly one input** of `a72_checks.py`, each run and recorded.
Every mutated run exits **1** (the clean run exits 0). **All 22 checks are killed by at least one
mutation; no check had to be deleted.**

Reproduce (from this directory). Mutations are invoked with the environment variable
`A72_MUTATE=<name>` (an equivalent `--mutate=<name>` flag is also accepted):

```bash
python3 a72_checks.py                          # 22/22 PASS, exit 0
A72_MUTATE=kappa_one python3 a72_checks.py     # exit 1, breaks C1,C2
...
A72_MUTATE=de_naive python3 a72_checks.py      # exit 1, breaks C20
python3 a72_checks.py --list-mutations
```

| mutation | the ONE input changed | exit | checks broken | why it breaks them |
|---|---|---|---|---|
| `kappa_one` | κ: 0.5 → 1.0 | **1** | C1, C2 | a0/(cH) doubles while the published 1/Z and 1/7 stay put |
| `omega_quarter` | Ω_Λ: 0.683800 → 0.25 | **1** | C2, C9, C18, C20 | the identity √Ω_Λ/Z and the 32π/147 coincidence both fail; the falsifier-band comparison fails |
| `hubble_for_ds` | H_dS: H_Λ → H0 | **1** | C5, C6, C8, C15 | the thermal/Unruh routes return cH0/2π instead of cH_Λ/2π (ratio 1.2093) |
| `thin_pool` | pool operations: 5 → 2 | **1** | C11, C12, C19, C22 | distinct values fall below 200,000, so the hit counts and the Monte-Carlo probability lose their meaning |
| `sigma_small` | σ(a0): 2.73e-11 → 1e-12 | **1** | C14, C15, C17 | the separation becomes 7.4σ instead of 0.27σ and Δχ² = 54 instead of 0.0875 |
| `two_pi_is_Z` | the thermal factor 2π → Z | **1** | C4, C8, C15 | the thermal coefficient becomes 1/Z, i.e. identical to the theory's |
| `route_1_7` | an extra route returning cH0/7 | **1** | C13, C21 | a stated premise would then "produce" 1/7, which is exactly the claim under test |
| `omega_rational` | the solved Ω*: 32π/147 → 41/60 | **1** | C3, C10 | 41/60 is rational, so the no-rational-count argument fails and the root finding disagrees |
| `unruh_no2pi` | T_Unruh factor 2π → 1 | **1** | C6, C8 | Unruh matching then returns cH/2π, not cH |
| `komar_one` | N_bulk factor 2 → 1 | **1** | C7 | equipartition no longer reproduces Friedmann (N_b/N_s = 0.5) |
| `wb_better` | σ(κ) of the wide-binary forecast: 0.040 → 0.008 | **1** | C16 | the forecast would then separate the candidates at 4.07σ, not 0.814σ |
| `de_naive` | κ_DE = κ_P3/√Ω_Λ → κ_P3/Ω_Λ | **1** | C20 | the two-convention ratio becomes 1.4645 instead of 1.2093 |

## Kill matrix (check × mutation)

| check | killed by |
|---|---|
| C1 | kappa_one |
| C2 | kappa_one, omega_quarter |
| C3 | omega_rational |
| C4 | two_pi_is_Z |
| C5 | hubble_for_ds |
| C6 | hubble_for_ds, unruh_no2pi |
| C7 | komar_one |
| C8 | hubble_for_ds, two_pi_is_Z, unruh_no2pi |
| C9 | omega_quarter |
| C10 | omega_rational |
| C11 | thin_pool |
| C12 | thin_pool |
| C13 | route_1_7 |
| C14 | sigma_small |
| C15 | hubble_for_ds, sigma_small, two_pi_is_Z |
| C16 | wb_better |
| C17 | sigma_small |
| C18 | omega_quarter |
| C19 | thin_pool |
| C20 | omega_quarter, de_naive |
| C21 | route_1_7 |
| C22 | thin_pool |

## Recorded runs

Each mutated run's full stdout is stored beside this file:

```
a72_MUTATE_kappa_one.out        # C1,C2
a72_MUTATE_omega_quarter.out    # C2,C9,C18,C20
a72_MUTATE_hubble_for_ds.out    # C5,C6,C8,C15
a72_MUTATE_thin_pool.out        # C11,C12,C19,C22
a72_MUTATE_sigma_small.out      # C14,C15,C17
a72_MUTATE_two_pi_is_Z.out      # C4,C8,C15
a72_MUTATE_route_1_7.out        # C13,C21
a72_MUTATE_omega_rational.out   # C3,C10
a72_MUTATE_unruh_no2pi.out      # C6,C8
a72_MUTATE_komar_one.out        # C7
a72_MUTATE_wb_better.out        # C16
a72_MUTATE_de_naive.out         # C20
```

Each file ends with `# MUTATION CONFIRMED` and the list of broken checks; the shell exit code
for every one of them is **1** (recorded in the table above and re-verified by the run that
produced them).

## Why a mutation can break several checks

A mutation changes one *physical input*, and several checks legitimately depend on that input.
For example H_dS appears in the thermal-wavelength route (C15), the Unruh inversion (C6), the
2π identity (C8) and the quantum-carrier mass-independence (C5); corrupting it must break all
four. The requirement — one input per mutation, every check killed by at least one mutation — is
satisfied without any check being a restatement of another.
