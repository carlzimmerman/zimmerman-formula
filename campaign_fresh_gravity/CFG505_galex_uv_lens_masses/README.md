# CFG505: GALEX UV for the KiDS isolated lenses. The UV barely moves the stellar masses; the mass METHOD moves the a₀ levels by about −0.2 dex; the early/late split is NOT MATERIALLY changed and stands at 4.5σ

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone (398405fc8) after the cross-match returned and before any mass set or lensing re-score.
- **Data:** one approved fetch (owner go in chat, 2026-10-08): CDS XMatch, RA/Dec only, 3", GUVcat_AIS (`vizier:II/335/galex_ais`) and GR5 MIS (`vizier:II/312/mis`). Log, sizes and sha256 in `../../../_external_data/cfg505_work/FETCH_LOG.md`. Everything else was on disk.
- **Scripts, in order:** `cfg505_fetch.py` → `cfg505_match.py` → `cfg505_masses.py` → `cfg505_stage.py` (one pass of CFG110's per-lens estimator, about 6 min) → `cfg505_score.py` (about 5 min; `CFG505_MUTATE=1` for the control). Each writes a `.out`, and most write a `_results.json`. All run under nice 15 with at most 4 threads.
- **Standing rules:** κ = ½ is fitted. The two footings are scored separately and never pooled. The cold energy's mass is still required. Nothing here says the data favour the framework, and nothing says "theory closed".

## Bottom line
1. **Match:** 34.6% of the 181,477 stack-P lenses are detected in NUV. A further 55.1% are covered non-detections, which are kept with upper limits rather than dropped; 10.4% have no coverage. Detection is strongly class-dependent: late 57.7%, early 10.1%. The detections are faint (AIS median NUV 21.9 at about 3σ; MIS 22.2). The limits are too shallow to show any lens is UV-quiescent. 6.9% of the early class (6,117 lenses) are UV star-forming (rest NUV − r < 4). β (FUV − NUV, both bands with e ≤ 0.25) is measured for 8,547 lenses: 8,009 late and 538 early.
2. **Masses:** the UV-dust-corrected colour-M/L masses (M2) are **+0.298 dex** above LePhare on average (late +0.330, early +0.264). Almost all of that is the method, Bell+03 against LePhare: M1 without UV gives +0.297. **The UV itself moves M\* by +0.001 dex on average** and by +0.025 dex over the β-measured lenses. This is the expected result: Calzetti dust runs almost along the g − i / M/L_i relation, so d log M\*/dA_FUV = +0.009. Scatter against LePhare is 0.127 dex (late 0.16, early 0.10). The offset trends with colour: slope −0.43 per mag of u − r inside the late class, +0.15 inside the early class. Its early-minus-late part is −0.066 dex (mean), so the new masses make early types slightly *lighter* relative to late types, not heavier.
3. **Early/late split (headline, re-measured, K1, jackknife):** χ² 35.03/7 (4.40σ, M0) → **36.34/7 (4.52σ, M2)**, the same on both footings. Δσ = +0.12 is **NOT MATERIAL**; the UV-only part is −0.03 and the method part +0.15. **The split stands.** Every variant stays between 4.18σ and 4.76σ.
4. **a₀ levels (CFG261 estimator):** the method change is **MATERIAL** in five of six rows. It lowers log s\* by 0.14–0.25 dex, except late-HI (+0.05, inside its error). The UV-only change is at most 0.011 dex: NOT MATERIAL everywhere. The early class still sits about 2.5× above the late class at the same nominal g_bar. So the colour disagreement in the absolute level survives the mass rebuild; only the overall level moves.

## Mass comparison (log M\*(set) − log M\*(LePhare + 0.15); `cfg505_masses.out`)

| set | median (all) | robust SD | late / early median | early − late (mean) | trend with u − r |
|---|---|---|---|---|---|
| M1 Bell+03 g − i → M/L_i | +0.292 | 0.127 | +0.304 / +0.282 | −0.064 | ρ −0.26 |
| **M2 = M1 + UV dust** | **+0.292** | 0.127 | +0.306 / +0.282 | **−0.066** | ρ −0.27 |
| M2i (imputed dust bracket) | +0.312 | 0.127 | +0.326 / +0.302 | −0.066 | ρ −0.27 |
| M1b u − r → M/L_K | +0.331 | 0.150 | +0.375 / +0.304 | −0.107 | ρ −0.37 |
| M1c g − r → M/L_r | +0.327 | 0.127 | +0.324 / +0.332 | −0.031 | ρ −0.12 |

- **By UV status (M2):** the β-measured lenses are +0.43; other detections +0.29; non-detections +0.29; no coverage +0.29. The β-measured lenses sit higher for two reasons: they are blue discs, where Bell+03 departs most from LePhare, and they carry the dust term.
- **By z third (M2):** +0.34, +0.29, +0.26.
- **Fitted dust:** A_FUV has median 2.82 mag (Meurer law, clipped to [0, 5]; 4% of values sit at 0 and 10% at 5). The β values are noisy, because the AIS errors are about 0.3 mag.
- **The total-vs-aperture r flux scale:** measured per lens, its median is +0.170 dex, against the record's constant +0.15. That difference is a further possible +0.02 dex on every set, not applied.

## Lensing re-scores (`cfg505_score.out`; MUTATE in `cfg505_score_MUTATE.out`)

**T1, the re-measured early/late split on K1** (7 bins). Canonical and alt agree to 0.01 in χ².

| set | χ²/7 | σ | uniform early-class differential for p > 0.05 (best) |
|---|---|---|---|
| M0 LePhare | 35.03 | 4.40 | 0.20–0.50 dex (0.40; alt 0.35) |
| M1 | 36.63 | 4.54 | 0.20–0.40 (0.30); alt 0.15–0.40 |
| **M2** | **36.34** | **4.52** | 0.20–0.40 (0.30); alt 0.15–0.40 |
| M2i / M1b / M1c | 39.05 / 38.43 / 32.80 | 4.76 / 4.71 / 4.18 | — |
| R2: UV star-forming early lenses moved to late (M2) | 44.30 | **5.21** | — |
| R2 variant: those lenses dropped from both classes | 39.65 | 4.82 | — |

- **The UV class sharpens the split.** Cleaning the early class of UV star-formers raises the split to 5.2σ.
- **The needed differential stays large.** With the new masses the split still wants early-type lenses about 0.3 dex (2×) heavier than late types. The new masses supply −0.07 dex.

**T2, implied a₀ scale s\*** (a₀ = s\* × 9.3603e-11; κ_implied = ½ s\* on the canonical footing, ½ s\* × 0.8275 on alt; jackknife SD of log s\* in brackets).

| row | M0 (= CFG261) | M1 | **M2** | Δ log s\* M2 − M0 | κ_implied M2 (can / alt) |
|---|---|---|---|---|---|
| T-late-LO | 1.670 (0.105) | 0.954 | **0.930** | −0.254 MATERIAL | 0.47 / 0.38 |
| T-late-HI | 0.683 (0.180) | 0.772 | **0.758** | +0.045 not | 0.38 / 0.31 |
| T-early-LO | 2.485 (0.053) | 1.808 | **1.788** | −0.143 MATERIAL | 0.89 / 0.74 |
| T-early-HI | 4.118 (0.044) | 2.418 | **2.418** | −0.231 MATERIAL | 1.21 / 1.00 |
| late (all z) | 1.278 (0.077) | 0.801 | **0.781** | −0.214 MATERIAL | 0.39 / 0.32 |
| early (all z) | 3.192 (0.032) | 2.008 | **2.002** | −0.203 MATERIAL | 1.00 / 0.83 |
| ALL | 2.416 (0.034) | 1.551 | **1.542** | −0.195 | 0.77 / 0.64 |

- **The method, not the UV.** Every MATERIAL entry comes from the method change (M1 vs M0). M2 vs M1 is at most 0.011 dex.
- **The early rows close only part of their gap.** CFG261 said the early rows need +0.36 / +0.57 dex more baryons to reach s\* = 1. The new masses supply +0.26 dex in M\*, which is less in M_gal because f_cold falls. That brings s\* to 1.79 / 2.42, still above 1.
- **The late rows move the other way.** With M2 the late rows sit at or below 1 (0.93 / 0.76). The early and late classes still disagree at the same nominal g_bar.
- **The absolute level is method-limited.** Bell+03 against LePhare alone moves every level by about 0.2 dex. That is larger than the jackknife errors and comparable to CFG261's ±0.15 dex inner band.
- **What a level is not.** None of these levels is a measurement of a₀. κ stays fitted.

**R3, the CFG503 environment term E** (nlz, W10, Moster), restacked with each mass set. Reported only.

| quantity | M0 | M2 |
|---|---|---|
| split + E, K1 (both footings) | 35.6/7 | 39.3/7 |
| split + E, inner 9 bins (R ≤ 0.445 Mpc) | 50.3/9 | 83.3/9 |
| ALL-lens law + E, inner 9, canonical (no E) | 46.4 (124.7) | **10.2 (43.5)** |
| ALL-lens law + E, inner 9, alt (no E) | 27.7 (91.0) | **12.6 (21.2)** |
| ALL-lens law + E, outer 6, canonical / alt | 48.3 / 41.0 | 68.8 / 62.4 |

- **Outer bins are never in a verdict.** CFG503's LCDM validation fails at 1–1.4 Mpc.
- **K1 stays inside 0.3/h.** With the new masses the K1 bins' pair-weighted mean R grows from at most 0.251 Mpc to at most 0.324 Mpc (R5). That is still inside Brouwer+21's 0.3/h ≈ 0.43 Mpc.

## Controls and MUTATE
- **Controls pass (1 to 3).**
  - **C1:** the re-staged M0 sums equal `cfg110_perlens.npz` exactly (deviation 0).
  - **C2:** T1 with M0 = 35.0254 / 35.0263, against CFG95-MUTATE's 35.025 / 35.026.
  - **C3:** T2 with M0 reproduces CFG261's four T-row s\* and jackknife SDs exactly.
- **Controls pass (4 and 5).**
  - **C4:** the Bell+03 coefficients are parsed from the table on disk and match the transcription; M2 with A_FUV = 0 equals M1 exactly.
  - **C5:** every match row joins to a lens to better than 1e-6 deg (an assertion).
- **MUTATE (shuffled UV record, seed 5050):**
  - **MU1 passes:** ρ(NUV − r, u − r) falls from +0.80 to −0.004.
  - **MU2 passes:** Δσ_split −0.016; |Δ log s\*| ≤ 0.009; the early − late UV shift is 0.0000.
  - **For the mass headline the MUTATE is uninformative.** As pre-declared, the real UV-only change (Δσ −0.03, ≤ 0.011 dex) is itself below the MU2 thresholds, so the two cannot be told apart.
  - **The class lever does respond to the UV data.** With the shuffled UV classification, R2 moves 28,904 random early lenses and the split falls to 2.87σ. The real UV classification raises it to 5.21σ.

## Limits
- **No SPS fit.** No SPS code or template library is on disk, and no further download was approved. The masses come from published colour–M/L relations (Bell et al. 2003, Table 7, parsed from the on-disk copy). The UV enters only through the Meurer IRX–β dust law, with the Calzetti curve, and through the class. An SPS fit with the UV bands could move ages and bursts by more than the dust law does, so **the UV leverage measured here is a lower bound.**
- **Large spread between relations.** The three relations differ among themselves by 0.04 dex in the median and 0.08 dex in the early − late term. The IMF shift (−0.15 dex, from the Bell+03 note) sets the absolute M1/M2 level, and its uncertainty of ±0.05 or more enters every s\* directly.
- **Meurer overestimates dust for normal discs.** It is a starburst law, so M2's dust is an upper side; M2i is the bracket for selection bias. β is measured for only 538 early lenses.
- **Gas, K-corrections and the flux scale.**
  - Gas stays on the record's mass-only relation, evaluated at the new M\*. No sizes are on disk, so no UV gas estimator was possible.
  - The rest-frame NUV uses a flat-f_ν K-correction.
  - r is not extinction-corrected (±0.1 mag).
  - The record's constant flux scale is kept.
- **Not cross-checked against a third SED code.** The DESI DR1 CIGALE VAC is on disk; CIGALE is a different SED code from LePhare, but its fits use no GALEX bands. It was not used here.
- **Disclosures.**
  - `cfg505_fetch.out` had absolute local paths in two Python warning lines. They were rewritten to relative paths after the run, and the warning source was fixed. No numbers changed.
  - The false-match line in `cfg505_match.py` had a per-lens normalisation bug. It was fixed and re-run before the freeze; it is a match statistic only.
  - numpy prints the known Accelerate matmul RuntimeWarnings to stderr. Every result is finite.

## Files
- `FROZEN_CRITERIA.md`
- `cfg505_fetch.py` / `.out`
- `cfg505_match.py` / `.out` / `_results.json`
- `cfg505_masses.py` / `.out` / `_results.json`
- `cfg505_stage.py` / `.out`
- `cfg505_score.py` / `.out` / `_results.json`, plus `cfg505_score_MUTATE.out` / `cfg505_score_results_MUTATE.json`
- **Data dir (not in git):** `../../../_external_data/cfg505_work/`. It holds the match CSVs, the UV table, the mass sets, the seven re-staged per-lens sum files (about 65 MB each), the copied CFG261 cache and FETCH_LOG.md.
