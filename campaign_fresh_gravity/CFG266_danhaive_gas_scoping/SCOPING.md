# CFG266: gas masses for the 41 Danhaive+25 gold JADES discs (scoping, page reads only, 2026-10-01)

> **kappa = 1/2 is FITTED. a0(z) FLAT is the framework's distinctive law; a0 proportional to H(z) is the rival. No a0 analysis is made here and no s\* is computed.** The only numbers taken from the record are CFG273's own columns (`gas_to_star_req`, `lever`, `y`, `D`) and the CFG240 break-even table. **Nothing was downloaded.** Every source below was read as a web page (arXiv HTML/abstract, a PDF streamed to text without saving, VizieR/MAST listings, or a page reader), or from files already on disk. Anything not checked against its primary page is marked **UNVERIFIED**. Nothing is committed.
> Script: `cfg266_gas_scoping.py` (field per row, requirement fluxes, counts, precision arithmetic). Outputs: `cfg266_gas_scoping.out`, `cfg266_rows.csv`. `MUTATE=1` inverts the field rule and must fail control C2: it does (exit 1, `cfg266_gas_scoping_MUTATE1.out`).

## Bottom line
1. **Coordinates: not obtainable from page-read tables.** The paper prints no RA/Dec, VizieR has no catalogue for it, and none of nine follow-up or related papers prints a position for any of the 41 IDs. **The FIELD of every row is fixed, by two independent rules that agree for all 41:** **38 GOODS-N** (33 CONGRESS F356W + 5 FRESCO F444W) and **3 GOODS-S** (191250, 214966, 201125; FRESCO).
2. **ALMA cannot observe GOODS-N.** Its adopted upper declination limit is +47°, and GOODS-N is at +62°. So **GOODS-ALMA 2.0, ASPECS, CRISTAL, REBELS and the ALMA archive can reach at most the 3 GOODS-S rows.**
   - In GOODS-N the public millimetre data are single-dish dust maps (SCUBA-2 SUPER GOODS, NIKA2 N2CLS), VLA COLDz (CO(2–1), z 4.91–6.70 only), and NOEMA (the 8.5 arcmin² HDF-N 3 mm scan, plus 116 targeted pointings of other sources).
   - **No row has a gas measurement.**
3. **Count.** The ceiling of 12 below assumes every row lies inside the relevant footprint; the expected numbers are estimates (section 3).
   - **10 rows cannot be moved by gas on the FLAT side:** 7 floor rows (D ≤ 1) and 3 rows whose stars-only bound is already below s = 1.
   - **2 rows are ceiling rows:** their requirement was not computed in CFG273.
   - **29 rows need gas for FLAT.**
   - **Favourable end of the conversions:** 12 rows are "powered" (the gas FLAT needs would give a flux at or above 3σ of some survey) **if they lie inside that survey's footprint**, which cannot be checked without positions. Expected number of usable limits: **about 3–5 (estimate).**
   - **Generous end** (gas-to-dust ×2 and the CMB contrast; sub-thermal CO): only the 3 GOODS-S rows stay powered, through ASPECS, and only if they fall in its 4.2 arcmin² (about 7% each). In GOODS-N, at most 2 rows remain, through NOEMA HDF-N. Expected number: **0–1 (estimate).**
