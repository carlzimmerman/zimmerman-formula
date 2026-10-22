# A76 — mutation record

Invocation: `A76_MUTATE=<name> python3 a76_checks.py`; each run writes
`a76_MUTATE_<name>.out` and `a76_results_MUTATE_<name>.json`. Baseline: **35/35 PASS, exit 0**
(`a76.out`). Every mutation changes **one** input and returns **exit 1**. The last column is the
exit code actually observed.

| # | name | the one input changed | baseline value → mutated | checks broken | exit |
|---|---|---|---|---|---|
| 1 | `stiff` | `K_factor` (the K in `L*² = 2c_s²/(Kρ_c)`) | `4πG` → `8πG` (BRIEF §1 convention) | K1 | 1 |
| 2 | `mu_ion` | `mu` (mean molecular weight) | `1.22` → `0.60` (fully ionised) | K4, K5, K6, K8 | 1 |
| 3 | `footing` | `a0_can` | `9.36e-11` → `1.13e-10` (P3) | K5, K6, K8, K12, K13 | 1 |
| 4 | `floor` | `Lstar_anchor` | `24.0` → `23.4289` pc (no rounding) | K7, K8, K15, K17, K18 | 1 |
| 5 | `obs_rc` | the measured-core datum list | 26 rows → 27 rows, adding `(53.31, 0.64)` pc as if it were an observation | K19, K20, K21, K31 | 1 |
| 6 | `beam` | LITTLE THINGS beam scale | `Rmax/(Rmax/HI)` → `×0.1` | K22, K36 | 1 |
| 7 | `rfirst` | LITTLE THINGS innermost-radius scale | `R×R0.3` → `×0.1` | K23, K24 | 1 |
| 8 | `sparc` | SPARC innermost-radius scale | `r_first` → `×0.1` | K26, K27 | 1 |
| 9 | `sparc_drop` | SPARC sample size | 175 curves → 174 (one lost) | K25 | 1 |
| 10 | `chan` | ALFALFA `BW` (bandwidth) | 24.975586 MHz → ×1e5 (0.05 km/s channels) | K28, K29 | 1 |
| 11 | `a0k` | `a0_k12` (the κ = ½ closure value) | `9.354746e-11` → `9.00e-11` | K9, K10, K12 | 1 |
| 12 | `jeans` | cosmic cold density `rho_c` | `2.2565e-27` → `2.2565e-26` kg/m³ | K2, K3, K14, K18 | 1 |
| 13 | `probe_r` | pressure-probe radius `r_probe` | `1 kpc` → `24 pc` (inside the core) | K15 | 1 |
| 14 | `probe_far` | cluster-band probe radius `r_probe2` | `1 Mpc` → `24 pc` | K16 | 1 |
| 15 | `rar_gamma` | `rar_coupling` (a γ-dependence inserted into `g(g_N)`) | `0` → `1` | K34 | 1 |
| 16 | `a18_amp` | A18's Newton amplitude `A_newton` | `10.17` → `12.0` | K33 | 1 |
| 17 | `a0_th` | `a0_th` (thermal footing cH_Λ/2π) | `8.618166e-11` → `9.00e-11` | K9, K10, K11 | 1 |
| 18 | `quoted` | `Lstar_th_quoted` (A65's published 23.4289 pc) | `23.4289` → `20.0` (mis-transcription) | K5, K13, K30, K32 | 1 |

**Coverage: 35/35 checks are killed by at least one mutation** (union of column 5 = every check id).

## Notes on three mutations that are not a raw number

- `obs_rc` is the mutation that matters for this lane: it asserts the premise the task invites
  ("the observed core is 53.31 pc with its error bar"). Four data checks fail immediately, because
  no such datum exists in `table2.dat`. That is the check that refuses the premise.
- `rar_gamma` inserts a γ-dependence into the interpolation `g = (g_N/2)(1+√(1+4a0/g_N))`. With
  `rar_coupling = 0` (the theory as written) the two evaluations in K34 are bit-identical; with the
  coupling on, K34 fails by `ln 2`. This is a *falsifier of the null*, not an input of the theory —
  it is included because a null that cannot fail is not a check.
- `quoted` mis-transcribes a number read out of A65. It exists because K5, K13, K30 and K32 all
  consume that published value; without it those four would be unfalsifiable.

## Deleted check (and why)

One check was written and then **deleted**: *"R_core moves by √2 when γ → 2γ"*
(`R_core(√2 L*)/R_core(L*) = √2`). It is an algebraic identity of `R_core ∝ L*` and survives every
single-input mutation — changing `rc_coef`, `Lstar_anchor`, `rho_c`, `a0` or `mu` leaves the ratio at
√2 exactly. It could not be made to fail without changing the *model* (making `R_core` non-linear in
`L*`), which is not a mutation of an input. Per the rule it was removed; the quantity is reported in
`report.md` §4 as a derived ratio (`Rc_sqrt2_pc` = 75.398 pc), not as a check.

A second candidate, `d ln M_J/d ln γ = 3/2`, was removed for the same reason (it is a scaling
exponent of the `Γ = 2` polytrope and is invariant under every input mutation). The Jeans **value**
is kept as K18, which does fail (`jeans`, `floor`).
