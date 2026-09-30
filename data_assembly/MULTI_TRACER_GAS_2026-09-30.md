# Galaxies with gas masses from two or more independent tracers (data front, 2026-09-30)

Request (orchestrator, after CFG217/219/221/223): the gas-mass calibration at z ~ 1-5 has to be known to 0.05-0.15 dex, so list every galaxy on disk or in readable tables with gas masses from >= 2 independent tracers (CO with alpha_CO, dust with T_d and beta, [CI], [CII] with a conversion).
Method: READ-ONLY. Local tables and TeX, plus abstract-level page reads (marked UNVERIFIED). Nothing downloaded. One reconstruction was computed from tabulated fluxes (section 1) with a committed script and a control; everything else quotes stated values.

## 1. On disk: NOEMA3D (10 galaxies, z 1.12-1.63): CO + dust for all 10, CO + [CI] + dust for 6
Paper 2 (arXiv:2604.18504) tabulates, for every galaxy, the integrated fluxes S_CO, S_CI and S_dust (Table 2) and only the CO-based M_mol (Table 1); the dust and [CI] masses exist only in its figures. `multitracer_gas/noema3d_three_tracer.py` reconstructs all three from the TABULATED fluxes with the paper's stated recipes (Sect. 3.4: CO alpha_CO = 4.36 with R_14 = 2.4 (CO(4-3), group 1) or R_13 = 1.8 (CO(3-2), group 2); dust T_d = 25 K, beta = 1.8, alpha_850 = 6.7e12 W/Hz/Msun; [CI](1-0) alpha_CI = 18.7; Planck18 distances, which matches the paper's CO masses better than H0 = 70, Om = 0.3 over group 1).
**These are this script's reconstruction, not the paper's numbers.** The CO control (reconstructed vs Table 1) is 0.000-0.005 dex for 5 of the 6 group-1 galaxies and **fails for the other 5**: G4_23011 (+0.149 dex, unexplained) and all four group-2 galaxies (+0.24 to +0.26 dex, a factor ~1.76; the R_13 = 1.8 reading of the paper's text does not reproduce Table 1, so the table evidently uses another convention). Where the control fails, the dust column is still listed but carries that unresolved uncertainty. The dust observed frequency is taken as the CO line frequency of the same tuning (the text says similar frequencies), about 0.05 dex extra uncertainty; conversion-factor uncertainties (alpha_CO +-0.9, alpha_850 +-1.7e12, alpha_CI +-0.6) are not propagated.

| galaxy | z | group | log M_mol CO (paper Table 1) | log M_mol CO (reconstructed; residual dex) | log M_mol [CI] (reconstructed) | log M_mol dust (reconstructed) | CO control | log M* (SED) |
|---|---|---|---|---|---|---|---|---|
| G4_38065 | 1.1151 | 1 (CO(4-3)) | 10.82 | 10.818 (-0.002) | 10.789 | 10.93 | PASS | 11.43 |
| G4_38232 | 1.1159 | 1 (CO(4-3)) | 10.54 | 10.535 (-0.005) | 10.457 | 10.698 | PASS | 10.82 |
| G4_20371 | 1.1165 | 1 (CO(4-3)) | 10.71 | 10.71 (-0.000) | 10.528 | 10.522 | PASS | 10.87 |
| G4_23011 | 1.1917 | 1 (CO(4-3)) | 10.67 | 10.819 (+0.149) | 10.829 | 10.753 | FAIL | 11.1 |
| GN4_24517 | 1.2411 | 1 (CO(4-3)) | 10.47 | 10.465 (-0.005) | 10.287 | 10.447 | PASS | 10.86 |
| GN4_18574 | 1.2463 | 1 (CO(4-3)) | 10.86 | 10.856 (-0.004) | 10.711 | 10.887 | PASS | 10.89 |
| G4_24078 | 1.3595 | 2 (CO(3-2)) | 10.5 | 10.755 (+0.255) | - | 10.504 | FAIL | 10.78 |
| GN4_32842 | 1.5233 | 2 (CO(3-2)) | 10.8 | 11.046 (+0.246) | - | 10.839 | FAIL | 11.32 |
| G4_17555 | 1.5372 | 2 (CO(3-2)) | 10.2 | 10.447 (+0.247) | - | 10.701 | FAIL | 10.45 |
| G4_37375 | 1.6335 | 2 (CO(3-2)) | 10.2 | 10.44 (+0.240) | - | 10.749 | FAIL | 10.63 |

Source files: `noema3d/noema3d_per_galaxy.csv` (Tables 1-3), `multitracer_gas/noema3d_three_tracer_reconstruction.csv`. Four dust fluxes are faint (0.04-0.07 mJy: G4_24078, G4_17555, G4_37375, GN4_32842); [CI] was observed only for group 1.

## 2. Explicit multi-tracer values in papers on disk or read
| galaxy | z | tracers and stated masses | where | status |
|---|---|---|---|---|
| J081740 (DLA0817g, Neeleman+2020) | 4.2603 | **CO(2-1)**: M_mol = (8.8+-2.6)e10 x (0.81/r_21) x (alpha_CO/3.0) Msun (JVLA; r_21 = 0.81, alpha_CO = 3.0); **FIR continuum**: 5.7+-0.7e10 x (6.7e19/alpha_850) (Scoville+2014); **[CII]**: 9.8+-0.6e10 x (alpha_[CII]/30) (Zanella+2018). The paper says the three agree and reports the CO one. Statistical errors only | TeX on disk (arXiv:2005.09661, Methods 'Molecular Gas Mass Estimates') | read; no table, three formulas |
| GN20 | 4.055 | CO(2-1)/(4-3): M_mol ~5-13e10 (Daddi09, Carilli10, Hodge12); NOEMA + radiative transfer: M_mol = 2.9e11 with alpha_CO = 2.8; dust M_dust = 5.7e9 (+0.8,-0.6), gas-to-dust ~50 (arXiv:2510.17804, abstract-level) | intro of arXiv:2403.03192 (TeX on disk); 2510.17804 not on disk | abstract-level, UNVERIFIED |
| REBELS-25 | 7.3065 | CO(3-2) ~3.5 sigma: (1.0+-0.4)e11 with alpha_CO = 3; radiative-transfer model 1.8(+1.0,-0.9)e11; [CII]: alpha_[CII] = 60+-25 derived from CO+[CII] (arXiv:2606.13393); Rowland+2024 dynamical gas M_dyn - M* = 1.1e11 (not independent) | CO paper not on disk | abstract-level, UNVERIFIED |
| CRISTAL-22 | not read in the local table | dust continuum (Scoville+2016, T_d = 50 K from FIR SED modelling, beta = 1.8) gives f_molgas = 0.71 (+0.28,-0.12), 'consistent with' VLA CO(2-1) of Pavesi+2019 | TeX on disk (arXiv:2507.11600 Appendix dust2gas) | CO mass not given in the paper text read |
| PKS 0529-549 | 2.57 | [CI](2-1), CO and dust; gas ~1e11 Msun by three methods that differ by up to a factor 4 (arXiv:2411.04290; ledger row; abstract-level) | not on disk | UNVERIFIED |
| ACE survey (Shivaei+, arXiv:2609.21604) | 2.0-2.5 | CO(3-2) (17 of 25 detected) and Band 7 continuum (17 of 25) | not on disk | abstract-level, per-galaxy masses not seen |
| DYNAMO discs (White+2017, Fisher+2014) | 0.1 | CO(1-0) with Halpha kinematics; dust from Herschel (ledger row; abstract-level) | not on disk | UNVERIFIED |

## 3. Checked and single-tracer (not multi-tracer)
- **PHIBSS 2013 and PHIBSS2 (z 0.5-0.8)**: CO only (Galactic alpha_CO; Tacconi formula). `kmos3d_phibss/`, `phibss2_z05_08/`.
- **CRISTAL (14 modelled discs)**: dust only (six detections, four upper limits); [CII] is the kinematic tracer, not a gas mass. `arxiv_tables/cristal2025_*.csv`.
- **Amvrosiadis+2025 (30 CO sources)**: CO only (several J lines converted with one excitation correction, alpha_CO = 0.92+-0.36 which the paper justifies with its dynamics); L_IR and SFR are tabulated but **no dust mass**; two footnoted sources take their gas mass from other papers (Wardlow+2018, Calistro Rivera+2018), still CO-type. `arxiv_tables/amvrosiadis_parent.csv`.
- **ALPAKA I (28 galaxies)**: one line per galaxy (CO(2-1)...(7-6) or one [CI] line, 1 CO(4-3) and 2 [CI] sources), no galaxy with two independent tracers. `alpaka1_alma_obs.csv`.
- **Girard+2021 (21 galaxies)**: f_gas of one kind per source (CO for PHIBSS and DYNAMO rows); not multi-tracer in the table read. **Ubler+2018** (EGS_13011166): CO gas from PHIBSS, plus the fitted mass model; no second tracer. **Roman-Oliveira+2023**: literature CO with alpha_CO = 0.8 only. **KURVS-15**: Band 6 dust not detected (upper limit), CO cubes not fetched.
- **CHILES XI (z 0.22-0.47, 4 galaxies)**: HI plus CO are components of the gas, not two tracers of one mass.

## 4. Compilations PARSED on 2026-09-30 (my user's go; arXiv HTML pages read by code, sources fetched; sha256 of pages in `multitracer_gas/manifest_multitracer.json`; script `multitracer_gas/build_multitracer.py`; checks in `checks_multitracer.txt`)
Per-galaxy CSVs are in `multitracer_gas/`. **Independence notes matter:**
| set (file) | N | z | tracers and what the table holds | independence and conversions |
|---|---|---|---|---|
| Stripe82, Bertemes+18 arXiv:1803.08926 (`stripe82_z_lt0.3_CO_dust.csv`) | 78 | 0.03-0.20 | log M_gas,CO and log M_gas,dust for every galaxy, plus M*, SFR, metallicity, T_dust, M_dust, M_dyn, M_HI | CO: alpha_CO,MW = 3.2 times the metallicity factor (geometric mean of G12 and B13); dust: Leroy+2011 metallicity-dependent dust-to-gas. The paper finds 0.17 dex scatter and 0.05 dex offset between the two |
| H-ATLAS z = 0.35, arXiv:2111.09067 (`hatlas_z035_CI_CO_dust.csv`) | 12 | 0.35 | L'_CI, L'_CO, L_850, M*, L_IR, M_dust, plus per-galaxy X_CI, alpha_CI, alpha_CO, delta_GDR, alpha_850, M_H2 | the conversions are solved jointly per galaxy so the three masses agree **by construction**; the independent content is the three luminosities |
| Bourne+19 arXiv:1810.01640 (`bourne2019_z1_CI_CO_dust.csv`, `bourne2019_line_fluxes.csv`) | 10 (9 with masses) | 0.84-1.22 | M_dust (SED and continuum), M_mol from [CI] (Q10 = 0.35, X_CI = 3e-5) and from the continuum; [CI], CO(2-1) and continuum fluxes | no CO-based mass column (CO flux only) |
| Kirkpatrick+19 arXiv:1905.11417 (`kirkpatrick2019_z2_CO_dust.csv`) | 12 | 1.65-2.93 | L'_CO(1-0), L_850, M_mol,CO, M_mol,RJ, M*, SFR, T_cold, M_dust | **alpha_CO = 6.5 is adopted for both, and the RJ method is calibrated to CO with that value, so the two masses are not independent** (the paper tests consistency of the ratio) |
| SMGs, arXiv:2404.05596 (`smg_CI_CO_3mm_arxiv2404.05596.csv`) | 20 | 2.26-4.78 | I_CI, L'_CI, M_gas,[CI] (X_[CI] = 5.1e-5), L'_CO(1-0) (some estimated from mid-J CO), L_IR, S_3mm | no CO mass and no dust mass column; masses would need a conversion choice |
| SPT lensed DSFGs, arXiv:2306.03153 (`spt_dsfg_CI_CO_CII_fluxes_arxiv2306.03153.csv`) | 29 | 1.87-4.80 | [CI](1-0), [CI](2-1), CO(7-6), [CII] fluxes | flux table only; per-galaxy masses are not tabulated (the paper's cross-calibration tables give means and slopes) |
| Dunne+2022 arXiv:2208.01622 (`dunne2022_SampleT_counts.csv`) | 407 | 0-6 | per-sample counts only: high-z SMG 89 CO / 42 [CI] / 114 sub-mm; Local SF 35/19/35; (U)LIRGs 85/19/114; z = 1: 11/18/9; z = 0.35: 12/12/12; 0.04 < z < 0.3 (VALES): 48/0/54; calibration samples: dust+CO+[CI] 101 (90 high-L_IR), CO+[CI] 109 (97), dust+[CI] 140 (128), CO+dust 326 (240) | **the paper has no per-galaxy table** (TeX has none; the data come from the cited surveys). Calibrations: alpha_CO 4.0, alpha_CI 17.0, alpha_850 6.9e12 W/Hz/Msun, X_CI 1.6e-5, T_mw 23-30 K |
| singles (`singles_multitracer_galaxies.csv`) | 4 | 2.33-4.26 | PKS 0529-549 ([CI], CO, dust; Table 5), Q1700-MD94 (CO, dust, [CI]), D49 (CO, [CI], dust), J081740 (CO, FIR, [CII]) | stated masses and conversions in the file |
Not parsed: ALPINE Dessauges-Zavadsky+2020 (no per-galaxy table; 11 galaxies with [CII] and dust, values in other papers' tables), Valentino+2018/2020 (not fetched; partly inside Dunne's z = 1 sample), 2509.25167 (Vz-GAL, a 40 MB source), 2508.09951, 2301.12976; they would add tens of galaxies.

## 5. Counts
**Galaxies with >= 2 tracers measured, from per-galaxy tables now on disk, by redshift** (all sets above plus NOEMA3D; SPT fluxes included, Dunne counted only as sample sizes):
| set | N | z<1 | 1-2 | 2-3 | 3-5 | >5 |
|---|---|---|---|---|---|---|
| Stripe82 (CO + dust masses) | 78 | 78 | 0 | 0 | 0 | 0 |
| H-ATLAS z=0.35 (luminosities, 3 tracers) | 12 | 12 | 0 | 0 | 0 | 0 |
| Bourne+19 ([CI], CO, dust) | 10 | 4 | 6 | 0 | 0 | 0 |
| Kirkpatrick+19 (CO and RJ dust masses; not independent) | 12 | 0 | 3 | 9 | 0 | 0 |
| NOEMA3D (CO, [CI], dust; reconstructed) | 10 | 0 | 10 | 0 | 0 | 0 |
| SMGs arXiv:2404.05596 ([CI] mass, L_CO, 3 mm flux) | 20 | 0 | 0 | 6 | 14 | 0 |
| SPT DSFGs arXiv:2306.03153 (fluxes only) | 29 | 0 | 1 | 7 | 21 | 0 |
| singles (PKS0529, MD94, D49, J081740) | 4 | 0 | 0 | 2 | 2 | 0 |
| **total parsed** | **175** | **94** | **20** | **24** | **37** | **0** |

Plus abstract-level (not parsed): GN20 (z 4.06, CO + dust), REBELS-25 (z 7.31, CO + [CII]), CRISTAL-22 (dust + VLA CO(2-1)), the ACE survey (up to 17 at z 2-2.5).
**With gas MASSES from >= 2 tracers (not luminosities or fluxes only): Stripe82 78 (z < 0.2), Bourne 9 (z 0.84-1.22), Kirkpatrick 12 (z 1.65-2.93, not independent), NOEMA3D 5 validated of 10 (z 1.12-1.25, reconstructed) and the four singles: about 108 independent or semi-independent galaxies, of which about 27 are at z > 1 (Bourne 6, Kirkpatrick 12, NOEMA3D 5, singles 4).** The z > 2 sample with two independent mass tracers is small (singles 4, plus Kirkpatrick 9 that share alpha_CO) and its calibration is tested by luminosities only in the SMG and SPT sets.


## 6. Added later on 2026-09-30 (my user: "keep downloading"): Dunne+22 per-galaxy CDS catalogue and the ACE survey
**Dunne+2022 per-galaxy catalogue** (VizieR J/MNRAS/517/962 "Metal-rich galaxies dust, CO and [CI]", fetched through the VizieR ASU interface: 207,141 B, sha256 62df37b6a19b1b0e...; `multitracer_gas/dunne2022/`, script `parse_dunne2022_cds.py`). The earlier note that the paper has no per-galaxy table is superseded: **the paper's data availability statement points to CDS, and the catalogue has 408 rows** (master: z, D_L, log L_IR, log L'_CI, log L'_CO, dust flux S_cont at lambda_obs, T_d, T_mw, log L_850, K_850, sample flags SMG/MS/SLUGs/B19/VALES/S16/V20, names) **and four optimisation tables with the per-galaxy optimised conversion factors and log M_H2**: opt_dax (dust+CO+[CI], 114 rows), opt_xa (CO+[CI], 121), opt_xd (dust+[CI], 152), opt_ad (CO+dust, 335). Counts by redshift from the master table (a galaxy counts for a tracer if its luminosity or flux is tabulated):
| z bin | all sources | >= 2 tracers | all three (CO, [CI], dust) | CO + dust | CO + [CI] | [CI] + dust |
|---|---|---|---|---|---|---|
| 0-0.1 | 193 | 178 | 60 | 173 | 60 | 65 |
| 0.1-0.5 | 44 | 44 | 12 | 44 | 12 | 12 |
| 0.5-1 | 3 | 3 | 0 | 0 | 0 | 3 |
| 1-2 | 41 | 39 | 8 | 19 | 17 | 19 |
| 2-3 | 79 | 77 | 24 | 74 | 24 | 27 |
| 3-5 | 40 | 40 | 12 | 24 | 12 | 28 |
| 5-10 | 8 | 8 | 0 | 8 | 0 | 0 |
**Total: 408 sources, 389 with >= 2 tracers, 116 with all three.** Above z = 1.6 the numbers of galaxies with >= 2 tracers are in the tens (z 2-3: 77, z 3-5: 40, z > 5: 8), and with all three at z 2-3 and 3-5: 24 and 12.
**ACE survey** (ALMA Chemical Evolution Large Program, z = 2.09-2.49, CO(3-2) and Band 7 dust continuum of 25 galaxies plus one more row; arXiv:2609.21604, 2609.21072, 2609.20926, 2609.21040; `ace_*.csv`, `build_ace.py`, `ace_merged_per_galaxy.csv`): **26 galaxies, 17 CO detections and 18 dust detections (15 with both)**, with CO-based M_mol, dust masses and 12+log(O/H). Conversions: CO(3-2) to CO(1-0) with r31 = 0.77 +- 0.14 (Boogaard+2020) and a metallicity-dependent alpha_CO (the ACE calibration); dust single-band Band 7, optically thin, beta = 2.08, kappa = 0.4 m2/kg at 250 micron. The paper's own summary: mean log(M_dust/M_mol) = -2.37 +- 0.05 at mean 12+log(O/H) = 8.45 for the detected galaxies (from the dust-to-gas paper's abstract).

Nothing here is an acceleration, an a0 or a verdict. Nothing in the repo was changed except new files in `multitracer_gas/` and this note.
