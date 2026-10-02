# CFG287 — integrity audit of the published tables behind the a₀ lanes: FROZEN CRITERIA

> Written 2026-10-02 before any check in this lane was computed. The repository was at commit 0383bbfc2 when this file was written. The owner's request: "make sure those scientists didn't mess up the data".
>
> **Scope:** a data audit, not physics. No lane is re-run and no lane number changes. Impact is bounded by arithmetic only (§7).
>
> **κ = ½ FITTED.** a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. Neither is scored here.
>
> **Writes:** only inside `campaign_fresh_gravity/CFG287_source_table_integrity/`. Nothing is committed or pushed. No downloads. Inputs are files on disk only:
> - the repo's `data_assembly/` and lane inputs;
> - the local arXiv TeX in `../_external_data/arxiv_src`;
> - the saved HTML pages in `data_assembly/*/raw_small`;
> - the on-disk PDFs and text layers in `../_external_data/papers` and `../_external_data/arxiv_pdf`.
>
> **Web:** page reads only, to check a version or an erratum (§5).
>
> **Not redone, cited instead:**
> - Heintz & Watson 2020: the α_[CI] row shift (`data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`).
> - Danhaive+25: arXiv v1 has 41 gold galaxies against a reported 37 in the published version (CFG266/273).
> - Amvrosiadis+: arXiv v1, α_CO 0.92 against a reported 0.74 (CFG267 F3).
> - FS+18: V_c has no radius (CFG267).
> - MIGHTEE: the a₁ sign flip with the M/L choice (CFG279).
> - KDS vs AMAZE (CFG268).
> - The CFG267 methods findings F1–F5.

## 1. Sources audited (the files the committed lanes read)

