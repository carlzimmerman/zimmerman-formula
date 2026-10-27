# CF2_decoupled_threshold_map: FROZEN CRITERIA (committed alone, before any script or number)

**Why.** CF1 (ef5a07c251 / e370b35e1c) found NO SINGLE c_f. When the switch threshold is X43's crossover, one number sets
two things, and they conflict:

- KiDS isolated-lens lensing needs the threshold ≥ 10^12.39 (canonical).
- Groups need c_f ≥ 4.75.
- A higher c_f lowers the crossover.

**Pre-check (reported, not graded).** Under the record's EM1 M_b → M200 relation, the 63 Tian groups span log M200
12.01–13.69 (10th percentile 12.28, median 12.76). The KiDS lens bins have mean log M200 11.35 / 11.72 / 11.90 / 12.05
(X53 README). So the populations barely overlap, and a threshold that does **not** depend on c_f might separate them.

**The question.** With the switch threshold T **decoupled** from the core concentration, so that a system carries a
route-E halo if it is a satellite or has M > 10^T, is there any (T, c_f) for which X62's full line set passes on both
footings? Two numbers are mapped. Nothing is adopted or claimed derived: a passing region would define *what a derivation
of the threshold must give*.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Harness

CF1's generated X62 harness, with one more patch: **the switch flag**.

- **X43:** `sig_core` returns `M > 10^T` instead of `η Σ_coll > Σ_a₀`. M is the same mass X43 already passes: M200 for
  SPARC and groups, M_b + Mfair for clusters, in M☉.
- **X53:** `halo_setup` returns `M200 > 10^T` instead of `sc > SIGA0`.
- **Unchanged:**
  - the core surface density, which is still max(Σ_a₀, η Σ_coll) with η(c_f);
  - the dwarfs, where X51's flag is satellite-only;
  - all lines and pass rules.

**Grid.** T ∈ {12.1, 12.2, 12.3, 12.4, 12.5} × c_f ∈ {4.75, 5.0, 5.25}, run on both footings.

## 2. Step 0 (stop rule)

- **S0a.** With the flag reverted to the crossover, the harness reproduces CF1's committed c_f = 5.0 grade exactly: the
  fail lists on both footings, groups Z and lensing Δχ² within 0.01.
- **S0b.** X62's switch-property check holds at every grid point.

## 3. Verdict (frozen)

- **DECOUPLED REGION EXISTS.** At least one (T, c_f) passes every line on both footings. The region is listed.
- **THRESHOLD SOLVED, CLUSTERS REMAIN.** Some T passes lensing, groups, SPARC and the dwarfs at some c_f, but no grid
  point also passes all 15 cluster keys. The remaining cluster keys are named. This is the expected inner/outer tension
  from CF1, which a threshold cannot fix.
- **NO DECOUPLED THRESHOLD.** No T passes lensing and groups together at any c_f. The binding line is named.

**Reported only:**
- the number of groups above T;
- per-line passing (T, c_f);
- the alt footing's MW ultra-faint class, which is c_f-independent in CF1 and so is expected to fail throughout. It is
  stated separately so that it cannot mask the threshold answer.

## 4. Checks and twin

- **K1.** The flag changes monotonically: the number of flagged SPARC galaxies, lenses and groups does not increase with T.
- **K2.** The switch property holds at every point.
- **K3.** Peak RSS < 1 GB, per process.
- **MUTATE (`CF2_MUTATE=1`, separate outputs).**
  - m1: the flag is inverted.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K2.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cf2_decoupled.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
