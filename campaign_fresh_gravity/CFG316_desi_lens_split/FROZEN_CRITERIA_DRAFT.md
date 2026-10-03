# CFG316: does spectroscopic isolation keep the KiDS early/late split? FROZEN CRITERIA — **DRAFT**

> **DRAFT. NOT FROZEN. NOT TO BE COMMITTED AS FROZEN.** Written 2026-10-03 at the data stage, before any value of any catalogue was read. Only the column schemas (header cards) were read. The orchestrator freezes this file after reading the column schema (`cfg316_column_schema.json`), not the values. Every item marked **[DECIDE]** must be settled before freezing. After freezing, nothing may change once a result is seen; any later deviation goes in the README as a disclosed departure.

κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law; this lane does not test a₀(z). The cold component is still required; no particle is added. No sentence of this lane may say the data favour a law.

## Why

The KiDS early/late lensing split is candidate B's one failure specific to B in shared machinery. It survives a data-driven covariance (CFG88: 4.4σ on K1), B's own stellar-mass calibration (CFG95: 2.8σ released, 3.6σ re-measured) and a twice-stricter photo-z isolation window (CFG96: 4.1σ, A₂₀ = 0.97 ± 0.19; CFG109: the isolated and neighbour splits do not differ within errors).

What no committed lane has removed (CFG108, CFG314): the KiDS isolation is a **photo-z** isolation (σ_z ≈ 0.026), validated by Brouwer+21 on **MICE**, a ΛCDM HOD + abundance-matching mock, at about 80% purity. Satellites contaminate early types more and raise their ESD, so an isolation impurity can fake a split. A jackknife cannot see this. Mistele & McGaugh (arXiv:2310.15248), with a 4 Mpc criterion and their own SPS masses, report one RAR for both types.

**The frozen question:** on the KiDS-1000 ∩ DESI DR1 BGS overlap, with lenses isolated by **spectroscopic** redshift, does the early/late split in the deep (1-halo) regime persist at fixed baryonic mass, beyond the M/L offset that B's own calibration supplies?

## Data (all outside the repo, under `_external_data/`; sizes and checksums in `CFG316_MANIFEST.json`)

- **Lenses:** DESI DR1 `BGS_BRIGHT_full_HPmapcut.dat.fits` (LSS v1.5; HDU `LSS`, 6,419,406 rows, 118 columns). It holds observed and unobserved BGS_BRIGHT targets, so the isolation census can see neighbours that were not observed.
  - Redshift column: `Z_not4clus` (with `ZWARN`, `DELTACHI2`, `SPECTYPE`, `COADD_FIBERSTATUS`). **[DECIDE]** the good-redshift rule; proposed: `ZWARN == 0`, `DELTACHI2 > 40`, `SPECTYPE == 'GALAXY'`, `COADD_FIBERSTATUS == 0` (the DESI BGS LSS convention; to be confirmed from the DESI LSS documentation before freezing).
  - Unobserved targets: rows with no good redshift. Their photometry (`FLUX_G/R/Z`, `FLUX_W1/W2`, `MW_TRANSMISSION_*`) and `RA`, `DEC` are kept for the isolation census.
  - Completeness weights present: `WEIGHT_ZFAIL`, `COMP_TILE`, `FRACZ_TILELOCID`, `FRAC_TLOBS_TILES`, `WEIGHT_NTILE`. Not used in the stack; used only in R-rows on isolation completeness.
