# CFG537: is CFG534's SPARC early-type outer excess replicated in an independent sample, and does it survive a free stellar M/L?

**Verdicts (frozen ladder, criteria 4d77eb8da):**
- **Part A, independent replication (WALLABY DR2, 87 non-SPARC discs): CONSISTENT on both footings, outer band only. It is NOT a replication.** Δ_out = +0.026 ± 0.038 (Z +0.68) canonical / +0.029 ± 0.038 (Z +0.76) alt. The sign matches H, but the result is 0.7σ from zero and does not exclude SPARC's +0.071. The inner band cannot be tested at WALLABY's beam, so REPLICATED was out of reach whatever the outer result.
- **Part B, SPARC robustness (not a replication): EXCESS SURVIVES M/L on both footings.** Each galaxy got a free Υ within 3.6 μm bounds (0.3–0.8). The early-type outer excess then shrinks from +0.071 to +0.046 but survives (Z +3.95 / +4.07, shuffle-calibrated Z-equivalent 2.65 / 2.97). Fitting Υ on the star-dominated inner points leaves it at +0.067 / +0.063. The fits do not make early-type stars heavier: early − late Δlog Υ is +0.02 to +0.04, below 1σ.

Settings: κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled. The kernel is ν(y) = 1/(1 − e^−√y). The cold energy's mass is still required. Nothing was downloaded. This is not "theory closed". All numbers below come from `cfg537_*_results*.json`, given as canonical / alt.

## Files
- `FROZEN_CRITERIA.md`: committed alone first (4d77eb8da).
- `cfg537_wallaby.py`: Part A.
  - `STAGE=forecast` gives the power forecast only (`cfg537_wallaby_forecast.out/.json`). It was run before any WALLABY residual existed.
  - The default run scores the sample (`cfg537_wallaby.out`, `cfg537_wallaby_results.json`).
  - `CFG537_MUTATE=1` gives `cfg537_wallaby_MUTATE.out` and `cfg537_wallaby_results_MUTATE.json`.
- `cfg537_sparc_ml.py`: Part B, with outputs `cfg537_sparc_ml.out` and `cfg537_sparc_ml_results.json`, plus `_MUTATE` versions.
- `cfg537_postfreeze.py`: post-freeze verification, dated 2026-10-09, with no verdict weight. Outputs are `cfg537_postfreeze.out` and `cfg537_postfreeze_results.json`.
- Run time is about 1 min in total. Everything ran at `nice -n 10` with 2 threads.

## 1. Independent-sample inventory (what is on disk)

| candidate | N | history proxy | baryon model | radial coverage | status |
|---|---|---|---|---|---|
| **WALLABY DR2 kinematic** (+ 2MASS XSC, RC3) | 236 → **87** after cuts | RC3 T for 87 (19 early) | HI Σ(R) + K-band disc (CFG445) | outer band: 85 of 87 have ≥ 2 rings at R ≥ 3 R_d; inner band: 16 have ≥ 2 rings at R ≤ 1.5 R_d (R_d/beam median 0.35) | **USED** (adequate for the outer band only) |
| MIGHTEE-HI DR1 (CFG301) | 47 | none in the catalogue | widths + M\* | catalogue W50 only, no resolved curves (CFG300) | unusable |
| LITTLE THINGS (Oh+15) | 26 | all Im/BCD (no early types) | yes | yes | unusable: no early types; log M_b < 9, below the matched range |
| Di Teodoro+23 massive spirals | 15 | RC3 T (10 early, 1 non-SPARC late) | totals only, no R_d or Σ_gas(R) | HI curves | unusable: no profiles, no late controls in range |
| den Heijer+15 ATLAS3D ETGs | 16 | all early | L_r, M/L | one outer point, radii not tabulated | unusable for the band statistic |
| DiskMass XI (Swaters+25) | — | — | none | one V_rot per galaxy | unusable |
| RC100, KMOS3D, MSA3D, Lelli+23 | — | — | — | z ≥ 0.6 | out of scope (not local) |

**WALLABY cuts.**
- 236 unique galaxies, keeping the best team release for each.
- QFlag ≤ 1: 231 remain.
- inc ≥ 30: 214 remain.
- XSC match ≤ 20″: 142 remain.
- RC3 T within 30″: 87 remain. The median separation is 7.8″ and the maximum 20.9″; no match was dropped as ambiguous.
- Distance and HI: all 87 have both.
- **SPARC overlap removed: 0.** The only WALLABY–SPARC pair is DDO 161, at 28″, and it had already failed the XSC/RC3 cuts.
- The A-C2 HI check passes: the median |Δ log M_HI| is 0.021 dex.

## 2. Part A: WALLABY, with CFG534's statistic copied exactly

