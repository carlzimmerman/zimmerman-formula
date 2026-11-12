# FINAL-14 (LEAN-AMOUNT) -- amount-budget arithmetic, certified in Lean

**Verdict: all six items compile as named theorems. `lean` exit code 0, zero errors,
zero warnings, zero `sorry`, zero `sorryAx`.**

- Toolchain: `leanprover/lean4:v4.34.0-rc2` (Lean 4.34.0-rc2, arm64-apple-darwin24.6.0), Mathlib `v4.34.0-rc2`.
- File: `FINAL14_lean_amount.lean` (namespace `Final14`), output: `verify.out`.
- Scope: pure real algebra. No physics claim is made here; every theorem is a statement about
  `ℝ`, `Real.sqrt`, `Real.pi` and rational constants.

## Reproduce

```sh
cd /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL-14_lean_amount/FINAL14_lean_amount.lean
echo "exit=$?"
```

(The Mathlib cache was already materialised in that project's `.lake`, so `lake env lean`
supplies the import path. A fresh clone + `lake exe cache get` would work equally.)

## Objects

| symbol | definition |
|---|---|
| `R_b` | `541/100` |
| `D_low`, `D_high` | `911/1000`, `7/5` |
| `X_s` | `119/2` |
| `a0_canon`, `a0_alt` | `93603/10^15`, `11312/10^14` |
| `G_N`, `G_gas1` | `66743/10^15` (lane brief), `6674/10^14` = 6.674e-11 (repo gas1.py) |
| `Msun_kg`, `pc_m`, `msun_pc2` | `1.989e30`, `3.0857e16`, `Msun_kg / pc_m^2` |
| `X (x)` | `(Real.sqrt (1 + 4*x^2) - 1)/2` |
| `x_b (R)` | `Real.sqrt (R*(1+R))` |
| `gas_column a0 G R` | `a0 / (Real.pi * G * (x_b R)^2) / msun_pc2` |

## Certified results (numeric brackets)

| # | theorem | statement certified | bracket |
|---|---|---|---|
| 1 | `X_monotone` | `0 < a -> a < b -> X a < X b` | monotone on `ℝ_{>0}` |
| 2 | `X_x_b` | `X (x_b R) = R` for every `R > 0` | exact identity: `1 + 4R(1+R) = (2R+1)^2` |
| 2 | `X_break_value` | `X (x_b (541/100)) = 541/100` | exact |
| 2 | `X_break_window` | `x_b (541/100)` | `(5.8887, 5.8889)` |
| 2 | `X_break` | value identity ∧ window | as above |
| 3 | `ratio_break` | `X (x_b R) / R = 1`, `R > 0` | exact |
| 3 | `ratio_break_Rb` | same at `R = R_b` | exact |
| 4 | `demand_over_budget_21p45` | `X (21.45) / R_b` | `(3.87, 3.88)` |
| 4 | `demand_over_budget_41p98` | `X (41.98) / R_b` | `(7.66, 7.67)` |
| 4 | `demand_over_budget_60p00` | `X (60.00) / R_b` | `(10.99, 11.00)` |
| 4 | `demand_over_budget_98p32` | `X (98.32) / R_b` | `(18.08, 18.09)` |
| 5 | `share_over_delivered_low` | `X_s / D_low = 59500/911` | `(65.3, 65.4)` (value 65.3128…) |
| 5 | `share_over_delivered_high` | `X_s / D_high` | `= 42.5` exactly (595/14) |
| 6 | `gas_column_canonical` | `a0_canon`, `G_N` | `(6.162, 6.163)` |
| 6 | `gas_column_alternative` | `a0_alt`, `G_N` | `(7.447, 7.448)` |
| 6 | `gas_column_canonical_gas1` | `a0_canon`, `G_gas1` | `(6.162, 6.163)` |
| 6 | `gas_column_alternative_gas1` | `a0_alt`, `G_gas1` | `(7.447, 7.448)` |
| 6t | `gas_column_canonical_tight` | `a0_canon`, `G_N` | `(6.1624, 6.1625)` |
| 6t | `gas_column_alternative_tight` | `a0_alt`, `G_N` | `(7.4473, 7.4474)` |
| 6t | `gas_column_canonical_gas1_tight` | `a0_canon`, `G_gas1` | `(6.1626, 6.1628)` -> **6.1627** |
| 6t | `gas_column_alternative_gas1_tight` | `a0_alt`, `G_gas1` | `(7.4476, 7.4478)` -> **7.4477** |

Exact values behind the brackets (independent high-precision cross-check, `Fraction`/`Decimal`):

- `x_b(541/100) = sqrt(346781/10000) = 5.888813…` ∈ (5.8887, 5.8889).
- `X(21.45)/R_b = 3.87338…`, `X(41.98)/R_b = 7.66783…`, `X(60)/R_b = 10.99854…`,
  `X(98.32)/R_b = 18.08157…` (round to 3.87 / 7.67 / 11.00 / 18.08 as expected).
- `X_s/D_low = 59500/911 = 65.3128…`, `X_s/D_high = 595/14 = 42.5`.
- `Sigma` (Msun/pc^2): with `G = 6.6743e-11` → 6.162422… / 7.447339…;
  with `G = 6.674e-11` → 6.162700… / 7.447674… .

## Flagged discrepancy (not hidden)

The brief states `G = 66743/10^15` (6.6743e-11) while quoting 6.1627 / 7.4477. Those two
targets are what `G = 6.674e-11` produces (the constant in the repo's
`HY4-1_GAS1_hot_gas_census/gas1.py`: `G = 6.674e-11; Msun = 1.989e30; pc = 3.0857e16`).
With the brief's `G` the values are 6.1624 / 7.4473. **Both** are certified above; they
agree to three decimals (6.162 / 7.447) and are separated by the 4-decimal tight brackets.
The discrepancy is 5e-5 relative -- it does not affect any bracket at 3 decimals.

## Method notes

- Monotonicity: `a^2 < b^2` from `0 < a < b` via `(b-a)(b+a) > 0`, then
  `Real.sqrt_lt_sqrt`, then affine rescaling. No differentiation, no continuity.
- Break identity: `x_b(R)^2 = R(1+R)` by `Real.sq_sqrt` (needs `R > 0`), hence
  `1 + 4 x_b(R)^2 = (2R+1)^2`, and `Real.sqrt_sq` gives `2R+1` since `2R+1 > 0`.
- Every numeric bracket is a **square comparison between exact rationals**, discharged by
  `norm_num`; no floating point enters the kernel.
- The only irrational in the gas column is `Real.pi`, handled by Mathlib's
  `Real.pi_gt_d6 : 3.141592 < π` and `Real.pi_lt_d6 : π < 3.141593` plus monotonicity of
  `a / b` in a positive denominator (the kernel never evaluates `Real.pi`).
