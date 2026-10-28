# DT1_threshold_tournament: can any zero-parameter candidate derive the switch threshold T?

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (d782d8ec78).
- **The window:** canonical (12.1, 12.5] and alt (12.2, 12.5], in log M200, from CF2 (a2704b5c66) and CL1 (bfbc7af384).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **T NOT DERIVED**

| id | candidate | log T, canonical / alt | grade |
|---|---|---|---|
| A | X43 crossover at the external c_f = 4 (reference only) | 12.09 / 12.43 | NEAR / HIT |
| B | crossover at the self-similar c_f = 1.85 (X44) | 13.85 / 14.20 | MISS |
| C | crossover with the native c_f(M) (X48 nine-seed table) | 9.83 / 10.14 | MISS |
| D | half-mass formation at acceleration onset (z = 0.638) | 13.59 | MISS |
| E | half-mass formation at Ω_Λ = Ω_m (z = 0.300) | 15.54 | MISS |
| F | M200 of the stellar-mass-function knee (Driver et al. 2022, via EM1's relation) | 11.87 (11.94 at 1.2 M★) | MISS |
| G | the law alone supplies the fair share at R200 / R500 / r_ta | 14.24 / 13.44 / no root | MISS |

None of the native candidates lands T. These are recorded exclusions.

## Clue for the next lane (reported, not graded)

The reference crossover A, the X43 core-floor crossover at c_f = 4, sits at the window: NEAR on canonical (12.09, against
the lower edge 12.1) and a HIT on alt. c_f ≈ 4 is also the level the cluster cores need at the measured gas budget (GS1,
CL1). CF1 rejected "threshold = crossover" only for a *single constant* c_f that must also serve groups. With CL2's native
mass slope supplying the groups' extra concentration, **T may be the crossover evaluated at the cluster-level c_f (L)**.
That would make T and L one number. It is to be frozen and tested as CL3, a hypothesis and not a result.

## Checks: 3/3

- K0: reproduces X43's crossovers.
- K1: the z_f table.
- K2: 0.24 GB.

The rerun is identical apart from the RSS line. The MUTATE twin (a₀ footings swapped, K0 target × 1.01) fails K0.

## Files

- `dt1_tournament.py`
- `dt1_tournament.out` and `dt1_tournament_results.json`
- `*_MUTATE.*`