4. **Precision.** Separating FLAT from a0 ∝ H(z) at z ≈ 4.2 (Δlog a0 = 0.81 dex; 0.94 at z 5.3) at 3σ needs a **common-mode baryon calibration of at most about 0.09 dex.** That uses CFG273's median per-row lever, 2.95, at stars-only baryons.
   - It is 0.24 dex with the pooled lever (1.15) and 0.06 dex with PAPER38's 4.8. Adding the gas FLAT needs makes every one of these tighter.
   - **What current tracers can do:** no public anchor pins the common mode to 0.10 dex even at z ≥ 1.6 (PAPER38; GAS_ANCHOR_SCOPING). The bracket at z ≈ 2.2 is about 0.2–0.7 dex, and these discs are at z 3.8–5.8 with sub-solar metallicity.
   - **Not reachable with current tracers.** The per-galaxy random part (for example [CII]'s 0.3 dex) would average down over about 30 detections; the common mode would not.
5. **Downloads that would be needed (not done; owner's go):**
   - positions: the JADES DR3 GOODS-N photometry catalogue (780 MB) and the DR2 GOODS-S-deep catalogue (642 MB), or the authors (section 5);
   - for the 3 GOODS-S rows: the ASPECS 1.2 mm continuum image and the GOODS-ALMA 2.0 maps;
   - in GOODS-N: the N2CLS maps, the SUPER GOODS 850 µm map and the NOEMA HDF-N cubes.
   - COLDz is not needed (0 rows powered).
6. **Side results (no re-run made):**
   - **The CRISTAL-08 z-candidates cannot be CRISTAL-08.** 1088814, 1077545 and 1086406 are GOODS-N rows; CRISTAL-08 is in GOODS-S. CFG273/CFG235 flag three candidates; the brief named two.
   - **The repo's 41-row table is arXiv v1.** The published MNRAS version has a 37-galaxy gold sample.

## 1. Coordinates (question 1)
**What was checked, and what each source holds**
- **Danhaive+25, arXiv:2503.21863 TeX on disk** (`../_external_data/arxiv_src/2503.21863/main.tex`, read-only).
  - The gold table (`tab:results-gold`, header line 820, caption line 854, continued at line 862) has the columns JADES ID, z, log M\*, log SFR, r_e, v/σ0, σ0, log M_dyn. **No RA/Dec.**
  - Line 209: "we obtain 41 galaxies in the gold sample, 132 in the silver sample, and 99 in the unresolved sample".
- **arXiv abstract page:** one version only ("Version 1 (v1): Thursday, 27 March 2025"); journal reference MNRAS (2025) 3249–3302 (page reader).
- **The published MNRAS version (OUP page, read twice by the page reader; direct requests return HTTP 403):**
  - "comprised of 213 H α emitters";
  - "we obtain 37 galaxies in the gold sample, 126 in the silver sample, and 50 in the unresolved sample".
  - **So the repo's `danhaive2025_gold.csv` (41 rows) is the v1 table.** Which rows were dropped, and whether values changed, is **UNVERIFIED**: the published table could not be read. This matters for CFG273, which used all 41.
- **VizieR J/MNRAS/543/3249:** "Catalogue is not found or not available" (cdsarc page).
- **Related papers.** Each HTML page was streamed and grepped for all 41 IDs, nothing saved:
  - Danhaive+25b, arXiv:2510.14779 (163 galaxies; abstract: "Gas masses are estimated via scaling relations", median f_gas 0.77): 0 IDs;
  - arXiv:2510.06315 (Hα sizes): 0;
  - Lin+25, arXiv:2504.08028 (888 GOODS-N HAEs; its Data Availability lists only the MAST survey DOIs, no catalogue): 0;
  - arXiv:2505.02895: 0;
  - arXiv:2505.02896: 0;
  - Covelo-Paz+25, arXiv:2409.17241: 0;
  - arXiv:2601.15961: 0;
  - arXiv:2306.02468 (uses RA/Dec names, not integer IDs): 0;
  - the geko paper, arXiv:2510.07369: 1 ID, 1025527, in "Figure 9: … a galaxy in the FRESCO survey (JADES ID 1025527)", with no position.
- **The repo:**
  - `grep -i jades` over `data_assembly/` and `real_research/data/` finds only the Danhaive table and its build files, plus mentions in `Z2_Z5_UNCOMPUTED_RAR_DATA_2026-09-30.md`, `ALMA_CUBES_FETCHED_2026-09-30.md` and two cached HTML pages.
  - `../_external_data/` holds the Danhaive TeX source (no positions; the `Summaries/` PNGs are labelled by ID) and **no JADES catalogue**.
- **A Zenodo grism redshift catalogue matched to JADES IDs** (10.5281/zenodo.18328404) is the JADES Origins Field, GTO-4540, in GOODS-S, not the CONGRESS/FRESCO sample (Zenodo API record metadata).

**Field per row: two independent rules, both page-verified, agreeing for all 41** (control C2; MUTATE=1 bites)
- **ID rule.** 7-digit IDs starting with 10 are GOODS-N. arXiv:2505.02895 (HTML) writes "GN-1034620" and "JADES ID: 1080661; RA = 189.27616 deg, Dec = 62.21416 deg", "JADES ID: 1089616; RA = 189.18713 deg, Dec = 62.27289 deg", and its table note says "IDs are from JADES DR2". 6-digit IDs are GOODS-S.
- **Filter rule.** Paper line 178: FRESCO "F444W filter (3.9–5.0 µm) in both GOODS fields" and CONGRESS "F356W filter (3–4 µm) … in GOODS-N" (also line 167). Hα (6564.61 Å) falls in F444W only for z ≥ 4.941, so the **33 rows at z < 4.941 must be CONGRESS, i.e. GOODS-N.** All 33 have 7-digit IDs.
- Of the 8 FRESCO rows (z ≥ 5.18), five are GOODS-N (1028887, 1002030, 1002222, 1025527, 1001674) and three are GOODS-S (191250, 214966, 201125).
- `cfg266_rows.csv` carries the field, the grism survey and a z-only protocluster tag.

**Redshift-only screens (positions are needed to resolve any of these)**
- **CRISTAL-08** (vuds_efdcs_530029038, z 4.43) sits at RA 53.0793, Dec −27.8771: GOODS-S (`data_assembly/arxiv_tables/cristal2025_sample.csv`). The CFG273 z-candidates 1088814, 1077545 and 1086406 (z 4.41–4.42) are GOODS-N by both rules. **They are not CRISTAL-08**, so the P38 pooled row's exclusion was unnecessary. Nothing was re-run.
- **CRISTAL's other GOODS-S discs** are CRISTAL-12 (z 5.572) and CRISTAL-16a (z 5.571). Both are |dz| ≥ 0.03 from 214966 (z 5.54).
- **ALPINE DR1** (VizieR J/A+A/643/A2, 118 rows; 13 have Dec < 0, all ECDFS/GOODS-S):
  - no target lies within |dz| ≤ 0.02 of 191250 (5.39) or 201125 (5.82);
  - **three lie within it for 214966 (5.54):**
    - CANDELS_GOODSS_14: z_CII 5.5527, [CII] 0.15 Jy km/s, RA 53.0788, Dec −27.8841, log M\* 10.49;
    - CANDELS_GOODSS_42: z_CII 5.5252 (z_orig 5.543), 0.07 Jy km/s, RA 53.1659, Dec −27.8828, log M\* 9.38;
    - CANDELS_GOODSS_57: no [CII]; z_orig 5.559; RA 53.1626, Dec −27.8731.
  - The redshift differences against an Hα z of 5.54 ± 0.005 are ≥ 350 km/s (GOODSS_14) and ≥ 450 km/s (GOODSS_42, from its [CII] z), so **an identity is unlikely and unresolved.**
- **GOODS-ALMA 2.0** (88 sources on disk, 86 with a catalogue z): **no source has z ≥ 4.9.** If a GOODS-S row lies inside that mosaic, it is a catalogue non-detection, unless its counterpart's (mostly photometric) catalogue z is wrong.
- **Lin+25 protoclusters** (abstract: "two prominent filamentary protoclusters at z ≈ 4.41 and z ≈ 5.19", GOODS-N, ~62 arcmin²):
  - 7 GOODS-N rows are z-consistent with z ≈ 4.41: 1088814, 1087148, 1077545, 1014130, 1086406, 1028072, 1008197;
  - 3 rows are z-consistent with z ≈ 5.19: 1028887, 1002030, 1001674.
  - The z ≈ 5.19 structure contains HDF 850.1 and the N2CLS z ~ 5.2 dusty overdensity (arXiv:2506.15322 abstract).
  - **UNVERIFIED (not read):** whether the rows at z 4.02–4.07 belong to the GN20 structure at z ≈ 4.05.

## 2. Gas tracers that exist now (question 2)
"Powered" means the gas FLAT needs (CFG273's `gas_to_star_req` × M\*) would give at least 3σ at the survey's quoted depth (section 3).

**GOODS-N (38 rows)**
- **ALMA anything:** **no coverage possible.** ALMA Cycle 13 Proposer's Guide, section A.8 (page text): "The adopted upper declination limit for ALMA is +47°, corresponding to a maximum elevation of 20° at the ALMA site." The GOODS-N positions above are at Dec +62.2°.
- **SUPER GOODS SCUBA-2** (Cowie+2017, arXiv:1702.03002):
  - covers the whole of GOODS-N, at 850 µm (dust);
  - depth (abstract): "central rms noise of 0.28 mJy and 2.6 mJy" at 850 and 450 µm. The depth outside the centre was not read: **UNVERIFIED**;
  - catalogue: VizieR J/ApJ/837/139 table5, "SCUBA-2 850um (4σ)", **186 rows**. It lists only ≥4σ sources, so a non-detection there is not a limit; the map would be needed;
  - powered: **2 rows** (1001674, 1090891) at the central depth, favourable end only; 0 at the generous end.
- **N2CLS NIKA2** (arXiv:2506.22046, section 2.1):
  - covers GOODS-N at 1.2 and 2 mm (dust). Text: "The GOODS-N field covers 159 arcmin2 with a 1 σ depth of 0.17 mJy/beam and 0.047 mJy/beam at 1.2 mm and 2 mm"; beam ~12″ and ~18″; "These data are close to the confusion limit";
  - catalogue: Table 2, the 2 mm high-quality (95% purity) catalogue; row count not counted. Data at data.lam.fr/n2cls/;
  - powered: **2 rows** (the same two), favourable end only; 0 at the generous end. The large beam means blending.
- **COLDz VLA** (arXiv:1808.04372):
  - covers "~51 arcmin²" of the GOODS-N wide field (abstract), with CO(2–1) at "z = 4.91–6.70";
  - depth (Appendix D.2): "median 6σ limits … of 0.18 mJy beam−1 and 0.55 mJy beam−1 for the COSMOS and GOODS-N fields", for a 200 km/s line;
  - catalogue: line candidates in the paper; not counted;
  - powered: in the z window, 5 rows with a requirement; **0 powered**, even at α_CO = 4.36 with r21 = 1.
- **NOEMA HDF-N 3 mm scan** (Boogaard+2023, arXiv:2301.05705):
  - covers "8.5 arcmin2" (45 pointings) centred on HDF-N, about 14% of the ~62 arcmin² grism area;
  - frequency range 82.394–113.322 GHz (Table 1 note): CO(4–3) at z 3.07–4.59, CO(5–4) at z 4.09–5.99, [CI](1–0) at z 3.34–4.97;
  - rms 0.42–0.95 mJy/beam per 9 MHz (Table 2);
  - catalogue: "the 7 highest-fidelity sources as CO emitters at 1 < z < 6, including … HDF 850.1";
  - powered: **9 rows, only for thermalised CO (r_J1 = 1).** Each row stays powered only above an excitation of: 1001674 CO(5–4) 0.34, 1090891 CO(4–3) 0.40, 1000110 0.47, 1090054 0.51, 1025527 0.67, 1094903 0.74, 1013488 0.82, 1002030 0.88, 1029814 0.90. Typical main-sequence excitation was not read: **UNVERIFIED.**
- **Other NOEMA observations** (log VizieR B/iram/noema, cone of 9′ around 189.23, +62.24; 568 log rows):
  - 116 distinct pointing centres (134 programme-target pairs), all targeting OTHER sources: PHIBSS-type programmes (L14GN…), L19MD…, N2CLS follow-ups (W21CV…, N2GN-…), GN-z11, GN-z10-3, GNQZ7 and others;
  - a 3 mm primary beam of about 50″ means serendipitous coverage is possible, but tuned for other redshifts;
  - no catalogue; the observations are headers only;
  - powered: unknown without positions. One N2CLS source at z = 5.182 was confirmed with targeted NOEMA (arXiv:2506.15322).
- **IRAM archive access** (search summary; **UNVERIFIED verbatim**): Large Programme data public after 18 months; standard programmes on request after 3 years.

**GOODS-S (3 rows: 191250, 214966, 201125)**
- **GOODS-ALMA 2.0** (Gómez-Guijarro+2022, arXiv:2106.13246; read on disk via `data_assembly/goodsalma_crossmatch/README.md`):
  - covers 72.42 arcmin² centred 03:32:30, −27:48:00, at 1.13 mm (265 GHz; dust);
  - depth: rms 67.7–68.8 µJy/beam per slice;
  - catalogue: **88 sources** (on disk); none at z ≥ 4.9;
  - overlap with FRESCO GOODS-S: **UNVERIFIED**;
  - [CII] is not in its band at these redshifts (it would need z 5.9–6.5);
  - powered: 2 at the favourable end (191250, 201125); 1 at gas-to-dust ×2 (201125); **0** with the CMB contrast.
- **ASPECS** (arXiv:2002.07199):
  - covers the HUDF: "2.9 (4.2) arcmin² within a primary beam response of 50% (10%)", about 7% of a ~62 arcmin² mosaic;
  - 1.2 mm (dust); depth "9.3 µJy beam−1";
  - catalogue: "35 sources at high significance";
  - powered: **3 rows, at every calibration end.** Whether any of the 3 is in the HUDF is unknown.
- **CRISTAL** (arXiv:2507.11600; on disk):
  - covers ALPINE targets in COSMOS and ECDFS; [CII] at 4.4–5.7;
  - catalogue: 32 galaxies (sample table); 3 in GOODS-S (08, 12, 16a);
  - none can be a gold row (section 1).
- **ALPINE** (VizieR J/A+A/643/A2):
  - targeted [CII] and continuum at z 4.4–5.9;
  - catalogue: **118 targets**, 13 in ECDFS/GOODS-S;
  - only z-coincidences with 214966 (section 1).
- **REBELS** (arXiv:2106.13719):
  - covers "40 of the brightest UV-selected galaxies identified over a 7-deg² area", at "z>6.5";
  - **excluded by redshift:** the gold rows reach z 5.82 at most.
- **A3GOODSS ALMA archive mining** (arXiv:2403.03125):
  - covers archival ALMA continuum in COSMOS and GOODS-S: "~4,000 pipeline-processed continuum images … 2,050 unique detected sources";
  - catalogue on CDS, per `data_assembly/GOODSALMA_HOSTING_2026-09-29.md`; size not checked;
  - this is the route for "the ALMA archive by position", once positions exist.
- **JADES-ALMA or other targeted programmes:** none found by these page reads. The search was not exhaustive.

**[CII] in GOODS-N** would need NOEMA band 4. The requirement fluxes (Zanella+2018, as quoted in arXiv:2004.10771 on disk, lines 212 and 228–232: log L = −1.28 + 0.98 log M_mol, "0.3 dex dispersion") are 0.006–3.9 Jy km/s (29 rows) and are listed in the CSV. They describe future observations; no public [CII] data cover GOODS-N gold rows. The upper frequency of NOEMA band 4, and hence which z rows it can reach, is **UNVERIFIED**.

## 3. Count (question 3)
**Definitions**
- A "meaningful upper limit" here is a 3σ non-detection at a known position that lies **below the gas FLAT needs** (CFG273 `gas_to_star_req` × M\*, canonical footing).
  - It can only exclude FLAT's gas need row by row.
  - CFG273 has no rival-side requirement and none is computed here, so a limit says nothing about the rival.
  - Only a **calibrated detection** constrains both laws.
- The requirement fluxes use CFG142's conversion. Control C3 reproduces CFG142's committed KURVS-11 value: 0.9121 against 0.912 mJy.
  - **The favourable end:** solar gas-to-dust, Galactic α_CO = 4.36, r_J1 = 1.
  - **The generous end:** gas-to-dust ×2, plus the CMB contrast at 25 K.
  - T_d is fixed at 25 K. A warmer dust temperature would raise the dust flux, so the temperature is not a favourable choice.
  - The line FWHM is max(200, 2.355 σ0) km/s.

**Rows by category** (all 41)
| category | n | rows |
|---|---|---|
| floor (D ≤ 1): gas cannot change the FLAT reading | 7 | 1088814, 1015956, 1085659, 1082948, 1091153, 1086406, 1009935 |
| stars-only bound already below s = 1 | 3 | 1090526, 1086992, 1079264 |
| ceiling (requirement above CFG273's bracket, not computed) | 2 | 1094616, 1025101 |
| needs gas for FLAT | 29 | the rest; requirement per row in the CSV (1090742 needs only 0.04 M\*) |

**Powered, if inside the footprint** (`cfg266_gas_scoping.out`, COUNTS)
- GOODS-N dust:
  - SCUBA-2 central depth: 2 rows (1001674, 1090891);
  - N2CLS 1.2 mm and 2 mm: the same 2;
  - all **0** at gas-to-dust ×2.
- GOODS-N COLDz: 0 of 5.
- GOODS-N NOEMA HDF-N: 9 (thermalised CO only; excitation thresholds in section 2).
- GOODS-S GOODS-ALMA 2.0: 2 at the favourable end, 1 at ×2, 0 with the CMB contrast.
- GOODS-S ASPECS: 3 at every end.
- **Union, favourable end: 12 rows:** 1002030, 191250, 214966, 1025527, 1001674, 201125, 1090054, 1000110, 1094903, 1013488, 1090891, 1029814.

**Expected number of usable limits — ESTIMATE**
- Method: P(inside) is the footprint area over a ~62 arcmin² grism area, assuming the rows are spread uniformly (they cluster, so this is rough). Lin+25 gives the ~62 arcmin² for GOODS-N; using the same area for FRESCO GOODS-S is **UNVERIFIED**.
- **Favourable end:**
  - 2 GOODS-N dust rows, but the maps are confused and the 850 µm depth is the central value;
  - plus 9 × 0.14 ≈ 1.2 from HDF-N (higher for the three z ≈ 5.19 rows, since HDF 850.1 is inside the scan);
  - plus ≤ 2 from GOODS-ALMA (overlap UNVERIFIED);
  - plus 3 × 0.07 ≈ 0.2 from ASPECS.
  - **About 3–5 rows.**
- **Generous end** (and r_J1 ≲ 0.4, UNVERIFIED as typical): 2 × 0.14 + 0.2 ≈ **0.5, i.e. 0–1 row.**
- **Gas measurements on hand: 0.**
- With positions, the "if inside" condition becomes a count, and the local rms replaces the survey average.

## 4. Calibration caveat and the precision needed (question 4)
**The record's position**
- PAPER38 (DOI 10.5281/zenodo.23085582; TeX on disk, abstract line 33):
  - "The gas calibration at z ≈ 2.2 is a prescription bracket (~0.2–0.7 dex); tracer agreement does not fix the absolute scale, and no public dynamics-independent anchor reaches 0.10 dex";
  - "A decisive a0(z) test needs baryon errors and band ≤ 0.10 dex".
- `data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`, bottom line 1: "No public route pins the common-mode gas calibration at z >= 1.6 to 0.10 dex."
- CFG238, bottom line 2:
  - K is the error of a pooled mean, not a per-galaxy gas error;
  - the SD of log α_CO is 0.18 at z ≥ 1.6;
  - "A common-mode bias is invisible to every diagnostic and is bounded by nothing on disk that is independent of the dynamics under test."
- **These discs are harder still.** They are at z 3.8–5.8 with log M\* 8–10.7, so their metallicities are sub-solar (not measured here). α_CO, the gas-to-dust ratio and α_[CII] are extrapolated there, and the CMB is 13–18.6 K against a 25 K dust temperature.

**Precision needed** (`cfg266_gas_scoping.out`, PRECISION; arithmetic on CFG273's own columns)
- The rival-to-FLAT separation in log a0 is log10 E(z): 0.81 dex for PALL (z 4.17; E = 6.49–6.65 for Ωm 0.30–0.315) and 0.94 dex for Pz3 (z 5.30).
- A common-mode baryon error σ_cal moves log s\* by |lever| σ_cal. That does not average down, so a 3σ separation needs σ_cal ≤ log10 E / (3 |lever|):

| row | z | Δlog a0 | σ_cal (3σ), pooled lever | median per-row lever (2.95) | PAPER38 lever 4.8 | CFG240 T4 floor 3·0.2/√N |
|---|---|---|---|---|---|---|
| PALL | 4.17 | 0.812 | 0.236 (lever 1.15) | 0.092 | 0.056 | 0.094 |
| Pz1 | 4.04 | 0.796 | 0.179 (1.48) | 0.090 | 0.055 | 0.131 |
| Pz2 | 4.42 | 0.842 | 0.228 (1.23) | 0.095 | 0.058 | 0.173 |
| Pz3 | 5.30 | 0.939 | 0.264 (1.18) | 0.106 | 0.065 | 0.212 |
| P38 | 4.16 | 0.811 | 0.227 (1.19) | 0.092 | 0.056 | 0.097 |

- **These are upper bounds on the allowed σ_cal.** The levers are at stars-only baryons (y 0.08–8.8). The gas FLAT needs (2.8–5.7 × M\* pooled) raises y by 3.8–6.7 times, toward the Newtonian side, where |lever| grows (per-row conditioned |lever| ranges 1.31–8.49).
- **So the requirement is of order ≤ 0.1 dex common-mode, the same as PAPER38's line.**

**Self-calibration with the calibration left free** (CFG240 README, section 4, the 0.1 dex target)
- For y_min = 0.1, which is roughly where this sample would sit once gas is added:
  - N = 50 at per-point σ = 0.1 dex needs y_max\* = 2.51 (P2) or 7.94 (ν_mono);
  - **N = 20 at σ = 0.1 never reaches it;**
  - **at σ = 0.2 dex, no N ≤ 100 reaches it**, for either kernel.
- **The 3σ FLAT-vs-H(z) target (about 0.27 dex in log a0) is easier, but CFG240 does not tabulate it.** A forecast at N ≈ 29–41 with the gas-inclusive y distribution is a calculation-thread item; it was not run here.
- The CFG240 T4 floor for these N is 0.09–0.21 dex at σ = 0.2 (as CFG273 states).

**Can current tracers reach it? No.**
- The random part could work. A 0.3 dex per-galaxy gas error (the [CII] scatter) times the median lever 2.95, over √29 detections, is about 0.16 dex on the pooled log s\*, against a 0.81 dex separation (my arithmetic).
- The common mode cannot. No anchor exists at z ≥ 1.6 to 0.1 dex, and at z 4–6 the metallicity-dependent conversions add more.
- The dust route also carries T_d and the CMB: the CMB contrast at 25 K is 0.61–0.95 across these rows and bands (CSV), and its sign and size depend on the assumed T_d.

## 5. Downloads that would be needed (question 5; none performed; each needs the owner's go)
| # | item | source | size | why |
|---|---|---|---|---|
| D1 | `hlsp_jades_jwst_nircam_goods-n_photometry_v1.0_catalog.fits` (DR3) | MAST `archive.stsci.edu/hlsps/jades/dr3/goods-n/catalogs/` | **780 MB** (listing, 2024-03-28) | positions for the 38 GOODS-N IDs. **ID-version check first:** the 2505.02895 pairs 1080661 → (189.27616, 62.21416) and 1089616 → (189.18713, 62.27289) must reproduce; Danhaive's IDs may predate DR3 and DR5 renumbering, which is **UNVERIFIED** |
| D2 | `hlsp_jades_jwst_nircam_goods-s-deep_photometry_v2.0_catalog.fits` (DR2) | MAST `.../dr2/goods-s/catalogs/` | **642 MB** | positions for 191250, 214966, 201125 |
| D1′ | alternative to D1/D2: the authors' positions for the 41 (no download; the owner decides on any contact) | the authors | — | 41 rows instead of about 1.4 GB |
| D1″ | JADES NIRSpec GOODS-N line-flux catalogues (DR3 v1.1: 970 KB and 1.1 MB; DR4 v1.2: 32 MB) | MAST | 1–32 MB | cheap partial positions, only for gold rows that were NIRSpec targets (unknown how many) |
| D3 | ASPECS 1.2 mm continuum image | ALMA LP page (`almascience.eso.org/alma-data/lp/ASPECS`) | image size not listed (the full band-6 tarball is **902 GB**; only the continuum image is needed) | the 3 GOODS-S rows are powered at every end if inside the HUDF |
| D4 | GOODS-ALMA 2.0 maps and noise maps | ALMA archive | not priced | local rms at the GOODS-S positions (the HTML has none) |
| D5 | A3GOODSS catalogue | CDS (VizieR name not found) | not checked | other archival ALMA continuum at the GOODS-S positions |
| D6 | N2CLS GOODS-N 1.2 and 2 mm maps | `data.lam.fr/n2cls/` | **not readable** (JavaScript cookie challenge) | per-position dust limits (2 rows powered, favourable end only) |
| D7 | SUPER GOODS SCUBA-2 850 µm map | JCMT archive or the authors (the VizieR catalogue has only ≥4σ sources) | not priced | the same 2 rows |
| D8 | NOEMA HDF-N 3 mm cubes (projects W18DI001/W19CR001 per the log) | IRAM archive | not checked; proprietary status **UNVERIFIED** | up to 9 rows, only if inside the 8.5 arcmin² and the CO excitation is high |
| — | COLDz cubes | — | — | **not needed** (0 rows powered) |
D1 or D1′ comes first. Without positions, no row's coverage can be decided.

## 6. Not verified / open
- **The published 37-row gold table:** its rows and values are not read (OUP blocks direct requests; no supplementary table was seen).
- **The ID system** used by Danhaive (DR2-era internal) against DR3 and DR5.
- **Coverage overlaps:** FRESCO GOODS-S against GOODS-ALMA 2.0, and against the HUDF.
- **Survey details:**
  - the SCUBA-2 depth outside the centre;
  - the N2CLS catalogue size;
  - the IRAM proprietary rules quoted from a search summary;
  - NOEMA band 4's upper frequency;
  - typical main-sequence CO excitation at z ~ 4–5.
- **Membership:** GN20-structure membership of the z ≈ 4.05 rows.
- **The 2 ceiling rows**, whose requirement is not computed in CFG273.
- **The rival side:** no rival-side gas requirement exists in CFG273, and none is computed here.

## Files
- `SCOPING.md` (this file)
- `cfg266_gas_scoping.py`
- `cfg266_gas_scoping.out`
- `cfg266_rows.csv`: 41 rows with field, grism survey, z-only tag, CFG273 columns, requirement fluxes, powered flags at three calibration ends, [CII] requirement
- `cfg266_gas_scoping_MUTATE1.out` and `cfg266_rows_MUTATE1.csv`: the control run, exit 1 as required
- Run: `python3 cfg266_gas_scoping.py`, then `MUTATE=1 python3 cfg266_gas_scoping.py`. It takes seconds and fetches nothing.
