# Data at z = 2-5 that observers took but nobody turned into a RAR or a0, and what we hold or can get (data front, 2026-09-30)

Request (my user): find all the data between z 2 and z 5 that scientists took, where the a0 or RAR was not calculated in the original work, but which we can process now.
Method: our own inventories (ledger, parsed tables, `HIGHZ_SOURCE_TABLE_2026-09-29.md`), the tables parsed today, and targeted read-only searches (abstract and arXiv-page level). **"Not computed by the authors" is UNVERIFIED for every row unless stated**: I checked abstracts and tables, not full texts. No paper I read reports a RAR or a0 at z = 2-5; the nearest are dark-matter fractions (RC100, Genzel+2020, CRISTAL, NOEMA3D, Ubler+2018) and one MOND mass-model test on two discs (Lelli+2023, z = 1.47 and 2.24).
To build a RAR point one needs V at a stated radius (or a curve), a baryon model (stars and gas) and a radius. The last column says how many galaxies in each set are at 2 <= z <= 5.

## A. Already on disk, parsed, kinematics plus baryons (ready to process now)
| set | N (all z) | N at z 2-5 | kinematics | baryon inputs | on disk | note |
|---|---|---|---|---|---|---|
| RC100 (Nestor Shachar+23) | 100 | **41** | V_c(R_e), R_e, sigma_0, f_DM (Table 3, three-method average) | M_baryon (fitted with an SED+scaling-gas prior, 0.2 dex in the Price+21 method) | `rc100_provenance/rc100_table3_six_fields_paper_values.csv` (the repo's own CSV has 16 wrong rows) | one radius (R_e) per galaxy; curves to 1.3-4 R_e exist in the papers but are not tabulated |
| SINS/zC-SINF AO (Forster Schreiber+18) | 35 (+3 components) | **35** | V_rot, sigma_0, V_c, M_dyn, R_e, sin i (Table 6) | SED M*; no gas in the release | `highz_literature_tables/sins_ao/` (+ 6.7 GB of AO cubes, unprocessed) | six overlap PHIBSS (CO gas, one velocity each) |
| ALPAKA I (ALMA CO/[CI]) | 19 discs | **10** | V_max, V_ext, digitised rings (118 rings, R_ext to 6.3 kpc) | SED M*; CO or [CI] line luminosity, **no conversion applied** | `arxiv_tables/alpaka1_*.csv`, `alpaka1_digitised/` | |
| Amvrosiadis+25 (ALMA CO, SMGs) | 12 modelled (30 parent) | **9** | V_circ at 2 r_e, V_max, M_dyn(<10 kpc) | MAGPHYS M*; CO gas with alpha_CO = 0.92 (justified by the paper's own dynamics: circular) | `arxiv_tables/amvrosiadis_*.csv` | |
| ALMA-CRISTAL | 14 modelled | **6** (8 more at z 5.0-5.7) | model V_circ curves read exactly from the vector figure plus observed markers | SED M*; dust gas for 6, upper limits for 4 | `arxiv_tables/cristal_vector/`, `cristal2025_*.csv` | baryon mass is a fitted DysmalPy parameter |
| ALPINE rotators, Jones+21 (new today) | 8 with rings (30 classified) | **3** (5 at z 5.0-5.7) | per-ring R, v_rot, sigma_v, M_dyn (2-3 rings per galaxy, R 0.5-5.5 kpc) | **none in the tables**: M* in Faisst+20, [CII]-gas in Dessauges-Zavadsky+20 (neither parsed; no per-galaxy gas table) | `highz_literature_tables/jones2021_alpine/` | table gives 7 'ROT' (abstract says 6) |
| ZFIRE (Alcorn+18, new today) | 44 | **44** (z 2.06-2.44) | V_2.2 (velocity at 2.2 scale lengths), sigma_g, j_disk | SED M*, SFR; gas would be a scaling (not measured) | `highz_literature_tables/zfire2018/` | slit (MOSFIRE) kinematics, one point each |
| Roman-Oliveira+23 (ALMA [CII]) | 4 | **4** (z 4.3-4.4) | V_max, V_ext, sigma | CO gas (alpha_CO 0.8); **no M*** | `arxiv_tables/romanoliveira2023_*.csv` | |
| Danhaive+25 (JWST grism Halpha) | 41 | **33** | v/sigma_0, M_dyn (R_e only) | SED M*; **no gas** | `arxiv_tables/danhaive2025_gold.csv` | gas-independent floor only |
| Lelli+23 (two ALMA CO discs) | 2 | **1** (z 2.24; the other is 1.47) | 3DBarolo curves to ~8 kpc | CO gas, stars, bulge; MOND and NFW mass models | `arxiv_tables/lelli2023_*.csv` | **the authors did test MOND here** |
| Singles with V plus several gas tracers | 4 | **4** | J081740 (V_rot 272 km/s, [CII] to 4.2 kpc), GN20 (CO V_max 575, Halpha ~500), REBELS-25 (z 7.3, out of range), PKS 0529-549 (z 2.57, curve to 3.3 kpc) | see `MULTI_TRACER_GAS_2026-09-30.md` | partly | each N = 1 |
**In range with some kinematics and baryons: about 190 galaxies** (41 RC100, 35 SINS, 10 ALPAKA, 9 Amvrosiadis, 6 CRISTAL, 3 Jones, 44 ZFIRE, 4 Roman-Oliveira, 33 Danhaive without gas, 1 Lelli, plus singles), with overlaps (SINS x PHIBSS, CRISTAL x ALPINE) not removed. **Only the gas-carrying, tabulated-radius subsets are real RAR candidates:** ALPAKA 10, Amvrosiadis 9, CRISTAL 6, Roman-Oliveira 4, Lelli 1 and the singles (about 30); RC100, SINS and ZFIRE give one radius each and use scaling or no gas.

## B. Public data that exist but are NOT yet in our hands (z 2-5; each would need a fetch and then an extraction)
| data | what it is | why it qualifies | status |
|---|---|---|---|
| **KMOS3D cubes, z >= 2 part** | 739 galaxies' Halpha cubes (6.7 GB on disk, verified, unprocessed) | velocity fields; RC100 and Sharma+24 used them for curves | **on disk** |
| **SINS/zC-SINF AO cubes** | 35 galaxies (6.73 GB on disk) | AO-resolved Halpha kinematics | **on disk** |
| ALPINE [CII] cubes and the **High-z Kinematic Corpus Z1** (31 galaxies, z 4.26-5.68; 8 tier-1 rotation curves; SED M*, no gas; arXiv:2605.25339) | public; Zenodo DOI 10.5281/zenodo.20369285 (corrected 21834678) | rings plus M*; gas from [CII] | **Zenodo returned 403 (bot protection) to my fetch**; needs a browser download |
| **JADES DR3 NIRSpec** (~1,000 galaxies at z > 1.5 with Halpha; group rotation curves in arXiv:2609.14071) | public MAST | statistical rotation curves at cosmic noon, stellar masses from SED; no gas | not fetched (size not priced) |
| ASPECS / VLASPECS CO cubes (HUDF, z 1-3.6; only three sources with a clear velocity gradient) | public ALMA | direct CO gas | not fetched |
| SDP.81 (z = 3.042, lensed; CO rotation v = 320+-20 km/s, M_dyn = 3.5e10 within 1.5 kpc) and the SPT lensed SMGs with [CII] cubes (Rizzo+21, five sources, z ~4.2-4.4) | public ALMA archive | resolved gas curves, gas and dust | not fetched; baryon models would be ours |
| GA-NIFS (JWST NIRSpec IFU, 55 targets z 2-11, e.g. the z = 4.26 disc, GS5001 z 3.5, GN20 z 4.06) | public from MAST after the proprietary period | ionised-gas kinematics plus ALMA gas where observed | not fetched |
| KLEVER (z 1.2-2.5 lensed, KMOS), HATLAS J0849 z = 2.4 overdensity (arXiv:2603.23608), a DOG at z = 3.11 (arXiv:2603.01352), a compact SFG at z = 2.3 (arXiv:1712.01283) | ESO and ALMA archives | single or few objects | not fetched; most z below 2 |
| Dunne+22 and ACE (gas only) | in hand | gas calibration at z 2-5, no kinematics | **on disk** |

## C. What the authors already did (so these are not 'uncomputed')
RC100, Genzel+20, Price+21, CRISTAL, NOEMA3D and Ubler+18 computed **dark-matter fractions** inside R_e (not a RAR). Lelli+23 fitted **MOND** mass models to two CO discs (z 1.47, 2.24). MUSE-DARK III (z 0.33-1.44, out of range) fitted a RAR and claims a0 rising with z. The z = 2-5 RAR/a0 has no dedicated published test that I found.

## D. What I suggest next (my user decides)
1. Process the two cube sets already on disk (KMOS3D z >= 2 and SINS): extract rotation curves and, with the SED masses and the Tacconi scaling gas, build RAR points. This is analysis (the calc thread's lane, under frozen criteria) but the raw data are here.
2. Get the ALPINE Corpus Z1 and the per-galaxy gas tables of Dessauges-Zavadsky+20 (the Zenodo block needs a browser).
3. Price (read-only) and then fetch the JADES DR3 NIRSpec table, the ASPECS and SDP.81 cubes and the SPT [CII] cubes.