| ID | Source (paper) | Files audited | Lanes that read them |
|---|---|---|---|
| S01 | SPARC, Lelli+16 (z = 0 anchor) | `real_research/data/SPARC_Lelli2016c.mrt`, `real_research/data/sparc_data/*_rotmod.dat` (175). `SPARC_table.txt` is tested only to confirm it is a 404 page and to list any script that reads it | the SPARC-anchored lanes (CFG2/4/5 common loaders, CFG140, …) |
| S02 | Local Volume Database, Pace (dwarfs) | `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` | CFG7, 18, 28, 29, 31, 42, 46, 51, 66, 73, 74, 78, 83, 92, 93 |
| S03 | KiDS-1000 lensing RAR, Brouwer+21 | `real_research/data/lensing_rar/brouwer2021_rar/*.txt` | CFG15, 21, 61, 88, 95, 107, 108, 110, 115, 116, 255, 261 |
| S04 | RC100, Nestor Shachar+23 | `real_research/data/rc100_nestorshachar2023_table3.csv` (original), `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv` (paper values) | CFG216/217/218/222/223/227/233/237 (paper values); CFG6/52/90 and real_research L320/L322/L323/L331/L332 (original file) |
| S05 | KMOS3D release, Wisnioski+19 | `data_assembly/kmos3d_phibss/kmos3d_catalog.csv` (+ the FITS in `raw_small`) | CFG229, CFG270 |
| S06 | RC41, Price+21 | `data_assembly/price2021_rc41/price2021_rc41.csv` (+ HTML) | CFG210, 215, 217, 233 |
| S07 | SINS/zC-SINF AO, Förster Schreiber+18 | `data_assembly/highz_literature_tables/sins_ao/sins_ao_table{1,5,6}_*.csv` (+ HTML) | CFG229, 270, 280 |
| S08 | SINS, Förster Schreiber+09 | `data_assembly/high_z_tf_tables/sins2009_dynamics.csv` (+ CDS .dat) | CFG196 |
| S09 | PHIBSS, Tacconi+13 | `data_assembly/kmos3d_phibss/phibss13_joined.csv` (+ CDS .dat) | CFG196, 233, 280 |
| S10 | ALMA-CRISTAL, Lee+25 | `data_assembly/arxiv_tables/cristal2025_{sample,kinematics,dynamics}.csv` (+ TeX) | CFG213, 215, 219–223, 229, 234 |
| S11 | ALPINE, Jones+21 (+ the corpus copy) | `data_assembly/highz_literature_tables/jones2021_alpine/*.csv` (+ HTML), `alpine_corpus_z1/corpus_z1_{galaxies,rings}.csv` | CFG228, 271, 277 |
| S12 | HZ9 et al., Parlanti+23 (via the σ–M★ compilation) | `real_research/virial_floor_2026/highz_sigma_mstar.csv` | CFG271 |
| S13 | ALPAKA I, Rizzo+23 (+ the digitised curves) | `data_assembly/arxiv_tables/alpaka1_*.csv` (+ TeX), `alpaka1_digitised/*.csv`, `alpaka_jwst2026_*.csv` | CFG229, 272, 283, 284, 285 |
| S14 | Amvrosiadis+25 | `data_assembly/arxiv_tables/amvrosiadis_{parent,bestfit}.csv` (+ TeX) | CFG227, 229, 274 |
| S15 | Danhaive+25 | `data_assembly/arxiv_tables/danhaive2025_gold.csv` (+ TeX) | CFG273 |
| S16 | Roman-Oliveira+23 (+ the RO stellar-mass look-up) | `data_assembly/arxiv_tables/romanoliveira2023_*.csv` (+ TeX), `data_assembly/ro23_stellar_masses_2026-10-01/ro23_stellar_masses.csv` | CFG277, 282 |
| S17 | Lelli+23 (+ the digitised curve) | `data_assembly/arxiv_tables/lelli2023_*.csv` (+ TeX), `data_assembly/lelli2023_rotcur_digitised/lelli2023_rotcur_digitised.csv` | CFG278 |
| S18 | MUSE-DARK I numeric set (+ MUSE-DARK II/III tables) | `data_assembly/musedark_catalogues/musedark_numeric.csv`, `data_assembly/arxiv_tables/musedark_II_III/*.csv` | CFG190, 198, 199, 215, 236, 262 |
| S19 | ADF22.5: Umehata+25 / Huang+25 / ADF22-WEB 2026 | `data_assembly/adf22_5_literature_2026-10-02/adf22_5_literature_values.csv` | CFG284, 285 |
| S20 | PKS 0529-549, Lin+24 (digitised) | `campaign_fresh_gravity/CFG275_pks0529_ci_rings/lin2024_rings_digitised.csv`, `data_assembly/multitracer_gas/singles_multitracer_galaxies.csv` | CFG275 |
| S21 | GN20, Übler+24 / Boogaard+25 | the constants hard-coded in `CFG276_gn20/cfg276_gn20.py` (+ TeX) | CFG276 |
| S22 | MIGHTEE: Vărăşteanu+26 (published a₀ table) and Jarvis+25 | the constants in `CFG279_mightee_published_values/cfg279_mightee_published.py` (+ TeX); `data_assembly/mightee_hi_highz/mightee_hi_highz.csv` (+ HTML) | CFG279 (CFG258 used mocks only) |

## 2. Printed precision and the rounding envelope

1. **Printed half-unit h(x).** For a value printed with d decimals, h = 0.5 × 10⁻ᵈ.
   - The precision is taken from the source print when the check reads the source. Otherwise it comes from the CSV text.
   - In CSV text, a trailing ".0" counts as an integer print (h = 0.5). This is conservative: it widens the envelope.
   - For mantissa prints (a × 10ⁿ, or a CSV number carrying only trailing zeros), h = 0.5 in the last significant digit.
2. **Envelope E** for a quantity recomputed from printed inputs, compared with a printed value f_p:
   - E = Σᵢ |∂f/∂xᵢ| h(xᵢ) + h(f_p);
   - linear worst case, with the partial derivatives taken by finite differences.
3. **Convention allowance C** (relative), declared per check:
   - 0 for pure arithmetic (sums, ratios, logs, copies);
   - 1% where G, kpc or M☉ constants enter;
   - 2% where a cosmology enters and the paper's exact parameters are not used;
   - 0.5% where the paper's own cosmology is used.
4. **Per-row class:**
   - **CONSISTENT:** |Δ| ≤ E + C|f|.
   - **ROUNDING-EDGE:** E + C|f| < |Δ| ≤ 2(E + C|f|). This counts as a rounding difference, not a problem, and is reported.
   - **PROBLEM:** |Δ| > 2(E + C|f|).
