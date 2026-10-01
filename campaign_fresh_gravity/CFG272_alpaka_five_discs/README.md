# CFG272 — the ALPAKA I discs 13 / 23 / 24 / 25 / 28: two have a robust NO ROOT, two have a root that is only an ill-conditioned upper bound, one has no point

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival, ΛCDM has no a₀ (PROXY = CFG223's effective-a₀ curve). The ALPAKA tables carry no gas conversion: the baryons used here are LOWER LIMITS (stars only; stars plus a gas floor), so a root is an UPPER BOUND on s\* and a NO ROOT is robust against any added gas. No sentence says the data favour a law. NOT blind: CFG227 / CFG237 already held the stars-only group result (7 of 9 bounds below 0).**
> Hashes: criteria **e06a91b8a** · stage A pre-flight **ca17402ea** · SELFTEST **b8b483476** · measurement, MUTATE and this README: the commit that carries this file. The α_CO / α_[CI] routes were frozen in the criteria before any velocity was read. Data on disk only; nothing fetched.

## Bottom line
1. **Stars-only baryons (B0, the headline lower limit) at R_ext:** D = g_obs/g_bar and the verdict per disc:

| disc | z | line (S/N) | y (B0) | D (B0) | δ_FLAT (68 %) | Δ_floor (dex) | headline |
|---|---|---|---|---|---|---|---|
| **13** COSMOS 3182 (MS) | 2.103 | [CI](2–1) (2.7σ) | 13.7 | **0.442** | −0.38 (−0.61…−0.07) | −0.35 | **NO ROOT** |
| **23** ADF22.1 (MS, AGN) | 3.089 | CO(3–2) (2.0σ) | 15.3 | **0.856** | −0.09 (−0.33…+0.15) | −0.07 | **NO ROOT** |
| **24** ADF22.5 | 3.094 | CO(3–2) (7.0σ) | – | – | – | – | **no M\*: no point** |
| **25** ADF22.7 (SB, AGN) | 3.088 | CO(3–2) (3.0σ) | 8.2 | **1.260** | +0.07 (−0.12…+0.25) | +0.10 | root: **s\* ≤ 3.3** |
| **28** W0410-0913 (SB, hot DOG) | 3.630 | CO(6–5) (104σ) | 12.1 | **1.043** | −0.01 (−0.22…+0.21) | +0.02 | root: **s\* ≤ 0.74** |

   - **13 and 23 have NO ROOT with the stars alone, so no gas can create one** (any added gas raises g_bar and lowers D further): the CFG227 stars-only floor is a robust floor here. The baryon mass would have to fall by 0.36 dex (13) and 0.07 dex (23) before a root exists.
   - **25 and 28 have a root with stars only, which is an UPPER bound on s\*** (a₀ ≤ 3.1e-10 and ≤ 0.70e-10): **ID 25 keeps a root with the gas floor B1 (D = 1.047, s\* ≤ 0.68) and with the conventional gas B2 (the same, because the starburst α_CO is 0.8); ID 28 loses it with the gas floor (D = 0.694: NO ROOT).** Both discs sit at y = 8–12 (ν_mono = 1.06–1.08), where the root is an ill-conditioned residual D − 1 of 4–26 %: **not an a₀ measurement.**
   - **Pooled P4** (13, 23, 25, 28): median D = 0.949, **NO ROOT**.
2. **ID 24 has no stellar mass, so its baryon lower limit would be the gas alone** (g_bar 2.1e-10 m/s² for the floor α_CO 0.8, D = 4.06; 1.1e-9 for α_CO 4.36, D = 0.75): uninformative; **no point** (as CFG227).
3. **All four discs with an M\* were foreseen ILL-CONDITIONED at stage A** (y = 13.7, 15.3, 8.2, 12.1; ν_mono = 1.05–1.08; one radius per disc, no deep point): **CFG240's conditioning theorem (7b73ef6a0, Lean `T3_newton_limit`: ν → 1 at large y removes the a₀ dependence; its break-even table: no point below y = 0.1, no 0.1 dex)** predicts a root here to be a statement about a few-per-cent residual. The recipe half-widths confirm it: **0.95 dex (25) and 1.50 dex (28)** — stars at 2 R_e +0.90 / +1.06, R_e × 1.5 +0.57 / +0.72, pressure + 3.36 σ² +0.19 / +0.70, the inclination ±1σ ∓0.09 … +0.78 — while 13 and 23 have a root in only 1 of 12 and 3 of 10 knob variants.
4. **Chart treatment suggested:** floor triangles at s = 0.001 for 13 (z 2.103) and 23 (z 3.089); labelled open symbols with downward arrows ("upper bound; baryons are a lower limit; near-Newtonian, ill-conditioned") for 25 (z 3.088, s\* ≤ 3.3) and 28 (z 3.630, s\* ≤ 0.74); nothing for 24. For the NO ROOT rows ignore the `stat68/95` columns (they hold percentiles of the 13 % (13) and 39 % (23) of the Monte Carlo draws that have a root).

## Controls and MUTATE (nothing hidden)
- **Stage A (ca17402ea): C1–C5 pass, including C3 in the exact-string form** (all four stars-only g_bar equal CFG227's printed S3 strings); C6 coverage fails for the ill-conditioned rows by construction (68 %: 0.02–0.28).
- **Stage B: M1 (alt footing 1e-16), M3 (P4 = 13, 23, 25, 28), M4 (header) pass. M5 passes exactly: ALPAKA 15 through this lane's functions with CFG229's committed inputs reproduces CFG229's g_obs, g_bar and D with a deviation of 0.** **M2 MUTATE=1 passes:** with every V_ext × 2 four rows have a root (the main run has two) and each equals the independent closed-form inversion of its own (D, g_bar) to 9e-16 dex.
- **SELFTEST (b8b483476):** a world exactly on the law at s_true = 2 with 0.15 dex scatter returns s\* = 2.2 / no root / 7.7 / no root for 13 / 23 / 25 / 28: the ill-conditioning in action.

## Hand estimates (frozen before any number; kept as they fall)
- **Stage A:** HE1 and HE2 hit. **Stage B:** **HE3 misses** (two of the four rows with an M\* have NO ROOT, not at least three; P4 has none); **HE4 misses** (25 has s\* ≤ 3.3 ≥ 2 but keeps the root with B1 / B2; 28 loses the root with B1 but its s\* is ≤ 0.74, not ≥ 2); **HE5 hits** (ID 13's two inclinations differ by 0.34 dex in g_obs); **HE6 hits** (ID 24: no point); **HE7 hits** (M5).

## Disclosures
- The rooted-draw Monte Carlo of a row whose central estimate is near the floor can lie entirely above its central s\* (28: central 0.74, rooted 68 % 2.2–18.2): conditioning on a root biases the interval high (stage A's coverage test). The bound to read is the central B0 / B1 value with the knob and band spread, not the interval.
- The published errors are used as given: ID 13 / 23 / 25 inclination errors (HST 11°, ALMA 3° / 4.5°); the paper's 15 % assumed HST errors; M\* STARDUST with AGN templates for 23, 25, 28 (the AGN caveat for M\* and for the inner kinematics; ID 28 "with caution"); three of the five discs (23, 24, 25) sit in the SSA22 protocluster (an external field is not modelled).
- ID 13's JWST stellar disc (3.34 kpc) and gas disc (5.1 kpc) are knobs only (quoted from the data card). One run; no re-run to change a result. The helper library `../HZQ_common/hzq_core.py` is shared with lane E.

## Files
`FROZEN_CRITERIA.md`, `PREFLIGHT_RESULTS.md`, `cfg272_alpaka_five.py`; `cfg272_stageA.out` / `_results.json`, `cfg272_stageB.out` / `_results.json`, **`cfg272_points_stageB.csv`** (chart shape; 6 rows: 13, 23, 24, 25, 28, P4; extra columns y, lever, D, δ_FLAT, Δ_floor, baryon shift for s\* = 1, gas-only and stars-only bands, `s_B1`, `s_B2`, `limit`, flags, quality), `cfg272_stageB_MUTATE1.*`, `cfg272_stageB_SELFTEST*.*`. Run: `STAGE=A python3 cfg272_alpaka_five.py`, then `STAGE=B` (and `STAGE=B MUTATE=1`); a few seconds.
