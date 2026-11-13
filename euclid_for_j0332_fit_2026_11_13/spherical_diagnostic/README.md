# FOR J0332 spherical Einstein-radius diagnostic

This directory is a conditional radius-and-stellar-mass calculation for
EUCL-DR1-L014994 (FOR J0332−3557). It is **not the image fit**, a non-spherical
AQUAL solution, or an exclusion test of a covariant theory.

`diagnostic.py` independently extracts the raw catalogue rows and solves

    (D_ls / D_s) alpha_hat(theta_E D_l; M_star, R_e, n, a0) = theta_E

with an isolated spherical Sérsic stellar distribution, numerical integration
of its exact Abel deprojection, and simple-mu AQUAL acceleration
`g=(g_N+sqrt(g_N²+4 a0 g_N))/2`. Using this field as the lensing potential is an
explicit additional assumption. “Exact Abel” describes the integral being
approximated, not exact numerical arithmetic.

The reported Salpeter surviving-mass summary is fixed at photo-z 0.98. Its
`low` and `upp` columns are error offsets (median minus 16th percentile and
84th percentile minus median); lens-model `lower_1_sigma`/`upper_1_sigma`
columns are endpoint values. Those semantics are stated in the raw archive
READMEs. Spectroscopic geometry uses z_l=0.986±0.005 and z_s=3.773±0.003.

The sampler reconstructs approximate, independent marginal distributions
from the available summaries. For stellar log mass, a two-piece transform of
a standard normal has its median and 16th/84th percentiles exactly matched to
the catalogue. This is not the usual continuous split-normal density about
a mode. For lens-model quantities, the first surrogate matches median and
±1-normal-sigma bounds. A second surrogate also matches the supplied ±3-sigma
bounds by piecewise linear interpolation of normal quantiles. These are
assumed tail shapes and assumed independence, not native posterior samples.
The one-sided SED survival probability is integrated analytically conditional
on each required-mass sample, reducing sampling noise in a small tail. Its
normal-equivalent z is a convenient conditional summary, not a calibrated
frequentist goodness-of-fit probability or a definitive failure.

Both tabulated radius times sqrt(q) and tabulated radius divided by sqrt(q)
are recorded only as convention diagnostics. The calculation does not decide
which radius convention correctly describes the real 3D galaxy. The
luminosity-distance-only mass adjustment is also only a diagnostic; it is not
a new SED fit at the spectroscopic redshift.

Numerical checks include analytic 3D Gaussian enclosed mass; transformed
vectorized Abel versus independent adaptive integration; high-order LOS and
Abel convergence; adaptive LOS agreement at each central mass root; and
Newtonian deflection versus the analytic projected Sérsic enclosed mass.

The bounded run is specified in `contract.json`. From the repository root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/contract.json \
  --input euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/diagnostic.py \
  --input euclid_eclipse_screen_2026_11_13/inputs/ECLIPSE_D_dr1_redshifts_and_physical_properties.zip \
  --input euclid_eclipse_screen_2026_11_13/inputs/ECLIPSE_lens_models.zip \
  --input euclid_eclipse_screen_2026_11_13/external_verified_redshifts.csv \
  --output euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/run_01 \
  --result euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/run_01/result.json \
  --result euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/run_01/required_mass_samples.npz \
  --timeout 600 --max-output-bytes 262144 --max-cpu-seconds 580 --max-threads 1 \
  -- python3 euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/diagnostic.py \
  --output euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/run_01 --power 13
```

The runner requires a new run directory. For reproduction, replace every
`run_01` occurrence with a fresh run name. Validate the resulting manifest:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  euclid_for_j0332_fit_2026_11_13/spherical_diagnostic/run_01/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Observed run_01 results

The bounded run completed in 24.36 seconds. Manifest validation with `--root`
passed and confirmed the observed input/output hashes. There are no missing
results or stderr messages. All numerical assertions passed. The Gaussian
benchmark's largest relative error was 7.37e-9; independent adaptive Abel and
analytic Newtonian projected-mass checks agreed to floating-point roundoff;
central adaptive LOS residuals were about 1.1e-11. This establishes finite
numerical agreement for the named checks, not a certified uniform error bound.

| a0 (m/s²) | Required stellar log10(M/Msun), central inputs | Required mass | Ratio to Salpeter SED median |
|---|---:|---:|---:|
| 9.3603e-11 | 12.05023057 | 1.12261e12 Msun | 1.6563 |
| 1.1312e-10 | 12.02943605 | 1.07013e12 Msun | 1.5789 |

The conditional SED mass is log10(M/Msun)=11.83108731 with lower/upper offsets
0.10419239/0.08637887 dex. At its median, the predicted reduced deflection at
the observed Einstein radius is 0.67264 or 0.70474 times that radius,
respectively. These ratios are evaluated at the measured radius; they are
not predictions for the ratio of fitted Einstein radii.

For the first marginal-summary reconstruction and first Sobol scramble, the
required log mass has median and 16th/84th percentiles
12.05035 [12.03316, 12.06833] or 12.02955 [12.01246, 12.04742]. Integrating the
asymmetric SED distribution over those required masses gives upper-tail
probabilities 0.0066702 and 0.0125288, with one-sided normal-equivalent
summaries 2.47455 and 2.24051. The second independent scramble changes either
tail by less than 5.8e-7. Using the additional 3-sigma shape bounds changes
the summaries to 2.48179 and 2.24702. Unknown SED tail shape and missing joint
covariance remain more important qualifications than this sampling precision.

Re uncertainty dominates the required-mass measurement width: its separate
1-sigma shifts are −0.01696/+0.01804 dex. Lens-redshift and Sérsic-index shifts
are each about 0.002 dex; source-redshift and effective-Einstein-radius shifts
are around 0.00015–0.00025 dex. The Re*sqrt(q) and Re/sqrt(q) convention trials
move central baseline log mass to 12.03286 and 12.06848. A luminosity-distance-
only transport of the SED normalization from z=.98 to z=.986 gives +0.00653 dex,
without incorporating stellar-population or K-correction changes.

The result is **conditional on the stated numerical approximation and marginal
uncertainty surrogates**. No image likelihood, field solution for the measured
flattening, environment treatment, spectroscopic-redshift SED fit, or stellar
mass systematics are included. The next discriminating step is the separately
owned image fit and a native joint SED/light-model posterior or explicit
robustness analysis of its unavailable covariance and tails.
