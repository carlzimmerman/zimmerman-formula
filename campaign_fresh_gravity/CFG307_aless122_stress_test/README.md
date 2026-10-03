# CFG307 — stress test of ALESS 122.1's implied a₀: NOT ROBUST

> **Owner request: "stress test it".** This is a stress test of one galaxy. It is descriptive, and the implied a₀ is not a measurement of a₀(z). **κ = ½ is FITTED.** FLAT a₀(z) is the framework's distinctive law, a₀ ∝ H(z) is the rival, and ΛCDM has no a₀. Only framework-native inputs are used: no halo-fit quantity enters a cell. Nothing was downloaded. No sentence here says the data favour a law, and a NO-ROOT cell says something about the baryons against the dynamics, never about a₀.
> **Criteria:** `FROZEN_CRITERIA.md`, committed as **3b1ca88f7** before any cell was computed.
> **Code:** CFG229's committed inputs, estimator and random stream, all replayed exactly.

## Bottom line
1. **Decision under the frozen rule: NOT ROBUST.** Over the 540-cell grid, both NOT ROBUST triggers fire:
   - no nominal root in **43.7 %** of cells (the threshold is 25 %);
   - FLAT inside the 95 % interval in **29.3 %** (threshold 25 %);
   - FLAT excluded from above in only **27.0 %**, and H(z) in **14.6 %** (ROBUSTLY ABOVE BOTH would need 80 % and 50 %).

   Every side reading gives the same verdict: the all-draws convention, the alt footing, the 2 r_e-only subgrid (no root 27 %, FLAT inside 33 %, FLAT excluded 40 %, H(z) excluded 24 %) and the one-axis-at-a-time set.
2. **The committed cell is CFG229's result, exactly** (C1, bit-level): s★ = 8.82 (log₁₀ 0.945356), 68 % 4.20–14.37, 95 % 1.51–22.64, no-root fraction 0.0103.
   - Counting the 1 % no-root draws as s → 0 lowers the 95 % lower bound to **1.07**, so FLAT is excluded only barely, even in the committed cell.
3. **The gas axis moves s★ most, and it removes the root.**
   - The committed gas is Dunne+22's per-galaxy optimised value. Its α_CO = 1.41 is the lowest of the six CO galaxies in the class (2.64–4.60), and its κ_H = 3362 is the highest of the six galaxies with a κ_H (1199–2038).
   - With Dunne's own single-tracer CO conversion (SMG row, α_CO 3.8), s★ = **1.16** (95 % 0.10–7.8): FLAT and H(z) are both inside.
   - With the record's α_CO 3.6, s★ = **1.76**. With α_CO 4.36 there is **NO ROOT**.
   - With Dunne's single-tracer dust conversion, s★ = **15.7**; with α_CO 0.8, **22.7**.
   - The CO tracer and the dust tracer disagree by about 0.5 dex in gas mass for this galaxy, and the root depends on which one wins.
4. **The other axes, in order:**
   - **Radius:** at r_e, s★ = **0.35**, D = 1.02 at the floor, and 51 % of MC draws have no root.
   - **Pressure:** rotation only gives **2.7** (FLAT and H(z) inside), the constant 1.68 σ² gives 5.4, the measured σ = 129 km/s gives 6.5, and Burkert's 3.36 σ² R/r_e gives 17.9.
   - **Inclination:** 6.2 to 12.4.
   - **M\*:** 6.6 to 10.6.
5. **Siblings: 4 of 6 gain a root somewhere, but only at stacked extremes.**
   - ALPAKA 19, ALPAKA 22 and BX610 root only with the α_CO 0.8 gas, in 5, 30 and 15 cells; ALPAKA 22 and ALPAKA 19 also need i_used − 1σ.
   - ALPAKA 18 roots in 187 cells, 180 of them at i = 8° (its 26° − 18°).
   - ALPAKA 15 and 20 never root.
