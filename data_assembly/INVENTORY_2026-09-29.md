# Data inventory: high-z kinematics, gas and baryons (data front)

Compiled 2026-09-29. Everything below is public data; large files live OUTSIDE the repo in `~/new_physics/_external_data/`. "Parsed" means turned into CSV
with checks in this repo; nothing here is a fit or a test of a0. Companion: `HIGHZ_SOURCE_TABLE_2026-09-29.md` (18 samples, gas source, radius reached, table access).

## In the repo (parsed, checked, pushed)
| package | what | key caveat |
|---|---|---|
| `kmos3d_phibss/` | KMOS3D catalogues (785 rows, no kinematics); PHIBSS Tacconi+2013 (73 galaxies, 65 with Vrot, direct CO gas); the two do not overlap | Vrot has no defined radius (`TACCONI2013_VROT_RADIUS_NOTE.md`); 6 CO upper limits; 3 rows with an fgas the source does not reproduce |
| `high_z_tf_tables/` | Ubler+2017 (135), BUDHIES (166 HI, z~0.2), Tiley+2019 KROSS/SAMI (754), KROSS V2 (586, velocity at 1.3 and 2 R_1/2), SINS (47), SIGMA (49) | BUDHIES has no stellar masses; KROSS V2 has no gas and sentinel-like magnitudes in nine rows; SINS gas is a model |
| `arxiv_tables/` | tables from public TeX/FITS source: MSA-3D (30), Mancera Pina (43), Amvrosiadis (12 ALMA CO discs), Sharma 2024 (225 KROSS, velocities to about 5 R_D), ALPAKA I (28 galaxies, 19 disks), Lelli 2023 (2 discs), the three JWST-informed ALPAKA decompositions, ALMA-CRISTAL (32 galaxies, 14 modelled) | Sharma gas is scaling-relation, not measured; ALPAKA I gives L' not gas mass; CRISTAL is [CII] and model-based |
| `arxiv_tables/alpaka1_digitised/` | ALPAKA I rotation curves digitised from a raster figure (118 rings, 19 disks), R_ext, R_e where drawn | validated to 1.6% against the paper's table; R_e only for 7 disks |
| `arxiv_tables/cristal_vector/` | CRISTAL V_bary, V_DM, V_tot, f_DM, sigma_0, R_e and markers read exactly from a vector PDF | model curves (asymmetric-drift corrected, fitted baryon mass, [CII] gas); CRISTAL-09 and -15 disagree with the table |

## Outside the repo (`~/new_physics/_external_data/`)
| folder | content | status |
|---|---|---|
| `kmos3d/` | 739 KMOS3D cubes (3.8 GB unpacked) and tarballs | complete, sizes = server Content-Length, gzip OK; hashes in `kmos3d_phibss/manifest.json`; no fit run here |
| `sins_ao/` | SINS/zC-SINF AO release, 35 z~2 galaxies, five FITS per galaxy (4.0 GB) | downloading; `finish.sh` verifies size and gzip and unpacks; read `finish.log` |
| `arxiv_src/` | TeX/figure sources of 11 papers (the tarballs are about 130 MB; the extracted folders are larger) | fetched; parsed where the tables were extractable |
| `cds_tables/` | CDS copies of the tables parsed into `high_z_tf_tables/` (Ubler, BUDHIES, Tiley, KROSS V2, SINS, SIGMA) | parsed; the PHIBSS 2013 tables are in `kmos3d_phibss/raw_small/` |
| `papers/` | Tacconi+2013 PDF, RC100 PDF | read for text and tables |

## Where the a0 test stands on this data (facts only)
- No sample I could open pairs a MEASURED gas mass with a velocity at a radius where g_bar < a0. Closest: ALPAKA I (measured CO/[CI] luminosity, 19 disks, outer radius from the digitised figure; total acceleration at the outermost ring 2-32 a0), Lelli+2023 (V^2/R > 3-4 a0 by the paper's own statement), Amvrosiadis (about 10 a0).
- CRISTAL z 4.4-5.7 is the only set with model g_bar < a0 at the outermost observed marker (7 of 14), and it is pressure-supported with [CII] gas and a fitted baryon mass.
- ALPAKA ID1 (z 0.56) is about 1.6 a0 with the JWST-informed baryon mass; an earlier note of mine (0.5-0.8 a0) is superseded.

## Candidates not fetched
Neeleman+2020 z = 4.26 disc (arXiv:2005.09661, source 5.5 MB), Roman-Oliveira+2023 four z~4.5 discs (arXiv:2302.03049, 5.5 MB), Rizzo+2020 SPT0418-47 (arXiv:2009.01251), REBELS-25 (arXiv:2405.06025). RC100's per-galaxy values are not in its paper (only counts and medians).