- **Stellar masses:** DESI DR1 CIGALE VAC `IronPhysProp_v1.2.fits` (Redrock redshifts), joined on `TARGETID`. HDU `DATA`, 17,149,172 rows, 69 columns (header read): `TARGETID`, `Z`, `CHI2`, `LOGM`, `LOGM_ERR`, `LOGSFR`, `AGNFRAC`, `FLAG_MASSPDF`, `FLAGOPTICAL`, `FLAGINFRARED`, rest-frame `LNU_U/G/R/I/Z` and colours `NUVR, RK, UV, VJ, GR` (no direct u−r column; u−r can be formed from `LNU_U`/`LNU_R`). Quality cut **[DECIDE]**, proposed: 1/5 ≤ `FLAG_MASSPDF` ≤ 5 (the VAC's own recommendation), `AGNFRAC < 0.1`.
- **Shear:** KiDS-1000 SOM-gold `KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` (HDU `OBJECTS`, 21,262,011 rows, 193 columns): `RAJ2000`, `DECJ2000`, `e1`, `e2`, `weight`, `Z_B`, `MASK`, `THELI_NAME` (patch/tile), and the SOM n(z) from `KiDS1000_SOM_N_of_Z.tar.gz`. Multiplicative bias m per tomographic bin from Giblin+21 / Asgari+21 as committed in the June re-measurement (`lr_esd_remeasure.py` v4), read-only.
- **Stage B (not in this lane's first run):** DES Y3 metacal (`DESY3_metacal_v03-004.h5`, 312,037,859,376 B; NOT downloaded, exceeds free disk; a separate owner decision) and HSC Y3 (needs an account the owner creates).
- **Overlap (arXiv:2512.15960 Table 3, nside-1024 HEALPix; read from the arXiv HTML, to be re-read from the PDF before freezing):** KiDS-1000 ∩ DESI-BGS **448.2 deg²** (∩ LRG 446.8; ∩ BGS+LRG 446.3). DES-Y3 ∩ BGS 716.8; HSC-Y3 ∩ BGS 440.6. Note: CFG314 quoted the BGS+LRG column (446.3 / 587.5 / 413.3, total 1,447 deg²); the BGS-only column, which is what a BGS-lens lane uses, is 448.2 / 716.8 / 440.6 (1,605.6 deg²).

## Lens sample

- In the KiDS-1000 footprint (KiDS `MASK` footprint via HEALPix nside 1024 of the source positions **[DECIDE]**), 0.05 < z < 0.5 **[DECIDE: match the KiDS bright range]**, good redshift, good CIGALE mass.
- **Class:** early vs late. **[DECIDE]** one of: (a) CIGALE rest-frame u−r from `LNU_U`/`LNU_R` (or `UV`/`GR`), with the KiDS valley transferred by matching the KiDS bright sample on the overlap), (b) the KiDS LePhare u−r > 2.0 for lenses matched to the KiDS bright sample (the committed CFG88 definition). Proposed headline: (b) on the matched subset, so the class is identical to CFG88's and only the isolation changes; (a) as R-row.

## Isolation (spectroscopic)

- **Headline (ISO-S):** a lens is isolated if no galaxy with M★ > 0.1 M★,lens lies within R_iso = 3 Mpc (physical, transverse) with |Δv| < 1000 km/s **[DECIDE: 3 Mpc physical vs 3 Mpc/h; |Δv| window]**, using DESI spectroscopic redshifts for every neighbour that has one.
- **Unobserved neighbours:** a BGS target without a good redshift that is within R_iso and bright enough to exceed 0.1 M★,lens at the lens redshift (flux-to-mass at the lens z with the lens-class median M/L) **counts as a neighbour** (conservative). The fraction of lenses excluded only by unobserved neighbours is reported (R2).
- **Fainter-than-BGS neighbours:** BGS_BRIGHT is r < 19.5. At the lens redshift, a 0.1 M★,lens neighbour must be brighter than r = 19.5 for the census to be complete; lenses where it is not are dropped (the completeness cut). **[DECIDE]** whether to supplement with Legacy Surveys photo-z below the BGS limit (would re-introduce photo-z).
- **Strict variant (ISO-S4):** R_iso = 4 Mpc, M★ > 0.1 M★,lens, |Δv| < 2000 km/s, and unobserved neighbours counted as above (the Mistele & McGaugh scale).
- **Photo-z reference (ISO-P):** the committed KiDS photo-z isolation (|Δχ| < 10 Mpc, `lr_esd_remeasure.py` v4), applied to the same overlap lenses. This is the C1 contrast.

## Regime and binning

- g_bar from the lens M_b = M★ + M_gas, M_gas = f_cold(M★) M★ (Brouwer's relation, as CFG61), point mass at the bin radius; the 15 g_bar bins of CFG61's `EDGES`; **K1** = the seven 1-halo bins [8..14] (the deep regime).
- **Fixed baryonic mass:** the split is compared in the same g_bar bins, and also within two M★ bins **[DECIDE edges]** with the early and late M★ distributions matched by reweighting (R-row), so a class-dependent mass distribution cannot fake a split.

## Models

- **L (B's law):** ν_mono (FP1's committed kernel, executed read-only via `CFG4_common.nu_mono`) on **both footings** (a₀ = 9.36e-11 and 1.13e-10 m s⁻²). B's law is colour-blind; its predicted early-minus-late difference at fixed g_bar is zero except for the M/L offset.
- **B's M/L offset:** CFG95's calibration (α_dyn,foot(σ) for early types; Υ_SPARC/0.5 for discs), with the CIGALE masses read as Chabrier (the VAC's stated IMF). This gives B's predicted D_B (CFG314: about 0.035 dex in g_obs).
- **Λ (reference only):** CFG67's colour-split ΛCDM halo masses, as a comparison row, never as a fitted model.

## Statistic

- D = ESD_early − ESD_late on K1, per isolation definition. Covariance: leave-one-patch-out jackknife over N = 50 patches **[DECIDE: patches on the 448 deg² overlap; 50 may be too many for ~450 deg²; propose N = 30, Hartlap (N−p−2)/(N−1)]**.
- **χ²_B** = (D − D_B)ᵀ C⁻¹ (D − D_B) × Hartlap, 7 dof.
- **A_S** = the amplitude of D relative to the KiDS photo-z split shape on K1 (as CFG96's A).

## Checks

- **C1 CONTROL [the decisive contrast]:** on the overlap, the photo-z isolation (ISO-P) with KiDS shear and the CFG88 class reproduces a split consistent with the committed KiDS split (A_P consistent with 1 within 2σ). If C1 fails, nothing below is interpreted.
- **C2 CONTROL:** the stacking code, run on the committed `lr_lenses.npz` with the committed estimator, reproduces `lr_esd_jackknife.npz` sums to 1e-9 relative (needs the complete KiDS shear catalogue).
- **C3 CONTROL:** the isolated samples are nested where the definitions are nested (ISO-S4 ⊂ ISO-S); every count is printed.
- **C4 CONTROL:** random points (`DESI` randoms or uniform in the footprint) give ΔΣ consistent with zero on K1 (additive-bias test); cross-shear consistent with zero.
- **H1 [HEADLINE; MUTATE must fail]:** with ISO-S, B's prediction (D = D_B) is consistent on K1: p > 0.01 on both footings. *Reading:* H1 PASS means spectroscopic isolation removes B's specific failure; H1 FAIL means the split survives spectroscopic isolation.
- **H2:** the same for ISO-S4.
- **H3:** A_S (ISO-S) relative to A_P (ISO-P, same lenses): the difference, with its jackknife error. A_S more than 2σ below A_P = the split was (partly) an isolation artefact.

## Reported rows

- **R1:** counts per sample; early fraction; median log M★ per class; isolated fraction.
- **R2:** lenses excluded only by unobserved neighbours; the completeness-cut loss.
- **R3:** CIGALE vs KiDS LePhare M★ on matched lenses, per class (the class-dependent offset Q; Mistele's Q = 1.4 is the external reference).
- **R4:** the split with the class from CIGALE colours (option a).
- **R5:** χ²(Δ) for a uniform differential M/L offset Δ on CFG95's grid, 0–0.5 dex in 0.025 steps.
- **R6:** the WMAP7 → Planck distance rescaling of CIGALE masses (uniform offset; does not change D at first order) as a bracket.
- **R7:** K1 with each bin dropped in turn.

## MUTATE

MUTATE=1: early and late labels swapped with probability ½ per jackknife patch (seed 316) before stacking. This destroys the split and keeps the noise; the outputs are written under `*_MUTATE*` names. The README states whether the control is informative (only if the main run's H3/H1 discriminate).

## ΛCDM-model content of the stellar masses (flag)

From the DESI CIGALE VAC documentation (`data.desi.lbl.gov/doc/releases/dr1/vac/cigale/`):
- **Cosmology: WMAP7.** Luminosity distance (M★ ∝ D_L²) and the maximum stellar age (age of the universe) are ΛCDM-WMAP7. At z ≈ 0.2 the WMAP7 vs Planck distance difference is a near-uniform ≈ 0.04 dex offset (R6), common to both classes.
- **Not ΛCDM, but model priors:** delayed SFH with optional exponential burst; BC03 SSPs; Chabrier IMF; **solar metallicity fixed**; Calzetti attenuation; Dale+14 dust; Fritz+06 AGN; photometry g, r, z, W1–W4 only. Fixed solar metallicity and the SFH family are class-dependent systematics (old metal-rich early types vs discs) and are the M/L offset the split is degenerate with; R3 and R5 bracket them.
- **No halo, HOD or abundance-matching input** enters the CIGALE masses (unlike the KiDS isolation's MICE validation). This is why they are acceptable as framework-native masses, conditional on the WMAP7 distances.

## Readings (declared)

- **C1 PASS, H1 PASS, H3 shows A_S < A_P by > 2σ:** the KiDS split was an isolation artefact; B's specific failure is removed at this sensitivity.
- **C1 PASS, H1 FAIL, H3 consistent:** the split survives spectroscopic isolation on 448 deg² with DESI lenses; B's failure stands on cleaner lenses.
- **C1 FAIL:** the overlap does not reproduce the KiDS split even with photo-z isolation; the lane is NOT DIAGNOSTIC.
- Expected power (CFG314 P1, a scaling from KiDS, not a covariance forecast): KiDS-only overlap is MARGINAL; the CRISPY verdict needs DES Y3 and HSC Y3 (Stage B).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
