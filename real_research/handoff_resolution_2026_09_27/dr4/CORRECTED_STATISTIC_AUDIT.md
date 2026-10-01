# Executed observable and covariance audit

This is a bounded prospective calculation, not a frozen measurement pipeline. It uses the banked XR22 force table conditionally while the unchanged full force rerun is running. The distinction matters: this calculation tests the observable and Fisher likelihood, not force-table provenance or physical orbit validity.

`corrected_statistic_audit.py` ran three independent model/mock seed pairs. Each model starts from 300,000 population draws (the first gives 142,841 selected pairs); each independent mock starts from 81,000 draws and retains exactly 30,000 selected pairs. The audit uses both footings at the floor, .05 and .10 pc, with adjacent-knot derivatives to .03, .07 and .15 pc. All six configurations run in about 11 seconds per seed pair, sequentially with numerical-library thread settings at one. Memory is modest; no large bootstrap index matrix is allocated. These are new audit settings, not inherited frozen constants.

The data vector contains seven **log medians** in projected separation bins [2,3,5,7,10,15,20,30] kAU plus the two existing high-acceleration anchor-bin log medians [.5,1,2.2] in log10(g_proj/a₀). Each of 400 data bootstraps and 200 model bootstraps uses one common resample of full pairs for all nine summaries. This captures their overlap covariance. The finite model covariance is added to the independent mock covariance. The calibration derivative rescales the physical orbital velocity before noise at κ_cal=exp(±.005). A 2×2 Fisher matrix for ln ξ and ln κ_cal is profiled by its Schur complement; covariance is held at the fiducial point. Covariance eigenvalues are positive in every case; inversion is explicit, with no pseudoinverse or silently dropped bin.

The primary speed cut is ṽ<6 applied to each observable sample separately. Its Newtonian reference is also capped separately. Across all three clean-population seed pairs, **zero pairs disagree between the two cuts**, and the old intersection-cut versus corrected symmetric-cut median-ratio change is exactly zero in every evaluated bin. Thus the original cut is operationally unavailable on real data, but this test supplies no evidence that it biased these particular clean-sample forecasts. Hidden triples were not injected; one must not generalize the zero difference to contaminated samples.

| ξ | canonical σ(ln ξ), joint covariance and calibration profile, three seeds | alternative σ(ln ξ), same |
|---|---|---|
| respective floor | .3492, .3687, .3718 | .2596, .2676, .2747 |
| .05 pc | .3333, .3310, .3087 | .2450, .2536, .2404 |
| .10 pc | .8185, .8067, .7305 | .6281, .6253, .5200 |

For the first seed, keeping κ_cal fixed gives .2166/.1590 at the floor; profiling changes this to .3492/.2596. The largest separation-anchor correlation is .879 canonical and .829 alternative. Treating the anchor as independent would substantially double-count information. With the anchor entirely omitted, the first-seed floor profile errors are .3666/.2641, so the correctly included anchor helps modestly, not dramatically. The finite-model covariance and Monte Carlo derivative variability matter; no last-digit precision claim is appropriate.

Controls: the Newtonian velocity construction equals the frozen pipeline's own gamma=1 ṽ function to 1e-14; the ξ-independent mutation passes the same physical table at both neighboring ξ values through the actual prediction/summarization path and yields exactly zero ξ information; profiling never increases information. The mutation is a named degeneracy control, not a crashed run. Whole-pair resampling is adequate for these independent synthetic pairs only; actual shared Gaia components require a connected-component bootstrap.

These smaller-model runs support a **conditional statistical sensitivity of order .35/.27 near the floor**, not the original fixed-calibration .20/.16 as a total measurement uncertainty. It still does not supply a triple model, systematic covariance, self-consistent orbit population, real-sky field directions, mass-ratio force correction, goodness-of-fit calibration or finite-sample/boundary coverage. It is a Fisher sensitivity study, not an injection/recovery confidence-interval certification. The observed seed spread is reported, not folded into a claimed calibrated error bar.