5. **Rows with an upper or lower limit** are kept out of the equality tests. The direction of the limit is checked where it can be (for example, a ratio carrying a limit must point the same way as its input).
6. **A table is "clean within its rounding"** when every hard check (H) gives CONSISTENT or ROUNDING-EDGE, and every transcription cell sampled under §6 matches.
   - Soft checks (S) are plausibility or outlier tests with no exact formula. An S outlier is a FLAG, not a PROBLEM, unless the source itself confirms it.

## 3. Check 1: internal consistency (H = hard formula, S = soft plausibility)

**Generic checks, applied to every table:**
- (H) error bars must be ≥ 0;
- (H) quantities that are positive by definition (masses, radii, velocities, dispersions, distances) must be > 0;
- (H) log and linear copies must agree;
- (S) value − lower error < 0 for a positive-definite quantity;
- (S) an asymmetric pair whose two sides differ by more than 10×;
- (H) fractions must lie in [0, 1]; inclinations in [0°, 90°]; ellipticities in [0, 1).

**Source-specific checks:**
- **S01 SPARC.**
  - (H) SBeff = L[3.6]·10⁹ / (2π (10³ Reff)²) L☉/pc², with C = 0.
  - (S) L_disk = 2π SBdisk Rdisk² against L[3.6]. FLAG if L_disk/L > 1.5 or < 0.2.
  - (H) each rotmod header distance equals the MRT D.
  - (H) in each rotmod: Rad strictly increasing, errV > 0, Vobs ≥ 0.
  - (H) Vflat = 0 if and only if e_Vflat = 0.
  - (S) Vflat against the median of the last three Vobs. FLAG if |Δ| > 3 e_Vflat + 0.05 Vflat.
  - (H) 175 MRT rows, 175 rotmod files, names one-to-one.
  - (H) `SPARC_table.txt` is an HTML 404 page; list every committed `.py` that opens it.
- **S02 LVD.** For each formula below, the candidate constants or forms are tested. The one matching ≥ 90% of rows is adopted, and rows off that formula beyond the envelope (C = 0.1%) are reported.
  - (H) distance = 10^(μ/5 + 1) pc;
  - (H) M_V = m_V − μ;
  - (H) rhalf_physical = distance × rhalf(arcmin) in radians;
  - (H) rhalf_sph_physical = rhalf_physical × √(1 − ε);
  - (H) mass_stellar = log₁₀(2 L_V), with M_V,☉ chosen from {4.80, 4.81, 4.83};
  - (H) mass_dynamical_wolf = 930 σ² r, with r ∈ {rhalf_physical, rhalf_sph_physical}.
- **S03 KiDS.**
  - (H) the error column against √diag of the covariance (relative 1e-3), with or without the (1+K) bias factor; the matching form is reported.
  - (H) the covariance is symmetric and positive semi-definite.
  - (H) the g_bar grid is identical across bins and uniform in log (relative 1e-3).
  - (S) the bias (1+K) column is constant within each file and lies in (0.8, 1.2).
  - (S) the cross-shear ESD_x null χ²/dof per file, using the diagonal errors. FLAG if p < 0.001.
- **S04 RC100.**
  - (H) the original CSV's derived columns, recomputed with relative tolerance 1e-3: g_Re = V_c²/R_e; Vc⁴/(G M_bar); its ratio to 1.2e-10; the deep-MOND flag.
  - (H) the paper-values file: the `changed_cells` column against the actual differences from the original CSV.
  - (S) the implied baryon coefficient k = (1 − f_DM) V_c² R_e / (G M_bar). FLAG if |log k − median| > 0.5 dex.
- **S05 KMOS3D.**
  - (S) |Z − HAFIT_Z| ≤ 0.002 where both are present.
  - (H) 0 < Q ≤ 1, RHALF > 0, RHALFERR ≥ 0, HAFIT_SIG_ERR ≥ 0.
  - (H) FILE begins with the ID.
- **S06 Price+21.**
  - (H) the shortest-68% interval half-widths are ≥ 0.
  - (H) f_DM ∈ [0, 1].
  - (S) log M_bar against log(M★ + M_gas). FLAG if |Δ| > 0.5 dex.
