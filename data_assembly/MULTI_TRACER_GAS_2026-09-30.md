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

## 4. Compilations that would give many galaxies (per-galaxy tables NOT read; abstract or search-summary level; a parse needs my user's go)
| paper | sample | tracers | note |
|---|---|---|---|
| Dunne+2022, arXiv:2208.01622 | 407 galaxies, z 0-6 (local disks, z~0.35-1, SMGs to z~6) | CO(1-0), [CI](1-0), submm dust; Bayesian calibration: alpha_CO = 4.0, alpha_CI = 17.0, alpha_850 = 6.9e12 W/Hz/Msun, X_CI = 1.6e-5, T_mw 23-30 K | the page read shows no per-galaxy table; data may be in source or online files |
| arXiv:2306.03153 | 29 lensed SPT DSFGs | [CI], CO, [CII], dust | 6 tables; per-galaxy values implied |
| arXiv:2404.05596 | 20 unlensed DSFGs, z 2-5 | CO(1-0), [CI](1-0), 3 mm dust | abstract says no per-galaxy mass catalogue; conversion factors not dependent on z or L_IR |
| Kirkpatrick+2019, arXiv:1905.11417 | 12 galaxies, z~2 | CO(1-0) and dust | masses agree within a factor 2 |
| Dessauges-Zavadsky+2020 (ALPINE), arXiv:2004.10771 | 11 FIR-continuum-detected non-merger ALPINE galaxies with both | [CII] (Zanella+2018, 0.3 dex), 850 micron dust (T_d 41 K z<5, 43 K z>5, beta 1.8), dynamical; alpha_CO metallicity-dependent from 4.36 | no per-galaxy table in the paper; values sit in Faisst+20, Bethermin+20 and Fujimoto+20 tables |
| Valentino+2018/2020 (COSMOS z 1.1-1.7), Bourne+2019 (arXiv:1810.01640), arXiv:2111.09067 (z = 0.35), arXiv:1803.08926 (Stripe82, low z), arXiv:2305.00024 (z = 3 MS), arXiv:2109.01684 (Q1700-MD94), arXiv:2509.25167 (Vz-GAL z 1-6), arXiv:2508.09951 | not sized | CO, [CI], dust combinations | named by the search only |

## 5. Counts
Galaxies with >= 2 tracer masses obtainable NOW (local tables or stated values), by redshift:
- **z < 1: 0** (candidates only: Dunne+22 local and z~0.35-1 parts, DYNAMO, Stripe82, z = 0.35).
- **z 1-2: 10** (NOEMA3D, CO + dust); **6** of them CO + [CI] + dust; **5** with the CO reconstruction validated against the paper's Table 1 (G4_38065, G4_38232, G4_20371, GN4_24517, GN4_18574 at z 1.12-1.25).
- **z 2-3: 1 to ~18** (PKS 0529-549 at 2.57; ACE up to 17, abstract-level, masses not seen).
- **z 3-5: 3** (J081740 4.26 with three explicit formulas; GN20 4.055; CRISTAL-22, z not read).
- **z > 5: 1** (REBELS-25, 7.31; abstract-level).
- Total with numbers I can read now: 15 (10 + 1 + 3 + 1), of which only J081740 and the five validated NOEMA3D galaxies are solid; the compilations in section 4 would add tens to hundreds.

Nothing here is an acceleration, an a0 or a verdict. Nothing in the repo was changed.
