# X58_object_keyed_switch — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-27, at the owner's request: "freeze and run the object-keyed switch: below X43's crossover the system
follows the law (phantom tail, no halo); above it, route E collapse halos with Newtonian gravity. Grade on the same five
lines as X56."

**Why this lane.**
- X53 / X55: galaxy lensing wants the law's tail, and no route-E halo mass fits both SPARC and KiDS.
- X56: a universal max(law, route E) over-predicts cluster outskirts.
- X54: no exchange between cold dark energy and dark energy.
- So the one shape these results leave is a switch decided per object. This lane is the operational test of X57's
  class M5.

Standing rules: κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. No ΛCDM number
enters a rule. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Hypothesis SW (object-keyed switch)

For each bound system with halo mass M200, the flag is X43's own activity flag, **above ⇔ η(M200) Σ_coll(M200) > Σ_a₀**.

    above:  g = g_N[ρ_b + ρ_E]           (route E: Newtonian, X43 collapse-cored halo, as committed)
    below:  g = ν(g_b/a₀) g_b            (the law on the baryons alone; no halo, phantom tail to all radii)

- Each source lane's M200 and flag are unchanged:
  - SPARC, groups and lensing: EM1 R1 (bg A).
  - Clusters: X43's M_fair + M_b.
  - Dwarfs: every LG dwarf is below the crossover, as X49 verified, so all follow the law (isolated, X1's iso column
    convention).
- The law is the record's ν(y) = ½ + √(¼ + 1/y), isolated, on baryons only, as in X56 and F2 L4.
- **No new constant.** The crossover is X43's. The switch itself is the posit. It is disclosed as nonlocal (keyed on
  the object's M200), and no action is written.

## 2. Inputs and grade: identical to X56 (f17c99a508) §2–3

- **c_f:** X48 ng 48 table **primary**; c_f = 4 reported.
- **Lines, all on both footings:**
  - SPARC line (bg A and B);
  - groups CONSISTENT;
  - 15 cluster keys with |Z| ≤ 2 in both h cells;
  - five LG dwarf classes with |Z| < 2;
  - lensing (all radii, with 2h): Δχ²(SW2H − L2H) ≤ +9 **and** Δχ²(SW2H − H2H) < 0.
- **Verdict:** **SWITCH UNIFIES** if all lines pass on both footings. Otherwise **SW FAILS: <lines>**. If the footings
  disagree, the verdict is **UNDECIDED**.
- **Reported:**
  - the crossover masses;
  - the fraction of systems (or lens weight) on each branch per line;
  - the c_f = 4 variant.

## 3. Checks (all must pass; `--mutate` must fail K1)

- **K0, K2:** as X56. The route-E branch everywhere reproduces X48 ng 48, X53 H2H at c_f 4 and X51. The law branch
  everywhere reproduces EM1 LAW and X53 L.
- **K1 (switch property):** every system's profile equals the branch its flag selects, to 1e-12 relative, counted per
  line.
- **K3:** peak RSS < 1 GB, run as separate processes per scorer if needed.
- **MUTATE:** the flag inverted (above → law, below → route E). K1 must fail.