- **S07 FS+18.**
  - (H) Vc = √(Vrot² + 3.36 σ₀²) (eq. 1), C = 0.
  - (H) M_dyn = 2 R_e Vc²/G (eq. 2), C = 1%.
  - (H) Vrot/σ₀ = Vrot/σ₀, C = 0.
  - (H) sSFR = SFR/M★ in Gyr⁻¹, C = 0.
  - (S) C_PSF = Vrot sin i / (Δv_obs/2) ∈ [1, 2].
  - (S) r½,circ against R_e√q (Table 5). The paper says +10% ± 15%; FLAG if |ratio − 1.10| > 0.45.
- **S08 FS+09.**
  - (S) the coefficient k = M_dyn G / (V² r½), set by the majority. FLAG rows whose k lies more than 0.1 dex from the median.
- **S09 Tacconi+13.**
  - (H) M_bar = M_mol + M★ (C = 0) where it is not an upper limit.
  - (H) M_mol = 4.36 × 2 × L′ (L′CO(3–2) → (1–0) with r₃₁ = 0.5; C = 0).
  - (H) f_gas = M_mol/M_bar.
  - (H) L′ from S_CO, z and ν_obs (Solomon+97; flat H₀ = 70, Ω_m = 0.3; C = 2%).
- **S10 CRISTAL.**
  - (H) f_molgas and f_DM ∈ [0, 1].
  - (S) the implied baryon coefficient k = (1 − f_DM)(V_rot² + 3.36σ₀²) R_e / (G M_tot). FLAG if |log k − median| > 0.5 dex.
- **S11 Jones+21 and the corpus.**
  - (H) per ring, M_dyn = V_rot² R / G (C = 1%).
  - (H) the corpus columns: v/σ = V/σ per ring and per galaxy; log M_dyn = log₁₀(M_dyn,max); V_mean and σ_mean as means of the rings.
  - (H) the corpus rings are identical to the Jones rings, cell by cell.
- **S12 σ–M★ compilation.**
  - (H) σ_eff = √(σ₀² + V²/3) as written in each row's construction string.
- **S13 ALPAKA.**
  - (H) L′ = 3.25e7 S ΔV ν_obs⁻² D_L² (1+z)⁻³ with ν_obs = ν_rest/(1+z), Planck18, C = 0.5%. The line comes from the ALMA-observation table.
  - (H) V_ext ≤ V_max.
  - (H) V/σ columns against V/σ.
  - (H) digitised V_ext against the mean of the last two digitised V points, and V_max against the maximum digitised V. Tolerance: rounding + 3% digitisation allowance.
  - (H) the digitised kpc/arcsec against Planck18 at z, C = 2%.
- **S14 Amvrosiadis.**
  - (H) Vcirc(2r_e)² − 3.36σ² ≤ V_max², because their arctan V_rot(r) ≤ V_max. The test takes rounding plus 1σ on V_max.
  - (S) M_dyn(10 kpc) G/(10 kpc) against Vcirc(2r_e)², for discs with 2r_e within 20% of 10 kpc (Planck15, 67.8/0.308).
  - (S) (M★ + M_gas) against M_dyn(10 kpc): report the count with baryons > dynamics.
- **S15 Danhaive.**
  - (H) log M_dyn = log₁₀[1.8 r_e (v² + 3.36σ₀²)/G] with v = (v/σ₀)·σ₀, C = 1%. Limit rows are reported separately.
- **S16 Roman-Oliveira.**
  - (H) V_max/σ_mean and V_ext/σ_ext.
  - (H) V_ext ≤ V_max.
  - (H) kpc/arcsec against Planck18 (their 67.7/0.31), C = 0.5%.
- **S17 Lelli+23.**
  - (H) M_bar = M_gas + M_disk + M_bul.
  - (H) M_bul/M_bar.
  - (S) the tabulated mean V_rot against the mean of the digitised CO points (3% + rounding).
- **S18 MUSE-DARK.**
  - (H) log_X + log M_vir against the stored sum.
  - (H) R_e(kpc) from the table against R_e(″) × kpc/″.
  - (S) the catalogue R_e against the table R_e.
  - (H) kpc/″ against a cosmology at z (majority among Planck15, Planck18 and flat 70/0.3; C = 0.5%).
  - (H) has_bulge if and only if log M_bulge is finite.
