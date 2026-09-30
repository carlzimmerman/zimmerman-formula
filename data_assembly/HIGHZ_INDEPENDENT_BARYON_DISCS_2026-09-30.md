# Published discs at z > 3.5 with independent baryons (data front, 2026-09-30)

Request (orchestrator, prompted by CFG218): list every published disc at z > 3.5 with all of (i) a rotation curve or V at a stated radius, (ii) a stellar mass from SED, not from the dynamical fit, (iii) a gas mass from a measured tracer (CO, [CI], [CII] with a stated conversion, or dust).
Method: READ-ONLY. TeX sources already on disk (`~/new_physics/_external_data/arxiv_src/`), the tables already parsed in `arxiv_tables/`, and abstract pages read through a summariser (marked **abstract-level**, UNVERIFIED beyond the abstract). Nothing was downloaded. Nothing was computed except counts. No table values are restated beyond what identifies a disc. Rule used for (ii) and (iii): the input must exist **independently of the dynamical fit**; a mass that is M_dyn minus something, or a conversion factor fitted to the same kinematics, does not count.

## A. All three met by published independent inputs (8 discs, z 4.06-7.31)
| disc | z | (i) radius reached | (ii) M* source | (iii) gas tracer and conversion | table lives in | on disk |
|---|---|---|---|---|---|---|
| CRISTAL-11 | 4.439 | model/profile out to 2.9 R_e (the paper's Rout/R_e column) | SED: Li+2024 NIRCam, else Mitsuhashi+2024 | dust continuum, Scoville+2016 (T_d = 50 K, beta = 1.8, alpha_dust,0 = 6.7e19 erg/s/Hz/Msun), detection | TeX (arXiv:2507.11600) + vector figure | yes: `arxiv_tables/cristal2025_*.csv`, `cristal_vector/` |
| CRISTAL-19 | 5.233 | 1.7 R_e | same | same, detection | same | yes |
| CRISTAL-07a | 5.154 | 1.4 R_e | same | same, detection | same | yes |
| CRISTAL-02 | 5.294 | 3.0 R_e | same | same, detection | same | yes |
| CRISTAL-20 | 5.545 | 1.5 R_e | same | same, detection | same | yes |
| CRISTAL-03 | 5.689 | 2.3 R_e | same | same, detection | same | yes |
| GN20 | 4.055 | CO(2-1) disc diameter 14+-4 kpc; V_max 575+-100 km/s (Hodge+2012); NIRSpec Halpha v_rot ~500 km/s and Pa-alpha to 6 kpc (550+-40) (GA-NIFS, arXiv:2403.03192 intro) | SED, M* ~1.1-2.3e11 (Daddi09, Tan+14; JWST MIRI disc R_e 3.6 kpc) | CO(2-1): M_mol ~5-13e10 (Carilli10, Hodge12); NOEMA + radiative transfer M_mol 2.9e11 with alpha_CO = 2.8, M_dust 5.7e9 (arXiv:2510.17804, abstract-level) | Hodge+2012 HTML (arXiv:1112.3480, not read); 2403.03192 TeX | partly: TeX of 2403.03192 (intro values only) |
| REBELS-25 | 7.3065 | [CII], 0.14 arcsec = 710 pc beam; radius not extracted | BEAGLE SED 8(+4,-2)e9 (alt. 19e9, Topping+22) | **in Rowland+2024 the gas is M_dyn - M* (NOT independent)**; the separate CO paper (arXiv:2606.13393, abstract-level) detects CO(3-2) at ~3.5 sigma: M_mol = (1.0+-0.4)e11 with alpha_CO = 3, and gives alpha_[CII] = 60+-25 | Rowland TeX; CO paper HTML not read | Rowland TeX yes (2405.06025); CO paper no |

The CRISTAL discs have a caveat that the baryon mass is a fitted DysmalPy parameter; the SED M* and dust gas above exist as inputs separate from that fit. REBELS-25 is class A only if the CO(3-2) 3.5-sigma gas mass is accepted.

## B. Two of three independent, the third conditional, missing or circular
| disc / sample | z | why it is not class A | status |
|---|---|---|---|
| CRISTAL-08, -12, -15, -23b (four discs) | 4.43, 5.572, 4.58, 4.562 | SED M* yes; gas is a dust **upper limit** (continuum below threshold) | on disk |
| CRISTAL-06b, -09, -10a-E, -23c | 4.562, n/a, 5.671, 4.565 | 06b SED M* (9.19) but no dust-based gas fraction; 09 and 10a-E have no M* in the sample table; 23c has M* missing and a gas upper limit | on disk |
| J081740 (= DLA0817g, Neeleman+2020) | 4.2603 | [CII] rotation V_rot 272 km/s, extent 4.2 kpc; gas CO(2-1) M_H2 ~7.9e10 with r21 = 0.81, alpha_CO = 3.0 (also FIR and [CII]); **no SED stellar mass: only M_AB = 25.1 (near-UV)**; Roman-Oliveira+2023 says a stellar mass is still needed. GA-NIFS (arXiv:2512.05213) adds NIRSpec data, M* not found in the lines read | TeX on disk (2005.09661, 2512.05213) |
| Amvrosiadis+2025 (z >= 3.5 modelled: ALESS 065.1 z 4.445, ALESS 071.1 z 3.709) | 4.445, 3.709 | M* from MAGPHYS SED and V_circ at 2 r_e are tabulated, **but the adopted alpha_CO = 0.92+-0.36 is said to be justified 'later' by the paper's own section 'Dynamical constraints on alpha_CO'**, so it is not independent of the kinematics, and ALESS 071.1's log M* 12.31 carries the paper's 'SED possibly contaminated by an AGN' flag. 10 of the 30 parent sources are at z >= 3.5, only 2 have kinematic fits | parsed: `arxiv_tables/amvrosiadis_*.csv` |
| ALPAKA I, W0410-0913 (ID 28) | 3.63 | M* = 13e10 (SED) and V_max, V_ext tabulated (R_ext digitised); gas is a measured CO line luminosity with **no conversion applied in the paper** (ID 23, ADF22.1, z 3.09, is below the cut) | parsed + digitised on disk |
| Roman-Oliveira+2023: BRI1335-0417 (4.407), SGP38326-1 and -2 (4.4), AzTEC 1 (4.342, no kinematic fit) | 4.3-4.4 | gas from literature CO with alpha_CO = 0.8 is independent of the [CII] kinematics; **no SED stellar mass in the paper** for the kinematic sources (AzTEC 1 has ~1e11 from Yun+2015 but no kinematics) | parsed on disk |
| ALPINE rotators (Jones+2021, arXiv:2104.03099, abstract-level): 29 [CII] discs fitted, 14 robustly classified of which **6 rotators**; Corpus Z1 (arXiv:2605.25339): 31 galaxies, **8 tier-1 with per-ring rotation curves** (2-3 rings), all with SED M* (Faisst+2020); gas masses in Dessauges-Zavadsky+2020 (arXiv:2004.10771) from [CII] (with the Zanella conversion), 850 micron dust and dynamical mass | 4.4-5.9 | (iii) is [CII]-based with a stated conversion but is partly cross-checked against M_dyn; the per-galaxy gas table was not read; **overlap with CRISTAL (whose targets include ALPINE IDs) is not resolved, so these may double-count** | not on disk (Corpus Z1 is on Zenodo, DOI 10.5281/zenodo.20369285; a download needs my user's go) |
| Az9 (arXiv:2306.10450, abstract-level) | 4.274 | one low-mass disc: SED M* 2e9 (intrinsic), [CII] half-light radius 1.8 kpc, V/sigma 5.3; the gas tracer is [CII] and its conversion was not seen | not on disk |
| ALESS 073.1 (Lelli+2021, arXiv:2102.05957, abstract-level) | ~4.76 | rotation curve needs a bulge; M* and gas sources not checked | not on disk |

## C. Fail at least one criterion (for completeness)
| object | z | why |
|---|---|---|
| SPT0418-47 (Rizzo+2020, Nature; TeX on disk) | 4.225 | **M* = 1.2e10 comes from the rotation-curve decomposition and alpha_[CII] is a fitted parameter (prior 3.8-238, best 7.3)**: fails (ii) and (iii). TEMPLATES (arXiv:2307.10115) adds CIGALE and Prospector stellar masses (abstract-level; values not seen) and calls it a merger |
| Danhaive+2025 gold sample (41 discs, z 3.8-5.8) | 3.8-5.8 | JWST Halpha kinematics and SED M*, **no gas measurement** |
| GS-9209 (GA-NIFS, arXiv:2505.06349) | 4.66 | quiescent; stellar rotation; no cold gas |
| GS5001 (GA-NIFS, arXiv:2406.10348) | 3.47 | below the cut; gas not seen |
| Big Wheel (Xu+2024, TeX on disk, arXiv:2409.17956) | 3.245 | below the cut, listed as asked: SED M* 3.7e11 (Prospector; 1.7e11 with a parametric SFH), CO(4-3) L = 1.3e8 Lsun with an assumed alpha_CO (H2 1.8e11), but the rotation curve is a model assumption (flat), radius not stated |
| Lelli+2023 (two ALMA CO discs, arXiv:2302.00030) | 1.47, 2.24 | below the cut (parsed: `arxiv_tables/lelli2023_*.csv`) |

## Counts
- **Class A (all three independent): 8 discs**, by redshift: z 3.5-4.5: 2 (GN20 4.06, CRISTAL-11 4.44); z 4.5-5.5: 3 (CRISTAL-07a 5.15, -19 5.23, -02 5.29); z 5.5-6: 2 (CRISTAL-20 5.55, -03 5.69); z > 7: 1 (REBELS-25). **By gas tracer: dust 6 (all CRISTAL), CO 2 (GN20; REBELS-25 via its 3.5-sigma CO(3-2))**; [CII]-with-conversion 0, [CI] 0.
- **Class B (one criterion conditional): at least 20 discs**: CRISTAL gas upper limits 4, CRISTAL without a usable M* or gas 4, J081740 1 (no SED M*), Amvrosiadis 2 (circular alpha_CO), ALPAKA 1 (no conversion), Roman-Oliveira 3 (no M*), ALPINE rotators 6-8 (gas [CII], overlap unresolved), Az9 1, ALESS 073.1 1. Gas tracer of B: CO 7 (J081740, Amvrosiadis 2, ALPAKA 1, Roman-Oliveira 3), [CII] ~8-10 (ALPINE, Az9, ALESS 073.1), dust upper limits or no dust gas 8 (CRISTAL).
- The calc thread's 'CRISTAL 9 already parsed': my count of CRISTAL discs with an SED M* and a dust-**detected** gas mass is **6** (02, 03, 07a, 11, 19, 20); with upper limits added (08, 12, 15, 23b) it is 10. **Which nine the calc thread uses needs reconciling.** CFG218's ~13 discs is therefore reachable only if the CRISTAL upper limits, GN20, REBELS-25 (CO) and the two-of-three sources are allowed; with strict class A it is 8.

## Not done, needs my user's go
Downloading Corpus Z1 (Zenodo) or the per-galaxy gas tables of Dessauges-Zavadsky+2020 and Jones+2021; reading GN20's Hodge+2012 table and the REBELS-25 CO paper HTML for the radii and the exact M* and gas values; none was fetched.
