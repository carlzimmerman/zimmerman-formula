# DATASETS — the new-instrument register for the equipartition law (G077)

Registered 2026-09-15. Files in `deepseek_push/data2/`, full URLs + sha256 in
`deepseek_push/data2/MANIFEST.md`. Nothing here duplicates the repo's existing
holdings (SPARC, X-COP, KiDS/Brouwer, G044 438-galaxy corpus, G051 master table).

The law under test: equipartition of the phantom — σ² = G M_b / 2 r_M (the G03g
floor), M_ph(<r_M) = M_b, v_c² = G M_b(<r)/r in the baryon-dominated interior, and
κ = σ²/v_flat² = 1/2 (G031/G03G, Lean-certified). Every lane below needs a fresh,
independently-measured instrument.

---

## D1. Simon 2019 — dwarf spheroidal compilation (the dSph floor)
- **What**: the definitive MW-satellite dSph/UFD table: M_V, r_1/2, distance,
  v_hel, σ (with full asymmetric errors), [Fe/H], per system (~70 dwarfs).
- **Who measured it**: compilation of the literature by J. D. Simon (Carnegie);
  individual σ from resolved-star spectroscopy (Keck/DEIMOS+LRIS, VLT/FLAMES,
  Magellan/MIKE+IMACS — the original papers' instruments); review data page
  maintained by the author.
- **Rows the law needs**: the rows with measured σ **and** M_V → M★ (Sculptor,
  Draco, Fornax, Leo I/II, Sextans, Ursa Minor, Carina, ... + the UFDs with
  σ≲5 km/s where the floor predicts the *upper* envelope); columns sigma ±,
  M_V ± (M★ derived with the lane's M/L), r_1/2 (for r_M = r_1/2 conversion).
- **Status**: DOWNLOADED (`simon2019_dwarf_tab_ascii_14sep2018.dat`, author's
  official ASCII of ARA&A Table 1). Citation note: **the "ApJ 884 42" ref in the
  brief is wrong** — that is Simon M. et al. 2019 (Taurus PMS stars); the
  compilation is Simon 2019, ARA&A, 57, 375 (verified via SIMBAD).
- **Lane**: the G03g dSph floor (deepseek_push, 7-dwarf σ_pred = (G M★ a₀)^{1/4}/√2,
  median log10(pred/obs) = −0.00) — re-run on the full table, and the new
  "equipartition in the UFD regime" check (σ below the isothermal floor).

## D2. Baumgardt & Hilker 2018 — globular cluster catalog (M★, σ, r_h)
- **What**: 112-cluster catalog of masses, structural parameters and velocity
  dispersion profiles; author-updated master table with 165 clusters (Mass,
  rc, rh,l, rh,m, rt, ρ_c, ρ_h,m, σ_c, σ_h,m, σ0, T_rh, MF slope, v_esc,
  mass-segregation η_c/η_h); per-cluster σ(r) profiles (CDS tabled).
- **Who measured it**: Baumgardt (UQ) & Hilker (ESO); ~15,000 new VLT/Keck RVs +
  ~20,000 literature RVs, N-body fits; distances from Baumgardt & Vasiliev 2021.
- **Rows the law needs**: every cluster with Mass and σ0 (and rh,l for the
  r_M = 2·r_h,l crossing) — the cluster analogue of the dSph floor at a NEW mass
  scale (10⁴–10⁶ M⊙, σ 1–20 km/s): equipartition predicts M_ph(<r_M) = M_b and
  σ² = G M_b/2 r_M with *no* dark component; globulars are the strong-field
  boundary (σ² ≫ G M a₀·r ... i.e. r_M ≪ r, κ → 1).
- **Status**: DOWNLOADED — CDS J/MNRAS/478/1520 (table2.dat 112 rows, tabled.dat
  σ-profiles) + author master `combined_table.txt` (165 rows) + pre-cleaned
  167-row subset (name/M/rh/σ0) found in data2 mid-session, verified bit-identical
  to the master table.
- **Lane**: the cluster section (G057 cluster table + the G03-series cluster
  lanes): σ² = GM_b/2r_M per cluster, plotted against the dSph floor.

## D3. Eilers+19 / Gaia-DR3-era — Milky Way rotation curve, 5–25 kpc
- **What**: v_c(R) with asymmetric errors, 38 bins from 5.27 to 24.82 kpc;
  v_c(R_⊙) = 229.0 ± 0.2 km/s, slope −1.7 ± 0.1 km/s/kpc. Derived from
  ~23,000 APOGEE red giants with Gaia DR2 astrometry via the Jeans equation.
- **Who measured it**: Eilers (MIT/MPIA), Hogg, Rix, Ness; data products on
  Zenodo 10.5281/zenodo.1468053 (star-level parallax catalog, downloaded) and
  Table 1 in the paper.
- **Rows the law needs**: v_c(R) over 5–25 kpc with errors — the MW equipartition
  integral: M_enc(<R) = R v_c²/G vs M_b(<R) (G031's sigma_MW = 119 km/s check and
  the G062 MW lane); the 8–12 kpc rows set the solar-circle normalization.
- **Status**: DOWNLOADED — `eilers2019_mw_rotation_curve_table1.csv` (values
  re-encoded from the published Table 1 via the arXiv HTML rendering — IOP ASCII
  export is bot-walled and no CDS catalog exists; provenance documented in
  MANIFEST) + the Zenodo FITS. Gaia-DR3 successor registered as citation
  (Zhou et al. 2023, ApJ 946, 73 — no machine-readable deposit found).
- **Lane**: G062 MW test / G031 MW row; also the rotation-curve flatness input
  for G03G's κ = 1/2.

## D4. DES-Y3 galaxy–galaxy lensing (lensing RAR instrument)
- **What**: the official DES Y3 3×2pt data vector (redMaGiC lens sample):
  `gammat` g–g lensing tangential shear (5×4 lens–source z-bin pairs × 20
  angular bins), `wtheta` clustering, cosmic shear, n(z)s, full covariance.
- **Who measured it**: DES Collaboration; measurement paper Prat et al. 2022
  (PRD 105, 083528), cosmology Amon et al. 2022 (PRD 105, 023520); released on
  the public DES server (des.ncsa.illinois.edu/releases/y3a2).
- **Rows the law needs**: the gammat bin rows (lens-bin/source-bin/angular-bin)
  → ΔΣ(R) → g_obs(R) via the Mistele exact deprojection; compare against the
  baryonic g_bar of the lens bins → the lensing RAR at 10–1000 kpc where
  equipartition predicts the phantom's mass follows M_b(<r).
- **Status**: DOWNLOADED (`des_y3_2pt_redmagic.fits`, 26.8 MB, sha256 in
  MANIFEST; MagLim twin available on the same server, not downloaded).
- **Honest scope note**: there is NO published DES-Y3 or HSC lensing-RAR paper
  (the two existing lensing RARs are KiDS-based: Brouwer+21 in repo, Mistele+24
  below). This data vector IS the DES-Y3 instrument; the lane builds the RAR.
- **Lane**: G03f lensing test (deepseek_push/g03f_lensing_test.py) — replace/
  extend the KiDS ΔΣ with the DES-Y3 vector; RAR slope + scatter at lensing radii.

## D5. Mistele+24 — the 2024 lensing RAR measurement (registered citation)
- **What**: RAR of galaxies from KiDS DR4 weak lensing with a new *exact*
  ESD→acceleration deprojection; lensing RAR to ~1 Mpc, consistent with the
  kinematic RAR; no machine-readable deposit (KiDS DR4 BRIGHT catalog is the data).
- **Who measured it**: Mistele, McGaugh, Lelli, Schombert (2024, JCAP 04, 020;
  arXiv:2310.15248) on KiDS DR4 (VST/OmegaCAM).
- **Rows the law needs**: the g_obs vs g_bar RAR relation + their deprojection
  formula (Eq. 2.3) reused for D4.
- **Status**: NOT-DOWNLOADED (no MRT; citation + method registered).
- **Lane**: G03f lensing test.

## D6. BIG-SPARC / WALLABY-DR2 (the e_N ~ 1 test)
- **What**: BIG-SPARC — ~4,000-galaxy H I rotation-curve database (APERTIF,
  ASKAP, ATCA, GMRT, MeerKAT, VLA cubes + NIR photometry), the registered path
  to the e_N ~ 1 environmental EFE split; **not yet public** (announced in
  Haubner et al., arXiv:2411.13329). WALLABY DR2 — the official ASKAP pilot
  data release: 30″ HI source catalogue (3454 rows) + kinematic models with
  full rotation curves (303 model rows: Rad, Vrot_model, e_Vrot, SD_model).
- **Who measured it**: WALLABY team (ASKAP/CSIRO; Deg, Murugeshan, Westmeier,
  Koribalski et al.); kinematic models via 3D-Barolo/FAT pipelines.
- **Rows the law needs**: per-galaxy rotation curves (Rad/Vrot/err) + the
  e_N columns (environment) — the e_N ~ 1 EFE split (registered threshold: the
  0.5-a₀ boundary, |offset| > 0.05 dex, additive-law sign). Per G044's frozen
  verdict: WALLABY DR2 max e_N ≈ 0.119 → the split is NOT yet enabled; the
  official tables now allow the Tier-2 cross-check at the source level.
- **Status**: WALLABY DR2 DOWNLOADED (CADC TAP, anonymous; CASDA portal needs
  login); BIG-SPARC NOT-DOWNLOADED (pre-release).
- **Lane**: G036/G044 EFE and radial-scatter lanes (Tier 2, never pooled).

## D7. 2024–2026 RAR/BTFR papers — data tables
| paper | data | status | lane |
|---|---|---|---|
| Vărășteanu et al. 2025, MNRAS 541, 2366 (MIGHTEE-HI RAR, arXiv:2504.20857) — 19 HI-selected galaxies z ≤ 0.08, resolved M★ from 10-band SEDs, σ_int = 0.045 ± 0.022 dex | `mightee2025_rar_galaxy_sample_table5.csv` (19 rows: z, i_opt, log M★, Υ★); per-ring g_obs/g_bar only in figures | sample table DOWNLOADED; per-ring NOT machine-published | G040 RAR offset decomposition / RAR slope lanes (z-evolution check on a₀) |
| Apertif AWES (A&A 2026, aa61305-26): HI rotation curves + mass–size for 568 galaxies | aanda.org PDF bot-walled; CDS code not yet locatable | NOT-DOWNLOADED | BTFR/mass–size context (future Tier-2-like sample) |
| Sofue 2025 PASJ URC2026 (MW RC, nucleus→halo) | PDF only (ioa.s.u-tokyo.ac.jp), no MRT | NOT-DOWNLOADED | MW RC cross-check for D3 |
| Mistele+24 (JCAP 2024) | see D5 | NOT-DOWNLOADED | G03f |

---

## How the set covers the law
- **dSph floor** (D1): σ_pred = (G M★ a₀)^{1/4}/√2 vs σ_obs — deep-MOND phantom,
  zero free parameters.
- **Globulars** (D2): same relation at the strong-field boundary (r_M ≪ r_h) —
  M_ph(<r_M) = M_b with no dark component, σ² = GM_b/2r_M.
- **MW** (D3): the flat 5–25 kpc v_c and the equipartition integral (κ = 1/2,
  σ_MW = 119 km/s).
- **Lensing** (D4+D5): the phantom's mass follows M_b to ~1 Mpc — the RAR at
  lensing radii from DES Y3 (new) and KiDS (in repo).
- **e_N ~ 1** (D6): the environmental split — still out of reach (registered
  honestly); BIG-SPARC is the path; WALLABY official tables give the Tier-2
  cross-check.
- **Fresh RARs** (D7): 2025 MIGHTEE-HI (resolved-M★ RAR) + 2024 lensing RAR.