- **S19 ADF22.5.**
  - (H) the log M★ conversion of the linear value and its errors.
  - (H) positions within 1″ between the ALPAKA table and the 2025 papers.
  - (H) z agreement.
- **S20 PKS 0529.**
  - (H) R_kpc/R_arcsec constant across rings (relative 1e-3).
  - (S) V_c ≥ V_rot ring by ring.
  - (H) errors ≥ 0 and radii increasing.
- **S21 / S22.** Covered by transcription (§6) and the generic checks.
  - (H) Jarvis+25: W50c = W50/sin i (C = 8%, the build's own statement re-tested).

## 4. Check 2: cross-survey overlaps

- **Matching.**
  - Matches are made by normalised name, with an alias table frozen in the script (for example "DEIMOS_COSMOS_494057" = "DC494057" = "HZ4", "Q2343-BX610" = "BX610", "zC-400569" = "ZC400569" = "zC 400569", "J081740" = "J0817").
  - Where both tables give coordinates, a positional match within 1.0″ is required. A name match that fails the 1″ test is itself reported.
- **Pull.** pull = Δ/√(σ₁² + σ₂²), with σ the symmetrised quoted errors.
  - If only one side quotes an error, that error is used.
  - If neither does, only the relative difference is reported and there is no pull.
- **Classes:**
  - AGREE: |pull| ≤ 2;
  - TENSION: 2 < |pull| ≤ 3;
  - DISAGREE: |pull| > 3.
- **Redshift** is classed by velocity, Δv = c|Δz|/(1+z):
  - AGREE ≤ 300 km/s;
  - TENSION 300–1000 km/s;
  - DISAGREE > 1000 km/s.
- **A cross-survey difference is a PROBLEM only when:**
  - (i) the same quantity at the same definition (same radius, same tracer, same method) is a DISAGREE; or
  - (ii) the two tables are copies of one source and differ beyond rounding.
  - Differences between definitions (different radius, tracer or method) are reported as DEFINITION differences, with their size, and are not problems.
- **Pairs examined (at least these):**
  - RC100 ∩ Price+21 (RC41 ⊂ RC100) in z, log M_bar, R_e, σ₀, f_DM;
  - RC100 / Price ∩ KMOS3D in z and M★;
  - RC100 / KMOS3D / Price ∩ FS+18 ∩ FS+09 ∩ Tacconi+13 ∩ Lelli+23 in z, V_c, σ₀, R_e, M★;
  - ALPAKA ∩ ADF22 literature (ALPAKA 24) and ALPAKA ∩ arXiv:2601.03338 (IDs 1, 3, 13) and ALPAKA ID 14 ∩ FS+18/FS+09/Tacconi+13 (BX610);
  - CRISTAL ∩ ALPINE (Jones Table 1 and the corpus) in z and M★;
  - HZ9 / HZ4 / HZ7 between Jones, CRISTAL and the σ–M★ compilation;
  - J0817 between Jones' rings, Roman-Oliveira and the corpus;
  - Danhaive ∩ the σ–M★ compilation;
  - SPARC ∩ LVD by name.
- KDS ∩ AMAZE is cited from CFG268 and not redone.

## 5. Check 3: versions and errata

For every paper behind S01–S22, the following is recorded by page reads only (arXiv abstract page or export API; Crossref `filter=updates:<DOI>`):
- the latest arXiv version and its dates;
- the journal reference and DOI;
- any registered erratum or corrigendum.

The version the repo used is set by the on-disk source file and its date:
- the tarball fetch date against the version dates;
- for ALPAKA, the TeX file the arXiv compile used (its `.fls`), with differences against the other drafts in the tarball counted.

Status codes:
- **SAME:** the version used is the latest, and no erratum is registered.
- **NEWER-VERSION:** a later arXiv version exists than the one read.
- **PUBLISHED-DIFFERS:** a difference is documented in the record.
- **ERRATUM:** a notice is registered; its content is read where it is open access.
- **UNVERIFIED:** not confirmable by page reads.

## 6. Check 4: transcription (tables the repo transcribed from TeX, HTML or PDF)

1. **Seed:** numpy `default_rng(287)`.
   - Tables are processed in the frozen order S04, S06, S07, S10, S11, S13, S14, S15, S16, S17, S18 (II/III), S22 (Jarvis).
   - For each table, n = max(5, ⌈0.10 N⌉) of the N mapped numeric cells is drawn without replacement (all cells if N < 5).
2. **Independence:** source rows are extracted by this lane's own parser from the ORIGINAL source, not from the build's copies:
   - TeX from the tarball, choosing the file the compile used;
   - HTML from the saved page.
   The build's `raw_small` TeX fragments are checked to be verbatim substrings of the original TeX (whitespace-normalised).
3. **Column mapping.** Each CSV column maps to (source cell index, component ∈ {value, +err, −err}, power-of-ten scale), chosen by majority: ≥ 60% of rows must match.
   - Columns without such a mapping are UNMAPPED. They are derived or converted, are listed, and are excluded from the sample.
   - An error column whose name says + (errhi, E_, ep) must map to the + component, and − (errlo, e_, em) to the − component, in asymmetric cells. A swap is a PROBLEM.
4. **Cell match and row count.**
   - A sampled cell PASSES if it equals the source component at its mapping within 1e-9 relative, after the scale.
   - CSV rows against source data rows: a mismatch is a PROBLEM unless the README documents it.
5. **Machine reads.** For the FITS/CDS reads (S05 KMOS3D FITS, S08 FS+09 .dat, S09 Tacconi+13 .dat), the same 10% sample is drawn and compared with the raw file.
6. **RC100.** Table 3 has no text layer. The rows sampled by the seed (10 of 100) are re-read visually by the auditor from the page images on disk (`_external_data/papers/rc100_table3_images/`), entered into `rc100_visual_reread.csv`, and compared field by field.
7. **Sources not on disk** (read through a page summariser) are UNVERIFIED: ADF22.5 values not in an on-disk PDF; Parlanti+23's rows. Where an on-disk PDF exists (arXiv:2609.06679 for ADF22-WEB), the cited numbers are searched in its text layer.
8. **Digitised curves** (ALPAKA, Lelli+23, Lin+24) cannot be transcription-checked. They are checked against the tabulated numbers of the same paper under §3.

## 7. Check 5: impact (arithmetic only)

For each problem found:
1. List the lanes that read the affected cells (by file name in the lane scripts, and by object in the combined chart).
2. Bound the change in the lane's key quantity (g_obs, g_bar, D or s*). Use only the lane's own printed sensitivities from its README or results JSON, and arithmetic on the affected cells.
3. Compare the bound with the margin between the lane's number and its verdict boundary.

Severity:
- **CRITICAL:** the bound crosses a committed verdict.
- **MAJOR:** the bound could reach the boundary, or the input cannot be verified and has documented leverage that large.
- **MINOR:** it cannot move a verdict. Either the bound is below the margin and the lane's own recipe half-width, or no lane reads the affected cells.

## 8. MUTATE (each check must catch its planted error)

**Base copy:** an in-memory copy of S07 Table 6 (`sins_ao_table6_kinematics.csv`), written as `CFG287_MUTATE_sins_ao_table6.csv`. The original file is untouched.

**Plants:**
- **M1, shifted row:** the `Vc_kms` column of CSV data rows 10–14 (1-based) is shifted down by one row. Row 10 takes row 9's value, …, and row 14 takes row 13's.
- **M2, unit slip:** `Mdyn_1e10Msun` of data row 20 is multiplied by 10.
- **M3, sign flip:** `Vrot_kms` of data row 25 is negated.

**Pass rule:**
- each plant is flagged PROBLEM by its target checks:
  - M1 by the Vc formula (eq. 1);
  - M2 by M_dyn (eq. 2);
  - M3 by the positivity check and by Vrot/σ₀;
- the transcription comparison, run over ALL cells of the mutated table, flags exactly the planted cells;
- no check flags a row the unmutated copy does not flag.

Cross-survey detection of M1 is reported but is not required.

## 9. Outputs

- `cfg287_integrity.py`, its `.out` and `cfg287_results.json`;
- `cfg287_mutate.out`;
- `rc100_visual_reread.csv`;
- `versions_errata_pagereads.json`: the page-read record, entered from the reads;
- `AUDIT.md`: the table of source → checks → problems (severity) → lanes; the clean list; the impact bounds.