6. **Is ALESS 122.1 the outlier of a common calibration? Yes.** Under every one of the 24 shared recipes (4 pressure forms × up to 6 gas recipes, each galaxy at its committed M\*, inclination and radius), ALESS 122.1 has the **largest D of the seven**. Its gap to the largest sibling is a median **+0.40 dex** (range +0.17 to +0.97).
   - In 17 of the 24 recipes, ALESS 122.1 is the only galaxy with a root. In the other 7 (the CO-based recipes under the weaker pressure forms), no galaxy roots, ALESS included.
   - No shared recipe gives the siblings a root.
7. **Controls:**
   - Main run: 11/11 pass (C1, C1b, C2a–c, C3–C8).
   - MUTATE (V × 0.7): 10/10 pass. M1: every cell equals the independent inversion at D × 0.49. M2: every cell that keeps a root has a smaller s★. The committed cell loses its root (D 0.936), and 103 of 540 cells keep one.
   - Hand estimates: **13 of 14 reproduce.** H11 is WRONG, because ALPAKA 18's rooted fraction is 0.26, not < 0.15. H13 is scored in the MUTATE run.

**Plain reading.** ALESS 122.1's s★ = 8.82 is one corner of the record's own choices. The same record's other choices for its gas tracer, its radius and its pressure term give anything from no root through FLAT-compatible values (about 0.35–2.7) to about 20. Taken together, the grid puts ALESS 122.1 neither above FLAT nor above H(z) robustly.

## One axis at a time about the committed cell (canonical footing; CFG229-convention intervals)
| axis | level | V (km/s) | y | D | s★ | 95 % | MC no-root | FLAT | H(z) |
|---|---|---|---|---|---|---|---|---|---|
| — | **committed** (EQ8, G0, M\*, 55°, 2 r_e) | 533.0 | 4.84 | 1.911 | **8.82** | 1.51–22.6 | 0.010 | excluded above | inside |
| pressure | P0 (rotation only) | 448.6 | 4.84 | 1.354 | 2.69 | 0.20–9.6 | 0.149 | inside | inside |
| pressure | C168 (1.68 σ²) | 492.6 | 4.84 | 1.632 | 5.38 | 0.60–15.4 | 0.041 | inside | inside |
| pressure | P1 (3.36 σ² R/r_e) | 605.7 | 4.84 | 2.468 | 17.9 | 4.72–41.8 | 0.001 | excluded | excluded |
| pressure | MSIG (σ = 129) | 507.1 | 4.84 | 1.730 | 6.50 | 0.90–17.8 | 0.025 | inside | inside |
| gas | CO1 (Dunne single CO, α 3.8) | 533.0 | 8.48 | 1.091 | 1.16 | 0.10–7.8 | 0.363 | inside | inside |
| gas | DU1 (Dunne single dust) | 533.0 | 3.47 | 2.668 | 15.7 | 4.82–33.1 | 0.000 | excluded | excluded |
| gas | A08 (α_CO 0.8) | 533.0 | 2.70 | 3.426 | 22.7 | 7.13–48.7 | 0.000 | excluded | excluded |
| gas | A36 (α_CO 3.6) | 533.0 | 8.09 | 1.143 | 1.76 | 0.14–8.4 | 0.286 | inside | inside |
| gas | A436 (α_CO 4.36) | 533.0 | 9.56 | 0.968 | NO ROOT | — | 0.589 | — | — |
| M\* | +0.21 dex | 533.0 | 5.56 | 1.663 | 6.58 | 0.78–19.1 | 0.045 | inside | inside |
| M\* | −0.21 dex | 533.0 | 4.40 | 2.104 | 10.6 | 2.40–25.9 | 0.004 | excluded | inside |
| inclination | 49° | 565.6 | 4.84 | 2.152 | 12.4 | 2.75–30.2 | 0.004 | excluded | inside |
| inclination | 63° | 502.9 | 4.84 | 1.701 | 6.16 | 0.82–17.0 | 0.030 | inside | inside |
| radius | r_e (5.31 kpc) | 409.5 | 10.67 | 1.023 | 0.352 | 0.11–10.5 † | 0.507 | inside | inside |

