# MF1_h2_cooling_floor_mass: H2 cooling gives lg M_f ~ 6.2–6.6, near PC1's window, but the grade cannot confirm it and the core-density variant removes the floor

Criteria: `FROZEN_CRITERIA.md` (b612d856a4, committed alone). **NOT blind:** the window and a rough estimate were known first. κ = ½ FITTED.
Footings never pooled. Route E, Newtonian. Cold dark energy, not matter; no particle species. Not "theory closed". Nothing here says the data
favour the framework. Numbers are from `mf1_cooling.out` / `mf1_results.json`, or `mf1_posthoc.out` where marked POST-HOC.

## Verdict (frozen): **canonical NOT DIAGNOSTIC; alt CONSISTENT, z-DEPENDENT.** M_f is NOT derived in the sense asked.

| z | T_crit (K) | V (km/s) | lg M_f canonical | lg M_f alt | in [6.25, 7.00] |
|---|---|---|---|---|---|
| 10 | 1337 | 4.25 | 6.551 | 6.483 | yes / yes |
| **15 (primary)** | 991 | 3.66 | 6.303 | 6.234 | yes / **no** |
| 25 | 690 | 3.06 | 6.002 | 5.933 | no / no |

T_crit comes from the chemistry; nothing was tuned. Regrade at the z = 15 M_f (Z, canonical / alt):

| class | H2 floor | atomic 1e4 K (lg M_f 8.21 / 8.15) |
|---|---|---|
| MW ultra-faint | +1.30 / +1.29 | −1.78 / **−2.62** |
| bright M31 | +1.70 / +1.55 | −1.70 / −1.48 |
| M31 others | +1.71 / +1.59 | +0.02 / −0.16 |
| MW classical | +0.91 / +0.56 | −0.02 / −0.96 |
| LG field | −0.49 / −0.95 | −1.37 / −1.76 |

- **Canonical:** the H2 floor reproduces all five classes, but so does the atomic tooth, so by the frozen rule the test has no power there.
- **Alt:** the H2 floor reproduces all five and the atomic tooth fails, but the band leaves the window, and z = 15 itself sits 0.016 dex below it.
- Spearman(E, lg M★) −0.21 / −0.26 (X49 −0.64). Systems off by > 2 s: 19 above, 4 below / 18 above, 4 below. **A floor does not remove the scatter.**

Checks K1–K5 pass. MUTATE (Λ / 1000) has no H2 solution, so the threshold caps at 1e4 K: T_crit rises and lg M_f moves by about 1.9; it bites.

## The main problem: the gas density assumption

The primary run takes the *depth* from the floor core but the *gas density* from the virial value (n 0.14 cm⁻³ at z = 15). That is inconsistent if
the core already exists. The frozen variant with gas at fair share in the core (n 268 / 392 cm⁻³) cools at the bottom of the T range (100 K), giving **lg M_f 4.39 /
4.32, far below the window, so effectively no floor at this scale.** T_crit there is a grid edge, not a measurement.

So the threshold lands near the window only if the floor core forms *after* the gas first cools, or the gas never reaches fair share in it.
The floor has no mechanism, and X81 found native 1e12 halos are cusps, so nothing in the record says which. This is the question to settle next.

## POST-HOC (no verdict depends on this)

Per-system fit on all 82 systems, on a 0.25 dex grid, with σ_int fixed at X49's own value (0.432 / 0.421 dex; this choice favours improvement over X49):

| lg M_f | χ²_σint can | χ²_σint alt | raw χ² can | raw χ² alt |
|---|---|---|---|---|
| none (X49) | 82.0 | 82.0 | 1058 | 1042 |
| 6.00 | 53.1 | 52.5 | 931 | 916 |
| 6.25 | 44.4 | 43.9 | 876 | 864 |
| 6.50 | 39.6 | 39.6 | 834 | 827 |
| 6.75 | **38.0** | **39.1** | 816 | 816 |
| 7.50 | 41.3 | 46.2 | 724 | 752 |
| 8.25 | 47.8 | 55.8 | **433** | **518** |

- With scatter included, a floor improves the fit by Δχ² ≈ 43 for one parameter, with the minimum at lg 6.5–6.75. The lower side is sharp, and z = 25 is disfavoured (Δχ² ≈ 15). The upper side
  is soft (Δχ² ≈ 4 near lg 7.5–7.75 canonical, 7.0–7.25 alt).
- **Raw χ² prefers lg ~ 8.25, not the window, and stays at hundreds for 82 systems.** The result depends on the scatter model. Unexplained scatter of about 0.4 dex is the larger problem.
- **Correction to PC1:** its window was read from a grid ending at lg 8. On this finer grid, canonical passes all five classes again at lg 8.25, so 6.25–7.00 has no sharp upper edge on canonical. Class-median Z has little power.

## Limits and deviations

- z = 15 is a choice, not derived. Lyman-Werner feedback, streaming velocity, HD and metals are not modelled.
- T_crit is computed with gas at 178 × mean density for every halo, with no Jeans filter.
- Deviation: the first MUTATE run crashed (NaN, no H2 solution), so the cap at 1e4 K was added to the mutate path only, after that run. Normal-run results are unaffected.
- A selection floor says which halos host stars. It does not explain DF1's shape result or why kinematics scatter.
