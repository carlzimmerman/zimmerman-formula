# DATA2 MANIFEST — G077 new-dataset expedition (registered 2026-09-15, 22:05 EDT)

Every row: official public URL, sha256 of the local copy, size, citation, status.
Status: DOWNLOADED (byte-verified) | NOT-DOWNLOADED (reason).

All local files live in `deepseek_push/data2/`. No file here duplicates the repo's
existing SPARC, X-COP, KiDS/Brouwer, G044-corpus or G051-master-table holdings.

---

## (1) Simon 2019 — dwarf spheroidal compilation (sigma–M★ tables)

| field | value |
|---|---|
| URL | https://users.obs.carnegiescience.edu/jsimon/data/dwarf_tab_ascii_14sep2018.dat |
| local | `simon2019_dwarf_tab_ascii_14sep2018.dat` |
| sha256 | `fffe4faefc547bd6c1e2b4d82e51d159f6f96ad7b452f37e73a1279f1d91146f` |
| size | 15392 B |
| status | DOWNLOADED |
| citation | Simon, J. D. 2019, ARA&A, 57, 375, "The Faintest Dwarf Galaxies" (arXiv:1901.05465), Table 1 machine-readable version, official author data page (users.obs.carnegiescience.edu/jsimon/data.html). |

**Citation correction (verified via SIMBAD, 2026-09-15):** the task brief's "ApJ 884,
42" is NOT the dSph compilation — ApJ 884, 42 (2019) is Simon M., Guilloteau S.,
et al., "Masses and implications for ages of low-mass pre-main-sequence stars in
Taurus and Ophiuchus". The sigma–M★ dSph compilation is the **ARA&A 57, 375**
review (J. D. Simon); its Table 1 (M_V, r_1/2, Dist, sigma, [Fe/H], all with
asymmetric errors) is the file above. M★ is not a column — the lane derives it
from M_V with its standing M/L convention (G03g precedent: 7 dwarfs, median
log10(pred/obs) = −0.00). Companion IDL file (same data): data/dwarf_struc_14sep2018.sav (not downloaded).

## (2) Baumgardt & Hilker 2018 — globular cluster catalog (M★, sigma, rh)

| field | value |
|---|---|
| URL (2018 release) | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/478/1520/ (table2.dat, tabled.dat.gz, ReadMe) |
| local | `bh2018_cds_table2.dat` sha256 `86c5a8612789c2430551277c3b9a820b70e3e6e78456950dd13525872ce9b13e` (14000 B, 112 clusters) |
| local | `bh2018_cds_tabled.dat.gz` sha256 `30c3cf5896dfcb31a7678a4eb395cc6350c2ff19dcf2e5e7b4873cedfcc94666` (373893 B) + gunzipped `bh2018_cds_tabled.dat` sha256 `9deaeb5522c5b60fdd247493bc2f71a7cea1c62c03b26d76f5b9ceddc79b76da` (1435961 B, velocity-dispersion profiles) |
| local | `bh2018_cds_ReadMe` sha256 `3c68377843f7d14ec88dfeffd51e0c2e27d36cb272c797e0cffde94a9c022598` (7208 B) |
| URL (updated master) | https://people.smp.uq.edu.au/HolgerBaumgardt/globular/combined_table.txt |
| local | `baumgardt_combined_table.txt` sha256 `783099d2ed825991b41d0c5f0c08d4ddf462b3b64e69984988aabd155c9ed7cc` (49192 B; 165 clusters; Mass, rc, rh,l, rh,m, rt, rho_c, rho_h,m, sig_c, sig_h,m, sig0, Trh, MF slopes, vesc, mass-segregation etac/etah). |
| local | `bhv4_parameters_2023.csv` sha256 `32420f1f451cc5ea3aaa691eefbc0513f205f64ada5052c36e92ec3d78d1eb33` (5648 B; 167 rows name/M_Msun/rh_pc/sigma0_kms). Found in data2 during this session (created 21:57 by a parallel process, NOT this session); values verified bit-identical to combined_table.txt cols (10)/(17)/(31) for every row. |
| status | DOWNLOADED (CDS 2018 release + author master table). |
| citation | Baumgardt, H. & Hilker, M. 2018, MNRAS, 478, 1520 (arXiv:1804.08359); updated parameters per the author's globular-cluster pages (Baumgardt et al. 2019–2023 series: distances, M/L_V, mass functions, sigma0). |