† The r_e interval comes from the rooted draws only (CFG229's convention). With 51 % of draws having no root, the rooted-draw 68 % range (0.84–5.86) does not even contain the nominal 0.35. The all-draws 95 % interval is 0 to 8.8.

## Decision table (`cfg307_stress.out`)
| set | N | FLAT excl. | H(z) excl. | FLAT inside | no root | decision |
|---|---|---|---|---|---|---|
| **primary** (gates the wording) | 540 | 0.270 | 0.146 | 0.293 | 0.437 | **NOT ROBUST** |
| all draws (no-root → s = 0) | 540 | 0.215 | 0.143 | 0.348 | 0.437 | NOT ROBUST |
| alt footing (FLAT at s = 1.2085) | 540 | 0.246 | 0.128 | 0.317 | 0.437 | NOT ROBUST |
| 2 r_e only | 270 | 0.400 | 0.244 | 0.330 | 0.270 | NOT ROBUST |
| one axis at a time | 15 | 0.400 | 0.200 | 0.533 | 0.067 | NOT ROBUST |

- **Rooted cells:** 304 of 540, with median s★ 6.65; the 5–95 % range of the rooted cells is 0.49–29.4 and the full range 0.070–63.3.
- **Overlap:** 158 cells have both laws inside the 95 % interval. 67 cells have FLAT excluded with H(z) inside.
- **Per gas level** (cells with a root / FLAT excluded / H(z) excluded, out of 90 each): G0 66/21/8, CO1 22/2/0, DU1 86/54/28, A08 89/66/43, A36 27/3/0, A436 14/0/0.
- **The r_e slice:** every CO-based gas cell has no root.

## Axis ranking (frozen rule)
| rank | axis | removes the root? | rooted one-axis range |
|---|---|---|---|
| 1 | gas | **yes** (A436) | 1.29 dex |
| 2 | radius | no | 1.40 dex |
| 3 | pressure | no | 0.82 dex |
| 4 | inclination | no | 0.30 dex |
| 5 | M\* | no | 0.21 dex |

In the full grid, the root fraction runs from 0.16 to 0.99 across the gas levels, 0.40 to 0.73 across the radii, and 0.38 to 0.75 across the pressure forms.

## Beside (excluded from the grid by the criteria; printed only)
| change from the committed cell | s★ | 95 % |
|---|---|---|
| Dunne's luminosity-dependent CO fit | 1.64 | 0.14–10.4 |
| Dunne's luminosity-dependent dust fit | 15.2 | 4.0–35.6 |
| parent-table gas 11.30 (Calistro Rivera+18; conversion not on disk) | 11.8 | 2.6–28.5 |
| Amvrosiadis α_CO 0.92 (halo-anchored, f_DM = 0.25: **excluded**) | 20.2 | 5.9–45.9 |
| M\* ±0.30 dex (CFG229's declared band) | 5.49 / 11.2 | — |
| Burkert P1 form with σ = 129 | 11.7 | — |
| P2 kernel (committed cell) | 12.8 | — |

## Siblings (`cfg307_siblings_grid.csv`)
| galaxy | cells | committed D | max D | cells with a root | what the roots need |
|---|---|---|---|---|---|
| ALPAKA 15 | 360 | 0.204 | 0.535 | 0 | — |
| ALPAKA 18 | 720 | 0.277 | 10.4 | 187 (26.0 %; 30 at the s★ > 10³ LIMIT) | 180 of them at i = 8° (i_used − 1σ); 7 with α_CO 0.8 + M\* − 1σ at i_used or i_alt |
| ALPAKA 19 | 720 | 0.294 | 1.05 | 5 (0.7 %) | α_CO 0.8 + M\* − 1σ + i − 1σ; s★ 0.04–1.0 |
| ALPAKA 20 | 360 | 0.289 | 0.598 | 0 | — |
| ALPAKA 22 | 720 | 0.269 | 1.75 | 30 (4.2 %) | α_CO 0.8 + i = 17.5° |
| BX610 | 360 | 0.456 | 1.85 | 15 (4.2 %) | α_CO 0.8 (+ M\* − 1σ or i − 1σ); s★ 0.65–6.3, FLAT inside in all 15 |

Shared recipes: in all 24 (`cfg307_stress.out`, COMMON-CALIBRATION block), ALESS 122.1 has rank 1 in D. Under MUTATE only ALPAKA 18 (at i = 8°) keeps any root.

## Controls (main 11/11; MUTATE 10/10)
- **C1:** the committed cell equals CFG229, with max |Δq| = 0.
- **C1b:** the replayed stream reproduces CFG229's MC for all seven galaxies (Δ = 0).
- **C2a–c:** the source constants are parsed from the Amvrosiadis and Dunne TeX and match the repo CSVs.
- **C3:** the eq.-8 and arctan reconstructions return 533 km/s and V_rot(2 r_e) to 1e-9.
- **C4:** all 304 rooted cells match an independent brentq inversion to 1e-6 dex.
- **C5:** the Hankel disc force matches the closed form at both radii.
- **C6:** no direction violations.
- **C7:** the bookkeeping sums to 1.
- **C8:** the siblings' committed D equals CFG229's (Δ = 0).
- **MUTATE M1/M2:** pass. The mutation propagates exactly as predicted, cell by cell.

## Disclosures (kept)
- **Post hoc fix after the first run.**
  - The bug: the sibling block counted cells at the bracket LIMIT (s★ > 10³) as "no root", although the criteria count a LIMIT as a root above both laws. That covered 30 ALPAKA 18 cells.
  - The fix: the first-run outputs are kept as `cfg307_stress_firstrun.out`, `cfg307_stress_MUTATE_firstrun.out` and `cfg307_siblings_grid_firstrun.csv`.
  - What changed: only ALPAKA 18's count (157 → 187) and the alt-footing label (1.2086 → the exact ratio 1.2085).
  - What did not change: the ALESS 122.1 grid CSVs and the MUTATE sibling CSV are byte-identical to the first run.
  - H11 was WRONG in both runs.
- **The 1.2086 in the criteria** is CFG229's rounding. The code uses the exact footing ratio, 1.1312/0.93603 = 1.2085.
- **The r_e level rests on a reconstruction.** r_t is not tabulated, so it was solved from the published V_max, V_circ and σ, which are posterior summaries. The 2 r_e-only decision is printed for this reason, and it is also NOT ROBUST.
- **σ = 129 km/s** is Calistro Rivera+18's image-plane fit, quoted by Amvrosiadis+, who say its error is underestimated.
- **The full factorial weights every declared level equally.** The fractions describe how much the record's own choices spread, not a probability.
- **σ_int (0.15 dex)** is in no interval, as in CFG229.
- **MC simplifications:** σ is held fixed in the MC, and the velocity scatter is proportional (V_cell × V_draw/533).
- **Hand estimates were made before freezing.** Before the freeze I evaluated ν_mono at seven y values to sharpen the hand estimates; no lane quantity was computed then.

## Files
- **Criteria:** `FROZEN_CRITERIA.md` (3b1ca88f7).
- **Script:** `cfg307_stress.py`, which runs in about 80 s.
- **Main run:** `cfg307_stress.out` + `cfg307_stress_results.json` + `cfg307_grid.csv` (540 cells) + `cfg307_siblings_grid.csv` (3,240 cells).
- **MUTATE run:** `cfg307_stress_MUTATE.out` + `cfg307_stress_results_MUTATE.json` + `cfg307_grid_MUTATE.csv` + `cfg307_siblings_grid_MUTATE.csv`.
- **First run:** the `*_firstrun.*` files above.
- **Run:** `python3 campaign_fresh_gravity/CFG307_aless122_stress_test/cfg307_stress.py`, then the same command with `MUTATE=1`.
- **Reads:** CFG229's committed input CSVs and results JSON, `data_assembly/` tables, and the Amvrosiadis and Dunne TeX in the external data directory beside the repo.
