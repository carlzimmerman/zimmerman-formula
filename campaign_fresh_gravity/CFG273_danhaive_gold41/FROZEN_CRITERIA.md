# CFG273 — FROZEN CRITERIA: implied-a₀ upper bounds (or no-root floors) for the 41 Danhaive+25 "gold" JADES discs (z 3.80–5.82), stars-only baryons, class D (no gas)

**This file is committed before any CFG273 script exists and before this lane has computed any g_obs, D or implied-a₀ scale of the 41 discs.** It is **NOT blind** in the sense of §0.

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival, ΛCDM has no a₀ (PROXY = CFG223's effective-a₀ curve). The table carries NO gas mass, NO inclination and NO rotation-velocity column: the baryons used are a LOWER LIMIT (stars only) and the dynamics are the authors' own M_dyn, so an implied a₀ is an UPPER BOUND on s\* when a root exists and a NO ROOT is robust. Class D: no law statement is made. No sentence in the outputs says the data favour a law.**

Request (the owner, relayed 2026-10-01 by the "High-z kinematic corpus analysis" session): lane D — the Danhaive+25 gold 41 (CFG273): "no rotation-velocity column (rebuild V = (v/σ₀)·σ₀; 17 σ₀ limits), no gas (class D); cross-match CRISTAL"; deliverable a results JSON and a points CSV in the `chart_a0z_points.csv` shape. Nothing is fetched.

## 0. What the record already holds and what I have read (disclosure)
1. **From the data card of this lane (baryon and geometry columns, counts; no per-galaxy D):** 41 rows, z 3.80–5.82 (median 4.17), log M\* 8.01–10.68 (median 9.46; errors median +0.16 / −0.24, no limits), r_e 0.84–3.42 kpc (median 1.32; the Hα size: the paper's size prior is the UV size × 1.58), σ₀ upper limits on 17 of 41 rows, `logMdyn_lim` and `v_over_sigma0_lim` empty for all rows although the paper marks v/σ₀ a lower limit where σ₀ is a limit; M\* by Prospector (nonparametric SFH; IMF unstated; outshining can bias it low); M_dyn = 1.8 r_e v_c²/G with v_c² = v_rot² + 3.36 σ₀² (D25:378–389), so **the paper's M_dyn already carries the pressure term**; the table's z-only coincidences with CRISTAL-08 (1088814, 1077545, 1086406; unresolved; CRISTAL-08 is in ECDFS, so only the GOODS-S rows could match).
2. **CFG197 (via the data card):** a gas-free floor on M_dyn(<r_e)/M\* for the 41 rows, both laws CONSISTENT; V = (v/σ₀) × σ₀ reproduces the paper's M_dyn to a median +0.008 dex on the 24 σ₀-detected rows only. **CFG235 (data card + `CFG235_00_sample.out`, read):** all 41 scored as stars-only floor rows, one flag (1082948), nothing survives the trials correction; known low-M_dyn rows 1082948, 1009935, 1015956, 1085659 (three of them σ₀ limits); frozen rule 3.5: M_dyn upper limits at face value, σ₀ limits already inside the table's M_dyn. **CFG227:** "listed without a point (no gas)". **I have read no per-galaxy g_obs, g_bar, D or δ of these rows.**
3. **CFG240 (7b73ef6a0) cited as the conditioning theorem:** Lean `T3_newton_limit` / `T3_newton_limit_a0` (for ν → 1 at large y the a₀ dependence disappears), `T4_sigma_floor` (σ(log a₀) ≥ 3σ/√N with the calibration f free) and the break-even table (a sample needs points with y ≳ 8 and deep points to reach 0.1 dex; with no point below y_min = 0.1 it never does). **A rough hand calculation made while designing, before any number was computed:** stars only, in one exponential disc at r = r_e, gives y of order 1–3 for the typical low-mass disc (M\* ≈ 10^9.5, r_e ≈ 1.3 kpc) and 5–10 for the most massive ones: **an intermediate regime, not the near-Newtonian one of lanes C and E.**
4. The machinery of CFG272/CFG274 (`HZQ_common/hzq_core.py` and their scripts) is reused read-only.

## 1. Data (all on disk)
`data_assembly/arxiv_tables/danhaive2025_gold.csv` (41 × 26). Stage A loads only `jades_id, z, logMstar (+errors), logSFR, re_kpc (+errors)`; the columns `v_over_sigma0`, `sigma0_kms`, `logMdyn` (+ errors and flags) are loaded at stage B only.

## 2. Rows (fixed here)
- **41 galaxy rows** (no selection; flags per row: σ₀ limit, CRISTAL-08 z-candidate, the four known low-M_dyn rows, M\* lower error ≥ 0.3 dex).
- **Pooled rows (never the headline of a single galaxy):** **PALL** (all 41), **PDET** (the 24 σ₀-detected), **Pz1** (3.8 ≤ z < 4.2, 21), **Pz2** (4.2 ≤ z < 5.0, 12), **Pz3** (z ≥ 5.0, 8), **P38** (PALL without the three CRISTAL-08 z-candidates, secondary). z of a pooled row = the median z of its members.

## 3. g_obs, g_bar and the gas route
- **g_obs = G M_dyn / (1.8 r_e²)** at r = r_e (= v_c²/r_e with the paper's v_c² = v_rot² + 3.36 σ₀², pressure included once), M_dyn the published value at face value (σ₀-limit rows included, CFG235's rule 3.5); G = 4.30091e-6 kpc (km/s)² M⊙⁻¹.
- **Headline baryons B0 = STARS ONLY (a lower limit):** M\* in one thin exponential disc (Freeman, R_d = r_e/1.678) with R_e,\* = r_e (the Hα size, the most extended plausible stellar disc), g_bar at r = r_e (CFG229's `gdisc`). **A root with B0 is an UPPER bound on s\*; a NO ROOT with B0 is robust against any added gas.**
- **Sensitivity B2 (class D scaling-relation gas, an extrapolation labelled as such):** M_gas = μ_mol(z, M\*) M\* with CFG236's μ_mol (log₁₀ μ = 0.06 − 3.3 (log₁₀(1 + z) − 0.65)² − 0.41 (log₁₀ M\* − 10.7); calibrated at z ≲ 4; used here at z 3.8–5.8), in the same disc. B2 is not a limit.
- D = g_obs/g_bar; the headline row is B0.

## 4. Estimator and statistics (the programme's, as CFG272/274)
- **s\*** = CFG223's median-residual root (CFG229's a0implied, ν_mono, canonical 9.3603e-11); a root only if the row's D > 1, otherwise NO ROOT; absolute a₀ footing-independent (M1).
- **Per-galaxy Monte Carlo (B = 10,000, seed = crc32(row label) mod 100000):** log M_dyn by a split-normal with its published errors; log M\* by a split-normal with its published asymmetric errors; r_e held fixed (the CFG229 convention); percentiles over the draws that have a root with the fraction without a root reported; a row whose central estimate has no root is NO ROOT whatever its draws do. **Pooled rows:** galaxy bootstrap, B = 10,000, central values.
- **δ_FLAT**, **Δ_floor = log₁₀ D**, **the baryon shift for s\* = 1** and **the gas-to-stars ratio required for s\* = 1**, 10^Δ₁ − 1 (positive: the extra baryons, as gas, that the FLAT canonical law needs; compared with B2's μ_mol), per galaxy.
- **ILL-CONDITIONED** iff the noiseless-world baryon lever |d log₁₀ s\*/d(baryon dex)| ≥ 10 or cannot be computed because ±0.03 dex of baryon mass destroys the root (CFG274 Addendum 1's reading).

## 5. Bands, named systematics and knobs
- **Baryon bands:** all baryons × 10^(±0.15) inner and × 10^(±0.30) outer at fixed g_obs; the downward corners violate the stars-only lower limit and are labelled so. Extra: stars-only corners as CFG274 and the B2 route as columns.
- **Knobs (recipe half-width = quadrature over knob groups of the largest |Δ log₁₀ s\*|, only knobs that leave a root):** (a) compact stars R_e,\* = r_e/1.58 (CFG197's stellar size; raises g_bar); (b) R_e × 1.5 and / 1.5; (c) spherical baryons; (d) kernel P2; (e) **g_obs from the rebuilt V = (v/σ₀)·σ₀, v_c² = V² + 3.36 σ₀², on the 24 σ₀-detected rows only** (a check of the M_dyn route, control M5).
- **Named systematics:** the missing gas (the baryons are a lower limit: at z 4–5 gas fractions are typically large); M\* by Prospector (IMF unstated; outshining biases it low; M\* lower errors ≥ 0.3 dex in 15 rows); the Hα size r_e is the kinematic scale, not the stellar one; **σ₀ upper limits on 17 rows with the table's v/σ₀ not flagged as a lower limit** (M_dyn at face value, prior-influenced); no inclination in the table (it is inside the authors' fit); the three CRISTAL-08 z-candidates (P38).
- **Expected laws for the flags:** FLAT, H(z), PROXY at each row's z (`na` when the row has no root).

## 6. Stage A — the blind pre-flight (committed with its outputs before stage B)
**No M_dyn, σ₀ or v/σ₀ column is loaded; no g_obs, D, δ or s\* is formed.** It uses M\*, r_e, z, the published M\* errors, a noiseless world and a declared M_dyn error.
**Controls:** C1 rows, ids, counts (41; z bins 21 / 12 / 8; σ₀ limits 17 are counted from `sigma0_kms_lim` only at stage B), finite M\* and r_e, CSV hash; C2 the disc function (as CFG272); C3 the committed CFG235 sample counts (41 D rows, `CFG235_00_sample_results.json`; counts only); C4 the estimator is bit-equal to CFG223's; C5 the noiseless identity on every row's B0 baryon side; C6 coverage in the noiseless world with a declared 0.15 dex error on log M_dyn, the published M\* errors, r_e fixed; C7 the baryon-side table.
**Reported:** A1 y = g_bar/a₀ for B0 and B2 and the noiseless-world lever per row; **A2 the CFG240 reading: the y range of the pooled sample (the deepest row), the number of rows with y < 0.3, y > 6 and y > 8, and the T4 floor 3σ/√N for N = 41, 24, 21, 12, 8 at σ = 0.2 dex**; A3 knob effects on g_bar (baryon side); A4 μ_mol and B2/B0 per row; A5 per z-bin y medians.
**Decisions:** PF-D1 ESTIMATOR VALIDATED iff C1–C5 pass; PF-D2 ILL-CONDITIONED rows; **PF-D3 DRAWABLE as an upper bound iff PF-D1 passes and the row is not ILL-CONDITIONED (every drawable row is an upper bound on s\*, never a measurement).**

## 7. Stage B — the measurement (run once, after stage A and the script are committed)
Per galaxy: g_obs, g_bar (B0, B2), D, δ_FLAT with its interval, s\* or NO ROOT (B0, B2), the intervals, the bands, the knob table, Δ_floor, Δ₁ and the required gas ratio, flags, quality. Pooled rows with bootstrap, bands and knobs. **Points file `cfg273_points.csv`:** first 18 columns = the chart header (M4), then CFG272's extra columns plus `gas_to_star_req`, `s_B2`, `noroot_B2`, `sigma0_limit`, `cristal08_candidate`, `limit`. gas_class = "D (no gas; stars-only lower limit)". **No verdict words.**
**Controls at stage B:** M1 alt footing; **M2 MUTATE=1** (every M_dyn × 4, i.e. g_obs × 4: rows with a root satisfy the closed-form inversion to 1e-6 dex and their number is at least the main run's); M3 the pooled memberships (41, 24, 21, 12, 8, 38) and that the z bins partition PALL; M4 header; **M5: V = (v/σ₀)·σ₀ with v_c² = V² + 3.36 σ₀² reproduces the published M_dyn on the 24 σ₀-detected rows to a median |Δ log M_dyn| ≤ 0.02 dex (CFG197 found +0.008)**; SELFTEST (fabricated M_dyn on the law at s_true = 2 with 0.15 dex scatter on every row's B0 baryons; truth recovery only for conditioned rows with a root).

## 8. Run order and outputs
`cfg273_danhaive_gold41.py` (shared `HZQ_common/hzq_core.py`), `STAGE=A`, then `STAGE=B` once (and `MUTATE=1`, `SELFTEST=1`); README; first runs kept as `*_firstrun*` if a control fails; every post-hoc change a dated addendum written before the rerun. Commit explicit paths only; push; hashes to the orchestrator and the peer.

## 9. Hand estimates (written after §0; scored by stage A / B and kept as they fall)
- **HE1 (A):** the median y(B0) of the 41 rows lies in [0.7, 4]; at least 33 rows are conditioned (|lever| < 10); the ILL-CONDITIONED rows are the most massive ones (M\* ≥ 10^10).
- **HE2 (A):** at least 3 rows have y(B0) < 0.3 (deep points exist at low M\*), unlike lanes C and E.
- **HE3 (B):** the four known low-M_dyn rows (1082948, 1009935, 1015956, 1085659) have NO ROOT with B0; between 4 and 10 rows in all have no root.
- **HE4 (B):** PALL has a root (median D > 1) with s\*(B0) between 1 and 10 (an upper bound); the z-bin rows Pz1, Pz2, Pz3 have roots.
- **HE5 (B):** for the rows with a root the median δ_FLAT(B0) is positive (g_obs above the stars-only law: the missing gas).
- **HE6 (B):** M5 holds (median |Δ log M_dyn| ≤ 0.02 on the detected rows).
- **HE7 (B):** the gas-to-stars ratio required for s\* = 1 has a median between 0.3 and 3 among the rows with a root, and B2's scaling gas (μ_mol of order 1–4) removes the root in at least half of the rows that have one with B0.

## 10. What this lane cannot say
- It does not measure a₀ at z = 3.8–5.8: the baryons are a lower limit (no gas), M\* is a Prospector value with an unstated IMF and outshining, the kinematic size is the Hα size, σ₀ is an upper limit in 17 rows, and the dynamics are the authors' model output (M_dyn), not a rotation curve.
- A NO ROOT with stars only is robust against any added gas (the baryons exceed the dynamics); a root with stars only is an upper bound on s\*; class D carries no law statement.
