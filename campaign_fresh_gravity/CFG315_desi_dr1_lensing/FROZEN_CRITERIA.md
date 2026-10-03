# CFG315: FROZEN CRITERIA. The small scales DESI DR1 lensing cut

Written and committed **before any ΔΣ value was read.** What had been read when this was written: the file names and FITS column names in the release, the header lines of the covariance index files (`bin_ds_*.dat`, `rmax_values.dat`), the first lines of one covariance file (a variance and one off-diagonal term, to learn the format), and the paper's text (arXiv:2506.21677v1, saved beside the data). No `ds`, `ds_raw`, `ds_err`, `magnification_bias` or B-mode value was printed or computed.

κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law; a₀ ∝ H(z) is the rival. The cold component is still required and no particle is added. No line of the eventual README may say the data favour the framework.

## Data (owner-approved download, 2026-10-03)
- **What was approved:** "the DESI DR1 lensing measurements of Heydenreich et al. 2025", believed by CFG314 to sit in the GitHub repo `sheydenreich/DESI_Y1_measurements` (MIT).
- **What was found:** that repo is 3 kB, a single 2024 "Initial commit" with no data. The paper's Data Availability section says the release goes "on Zenodo and at" that GitHub address. The Zenodo record 10.5281/zenodo.22914838 (23 Sep 2026; "Galaxy-Galaxy Lensing and projected clustering measurements of DESI"; uploader C. Blake, the paper's third author; licence CC-BY-4.0, not MIT) holds one file, `lwb_DESI_dr1.tar.gz` ("Lensing Without Borders", the paper's title), 46,198,472 B. Its md5 matches Zenodo's.
- **Location:** `../_external_data/desi_dr1_lensing/` from the repository root (outside git). The fetch record (URL, bytes, sha256, date) is in `FETCH_LOG.md` there and in this lane's `MANIFEST.md`.
- **Units** (from the pipeline code `sheydenreich/desi-lensing`, `config/computation.py`: Planck18 cloned to H0 = 100, `comoving = True`): r_p in comoving h⁻¹ Mpc; ΔΣ in comoving h M☉ pc⁻². Physical conversion: R_phys = r_p / [h(1+z)], ΔΣ_phys = ΔΣ h (1+z)², with h = 0.6766 (Planck18). This is the v2 pipeline's default. If the release was made with an older configuration the conversion could differ by (1+z)², which is 0.2–0.3 dex for BGS. That is declared now as caveat K-units, and (b) and (c) are reported under both readings.
- **Measurements used:**
  - **Tomographic** (the paper's source-redshift test): `ggl/{KiDS,DES,HSCY3}/deltasigma_{BGS_BRIGHT,LRG}_zmin_a_zmax_b_lenszbin_k_blindA_boost_False.fits`, where k is the 0-based source bin, column `ds`.
  - **Combinations:** only the paper's conservative source–lens pairs (Table 2, 'c'). Per BGS bin these are KiDS 4, 5; DES 3, 4; HSC-Y3 2, 3, 4, i.e. 7 measurements. LRG1 has KiDS 4, 5, DES 4, HSC 3, 4 (5); LRG2 has HSC 3, 4 (2). HSC-Y1 and SDSS are not used.
  - **Covariance:** the joint analytic covariance with cross-survey terms, `covariances/dscovcorr_kids1000desy3hscy3_desiy1{bgs,lrg}_pzwei.dat`. Format: a size line, then `i j C_ij` with 1-based indices into `bin_ds_kids1000desy3hscy3_desiy1{bgs,lrg}.dat` (isurv 1 KiDS, 2 DES, 3 HSC; ilens; itom; isep).
  - **Lens magnification bias:** the release is uncorrected (paper §4.2.4). Primary `ds`. Variant `ds − magnification_bias` (the column read as the additive term). The variant is used only for C1 (the paper's amplitudes were corrected). If the column's median |value| / |ds| at r_p ≤ 1 for BGS exceeds 0.3, that reading is wrong, the variant is dropped, and this is flagged.
- **Scale cuts** (as the paper; HSC is the most conservative):
  - **Blending:** drop a radial bin if r_p / χ(z_mid) < 0.5 arcmin, where χ is comoving h⁻¹ Mpc in Planck18 and z_mid is the lens-bin midpoint (0.15, 0.25, 0.35, 0.5, 0.7).
  - **Maximum:** drop r_p > min over KiDS (1), DES (2) and HSC-Y3 (4) of `rmax_values.dat` for that lens bin.
  - **Small scales:** the `rp` column ≤ 1.0. **Large scales:** > 1.0. **All:** both.

## Test (a): cross-survey consistency of the small-scale ΔΣ
- **Template t** (per lens bin): the GLS common profile of all included measurements under the joint covariance (d = X t; t̂ = (XᵀC⁻¹X)⁻¹XᵀC⁻¹d). Variant: t ∝ r_p⁻¹. The paper's AbacusSummit reference is not in the release. By the paper's App. E the template sets the sensitivity, not the validity.
- **Amplitudes** (as the paper, §5.1): w = (Σ_j C_jj)⁻¹ t over the scale range, A_j = wᵀd_j / wᵀt. Cov(A) comes from the FULL joint covariance (cross-survey and cross-bin terms kept).
- **S1, total scatter:** χ²_A = (A − Ā)ᵀ Cov_A⁻¹ (A − Ā), with Ā the GLS mean; dof n − 1. The error inflation factor is s = √(χ²_A / dof), with the 95% interval from the χ²_dof quantiles. The three BGS bins are pooled by summing χ² and dof (dof 18).
- **S2, between surveys:** the GLS survey-mean amplitude per survey (KiDS, DES, HSC), χ² about the common mean using their covariance, dof 2 per bin, pooled dof 6, s_between as above. It targets a survey-level multiplicative error (KiDS against the others).
- **The factor compared with CFG108:** CFG108's 1.58 multiplies the ERROR BARS (its code divides χ² by f²), i.e. ×2.5 on the covariance. Here s is on the same footing (error bars).
- **Decision rules** (on the pooled BGS small-scale S1 and S2):
  - **A1, "×1.58 disfavoured":** the 95% upper limits of BOTH s_S1 and s_S2 are < 1.58.
  - **A2, "excess of CFG108's size present":** the point s ≥ 1.58 with 95% lower limit > 1.25, for S1 or S2.
  - **A3, otherwise "inconclusive at CFG108's level":** the upper limits are reported.
  - **CFG314's f_x < 1.25 line is reported:** whether the S1 point estimate is below 1.25.
  - **Large scales and LRG bins:** reported with the same statistics and not used for the verdict. The paper finds the large scales consistent at 2σ, so a large-scale s with a 95% interval excluding 1 is flagged.
- **Transfer caveat (declared now):** s measures how far independent surveys scatter beyond an ANALYTIC covariance at fixed lenses. The ×1.58 question concerns a JACKKNIFE covariance of a within-survey early/late difference, in which a survey-wide multiplicative error cancels. So (a) bounds the general size of small-scale covariance under-estimation plus survey calibration. It is not a direct measurement of the KiDS jackknife's error, and the README must say so.

## Test (b): the galaxy-scale RAR from these ΔΣ
- **g_obs, primary:** Brouwer's SIS conversion g_obs(r) = 4G ΔΣ_phys(R = r), as in the record (`real_research/reviews/confront_lensing_rar.py`; no 0.985 bias factor, which is KiDS-specific).
- **g_obs, variant:** the Mistele+24 deprojection g_obs(R) = 4G ∫₀^{π/2} ΔΣ(R / sin θ) dθ, with ΔΣ interpolated in log–log inside the usable range and continued as R⁻¹ beyond its last usable bin (the integral otherwise reaches the 2-halo regime).
- **Usable radii, declared now:**
  - R_phys ≤ 0.30 Mpc (the record's 1-halo boundary, CFG61 K1), with h = 0.6766 and z_mid;
  - and inside the blending cut.
  - **Only BGS.** The LRG bins have no stellar-mass calibration on disk at z > 0.4 and are not used for (b) or (c).
  - **These lenses are NOT isolated.** At these radii the stack includes satellites, whose signal carries their hosts' mass, and centrals of groups. The "RAR" built here is therefore a population RAR, not Brouwer's isolated RAR.
- **g_bar:** G M_b,eff / r², with M_b,eff = ⟨√M_b⟩² over the stellar-mass sample of (c). For the law in the deep regime ΔΣ ∝ √M_b, so this is the matching mean.
- **Outputs:** (g_bar, g_obs) per lens bin and radius, with the stat error from the joint covariance (each lens bin's usable-radius data combined over the included measurements by GLS). No pass/fail in (b); it feeds (c).

## Test (c): the framework's prediction against the data at the usable radii
- **Prediction:** the law with ν_mono (CFG7_common.M_law, C.nu_mono), both footings (a₀ = 9.3603e-11 / 1.1312e-10 m s⁻²).
  - M_L(<r) = M_b ν_mono(G M_b / r² a₀) out to r_e = 0.40 r_ta(z_mid) (CFG7_common.r_ta_law), frozen beyond (CFG61's convention).
  - ΔΣ = M_b / (πR²) + the projected phantom (this lane's projector, checked in C4).
  - **B's cold-mass rule is not added:** CFG313 showed that on native inputs it reduces exactly to the bare law in every population.
- **Lens masses: the release gives NONE.** There is no M★ column and only the M_R cuts (−19.5, −20.5, −21 for BGS 1, 2, 3; pipeline column ABSMAG_RP0). The masses are therefore an external calibration:
  - **Calibration sample:** the KiDS-bright LePhare catalogue on disk (`../_external_data/kids_lensing_zsplit/KiDS_DR4_brightsample_LePhare.fits`, read-only). Galaxies with REDSHIFT inside the lens bin and MAG_ABS_r brighter than the converted cut give the sample of log M★ = MASS_MED.
  - **What these masses are:** SPS fits (LePhare, Chabrier). They are not ΛCDM-model outputs. The photo-z is ANNz2.
  - **Cut conversion bracket:** (i) the DESI cut read as M − 5 log h (h = 1): KiDS (h = 0.7) cut = cut − 0.775 mag. This is the primary reading; at BGS3 only this places the −21 cut near the BGS r < 19.5 flux limit. (ii) The cut read with h = 0.6766: KiDS cut = cut + 0.074 mag.
  - **SPS bracket:** ±0.1 dex on M★.
  - **Gas:** M_b = M★(1 + f_cold), with f_cold = 10^(−0.69 log M★ + 6.63) (the record's Brouwer cold-gas term).
  - **Completeness caveat:** KiDS-bright is r < 20. A converted cut fainter than KiDS's limit at the bin's upper z biases the sample bright. The script reports, per bin, the KiDS apparent magnitude of the cut at z_max. Equal lens weights are assumed (the release has no per-lens weights).
- **Statistic:** per BGS bin, the usable-radius data of all included measurements, with the joint covariance, are fitted by a single amplitude on the prediction template: Q̂ = ΔΣ_obs / ΔΣ_law ± σ_Q (GLS). Also reported: χ² at Q = 1 and at Q̂.
- **Decision rules** (both footings; the M★ bracket ends are lowest = reading (ii) − 0.1 dex and highest = reading (i) + 0.1 dex):
  - **C-FAIL, "the law over-predicts":** Q̂ + 3σ_Q < 1 computed against the LOWEST prediction, in ≥ 2 of 3 BGS bins. A failure is claimed only if it holds at the end most favourable to the law, and under both unit readings.
  - **C-EXCESS, "data exceed the isolated law at every bracket end":** Q̂ − 3σ_Q > 1 against the HIGHEST prediction in ≥ 2 of 3 bins. For non-isolated lenses an excess is expected from satellites' hosts and neighbours, so it is NOT a framework failure and not separable here.
  - **C-CONSISTENT:** otherwise. Reported as "inside the bracket, not a test", with the bracket's width in dex.
  - **Also reported:** the M_b,eff the law would need for Q = 1, against the calibrated bracket.
- **Declared caveat:** in the framework, group members feel an external field that lowers their phantom. That would lower the prediction for satellites and is not modelled.

## Controls (each can fail)
- **C0, formats and units:**
  - the covariance is symmetric (to 1e-8 relative) and positive definite;
  - the index file's R matches the FITS `rp` to 1%;
  - the conservative-combination counts are 7 / 7 / 7 (BGS) and 5 / 2 (LRG1/2), all present on disk;
  - the median of √diag(C) / `ds_err` over the used small-scale bins lies in [0.6, 1.6] (an ordering or units check).
- **C1, reproduce a published number:** the paper's excess-scatter likelihood (§5.4, eq. 25: independent Gaussians with σ_stat,j² = wᵀC_jw / (wᵀt)², uniform priors A ∈ [−1, 1] on A − Ā and σ_sys ∈ [0, 2]; σ_sys = the mode of its marginal posterior on a grid), on the conservative tomographic BGS bin 2, magnification-corrected variant, GLS template.
  - **Target:** σ_sys = 0.077 (all scales) within ±0.030, AND 0.102 (small scales) within ±0.040.
  - **Reported, not gated:** BGS3 all 0.052; LRG1 all 0.068 and small 0.089; also the uncorrected `ds`.
  - The tolerance is wide because the paper's AbacusSummit template is not released.
- **C2, shuffled surveys:** 2,000 random relabellings of which survey each measurement belongs to (group sizes kept), computing S2 each time.
  - **Passes if:** the S2 flag (pooled BGS small-scale p < 0.01) fires in ≤ 5% of relabellings.
  - **Reported:** the observed S2's empirical p within the relabelling distribution.
- **C3, Gaussian null mocks:** 2,000 draws from the joint covariance about the GLS profile.
  - **Passes if:** the mean of s_S1² is within [0.9, 1.1], and A2 fires in ≤ 5% of the mocks.
- **C4, projector:** reproduces an untruncated NFW (Wright & Brainerd) to 1e-3 over 0.02–2 Mpc, and the point mass exactly.
- **C5, law asymptote:** for the untruncated law at g_bar ≤ 1e-12 m s⁻², ΔΣ is within 5% of √(M_b a₀ / G) / (4R), i.e. the deep-MOND SIS limit.
- **MUTATE** (`MUTATE=1`, outputs `*_MUTATE.*`): every KiDS ΔΣ × 1.2 (covariance unchanged).
  - **Required:** the pooled BGS small-scale S2 has p < 0.01, AND the KiDS survey amplitude relative to the other two is recovered within 1.2 ± 2σ, AND A1 is NOT issued.
  - If MUTATE does not flag, the test lacks power at a 20% survey offset, and that is recorded as a FAILED control, not hidden.

## Exit codes and files
- **Exit codes:** rc 0 if every gated control passes; rc 1 otherwise (MUTATE: rc 1 if its required flag does not fire).
- **Files:** script `cfg315_run.py` (run from the repository root); outputs `cfg315_run.out` / `cfg315_results.json` and `cfg315_run_MUTATE.out` / `cfg315_results_MUTATE.json`.
- **One run, then MUTATE.** Any later change is labelled post hoc.
