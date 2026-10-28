# DT1_threshold_tournament: FROZEN CRITERIA (committed alone, before any DT1 number)

**Goal (owner, 2026-10-27):** derive the switch threshold T, which CF2 and CL1 locate from data at log M ≈ 12.2–12.5,
without fitting it to the lines that locate it.

**The method.** A pre-registered tournament. Each candidate below is a zero-parameter (or external-data-only) prediction
of T, computed on the native background (or the record's own CLASS background where X43's machinery requires it), on
both footings. Each is compared with the frozen window. A **hit** is a derivation of T. A **miss** is a recorded
exclusion. No candidate may be added, altered or re-scaled after any DT1 number is seen; new ideas go to a new lane.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. The window (frozen, from committed lanes)

The window comes from CF2 (a2704b5c66) and CL1 (bfbc7af384). The mass is M200 in M☉, as in X62's switch.

| footing | HIT range for log T | evidence |
|---|---|---|
| canonical | (12.1, 12.5] | lensing fails at 12.1 and passes from 12.2; groups and lensing pass through 12.5 |
| alt | (12.2, 12.5] | groups are +2.01 at 12.2 |

- **NEAR:** within 0.15 dex outside the HIT range.
- **MISS:** anything else.
- The upper edge is the largest T tested. A candidate above 12.5 is reported as "untested above window", counted as a
  MISS, and flagged for testing.

## 2. Candidates (frozen list)

| id | candidate | type |
|---|---|---|
| A | X43 crossover η Σ_coll(M) = a₀/2πG at the **external** c_f = 4 | reference only; not a derivation |
| B | the same crossover at the **self-similar** c_f = 1.85 (X44) | native |
| C | the same crossover with **native** c_f(M) from X48's nine-seed table (self-consistent root) | native |
| D | half-mass formation redshift z_f(M) = z of acceleration onset (q = 0) | native epoch |
| E | z_f(M) = z where Ω_Λ(z) = Ω_m(z) | native epoch |
| F | M200 of the galaxy stellar-mass-function knee. Driver et al. 2022 log M★ = 10.745 (h70), converted to native h, mapped through EM1's M_b → M200 relation (a 11.18, b 0.90) with M_b = M★ (stellar only). Reported variant: M_b = 1.2 M★ | external data plus the record's fitted relation; disclosed as non-native |
| G | the mass at which the law alone supplies exactly the fair share at the halo edge: the law's dynamical mass at R200 equals (1 + Ω_c/Ω_b) M_b, with R200 of a total (1 + Ω_c/Ω_b) M_b at 200 ρ_c. Variants at R500 and at r_ta | native, parameter-free |

For **D** and **E**: M is the mass whose X43 Lacey–Cole half-mass formation redshift, on the record's CLASS background,
equals that epoch.

## 3. Verdict (frozen)

- **T DERIVED (candidate …):** a non-reference candidate (B–G) is a HIT on canonical, and a HIT or NEAR on alt.
- **T NEAR (candidate …):** the best non-reference candidate is NEAR on canonical.
- **T NOT DERIVED:** every non-reference candidate is a MISS on canonical. All values are reported as exclusions.

## 4. Checks and twin

- **K0.** Candidate A reproduces X43's crossovers, 12.09 / 12.43, within 0.01.
- **K1.** The z_f(M) table reproduces the scouting values within 0.005 (A_c2b_refit: 10^12 → 0.944, 10^12.3 → 0.886).
- **K2.** Peak RSS < 1 GB.
- **MUTATE (`DT1_MUTATE=1`, separate outputs).**
  - m1: a₀ is swapped between the footings.
  - m2: the K0 target × 1.01.
  - The twin must fail K0.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I dt1_tournament.py`.
