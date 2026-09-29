# High-z disc samples: gas mass, rotation-curve reach, table access

Source hunt for the a0(z) test. The question each row answers: does a published sample give BOTH a baryonic mass
(with a gas component) AND a rotation curve out to radii where g_bar < a0? Compiled 2026-09-28 (file dated as
requested). Every cell carries its basis. "unverified" means I did not read it from a source that would show it;
I opened only abstracts, summaries, arXiv abstract/HTML pages and the CDS copies listed. Publisher pages (IOP,
A&A) refused me (bot check, 403), so table access on those is "unknown", not "none".

**Bottom line.** For no sample below could I confirm all three of: a gas mass, a rotation curve, and a published
table that lets g_bar(R) be built out to g_bar < a0. Nothing here shows any high-z disc actually reaches
g_bar < a0; that is undetermined for every row. Closest candidates: RC100 / Genzel+2020 (curves to large radii,
gas from scalings), MUSE-DARK II (low-mass lensed discs, so low g_bar, but I could not confirm its gas method or
table), and PHIBSS (direct CO gas, but one velocity per galaxy).

| # | sample | N | z | gas source | curve / radius reached | table access (checked) |
|---|---|---|---|---|---|---|
| 1 | Genzel+2020 (KMOS3D, SINS/zC-SINF etc.), ApJ 902, 98 | 41 | 0.67-2.45 | CO or scaling: unverified | individual Halpha/CO curves; the 2017 Nature sample traced curves to 1.5-3 R_e (search summary) | none found; IOP blocked. https://iopscience.iop.org/article/10.3847/1538-4357/abb0ea |
| 2 | RC100, Nestor Shachar+2023, ApJ 944, 78 | 100 | 0.6-2.5 | scaling relations: unverified | outer-RC velocity; radius reached unverified | unknown (IOP blocked). https://iopscience.iop.org/article/10.3847/1538-4357/aca9cf |
| 3 | Price+2021 refit of the Genzel curves, ApJ 922, 143 | z~1-2 | ~1-2 | as Genzel | as Genzel | unknown (IOP blocked) |
| 4 | Ubler+2017 KMOS3D TFR sample, ApJ 842, 121 | 135 | 0.6-2.6 | modelled Mbar; method in paper, unverified | one number: max modelled circular velocity (no curve, no radius) | YES, CDS table, fetched: `data_assembly/high_z_tf_tables/ubler2017.csv` (no errors) |
| 5 | PHIBSS, Tacconi+2013, ApJ 768, 74 | 73 (65 with Vrot) | 1.2, 2.2 (+ lensed to 3.1) | DIRECT CO(3-2), Galactic X, 50% systematic | one Vrot per galaxy plus R_h; no curve | YES, CDS, fetched: `data_assembly/kmos3d_phibss/phibss13_joined.csv` |
| 6 | PHIBSS2, Freundlich+2019, A&A 622, 105 | 60 CO detections of 61 | 0.5-0.8 | DIRECT CO(2-1) | none in this paper (gas survey) | not at CDS (404); A&A page 403; arXiv 1812.08180 abstract says 4 tables |
| 7 | Tacconi+2018, ApJ 853, 179 | 1444 (all methods) | 0-4 | CO, dust, 1 mm | none (gas scaling relations) | not at CDS (404); IOP blocked; arXiv 1702.01140 |
| 8 | Amvrosiadis+2025 ALMA CO discs (arXiv 2312.08959) | 12 | 1.2-4.7 (median ~2.4) | DIRECT CO, alpha_CO 0.92 +/- 0.36 | V_circ at 2 R_e (ledger row) | unknown; not opened |
| 9 | MUSE-DARK II, Jeanneau+2026, A&A (arXiv 2603.28856) | 95 lensed | 0.56-1.37; M* 10^8.1-10.3 | baryonic TFR used; gas method unverified | v at 1.8-2 R_e (ledger); lensing can extend curves beyond the turnover (search summary) | unknown; not opened |
| 10 | MSA-3D (JWST NIRSpec), arXiv 2606.27853 | 30 (23 golden) | 0.5-1.7 | t_depl x SFR scaling (paper) | rotation curves plotted; V_c at 2.2 R_d for TF | plots only in the supplementary PDF; no table found |
| 11 | KROSS / KMOS3D / KGES, Sharma+2024 (arXiv 2406.08934) | 263 | 0.6-2.5 | gas method unverified | v_c at about 5 R_d (ledger row), 3DBarolo | unknown; not opened |
| 12 | Lang+2017 stacked KMOS3D + SINS curves (arXiv 1703.05491) | stack | 0.6-2.6 | none (stack) | outer stacked curve, falling at 99.4% (abstract) | n/a (stack) |
| 13 | GA-NIFS JWST discs: GN20 (z 4.06), the z=4.26 disc, GS-9209 (4.66), GS5001 (3.5) | 4 named | 3.5-4.7 | GN20: ALMA CO (unverified per object) | 3D models; radius unverified | not opened |
| 14 | ALMA [CII] discs: ALPINE (arXiv 2104.03099), ALMA-CRISTAL | tens | 4-6 | [CII]-based, not CO | typical [CII] disc extent 3-5 kpc (search summary) | unknown |
| 15 | KROSS / SAMI matched, Tiley+2019 | 754 rows | ~0.9 and ~0 | none (stellar mass only) | v2.2 at 1.3 R_e | YES, CDS, fetched: `data_assembly/high_z_tf_tables/tiley2019.csv` |
| 16 | BUDHIES, Gogate+2020 | 166 | ~0.2 | DIRECT HI | HI line widths only | YES, CDS, fetched: `data_assembly/high_z_tf_tables/budhies_joined.csv` (no stellar masses) |
| 17 | MIGHTEE-HI RAR, Varasteanu+2025 (arXiv 2504.20857) | 19 | <= 0.08 | DIRECT HI + resolved stellar masses | HI curves (3D Barolo) to low g_bar | Table 1 in the paper; RAR points on request only |
| 18 | KMOS3D cubes, Wisnioski+2019 | 739 | 0.7-2.7 | none in the release | raw cubes, no curves | YES, cubes downloaded and verified: `data_assembly/kmos3d_phibss/` |

## What would settle it (proposals, none done)
- Rows 1-3 and 9: the per-galaxy g_bar(R), g_obs(R) or (R, V, baryon model) tables. If the papers' own appendix
  tables are printed, extracting them needs the PDFs (publisher pages refuse automated access).
- Row 13 and 14: per-object gas and curve at radius, if the papers publish them.
- The only samples with a baryonic mass that includes gas, a velocity, AND a table I could open today are rows 4,
  5, 16 and 17. Row 4 gives Mbar (modelled gas) with one maximum velocity; row 5 direct CO gas with one velocity;
  row 16 direct HI with line widths only and no stellar masses; row 17 direct HI with resolved masses but only
  at z <= 0.08 and with its RAR points on request. None gives a high-z curve with a gas mass.
