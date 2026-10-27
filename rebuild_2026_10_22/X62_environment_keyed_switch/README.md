# X62_environment_keyed_switch: the environment key fixes the hosted dwarfs; c_f decides the rest, and nothing passes at any c_f

Criteria: `FROZEN_CRITERIA.md` (8c7768d26d, committed alone; owner request 10-27). Machinery: X58 (c3b4f2c7d9).
No amendment. κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter. Not "theory closed". Nothing here says
the data favour the framework.

Folder note: this lane shares its number with another session's `X62_displacement_forest_prediction`. Cite this lane by
its full folder name.

**Hypothesis ENV:**
- **Route-E halo:** the system is a satellite (X1 host MW or M31) or lies above X43's crossover.
- **The law on baryons, no halo:** every other system.
- SPARC, lensing, groups and clusters keep X58's crossover flag. Only the dwarfs change.

## Verdict (frozen, primary c_f = X48 A2 nine-seed): **ENV FAILS** on both footings

| line | primary A2 c_f (canonical / alt) | reported: X58 3-seed | reported: c_f = 4 |
|---|---|---|---|
| SPARC (median Υ) | **FAIL** (0.32 / 0.32) | pass (0.56 / 0.50) | pass / **FAIL** (0.54 / 0.44) |
| groups | pass (Z +1.33) | pass (+1.53) | **ABOVE LAW** (+2.02) / pass |
| clusters | **G-IN-all, G-MID-T1, G-IN-Mall OVER** (Z −3.52) | G-IN-Mall OVER (−2.41) | **G-OUT-M3 UNDER** (+2.41) |
| dwarfs, five classes | all pass / **UFD OVER −2.77** | same | same |
| lensing Δχ²(ENV2H − L2H) | **+463.6 / +492.9** | **+432.5 / +452.3** | **+22.5** / 0.0 |

**Checks 7/7.**
- K0: route E everywhere reproduces X48 A2, X53 and X51.
- K2: the law everywhere reproduces EM1 LAW and X53 L.
- K1: 12 430 calls, 0 violations.
- K3: 0.65 GB.
- `--mutate` (flag inverted) fails K1, exit 1.

## What it means

1. **The environment key repairs the dwarfs.**
   - X58 (dwarfs on the law) had MW UFD Z +5.2. Here, with satellites on X51 halos, canonical passes all five classes; alt
     keeps X51's own UFD overshoot.
   - The LG field class passes on the law, class median +0.046 / +0.007. The class median hides individuals, though.
     **Leo T +0.41 ± 0.14 and Phoenix +0.40 ± 0.07** (canonical; alt +0.37, +0.35) sit above the law, X1's iso column.
     So X24's finding that isolated dwarfs need the extra too holds system by system. The environment key is not clean.
2. **Everything else is the c_f problem.**
   - **Native c_f (A2 or 3-seed):** the crossover falls below the KiDS lenses, which then carry route-E halos and fail
     lensing by +430 to +490. Native A2 also breaks SPARC and three cluster keys.
   - **c_f = 4:** lensing nearly passes (+22.5 canonical, 0 alt). But the groups (canonical), G-OUT-M3 and SPARC alt fail.
   - **No c_f tried passes every line on both footings.**
3. **The tension is internal to the halo branch.**
   - At low c_f the lensing galaxies stay on the law, but clusters lose the inner/outer balance.
   - At native c_f the clusters' inner band over-predicts.
   - So the halo core rule itself, not the switch, is the limiting piece. That matches IB1 (cores 2.5× too dense against
     gas hydrostatic equilibrium).

Graded lines: `x62_env_switch.out` / `x62_env_switch_results.json`.
