# RC100 input correction: CFG216 / CFG217 / CFG218 re-run (2026-09-29)

**Why.** The data chat's provenance check (03922e8c7) compared `real_research/data/rc100_nestorshachar2023_table3.csv` with the paper's Table 3 and found 16 rows differing in 17 cells (12 values, 5 names). Seven rows carry log M_bulge where log M_baryon belongs (58, 62, 63, 65, 77, 93, 95), rows 24 and 90 have small log M_baryon typos, V_c is wrong in rows 43 and 44, f_DM in row 36, and names in rows 24, 31, 32, 34 and 96. z, R_e and σ₀ match in all 100. I re-derived the difference list independently and it agrees cell for cell.

**What was run.** The three lanes' scripts with `RC100_INPUT=corrected`, which reads `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv`. The default (uncorrected) runs still reproduce the committed outputs, which are kept. The corrected outputs are `*_corrected*`. **The corrected file lacks no column the lanes used** (name, z, log M_bar, R_e, f_DM, V_c, σ₀); it lacks the original's derived columns (g_Re, a0 columns, deepMOND flag), which were not used.

**Which cells enter which lane.**

- The primary statistic of CFG216 and CFG217's baseline use z, R_e, V_c and f_DM only. V_c rows 43 and 44 and f_DM row 36 enter them.
- M_bar enters only CFG216's variant (d), CFG217's M★ reconstruction (C-recon, G1's reconstruction, G2 through Δ_prior) and CFG218's b_RC100.
- The names enter the RC41-overlap matching (38 of 41 before; 41 of 41 now).

## What moves materially

- **Conclusions unchanged:** CFG216's outcome is W-flat in both runs; CFG217's literal D3 is ATTACK-BROKEN (the same power artefact) in both; CFG218's classification of RC100 is 'marginal' in both, and the calibration needed for S/3 is 0.040 dex in both.
- **CFG216 slopes (nu_mono, canonical):** delta_flat -0.025 [-0.068, +0.010] to -0.025 [-0.068, +0.010]; delta_rival -0.086 [-0.125, -0.050] to -0.086 [-0.125, -0.050]. All within 0.003.
- **The 5.5 sigma and 4.9 sigma from the rival's expected slopes become 4.97 and 4.47** (from 4.97 and 4.47); the distances from the flat expectations move from 1.28 and 1.45 to 1.28 and 1.45.
- **CFG216 variant (d), which uses the M_bar column that was wrong in 9 rows:** the flat median goes from +0.028 [-0.007, +0.061] (CONSISTENT) to +0.028 [-0.007, +0.061] (CONSISTENT), and the flat slope from -0.046 [-0.104, +0.004] to -0.046 [-0.104, +0.004] (its CI now excludes 0 on the negative side). This is the biggest mover.
- **CFG216 by z-half (from the .out files):** the low-z half's flat median goes from +0.041 to +0.061; the high-z half is unchanged.
- **RC41 overlap:** 38 to 41 galaxies matched (the corrected names). The RC41 subset's flat median is +0.041 [+0.001, +0.099] (was +0.041 [+0.004, +0.109]).
- **CFG217 G2 (prior-driven f_DM) flips from 'no' to 'yes' by the frozen line:** Spearman rho +0.33 (p = 0.036) to +0.33 (p = 0.036). The z-slope after removing the Delta_prior dependence stays near zero (+0.014 [-0.027, +0.069]).
- **CFG217 C-recon is still rejected** (0.223 to 0.223 dex against the 0.15 line), so G1 still runs on the 41-galaxy overlap only and the literal D3 is unchanged.
- **CFG217 mock:** the best chi2 within the plausible 0.2 dex is 1.68 to 1.68 (still above the frozen 2); the differential mis-scaling that reproduces the flat slope moves +0.062 to +0.062 dex, and the calibration that makes the rival slope exactly 0 stays at -0.237 to -0.237 dex.
- **CFG217 post hoc gas variants:** V2's rival deficit crosses from 2.99 sigma to 3.1 sigma, so the 'survives' flag for V2 goes from NO to YES (borderline either way); V1 and V4 still reverse the result.
- **CFG218 RC100 row:** the statistical band 0.035 to 0.035 dex; b_s +0.100 to +0.097 dex; S_sys 0.080 to 0.078.
- **CFG216 post hoc index:** p = -0.72 [-1.49, +0.14] to -0.71 [-1.52, +0.15] (canonical); the rival is 4.7 sigma away (was 4.8); flat 1.7 sigma in both.

## Every quantity compared ("moves" marks any difference in the printed value, including third-decimal noise)

| lane | quantity | original | corrected | |
|---|---|---|---|---|
| CFG216 | slope of delta_flat on z (nu_mono, canonical) [95% CI] | -0.025 [-0.068, +0.010] | -0.025 [-0.068, +0.010] |  |
| CFG216 | median delta_flat [95% CI] | +0.035 [+0.009, +0.078] | +0.035 [+0.009, +0.078] |  |
| CFG216 | z-score of delta_flat's slope against 'flat true' | -1.28 | -1.28 |  |
| CFG216 | z-score of delta_flat's slope against 'rival true' | -4.97 | -4.97 |  |
| CFG216 | slope of delta_rival on z (nu_mono, canonical) [95% CI] | -0.086 [-0.125, -0.050] | -0.086 [-0.125, -0.050] |  |
| CFG216 | median delta_rival [95% CI] | -0.044 [-0.071, -0.018] | -0.044 [-0.071, -0.018] |  |
| CFG216 | z-score of delta_rival's slope against 'flat true' | -1.45 | -1.45 |  |
| CFG216 | z-score of delta_rival's slope against 'rival true' | -4.47 | -4.47 |  |
| CFG216 | expected slopes if flat true (delta_flat, delta_rival) | +0.000, -0.058 | +0.000, -0.058 |  |
| CFG216 | expected slopes if rival true (delta_flat, delta_rival) | +0.072, +0.000 | +0.072, +0.000 |  |
| CFG216 | primary outcome | W-flat | W-flat |  |
| CFG216 | (a) the RC41 subset, flat: median / slope | +0.041 [+0.001, +0.099] | +0.009 [-0.056, +0.068] | +0.041 [+0.001, +0.099] | +0.009 [-0.056, +0.068] |  |
| CFG216 | (a) the RC41 subset, rival: median / slope | -0.043 [-0.080, +0.012] | -0.051 [-0.118, +0.015] | -0.043 [-0.080, +0.012] | -0.051 [-0.118, +0.015] |  |
| CFG216 | (b) the other galaxies, flat: median / slope | +0.035 [+0.004, +0.091] | -0.053 [-0.106, -0.005] | +0.035 [+0.004, +0.091] | -0.053 [-0.106, -0.005] |  |
| CFG216 | (b) the other galaxies, rival: median / slope | -0.046 [-0.096, -0.011] | -0.109 [-0.155, -0.060] | -0.046 [-0.096, -0.011] | -0.109 [-0.155, -0.060] |  |
| CFG216 | (c) g_bar < 3 a0, flat: median / slope | +0.052 [+0.004, +0.096] | -0.036 [-0.094, +0.020] | +0.052 [+0.004, +0.096] | -0.036 [-0.094, +0.020] |  |
| CFG216 | (c) g_bar < 3 a0, rival: median / slope | -0.057 [-0.102, -0.021] | -0.105 [-0.160, -0.052] | -0.057 [-0.102, -0.021] | -0.105 [-0.160, -0.052] |  |
| CFG216 | (d) table M_bar geometry, flat: median / slope | +0.028 [-0.007, +0.061] | -0.046 [-0.104, +0.004] | +0.028 [-0.007, +0.061] | -0.046 [-0.104, +0.004] |  |
| CFG216 | (d) table M_bar geometry, rival: median / slope | -0.062 [-0.095, -0.039] | -0.102 [-0.160, -0.057] | -0.062 [-0.095, -0.039] | -0.102 [-0.160, -0.057] |  |
| CFG216 | C2: RC41 galaxies matched by name; median shift (dex) | 41; -0.043 | 41; -0.043 |  |
| CFG216 post hoc | a0(z) index p (canonical) [95%], sigma | -0.58 [-1.37, +0.26], 0.43 | -0.58 [-1.37, +0.26], 0.43 |  |
| CFG216 post hoc | flat / rival distance in sigma | 1.4 / 4.4 | 1.4 / 4.4 |  |
| CFG217 | RC41 overlap (galaxies found by name) | 38 | 41 | **moves** |
| CFG217 | C-recon: median /Delta log M*/ (dex); accepted? | 0.223; False | 0.223; False |  |
| CFG217 | G2: Spearman rho(delta_flat, Delta_prior), p; prior-driven | +0.33, 0.036; True | +0.33, 0.036; True |  |
| CFG217 | G3 alpha = 3.36: slope of delta_flat | -0.025 [-0.068, +0.010] | -0.025 [-0.068, +0.010] |  |
| CFG217 | G3 alpha = 3.36: slope of delta_rival | -0.086 [-0.125, -0.050] | -0.086 [-0.125, -0.050] |  |
| CFG217 | G3 alpha = 1.68: slope of delta_flat | -0.063 [-0.110, -0.023] | -0.063 [-0.110, -0.023] |  |
| CFG217 | G3 alpha = 1.68: slope of delta_rival | -0.118 [-0.160, -0.076] | -0.118 [-0.160, -0.076] |  |
| CFG217 | G3 alpha = 0.0: slope of delta_flat | -0.093 [-0.135, -0.044] | -0.093 [-0.135, -0.044] |  |
| CFG217 | G3 alpha = 0.0: slope of delta_rival | -0.141 [-0.189, -0.097] | -0.141 [-0.189, -0.097] |  |
| CFG217 | G5 M1: differential dlogM (dex) that reproduces the flat slope | +0.062 | +0.062 |  |
| CFG217 | G5 M2: best differential dlogM (dex); chi2 at the best beta | +0.244; 0.02 | +0.244; 0.02 |  |
| CFG217 | G5 M2: best chi2 within the plausible 0.2 dex | 1.68 | 1.68 |  |
| CFG217 | G7: residual z-slope of delta_flat | -0.023 [-0.058, +0.012] | -0.023 [-0.058, +0.012] |  |
| CFG217 | G7: residual z-slope of delta_rival | -0.087 [-0.123, -0.050] | -0.087 [-0.123, -0.050] |  |
| CFG217 | post hoc (A) V0: slope of delta_flat (all 100, reconstructed M*) | -0.025 [-0.068, +0.010] | -0.025 [-0.068, +0.010] |  |
| CFG217 | post hoc (A) V0: slope of delta_rival (all 100, reconstructed M*) | -0.086 [-0.125, -0.050] | -0.086 [-0.125, -0.050] |  |
| CFG217 | post hoc (A) V1: slope of delta_flat (all 100, reconstructed M*) | +0.069 [+0.028, +0.105] | +0.069 [+0.028, +0.105] |  |
| CFG217 | post hoc (A) V1: slope of delta_rival (all 100, reconstructed M*) | +0.000 [-0.036, +0.036] | +0.000 [-0.036, +0.036] |  |
| CFG217 | post hoc (A) V2: slope of delta_flat (all 100, reconstructed M*) | +0.014 [-0.025, +0.053] | +0.014 [-0.025, +0.053] |  |
| CFG217 | post hoc (A) V2: slope of delta_rival (all 100, reconstructed M*) | -0.053 [-0.090, -0.014] | -0.053 [-0.090, -0.014] |  |
| CFG217 | post hoc (A) V3: slope of delta_flat (all 100, reconstructed M*) | -0.076 [-0.118, -0.040] | -0.076 [-0.118, -0.040] |  |
| CFG217 | post hoc (A) V3: slope of delta_rival (all 100, reconstructed M*) | -0.125 [-0.162, -0.087] | -0.125 [-0.162, -0.087] |  |
| CFG217 | post hoc (A) V4: slope of delta_flat (all 100, reconstructed M*) | +0.054 [+0.013, +0.098] | +0.054 [+0.013, +0.098] |  |
| CFG217 | post hoc (A) V4: slope of delta_rival (all 100, reconstructed M*) | -0.019 [-0.060, +0.023] | -0.019 [-0.060, +0.023] |  |
| CFG217 | post hoc (A) V5: slope of delta_flat (all 100, reconstructed M*) | -0.054 [-0.096, -0.019] | -0.054 [-0.096, -0.019] |  |
| CFG217 | post hoc (A) V5: slope of delta_rival (all 100, reconstructed M*) | -0.109 [-0.145, -0.070] | -0.109 [-0.145, -0.070] |  |
| CFG217 | post hoc (B): dlogM that makes the rival slope 0 / the flat slope 0 | -0.237 | -0.063 | -0.237 | -0.063 |  |
| CFG217 | D3 (literal, frozen) | ATTACK-BROKEN | ATTACK-BROKEN |  |
| CFG218 | MUSE-DARK (unchanged by construction): signal / S_sys | 0.092 | 0.300 | 0.092 | 0.300 |  |
| CFG218 | RC41 (unchanged by construction): signal / S_sys | 0.083 | 0.043 | 0.083 | 0.043 |  |
| CFG218 | NOEMA3D (unchanged by construction): signal / S_sys | 0.048 | 0.043 | 0.048 | 0.043 |  |
| CFG218 | CRISTAL (unchanged by construction): signal / S_sys | 0.288 | 0.038 | 0.288 | 0.038 |  |
| CFG218 | RC100: signal / stat band / b_s / S_sys / calibration for S/3 | 0.094 | 0.035 | +0.100 | 0.080 | 0.040 | 0.094 | 0.035 | +0.097 | 0.078 | 0.040 | **moves** |
| CFG218 | RC100 classification | marginal | marginal |  |
