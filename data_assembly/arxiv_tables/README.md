# Per-galaxy tables taken from the public TeX/FITS source of twelve arXiv papers

Built 2026-09-29 by `build.py`. The source tarballs (arxiv.org/e-print/<id>, about 125 MB in total) are kept outside the
repo in `~/new_physics/_external_data/arxiv_src/`; the exact table fragments and the two FITS files are
byte-for-byte in `raw_small/` with sha256 in `manifest.json`. Every parse is checked in `checks.txt` (all PASS).
This is how the tables the PDFs and supplements did not give became available: the papers' own LaTeX and
`extra_material/` files. No author was contacted. No fit, no derived physics.

Commented-out LaTeX (lines starting with `%`) is ignored: these files keep superseded drafts of their tables.

| output | rows | paper | holds |
|---|---|---|---|
| `msa3d_galaxies.csv` | 30 (23 golden, 7 good) | MSA-3D, arXiv:2606.27853 (JWST/NIRSpec, z 0.58-1.68) | z, RA, Dec, log M*, SFR, R_e (arcsec) |
| `msa3d_kinematics.csv` | 30 | same | inclination, PA, disk R_e (kpc), sigma0, **Vrot at R_e**, V/sigma, **f_DM(R_e)**, B/T, rotation-curve shape, each with errors and a fixed-parameter flag |
| `manceraPina2026_sample.csv` | 43 | Mancera Pina+2026, arXiv:2511.08685 (KROSS + KMOS3D, z 0.79-1.03) | z, log M*, j*, flat circular velocity V_circ,f (p16/p50/p84), V/sigma |
| `amvrosiadis_parent.csv` | 30 | Amvrosiadis+2025, arXiv:2312.08959 (ALMA CO, z 1.2-4.7) | z, CO transition, beam, log M*, **log M_gas from CO**, SFR, L_IR, class |
| `amvrosiadis_bestfit.csv` | 12 | same | r_e (arcsec), inclination, V_max, sigma, **V_circ at r = 2 r_e**, M_dyn(r < 10 kpc), with errors |
| `alpaka1_sample.csv`, `alpaka1_alma_obs.csv`, `alpaka1_properties.csv`, `alpaka1_geometry.csv`, `alpaka1_kinematics.csv` | 28 galaxies (19 kinematic disks) | ALPAKA I, arXiv:2303.16227 (ALMA CO and [CI], z 0.56-3.63) | sample and fields; ALMA line, beam, rms; M*, SFR, MS offset, L_IR, line flux and **line luminosity L'(CO or [CI])**; PA and inclination from HST and ALMA, kinematic class (D 19, U 7, M 2); for the 19 disks **V_max, mean sigma, V_ext and sigma_ext** with errors |
| `lelli2023_massmodels.csv`, `lelli2023_3dbarolo.csv` | 2 galaxies (6 model fits) | Lelli+2023, arXiv:2302.00030 (ALMA CO, zC-488879 at z 1.47, zC-400569 at z 2.24) | 3DBarolo geometry and mean V_rot; baryons-only, baryons+NFW and MOND mass models with gas, disk and bulge masses (1e10 Msun) |
| `alpaka_jwst2026_data.csv`, `alpaka_jwst2026_fiducial_fit.csv` | 3 discs (ALPAKA IDs 1, 3, 13) | arXiv:2601.03338 (JWST NIRCam stars + ALMA CO/[CI] gas, z 0.56, 1.45, 2.10) | line luminosity, SED M*, SFR; rotation-curve decomposition with free gas normalisation: dynamical stellar mass, bulge, disc, gas, halo mass |
| `cristal2025_sample.csv`, `cristal2025_kinematics.csv`, `cristal2025_dynamics.csv` | 32 galaxies; 34 kinematic rows; 14 dynamical models | ALMA-CRISTAL, arXiv:2507.11600 ([CII], z 4.41-5.69) | positions, M*, SFR, beams; kinematic class (Best Disk 7, Disk 9, Non-Disk 18) and f_molgas; DysmalPy: M_tot, R_e,disk, V_rot(R_e), sigma0, f_DM(R_e), **R_out/R_e** and R_out/beam |
| `romanoliveira2023_sample.csv`, `_gasmasses.csv`, `_kinematics.csv` | 5 sources (4 with kinematics) | Roman-Oliveira+2023, arXiv:2302.03049 ([CII] with ALMA, z 4.26-4.43: AzTEC 1, BRI1335-0417, J081740, SGP38326-1/2) | [CII] data properties; SFR and H2 masses from literature CO (7.6e10-1.9e11 Msun); V_rot,max 198-562 km/s, V_ext, sigma with errors |
| `danhaive2025_gold.csv` | 41 | Danhaive+2025, arXiv:2503.21863 (geko, JWST NIRCam grism Halpha, gold sample, z 3.8-5.8) | log M*, SFR, r_e, v/sigma0, sigma0 (many upper limits), dynamical mass; NO gas mass |
| `sharma2024_gs21b.csv` | 225 | Sharma+2024, arXiv:2406.08934 (KROSS, z 0.76-1.04) | inclination, R_e, **velocities at R_e, R_opt and R_out (about 5 R_D)**, M*, M_H2, M_HI, gas radius, quality flags |

## Cross-checks that passed
- MSA-3D: 23 golden and 7 good galaxies as the paper states; the median f_DM(R_e) of the golden sample recomputed
  from the table is 0.63, the paper's stated median; the two tables share the same 30 IDs in the same order.
