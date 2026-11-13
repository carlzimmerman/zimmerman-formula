# Fixed-model source positivity sensitivity

This final bounded check constrains all625 source coefficients to be
nonnegative at frozen corrected `image_fit_02` AQUAL parameters and the
matched fixed published SIE. Each retains its own previously optimized source
precision. Lens-amplitude offset and sky remain unbounded with the same
proper Gaussian priors. It does not substitute for the later association-gated
fit or pending gated posterior.

For coefficient vector c, H=H0+Q and b are unchanged. The quadratic objective
is .5c.T H c-b.T c, with gradient Hc-b and source bounds c_i>=0. A diagonal
change of variables c_i=x_i/sqrt(H_ii) conditions this same problem. L-BFGS-B
solves it with analytic gradients. KKT uses the projected gradient: at a
zero source coefficient a nonnegative derivative is allowed; other
derivatives must vanish. The two nuisance derivatives must vanish.

| Fixed nonlinear model | Unconstrained chi2 | Positive-source MAP chi2 | chi2 increase | increase in chi2+prior penalty |
|---|---:|---:|---:|---:|
| AQUAL image_fit_02 |3092.853|3159.831|66.978|47.754|
| Published SIE |3124.043|3211.763|87.721|62.050|

Both optimizers stop successfully on relative objective tolerance. Maximum
scaled projected gradients are1.43e-6 and6.63e-7, respectively; relative
values are2.27e-8 and1.11e-8. Both satisfy the recorded numerical acceptance
targets. Source minima are exactly zero. The numbers of active zero source
coefficients are392 and441. The positive-source lens amplitudes are1.00302
and1.00127; sky values are7.13e-6 and-1.14e-5 in the image intensity units.

Neither unconstrained solution has a negative source pixel exceeding three
conditional posterior standard deviations, although234/625 and272/625
coefficients are negative. Positivity therefore makes a measurable collective
change without an individual strongly negative pixel. This is useful
sensitivity information; it does not establish source physicality under
all lens parameters or reject either model.

The calculation compares constrained MAP quadratic costs only. It does
**not** reuse the unconstrained Gaussian determinant formula to claim
truncated-Gaussian evidence, a Bayes factor or a physical-theory probability.
No nonlinear lens parameter, regularization, stellar prior, or noise model
was refitted. The frozen AQUAL point predates the final source-association
gate, so the final gated solution would need its own positivity analysis if
one wished to make a statement specifically about that solution.

The authoritative bounded outputs are in `run_01`: `result.json`, both NPZ
source/model/statistics arrays, and the v2 `manifest.json` plus captured logs.
The contract records all code, library and released-data inputs. The source
script writes only to its requested output folder.

Direct equivalent command (use a new output directory):

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /private/tmp/forj0332-fit-venv/bin/python -B euclid_for_j0332_fit_2026_11_13/positivity_check/check_positive_map.py --output NEW_OUTPUT_DIRECTORY