## (3) Milky Way rotation curve, 5–25 kpc, v_c with errors

| field | value |
|---|---|
| URL (v_c table) | https://arxiv.org/html/1810.09466v2 — published Table 1 rendered (IOP ASCII export bot-walled: iopscience.iop.org/article/10.3847/1538-4357/aaf648; CDS catalog J/ApJ/871/120 does NOT exist; author Zenodo deposit holds only the star-level catalog, see below) |
| local | `eilers2019_mw_rotation_curve_table1.csv` sha256 `3f7027904a9b56bed2c5c936e6731eba719969a531ce1cf3c8a810fcb1691f32` (922 B; 38 rows: R[kpc], v_c[km/s], sigma_vc−, sigma_vc+, 5.27→24.82 kpc; values extracted from the published Table 1, double-verified identical across arXiv HTML and ar5iv renderings; R=8.19 → 228.86 km/s, matches v_c(R_⊙)=229.0±0.2) |
| URL (official data deposit) | https://doi.org/10.5281/zenodo.1468053 |
| local | `eilers2019_zenodo_spectrophotometric_parallaxes.fits` sha256 `ee5e5f103174ca6c191fd307c542ab2a000d83c988806dd70f3e9c2b04234bfe` (2649600 B; the 23k-star spectrophotometric-parallax catalog the RC rests on) |
| status | DOWNLOADED (v_c table re-encoded from the publisher table via arXiv HTML; note this provenance — it is the published numbers, not a publisher-file byte copy) |
| citation | Eilers, Hogg, Rix & Ness 2019, ApJ, 871, 120 (arXiv:1810.09466); Hogg, Eilers & Rix 2018/2019, Zenodo 10.5281/zenodo.1468053. Gaia-DR3-era successor with the same 5–25 kpc range: Zhou et al. 2023, ApJ, 946, 73 (no CDS/arXiv MRT found; registered as citation). |

## (4) DES-Y3 galaxy–galaxy lensing (RAR instrument)

| field | value |
|---|---|
| URL | https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits (official DES Y3 data-release server; also des.ncsa.illinois.edu/releases/y3a2) |
| local | `des_y3_2pt_redmagic.fits` sha256 `a72a8ee02fa72474ad859edab27d946991901e3d9a5bdc95cc9a961b244a32a6` (26789760 B; 1008 HDUs: `gammat` = galaxy–galaxy lensing tangential shear, 400 rows = 5 (redMaGiC lens z-bins) × 4 (source bins) × 20 angular bins, plus wtheta clustering, xip/xim cosmic shear, nz distributions, full 900×900 covariance) |
| status | DOWNLOADED |
| citation | Prat et al. 2022, PRD, 105, 083528 (DES Y3 g–g lensing measurement); DES Collaboration (Amon et al.) 2022, PRD, 105, 023520 (Y3 3×2pt). MagLim twin: `2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits` on the same server (not downloaded). |

**Honest scope note (verified by search, 2026-09-15):** no published DES-Y3 or HSC
*galaxy–galaxy lensing RAR measurement* exists to date (the two lensing-RAR
papers in the literature are KiDS-based: Brouwer et al. 2021, in repo, and Mistele
et al. 2024, registered below). The DES-Y3 instrument registered here is therefore
the official Y3 ΔΣ/gammat data vector itself, which the G03f lensing lane can
convert to a lensing RAR with the Mistele deprojection.

## (5) BIG-SPARC / WALLABY-DR2 (e_N ~ 1 test instruments)

