# Conditional image-fit robustness

These checks use only `image_inversion/inversion_continuous.py`, the corrected
continuous zero-padded bilinear source basis. The withdrawn hard-window source
operator and its fit results are not used. Four nonlinear parameters are
optimized: stellar log mass, two external-shear components, and log source
precision. Gaussian source/light/sky coefficients are integrated analytically.
The stellar-mass and shear priors are exactly those in `fit_images_v2.py`.

The source representation, Gaussian regularization, fixed light geometry,
edge-on deprojection, isolated unscreened AQUAL law and diagonal released RMS
remain conditional modeling assumptions. Representation spread is a robustness
diagnostic, not a statistical uncertainty interval or theory exclusion.

## Run 01: local representation and multistart checks

The bounded run completed in 286.23 seconds; its v2 manifest passed hash
validation. All eight optimizations reported convergence.

| Source representation | Best log10(Mstar/Msun) | Conditional image-score difference versus matched fixed SIE | Chi² difference versus matched fixed SIE |
|---|---:|---:|---:|
| 33×33, h=.03″, ss3, center(−.03,−.05) | 12.0402496 | +33.4435 | −0.0295 |
| 33×33, h=.04″, ss3, center(−.03,−.05) | 12.0410740 | +50.1252 | −33.7036 |
| 25×25, h=.04″, ss3, center(−.01,−.03) | 12.0423221 | +34.8449 | −18.4877 |
| 25×25, h=.04″, ss2, center(−.03,−.05), best repeated basin | 12.0414774 | +50.0655 | −31.1914 |

The best canonical masses span 0.0020725 dex, or 0.478% in mass. This is local
stability around the recovered high-mass basin, not evidence that lower-mass
solutions were adequately represented by these relatively compact windows.
The finer-grid SIE and AQUAL chi² values are almost identical: its positive
conditional score difference arises from source-prior and complexity terms,
not from a comparably large improvement in pixel chi².

Each SIE entry uses the exact fixed catalogue SIE/shear deflection with source
regularization reoptimized on that particular grid. The AQUAL parameters are
optimized while the SIE parameters remain fixed. **These score differences
are not model Bayes factors.** Raw scores also should not be compared across
representations as if the source-prior probability measure were unchanged.

Four original-grid starts cross masses 12.00/12.08 with both shear components
shifted by −.03/+ .03 from the reference fit. Three recover the reference
basin (log mass about 12.0414–12.0415). One finds an inferior local optimum at
12.0365644, g2=−.186929, with total objective 26.34 lower. The tests therefore
do not prove a global optimum, despite all optimizer success flags.

On the original grid, the alternative a0=1.1312e-10 m/s², mapped through the
canonical library by exact joint homogeneity, gives log mass 12.0199860 and
a matched conditional image-score difference +45.2742. This is a conditional
alternative fit, not an a0 posterior or model-comparison Bayes factor.

Source coefficients at the outer rings remain nonzero. The two larger 33×33
representations put about 8.9% and 11.2% of positive source coefficients in
the outer two rings. Those fractions are source-grid diagnostics, not measured
physical flux fractions, because Gaussian source priors permit negative
coefficients and include pixels weakly constrained by the image.

## Run 02: wider source window and low-mass profiles

The separate bounded wide-window run completed in 289.46 seconds with all six
optimizations successful and a validated manifest. Its ns33,h=.06″,ss2 source
has outer nodes spanning 1.92″ and full bilinear support spanning 2.04″.

**The high-mass solution is not a global mass requirement of the unrestricted
image reconstruction.** A free fit started at log mass 11.85 reaches the lower
allowed bound 11.5600000, with a total objective 143.10 higher than the
high-start branch at 12.0374765. Its image chi² is 2970.19 versus 3161.38.
The bound-hitting solution is not a mass measurement. The preserved source
reconstruction resembles the extended image arc; no image-position association
condition was applied in this run.

| Wide-grid branch | log mass | Image + shear-prior score difference from best free branch | Pixel chi² |
|---|---:|---:|---:|
| Low-start free, lower bound | 11.5600000 | 0 | 2970.19 |
| High-start free | 12.0374765 | −143.815 | 3161.38 |
| Fixed SED median, best of two starts | 11.8310873 | −308.145 | 3434.14 |
| Fixed SED upper 1σ offset | 11.9174662 | −454.321 | 3863.43 |
| Fixed SED upper 2σ offset | 12.0038450 | −250.673 | 3429.02 |

These are conditional local profiles on the same wide source grid. The
nonmonotonic values are not a Gaussian mass likelihood or a calibrated
significance. The fixed-mass source/shear optimization is still sensitive to
source regularization and local branches. The raw name
`fixed_SED_median_from_high` is a labeling artifact: its recorded starting
parameters actually come from the best free fit, which was the low branch.
The independent second median start used the catalogue shear. Actual starts
are recorded explicitly in `result.json`.

`coverage_01` independently checks 1,660 subpixel rays through 415 released
source-segmentation pixels inside the fitted mask. At the SED median with
reference shear, 61.1% have compact-grid bilinear support versus 100% on the
wide grid. At the optimized SED-median shear, coverage is 52.5% versus 98.0%.
The low-bound free branch has only 88.6% coverage even on the wide grid, so its
reconstruction is not window-converged. Coverage is a diagnostic of the
released segmentation, not a claim covering every relevant PSF contribution.

