# Systematic Audit of Every Z² Calculation on Open-Source Data

**Date:** 2026-06-01 · **Scope:** all repo Python scripts that pull or process real
open-source observational data (cosmology, galaxies, GW, biology, meteorology).
**Method:** six parallel forensic auditors crawled the clusters read-only; the four
most consequential claims were then re-verified by hand (file:line below). Nothing
in the repo was modified.

---

## Bottom line (one paragraph)

**The data is real; the analyses are not evidence.** The repo genuinely downloaded
and stored large real datasets (Planck SMICA 2 GB, DESI DR1 LRG 2.1 M galaxies,
SDSS DR16Q 750 k quasars, El-Badry Gaia wide binaries 1.4 GB, the real SPARC
175-galaxy database, RCSB PDB, ChEMBL, NOAA hurricane recon, ERA5, LIGO strain
1.6 GB, KMOS3D). But across **~45 audited analysis scripts, every defensible
real-data measurement returns a NULL or *falsifies* a Z² claim**, and **every
reported "detection/support" traces to one of five artifacts**: (1) synthetic data
dressed as real, (2) circular self-injection (generate data from the model, then
"recover" it), (3) hardcoded/cited significances, (4) a catastrophic units bug, or
(5) unpenalized look-elsewhere. The single empirical anchor that is real and sound
— SPARC → a₀ ≈ 1.14×10⁻¹⁰ — is just the 40-year-old Milgrom coincidence. The one
surviving *prediction* (a₀(z) ∝ E(z)) is **asserted, never measured**: its repo
"tests" run on a hand-typed mock CSV while the real KMOS3D survey file sits unused.

---

## 1. Data provenance (what is actually on disk — verified)

| dataset | on disk | real? |
|---|---|---|
| Planck PR3 SMICA map | `planck_cmb_smica.fits` (2.0 GB) | REAL |
| WMAP9 ILC | `wmap_ilc_9yr.fits` (25 MB) | REAL |
| DESI DR1 LRG clustering | `desi_data/LRG_{NGC,SGC}…fits` (198 MB, 2.1 M gal) | REAL |
| SDSS DR16Q quasars | (loaded once; 750 k in results JSON) | REAL |
| Gaia wide binaries (El-Badry) | `el_badry_wide_binaries.fits.gz` (1.4 GB) | REAL |
| SPARC rotation curves | `data/sparc_data/*_rotmod.dat` (175 galaxies) | REAL ✓✓ |
| KMOS3D high-z kinematics | `data/kmos3d/k3d_fnlsp_table_v3.fits` | REAL — **but UNUSED** ✓✓ |
| LIGO strain | `ligo_stuff/{h1,l1,v1}_strain.hdf5` (~1.6 GB) | REAL |
| PDB / ChEMBL / PubChem | live RCSB/EBI/PubChem API calls | REAL |
| NOAA EBTRK + ERA5 | `EBTRK_Atlantic_2021.txt`; ARCO-ERA5 Zarr | REAL |

✓✓ = personally re-verified (file format / contents inspected).

So: **not a fake-data problem.** The failure is interpretive and methodological.

---

## 2. Master ledger by cluster

Verdict keys: **NULL** (real data, honest null) · **FALSIFIES** (real data rejects
Z²) · **SYNTHETIC** (claim meaningless) · **CIRCULAR** (data generated from the model)
· **BUG** · **HARDCODED** (number pasted/cited, not computed) · **LEE** (look-elsewhere)
· **SOUND** (defensible) · **STUB**.

