# CFG535 INVENTORY: z ~ 1.4-2.1 kinematic and Tully-Fisher sources (compiled 2026-10-09)

Inclusion and "tried" rules: FROZEN_CRITERIA.md sections 1-2. TRIED means a committed lane scored an a0 or law comparison on that source; census = inventoried, not scored. Literature facts not already in the record come from abstract, listing or CDS ReadMe pages only and are PROVISIONAL (no table was fetched). "N in band" counts 1.4 <= z <= 2.1 where the source states it.

## A. On disk (repo or the external cube store)
| # | source | N in band / z | observable | gas route | status in the record |
|---|---|---|---|---|---|
| A1 | RC100, Nestor Shachar+23 (use the `_CORRECTED` csv) | ~half of 100; 0.6-2.5 | V_c(R_e), f_DM, M_bar (model outputs) | Tacconi+20 scaling prior | TRIED: CFG216, CFG233 referee, CFG289, CFG303. Within-sample delta(z) leans flat only at the authors' gas trend; W-none at the measured-gas tilt |
| A2 | RC41 / Genzel+20 / Price+21 (text of arXiv 2006.03046 in `_external_data/cfg567/`) | ~25; 0.67-2.45 | curves to 1.5-3.8 R_e; Table D1 decompositions | scaling + some CO | TRIED: CFG210 (mass-route drift null), CFG567 census (low-V discs reach 0.48-0.52 a0 but no gas map) |
| A3 | Genzel+17 six deep curves | 4; 0.85-2.4 | individual outer curves | Table 1 priors | TRIED: CFG400 INVALID, CFG401 gate FAIL (possible high-z tension, unscored) |
| A4 | KMOS3D cubes, K band z >= 1.9 | 195 | own 3-D arctan fits | none (stars only) | TRIED: CFG270 (class D, s* <= 2.4) |
| A5 | **KMOS3D cubes, H band z 1.3-1.8** (in `../_external_data/kmos3d/cubes relative to the repo root`, outside the repo) | 170 catalogue rows | cubes, no fit yet | none | **UNTRIED** (CFG270 fitted only the K-band set). A CFG270-type stars-only bound at z ~ 1.5 is possible on disk; class D; also the raw material for an in-band self-built stack (F1/F2) |
| A6 | KMOS3D x SINS overlaps | 5 | AO inner + seeing outer | none | TRIED: CFG386, CFG475 (pre-flight, < 10) |
| A7 | SINS AO (FS+18) and SINS 2009 dynamics | ~30-40 at z ~ 2.2 | V at one radius | SFR-based | TRIED: CFG280, CFG196 |
| A8 | Ubler+17 KMOS3D bTFR (`high_z_tf_tables/ubler2017.csv`) | 24 at 1.3-1.8, 46 at >= 1.8; 135 total | max modelled V_c, M_bar | modelled | TRIED as two published bin offsets (prep_2026 fork: WASH) and in CFG52/90's pooled count; **within-sample delta(z) = T1 here (NON-DIAGNOSTIC)** |
| A9 | PHIBSS Tacconi+13 | z 1.2 and 2.2 | one V_rot, R_1/2 | direct CO | TRIED: CFG164/166, CFG196/197 |
| A10 | KURVS-CDFS (Puglisi+23) | 22; z ~ 1.5 | deep outer curves to 4-7 R_d | none | TRIED: CFG140-142, 160, 161, 163-167, 170, 180, 184, 189, 569 (conditional lean rival, not robust) |
| A11 | MSA-3D (Ju+ 2026, arXiv 2606.27853) | 7 at 1.4-1.68 | vrot(R_e), f_DM; curves figure-only | t_depl x SFR | TRIED: CFG6, CFG52/90; per-radius curves not public |
| A12 | ALPAKA (Rizzo+) | 10 | [CI]/CO curves | resolved | TRIED: CFG272 |
| A13 | Amvrosiadis+25 | 2 | CO V at 2 R_e | CO | TRIED: CFG274 |
| A14 | Lelli+23 zC-400569 (2.24), zC-488879 (1.47); Bouche+23 same pair | 1-2 | CO curves to ~8 kpc | CO | TRIED: CFG278; CFG567 near-miss (never deep) |
| A15 | NOEMA3D (arXiv 2505.07925, z ~ 1.5 barred; 2604.18503, z 1.1-1.6) | 3-5 | CO kinematics | resolved CO | census only (CFG567): profiles not public, never deep |
| A16 | SDSS J0901 lensed (arXiv 2211.08488) | 1 at 2.26 | CO + Halpha | CO | census only (CFG567): curve stops at ~1 R_e |
| A17 | SIGMA, Simons+16 (`high_z_tf_tables/simons2016_sigma.csv`) | ~35 of 49; 1.3-2.5 | slit V_rot, fixed turnover radius | none | UNTRIED (stellar-only slit TF; weaker than A8; not ranked) |
| A18 | ALMA archive z 1.2-2.0; sealed predictions | 2 proprietary discs | | CO pending | CFG568-570; CFG571 sealed (U4_27928 public 2026-11-06, GS4_24110 public 2026-11-28); CFG572/573 |
| A19 | Roman-Oliveira+26 (arXiv 2601.03338) "fast rotations at cosmic noon" | compilation | | | census only (text on disk) |

