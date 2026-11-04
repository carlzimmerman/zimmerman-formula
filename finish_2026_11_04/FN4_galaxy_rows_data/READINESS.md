# FN4 readiness: the four galaxy rows, what has been tried and which data could move each (2026-11-04)

Item 4 of the finish push. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings: canonical a0 = 9.3603e-11 m/s², alt 1.1312e-10. Paths are relative to the repository root; `../_external_data/` is the folder beside it. Sizes come from HEAD requests or archive listings made today. Where a host did not answer, the size is marked "not obtained"; nothing is guessed in its place. No file was downloaded.

**Hosts that did not answer from this machine today:** things.cv.nrao.edu (the LITTLE THINGS HI cubes; ports 80 and 443 time out), CDS/VizieR at cdsarc and vizier.cds.unistra.fr, and its Harvard mirror (empty replies). RT1 met the same CDS timeouts on 10-28.

## 1. IC 1613: the law over-predicts (E −0.593, Z −7.9 canonical; −0.631, Z −8.42 alt)

**Tried**
| Lane | Commit | Label or result |
|---|---|---|
| HO3 | 1cf7d31d67 | stellar σ at r₁₂: E −0.535 (Z −6.75) |
| RT1 | 66c45c5082 | OVER-PREDICTED ON ROTATION: Oh+15 V(R_max) at their fixed i 48° |
| FD1 | 36b861cb74 | on-disk data close about half the gap; IC 1613 STANDS |
| IN1 | 362f0cf8f2 | consistent only if i 18.5–26.5° |
| IN2 | 5ce49c460e | MUSE stellar i 36 ± 11, 32 ± 11: REMAINS A FAILURE, disfavoured not excluded |
| RF2 | 5c949e3bd7 | FAILS under every halo-free inclination; IN1's band keeps 9–14 % probability |
| UX4 | d4679a8f69 | inclination or nothing: everything else moves E less than 48° → 38° does; with a 15 % velocity error, Z −2.35 / −2.83 at RF2's centrals |
| CZ1 Part D | 57cae09cc8 | Local Group external field 3.4e-4 a0, shift 1e-5 dex: lever closed |
| RS1 | 36742f590f | needs a negative source |
| NV2 | 472328c26c | no external-field estimate (no SPARC alias) |