**Power forecast** (run before scoring; this uses SPARC's within-bin scatter):
- σ_fc = 0.023, expected Z = 3.1, P(Z ≥ 2) = 0.87.
- With the scatter ×1.5: σ_fc = 0.034, P = 0.53.
- So the sample was not declared underpowered in advance.

**Realized σ is 0.038 / 0.038.** That is above even the ×1.5 forecast. WALLABY's per-galaxy outer residuals scatter more than SPARC's (late-type within-bin SD 0.12–0.20 dex against SPARC's pooled 0.128). Likely causes are Hubble-flow distances in the Hydra, Norma and NGC 4636/5044 fields, shallow 2MASS K photometry, and the lack of a bulge component.

| | canonical | alt |
|---|---|---|
| **Δ_out (R ≥ 3 R_d), early − late matched** | **+0.026 ± 0.038 (Z +0.68)** | **+0.029 ± 0.038 (Z +0.76)** |
| bins / early / late | 3 / 16 / 50 | 3 / 16 / 50 |
| per bin 9.8–10.2 / 10.2–10.6 / 10.6–11.0 | +0.008 / +0.051 / −0.027 | +0.012 / +0.052 / −0.023 |
| Δ_in, Δ_out − Δ_in | untestable (0 bins) | untestable |
| leave-one-galaxy-out Z | +0.29 to +1.04 | +0.36 to +1.09 |
| frozen verdict | **CONSISTENT** | **CONSISTENT** |

**Reading the result:**
- The sign is H's.
- The value is not significant and is about 1σ below SPARC: SPARC − WALLABY = +0.045 ± 0.046 (Z +0.99).
- The SPARC amplitude is not excluded: Δ + 2σ = 0.10 > 0.071.
- The "NOT REPLICATED by sign" route needed σ ≤ 0.0355, and the realized σ missed it.

**MUTATE (pass):**
- MU1, with T shuffled within bins: mean Z is +0.37 / +0.37 (|·| < 0.5).
- MU2, the injection: recovers +0.0710.

**Sensitivities** (no verdict weight; Δ_out canonical):

| sensitivity | Δ_out | Z |
|---|---|---|
| W1 luminosity in place of K | +0.003 ± 0.042 | +0.08 |
| RC3 match radius 15″ | +0.005 ± 0.033 | +0.14 |
| inclination error added to eV | +0.025 | +0.66 |
| early cut T ≤ 4 | +0.026 | +0.74 |
| bins shifted +0.2 dex | +0.018 | +0.53 |
| **early cut T ≤ 2** | **−0.103 ± 0.025** | **−4.18** |

The T ≤ 2 result was checked hard, in `cfg537_postfreeze.out`:
- It comes from one bin, log M_b 10.6–11.0. That bin holds two T ≤ 2 galaxies whose outer residuals differ by 0.003 dex (−0.138 and −0.142). The two-point variance is tiny, so that bin takes almost all the weight.
- With one pooled within-bin variance in place of per-class variances, the value becomes −0.019 ± 0.052 (Z −0.37).
- It is a weighting artefact of the frozen estimator at n = 2. It is not an opposite-sign detection, and it is not cited as one.

## 3. Part B: SPARC free stellar M/L (robustness on the same 153 discs; not a replication)

| variant | Δ_out | Δ_in | Δ_out − Δ_in | early − late Δlog Υ |
|---|---|---|---|---|
| B0 fixed Υ 0.5/0.7 (CFG534, reproduced to 1e-6) | +0.071 ± 0.026 (Z +2.75) / +0.072 (Z +2.76) | −0.037 / −0.027 | +0.104 / +0.098 | — |
| **B1 global free Υ_d 0.3–0.8** | **+0.046 ± 0.012 (Z +3.95) / +0.047 ± 0.012 (Z +4.07)** | −0.064 (Z −2.9) / −0.061 | +0.114 (Z +3.5) / +0.110 | +0.024 (Z +0.8) / +0.035 (Z +1.0) |
| **B2 inner-fit Υ** (132 galaxies) | **+0.067 ± 0.021 (Z +3.24) / +0.063 ± 0.021 (Z +2.95)** | −0.017 / −0.019 | +0.097 / +0.096 | −0.004 / +0.009 |
| B3 extreme: early 0.8, late 0.3 (bound) | −0.149 (Z −6.0) / −0.144 | **−0.377 (Z −9.8)** / −0.360 | +0.226 / +0.217 | fixed |

**Verdict: EXCESS SURVIVES M/L on both footings.** B1 and B2 both give Δ_out > 0 at Z ≥ 2.

- **The M/L freedom does not prefer heavier early-type stars.** The early − late difference in fitted log Υ is within 1σ of zero in B1 and B2, and the early and late medians are equal (0.53 / 0.53 canonical).
- **The global fit absorbs about a third of the outer excess,** by pushing early-type Υ up where that helps the outer points. It then over-predicts the inner region: Δ_in becomes −0.06 at about 2.9σ. The outer − inner contrast grows, to +0.11.
- **Only B3 can remove or flip the outer excess,** by forcing every early type to 0.8 and every late type to 0.3. That makes early-type inner residuals −0.38 dex, i.e. stars far too heavy where they dominate. The inner data rule it out.
- **The radial pattern stays "extra mass at large radius",** not "heavier stars".
- **B-MU1 (pass):** shuffling T kills it, with mean Z −0.18 / −0.19.

## 4. Post-freeze verification (dated 2026-10-09; no verdict weight)
The frozen `matched()` takes each bin's variance from the class samples. With small classes this over-disperses Z: the shuffle-null SD is 1.2–1.3, not 1. The shuffle-calibrated one-sided p values are:

| quantity | nominal Z | shuffle p (Z-equiv) | pooled-variance Z | bootstrap Z |
|---|---|---|---|---|
| SPARC Δ_out, CFG534 (fixed Υ) | +2.75 / +2.76 | 0.019 (2.07) / 0.020 (2.06) | +2.74 / +2.76 | +3.01 / +3.03 |
| SPARC Δ_out, B1 free Υ | +3.95 / +4.07 | 0.004 (2.65) / 0.0015 (2.97) | +3.83 / +3.96 | +4.30 / +4.44 |
| WALLABY Δ_out, frozen | +0.68 / +0.76 | 0.39 (0.28) / 0.37 (0.34) | +0.27 / +0.34 | +0.75 / +0.83 |

- **The calibration cuts SPARC's hint.** CFG534's 2.75σ is about 2.1σ once calibrated by the shuffle null. This should be carried wherever the 2.75σ is quoted.
- **The free-M/L version is about 2.7–3.0σ calibrated.** Fitting Υ per galaxy removes stellar-population scatter, so the M/L-free statistic is sharper, not weaker.

## What the record now holds
1. **SPARC.** The early-type outer excess at fixed M_b is **not an M/L artefact within population-synthesis bounds**. The fitted M/Ls do not favour heavier early-type stars. The excess survives at about +0.05 to +0.07 dex, and the inner region rules out the only M/L assignment that removes it.
2. **WALLABY, the one adequate independent sample on disk.** It does **not replicate** the excess. It is consistent with it in sign (+0.03 ± 0.04) and does not exclude it.
   - Its σ is 1.5× SPARC's.
   - Its inner band is beam-limited, so the outer − inner half of the pattern cannot be tested there.
   - The hint therefore still rests on SPARC alone, at about 2σ calibrated.
3. **Not a framework result.** No sentence here says the data favour the framework or ΛCDM. H, if real, is a statement about where the cold energy's mass sits. κ is fitted, and the cold energy's mass is still required.

## Fetch list for an adequate replication (owner's go needed; nothing fetched)
Each entry gives the source and its rough size. The sizes are estimates from catalogue descriptions and were not checked.
1. **GHASP Hα curves with WISE W1 mass models** (Korsaga et al. 2019, MNRAS 482, 154; VizieR J/MNRAS/482/154).
   - About 100 discs with Hubble types, bulge/disc decompositions and per-radius baryon curves. Size: tables of order 0.1–1 MB.
   - Overlap with SPARC is small but must be removed.
   - Hα reaches about 2–4 R_d, so the outer band is partial. The inner band is resolved, which is what WALLABY lacks.
2. **HyperLeda T types for the 55 WALLABY DR2 discs without an RC3 match** (142 have XSC; 87 have RC3). This is a query of a few KB and adds early types to the existing sample.
3. **Legacy Surveys DR10 or S-PLUS bulge/disc photometry for WALLABY DR2** (cutouts or tables, tens of MB). This would replace the shallow 2MASS K disc-only model, which is the leading scatter source identified above.
4. **BIG-SPARC** (about 4,000 HI curves with WISE mass models; announced, not released). This is the decisive sample when it appears.
5. Low value because of SPARC overlap: Noordermeer+07 early-type discs (19, mostly in SPARC), THINGS (19, mostly in SPARC) and Ponomareva+16 (32, partial overlap).

## Disclosures (dated 2026-10-09)
- **A typo in the frozen text.** FROZEN_CRITERIA A-C1 quotes CFG534's alt Δ_out as "+0.0718"; the CFG534 JSON value is +0.07215. The check tolerance (0.001) passes against either value. The frozen text was not edited.
- **The forecast underestimated σ.** The forecast σ (0.023) was 0.6× the realized σ (0.038). The ×1.5 variant (0.034) was also below the realized value.
- **The post-freeze script added nothing to the verdict.** `cfg537_postfreeze.py` was written after seeing the frozen results, because of the T ≤ 2 anomaly and the MU1 null SD. It changes no verdict.
- **The forecast was re-run once after scoring,** only to regenerate `cfg537_wallaby_forecast.out` without stderr warnings. The numbers are identical.
