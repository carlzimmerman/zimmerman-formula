# CFG315: the small scales DESI DR1 lensing cut

> **Frame.** κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law; a₀ ∝ H(z) is the rival. The cold component is still required and no particle is added. Nothing here says the data favour the framework. A failure was checked as hard as a pass, and the three failed controls are kept.

- **Criteria:** `FROZEN_CRITERIA.md`, committed in dd80cf2a0 (sha256 948e033c…2d5e) before any ΔΣ value was read.
- **Runs:** one main run, then MUTATE.
- **Post hoc, labelled:** `cfg315_posthoc.py`, which diagnoses the failed controls and changes no frozen verdict.
- **One pre-result fix:** the first launch crashed at the C0 step on `np.trapezoid` (numpy 1.26), before any ΔΣ result was printed or written. It was replaced by a `trapz` fallback. Nothing else changed between that launch and the run.

## Download record
- **Owner approval:** the owner's go (2026-10-03) on CFG314 recommendation #2.
- **The GitHub repo the approval named holds nothing.** `github.com/sheydenreich/DESI_Y1_measurements` is 3 kB, with one 2024 initial commit.
- **Where the data are:** the paper names Zenodo and that GitHub as its hosts. The release is Zenodo **10.5281/zenodo.22914838**, uploaded by C. Blake (the paper's third author), CC-BY-4.0 (not MIT).
  - File: `lwb_DESI_dr1.tar.gz`, **46,198,472 B**.
  - sha256 **641526ac9c0a6724ac8ddf0a446f3cbf852ad1adfcadd20fd4e5f8bebd34f557**; the md5 matches Zenodo.
  - Fetched 2026-10-03T12:18:32Z.
- **Where it is stored:** `../_external_data/desi_dr1_lensing/`, with `FETCH_LOG.md` there and `MANIFEST.md` here.
- **Contents:** ΔΣ and γ_t for BGS 1–3 and LRG 1–3 (DESI DR1) against KiDS-1000, DES-Y3, HSC-Y1/Y3 and SDSS, in 15 bins from 0.08 to 80 h⁻¹ Mpc, tomographic and non-tomographic. Also the joint analytic covariances with cross-survey terms, B-modes, systematics splits, and w_p.
- **Units:** taken from the pipeline code (Planck18 with H0 = 100, comoving), so r_p is comoving h⁻¹ Mpc and ΔΣ is comoving h M☉ pc⁻².

## Results

### (a) Cross-survey consistency at r_p ≤ 1 h⁻¹ Mpc
Setup: the conservative tomographic BGS measurements (7 per bin), the joint covariance, the GLS template. "s" is the error-bar inflation factor, on the same footing as CFG108's 1.58.

| BGS small scales | S1, total scatter | S2, between surveys | KiDS / (DES, HSC) |
|---|---|---|---|
| BGS1 | 2.31/6 (p 0.89) | 0.74/2 | |
| BGS2 | **22.0/6 (p 0.0012)** | 5.50/2 (p 0.064) | |
| BGS3 | 6.71/6 (p 0.35) | 2.63/2 | |
| **pooled** | 31.0/18, p 0.029, **s = 1.31 [95%: 0.99, 1.94]** | 8.87/6, p 0.18, **s = 1.22 [0.78, 2.68]** | **0.914 ± 0.034** |
| large scales (control) | 27.9/18, s = 1.25 [0.94, 1.84] | 9.42/6 | 0.928 ± 0.035 |
| all scales | 36.9/18, s = 1.43 [1.08, 2.12] | 11.1/6 | 0.922 ± 0.025 |

- **Verdict: A3, inconclusive at CFG108's level.**
  - The 95% upper limits (1.94, 2.68) do not exclude ×1.58.
  - The point estimates (1.31 / 1.22) do not reach it.
  - CFG314's line f_x < 1.25 is NOT met: S1 is 1.31.
- **What drives the excess:**
  - It is mostly BGS2, scatter between source bins WITHIN a survey (KiDS4 0.79 against KiDS5 0.97; DES3 1.16 against DES4 0.76). It is not one survey against the others: the observed S2 sits at the median of the shuffled-label distribution (empirical p 0.39).
  - The template choice does not matter (power-law template: s 1.31 / 1.19).
- **The large scales scatter about as much** (s = 1.25). The paper's "small scales drive it" is not reproduced as a scale-specific effect here (the paper used independent per-measurement errors and its AbacusSummit template).
- **Finding: KiDS ΔΣ is low against DES + HSC by 8.6 ± 3.4%** (small scales), 7.8 ± 3.4% at large scales and 7.8 ± 2.5% at all scales.
  - This is consistent with the paper's remark about low KiDS points.
  - A survey-wide factor cancels in the KiDS early/late split. It does not cancel in KiDS absolute levels (CFG261).
- **Transfer caveat (frozen):** s bounds how far independent surveys scatter beyond an analytic covariance. CFG108's ×1.58 concerns a jackknife covariance of a within-survey class difference. So this is evidence by analogy only. The honest reading is that small-scale lensing errors are under-stated by about 1.2–1.4× here, with ×1.58 neither excluded nor required.

### (b) Population RAR (BGS; R_phys ≤ 0.30 Mpc; lenses NOT isolated)
- **Usable radii:** only two radial bins per lens bin survive.
  - **Comoving reading:** r_p = 0.101 and 0.160 h⁻¹ Mpc for BGS1 (R 0.13, 0.21 Mpc); 0.160 and 0.253 for BGS2 and BGS3 (R 0.18–0.30 Mpc).
  - **The physical reading** keeps one bin for BGS2 and BGS3.
  - **Why so few:** the release's innermost bin is 0.08–0.13 h⁻¹ Mpc, and blending removes it for BGS2 and BGS3.
- **g_obs (SIS 4GΔΣ):** 6.4e-12 to 1.9e-11 m s⁻². The Mistele deprojection agrees to ≤ 5%.
- **g_bar:** 0.8–3.3e-13 m s⁻² (the KiDS-calibrated M_b,eff of 10^10.37 / 10^10.70 / 10^10.86).
- **So the points sit in the deep regime at g_obs / g_bar ≈ 50–100.** The values are in `cfg315_run.out` and the json.

### (c) The law (ν_mono, truncated at 0.40 r_ta) against the data at those radii
Q = ΔΣ_obs / ΔΣ_law; σ_Q is about 0.09–0.15.

| | canonical, primary (lowest-pred … highest-pred) | alt, primary |
|---|---|---|
| BGS1 | 2.27 (3.23 … 2.06) | 2.07 |
| BGS2 | 2.57 (3.63 … 2.31) | 2.34 |
| BGS3 | 3.30 (4.44 … 2.96) | 3.01 |
| physical-units reading | 1.95–2.40 | 1.78–2.19 |

- **Verdict: C-EXCESS on both footings and under both unit readings.**
  - The data exceed the isolated-galaxy law at every end of the stellar-mass bracket: ×1.6–4.4 across all bracket ends, readings and footings, and ≥ 7.3σ even at the highest prediction (physical reading, alt footing, BGS2). At the primary masses it is ×1.8–3.3.
  - The shape is consistent: χ² at Q̂ is 8–14 / 14.
  - For Q = 1 the law would need M_b,eff ≈ 10^11.0–11.9, against the calibrated 10^10.4–10.9. That is 0.6–1.0 dex, far outside SPS errors.
- **What this is NOT:**
  - **Not a framework failure, by the frozen rule.** The lenses are not isolated, so satellites carry their hosts' mass at these radii and centrals of groups carry group mass.
  - **Not a measurement of the isolated RAR,** and **not a ΛCDM win.** The paper's own reference is an AbacusSummit HOD; it was not released and not used.
- **Lens masses:** the release has none. They were calibrated on KiDS-bright LePhare (SPS, Chabrier; not ΛCDM-model outputs), matched on the M_R cuts. The h-convention of the cut moves them by 0.2–0.3 dex; the full bracket is 0.18–0.20 dex in ΔΣ.
- **Not modelled:** the framework's external-field effect for group members would LOWER the prediction for satellites, which would widen the gap.

## Controls
- **C0 formats/units PASS:**
  - the covariance is symmetric and positive definite;
  - the conservative-combination counts are 7/7/7 and 5/2;
  - R matches to 0.3%;
  - √diag(C_analytic) / ds_err has median 1.06.
- **C1 reproduction PASS:** σ_sys for BGS2 is **0.068 (all) / 0.118 (small)** against the paper's 0.077 / 0.102.
  - BGS3: 0.052 against 0.052.
  - LRG1 comes out low: 0.038 / 0.050 against 0.068 / 0.089. This is reported and not gated; it is perhaps the paper's template, or its LRG magnification correction.
- **C2 shuffled surveys FAIL (kept):** the false-flag rate is 0.116 against ≤ 0.05.
  - **Post hoc P3:** with Cov(A) inflated by the observed s₁² = 1.72 the rate is 0.000. So C2 failed because the real total scatter exceeds the covariance, which relabelling moves into the between-survey statistic. It is not a code error.
  - The threshold assumed a covariance-consistent total. That assumption is exactly what (a) found violated.
- **C3 null mocks PASS:** the mean s₁² is 1.002 and the A2 rate is 0.0005. The null 95th percentile of s₁ is 1.265, against the observed 1.31.
- **C4 projector PASS:** 2.6e-5.
- **C5 law asymptote FAIL (kept):** 6.7% at g_bar = 1e-12, against the 5% tolerance.
  - **Post hoc P1:** the deviation is 2.1% at 1e-13 and 0.66% at 1e-14, scaling as √y and mass-independent.
  - The law converges to the SIS limit; the frozen tolerance was set at a g_bar where the baryonic and sub-leading ν terms are still 7%.
- **MUTATE (KiDS × 1.2) FAIL as frozen (kept):** S2 p is 0.075, not < 0.01.
  - **The recovery itself is exact:** the KiDS ratio moved from 0.914 to 1.096, i.e. ×1.199. The frozen check "within 1.2 ± 2σ" assumed a baseline of 1; the true baseline is 0.914.
  - **Why the flag did not fire:** the ×1.2 injection carried KiDS from −9% to +10%, through consistency.
  - **Post hoc P2, the power of S2:** a net +20% KiDS offset (×1.313) gives p 1.4e-6, and a net −18% (×0.9) gives p 8e-5. So the test flags survey offsets of ≥ 15–20% and is blind to about 10%.
- **Gated tally:** main run 4/6, MUTATE 4/7. Both exit with rc 1.

## What this means for CFG316 (the spec-z isolation lane)
1. **Carry a small-scale covariance factor of about 1.3** (S1 point; 95% range up to about 1.9) on DES/KiDS/HSC ΔΣ errors.
   - ×1.58 is not excluded, so the KiDS split's significance should be quoted at ×1 and ×1.58 both.
   - Scatter between source bins of one survey (BGS2) is the dominant excess. Use survey-combined source samples, or carry the per-source-bin scatter.
2. **KiDS is 8–9% low against DES + HSC.** That is harmless for a within-survey early/late split but matters for any absolute level. Compare the classes within each survey, and check the split survey by survey (CFG314's C5).
3. **The non-isolated BGS signal at 0.13–0.30 Mpc is about ×2–3.3 the isolated law** (×1.6–4.4 over the full bracket). This sets the size of the environment term (satellite hosts, group centrals) that spec-z isolation has to remove.
   - If the isolated DESI stack still sits at Q ≳ 2 at these radii, isolation has not removed it and the law has a problem.
   - If it drops to Q ≈ 1, the excess here was environment.
   - The decision needs per-lens stellar masses (the DESI CIGALE / FastSpecFit VACs), not this lane's KiDS-matched calibration.
4. **Inner radii are scarce:** the release's smallest bin is 0.08–0.13 h⁻¹ Mpc. CFG316 should measure finer bins below 0.3 Mpc itself.

## Caveats
- **Units:** the comoving reading comes from the v2 pipeline's defaults. The physical reading is reported and moves Q by (1+z)².
- **Lens masses:** an external KiDS calibration, not per-lens. At its fainter reading the KiDS cut sits past the KiDS r < 20 limit at the upper z, which biases the masses high, i.e. toward the law. Equal lens weights are assumed. Boost factors are not corrected, as in the paper.
- **WebFetch was not used.** The paper was read from its saved HTML.

## Files
- **Criteria and records:** `FROZEN_CRITERIA.md`, `MANIFEST.md`.
- **Main run:** `cfg315_run.py`, giving `cfg315_run.out` and `cfg315_results.json`.
- **Control run:** `MUTATE=1`, giving `cfg315_run_MUTATE.out` and `cfg315_results_MUTATE.json`.
- **Post hoc:** `cfg315_posthoc.py`, giving `cfg315_posthoc.out`.
- **How to run:** from the repository root, with the data in `../_external_data/desi_dr1_lensing/extracted/`. The main run takes about 10 s.
