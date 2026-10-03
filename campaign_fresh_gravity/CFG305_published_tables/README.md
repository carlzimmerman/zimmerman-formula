# CFG305: the journal tables against the arXiv copies we used (orchestrator lane, 2026-10-02)

**Why.** CFG287 left one question open: do the journal versions of three source tables match the arXiv copies the repo used? The owner said yes, in the data-release chat, to fetching the open-access journal PDFs. This lane checks the two differences that chat reported, builds a journal-version RC100 table, and bounds how far the change reaches. κ = ½ is FITTED. Nothing was downloaded. The PDFs were read in place from the data-release chat's scratch copy.

**Order.**
- The criteria were committed before any CFG305 script existed: **82dfcc1b3**, FROZEN_CRITERIA.md sha256 prefix cac9836140630bea.
- While scoping I looked at the text layer of the two RC100 rows and the Umehata row (disclosed in the criteria).
- This README was written after all the runs.

## Bottom line
- **Both reported differences are CONFIRMED, cell by cell:** 6 of 6 RC100 cells and 4 of 4 Umehata+25 cells. The text layer (`cfg305_confirm.py`) and the page images read by eye agree. No other RC100 cell differs among the 600 compared.
- **RC100 row 87 (J0901+1814) is a genuine refit between arXiv v1 and the journal; our transcription of v1 was right.** Row 78's σ₀ (75 → 77) was our transcription slip: the v1 image also says 77.
- **Umehata's 870 µm masked fit also changed between arXiv v1 and the journal.** The repo's values equal the arXiv v1 PDF exactly. They had been confirmed by a direct read of that PDF, not only through a summary.
- **The PUBLISHED RC100 table** is `real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv`, sha256 **8a7ed57a99be6799**…aa930e7. It differs from the CORRECTED CSV in 6 primary cells (row 87 ×5, row 78 σ₀), plus row 87's derived cells. Controls B1–B4 pass.
- **The RC100 inversion slope moves from −0.111 to −0.092 ± 0.064 (+0.019, 0.30σ).** The data move toward zero, so every distance shrinks by about 0.3σ: from the flat law, from the rival a₀ ∝ H(z) and from ΛCDM. The hand estimate (+0.02, 0.4σ) hit. **RC100 still decides nothing.**
- **Verdict rows that move:**
  - **Non-mechanical, all against the framework's preferred reading:**
    - **L331 R4** goes PASS → FAIL: the ΛCDM residual trend falls from +2.6σ to +2.3σ, under its frozen 2.5σ line.
    - **CFG223's RC100 z-quartile 4** s* goes 0.99 → 1.07, and the ΛCDM proxy's expected ratio now sits inside the statistical 95% interval (n → Y; 5/8 → 6/8 points).
    - **CFG217**'s rival-truth mis-scaling M2 goes "no" → "YES" (χ² 3.02 → 1.68 within |Δlog M_bar| ≤ 0.2 dex), and V2's "rival's deficit survives" goes YES → NO.
    - **MNRAS v3.1 paper_numbers S5e** goes PASS → FAIL. Its post-hoc wording tolerance is "a −0.05 dex/z drift puts the slope within 0.5σ of constancy"; the slope now lands at +0.6σ.
  - **Mechanical** (a reproduction or sha256 row comparing against the old table): L320 D0, h101 101-3, CFG233 R5, MNRAS v3 S5h/S5i, and C2 of CFG217 in group C.
  - Everything else is NUMERIC-MINOR (each headline under 1σ) or UNCHANGED.
- **ADF22.5 (A7) with the journal's 870 µm fit:**
  - The 870 µm thin-disc inclination goes 54.5° → **64.2°**, so that row's bounds nearly halve: S0 stars-only s* ≤ 13.7 → **≤ 7.49**; G1 gas-only ≤ 18.8 → **≤ 11.0**.
  - The gas-proxy radius goes 1.53 → 1.58 kpc, which moves the six post-hoc rows by ≤ 0.012 in D: G1 s* ≤ 7.14 → ≤ 7.24; G2 0.375 → 0.462.
  - No status or resolution changes.
  - CFG284/285's frozen headline rows are unchanged. Their 870 µm inclination knobs roughly halve (B0/S0 +0.43 → +0.19 dex; G1 +0.39 → +0.17), the recipe half-widths shrink 0.03–0.06 dex, and hand-estimate row HE6 turns hit → MISS on B1 and G1.

