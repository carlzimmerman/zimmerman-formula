# CFG287: integrity audit of the published tables behind the a₀ lanes

> **κ = ½ FITTED.** a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. This audit scores neither.
>
> **Scope:** a data audit only. No lane is re-run and no lane number changes. Impact is bounded by arithmetic on committed files.
>
> **Request:** "make sure those scientists didn't mess up the data".
>
> **Criteria:** `FROZEN_CRITERIA.md`, written before any check, sha256 3cc1d8df…eea77 (printed at the head of every output).
>
> **Inputs:** on disk only. Page reads were used only for versions and errata (`versions_errata_pagereads.json`).
>
> **Script:** `cfg287_integrity.py`.
> - Its main run gives `cfg287_integrity.out` and `cfg287_results.json`.
> - `MUTATE=1` gives `cfg287_mutate.out` and `cfg287_mutate_results.json`.
> - Two cold runs gave byte-identical `.out` files.

## 1. Bottom line

1. **No problem found here can change a committed verdict (no CRITICAL).** Every lane-bearing error bounds to at most about 0.1σ to 0.25σ against its lane's margin:
   - CFG28's ultra-faint offset stays 3.67–3.77σ;
   - CFG52/CFG90's pooled z ≥ 1.5 mean moves by 0.03 dex against σ = 0.136;
   - every other defect sits in a cell no committed lane reads.
2. **The transcriptions the repo made itself are clean.**
   - 3,703 cells were sampled with seed 287 across 29 tables (TeX, HTML, PDF images, FITS, CDS): **0 mismatches.**
   - The full scans beyond the sample found only three bad cells: ALPAKA `lambda_rest_eff_A` for IDs 23–25. The build read a TeX comment ("%CO_1/3/2") as a number. No lane reads that column.
3. **The authors' published tables are internally consistent for almost every source.** Where a paper prints a formula, its columns satisfy it to the printed rounding. The exceptions are source-level defects:
   - one row in Tacconi+13;
   - one galaxy in SPARC;
   - two rows in RC100;
   - one catalogue row in the KMOS3D release;
   - stale size columns in the Local Volume Database.

   None of them is a transcription slip by the repo.
4. **One repo-side error has a long tail.** The original RC100 CSV still carries the 17 wrong cells found on 09-29 (seven rows with log M_bulge in place of log M_baryon). It is still read by the older lanes (CFG6/52/90 and the real_research L-series).
   - This audit traces CFG52/CFG90's "mutually inconsistent" outlier GS4 01529 to that error. The CSV's log M = 9.63 is the paper's log M_bulge; log M_baryon is 11.33. So the object is not a g_bar < a₀ galaxy at all (y 0.20 → 9.8).
5. **No erratum or corrigendum is registered for any of the 34 papers.**
   - Three lane-bearing tables come from **pre-referee arXiv copies** whose published versions could not be read: RC100, FS+18, and the Umehata+25 geometry. These are open (UNVERIFIED), not problems found.
   - The repo's Local Volume Database citation is wrong: `real_research/data/dsph/PROVENANCE.md` gives a DOI that does not exist.

## 2. Disclosed departures from the frozen criteria

