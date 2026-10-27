# X56_law_floor_structure: "gravity is never weaker than the law" fails, on cluster outskirts, the SPARC Υ line and lensing at native c_f

Criteria: `FROZEN_CRITERIA.md` (f17c99a508, committed alone). No amendment. κ = ½ FITTED. Footings never pooled. Cold dark
energy is not matter. Not "theory closed". Nothing here says the data favour the framework.

**Hypothesis LF:** g = max(ν(g_b/a₀) g_b, g_N[baryons + route-E halo]). Each grade is the source lane's committed scorer,
executed read-only, with only that one line changed: X43 for SPARC, groups and clusters (X48 ng 48 c_f, as X48's
regrade); X53 for lensing; X51 for the dwarfs.

## Verdict (frozen): **LF FAILS** on both footings

| line | canonical | alt |
|---|---|---|
| SPARC (rms @ median Υ) | 0.0601 @ **0.47**: line FAIL | 0.0594 @ **0.40**: FAIL |
| groups | Z −1.38 CONSISTENT | Z −1.74 CONSISTENT |
| clusters | **G-OUT-all OVER (−2.38)**, G-OUT-M3 UNDER (+2.23), G-IN-Mall OVER (−2.43) | **7 OUTER keys fail**, G-IN-Mall OVER |
| dwarfs (X51) | all five pass | MW ultra-faint OVER (Z −2.77; X51's own miss) |
| lensing Δχ²(LF2H − L2H) / (LF2H − H2H) | **+11.2** / −421.8 (gate ≤ +9) | +6.0 / −456.2: pass |

**Reported: c_f = 4.**
- canonical: SPARC passes; lensing is identical to the law (Δχ² 0.0); fails G-OUT-all, G-OUT-b, G-OUT-M3.
- alt: fails the SPARC line, 7 cluster keys and the ultra-faints.

**Checks 6/7.** K0 (route E alone reproduces X48 ng 48, X53 H2H at c_f 4 and X51), K1 (the floor property, 0 violations
in 3.8e7 grid points) and K2 (the law alone reproduces EM1's LAW rms and X53's L χ²) pass.
- **K3 FAILED:** peak RSS 1.15 GB against the 1 GB gate. It is cumulative over nine in-process executions of the source
  scorers, an implementation cost, not a graded number.
- `--mutate` (law branch dropped) fails K1, exit 1.

## What it means

1. **The law on cluster baryons is too strong in cluster outskirts.**
   - The law branch wins on 48 % of the cluster grid.
   - At 1.4–3 Mpc it predicts lensing amplitude 1.00–1.05 against the measured 0.66–0.72 (X30's calibrated ratio).
   - So a perpetual phantom tail around clusters is excluded by the same X30 data that route E passes.
2. **Galaxies want that tail; clusters forbid it.**
   - X53 showed isolated-galaxy lensing wants the law's tail to 3 Mpc. With the floor added, galaxy lensing equals the law
     (Δχ² 0 at c_f 4).
   - So a universal "never weaker than the law" cannot be the structure. Whatever supplies the tail must switch off in
     systems whose collapse core is above the floor, i.e. above X43's crossover.
   - That is the same object-keyed, nonlocal switch X47 found the floor itself needs.
3. **SPARC:** the law adds mass where the halo is lighter, so the fitted Υ drops below the 0.50 line (0.47 / 0.40). The
   rms improves (0.060 vs X43's 0.065, the law's 0.054).

Every graded line is in `x56_law_floor.out` / `_results.json`. The per-scorer copies' own outputs are `x56_x4?copy_*`.