## 1. The confirmed differences (`cfg305_confirm.py` → `cfg305_confirm.out`, `_results.json`; 6/6 controls pass)

| table | row | cell | repo | journal | arXiv v1 | decision |
|---|---|---|---|---|---|---|
| RC100 Table B1 (ApJ 944:78) | 87 J0901+1814 | log M_baryon | 11.09 | **10.72** | 11.09 | CONFIRMED (v1 → journal refit) |
| | | R_e (kpc) | 4.33 | **3.85** | 4.33 | CONFIRMED |
| | | f_DM(<R_e) | 0.06 | **0.44** | 0.06 | CONFIRMED |
| | | V_c(R_e) (km/s) | 209 | **250** | 209 | CONFIRMED |
| | | σ₀ (km/s) | 55 | **37** | 55 | CONFIRMED |
| | 78 BX610 | σ₀ (km/s) | 75 | **77** | 77 | CONFIRMED (our transcription slip) |
| Umehata+25 Table 3 (ApJ 997:79), masked, A7 | ADF22.A7 | Sérsic n | 1.01 ± 0.17 | **1.42 ± 0.36** | 1.01 ± 0.17 | CONFIRMED |
| | | R_e (kpc) | 1.53 ± 0.15 | **1.58 ± 0.15** | 1.53 ± 0.15 | CONFIRMED |
| | | b/a | 0.58 ± 0.06 | **0.435 ± 0.05** | 0.58 ± 0.06 | CONFIRMED |
| | | PA (deg) | 17.4 ± 2.5 | **17.9 ± 2.6** | 17.4 ± 2.5 | CONFIRMED |

- **Controls:**
  - **J0:** the PDF sha256s match the chat's `SHA256.txt`.
  - **J1:** all 100 rows parse. Rows 24, 47, 70 and 93 have their R_e/f_DM pair on a page-break line, and it is recovered.
  - **J2:** CFG289's 12 corrected value cells equal the journal.
  - **J3 (negative):** the original CSV shows all 12 of them, and 18 differing cells in all, which is the 12 plus the 6 above.
  - **J4:** Umehata Table 2 (position, S₁.₁mm 2.03 ± 0.04) and Table 4 (free-n and n = 1 F444W fits) equal the repo.
- **Page images (read by eye, one reader, rendered outside the repo):**
  - The journal rows 78 and 87 read exactly as the text layer.
  - The arXiv v1 raster table (p. 28–29 images in the external-data folder) shows row 87 = 11.09/4.33/0.06/209/55 and row 78 σ₀ = 77 ± 5.
  - Umehata Table 3 A7 reads as extracted.
- **Other row-87 columns the journal also changed** (not in the repo CSV): δlog SFR 0.62 → −0.05, log M_bulge 10.09 → 9.98, log M_vir 12.17 → 11.89, Σ_SFR 0.67 → 0.63, Σ_DM 7.64 → 8.72. The errors also changed: log M_bar ±0.07 → ±0.14, R_e ±0.85 → ±2.00, f_DM ±0.06 → ±0.15, σ₀ ±3 → ±2. log M* (10.96) is unchanged. CFG303's lane transcription `rc100_table3_cols5to8_transcribed.csv` carries the v1 δlog SFR and M_bulge for row 87.
- **Other Umehata cells that differ (error bars only):** the masked n, b/a and PA errors above, and the **unmasked n error, 0.22 → 0.37** (value 1.70 unchanged). The thin-disc inclination arccos(b/a) of the masked fit goes 54.55° → **64.21°**. The arXiv PDF on disk is v1 (stamp 2502.01868v1).

## 2. The PUBLISHED CSV (`cfg305_build_published.py` → `.out`, `_results.json`; 4/4 controls pass)
- **Changes:** row 87: 10.72 / 3.85 / 0.44 / 250 / 37; row 78: σ₀ 77.
- **Derived cells:** recomputed for row 87 only, with CFG289's constants and format:
  - g_Re 3.2693e-10 → **5.2610e-10**;
  - V_c⁴/(G M_bar) 1.1683e-10 → **5.6071e-10** (a0/1.2e-10 0.974 → 4.673);
  - the deep flag stays 0.

  Row 78's derived cells are kept, because σ₀ does not enter them.
