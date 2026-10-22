# A47 mutations

Three mutations, one per check group. Each is run as `A47_MUTATE=<name> python3 a47_checks.py`; each
writes `a47_MUTATE_<name>.out` / `a47_results_MUTATE_<name>.json` and exits 1. The primary run is
`python3 a47_checks.py` → 18/18, exit 0.

| mutation | what it changes | checks that fail | exit |
|---|---|---|---|
| `system` | `f_ret ≡ 1` (the system, not the catchment, is the reservoir) — the record's excluded model | K2, K5, K6, K7, K8, K10, K11, K12, K13, K14, K15, K16, K17 (13 of 18) | 1 |
| `density` | reads the factor 10 as a **density** ceiling: `M_max = 10 ρ̄_cold V(r_e)` | K8, K13 | 1 |
| `freeze` | `f_ret ≡ 0.10` at every mass (A44's constant, without the CFG416 `M_ta` dependence) | K2, K12, K15 | 1 |

## `system` — f_ret = 1

The denominator error the lane is about. With `f_ret = 1` the budget collapses to `N = 5.364`
(5.364 M_b), which is CFG801's excluded model:

- K13 fails: `N_avail/N_req = 5.36/15.94 = 0.34` — now genuinely capped below the requirement.
- K14 fails: `Δχ²(5.364) = +197.0` (the no-edge tension returns in full).
- K6/K5 fail: `53.643` and `s_edge = 54.14` no longer reproduce (`5.364`, `5.843`).
- K16 fails: `R_tot/N = 25.043/5.364 = 4.67`, i.e. 116σ from A29's `u_MID = 0.4716` — `u > 1`, which is
  the sense in which the *system* denominator is impossible (the phantom would carry 4.7× the whole cold
  budget).
- K17 fails: the edge falls to `0.07-0.10 r_ta`, i.e. 34-81 kpc, far inside the catchment.

This mutation is the control that proves the checks are about the denominator and not about arithmetic:
the same code, with `f_ret = 1`, reproduces the record's +197.

## `density` — the brief's premise taken literally

If "ten times the cosmic share" were a density ceiling, the maximum cold mass inside `r_e = 0.661 Mpc`
would be `10 ρ̄_cold V(r_e) = 4.04 M_b` (0.40 M_b at the mean density alone):

- K13 fails: `N = 4.0 < N_req = 15.9`.
- K8 fails: the mean-density fraction becomes `1.80` (>1) because the ceiling, not the physics, is doing
  the work.

This mutation isolates the category error. Note that it fails even though it is *more generous* than the
actual cosmic mean by a factor 10: the correct ceiling is not a density at all but the mass of the
catchment, which is `1.0 × 10^3` times `ρ̄_cold V(r_e)` because a halo is collapsed.

## `freeze` — f_ret = 0.10 everywhere

A44's constant applied at all masses, ignoring CFG416's `M_ta` dependence:

- K12 fails: at `1e11` it returns `N = 53.64` where the table's fixed point is `44.15` (A18: 44.125);
  at `1e12`, `53.64` against 14.92.
- K15 fails: `53.64/37.9 = 1.00`, i.e. it erases the statement that the factor 10 is a low-mass branch.
- K2 fails: the "table" is constant, so it is not CFG416's table.

This is the mutation that would hide the lane's one real correction to A44: `53.64` is the value at
`M_b ≤ 7.4e10`, not at `1e11` or at the top KiDS bin. It does *not* change the verdict (both values clear
`N_req`), which is why the verdict is stated as a ratio and not as a single number.
