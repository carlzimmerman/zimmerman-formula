# A73 — mutation control

Run a mutation with the environment variable (no argument parsing, so a mutated run cannot
silently fall back to the clean one):

```
A73_MUTATE=<name> python3 a73_checks.py
```

A mutated run prints `[A73_MUTATE=<name>]` in the banner, fails the checks listed below,
and exits **1**. The clean run exits 0 and is the only run that writes `a73_results.json`.
Each mutation changes exactly **one** input of the `BASE` dict; nothing in the check bodies
is switched off by hand, so a check fails only because the number it recomputes moved.

Captured stdout: `a73_MUTATE_<name>.out` (12 files).

## The 12 mutations

| # | name | the one input changed | exit | checks killed |
|---|---|---|---|---|
| 1 | `planck_sigma` | `PLANCK_SIGMA` 0.0073 → 0.00073 (10× tighter Planck) | 1 | K5 K16 K17 |
| 2 | `h0_70` | `H0` 67.4 → 70.0 km/s/Mpc | 1 | K6 K7 |
| 3 | `denom_148` | `DEN` 147 → 148 (the integer under audit) | 1 | K1 K2 K3 K5 K6 K17 K18 K19 K20 K21 K22 K23 K24 K26 |
| 4 | `omega_0688` | `PLANCK_OMEGA` 0.6847 → 0.6889 | 1 | K5 K15 K16 K17 K18 K19 |
| 5 | `kappa_051` | `KAPPA` 0.5 → 0.51 | 1 | K2 K4 K20 K22 |
| 6 | `pool_1op` | `POOL_OPS` 3 → 1 (pool built with one operation) | 1 | K10 K11 K12 K13 |
| 7 | `a0_alt` | `A0` 9.36e-11 → 1.1312e-10 m/s² | 1 | K4 K7 K9 |
| 8 | `curvature` | `SIGMA_K` 0.0019 → 1e-6 (curvature declared exact) | 1 | K18 |
| 9 | `pantheon_om` | `PANTHEON_OM` 0.334 → 0.3153 | 1 | K24 K25 |
| 10 | `desi_om` | `DESI_OM` 0.30203 → 0.3153 | 1 | K23 K25 |
| 11 | `kappa_p3` | `KAPPA_P3` 0.37765 → 0.4137 (the other kappa footing) | 1 | K8 |
| 12 | `family_small` | `FAM_KMAX/FAM_NMAX` 64/400 → 8/20 (own-shape scan) | 1 | K14 |

## Which mutation kills which check (full coverage)

| check | killed by |
|---|---|
| K1 exact value to ten digits | `denom_148` |
| K2 Ω = 32π/147 ⟺ a0/(cH0) = 1/7 | `kappa_051`, `denom_148` |
| K3 the closure at that point is κ = ½ | `denom_148` |
| K4 a0 from Λ, two routes | `a0_alt`, `kappa_051` |
| K5 Planck pull | `denom_148`, `planck_sigma`, `omega_0688` |
| K6 the theory's own H0 footing | `h0_70`, `denom_148` |
| K7 canonical a0 vs 1/7, at its own precision | `a0_alt`, `h0_70` |
| K8 joint-fit a0 vs 1/7 | `kappa_p3` |
| K9 κ_DE/κ_P3 convention factor | `a0_alt` |
| K10 pool ≥ 200 000 | `pool_1op` |
| K11 hits within 0.11σ, two counting routes | `pool_1op` |
| K12 random-target base rate and P(≥1) | `pool_1op` |
| K13 density vs the 11.5776 baselines | `pool_1op` |
| K14 the target's own kπ/n family | `family_small` |
| K15 the two-operation rival | `omega_0688` |
| K16 nearest simple alternatives | `planck_sigma`, `omega_0688` |
| K17 3σ precision requirement | `denom_148`, `planck_sigma`, `omega_0688` |
| K18 curvature dependence | `curvature`, `denom_148`, `omega_0688` |
| K19 H0-footing sensitivity | `denom_148`, `omega_0688` |
| K20 147 = 3(cH0/a0)², 32 = 8/κ², area ratio | `kappa_051`, `denom_148` |
| K21 1/Ω = 147/32π vs A33's 1.462 | `denom_148` |
| K22 1/7 vs 1/(2Z) are different numbers | `kappa_051`, `denom_148` |
| K23 repo DESI DR2 + Pantheon+ pull | `desi_om`, `denom_148` |
| K24 Pantheon+ pull | `denom_148`, `pantheon_om` |
| K25 dataset spread | `desi_om`, `pantheon_om` |
| K26 no standard count gives 147 | `denom_148` |

**26/26 checks are killed by at least one mutation.** No check had to be deleted.
`denom_148` is the broadest killer (14 checks) because 147 is in the identity chain of
every number quoted; `kappa_p3`, `family_small` and `curvature` are single-target mutations
that prove K8, K14 and K18 are computed rather than asserted.

### Why these are the right mutations

- `denom_148` is the claim's own integer moved by one; every identity that is supposed to
  *force* 147 must break, and it does (K1 K2 K3 K20 K21 K22).
- `planck_sigma` and `omega_0688` move the measurement, not the prediction: a genuine
  prediction's sigma-distance must change, and it does.
- `h0_70` and `a0_alt` move the two footings the theory actually uses; K6/K7/K19 and
  K4/K7/K9 are the checks that claim those footings reproduce the prediction.
- `kappa_p3`, `pool_1op`, `family_small` and `curvature` each attack one *method* input
  (the other κ convention, the pool depth, the family scan, the curvature error); the
  corresponding check must fail or it is not measuring that input.
