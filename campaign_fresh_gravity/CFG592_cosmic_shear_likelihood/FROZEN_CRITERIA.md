# CFG592 FROZEN CRITERIA: a real cosmic-shear likelihood (KiDS-1000 ξ±, DES Y3 ξ±) for ΛCDM + feedback and for the framework's R(k)

Date frozen: 2026-10-10. Committed alone, before any value of the data vectors or covariances was read and before any number of this lane was computed. Before freezing, only the downloaded files' formats were inspected: FITS extension names, column names, header keywords (bin counts, angular units, covariance block offsets), and the public pipeline configuration files (priors, nuisance parameterisation, scale cuts). The published chains in the KiDS release were NOT opened.

Settings: κ = ½ FITTED; footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s², never pooled; flat a0 = κ c √(G ρ_DE); kernel ν_mono; candidate B. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework. Other lanes are read only.

## 0. Question

CFG590 judged the framework's matter power against cosmic shear through a projected-A_mod shortcut with recalled A_mod values (framework PRIMARY EXCLUDED; ΛCDM + feedback CONSISTENT). This lane replaces the shortcut with the surveys' own data vectors, covariances, n(z), nuisance priors and scale cuts, and asks the same question as a likelihood: Δχ² (framework − ΛCDM) at best-fit nuisances, and the S8 the framework would need.

## 1. Data (downloaded with the owner's approval of 2026-10-10; outside git; logged in FETCH_LOG.md)

- **KiDS-1000** (Asgari+21 release `KiDS1000_cosmic_shear_data_release.tgz`): `xipm_KIDS1000_BlindC_with_m_bias_..._SOM_Fid.fits`: ξ+ and ξ− for 5 tomographic bins (15 pairs × 9 log θ bins, 0.5–300 arcmin), the 270 × 270 covariance (m-bias uncertainty included in it, as published), NZ_SOURCE. ξ± chosen (not COSEBIs / band powers) because its theory is a direct Hankel transform; COSEBIs and band powers are not used.
- **DES Y3** (`2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits`): xip / xim for 4 source bins (10 pairs × 20 θ bins), the corresponding 400 × 400 block (rows 0–399) of COVMAT, nz_source. γt and w(θ) are not used (cosmic shear only); the shear-ratio likelihood is not used.
- **Scale cuts (published):** KiDS ξ+ θ ∈ [0.5, 300]′, ξ− θ ∈ [4, 300]′ (Asgari+21 pipeline.ini). DES: the Y3 fiducial ξ± angle ranges of `des-y3-scale-cuts.ini` (cosmosis-standard-library), applied to the bin-centre column ANG.
- The covariances are used as published (analytic; no Hartlap factor).

## 2. Theory (own implementation; pyccl as a cross-check)

