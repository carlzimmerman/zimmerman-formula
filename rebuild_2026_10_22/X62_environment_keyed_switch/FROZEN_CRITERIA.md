# X62_environment_keyed_switch — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-27, at the owner's request: "freeze and run an environment-keyed switch: satellites (hosted dwarfs) and
systems above X43's crossover carry route-E halos; isolated systems below the crossover follow the law. Same five lines as
X58."

**Why this lane.** X58 (c3b4f2c7d9) found the need is non-monotone in mass:
- dwarfs need halos;
- L* lenses need the law;
- clusters need halos.

X59 (formation epoch) and X60 (acceleration) keys fail it. Most graded dwarfs are satellites of the MW or M31; the SPARC
discs and the KiDS lenses are isolated. **Environment is the remaining simple key.**

Standing rules: κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. No ΛCDM number
enters a rule. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Hypothesis ENV

    halo branch (route E: Newtonian + the source lane's route-E halo)  if  satellite  OR  η Σ_coll(M200) > Σ_a₀
    law branch  (ν(g_b/a₀) g_b on baryons, no halo)                    otherwise

**Satellite** means X1's `host` column is MW or M31. That covers every MW and M31 class and the individuals; the 13
"LG field" systems are not satellites.

**Isolated by construction:**
- SPARC discs: SPARC has no host flag, and they are treated as isolated (disclosed);
- KiDS lenses: isolated by B21's selection;
- groups and clusters: centrals.

So for SPARC, lensing, groups and clusters the switch is X58's crossover flag, unchanged. Only the dwarfs differ from X58:
the hosted dwarfs carry X51's cooling-floor halos, and the LG field dwarfs follow the law.

**No new constant.** The switch is the posit. It is disclosed as nonlocal (it keys on a host), and no action is written.

## 2. Inputs

- **c_f PRIMARY:** X48 AMENDMENT A2's nine-seed table (`x48_analyze_results_ng48_A2.json`; 11.63 / 8.22 / 7.31). It is
  the record's current native measurement. It is used in the halo cores (X43 copy) and in X53's lens halos.
  - **Disclosed before the run:** X48 A2's own regrade fails the SPARC line with it (Υ 0.31). That fail applies here only
    to SPARC galaxies above the crossover.
- **Reported:**
  - X58's 3-seed ng 48 table;
  - c_f = 4.
- Everything else is as X56 / X58 (same scorers, executed read-only, each in its own process).

## 3. Grade: identical to X58 (9964127dfd) §2

- **Lines, all on both footings:**
  - SPARC line (bg A and B);
  - groups CONSISTENT;
  - 15 cluster keys with |Z| ≤ 2 in both h cells;
  - five LG dwarf classes with |Z| < 2;
  - lensing (all radii, with 2h): Δχ²(ENV2H − L2H) ≤ +9 and Δχ²(ENV2H − H2H) < 0.
- **Verdict:** **ENVIRONMENT SWITCH UNIFIES** if all lines pass on both footings. Otherwise **ENV FAILS: <lines>**. If
  the footings disagree, the verdict is **UNDECIDED**.
- **Reported:**
  - the branch fractions per line;
  - Crater II, Antlia II and Sagittarius individually;
  - both reported c_f variants.

## 4. Checks (all must pass; `--mutate` must fail K1)

- **K0:**
  - route E everywhere reproduces X48 A2's regrade (SPARC 0.0774 / 0.0774, groups Z +1.33);
  - route E everywhere reproduces X53 H2H at c_f 4 (583.9 / 580.6);
  - X51's class medians are reproduced.
- **K2:** the law everywhere reproduces EM1 LAW and X53 L.
- **K1:** every system call equals its flagged branch. The flag is satellite OR above crossover.
- **K3:** peak RSS < 1 GB per process.
- **MUTATE:** the flag is inverted, so K1 must fail.