A separate force-table inspection reinforces the orbit caveat: at M=.6 M☉, s=30 kAU, θ=45°, floor ξ and primary field, the banked tangential/radial force ratios are .09028 canonical and .10531 alternative. They do not directly equal a velocity-estimator bias; they show that fixed-orbit radial velocity scaling omits a nonzero force component in a tested regime.

Raw outputs: `corrected_statistic_results.json`, `corrected_statistic_results_seed1000.json`, `corrected_statistic_results_seed2000.json`, and corresponding logs. Every record carries code/table/pipeline hashes, settings, full covariances, derivatives, cap counts and diagnostics. The code extracts only the unchanged XR22 interpolation functions via AST; it never executes the original statistics main or rewrites frozen files.

The speed-cut path also has a nontrivial hand-computable failure control (`cap_control.py`). For orbital components [.5,.8,1,1] with fixed additive noise [0,0,0,4.99], Newtonian observed values are [.5,.8,1,5.99]. A 1.05 orbital boost applied **before** that noise gives [.525,.84,1.05,6.04]; separate observable caps leave 3 boosted versus 4 reference values, giving .84/.9−1=−.0666667. The counterfactual-intersection mutation removes the fourth reference value too and instead gives .84/.8−1=.05. Reverting to the old mask fails the named corrected-observable check without crashing. This artificial threshold witness demonstrates the estimand difference; it estimates neither the real contamination frequency nor the size of a DR4 bias.

## Original-population convergence check

`mc_convergence_audit.py` restores XR22's original 1,500,000 model draws and seed 20261216, retaining the independent 30,000-pair mock and sequential joint bootstrap. Runtime was 43.04 seconds and measured peak resident memory was 0.998 GiB on macOS. The six corrected separation-ratio vectors match the banked original vectors to **4.44×10⁻¹⁶**, validating the reused interpolation and observable calculation at the original model population. The exact cap change remains zero.

| ξ | profile σ(ln ξ), empirical independent-mock covariance, canonical / alt | profile σ(ln ξ), expected covariance from model bootstrap, canonical / alt |
|---|---|---|
| respective floor | .3093 / .2355 | .3368 / .2595 |
| .05 pc | .2919 / .2209 | .2761 / .2149 |
| .10 pc | .7561 / .6147 | .6571 / .5457 |

The second column uses the independently resampled mock's empirical covariance, just as the smaller-model audit does. The third substitutes C_expected = (N_model/30000 + 1) C_model, where C_model is the full paired-bootstrap covariance of the model medians; the +1 retains finite model uncertainty. This is a covariance-estimation sensitivity study, not another independent mock or coverage test. It helps explain why a single 30k mock can give a different weak-transition Fisher forecast from the large-population source's rescaled bootstrap. The 200-model-bootstrap versus original 100-bootstrap noise and changed use of log medians also remain. No single last-digit error is adopted: the evidence supports conditional floor sensitivity of order .3–.4 canonical and .24–.28 alternative under these nuisance/covariance treatments, with materially weaker sensitivity by .1 pc.

The paired bootstrap and explicit κ profile are now **executed**, while systematic covariance, contamination and coverage remain unestablished. Restoring the original model's bin ratios does not repair the underlying fixed-orbit force-to-population approximation.

Nuisance-convention sensitivity: the proposed new statistic scales orbital velocity before adding noise. The frozen estimator instead multiplies the model medians analytically. These are explicitly different nuisance conventions; the old estimator is not rewritten. Replacing the new derivative by the exactly unit log-median derivative of the frozen-style convention, at unchanged joint covariance, gives floor profile uncertainties .31268/.23738 instead of .30929/.23549 (about 1% difference). At .1 pc the values are .75683/.61572 instead of .75612/.61472. The result is not driven by this convention choice; the draft nevertheless identifies it as proposed. See `calibration_convention_audit.py` and its hashed-input result.
