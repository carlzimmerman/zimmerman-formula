# CFG305 — FROZEN CRITERIA: the journal tables against the arXiv copies we used (orchestrator lane, 2026-10-02)

**Written and committed before any CFG305 script exists or runs.** It closes the item CFG287 left open: do the journal versions of the source tables match the arXiv copies the repo used? The owner said yes, in the data-release chat, to fetching the open-access journal PDFs. They sit outside the repo, in **the data-release chat's scratch copy** (that location is never written into a committed or lane file). κ = ½ is FITTED. No knob scans. Nothing is downloaded.

**Disclosed before freezing.** While scoping this file I ran pdftotext on two of the PDFs and looked at the text layer of RC100 rows 78 and 87 and of Umehata+25 Table 3, row ADF22.A7. The values I saw agree with the data-release chat's report. The frozen confirmation below is a script plus a page-image read, and it is the record. No reader was re-run and no derived number was computed before this file.

## Inputs (read in place, never copied into the repo)
- **The three journal PDFs**, each checked against the chat's `SHA256.txt` (control J0):
  - RC100: ApJ 944:78, doi 10.3847/1538-4357/aca9cf, sha256 prefix 25be02d39d50b998. The paper's Table 3 is printed there as Table B1.
  - FS+18: ApJS 238:21, sha256 prefix b3b1390447c1e1c3. It is not part of either reported difference and is not re-checked here.
  - Umehata+25: ApJ 997:79, sha256 prefix c17bf645d8ef3cc7.
- **Repo tables:**
  - `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv` (CFG289, sha256 prefix a1778d75476ede17), never edited;
  - `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv` (the arXiv v1 read), never edited;
  - `data_assembly/adf22_5_literature_2026-10-02/adf22_5_literature_values.csv` and `adf22_pdf_direct_reads_A7.csv`, never edited.
- **Context only (outside the repo, on disk, not downloaded; read but never decisive):**
  - the arXiv v1 RC100 table images (raster) in the external-data folder;
  - the arXiv v1 PDF of Umehata+25 (2502.01868v1) in the external-data folder.

## Step 1 — independent confirmation (`cfg305_confirm.py`; then a page-image read)
- **RC100 Table B1.**
  - The script runs `pdftotext -layout` itself and parses every row 1–100: index, z, log M_baryon, R_e, f_DM, V_c, σ₀.
  - Rows whose R_e/f_DM pair prints on a separate line at a page break are recovered from that line, and the script lists them.
  - It compares all 600 numeric cells with the CORRECTED CSV, numerically at the printed precision.
- **Umehata+25.**
  - The same extraction is run.
  - Table 3, row ADF22.A7, masked and unmasked fits: n, R_e, b/a, PA and their errors.
  - Also Table 4 row A7 (free-n and n = 1), Table C1 row A7 and Table 2 row A7.
  - These are compared with the repo's two ADF22.5 CSVs. The arXiv v1 PDF's Table 3 row A7 is extracted as context.
- **Decision per reported cell.** The reported cells are:
  - RC100 row 87: log M_baryon 10.72, R_e 3.85, f_DM 0.44, V_c 250, σ₀ 37;
  - RC100 row 78: σ₀ 77;
  - Umehata+25 Table 3 masked A7: n 1.42, R_e 1.58 ± 0.15, b/a 0.435 ± 0.05, PA 17.9.

  A cell is **CONFIRMED** if the extracted published value equals the reported value and differs from the repo value. Otherwise it is **REFUTED**.
- **New differences.** Any other published ≠ CORRECTED cell among the 600 counts as a NEW difference. It is re-read on the page image. If the image agrees with the text layer, the cell joins the confirmed set (disclosed). If it does not, the cell is a parse artefact and is excluded (disclosed).
- **Controls that can fail:**
  - **J0:** each PDF's sha256 equals `SHA256.txt`.
  - **J1:** all 100 RC100 rows parse with all six fields.
  - **J2 (positive):** the 12 value cells CFG289 corrected (rows 24, 36, 43, 44, 58, 62, 63, 65, 77, 90, 93, 95) equal the CORRECTED CSV in the published table.
  - **J3 (negative):** the same comparison against the original CSV (`rc100_nestorshachar2023_table3.csv`) must report all 12 of those cells as differences. This proves the comparison can see a difference.
  - **J4:** the Umehata+25 Table 2 and Table 4 A7 values equal the repo's. They are the cells the chat reported as matching.
- **Page-image read (by eye, recorded in README.md).**
  - The published rows 78 and 87 and Table 3 row A7 are rendered to images outside the repo and read.
  - The arXiv v1 RC100 image rows 78 and 87 are read as well.
  - This read is a cross-check of the text layer. It is one reader.

