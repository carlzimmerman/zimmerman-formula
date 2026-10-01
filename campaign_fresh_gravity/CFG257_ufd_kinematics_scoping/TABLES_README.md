# CFG257 transcribed tables (data front, 2026-10-01)

Two tables transcribed from the PDFs already held (fetched earlier in this session by page reads; the PDFs themselves and their text are NOT committed). **No offset, difference or score is computed in any file here**; the calculation lane freezes its criteria first.

| file | what | rows |
|---|---|---|
| `arroyo_polonio2026_tableA1.csv` | Arroyo-Polonio, Battaglia & Thomas 2026, A&A 708, A287 (arXiv:2603.03129), **Table A.1**: single-epoch sigma_los without binaries (f = 0), with a flat prior on the binary fraction (free f), and with f = 0.7, plus the literature value used, N stars, log M, log J, data reference | 12 (8 flagged `in_cfg28_29_sample`) |
| `geha2026_paperII_tableA1.csv` | Geha 2026, Keck/DEIMOS Stellar Archive II (arXiv:2602.10202), **Table A1**: DEIMOS velocity dispersion (resolved, or 95% upper limit), N member stars, v_sys, [Fe/H], for all systems | 67 |
| `geha_vs_lvd_match.csv` | for each of the 40 ultra-faint rows with a dispersion or limit in `real_research/data/dsph/lvd_dwarf_mw.csv` (the CFG28/29 table): the LVD value and reference beside the Paper II row (matched by sky position < 0.2 deg, else identical name; only Bootes III by name, 0.34 deg apart), values side by side, nothing subtracted | 40 (19 matched) |
| `build_arroyo_tableA1.py`, `build_geha2_tableA1.py`, `check_tables.py`, `check_tables.out` | the transcription scripts (input: `pdftotext -layout` of each PDF) and the row-by-row check; all checks pass | |

## How to reproduce
Fetch the two arXiv PDFs (4.6 MB and 0.68 MB), run `pdftotext -layout` on each, then `python3 build_arroyo_tableA1.py <txt>`, `python3 build_geha2_tableA1.py <txt>`, `python3 check_tables.py <arroyo txt> <geha txt>`. The PDFs used here (SHA-256 of the cached files): Arroyo-Polonio+26 `b0c9df8a8b655a4ee50740d8cbc15f6ad26637704ccf1ded280b1f39dbdde5ec`; Geha II `1204e5135a2e99ae8498e2d3c5f1b840108ed4fbdffbf7c5477d765ca2fd6fc3`.

## Conventions and cautions (read before using)
- **Arroyo-Polonio: asymmetric posteriors.** Each corrected quantity is the median with +1sigma(+3sigma) and -1sigma(-3sigma) ranges as printed (`*_up1`, `*_up3`, `*_lo1`, `*_lo3`; the literature sigma and a_1/2 have 1-sigma values only). `sig_f0` is the paper's own no-binary estimate **from the same dataset**, so the binary correction is `sig_free` or `sig_f07` against `sig_f0`, not against `sig_lit`; the datasets (`ref`) are single-epoch literature data and are **not the LVD datasets** (Boo I: Koposov+2011 here, Sandford+2026 in LVD; Seg 1: Simon+2011 here, Geha+2026 in LVD; Ret II: Koposov+2015b here, Walker+2015 in LVD; Willman 1: Willman+2011 here, Chiu+2026 in LVD; Leo IV and Leo V: Jenkins+2021 here, Geha+2026 in LVD).
- Eri III's literature value (`0.0 +9.1 -0.0`, footnote [a]) is the 90% upper bound, not a measurement; Ret II's value differs from the literature for a reason given in the paper's Appendix B (footnote [b]). Eri III, Cra II, Sag II and UNIONS 1 are not in the CFG28/29 table (they are not in the LVD ultra-faint list used there).
- **Geha II: -999 means "not applicable".** A row with `sigma_resolved = 0` is an unresolved dispersion (the Bayesian evidence test failed) with the 95th-percentile upper limit in `sigma_ul95`; resolved rows carry sigma and the 16th-84th percentile errors (`e_sigma_ll`, `e_sigma_ul`). The `*_raw` columns keep the printed values and `source_line` the PDF line. The M_V, distance and r_1/2 columns are the paper's (from Pace 2025).
- 2 of the 15 LVD rows that cite Geha+2026 (Columba I, Pisces II) are not in Paper II's 67 rows (Paper II requires 10 or more member stars); 13 of 13 that are in Paper II equal the LVD value exactly (check G9, an independent control on the transcription).
- Check A5b (informational): the paper's literature error for Hydrus I (+-0.5) is symmetrised against LVD's +0.51/-0.43.
- The match file is by position and name only; a missing `geha_*` column means the system is not in Paper II's table (not observed with DEIMOS in this compilation, or fewer than 10 members).
