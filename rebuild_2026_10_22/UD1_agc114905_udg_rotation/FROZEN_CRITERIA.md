# UD1: the a0 law on the gas-rich ultra-diffuse galaxy AGC 114905 (FROZEN CRITERIA)

Committed alone, before any script, fetched table or number of this lane exists in the repository. κ = ½ is FITTED. Not
theory closed. Footings never pooled. Not blind: the published claim (the galaxy rotates too slowly for MOND-type laws at
the published inclination) is known from memory. Adopts nothing.

## 0. Why

Owner 2026-11-04 asked for the galaxies with the lowest mass per area. The record has the dispersion-supported ones
(Crater II, Antlia 2, DF2, DF44) but no isolated, gas-dominated, rotation-supported ultra-diffuse disc. AGC 114905 is
the best-known one and a published problem case for MOND-type laws. Record check (grep over campaign_fresh_gravity,
rebuild_2026_10_22, data_assembly): 0 files name AGC 114905. One galaxy excludes nothing (owner rule): the output is a
single-object label, not a verdict on the law.

## 1. Data (fetched after this commit)

- **Primary:** Mancera Piña et al. 2022 (MNRAS; arXiv:2112.00017, id from memory, confirmed at fetch): observed rotation
  curve V(R) with its published errors, the gas and stellar contributions V_gas(R), V_*(R) (or the gas surface density and
  stellar mass and profile from which they are built), the published inclination i0 ± σ_i, distance and stellar mass with
  its error. Taken as published: no refit of their cube.
- **Secondary:** any later table by the same team on the same galaxy found during the fetch is reported beside, never
  pooled with the primary.
- If the primary has no tabulated rotation curve and baryon curves, the lane stops as NOT EVALUABLE (no digitising).

## 2. The law

g = ν(g_b/a0) g_b with ν(y) = ½ + √(¼ + 1/y), as LW1/C4. g_b from V_b² = V_gas² + V_*² as published (their helium factor,
their stellar mass-to-light or stellar mass). Both footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻²,
reported separately. No free parameter is fitted to the rotation curve.

## 3. Grade (per footing, at the published i0 and published M*)

- χ² of V_obs against V_law over all published points, with published errors only.
- **CONSISTENT** if p ≥ 0.05; **FAIL** if p < 0.01; **TENSION** between.
- Reported beside, not graded: the same at M* ± its published 1σ.

## 4. Inclination (the known weak point)

V_obs scales as sin(i0)/sin(i). Reported per footing:
- i_best: the inclination minimising χ² (scan 5°-90°, step 0.1°), and the range where p ≥ 0.05.
- **RESCUED WITHIN ERRORS** if that range overlaps [i0 − 2σ_i, i0 + 2σ_i]; otherwise **NOT RESCUED**, with the distance
  from i0 in units of σ_i.
- The published i0 label in §3 stands as the primary label; §4 is the stated escape and is graded as hard.

## 5. External field (reported, not graded)

The galaxy is described as isolated; primary run uses no external field. Sensitivity: LW1's E2 1-D form
g = ν(|g_N + g_e|)(g_N + g_e) − ν(g_e) g_e at g_e/a0 = 0.01 and 0.03, stated as assumed values, not measured.

## 6. Checks (a failed check means no clean label)

- **K0** reproduce the published Newtonian baryon curve (or its points) from the fetched inputs to 2 %.
- **K1** grep the script: no fitted M/L, no fitted a0, no fitted distance.
- **MUTATE** ν ≡ 1 (Newton): must give a worse χ² than the law at i0 on both footings; outputs written to separate files.
- **Rerun** byte-identical outputs.

## 7. Prior art (from memory, unverified until fetched)

Mancera Piña et al. 2019/2022 (rotation below the baryonic Tully-Fisher relation; MOND fit needs a much lower
inclination); Banik et al. 2022 and Sellwood & Sanders 2022 (inclination may be overestimated). Cited as context only.

Output: table per footing (χ², p, label, i_best, rescue label), EFE rows, checks. Nothing is a verdict on a theory.