- **Controls:**
  - **B1:** the constants reproduce the derived columns of the 99 other rows to 3.7e-5.
  - **B2:** the 98 untouched rows are byte-identical.
  - **B3:** exactly the 6 primary cells plus row 87's 3 derived cells changed.
  - **B4:** all 100 rows equal the journal parse.

## 3. The readers (`cfg305_rerun.py`, `cfg305_supplement.py`, `cfg305_compare.py`; ORIG = CORRECTED, FIX = PUBLISHED)
- **Run:** group O ran 36 entry points in 52 minutes; group C ran 3. MUTATE: row 50 log M_bar +0.30 dex changes L323's output (290 lines) and cfg216's (28 lines), so the substitution path is live (**PASS**).
- **Group C liveness:** paper_numbers v3 printed the PUBLISHED sha256 prefix (8a7ed57a99be6799).
- **Reproduction:** every group-O ORIG text output equals CFG289's FIX copy, or the committed file where CFG289 saw no change (PNG figures are not compared byte for byte). There are two exceptions:
  - `rc100_input_correction_compare` (frozen move after CFG217/218, so it compares fresh outputs);
  - CFG290 (its ORIG differs from its committed output only in the manuscript word counts, which were edited after CFG290).

  Group C's ORIG reproduces the committed outputs, and paper_numbers' stdout equals its committed `paper_numbers.out`. The L323 flagged-rows ORIG reproduces CFG289's post-hoc numbers. CFG52 pooled/mock_bias and CFG90 (mirror path) ORIG equal CFG289's FIX files.