### 2a. CMB topology / parity (Planck, WMAP, DESI)
| script | data | claim | verdict |
|---|---|---|---|
| `WORK_ORDER_OO_cmb_matched_circles.py` | REAL SMICA | "5.5σ" V2↔V3 circles | **LEE** (1030 trials, wrong null) |
| `WORK_ORDER_PP_wmap_verification.py` | REAL WMAP9 | "5.8σ confirmed" | **CIRCULAR** (tests only OO's pre-picked axis) |
| `digital_twin/cmb_circles_optimized.py` | REAL SMICA | r=0.86 "3.1σ" | **CIRCULAR** (fits center to maximize r, then tests r) |
| `four_point_parity_violation.py` | **np.random** mock | parity proxy | **SYNTHETIC** + **HARDCODED** 7σ (see §3A) |
| `python_parity_odd_4pcf.py` | REAL DESI | "4.4σ asym" | **BUG** (÷ 1/√N, wrong estimator) |
| `directional_4pcf_extraction.py` | REAL DESI | 88° sep, 0.16σ | **NULL** (honest) |
| `parity_analyzer.py` | REAL map recomputed | "2.9σ" | **HARDCODED** (σ is a constant in source) |
| `planck_empirical_analysis.py` | hardcoded Dℓ | "T³ explains low-ℓ, Δχ²=12" | **CIRCULAR** (1-param fit to the one anomaly) |
| `run_encore_on_desi.py` | REAL DESI | proper 4PCF | **STUB** (`encore` binary absent — never ran) |

### 2b. Galaxy / LSS chirality, wide binaries, kSZ, voids (DESI, Gaia, Planck)
| script | data | claim | verdict |
|---|---|---|---|
| `z2_axis_test.py` | REAL DESI 300 k | z = −0.08 | **NULL / SOUND** (proper random-axis null) |
| `run_desi_chirality_test.py` | REAL DESI | 67° sep, 1.0σ | **NULL** |
| `run_desi_full_sample.py` | REAL DESI 500 k | 72° sep, 1.6σ | **NULL** |
| `prepare_full_desi.py` / `WORK_ORDER_BB_data_downloader.py` | REAL | data prep / download | **SOUND** (utilities) |
| `WORK_ORDER_AA_real_gaia.py` / `_v2.py` | REAL Gaia 1.4 GB | "16σ MOND, s≈997" | **BUG** (velocity scale ~1000×; see §3B) |
| `WORK_ORDER_AA_gaia_wide_binary.py` | synthetic | "best=Newton" | **SYNTHETIC** (MOND injected) |
| `chirality_axis_extraction.py` | synthetic mock | 0.91σ | **SYNTHETIC** (fails to recover own injection) |
| `WORK_ORDER_UU_desi_chirality_mapper.py` | REAL DESI | 50.2% RH | **OVERCLAIM** (50/50 forced for isotropy) |
| `WORK_ORDER_Z_ksz_stacking.py` | REAL SMICA @ **fake** voids | "3.0σ kSZ" | **SYNTHETIC voids** (signs flip; noise) |
| `ksz_velocity_crossmatch.py` | synthetic | "0.1% CF4 agreement" | **CIRCULAR** |
| `WORK_ORDER_Y_void_catalog.py` | np.random voids | 129 "aligned" | **SYNTHETIC** |
| `WORK_ORDER_DD_sparc_rotation.py` | **v_true=v_mond** | "MOND χ²=0.98" | **CIRCULAR** (see §3D) |
| `WORK_ORDER_FF_pantheon_h0.py` | ΛCDM mock | "resolves H₀ tension" | **SYNTHETIC** + **STUB** |

### 2c. Topological ghosts (SDSS DR16Q, JWST/MAST) — *did any pipeline detect a ghost? No.*
| script | data | result | verdict |
|---|---|---|---|
| `mast_ghost_query.py` | REAL MAST/NED/SIMBAD | all 8 null | **NULL / SOUND** |
| `WORK_ORDER_NN` spectral chain | REAL BOSS spectra | 5 candidates, **0 confirmed** (r=−0.18) | **NULL / SOUND** |
| `ghost_miner.py` | hardcoded 8 gal | ghosts at z=46–80 | **METHOD-FLAWED** (nonstandard ODE; ignores look-back) |
| `ghost_quasar_real_search.py` | synthetic fallback | 0 candidates | **NULL** (on toy set) |
| `ghost_spectral_matcher.py` (NN) | synthetic spectra | "unlikely ghost" | **SYNTHETIC** self-test |
| `multi_messenger_aggregator.py` | 4/6 np.random | aggregator | **SYNTHETIC** |

### 2d. SPARC / MOND a₀ + examples + "unsolved problems"
| script | data | claim | verdict |
|---|---|---|---|
| `sparc_mond_z2_validation.py` | REAL 175 SPARC | a₀=1.14e-10 (~5%) | **SOUND** (path now broken by reorg; ran before) |
| `analyze_full_sparc_v2.py` | REAL SPARC | RAR 0.20 dex; BTFR slope 4.00 | **SOUND** scatter; **BTFR=tautology** |
| `examples/01,04 (a₀↔H₀)` | real H₀ table | "bridges Hubble tension" | **CIRCULAR** (H₀ back-solved from a₀) |
| `examples/02 jwst_highz` | **mock CSV** | "evolving a₀ 2× better" | **CIRCULAR retrodiction** |
| `examples/07 btf_evolution` | **mock CSV; real FITS unused** | "−0.48 dex shift predicted" | **CIRCULAR** (see §3C) |
| `examples/05 el_gordo` | CSV ignored | "alleviates 6.2σ" | **OVERCLAIM** |
| `unsolved_problems/{bao,kbc_void}.py` | hardcoded obs | "5σ→2σ" | **OVERCLAIM** (fabricated E(z)^0.1 exponents) |
| `unsolved_problems/{lyman_alpha,cosmic_web}.py` | none | plots | **STUB / narrative** |
| `comprehensive_validation/*` | none | "281 problems SOLVED" | **OVERCLAIM** (hardcoded status strings) |

### 2e. Extra anomaly probes (dark flow, FRB, GW, NANOGrav, VPOS, lensing) — *all hardcoded literals; none read a file/API*
| script | data | claim | verdict |
|---|---|---|---|
| `gw_catalog_fetcher.py` | real masses, **fake positions** | boundary clustering | **NULL** (honest) |
| `radio_continuum_fetcher.py` | real sources | ORCs avoid boundaries | **NULL** (concludes *against* topology) |
| `nanograv_pta_fetcher.py` | real published GWB | "resonant box freqs" | **non-test** (resonances 11 decades off nHz) |
| `dark_flow_fetcher.py` | real bulk-flow + np.random field | "aligned <30°" | **CIRCULAR** (cube has no defined axis) |
| `multipole_alignment.py` | real Planck AoE | "27° to box axis" | **CIRCULAR** (axis undefined → guaranteed) |
| `cosmicflows4_velocity_field.py` | np.random field | "recovers bulk flow" | **CIRCULAR** (recovers injected vector) |
| `vpos_satellite_plane.py` | real MW satellites | "strongly favors MOND" | **OVERCLAIM** (0.449 < own MOND threshold 0.7) |
| `frb_catalog_fetcher.py` | real FRBs | 0.139 anisotropy | **BUG** (single M81 outlier, ÷≈0) |
| `cosmos_web_lensing.py` | np.random κ-map | "21% deep MOND" | **SYNTHETIC** |
| `jwst_lensing_fetcher.py` | **fabricated catalog** | "MOND validates 56%" | **OVERCLAIM** (contradicts own `dm_required=0`) |

### 2f. Biotech (PDB/ChEMBL/PubChem) + Meteorology (NOAA/ERA5)
| script | data | claim | verdict |
|---|---|---|---|
| `sqrt_z2_validator.py` | REAL 2583 PDB aromatic pairs | **z = −0.59σ** | **FALSIFIES** (5.789 Å below background) |
| `multi_species_resonance_audit.py` | REAL 64 proteins | 50% peak, mean 6.05 Å | **NUMEROLOGY** (±0.5 Å window; fails own 70% bar) |
| `decoy_proteome_falsification.py` | **np.random "proteins"** | "not falsified" | **CIRCULAR** (reference is Gaussian planted at Z) |
| `fda_{disease,manifold}_screening.py` | REAL ChEMBL | "drugs match Z-manifold" | **NUMEROLOGY** (0.3% hit < chance; p-hacked) |
| `empirical_vina_docking.py` / `openmm_relaxation.py` | REAL software | binding ΔG / MD | **SOUND tools, NO Z² content** |
| `m4_cftr_chaperone_docking.py` | random.choice peptides | "Ac-FF-NH2 restores CFTR" | **SYNTHETIC / OVERCLAIM** |
| `analyze_ebtrk_eye_rmw.py` | REAL NOAA 1647 obs | eye/RMW 0.581 vs 0.173 | **FALSIFIES** (p≈0, 3.4× off) |
| `z2_intensity_model.py` | real ERA5 | "Z² improves skill 64%" | **CIRCULAR** (eye_ratio hardcoded 0.18) |

---

## 3. The four smoking guns (re-verified by hand)

**A. The headline "7σ parity violation" is a pasted citation, not a measurement.**
`research/offensive_campaign/four_point_parity_results.json:43` →
`"significance_sigma": 7.0, "reference": "Philcox & Slepian (2021)"`. The code that
"finds" it (`four_point_parity_violation.py:427`) hardcodes the same. The script's own
*measurement* on data is `np.random` mock (null 0.22σ). The framework's "handed
universe" rests on someone else's number.

**B. The wide-binary "16σ MOND detection" is a units bug.**
`WORK_ORDER_AA_real_gaia_results.json` records `velocity_ratio_median.vs_newton =
1147.7` (and per-bin `ratio_z2` up to 977). Bound wide-binary orbital-velocity ratios
are ~1; the pipeline conflated full sky proper-motion velocity with orbital velocity
(plus a wrong absolute-magnitude formula). The "KS p = 4×10⁻¹⁶" is the bug, not gravity.

**C. The a₀(z) evolution — the surviving prediction — is "tested" on mock data while
the real survey file sits unused.** `examples/07_btf_evolution/run.py:127` reads the
1829-byte hand-typed `data/kmos3d_tully_fisher.csv`; the real
`data/kmos3d/k3d_fnlsp_table_v3.fits` (Übler 2019) is never opened. √(a₀/g)
monotonicity guarantees "evolving beats constant."

**D. The SPARC "MOND χ²/dof = 0.98" recovers data it generated from MOND.**
`WORK_ORDER_DD_sparc_rotation.py:277` → `v_true = v_mond(r, M_total)`; line 281 adds
noise; line 246 builds 10 synthetic galaxies — ignoring the real 175-galaxy database.
It then "fits" MOND and declares victory. Pure self-recovery.

---

## 4. What is genuinely sound (the credits)

- **SPARC a₀ extraction** (`sparc_mond_z2_validation.py`, `analyze_full_sparc_v2.py`):
  correct M/L, honest a₀ ≈ 1.14×10⁻¹⁰ (~5% from McGaugh), RAR scatter 0.20 dex.
  *(Currently broken by a path-changing repo reorg; committed PNGs prove prior runs.)*
- **Real DESI coordinate handling** (`prepare_full_desi`, `z2_axis_test`,
  `run_desi_chirality_test`) — and the resulting **null** is the honest answer.
- **The ghost spectroscopy** (`WORK_ORDER_NN` chain) — correctly used real BOSS
  spectra to *rule out* its own candidates.
- **The data downloader** (`WORK_ORDER_BB`) — correct public URLs, real plumbing.
- **Docking/MD** (Vina, OpenMM) — real, correctly run; simply carries no Z² content.
- **The hurricane eye/RMW test** — the cleanest science in the repo; it *correctly
  falsifies* its own Z² prediction.

---

## 5. The surviving prediction, audited

`a₀(z)/a₀(0) = E(z)` remains the one distinctive, falsifiable claim — but this audit
shows it has **zero real-data support in the repo**. Every "confirmation" is a
retrodiction on fabricated/mock data (§3C), and the catastrophic systematic is that
the real high-z kinematic data (KMOS3D) that *could* test it is sitting unused. Status
unchanged from `a0_constant_vs_evolving_fork.py`: **promising, falsifiable, not yet
evidence** — and now we know the repo's apparent "evidence" for it is not real.

---

## 6. The repo audits itself to the same verdict

The framework already contains honest self-refutations that independently agree with
this audit: `MATHEMATICAL_HONESTY_ASSESSMENT.md`, `Z2_STATISTICAL_VERDICT.md`
("the Z² framework cannot be used to design binding peptides"), `BIOTECH_PEER_REVIEW.md`,
`HONEST_CODE_AUDIT.md`, `Z2_HURRICANE_FINAL_VERDICT.md` ("FALSIFIED… 3.4× off"),
`DATA_INTEGRITY_AUDIT_MAY26.md` (wide-binary Gaia IDs "generated as representative
samples, not extracted from actual published tables"). The author's own honesty
culture reached these conclusions first.

---

## 7. What would change the verdict

One thing, and it is concrete: run the **already-downloaded real KMOS3D FITS** (and any
deep-MOND z>1 rotators) through the honest BTFR-zero-point pipeline and see whether the
zero-point shifts as E(z)^(1/4) (≈16% at z=1) or not at all. That is a real measurement
of the one surviving prediction, on real data already on disk — and it would either be
the first genuine positive result in the program or kill the last claim. Everything
else audited here is null, synthetic, circular, hardcoded, or bugged.
