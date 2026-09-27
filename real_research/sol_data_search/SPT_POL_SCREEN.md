# New calculation: foreground-clean SPT-3G × DES Y3 cross-lensing

**Date:** 2026-09-27. **Status:** conditional screen, not an action-level fit. This uses a newly published cross-observable that the [repository audit](REPO_AUDIT.md) found had no prior exact-paper fit. The older XR32 calculation supplies only a conversion-model growth history and halo-model response; the current one-action construction has not supplied a validated joint `Φ+Ψ` transfer and cross-spectrum. The screen therefore asks a narrow question: is XR32's nominal low `S8` already rejected by the published clean cross-lensing result, and how sensitive would a *uniform-power* approximation be to redshift?

## Inputs and equations

- [Ouellette et al., arXiv:2606.26223v2, Tables 4–5](https://arxiv.org/html/2606.26223v2): Full×Pol `A_Planck=1.02±0.073` and ΛCDM+NLA marginalized `S8=0.833(+0.047,-0.061)`. Full×Pol uses a polarization-only CMB lensing reconstruction. The raw Full×GMV `A_Planck=0.86±0.060` is foreground biased in the team's simulations and estimator comparisons; it is **not** the clean gravity target. The paper's amplitude is the inverse-covariance projection `A=tᵀC⁻¹d/(tᵀC⁻¹t)` onto its own Planck template `t`, not a generic gravity-model likelihood.
- [XR32's existing matter-power result](../cross_thread_review_2026_09_26/XR32_matter_power_results.json): Planck-normalized baseline `S8=0.8311719`, nominal conversion `S8(z=0)=0.7738369`, and linear `σ8` ratios `r(z)` at `z=0,0.5,1,2` of `0.931019,0.948024,0.963066,0.981281`. XR32 explicitly assumes a Planck ΛCDM early universe and brackets the nonlinear MOND phantom; its `S8` is **not** a present, action-complete prediction.

The first check places the two **published-template coordinates** side by side. With the paper's downward marginalized error, `(0.833−0.7738369)/0.061=0.970`. This does not reject the nominal XR32 `S8` coordinate even before accounting for model and Planck-normalization uncertainty. It does **not** transform the cross-spectrum posterior into a posterior on the proposed action.

The second check is intentionally a toy: if the matter-power change were independent of scale and constant across the entire lensing kernel at a chosen redshift, the cross-power amplitude would be approximated by `A_proxy(z)=r(z)^2`. The table reports `(1.02−A_proxy)/0.073`; these are fixed-parameter *sensitivity distances*, not detection or exclusion significances.

| Assumed uniform suppression at | `A_proxy=r²` | Distance from Full×Pol amplitude |
|---|---:|---:|
| `z=0` | `0.8668` | `2.10` reported σ |
| `z=0.5` | `0.8987` | `1.66` reported σ |
| `z=1` | `0.9275` | `1.27` reported σ |
| `z=2` | `0.9629` | `0.78` reported σ |

The wide change across rows is the result: assigning the low-redshift `S8` suppression to the whole sight line would overstate what this cross-correlation tests. XR32 itself gives a scale-dependent nonlinear response, for example `R(k=0.3 h/Mpc,z=0.5)=0.751` without its phantom stand-in; no row in the table includes that shape, intrinsic alignment, feedback, or the actual DES source kernels.

## Reproduce and decide the next gate

Run `python3 real_research/sol_data_search/spt_pol_screen.py` from the repo root. It reads XR32's existing result JSON and writes [these exact outputs](spt_pol_screen_result.json), with the paper values specified in the script. The only new numerical data entered by hand are the paper's Table 4 and 5 summaries. No catalogue or plotted points were digitized.

A decisive test needs the 96 Full×Pol bandpowers, window functions and covariance (four DES tomography bins × 24 bands), or an equivalent released likelihood, together with a **single-action** prediction for `C_ell^(κ_CMB γ_i)` including both metric potentials, nonlinear evolution, IA and baryonic feedback. The published paper shows the bandpowers graphically; I could not verify a public numerical cross-spectrum likelihood. Its SPT auto-spectrum shares maps with this cross-spectrum, and DES Y3 shear shares galaxies, so their likelihoods require overlap covariance. The [SPT D1 auto-lensing likelihood](https://pole.uchicago.edu/public/data/omori26/likelihoods/overview.html) is public but is a different observable.

**Disposition:** keep D22 as a high-priority quantitative target. The clean published posterior does not by itself close or rule out the conversion branch; the uniform-suppression proxy can look mildly strained or compatible depending on the redshift chosen. The action-implied all-matter MOND branch already fails the repository's [FP22 CMB-lensing gate](../derivation_chain_2026/CHAIN_STATUS.md); this cross-lensing screen does not undo that result.