| field | value |
|---|---|
| BIG-SPARC URL | https://arxiv.org/abs/2411.13329 (IAU Symp. 392 proceedings; database announced, rotation curves "will be provided" — NOT yet public as of 2026-09-15) |
| status | NOT-DOWNLOADED — dataset not released; registered for the e_N ~ 1 lane. |
| citation | Haubner, K., Lelli, F., Di Teodoro, E., Schombert, J., McGaugh, S. 2025, arXiv:2411.13329 (BIG-SPARC: The new SPARC database) |
| WALLABY DR2 URL | https://wallaby-survey.org/data/data-pilot-survey-dr2/ (catalogs via CASDA DOI 10.25919/7w8n-9h19 kinematic / 10.25919/qw7w-tn96 30″ source / 10.25919/47tr-k441 12″ source; CADC TAP table `cirada.Wallaby_dr2_kinematic_catalogue`) |
| local | `wallaby_dr2_kinematic_catalogue.tsv` sha256 `0c4cdde4d8eb0f92cfc37f95c8bacf4c44de4d35a71425ee35a63758889a9c4e` (179306 B; 303 rows — full official DR2 kinematic-model table: per-galaxy comma-separated Rad/Vrot_model/e_Vrot/SD_model ring arrays, incl. PDR1+PDR2 models) |
| local | `wallaby_dr2_source_catalogue.tsv` sha256 `246829bd0a2ce67096ec76cf6cc047d737383b1db90ef4b470c4485684eed5f8` (2145478 B; 3454 rows — official DR2 HI source catalogue, 30″) |
| status | DOWNLOADED via anonymous CADC TAP (ws-uv.canfar.net/youcat/sync); CASDA web portal requires login, CADC TAP works anonymously. |
| citation | Murugeshan et al. 2024, PASA, 41, e088 (WALLABY PDR2, arXiv:2409.13130); Koribalski et al. 2020, Ap&SS, 365, 118; Westmeier et al. 2022, PASA, 39, E058; Deg et al. 2022, PASA, 39, E059. |

Registry context (G044, frozen 2026-09-14): WALLABY DR2 max e_N ≈ 0.119 vs the registered 0.5-a₀ boundary — the e_N ~ 1 EFE split is NOT yet enabled by any public sample; BIG-SPARC is the registered path to it.

## (6) 2024–2026 RAR/BTFR papers — data tables

| paper | artifact | status |
|---|---|---|
| Mistele, McGaugh, Lelli & Schombert 2024, JCAP 04, 020 (arXiv:2310.15248) — lensing RAR (KiDS DR4, exact deprojection) | no machine-readable deposit; relies on public KiDS DR4; | NOT-DOWNLOADED (paper data = the KiDS BRIGHT catalog; registered as citation) |
| Vărășteanu et al. 2025, MNRAS, 541, 2366 (arXiv:2504.20857) — MIGHTEE-HI RAR, 19 HI-selected galaxies z≤0.08, resolved M★, sigma_int = 0.045 dex | `mightee2025_rar_galaxy_sample_table5.csv` sha256 `f6e49a7cafa825237f14956c81f8862e7bf03b0094ac5048ab1230e6f6e1eff7` (1499 B; 19 rows: galaxy, z, i_opt, log10 M★, Υ★ — Table 5 of the paper; per-ring v_rot/g_obs/g_bar published as figures only) | DOWNLOADED (sample table; per-ring data NOT machine-published) |
| Apertif AWES: "HI rotation curves and mass–size relation for 568 galaxies" (A&A 2026, aa61305-26) | aanda.org/articles/aa/pdf/forth/aa61305-26.pdf (bot-walled today); CDS code unknown | NOT-DOWNLOADED (URL registered in DATASETS.md) |
| Sofue 2025, PASJ (URC2026), "The unified rotation curve of the Galaxy from the nucleus to halo" | https://www.ioa.s-tokyo.ac.jp/~sofue/news/2026_urc26_mw.pdf (PDF only, no MRT) | NOT-DOWNLOADED (PDF registered) |

---

## Total: 13 files downloaded (17 504 4 B total), 4 registrations with NOT-DOWNLOADED status + 1 open question (BIG-SPARC pre-release).