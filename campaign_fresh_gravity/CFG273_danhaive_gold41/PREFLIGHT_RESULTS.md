# CFG273 stage 1 — the blind pre-flight: with stars-only baryons 37 of the 41 Danhaive+25 discs are well-conditioned (y from 0.08 to 8.8), but the gas the table lacks would move them into the Newtonian regime

> **κ = ½ FITTED. No M_dyn, σ₀ or v/σ₀ column was loaded; no g_obs, D, δ or s\* of any disc was formed. A forecast, not a measurement. No sentence says the data favour a law.**
> Criteria `FROZEN_CRITERIA.md` (**92a868901**). Script `cfg273_danhaive_gold41.py` (shared `../HZQ_common/hzq_core.py`); outputs `cfg273_stageA.out`, `cfg273_stageA_results.json`.

## Bottom line
1. **The stars-only baryon side is in the intermediate regime for most rows — unlike lanes C and E.** y = g_bar/a₀ at r = r_e (one exponential disc, R_e,\* = r_e): **min 0.08, 16 / 50 / 84 % = 0.29 / 1.65 / 3.69, max 8.80**; ν_mono(y) 1.08–4.1. **Seven rows have y < 0.3 (deep points: 1087148, 1065488, 1091580, 1086992, 1014130, 1079264, 1029814, all with log M\* ≤ 9.4 and the lowest M\*), four have y > 6, one y > 8.** The noiseless-world lever is −1.3 to −8.5 for 37 rows (conditioned) and **−12.4, −12.4, −12.7, −25.2 for the four ILL-CONDITIONED rows, 1088814, 1085659, 1091153, 1082948 (log M\* 10.17–10.68)**. By z: Pz1 median y 1.44 (3 ill), Pz2 0.93 (1), Pz3 2.37 (0).
2. **CFG240 reading (7b73ef6a0).** The pooled sample reaches y ≈ 0.08 and y ≈ 8.8, i.e. it contains deep points and points near the break-even y ≳ 8 — the design the theorem says is needed — so a pooled implied a₀ is conditioned *if the baryon calibration were known*. T4 (σ(log a₀) ≥ 3σ/√N with the calibration f free): at σ = 0.2 dex per galaxy **0.094 dex (N = 41), 0.131 (21), 0.173 (12), 0.212 (8)** — the floor the baryon calibration imposes even on a perfect design. **But the baryons used are a lower limit:** the scaling-relation gas of B2 (μ_mol of order 1.2–14, median B2/B0 g_bar ≈ 4.5) raises g_bar by factors 2–15 and puts the median y(B2) at 6.8 (near-Newtonian): **the regime of this lane is decided by the gas the table does not give.**
3. **Coverage (noiseless world, a declared 0.15 dex error on log M_dyn, the published M\* errors, r_e fixed): for the 37 conditioned rows the median 68 % coverage is 0.71 and the 95 % coverage 0.94** (the minimum 68 % coverage over all rows is 0.10, the ILL-CONDITIONED ones); the median 68 % half-width of s\* is 0.50 dex.
4. **Knobs move g_bar by the same factor in every row** (the stellar scale is tied to r_e): compact stars r_e/1.58 +0.203 dex, R_e × 1.5 −0.267, R_e / 1.5 +0.186, spherical −0.097.

## Decisions (the frozen map)
- **PF-D1 ESTIMATOR VALIDATED: True** (C1–C5 pass). **PF-D2 ILL-CONDITIONED: 4 of 41** (1088814, 1085659, 1082948, 1091153). **PF-D3 DRAWABLE as an upper bound: 37 of 41** (each an upper bound on s\*, never a measurement).

## Controls
- **C1 (41 rows, z bins 21 / 12 / 8, the three CRISTAL-08 candidates present), C2 (Freeman, `gdisc` equal to CFG229's), C3 (CFG235's committed counts: 41 Danhaive rows), C4 (estimator bit-equal to CFG223's), C5 (noiseless identity 2e-15) pass;** C6 passes for the conditioned rows (reported).
- CFG273 has no committed g_bar to compare with (the rows were "listed without a point" in CFG227); the M5 control at stage B compares the rebuilt V with the published M_dyn instead.

## Hand estimates (frozen before any number; kept as they fall)
- **HE1 hit** (median y 1.65 in [0.7, 4]; 37 conditioned rows ≥ 33; the four ILL-CONDITIONED rows are the most massive, log M\* ≥ 10.17). **HE2 hit** (seven rows with y < 0.3, at least three). HE3–HE7 are scored at stage B.

## Disclosures
- Only z, M\* and its errors, r_e and its errors, log SFR and the ids were loaded at stage A (`usecols`); no M_dyn, σ₀ or v/σ₀. CFG235's committed sample counts were read for C3 (counts only).
- The three CRISTAL-08 z-candidates (1088814, 1077545, 1086406) are flagged, not removed (P38 at stage B); 1088814 is one of the four ILL-CONDITIONED rows.