- Mancera Pina: 43 galaxies as the paper states; velocity percentiles ordered for every row.
- Amvrosiadis: 12 fitted discs, all present in the 30-source parent table.
- Sharma: 225 rows, every velocity and mass finite and positive.

## What each table cannot do (read before using)
- **MSA-3D:** ONE velocity per galaxy, at R_e of the disk; no gas mass in either table (the paper's gas comes from a
  depletion-time scaling inside the dynamical model). f_DM is a model output.
- **Amvrosiadis:** the only set here with a MEASURED gas mass (molecular, from CO luminosity with a conversion
  factor) and a velocity at a STATED radius (2 r_e). It is 12 massive dusty star-forming galaxies
  (log M* about 10.5-12.3, V_circ about 250-530 km/s). Their r_e are 0.19-0.62 arcsec, and a rough estimate
  (velocity squared over 2 r_e, about 8 kpc per arcsec) puts the total acceleration at 2 r_e near ten times a0,
  so they probe the high-acceleration regime. That estimate is my back-of-envelope arithmetic, not a calculation
  in the repo. Molecular gas only (no HI).
- **Sharma:** velocities out to R_out, about 5 disk scale lengths (the outermost of any sample here). BUT the gas
  masses are NOT measured: M_H2 comes from the Tacconi+2018 scaling and M_HI from a stacked M*-M_HI relation at z~1
  (Chowdhury+2022). The median M_HI is 4.1 times the stellar mass and the median M_H2 is 0.27 times it, so the
  baryon budget at large radius is set by an assumed gas mass. The FITS has no radius column; the radii are as
  the paper defines them. 19 rows have `Rout_Flag = F`, 15 have `Mstar_flag = F`.
- **ALPAKA I:** measured cold-gas tracers (CO or [CI]) and 3D-tilted-ring rotation curves for 19 secure disks at
  z 0.56-3.63, so it is the closest high-z set to measured gas plus an outer velocity. BUT (a) the tables give the gas
  as a line luminosity L' only; a gas mass needs a conversion factor and line ratio that are not applied here;
  (b) `V_ext` is the mean of the last two radial points of each curve, and the outermost radius R_ext and the
  optical effective radius are NOT tabulated (they appear only in plots; the rotation curves are a raster PNG,
  `figures/vrot.png`), so the radius in units of R_e is not available from the tables; (c) M* is missing for IDs
  16, 17 and 24; (d) the sample is biased to massive, actively star-forming galaxies in overdense environments,
  with AGN hosts, and the paper says the velocity dispersions of ID 3, 7 and 28 (kinematic anomalies absorbed by inflating the dispersion) are upper limits;
  (e) the paper's title and abstract say z = 0.5-3.5 but the table maximum is 3.63.
- **Lelli+2023:** two ALMA CO discs at z 1.47 and 2.24 with flat rotation curves out to about 8 kpc and free-gas mass models (baryons only, +NFW, MOND with a0 = 1.2e-10). The paper itself states the curves are limited to inner
  high-acceleration regions, V_obs^2/R > 3-4 a0, so they probe the Newtonian regime; the MOND fits do not test a0 evolution.
- **arXiv:2601.03338 (three ALPAKA discs):** JWST-informed decompositions with a free gas normalisation. For ID1 (z = 0.56) the dynamical stellar mass is log 10.6, several times the pre-JWST SED value the paper quotes as too low, with log M_gas 9.6:
  the baryon budget I guessed in an earlier note for ID1 (about 1.9e10 Msun) is superseded; with the paper's numbers the baryons are about 4.4e10 Msun.
- **ALMA-CRISTAL (z 4.4-5.7, [CII]):** 3 of the 14 modelled disks reach R_out/R_e >= 3 (CRISTAL-23c 9.2, -09 3.1, -02 3.0), median 2.5, but with only 1.6-5.5 beam elements at R_out; gas is [CII]-based, V_rot(R_e) is
  the only velocity in the tables, and the paper's figures show the observed V_rot below sigma0 for several disks, i.e. dispersion-supported systems whose 'circular velocity' comes from a pressure-support correction.
- **Big Wheel (arXiv:2409.17956, z = 3.245, JWST NIRSpec + ALMA CO(4-3)), one object, numbers from the paper's Table 1:** stellar mass 3.7e11 Msun (1.7e11 with a parametric star-formation history), H2 mass from CO 1.8e11 Msun (a
  conversion factor is assumed), half-light radius 9.6 kpc, stellar disk to at least 30 kpc in diameter, H-alpha v_rot 280 km/s, circular velocity 304 km/s, sigma_int 61 km/s. The rotation velocities come from three NIRSpec slits, and the paper
  FITS a two-parameter flat (pseudo-isothermal) rotation-curve model, so the outer velocity is a model assumption; the radii the slit velocities reach are not stated in the text (they are plotted). The table is not in a file here; no calculation was made.
- **Mancera Pina:** stellar-mass sample with a flat circular velocity; no gas.
- The CRC file (`sharma2024_2406.08934_CRCs_FitsParam_Burkert.fits`, 16 rows) holds Burkert-halo fits to 16
  stacked bins (`bin_0`...`bin_15`), not to individual galaxies; it is in `raw_small/` but not parsed.
- None of these is a test of a0 by itself. Calculations belong to the calculation thread.