The source-position audit uses the four released `positions.json` entries,
transformed from pipeline (south,west) coordinates to (west,north). Their
largest source-plane pair separation is 0.19155″ for the fixed SIE, 0.32526″
for the wide high branch, 1.51818″ for the low-bound branch, 0.81089″ at the
SED median, and 0.31868″ at the upper2σ mass profile. The released metadata
specifies a 0.3″ gate. This is a pipeline source-association condition, not
independent new data or proof that the chosen points identify exactly the
same physical source feature.

A preserved, inspected visualization is
`coverage_01/wide_branch_comparison.png`. It shows the high free, low-bound,
and fixed-SED branches with observed source residual light, modeled source
image, standardized residuals, and reconstructed source coefficients. The
original arrays remain in `run_02/images_sources.npz`.

## Run 03: explicit source-association gates

The gate run optimizes the wide and compact source representations subject
to all six pairwise source-position separations being at most 0.3″, with a
0.5″ sensitivity case. It uses an explicit inequality and independently
checks the final separation; it does not quietly select a compact source
window to reject the low branch. Wide-grid runs use both high- and low-mass
seeds projected into the feasible set. These fits condition on the released
pipeline's multiple-image association. They cannot be called a global
posterior over unrestricted extended-source models.

The gated bounded run completed in 89.14 seconds; all six SLSQP runs reported
success, every retained parameter set satisfied its gate, and the v2 manifest
validated. Six smooth squared-distance inequalities implement each gate,
with a 1e−6″ feasibility cushion. The source-position threshold is independently
recomputed from the final retained parameters.

| Representation | Gate | Local fitted log mass | Maximum source-position separation | Conditional image-score difference versus matched fixed SIE |
|---|---:|---:|---:|---:|
| Wide33,h=.06,ss2 | 0.3″ | 12.0332828 | 0.29999901″ | +37.7110 |
| Compact25,h=.04,ss2 | 0.3″ | 12.0411714 | 0.29999900″ | +49.1255 |
| Wide33,h=.06,ss2 | 0.5″ | 12.0355365 | 0.32248923″ | +46.4345 |
| Compact25,h=.04,ss2 | 0.5″ | 12.0414805 | 0.30465377″ | +50.0656 |

The 0.3″-gated wide-versus-compact mass difference is 0.007889 dex, about
1.83%. This source-representation effect must not be hidden behind a much
narrower conditional posterior from one chosen grid.

The pre-existing run02 wide high branch at log mass 12.0374765 is also feasible
for the 0.5″ gate (separation 0.32525769″), and its objective is 0.08056 higher
than the new local 0.5″ fit. It is therefore the slightly better already-known
feasible candidate on that same wide grid. The run03 table records its actual
new optimizer outputs; neither table nor optimizer success establishes the
global optimum. No additional optimization was performed after the requested
gate checks.

For the root-provided fixed-SED environmental illustration, log mass
11.8310873126, external convergence .30879265, g1=−.0138249 and g2=−.11248273,
the maximum source-position separation is **0.21041860″**. It passes both
association gates. This verifies only the position condition at those rounded
parameters; it does not measure or establish the physical plausibility of
that external convergence. The complete coordinates and six pair distances
are retained in `run_03/result.json`.

## Artifacts and reproduction

- `contract.json`, `run_robustness.py`, and `run_01/` contain the original
  representation/multistart run.
- `wide_contract.json`, `wide_window.py`, and `run_02/` contain the wide-window
  mass-profile test.
- `gate_contract.json`, `position_gate.py`, and `run_03/` hold the explicit
  association-gated optimizations and environment position check.
- `coverage_contract.json`, `window_coverage.py`, and `coverage_01/` hold the
  independent ray/position diagnostics and the preserved branch comparison PNG.
- Each completed optimization run contains `result.json`, `trace.json`,
  `images_sources.npz`, stdout/stderr and a v2 bounded-run manifest. The
  manifests record the exact child argv, software versions, supplied input
  hashes, limits and observed output hashes. Source and detector arrays are
  retained for inspection.

The direct child reproduction commands are:

```bash
/private/tmp/forj0332-fit-venv/bin/python euclid_for_j0332_fit_2026_11_13/image_robustness/run_robustness.py --output euclid_for_j0332_fit_2026_11_13/image_robustness/reproduce_01
/private/tmp/forj0332-fit-venv/bin/python euclid_for_j0332_fit_2026_11_13/image_robustness/wide_window.py --output euclid_for_j0332_fit_2026_11_13/image_robustness/reproduce_02
/private/tmp/forj0332-fit-venv/bin/python euclid_for_j0332_fit_2026_11_13/image_robustness/position_gate.py --output euclid_for_j0332_fit_2026_11_13/image_robustness/reproduce_03
/private/tmp/forj0332-fit-venv/bin/python euclid_for_j0332_fit_2026_11_13/image_robustness/window_coverage.py --output euclid_for_j0332_fit_2026_11_13/image_robustness/reproduce_coverage
```

For bounded evidence, launch those commands through the installed
computation-audit `run_experiment.py` with the corresponding contract, repeat
its `execution_artifacts` as `--input`, declare the three result files, and
use `--timeout 600 --max-output-bytes 1048576 --max-cpu-seconds 580 --max-threads 1`
for optimization. The coverage run instead uses a 60-second bound and declares
`result.json` plus `wide_branch_comparison.png`.
The bounded runner requires a fresh output directory. Validate with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py euclid_for_j0332_fit_2026_11_13/image_robustness/run_01/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py euclid_for_j0332_fit_2026_11_13/image_robustness/run_02/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```
