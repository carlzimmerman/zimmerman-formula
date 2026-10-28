# CL3_one_number: FROZEN CRITERIA (committed alone, before any CL3 number; CL2's remaining grid points not yet seen)

## Why

**CL2** (frozen b57ed8751f, partial results seen) uses:
- CF2's decoupled switch at T = 12.3;
- GS1's measured cluster gas budget;
- c_f(M) = L · c_nat(M)/c_nat(10^14), with the native nine-seed zoom slope (S9).

At L = 4 it passes **every graded line on the canonical footing**: SPARC, groups (Z +1.99), all 15 cluster keys, the five
LG dwarf classes, and KiDS lensing. Alt fails only its known L- and T-independent lines (the SPARC line and the MW
ultra-faints).

**DT1** (b4fbcf0707) found no native derivation of T. Its reference candidate, X43's core-floor crossover η(c_f) Σ_coll(M)
= a₀/2πG at c_f = 4, sits at the window: 12.09 on canonical (NEAR) and 12.43 on alt (HIT).

## The question

Set **T = X43's crossover evaluated at the same level L**, per footing, instead of locating T from CF2. Is there an L for
which every line passes?

If yes, **one external number L sets both the switch and the cores**. The two data-located numbers (T, L) reduce to one,
and the mass slope stays native.

There is a known risk. At L = 4 the canonical crossover is 12.09, just below CF2's lensing edge (lensing fails at 12.1 and
passes at 12.2).

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Harness

CL2's harness, with the switch flag per footing set to M > 10^{T_f(L)}:

- T_f(L) solves (4/(3B(1))) L^{5/4} Σ_coll(10^T) = a₀,f/(2πG);
- Σ_coll is X43's Lacey–Cole half-mass collapse surface density on the record's CLASS A background, computed exactly as
  DT1 (d782d8ec78);
- the shape is S9;
- the measured cluster budget is GS1's.

**Grid.** L ∈ {3.75, 3.9, 4.0}, both footings.

## 2. Step 0 (stop rule)

- **S0a.** T_f(4.0) reproduces DT1's candidate A: 12.093 / 12.429, within 0.002.
- **S0b.** With the flag forced to CL2's fixed T = 12.3 at L = 4, the grade reproduces CL2's committed S9 L 4 point. Fail
  lists must match; groups Z and G-OUT-all Z must match to 0.01. This is read from CL2's results JSON. If CL2 is not yet
  committed when CL3 reaches this step, the comparison uses CL2's results file on disk, and that is disclosed.

## 3. Verdict (frozen)

- **ONE NUMBER PASSES (canonical / alt / both):** some L passes every line on that footing. The passing L values are listed.
- **ONE NUMBER FAILS:** no grid L passes on either footing. The binding lines are named.
- **Alt:** its known L- and T-independent failures (the SPARC line and the MW ultra-faints) are labelled separately, as in
  CL1 and CL2.
- **Scope, frozen.** L is the single external number, the record's long-standing c_f level. A pass reduces the theory's
  calibrated numbers from two to one. It is not a derivation of L, which awaits converged native zooms.

## 4. Checks and twin

- **K1.** The switch property holds at every grid point.
- **K2.** T_f(L) decreases with L (the crossover moves down as η grows).
- **K3.** Peak RSS < 1 GB, per process.
- **MUTATE (`CL3_MUTATE=1`, separate outputs).**
  - m1: T_f uses c_f = 2L instead of L.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cl3_one_number.py`.