## B. Public, not on disk (would need the owner's go)
| # | source | N / z | what is public | size (approx.) | status |
|---|---|---|---|---|---|
| B1 | **Lang+17** stacked KMOS3D + SINS curve (arXiv 1703.05491; ApJ 840, 92) | 101; 0.6-2.6 (not split to 1.5-2 in the abstract) | stack slope -0.26 (+0.10/-0.09) in V/V_max per R/R_turn (abstract); stack points figure-only; a stacking-sample table on the arXiv HTML (seen by structure in the record, not read) | HTML ~0.3-1 MB; PDF ~5 MB | UNTRIED (cited only) |
| B2 | **Tiley+19** stacks (arXiv 1811.05982; MNRAS 485, 934) | ~1500; 0.6-2.2 | stacked curves normalised by R_d, flat or rising to ~6 R_d (abstract); figure-only | PDF ~5-10 MB | UNTRIED; its explanation of Lang's fall (normalisation and seeing) is not verified here |
| B3 | **KGES table A1** (Tiley+21, CDS J/MNRAS/506/323) | 288 (126 kinematic subsample); 1.2-1.8 | z, M* (MAGPHYS), R50, v2.2c at 1.31 R50, sigma0c, j | 288 x 148 B = 43 KB (ReadMe read 2026-10-09) | UNTRIED; same pipeline as the on-disk KROSS/SAMI Tiley+19 table |
| B4 | KGES reduced cubes | 288; 1.2-1.8 | cubes (hosting NOT confirmed; the Durham KROSS data page returned 404 today) | unknown (KMOS cubes ~5 MB each, so ~1.5 GB if hosted) | UNTRIED; KURVS targets are 20 of 22 KGES galaxies |
| B5 | Genzel+20 / Price+21 published tables (already as text on disk) and RC100 | | | | TRIED (A1, A2) |
| B6 | Nestor Shachar+25 zC406690 ring (arXiv 2503.00839), z 2.2 | 1 (just above the band) | ring 2e10 at 4.6 kpc, bulge 8e10, H2 7.1e10 (abstract-level) | PDF ~10 MB | UNTRIED: a ring geometry could replace the exponential-disc shape that broke CFG400/401 for this galaxy; single object, outside 1.4-2.1 |
| B7 | MSA-3D per-radius curves | 6 at 1.51-1.68 | figure-only; author request | | needs authors (CFG567) |

## C. Searched, nothing in band
JWST NIRCam grism kinematics (FRESCO / geko, z 4-6); GA-NIFS (z > 3); Danhaive+25 (3.8-5.8); MUSE-DARK II/III (z <= 1.44; CFG190); MAGPI (z < 0.85); Sharma+24 on disk (KROSS z 0.76-1.04); KDS (z ~ 3.5). No 2025-2026 paper with tabulated z 1.5-2 per-radius rotation curves plus a gas budget was found beyond A11, A15 and B6. Searches were web and abstract-level only (2026-10-09); a full ADS listing sweep was not possible (ADS / CDS HTML pages refused the fetcher).

## Ranked shortlist of untried tests (forecasts in `cfg535_forecast.out`, post hoc in `cfg535_posthoc_calibration_needed.out`)
Z_eff = min over truths (FLAT, H(z)) of sqrt(median Delta chi^2), nu_mono, sigma_stat(S) = 0.05, shared nuisances drawn per mock.
| rank | test | data | Z_eff canonical / alt (frozen priors) | class | what makes it crisp |
|---|---|---|---|---|---|
| 1 | F2 population self-calibration: stack shape S x amplitude A | own stack from A5 (on disk) + B3/B4 | 0.34 / 0.53 | WEAK | post hoc: pressure known (Kretschmer) + gas and M* to 0.10 dex: 1.78 / 1.55; everything to 0.05 dex and gas extent known: 2.25 / 2.39. Still < 3 at sigma_stat(S) = 0.05; needs sigma_stat(S) <~ 0.025 as well (several hundred in-band discs reaching 6 R_d) |
| 2 | F1 stacked outer shape alone | B1, B2 (published stacks) or own stack | 0.47 / 0.51 | WEAK | the pressure prescription alone moves S by 0.19-0.29 at central nuisances (Burkert vs Kretschmer) against a law separation of 0.17-0.20 |
| 3 | T1 within-sample delta(z) of Ubler+17 | A8 (on disk) | power gate Pi 0.54 / 0.62 | NON-DIAGNOSTIC (run) | needs the gas z-tilt known to <~ 0.05 dex per unit z |
| 4 | KGES same-pipeline amplitude (A only) | B3 (43 KB) | 0.41 / 0.55 | WEAK | the CFG170 two-epoch gas-ratio wall applies |
| 5 | zC406690 ring re-model | B6 | not forecast | single object | a stated ring + bulge mass model; outside the 1.4-2.1 band |