## Step 2 — the PUBLISHED CSV (`cfg305_build_published.py`)
- **Output:** `real_research/data/rc100_nestorshachar2023_table3_PUBLISHED.csv`. It has the CORRECTED CSV's columns, order and line endings, and is built only by the script.
- **Primary cells:** only the cells CONFIRMED in step 1 change. No other primary cell changes.
- **Derived columns:**
  - They are recomputed only in rows where an input of theirs (V_c, R_e or log M_baryon) changed. A σ₀-only change leaves them as they are.
  - The rules are CFG289's:
    - g_Re = V_c²/R_e;
    - a0_Vc4_over_GMbar = V_c⁴/(G M_bar);
    - a0_over_1.2e-10 to 3 decimals;
    - deepMOND = (g_Re < 1.2e-10).
  - The format is CFG289's (`.4e`).
  - The constants are CFG289's: G = 6.674e-11, kpc = 3.0857e19 m, M☉ = 1.989e30 kg.
- **Controls:**
  - **B1:** the constants reproduce the derived columns of every row whose derived cells are not recomputed (≤ 5e-5 relative, as CFG289's C1).
  - **B2:** the header and every untouched row are byte-identical to the CORRECTED CSV.
  - **B3:** exactly the confirmed primary cells differ from the CORRECTED CSV, plus only the derived cells of rows with a changed input.
  - **B4:** the PUBLISHED CSV's six numeric primary fields equal the step-1 published parse in all 100 rows.

## Step 3 — bounding the impact (`cfg305_rerun.py`, `cfg305_supplement.py`, `cfg305_compare.py`)
- **Code.** These are copies of CFG289's `cfg289_rerun.py`, `cfg289_supplement.py` and `cfg289_compare.py`, with the file names parametrised. CFG289's committed files are never edited. Outputs get the suffix `_PUBFIX` (CFG289 used `_RC100FIX`).
- **Readers:** every tracked `.py` that names the RC100 CSV (`git grep -l rc100_nestorshachar2023_table3 -- '*.py'`), run through its entry point, as CFG289. They split into two groups, each in its own pair of scratch mirrors:
  - **Group O (readers of the original path):**
    - CFG289's 32 entry points, in CFG289's order, except that `rc100_input_correction_compare.py` moves to after CFG217/CFG218. It compares their outputs, so it must run after them.
    - Plus four corrected-mode runs (`RC100_INPUT=corrected`): `cfg216_rc100.py`, `cfg216_posthoc_index.py`, `cfg217_attack.py` and `cfg218_ladder.py`. These read the paper-values file, and CFG227, `rc100_input_correction_compare.py` and the MNRAS v3 manuscript read their corrected-mode outputs.
    - Mirrors: ORIG has the CORRECTED CSV substituted at the original path. FIX has the PUBLISHED CSV at the original path and at the CORRECTED path, and the paper-values file with the confirmed cells replaced. The mirror copy is edited; the repo file never is.
  - **Group C (readers of the CORRECTED path):**
    - Entry points, in order: `cfg217_attack.py` (`RC100_INPUT=corrected`, because the manuscript reads its G2 output), the MNRAS manuscript's `qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.py` (read-only, run in the mirror), then `campaign_fresh_gravity/CFG290_mnras_v3_referee/cfg290_referee_checks.py`.
    - Mirrors: ORIG has nothing substituted, so it should reproduce the committed outputs, and paper_numbers' stdout is also compared with its committed `paper_numbers.out`. FIX has the PUBLISHED CSV at the CORRECTED path and the paper-values file with the confirmed cells replaced.
    - The original path is left untouched in group C, because paper_numbers reads it as "the earlier transcription".
  - **Excluded by design (stated):**
    - CFG287 (it reads the tables by design);
    - CFG289's build script (a writer, not a reader);
    - CFG289's driver;
    - `cfg227_rar_z2_5_v1_before_addendum.py` (a superseded copy that writes the same output files as `cfg227_rar_z2_5.py`, so running it in the same mirror would overwrite them).
  - **NOT-RUN by construction:** CFG229 (`cfg229_inputs.py`), CFG270 and CFG280 read only name, z and idx from the paper-values file, and none of these changes in a confirmed cell. This is checked by grep and stated.
- **Supplement:**
  - CFG90 with the mirror-path patch in ORIG and FIX of group O, kept from `cfg289_supplement.py`;
  - CFG52 `pooled.py` and `mock_bias.py`;
  - CFG289's post-hoc L323 flagged-rows re-run, parametrised: ORIG uses the CORRECTED table, FIX the PUBLISHED one, each without rows {67, 83} and without the 16 flagged rows. The flag sets are also re-derived from each table and reported.
- **Reproduction control (group O ORIG):** each output is compared with CFG289's FIX copy (`<name>_RC100FIX.<ext>`, mirror paths normalised) where one exists, and otherwise with the committed file. A difference beyond run-time lines makes the entry NOT-REPRODUCIBLE. The FIX-vs-ORIG difference is still reported.
- **Classification per entry point (CFG289's rules):**
  - **NOT-RUN:** cannot run (the reason is stated).
  - **NOT-REPRODUCIBLE:** see the reproduction control.
  - **UNCHANGED:** FIX equals ORIG apart from run-time fields.
  - **NUMERIC-MINOR:** numbers move, but no pass/fail row flips, no verdict word changes, and each headline shift is < 1σ of that headline's own quoted error.
  - **VERDICT-MOVES:** any of those happens.

  A "mechanical" flip (a reproduction or sha256 row that compares against the old table, so it must fail whenever the input changes) is labelled as such. The 1σ judgement is made by reading the diffs.
- **Consumers.** For every NUMERIC-MINOR or VERDICT-MOVES entry, the documents that quote it (STANDING, papers, the MNRAS manuscript) are listed by grep. For the MNRAS v3.1 text, every quoted RC100 number that would move is listed. So is its statement that the table "has not been compared with the published table" (it names "table 3"; the journal calls it Table B1).

## Step 4 — the ADF22.5 geometry (`cfg305_adf22_geometry.py`)
- **Mirrors.** Two scratch mirrors (git archive of HEAD plus read-through links, as in step 3):
  - **CTRL:** no substitution.
  - **PUBLISHED:** the CONFIRMED Table 3 masked A7 values (n, R_e, b/a, PA and errors as printed) replace `umehata25_870um_masked_*` in the mirror copy of `adf22_pdf_direct_reads_A7.csv` and `alma870_*` in the mirror copy of `adf22_5_literature_values.csv`. Any other confirmed Umehata cell (e.g. an error bar) is substituted the same way.
- **Run:** CFG285's post-hoc script `cfg285_posthoc_expfit_geometry.py`, unmodified except for one disclosed label patch. The two printed labels that quote the arXiv numbers ("870 um masked, b/a 0.58" and "870 um masked, n = 1.01") are rewritten to the published numbers in the mirror copy, each replacement asserted to hit exactly once. A banner naming the variant is prepended to the copied output.
- **Outputs:** `cfg285_posthoc_expfit_geometry_PUBLISHED.out` and `_PUBLISHED_results.json` in this lane, scrubbed of mirror paths.
- **Report.** For each of S0, S1, S2, G1, G2 and G3: D, status, s*, no-root fraction, resolution and rooted intervals, CTRL → PUBLISHED. Also the conversion equivalents and every inclination row, including the 870 µm masked row (thin-disc inclination 54.5° → arccos(published b/a)).
- **Control.** CTRL must reproduce the committed `cfg285_posthoc_expfit_geometry.out` and `_results.json` exactly. If it does not, the variant is reported as NOT-REPRODUCIBLE, with its differences.
- **Extra (labelled; these are the other readers of the 870 µm values).** STAGE=B runs of `cfg284_adf22_5_stars.py` and `cfg285_adf22_5_gas.py` in the same two mirrors. Only their rows that read the 870 µm values are reported (the knob rows "gas at the 870 um dust R_e" and "inclination from the 870 um axis ratio"). CTRL must reproduce the committed stage-B outputs. Their frozen headline rows do not read these values; if any does move, that is reported.

## MUTATE (a control that can fail)
- **The planted change:** in a copy of the PUBLISHED CSV, row 50 (EGS 13011166, not a confirmed row) gets log M_baryon +0.30 dex (11.25 → 11.55). Its derived columns are recomputed with the frozen constants.
- **Substitution:** as in FIX of group O.
- **Run:** `L323_rc100_framework_vs_lcdm_stress.py`, which reads log M_baryon in every row, and `cfg216_rc100.py`, which reads it in its M_bar-geometry block.
- **Pass rule:** `cfg305_compare.py` must report MUTATE ≠ FIX for L323. If it does not, the substitution path is dead and the lane is void. The cfg216 result is reported either way.
- **Group C liveness:** paper_numbers' printed "corrected file sha256" in FIX of group C must equal the PUBLISHED CSV's sha256 prefix. That proves the substituted file was read.

## Hand estimates (arithmetic only, written before any run)
- **MNRAS inversion, row 87 alone.**
  - â₀ = (1 − f_DM) g / [ln(1/f_DM)]² goes from about 3.9e-11 to 4.4e-10, about +1.05 dex at z = 2.26.
  - With about 99 points and Σ(z − z̄)² ≈ 30, the slope moves by about +0.02 dex per unit z. From −0.11 ± 0.06 that is about 0.4σ, so the printed "−0.11" may become "−0.09".
- **ADF22.5 870 µm inclination row.**
  - The g_obs factor (sin 75°/sin i)² goes from 1.41 (54.5°) to 1.15 (64.2°), −0.088 dex in D.
  - S0 s* ≤ 13.7 should fall towards about 7–8, and G1 ≤ 18.8 towards about 10–11.
- **ADF22.5 gas radius 1.53 → 1.58 kpc.** The gas force at R_ext changes by about 1%, so G1/G2/S1 move by about 0.01 in D.

## What this lane cannot say
- It does not re-score any physics. It replaces transcribed inputs with the journal's and bounds how far that propagates.
- The journal's row-87 values are the authors' refit (the text and the arXiv v1 image differ). Neither version is "true". The journal table is the version of record.
- The FS+18 table is not re-checked here (the chat's membership test only).