- **Cosmology fixed (PRIMARY):** CFG590's Planck-like set: h = 0.6736, ω_b = 0.02237, ω_c = 0.1200, n_s = 0.965, σ8 = 0.811 (S8 = 0.8314), massless neutrinos, flat.
- **Matter power:** P_X(k, z) = R_X(k, z) · P_HM(k, z; σ8, T), with P_HM the CAMB 1.6.6 HMcode-2020 spectrum: `mead2020_feedback` at log T_AGN = T (BAHAMAS-calibrated) for both models. T is a nuisance, flat prior on [7.3, 8.3] (HMcode-2020 calibration range). P_HM is tabulated on a (σ8, T) grid (T step 0.1; σ8 nodes 0.60–0.92 step 0.02 plus 0.811) and interpolated bilinearly in log P. R_ΛCDM ≡ 1 through the same code path. R(k < 1e-3) = 1, R(k > 10 h/Mpc) = R(10) (CFG590's rule).
- **Projection:** Limber, C_ℓ^{ij} = ∫ dχ W_i W_j P((ℓ + ½)/χ, z)/χ², lensing kernels from each bin's n(z); flat-sky ξ±(θ) = ∫ ℓ dℓ/2π C_ℓ J_{0/4}(ℓθ), averaged over each θ bin with weight ∝ θ (DES edges from ANGLEMIN/ANGLEMAX; KiDS edges = 10 log-spaced edges 0.5–300′; KiDS's pair-count weighting is not available: disclosed).
- **Intrinsic alignments: NLA**, P_GI = −A_IA C1 ρ_crit Ω_m / D(z) · f(z) · P_X, P_II = (…)² P_X, C1ρ_crit = 0.0134. KiDS: f = 1, A_IA flat [−6, 6] (its published prior). DES: f = [(1+z)/1.62]^η, A_IA and η flat [−5, 5] (its published NLA-z prior range; DES's fiducial TATT is not run: disclosed).
- **Photo-z shifts:** n_i(z) → n_i(z − Δz_i). KiDS: Δz = L u with L the Cholesky factor of the published SOM covariance (`SOM_cov_multiplied.asc`), u_i ~ N(μ_i, 1), μ = (0, −0.181, −1.110, −1.395, 1.265) (published). DES: Δz_i ~ N(0, σ_i), σ = (0.018, 0.015, 0.011, 0.017).
- **Shear bias:** DES m_i ~ N(m̄_i, σ_i), m̄ = (−0.0063, −0.0198, −0.0241, −0.0369), σ = (0.0091, 0.0078, 0.0076, 0.0076); ξ^{ij} × (1 + m_i)(1 + m_j). KiDS: m is in the covariance (published "with_m_bias"); the additive term δc ~ N(0, 2.3e-4) adds δc² to ξ+.
- **χ²** = (d − t)ᵀ C⁻¹ (d − t) + Σ Gaussian-prior terms (flat priors add 0). "Best fit" = minimum of this total over all nuisances (T, IA, Δz, m, δc; and σ8 when free), by bounded quasi-Newton from several starts (T starts 7.4, 7.8, 8.2); the lowest is kept.

## 3. Models

- **ΛCDM:** R ≡ 1.
- **Framework, per footing (canonical, alt; never pooled):**
  - **PRIMARY:** CFG559 `PRIMARY_kin` R(k), z = 0, held fixed in z. CFG591 (the redshift-dependent R(k, z)) has no committed R(k, z) at freeze time; it is NOT used.
  - **PRIMARY z-scaled (declared variant):** R_s(k, z) = 1 + s(z) [R(k) − 1], s(z) from CFG590's post-hoc cluster-share table (`cfg590_posthoc.json` `s_of_z`, linear in z between its nodes 0–1.0; s(z > 1) = s(1.0)). It enters the verdict as a variant (see §5), it is not a replacement for the PRIMARY.
  - **Survivors:** CFG556 `census|emg` (emergent edge) and CFG556 `census|cen|r200scope` (r200m scope), z = 0, held fixed.
  - **Reported only (class given, no verdict weight):** CFG559 `VARIANT_full_kin`, CFG557 `TESTED`, CFG556 `census|cen`.
- **Modes:** (A) cosmology fixed (σ8 = 0.811) — the PRIMARY verdict mode; (B) S8 free (σ8 free on [0.60, 0.92], Ω_m and the rest fixed) — reported with its own classes.

## 4. Statistics

- Δχ² = χ²_min(framework) − χ²_min(ΛCDM), same survey, same mode, each minimised over its own nuisances (T included). Positive = framework worse.
- Per survey and mode: χ²_min, number of data points after cuts, best-fit T and nuisances.
- **Mode B:** best-fit S8 = σ8 √(Ω_m/0.3) and its 68% interval from the profile Δχ² = 1, for ΛCDM and each framework model. Planck consistency (reported): T_P = (0.832 − S8)/√(0.013² + σ_S8²), Planck 2018 S8 = 0.832 ± 0.013 (recalled, PROVISIONAL); |T_P| < 2 PLANCK-CONSISTENT, 2–3 PLANCK-TENSION, ≥ 3 PLANCK-INCONSISTENT. Also the shift ΔS8 = S8_F − S8_ΛCDM.
- Combined KiDS + DES Δχ² (sum, treating the surveys as independent) is reported, not used for verdicts.

## 5. Verdicts (per survey × footing × model; mode A, then the same rule in mode B labelled "S8-free class")

Robustness set: (R1) the primary fit; (R2) every Gaussian nuisance prior widened × 2 (Δz / u, m, δc), both models; (R3) T fixed at 7.3, 7.8 and 8.3 in both models (nuisances still profiled).
- **EXCLUDED:** Δχ²(R1) ≥ 9 and min over {R1, R2, R3} ≥ 9.
- **TENSION:** Δχ²(R1) ≥ 4 and not EXCLUDED.
- **CONSISTENT:** Δχ²(R1) < 4 and max over {R2, R3} < 9.
- **NOT DIAGNOSTIC:** any other case (Δχ²(R1) < 4 but some robustness member ≥ 9), OR the survey failed a control of §6 (C1, C2) or the MUTATE tooth MU2 for that survey — then every framework class for that survey is NOT DIAGNOSTIC.
- **Footing verdict (per model):** the most severe class among the surveys that passed their controls (EXCLUDED > TENSION > CONSISTENT); NOT DIAGNOSTIC if neither survey passed.
- **VARIANT-SENSITIVE (flag):** the PRIMARY z-scaled variant or a survivor gives a different class from the PRIMARY.
- **Negative Δχ²** (framework better) is reported as is; CONSISTENT is the most it can earn (never "favoured").

## 6. Controls (a failed control makes that survey NOT DIAGNOSTIC, §5)

- **C1 (ΛCDM S8 reproduction):** mode B ΛCDM best-fit S8 within 0.04 of the published value. KiDS reference: the posterior median of S_8 in the released ξ± chain (`xipm/chain/output_multinest_C.txt`, weights as given), read AFTER this freeze. DES reference: 0.772 (Y3 cosmic shear, ΛCDM, recalled, PROVISIONAL; the tolerance 0.04 also covers the recalled fiducial-TATT 0.759 and the ~0.78 NLA values). Ω_m fixed at 0.3153 here vs. marginalised in the papers, and the HMcode-2020 feedback in place of each survey's baryon model, are disclosed as reasons for differences inside the tolerance.
- **C2 (projection cross-check):** pyccl 3.3.6 (venv outside the repo), given the SAME P(k, z) as a Pk2D and the same n(z), computes ξ± (FFTLog, bin-averaged on the same sub-grid) for the ΛCDM fiducial (T = 7.8, A_IA = 0.5, nominal nuisances); the χ² distance between mine and pyccl's in the survey's covariance (after cuts) must be ≤ 1.0.
- **C3 (reported):** CAMB σ8 at the fiducial node = 0.811 to 1e-3; R(1e-3) = 1 to 1e-3 for every R input; ΛCDM mode A χ²_min / N_data.

## 7. MUTATE (`CFG592_MUTATE=1`; separate `_MUTATE` outputs; exit 1 = all teeth bite)

- **MU1:** framework R ≡ 1 must reproduce the ΛCDM χ²_min and best-fit nuisances exactly (|Δχ²| ≤ 1e-9) in both surveys and both modes.
- **MU2 (tooth, per survey):** mock data = the ΛCDM mode-A best-fit theory vector multiplied through an injected R_inj(k) = 1 + 0.2 g(k), g = 0 for k ≤ 0.5, rising linearly in ln k to 1 at k = 1 h/Mpc, 1 above (applied at all z). Fit the mock (published covariance, no noise) with ΛCDM (mode A, all nuisances and T profiled): the excess must be detected, χ²_min(ΛCDM | mock) ≥ 9. If it fails for a survey, that survey is NOT DIAGNOSTIC for the framework (§5).
- **MU3 (sign):** the same mock fit with the framework PRIMARY canonical R must not return χ² below the injected truth (0) by more than 1e-6 (minimiser sanity).

## 8. Outputs and compute

`cfg592_like.py` → `cfg592_like.out`, `cfg592_results.json`; with `CFG592_MUTATE=1` → `cfg592_like_MUTATE.out`, `cfg592_results_MUTATE.json`; `FETCH_LOG.md`; `README.md`. The P_HM grid cache lives outside git. Compute: `nice -n 10`, ≤ 4 threads. All quoted numbers come from the JSON.

## 9. Pre-freeze disclosure (dated 2026-10-10)

Read before freezing: CFG590 criteria, README, script, post-hoc JSON keys; CFG591 criteria (folder: no committed R(k, z)); the KiDS release Read.me, read_data_files.py, pipeline/values/priors .ini; the DES Y3 cosmosis example .ini, values, priors and scale cuts; FITS headers and column names only. No data value, covariance value or chain value was read; no number of this lane was computed. Expectation (by hand, not a threshold): CFG590's shortcut suggests the PRIMARY Δχ² is large and positive and the survivors near zero; a real likelihood with T and IA free could absorb part of the excess, so either sign of the change is possible.