| reader | class | what moves (CORRECTED → PUBLISHED) |
|---|---|---|
| L331 fairness audit | **VERDICT-MOVES** (against interest) | R4 "ΛCDM residual trend ≥ 2.5σ for NFW and cored, framework < 1.5σ" PASS → FAIL. ΛCDM NFW +2.6σ → +2.3σ, cored +2.6 → +2.3; framework +0.3σ → +0.1σ. The trend slope moves 0.005 (0.2σ). |
| CFG223 a₀ over time | **VERDICT-MOVES** (containment flag) | RC100 corr/committed z-quartile 4 [2.19, 2.52]: s* 0.994 → 1.070, 68% [0.80, 1.14] → [0.85, 1.22], 95% upper 1.38 → 2.07. Pulls: flat −0.03 → +0.31, PROXY −3.12 → −2.74, H(z) −5.66 → −5.24. PROXY inside the stat 95% interval n → Y; summary 5/8 → 6/8. The s* shift is 0.3σ. |
| CFG217 attack (default, corrected mode; group C) | **VERDICT-MOVES** (words) | M2 "rival truth at a plausible mis-scaling" no → **YES**. V2 (0.5 μ) "rival's deficit survives" YES → **NO**. Baseline flat slope −0.030 → −0.025 (0.26σ). G2 unchanged (ρ +0.33, p 0.036, n 41). D3 stays ATTACK-BROKEN. In group C, C2 also fails mechanically (it compares with CFG216's committed v1-table outputs). |
| MNRAS v3.1 paper_numbers (group C) | **VERDICT-MOVES** | 85 checks: 0 FAIL → 3 FAIL. S5e (data; post-hoc wording tolerance): β = −0.05 gives +0.6σ from constancy, against < 0.5. S5h (identity: sha256 / "17 cells") and S5i ("the correction moves the slope < 0.001") fail mechanically. Numbers in §5. |
| L320 carrier price | **VERDICT-MOVES**, mechanical | D0 "reproduces h16's −0.112" PASS → FAIL (−0.092). C2: 2.8–3.2σ → 2.4–2.9σ (still PASS). |
| h101 f_DM inversion surveys | **VERDICT-MOVES**, mechanical | 101-3 reproduction of item 16's committed number fails. RC100 median a₀ 1.386 → 1.493e-10 (+0.03 dex, 0.4σ). Joint slope +0.075 → +0.084 ± 0.036 (0.24σ): flat 2.1σ → 2.3σ away, ΛCDM-native 1.6σ → 1.3σ. |
| CFG233 referee | **VERDICT-MOVES**, mechanical | R5 z-score rows against CFG216's committed targets: rows meeting their line 20 → 17 of 26. One sensitivity class label W-mixed → W-flat (thin-disc M_bar). |
| L323 stress | NUMERIC-MINOR | S1 "tie" stays FAIL: best framework cell [−0.038, −0.007] → [−0.042, −0.012]. S4 least-rising ΛCDM cell 3.2σ → 2.9σ above RC100's trend (PASS). Framework 0.9σ → 0.7σ. Data slope −0.055 → −0.041. |
| L323 flagged rows (supplement) | NUMERIC-MINOR | The flags are re-derived and unchanged ({67, 83} + 14). Without the 16 flagged rows: [−0.034, −0.004] → [−0.041, −0.009]. The S1 FAIL survives. |
| L322 | NUMERIC-MINOR | 3.3–3.5σ → 3.0–3.2σ. |
| L332 | NUMERIC-MINOR | At β = 0: ΛCDM +3.1σ → +2.8σ, framework +0.9σ → +0.7σ. RC100-as-L323 slope −0.055 → −0.041. |
| CFG216 ×3 (rc100, corrected mode, posthoc index ×2) | NUMERIC-MINOR | Flat slope −0.030 → −0.025 (σ 0.019). z vs rival-true −5.29 → −4.97 / −4.82 → −4.47. Index: flat 1.7σ → 1.4σ, rival 4.7σ → 4.4σ. Verdict words are unchanged. |
| CFG222 | NUMERIC-MINOR | FLAT z −1.55 → −1.28; PROXY −3.53 → −3.24; H(z) −4.70 → −4.38. |
| CFG227 / CFG237 | NUMERIC-MINOR | RC100 z ≥ 2 (class D, no band): PROXY median −0.045 [−0.075, −0.003] → −0.036 [−0.073, +0.008]. The CI now contains 0, but the row has no verdict word. CFG237 targets still PASS. |
| CFG6 | NUMERIC-MINOR | The RC100 slope pull for model A moves −1.78σ → −1.45σ; rival H(z) −5.29 → −4.92; ΛCDM-emergent −4.28 → −3.93. Replay control C2 already failed on the CORRECTED table (mechanical, unchanged). |
| h16, k02, k03, k04, k01, h105, k_contrarian, k_high-z_amplified_scatter, k_high-z_floor_census | NUMERIC-MINOR | h16: −1.8σ → −1.5σ (flat), −3.9σ → −3.5σ (ΛCDM-native); median a₀ +0.17 → +0.20 dex. k03: flat 1.70 → 1.41σ, ΛCDM 3.61 → 3.31σ. k-hzs: RC100 own slope −2.00σ → −1.83σ; k-hzs-4 stays FAIL. k02: common slope −0.065 → −0.047 ± 0.068. k_contrarian: the Υ offset that would fake the trend with gas goes 1.29 → 0.92 dex. All under 1σ. |
| CFG218 ×2 | NUMERIC-MINOR | RC100 band 0.032 → 0.035; still "marginal". |
| CFG52 feas / CFG90 (mirror path) | NUMERIC-MINOR | Per-galaxy row 87 only, plus C5 +0.022 → +0.021 and mock bias +0.0996 → +0.0998. The z ≥ 1.5 pools are unchanged (row 87 has g_bar > a₀). |
| CFG52 pooled / mock_bias | UNCHANGED | |
| MNRAS v2 paper_numbers (superseded) | NUMERIC-MINOR | The same S5 numbers as v3. |
| CFG290 referee checks | NUMERIC-MINOR (NOT-REPRODUCIBLE as committed: word counts) | All-rows slope −0.111 → −0.092; without the flagged rows −0.095 → −0.070. |
| rc100_input_correction_compare | NOT-REPRODUCIBLE (by the frozen order change) | A report generator, no physics. |
| a0z_clean_ledger, zimmerman_theory_figures, rc100_deepMOND_framework_fit | UNCHANGED | |
| CFG229, CFG270, CFG280 | NOT-RUN by construction | They read only idx/name/z from the paper-values file, and none of these changes. |

**Post hoc (labelled; out of the frozen scope, because both were committed after the criteria): the a₀(z) chart** (`cfg305_posthoc_chart_readers.py`)
- **Route B (CFG303, framework-native):** the chart's RC100 route-B quartiles stay **1.483 / 1.014 / 0.842 / no root**. Row 87's M* is unchanged; its g_obs moves 3.27 → 5.26e-10. The route-B pooled s* moves 1.449 → 1.480.
- **The faint CFG223 RC100 Q4 marker:** moves s* **0.99 → 1.07**.
- **CFG303's own control:** T1 ("transcribed column 7 equals the corrected table") FAILs on row 87, because its v1 transcription carries 11.09.
- **Disclosed:** the O_ORIG mirror held the older chart script, so the chart's own diff mixes versions. The numbers above come from the FIX run's checks and from CFG223/CFG303's outputs.

## 4. ADF22.5 (A7) with the journal's 870 µm values (`cfg305_adf22_geometry.py` → `cfg305_adf22_geometry.out`, `_results.json`; 5/5 checks)
- **Control:** CTRL reproduces CFG285's committed post-hoc `.out` and `_results.json` exactly. It also reproduces CFG284/285's stage-B outputs; a run-time field, "(4 s)" vs "(5 s)", is normalised (see §6).
- **The variant:** `cfg285_posthoc_expfit_geometry_PUBLISHED.out` (with a banner) and `_PUBLISHED_results.json`.

| row (post hoc, exp-matched geometry) | D | status | s* | no-root | resolution |
|---|---|---|---|---|---|
| S0 stars only | 1.459 → 1.459 | root | 4.59 → 4.59 | 0.212 → 0.212 | UNRESOLVED |
| S1 stars + gas (0.8) | 0.796 → 0.798 | floor | – | 0.702 → 0.699 | UNRESOLVED |
| S2 stars + gas (3.6) | 0.307 → 0.309 | floor | – | 1.000 | RESOLVED-FLOOR |
| G1 gas only (0.8) | 1.751 → 1.763 | root | 7.14 → **7.24** (68% [4.72, 10.9] → [4.80, 11.0]) | 0.000 | RESOLVED-ROOT |
| G2 gas only (1.36) | 1.030 → 1.037 | root | 0.375 → **0.462** | 0.388 → 0.369 | UNRESOLVED |
| G3 gas only (3.6) | 0.389 → 0.392 | floor | – | 1.000 | RESOLVED-FLOOR |

- **Conversion equivalents** (floor / FLAT / PROXY / H(z)):
  - stars + gas: 0.441 / 0.336 / 0.165 / nan → 0.444 / 0.338 / 0.166 / nan;
  - gas only: 1.401 / 1.296 / 1.125 / 0.950 → 1.411 / 1.305 / 1.132 / 0.957.
- **Inclination rows** (S0 / G1):
  - kinematic 75°: ≤ 4.59 / ≤ 7.14 → ≤ 4.59 / ≤ 7.24;
  - F444W free n (57.3°): ≤ 11.4 / ≤ 15.8 → ≤ 11.4 / ≤ 16.0;
  - F444W n = 1 (55.2°): ≤ 13.1 / ≤ 18.0 → ≤ 13.1 / ≤ 18.2;
  - **870 µm masked: b/a 0.58 (54.5°) → 0.435 (64.2°): ≤ 13.7 / ≤ 18.8 → ≤ 7.49 / ≤ 11.0**;
  - 870 µm unmasked (66.4°): ≤ 6.66 / ≤ 9.81 → ≤ 6.66 / ≤ 9.94.
- **Hand estimates (all hit):** −0.088 dex in D (measured knob Δlog D +0.148 → +0.061); S0 7–8; G1 10–11; the gas radius moves D by about 0.01.
- **Extra (labelled): CFG284/285 STAGE=B.**
  - The frozen headline rows are unchanged.
  - Only the 870 µm knob rows move (`cfg284_stageB_PUBLISHED.diff`, `cfg285_stageB_PUBLISHED.diff`). Each entry is the Δlog s* of the "inclination from the 870 µm axis ratio" knob, then the change in the recipe half-width:
    - CFG284 B0: +0.425 → +0.185; half-width 0.754 → 0.714;
    - CFG284 B1: +0.745 → +0.401; half-width 1.202 → 1.141;
    - CFG285 S0: +0.425 → +0.185; half-width 0.946 → 0.915;
    - CFG285 G1: +0.390 → +0.167; half-width 0.582 → 0.537;
    - CFG285 G2: +0.587 → +0.280; half-width 1.079 → 1.031.
  - The "gas at the 870 µm dust R_e" knob moves slightly (B1 −0.374 → −0.350; G2 −0.822 → −0.731).
  - HE6 (frozen hand estimates for the B1/G1 knobs) goes hit → **MISS**.

## 5. Recorded statements that change (forward addenda are the owner's call; nothing here edits another lane)
- **MNRAS v3.1** (`mnras_a0_lambda_v3.tex`). The text says "We use their table 3 as posted in arXiv:2209.12199v1 … it has not been compared with the published table". It has now been compared:
  - the journal's Table B1 refits one row (J0901+1814);
  - our v1 transcription had one σ₀ slip (BX610);
  - the journal calls the table "Table B1".

  Numbers that would move on the journal table (`C_paper_numbers_PUBFIX.diff`):
  - median y **1.45 → 1.37**;
  - median â₀ **1.4 → 1.5 × 10⁻¹⁰**;
  - slope **−0.11 ± 0.06 → −0.09 ± 0.06** (§sec:existing and the conclusions);
  - without the flagged rows **−0.09 → −0.07 ± 0.06** (still about 0.3σ);
  - controlling for g_obs **−0.14 → −0.12 ± 0.06**;
  - controlling for y **+0.01 → +0.02 ± 0.05**;
  - β = −0.05: **+0.02 → +0.04 ± 0.06** (constancy +0.6σ, halo law matched 1.9σ, "about 2σ" still holds);
  - β = −0.10: **+0.16 ± 0.07 → +0.175 ± 0.070** and "2.3σ from constancy" → **2.5σ**;
  - the halo law comes within 2σ already at β = −0.05 in the matched fit (was −0.075).

  Unchanged at the printed precision:
  - the 68% y range (0.33–5.3), "15 of 99 below 0.3" and the 0.4 dex scatter;
  - the matched comparators (+0.22, +0.15) and the injections;
  - the edge-galaxy 0.4σ;
  - "0.2 dex becomes 0.6 dex at the median" (A_obs at the median 3.9 → 3.8, so 0.58 → 0.56 dex, still "0.6");
  - CFG217's ρ = +0.33, p = 0.036.

  Fig. 5 (built from the same inversions) would move row 87's point by +1.05 dex.
- **CFG0 F14 and STANDING.md (root):** "−0.112 ± 0.063, 2.6–4.3σ" → **−0.092 ± 0.064, 2.3–4.1σ**. The root STANDING's L331 line, "a ~3σ trend against non-evolving ΛCDM halos", becomes **+2.3σ**, below L331's own 2.5σ line. L320 "3.0–3.4σ" (2.8–3.2σ after CFG289) → **2.4–2.9σ**.
- **CFG0 addendum / STANDING_2026-09-29 CFG289 entry:**
  - "the tie rests on L331 alone (framework +0.3σ, ΛCDM +2.6σ)" → **+0.1σ / +2.3σ**;
  - L323's best cell [−0.038, −0.007] → **[−0.042, −0.012]**; without the flagged rows [−0.034, −0.004] → **[−0.041, −0.009]**;
  - k-hzs RC100 slope −2.00σ → **−1.83σ**.
- **CFG216/217 record (STANDING §4):** the rival separations of CFG216 (4.9–5.5σ) become 4.5–5.0σ. The record already says "not to be quoted". CFG217: M2 now YES and V2 now NO, which strengthens "gas-route-limited".
- **a₀(z) chart:** the faint RC100 Q4 marker 0.99 → 1.07. The route-B markers are unchanged.
- **ADF22.5:**
  - The `data_assembly/adf22_5_literature_2026-10-02/` alma870_* and umehata25_870um_masked_* rows are the arXiv v1 values; the journal differs (above).
  - In the CFG284/285 READMEs: "870 µm (54.5°) +0.43 / +0.75 / +0.39" → **64.2°: +0.19 / +0.40 / +0.17**.
  - The CFG285 post-hoc addendum's "54.5–57.3° raise S0 to ≤ 11–14 and G1 to ≤ 16–19" → ALMA 64.2°: **≤ 7.5 / ≤ 11.0**; F444W unchanged.
  - "Kinematic vs morphological inclinations disagree by 3σ" now holds for F444W (57.3°, 2.95σ) but not for ALMA (64.2°, 1.8σ).
  - The CFG284 record's "recipe half-width 0.75 dex" → **0.71**.

## 6. Failed or disclosed
- **Departures from CFG289's code (disclosed):**
  - **Clones instead of byte copies.** Materialised read-through files are APFS copy-on-write clones. The first group-O attempt filled the disk while byte-copying ~47 GB of real_research cubes; it was deleted and re-run.
  - **Mirror-path normalisation.** `cfg305_compare.py` replaces the mirror paths before comparing FIX with ORIG.
  - **Unique log tags.** Corrected-mode runs carry tags such as `__RC100_INPUT-corrected`.
- **The two group-O mirrors were built at different HEADs** (O_ORIG at 21:37 = 10dfc8a22; O_FIX at 22:03 = 5f436da8c). The commits in between touched only CFG303, CFG294, the chart, STANDING and a data_assembly note. No entry script or common module reads them (checked by grep). The reproduction control and every FIX-vs-ORIG line trace to RC100. Group C (22:28/22:30) and the ADF mirrors (21:39/21:40) each share one HEAD.
- **Write-through flags from parallel sessions:**
  - The C_ORIG paper_numbers run flagged a changed link target, `CFG308/cfg308_cristal_stress.py`. A parallel session edited it at 22:29:28. paper_numbers never references CFG308, and its ORIG output and stdout reproduce the committed ones exactly, so the run is kept.
  - The first group-C attempt flagged CFG294 files edited by another session in the same way. It was discarded anyway, because it overlapped the disk-full event; the group-C results come from the clean re-run.
  - The ADF runner's first complete PUBLISHED run flagged changed targets without listing them. It was re-run with the targets listed: none changed. The post-hoc rows of both runs are identical.
  - The ADF checks now list CFG294 targets without counting them; none appeared.
- **Run-time field.** CTRL cfg284 stage-B differed from the committed file only in a run-time field, "(4 s)" vs "(5 s)". It is normalised by CFG289's run-time rule; the normalisation was added after that first run.
- **A correction to the brief.** The repo's 870 µm values did not come "from arXiv v1 via a summary" alone: `adf22_pdf_direct_reads_A7.csv` records a direct read of the arXiv v1 PDF, and those values equal v1 exactly. The difference is v1 → journal, not a reading error.
- **The flip detector** does not see YES/NO words. CFG217's word changes and CFG223's Y/n flag were found by reading the diffs. The 1σ judgements were made by reading them, as frozen.
- **The data-release chat's committed note** (`data_assembly/PUBLISHED_VS_ARXIV_CFG287_2026-10-02.md`, a073efda0) says the PDFs now sit in `~/new_physics/_external_data/papers/`. This lane read them from that chat's scratch copy, and the sha256s match.
- **FS+18 is not re-checked** here.

## Files (all untracked; the orchestrator re-runs and commits)
- **Criteria:** `FROZEN_CRITERIA.md` (committed, 82dfcc1b3).
- **Scripts:**
  - `cfg305_confirm.py`;
  - `cfg305_build_published.py`, which writes `real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv`;
  - `cfg305_rerun.py`, `cfg305_supplement.py`, `cfg305_compare.py`;
  - `cfg305_adf22_geometry.py`;
  - `cfg305_posthoc_chart_readers.py` (post hoc).
- **Outputs:**
  - `cfg305_confirm.out/_results.json`, `cfg305_build_published.out/_results.json`;
  - `cfg305_compare_{O,C}.out/_results.json`;
  - `*_PUBFIX.diff` and `*_PUBFIX.*` (FIX outputs; the group-C ones are prefixed `C_`);
  - `cfg305_l323_flagged_{ORIG,FIX}.out`, `cfg52_{pooled,mock_bias}_{ORIG,FIX}.out`, `cfg90_mirrorpath_{ORIG,FIX}.out`;
  - `cfg305_adf22_geometry.out/_results.json`, `cfg285_posthoc_expfit_geometry_PUBLISHED.out/_results.json`, `cfg28{4,5}_stageB_PUBLISHED.diff`;
  - `cfg305_posthoc_chart_readers.out`, `*_POSTHOC_PUBFIX.diff`.
- **Re-run order:**
  1. `cfg305_confirm.py <journal dir>`
  2. `cfg305_build_published.py`
  3. `cfg305_rerun.py <s> O ALL`
  4. `cfg305_rerun.py <s> C ALL`
  5. `cfg305_supplement.py <s>`
  6. `cfg305_compare.py <s> O`, then `cfg305_compare.py <s> C`
  7. `cfg305_adf22_geometry.py <s2>`
  8. (post hoc) `cfg305_posthoc_chart_readers.py <s>`