1. **RC100: added after I re-read row 83 in the page image (post hoc).**
   - The checks "V_rot(R_e)² = V_c² − 3.36σ₀² > 0" (the paper's eq. 8 at R_e) and "V_rot/σ₀ ≥ 2.3".
   - The targeted re-read of row 83, which is not part of the seed sample.
2. **Redshift classes.** The §2 printed half-units of both redshifts are added to the §4 velocity thresholds as a rounding allowance. RC100 prints z to 0.01, which is 460–930 km/s.
3. **Post-hoc characterisations, marked "POST-HOC" in the output.** For SPARC, the LVD and the KMOS3D release, I characterised the rows the frozen rules flagged. The frozen counts are reported unchanged.
4. **Transcription full scan.** Beyond the frozen 10% sample, every mapped cell was also compared, and mismatches outside the sample are reported.
5. **Cross-survey tagging.** RC100 against Price+21 fitted quantities is tagged "different method": RC100 averages methods A, B and C, while Price is method B. So those differences are not treated as same-definition problems.
6. **MUTATE wording.** §8's "no check flags a row the unmutated copy does not flag" is applied as "no newly flagged row outside the planted rows".

## 3. Master table

**Severity:**
- **CRITICAL:** changes a committed verdict.
- **MAJOR:** could change one.
- **MINOR:** cannot.
- **NIT:** cosmetic, and no lane reads the cell.

"H" checks are hard formulas; "S" checks are soft plausibility tests.

| Source | Files | Checks run | Problems (severity) | Lanes touched |
|---|---|---|---|---|
| **S01 SPARC (Lelli+16)** | MRT + 175 rotmod | (1) SBeff = L/2πReff²; (2) rotmod distance = MRT D; (3) Rad, errV, Vobs sanity; (4) Vflat ⇔ e_Vflat; (5) generic; (6) the `SPARC_table.txt` trap; (S) L_disk/L; (S) Vflat vs outer Vobs | (a) **NGC4010:** SBeff 14.75 against the 62.2 implied by L and Reff, a factor 4.2 (MINOR). The frozen C = 0 rule flags 52 further rows, but the printed/recomputed median is 0.996 (16–84%: 0.986–1.001), a ≈0.4% definitional offset. Only 4 rows are off by >5%: NGC4010, UGC03205, UGC02953, UGCA444. (b) The data rows are 131 bytes wide, while the header's byte layout ends at 113. A CDS reader would misparse; every repo loader splits on whitespace (MINOR). (c) `SPARC_table.txt` is a 404 page, named only by `deepseek_push/L06_rar_moment.py` (NIT). Rotmod distances are 175/175 consistent | SBeff: CFG252's ρ_local fork (1 of 175 rows). None of the a₀ curves |
| **S02 Local Volume Database (Pace)** | MW / M31 / field CSVs | distance from μ; M_V = m − μ; rhalf_physical; rhalf_sph; mass_stellar; Wolf mass; generic | (a) **rhalf_sph_physical** is 2–12% below rhalf_physical·√(1−ε) in 22 rows (worst Andromeda XXVI 0.88, Andromeda XX 0.90, Phoenix III 0.92). These are stale derived columns. (b) rhalf_physical/(D·rhalf) has a median of 0.997. (c) 9 Wolf-mass rows follow from (a). (d) The repo's citation DOI is wrong (see §6). All MINOR. distance, M_V and M★ are clean (175/173/173) | CFG7/28/29/42/46/51/66/73/74/78/83/92/93. CFG28 bound: only 3 of its 31 ultra-faints are affected (≤ 0.018 dex in r), so the median offset shifts by ≤ 0.009 dex and the significance stays 3.67–3.77σ |
| **S03 KiDS-1000 lensing RAR (Brouwer+21)** | 20 profiles + 9 covariances | covariance symmetric and PSD (9/9); error = √diag C within 1e-3 (9/9; the printed groups are ≤ 4e-5); g_bar grid; bias column; ESD_x null p ≥ 0.001 in all 20 files (the six printed: 0.18–0.88) | **none** | — |
| **S04 RC100 (Nestor Shachar+23)** | original CSV + paper-values file | derived columns; changed_cells; (S) baryon coefficient; visual re-read; POST-HOC eq. 8 | (a) **The original CSV still differs from the paper in 17 cells** (16 rows). It is read by 33 committed .py files, including CFG6/52/90 and L320/322/323/331/332. Arithmetic: median V_c⁴/(G M_bar) +0.043 dex; largest row 1.70 dex (GS4 01529). For the CFG52/CFG90 pool, K20 ID9 leaves the g_bar < a₀ pool (y 0.45 → 1.5), so the pooled Df/Dr shifts by −0.030/−0.029 dex against σ = 0.136: **MINOR for CFG52/90**. For the L-series outputs: **MAJOR, not bounded here.** (b) **Rows 67 (zC 405501) and 83 (K20 ID5)** have V_c² < 3.36σ₀², so the paper's own eq. 8 gives V_rot² < 0 at R_e. Row 83 is confirmed on the page image (σ₀ = 100, V_c = 174, log M_bulge 11.17). 14 more rows have V_rot(R_e)/σ₀ < 2.3. MINOR: 2 of 100 rows enter median statistics. (c) **Row 80 "U3 10584"** (see S05). (d) Prints z = 0.61 for U4 38210 (KMOS3D 0.6022) and 2.02 for zC 412369 (FS+18 2.0281): last-digit TENSION (NIT) | (a) older a₀(z) lanes; (b) CFG216/217/218/222/223/227/233/237 |
| **S05 KMOS3D release (Wisnioski+19)** | catalogue CSV (+ FITS) | Z vs HAFIT_Z; Q, errors, sentinels; FILE; machine read (2,628 cells, 0 fail) | (a) **U3_10584's catalogue row is self-inconsistent.** Its position lies outside its own cube (the cube pipeline's README says so), it has no 3D-HST counterpart (ID_SKELTON 99999), and LMSTAR = 8.99. RC100's "U3 10584" has log M★ 10.5 and z 2.22 against 2.2455, a 2,370 km/s DISAGREE. Identity UNRESOLVED (MINOR). In CFG270 this row is tier T0, with D = 70 and s* = 156, an outlier in the all-fits sensitivity row PT0 only. (b) 46 secondary targets (FLAG_PRIMARYTARG = 0) have cubes named after another galaxy; 15 are fitted in CFG270, all lowSN, so not in T1/T2 (MINOR). (c) RHALFERR = −999 sentinel in 3 rows (NIT) | CFG270 (PT0 only); RC100 lanes (identity only) |
| **S06 RC41 (Price+21)** | CSV (+ HTML) | interval half-widths, f_DM, R_e; (S) M_bar vs prior | **none**. 3 fits sit 0.5 dex below their prior centre (S); transcription 103/103 | — |
| **S07 SINS/zC-SINF AO (FS+18)** | Tables 1, 5, 6 (+ HTML) | eq. 1 (V_c), eq. 2 (M_dyn), V_rot/σ₀, sSFR, generic; (S) C_PSF; (S) r½,circ | **none**: eq. 1, eq. 2 and the ratio are all CONSISTENT (38/38). BX482's parenthetical H-band magnitude is left blank in K_AB (NIT) | — (CFG229/270/280 clean) |
| **S08 SINS (FS+09)** | CSV (+ CDS) | generic; machine read (99 cells, 0 fail); (S) M_dyn coefficient | **none** (the coefficient scatter is method-dependent, S) | — |
| **S09 PHIBSS (Tacconi+13)** | joined CSV (+ CDS) | M_bar sum; M_mol = 8.72 L′; f_gas; L′ from flux; machine read (87, 0 fail) | (a) **Q2343-MD59:** the published L′CO = 6.2e10 is inconsistent with its own flux (1.04e10) and M_mol (9.5e10 ⇒ 1.09e10). This is a typo in the journal table (MINOR: every lane uses M_mol). (b) 11 further M_mol rows are the CO(2–1)/lensed rows (BzK, PEP, J2135), whose conversion differs (definition). (c) 4 PEP rows have f_gas ≠ M_mol/M_bar (the build had flagged 3) (MINOR) | none (lanes read `mmol_msun`) |
| **S10 ALMA-CRISTAL (Lee+25)** | 3 tables (+ TeX) | generic; (S) lower errors; (S) baryon coefficient (median 0.52, tight) | **none**. σ₀ errors of 03 and 15 are very asymmetric (as printed) | — |
| **S11 ALPINE (Jones+21) + corpus copy** | Table 1, rings, corpus | M_dyn = V²R/G (18/18); corpus = Jones copy (18/18); corpus means | **none**. KC1 = class_L20 is the table's own header (KC1 is the L20 class). The corpus HZ9 M★ = 10.3 has no source (already disclosed in CFG271) | — |
| **S12 σ–M★ compilation (Parlanti rows)** | `highz_sigma_mstar.csv` | σ_eff construction (62/62) | (a) **The z of HZ4, HZ7 and HZ9 is 0.010–0.012 below the [CII] redshifts** of Jones+21 and CRISTAL (480–560 km/s, TENSION). Parlanti's TeX is not on disk: UNVERIFIED which value is Parlanti's (MINOR: E(z) changes by 0.3%; CFG271 uses z = 5.54). (b) The rows cannot be transcription-checked (UNVERIFIED) | CFG271 (z only), L328 |
| **S13 ALPAKA I (Rizzo+23)** | 5 tables, digitised curves, arXiv:2601.03338 | L′ (Planck18, 28/28); V_ext ≤ V_max; V/σ columns; digitised V_ext / V_max / scale (19/19 each); transcription 10% + full | (a) `lambda_rest_eff_A` = 1/3/2 for IDs 23–25: the build read the TeX comment "%CO_1/3/2" as a number. The notes text carries the same "\\%" artefacts (MINOR: no lane reads the column). The lane-used columns are clean. The compile used `alpaka_v2.tex` (from its `.fls`), as the build did | none |
| **S14 Amvrosiadis+25 (v1)** | parent + best-fit (+ TeX) | V_circ²−3.36σ² ≤ V_max² (12/12 within rounding); (S) M_dyn(10 kpc) vs V_circ (2 cases, ≤3%); (S) baryons vs dynamics | (a) The published table's (M★ + M_gas) exceeds M_dyn(10 kpc) for 4 of 12, up to 6.1× (071.1). This is source-level and already recorded by CFG227/274 (not new). (b) The source typo θ = 120_{5}^{−5} for 049.1 drops one CSV error bar (NIT) | CFG274 (already reflected) |
| **S15 Danhaive+25 (v1)** | gold table (+ TeX) | log M_dyn = log[1.8 r_e(v² + 3.36σ₀²)/G]: 23 CONSISTENT, 1 ROUNDING-EDGE of 24; transcription 75/75 | **none** (the published 37-gold version is known, CFG266) | — |
| **S16 Roman-Oliveira+23** | 3 tables (+ TeX); RO M★ look-up | V/σ ratios; V_ext ≤ V_max; kpc/″ (Planck18) | **none** | — |
| **S17 Lelli+23** | mass models, 3DBarolo, digitised | M_bar sum (6/6); M_bul/M_bar; digitised CO vs ⟨V_rot⟩ (≤0.3 km/s) | Dropped cell: zC-400569 (baryons only) M_disk +err is empty. The TeX prints "^{2.3}" without '+' (MINOR: no lane reads this CSV) | none |
| **S18 MUSE-DARK** | numeric set + II Table 3 | log sum; R_e conversion; kpc/″ (Planck15, exact); has_bulge; transcription of II Table 3 | ID 1035 has an inclination of 90.2° (NIT) | — |
| **S19 ADF22.5 literature values** | CSV | log M★ conversion; positions (0.04–0.06″); z | **none**. **Verified on disk** against the ADF22-WEB PDF Table 1: log M★ 10.64 (+0.20/−0.36), SFR 146, z 3.09536, and R_e,★ (circularized) 1.65 ± 0.21 kpc = 2.24 × √0.54. **Still unverified:** n = 3.21, and the 870 µm R_e 1.53 / q 0.58 (the 2026 table gives a circularized 1.05 ± 0.12; 1.53·√0.58 = 1.17, within 1σ) | CFG284/285 |
| **S20 PKS 0529 (Lin+24, digitised)** | rings CSV | kpc/″ constant (5e-4); V_c ≥ V_rot; radii | **none** | — |
| **S21 GN20 constants (CFG276)** | in-script | 13 constants in the TeX and the script; v_c = √(v_rot² + 3.36σ₀²) | **none** | — |
| **S22 MIGHTEE** | CFG279 constants; Jarvis+25 | 7/7 constants in the TeX; W50c = W50/sin i (11/11); transcription | **none** (11b's ditto cells: W50 left blank, the others copied; NIT) | — |
| *cited, not redone* | — | — | Heintz & Watson 2020 α_[CI] row shift; Danhaive 41→37; Amvrosiadis v1 α_CO; FS+18 V_c radius; MIGHTEE a₁ sign; KDS vs AMAZE; CFG267 F1–F5 | as recorded |

## 4. Problems ranked by severity

**CRITICAL:** none.

**MAJOR (one, unbounded rather than shown):**
1. **The uncorrected RC100 CSV in older outputs.**
   - `real_research/data/rc100_nestorshachar2023_table3.csv` keeps 17 wrong cells. 33 committed scripts name it.
   - Bounded here, all MINOR:
     - the population median of the V_c⁴/(G M_bar) proxy moves +0.043 dex;
     - CFG52/CFG90's pool moves by 0.03 dex (0.22σ);
     - CFG90's "GS4 01529 is mutually inconsistent" is this transcription error, not the galaxy.
   - **Not bounded:** the older real_research L-series outputs (L320/L322/L323/L331/L332, `rc100_deepMOND_framework_fit.py`, `a0z_clean_ledger.py`, a theory-figures script). Some count deep-MOND or outlier rows that rows 43, 44 and 65 can flip.
   - The current STANDING does not cite them. Re-running them on the paper values, or retiring them, closes this.

**MINOR (cannot move a verdict):**
1. RC100 rows 67 and 83 violate the paper's own eq. 8 at R_e.
2. RC100 row 80 / KMOS3D U3_10584: identity unresolved; the KMOS3D catalogue row is self-inconsistent.
3. LVD stale rhalf_sph_physical in 22 rows. CFG28 worst case: 3.77σ → 3.67σ.
4. Tacconi+13 Q2343-MD59 L′ typo. Lanes use M_mol, which is consistent.
5. The S12 compilation's HZ4/HZ7/HZ9 redshifts sit about 500 km/s below [CII].
6. SPARC NGC4010 SBeff inconsistent (×4.2); the MRT layout does not match its header.
7. ALPAKA `lambda_rest_eff_A` artefacts and notes text (an unread column).
8. Lelli+23 dropped error bar (an unread file).
9. CFG270 PT0 holds 15 lowSN secondary-target fits plus the U3_10584 outlier. T1/T2 are untouched.
10. The LVD citation in PROVENANCE.md.

**NIT:** the `SPARC_table.txt` reader in deepseek_push; the KMOS3D −999 sentinel; MUSE-DARK inclination 90.2°; the FS+18 BX482 K_AB blank; Amvrosiadis 049.1 θ; Jarvis 11b dittos; RC100 last-digit z misprints.

## 5. Clean within their printed rounding

Clean means every hard check is CONSISTENT or ROUNDING-EDGE and the transcription sample matched.

**Clean as audited:**
- KiDS-1000 lensing RAR (Brouwer+21);
- FS+18 Tables 1/5/6;
- FS+09 (CDS);
- Price+21 RC41;
- ALMA-CRISTAL (all three tables);
- Jones+21 and the corpus copy;
- ALPAKA I, every column a lane reads (L′, kinematics, geometry, digitised curves);
- arXiv:2601.03338;
- Amvrosiadis v1 tables as printed (the baryon–dynamics excess is the authors', already in the record);
- Danhaive v1 gold;
- Roman-Oliveira+23 and the RO M★ look-up;
- Lelli+23 (apart from one dropped error bar);
- MUSE-DARK I numeric set and II Table 3;
- PKS 0529 digitised rings;
- GN20 constants;
- MIGHTEE (Vărăşteanu+26 constants, Jarvis+25);
- ADF22.5 on-disk-verified values.

**Not clean** (see §3):
- SPARC (one galaxy, layout);
- the LVD derived size columns;
- RC100 (two eq.-8 rows; the uncorrected repo CSV);
- the KMOS3D release (one catalogue row);
- Tacconi+13 (one L′ cell).

## 6. Versions and errata (`versions_errata_pagereads.json`)

- **Errata.** Crossref `updates:` returned no notice for any listed DOI; a positive control returned 3. No A&A "<DOI>e" corrigendum and no MNRAS "Correction to:" title exists for these papers.
- **Pre-referee copies used, published table not readable by page read (UNVERIFIED):**
  - RC100 (arXiv v1, "Submitted to ApJ"; ApJ 944, 78). The iopscience page did not expose Table 3.
  - FS+18 (v1, "Submitted to ApJS"; ApJS 238, 21).
  - Umehata+25 (v1; ApJ 997, 79), which supplies CFG284's geometry.

  If any published table differs, CFG216/233 (RC100) are the lanes with leverage. Their standing is already "gas-route-limited". CFG280 and CFG196 are coverage-only or non-diagnostic.
- **Already known:** Danhaive (41 → 37) and Amvrosiadis (α_CO, 065.1).
- **Machine-read sources are the journal or release products:** Tacconi+13 and FS+09 (CDS), and the KMOS3D release (FITS v3).
- **ALPAKA:** the tarball holds three drafts. The compile read `alpaka_v2.tex`, which the build used. `aanda2.tex` is identical to it for the geometry and kinematics tables.
- **LVD citation:** `real_research/data/dsph/PROVENANCE.md` says "Pace 2024, ApJS 273, 15, doi:10.3847/1538-4365/ad9f2c". That DOI is not registered, and ApJS 273, 15 is a different paper. The LVD is Pace 2025, The Open Journal of Astrophysics 8, doi:10.33232/001c.144859 (arXiv:2411.07424 v2). The data used are the GitHub CSVs, so no number changes.

## 7. Transcription (seed 287, frozen order)

- **Sample:** 3,703 cells in 29 tables, 0 failures:
  - RC100: 77 cells read from the page images (seed rows 1, 5, 7, 56, 59, 68, 70, 79, 80, 85), plus row 83;
  - Price+21: 103;
  - FS+18: 254;
  - CRISTAL: 76;
  - Jones+21: 49;
  - ALPAKA plus arXiv:2601.03338: 138;
  - Amvrosiadis: 56;
  - Danhaive: 75;
  - Roman-Oliveira: 18;
  - Lelli+23: 11;
  - MUSE-DARK II: 5;
  - Jarvis+25: 27;
  - KMOS3D FITS: 2,628;
  - FS+09 CDS: 99;
  - Tacconi+13 CDS: 87.
- **Full scans (all mapped cells, beyond the sample):** 3 mismatches, all `lambda_rest_eff_A` for ALPAKA IDs 23–25. 3 dropped cells:
  - Lelli+23 M_disk +err;
  - Amvrosiadis 049.1 θ +err;
  - FS+18 BX482 K_AB.
- **Fragments:** all 23 `raw_small` TeX fragments are verbatim in the original tarball TeX.
- **Errors found in the parsers:** my own parser started with five faults, all fixed before the final run:
  - a TeX `\\%` row-comment;
  - `\substack` spacing;
  - per-cell ×10ⁿ scales;
  - sidewaystable;
  - continued tables.

  Every apparent mismatch was traced to my parser or to a source typo, never to a repo cell, except the three ALPAKA cells above.

## 8. MUTATE (`cfg287_mutate.out`): PASS

The copy is FS+18 Table 6, written as `CFG287_MUTATE_sins_ao_table6.csv`.

| Plant | What was changed | Caught by |
|---|---|---|
| **M1, shifted row** | V_c of rows 10–14 moved down one row | eq. 1 flags exactly those 5 rows (Deep3a-6397, Deep3a-15504, K20-ID6, K20-ID7, GMASS-2303) |
| **M2, unit slip** | ZC400569N M_dyn × 10 | eq. 2 (460 against 45.7) |
| **M3, sign flip** | ZC405501 V_rot negated | the positivity check and V_rot/σ₀ (printed 1.9 against −1.94) |

- No row outside the planted ones is newly flagged.
- The full transcription comparison flags exactly the 7 planted cells.
- The cross-survey view (RC100 V_c(R_e) against FS+18 V_c) is a different definition, so it is reported only.

## 9. What this audit cannot say

- It cannot confirm that the published RC100, FS+18 and Umehata+25 tables equal the arXiv copies used.
- It cannot verify Parlanti+23's rows: the TeX is not on disk.
- It cannot check the digitised curves cell by cell. They were checked only against the same paper's tabulated numbers.
- It does not re-run any lane. The MAJOR item above is an exposure, not a demonstrated change.
- A table that is consistent and correctly transcribed can still be wrong physically, for example through its gas recipe, pressure term or radius (CFG267). That is a methods question, outside this audit.

## Files

- `FROZEN_CRITERIA.md`: written first.
- `cfg287_integrity.py`, `cfg287_integrity.out`, `cfg287_results.json`.
- `cfg287_mutate.out`, `cfg287_mutate_results.json`, `CFG287_MUTATE_sins_ao_table6.csv`.
- `rc100_visual_reread.csv`.
- `versions_errata_pagereads.json`.
- `AUDIT.md`.