**Inputs that could move it**
| Input | What it could move | On disk | Download (file; source; size) |
|---|---|---|---|
| HI cube, natural and robust weighting | inclination from the velocity field itself; non-circular motions; pressure support; beam smearing; the 1D curve's slow rise (Taibi+24 put it on HI holes) | no (only Oh+15 tables: `../_external_data/little_things_oh2015/`) | `IC1613_NA_ICL001.FITS`, `IC1613_R_ICL001.FITS`; http://things.cv.nrao.edu/littlethings/ic1613/HI/ (named on https://science.nrao.edu/science/surveys/littlethings/data/ic1613.html); **size not obtained, host times out** |
| HI moment maps | gas surface density map (×1.33); RF2's footprint ellipticity from the FITS, not a rendered figure | no | `IC1613_NA_X0_P_R.FITS`, `IC1613_NA_XMOM1.FITS`, `IC1613_NA_XMOM2.FITS` (and `_R_` versions); same host; **size not obtained** |
| Optical images | a stellar mass map, so the baryons need not be smooth | no | `ic1613v.fits` 10,082,880 B; `ic1613b.fits` 10,082,880 B; `ic1613u.fits` 3,824,640 B; `ic1613_ubvcalib.txt` 1,881 B; https://science.nrao.edu/science/surveys/littlethings/data/ic1613/ |
| Hα image | ionised gas, minor | no | `ic1613ha.fits` 5,273,280 B, same folder |
| Spitzer 3.6 µm | old-star mass map | no | IC 1613 is not in LVL (IRSA `SPITZER/LVL/images/irac/` listing checked); a Spitzer Heritage Archive search would be needed |
| MUSE per-star velocities (Taibi+24) | a stellar velocity field across the disc, an inclination with less than ±11° | the paper's TeX only (`_external_data/ic1613_muse2024/`) | no data statement in the TeX; VizieR unreachable; **not found** |
| Distance, stellar mass | already bracketed (UX4: ±10 % distance, M★ = 0 move E by < 0.1) | yes | none |
| An independent inclination better than ±11° | the deciding number (IN1's falsifier) | | **new observations** (a wide-field stellar velocity map, or deep star-count isophotes with radius) |

The cube model is lane **FN4a** (the council's CW7), criteria frozen; it runs on the owner's yes for the cube and moment maps.

## 2. Local Group dwarfs and ultra-faints: they want more gravity than the law

**Tried**
| Lane | Commit | Label or result |
|---|---|---|
| X1 | c74c622229 | hosted recount on LVD: bright M31 +0.39 even on the published recipe |
| Z2 | 14be14f282 | satellite systematics: binaries vs physics not separated |
| UX4 | d4679a8f69 | FAILURES STAND; the EFE predicts a host-field slope (−0.75) the data lack (−0.05 ± 0.20) |
| LW1 | afcf01fc96 | Dw FAIL both footings; with the EFE the ultra-faint median is +1.30 (Z +6.76) |
| CFG821 | ac7002034a | classical dSphs about 2× above even the unscreened law |
| CZ1, CW3 | 57cae09cc8, 5540d45cb5 | Newtonian host field in ν: item 8 moves (MW +0.641 → +0.372, M31 +0.294 → +0.106), label holds |
| KT15–KT32, CZ5 | 528285bafe | filters pass the dwarfs but every filter form fails Cassini on the 3D field |
| NV1, NV2 | e5371291f9, 472328c26c | basin mass moves dwarfs but breaks SPARC holdouts; no external-field estimate for the Local Group |
| RS1 | 36742f590f | the ultra-faints are a wall for every source form |

**Inputs that could move it**
| Input | What it could move | On disk | Download (file; source; size) |
|---|---|---|---|
| Local Group external field from a catalogue | E1 for field dwarfs and satellites, which NV2 could not compute; the sign test | **yes**: UNGC (`real_research/data/ungc_karachentsev2013.tsv`, 869 galaxies with K luminosity, HI mass, distance, tidal index); LVD (`real_research/data/dsph/lvd_dwarf_*.csv`); X1's per-system residuals (`rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv`) | none |
| Multi-epoch velocities (binaries) | the ultra-faint dispersions (UX4: binaries can make about half the uncorrected dex, not the data) | partial: Walker multi-epoch for 6 systems (UX4) | literature tables on VizieR, **size not obtained**; for most ultra-faints, **new observations** |
| M31 satellite per-star velocities | membership and binaries for M31 others (5 systems) | summary only (`real_research/data/dsph/collins2013_m31_dsph.tsv`) | Collins+13 J/ApJ/768/172, Tollerud+12 J/ApJ/752/45 on VizieR; **size not obtained** |
| Satellite proper motions | pericentres, so tides are computed rather than bracketed | MW: in LVD for many; M31: none | Gaia EDR3 tables (e.g. Battaglia+22 J/A+A/657/A54), **size not obtained**; M31 satellites: **new observations** |
| A spectroscopic isolated ultra-faint | the environment test UX4 says no on-disk class can make | | **new observations** |

**FN4b** (Local Group external field from UNGC + MW + M31) needs no download. Its criteria are frozen; it can run now.

## 3. Milky Way vertical force: the law's K_z sits above Bovy & Rix

**Tried**
| Lane | Commit | Label or result |
|---|---|---|
| X5 | 7d0b1d93c0 | FEASIBLE (wide priors only); every passing cell K_z(R₀) 76.7–80.9 against 66.4 ± 2.2 |
| UX5 | 53a7e55b76 | K_z FAILURE SURVIVES on AQUAL and QUMOND |
| RF1 | 522130ed18 | UNDETERMINED: no halo-free bulge mass on disk; the decider is the disc scale length |
| UR3 | b703359758 | SPLIT |
| LW1 | afcf01fc96 | form A INFEASIBLE; form R 1 (canonical) and 6 (alt) in-prior cells; every one misses the K_z scale length (3.30–3.38 against 2.72 ± 0.15 kpc) |
| KT13 | 2f922d7bd7 | NO KERNEL IN FAMILY: K 75.0–76.3 at the v_c line |
| KT18, KT22 | 42831c5e54, dc6511c3be | star-count share 0.12: 0 of 450 cells; alt passes at share 0.20 (9 cells) |
| CZ5 | 528285bafe | no filter form survives |
| OD1 | 2ed2a097ed | DiskMass old-star dispersions NOT SEPARATED |

**Inputs that could move it**
| Input | What it could move | On disk | Download (file; source; size) |
|---|---|---|---|
| K_z(R₀, 1.1 kpc) measured without a Newtonian potential family | UX5: ≤ 71 rules out forms A and Q; ≥ 75 says Bovy & Rix's summary is wrong | Bovy & Rix 2013 table 3 (`real_research/data/mw_kz11_bovyrix2013_table3.tsv`) | pulsar accelerations exist (Chakrabarti+21, arXiv:2010.04018) with errors about 5× the kinematic ones (UX5, PROVISIONAL): **new observations** |
| Thick-disc share, measured | KT22: alt passes at 0.20, canonical needs more; star counts give 0.12, chemistry 0.26 (both web lookups, PROVISIONAL) | no | `allStar-dr17-synspec_rev1.fits` 3,970,621,440 B, https://data.sdss.org/sas/dr17/apogee/spectro/aspcap/dr17/synspec_rev1/ ; `apogee_astroNN-DR17.fits` 647,328,960 B, https://data.sdss.org/sas/dr17/env/APOGEE_ASTRO_NN/ |
| Disc scale length, read at the source | RF1: the input that matters most (−1.3σ against −5.4σ) | values from memory only | Bland-Hawthorn & Gerhard 2016 and Licquia & Newman 2016: papers, read as web pages; no data file |
| Halo-free bulge mass | RF1's undetermined row | no | Kent 1992, Dwek+95 (papers); **no data file** |
| Gas Σ_HI(R), Σ_H₂(R) | the column held at McMillan17's | Kalberla & Dedes 2008 (flaring only) | survey tables, **size not obtained** (VizieR) |
| A potential-free vertical Jeans K_z(R) from Gaia DR3 | K_z and its scale length together | no | Gaia archive ADQL query; size depends on the cut, **not obtained** |

No FN4 lane is frozen for this row. The deciding number (K_z without a potential family) is a new-observation item. The APOGEE share measurement would fit a lane, but KT22 and CZ5 already show the share only rescues alt inside a filter family that fails Cassini.

## 4. KiDS isolated-lens lensing: the law about 0.09 dex short

**Tried**
| Lane | Commit | Label or result |
|---|---|---|
| KN1, BL1 | a42ae32a01, 9b7b3bc8fc | LAW on both mass choices; blue lenses need no halo-mass shift |
| LE1 | 17574fce14 | ESTIMATORS DISAGREE, NO DEFECT: the law short under every grader |
| CX1 | 1cba79837d | no gradable collision; the flag rests on one lensing radius |
| CW6 | b01c37cdc7 | GAP UNCHANGED with measured kSZ gas; red 1.31 / 1.20, blue 0.88 / 0.80 |
| NV2, LAM1 | 472328c26c, 53d1be5347 | isolated-lens rebuild FAILED (486,584; 554,316) |
| **FN4c** | 7f4f3e98ce and after | **REBUILD MATCHES** (255,052, −1.7 %; −0.1 % with LePhare-rebuilt flux scale); **GAP STANDS** on both footings (A1 +0.085 / +0.046 dex) |

**Inputs that could move it**
| Input | What it could move | On disk | Download (file; source; size) |
|---|---|---|---|
| Brouwer+21's lens sample | per-lens inputs for any lensing lane | **rebuilt** (FN4c, `cache/fn4c_lenses.npz`, gitignored) | none |
| MAG_GAAP_r for all 1.24 M bright rows | the exact flux scale (FN4c's one stand-in) | for 3.7 % of rows, from the shear catalogue | ESO TAP, table `KiDS_DR4_1_ugriZYJHKs_cat_fits`, columns RAJ2000, DECJ2000, MAG_GAAP_r for MAG_AUTO < 20.5; **a query, no file to HEAD**: about 30 MB by CFG722's fetch (110 MB for 13 columns of 1.545 M rows). FN4c's V8 says it would change little |
| Spectroscopic isolation | the photo-z contamination B21 puts at about 30 % beyond 0.3 Mpc | DESI DR1 BGS (`../_external_data/desi_dr1_bgs/`, 5.19 GB); GAMA DR4 G09 masses (`../_external_data/gama_dr4_gkv/`) | GAMA DR4 G12, G15 by the same TAP query as G09 (73,648 rows, 11,899,298 B for G09); about 24 MB more |
| Hot gas around the lenses | CW6 used measured kSZ; the gap did not move | yes (`../_external_data/desi_dr2_ksz_zenodo`, `act_dr6_nilc`) | none |
| Per-lens lensing weights from the shear catalogue | FN4c's modelled weights (K7 shows the model moves Z by at most 0.015) | the 17.7 GB catalogue is on disk | none; a long single pass, not run |
| Gas-dominated lenses (CY6) | a lensing a0 that stellar M/L hardly moves | ALFALFA α.100 (`../_external_data/alfalfa_sdss/`), FASHI DR2 (`_external_data/fashi_dr2_2026_10_18/`), KiDS-1000 shear (on disk) | none for stage 0 or stage 1 |

## 5. The council's two extra items, taken under FN4 ids
| Item | FN4 lane | Data | State |
|---|---|---|---|
| CY4, Local Group discs weighed by star counts (M31, M33, Clouds, NGC 6822) | **FN4d**, criteria frozen | resolved-star mass or SFH maps and HI curves. On disk: none. PHATTER (M33) on MAST: per-brick photometry 574,197,120 B each (brick b01-ne), F814W mosaic 5,278,852,800 B, F160W mosaic 1,791,043,200 B, https://archive.stsci.edu/hlsps/phatter/ . Published maps and HI curves (Lewis+15, Lazzarini+22, Chemin+09, Corbelli+10, Corbelli+14) are VizieR tables, **size not obtained** | needs the owner's yes |
| CY6, lensing on HI-selected lenses | **FN4e**, criteria frozen | all on disk | stage 0 (counts and σ(a0) forecast) can run now |

## Downloads for the owner
| For | File | Source | Size |
|---|---|---|---|
| FN4a | `IC1613_NA_ICL001.FITS`, `IC1613_R_ICL001.FITS`, `IC1613_NA_X0_P_R.FITS`, `IC1613_NA_XMOM1.FITS`, `IC1613_NA_XMOM2.FITS` | http://things.cv.nrao.edu/littlethings/ic1613/HI/ | not obtained: host unreachable today |
| FN4a | `ic1613v.fits`, `ic1613b.fits`, `ic1613_ubvcalib.txt` | https://science.nrao.edu/science/surveys/littlethings/data/ic1613/ | 10,082,880 + 10,082,880 + 1,881 B |
| FN4c (optional) | MAG_GAAP_r for KiDS-bright | ESO TAP `KiDS_DR4_1_ugriZYJHKs_cat_fits` | query, about 30 MB (estimate) |
| FN4c (optional) | GAMA DR4 G12, G15 stellar masses | datacentral.org.au TAP, as `../_external_data/gama_dr4_gkv/FETCH_LOG.md` | about 24 MB (estimate from G09) |
| Milky Way (no lane) | `allStar-dr17-synspec_rev1.fits`, `apogee_astroNN-DR17.fits` | data.sdss.org DR17 | 3,970,621,440 B; 647,328,960 B |
| FN4d | PHATTER HLSP products; published SFH maps and HI curves | MAST hlsps/phatter; VizieR | 0.57 GB per photometry brick; VizieR sizes not obtained |

## New observations, not downloads
An IC 1613 inclination better than ±11°; multi-epoch spectroscopy of most ultra-faints; a spectroscopic isolated ultra-faint; M31 satellite proper motions; K_z(R₀) without a potential family to about ±3.

κ = ½ FITTED. Not theory closed.
