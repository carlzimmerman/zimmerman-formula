# Two finite-radius predictions confronted with SPARC

2026-09-04. **Mathematics derived; empirical discrimination inconclusive;
no new law of nature established.** This is a completed bounded study, not
a completed relativistic theory.

## 1. Outcome first

The fixed exponential algebraic response predicts the measured two-point
changes substantially better than extending either limiting power law over
the entire selected acceleration range. It does not clearly outperform the
distinct RAR exponential or the simple-mu rival. The three-point statistic
does not establish the predicted curvature; its modest primary-sample
offset is sensitive to stellar mass assumptions, radius selection and
quality cuts. None of these results earns a Kepler-grade discovery claim.

The actual advance is a reproducible pair of finite-interval tests, including
full shared-measurement contrast covariance, rather than another fit of a
pooled acceleration curve or a derivative of noisy velocities. The new
implementation checks whether the exact exponential response gets both the
amount of change and its curvature right on the same galaxy triples.

## 2. The equations and what they assume

Let b denote the Newtonian baryonic acceleration and g=V^2/R the dynamical
acceleration. Define I(s)>0 by I(s)[1-exp(-I(s))]=s. The primary prediction is

\[
g(b)=a_0 I(b/a_0),\qquad a_0=9.36\times10^{-11}\ {\rm m\,s^{-2}}.
\]

The proposed a0-Lambda relation supplies this normalization as input; this
study does not derive it from an action.

**Equation 1: finite response.** At two radii ordered by b_lo<b_hi,

\[
\frac{g_{\rm hi}}{g_{\rm lo}}
 =\frac{I(b_{\rm hi}/a_0)}{I(b_{\rm lo}/a_0)},\qquad
\sqrt{\frac{b_{\rm hi}}{b_{\rm lo}}}
 <\frac{g_{\rm hi}}{g_{\rm lo}}
 <\frac{b_{\rm hi}}{b_{\rm lo}}.
\]

We measure D=log10(g_hi/g_lo) and compare its exact prediction. A factor 100
in baryonic acceleration must produce a factor strictly between 10 and 100
in dynamical acceleration under this response, not necessarily either
endpoint power law.

**Equation 2: finite curvature.** For b0<b1<b2, with the physical radii not
necessarily in that order, define t=ln(b1/b0)/ln(b2/b0). Then

\[
J=\log_{10}\frac{g_1}{g_0^{1-t}g_2^t}
 =\log_{10}\frac{I(b_1/a_0)}{I(b_0/a_0)^{1-t}I(b_2/a_0)^t}<0.
\]

The proof uses L(y)=y/(exp(y)-1),
d ln(g)/d ln(b)=1/(1+L), and
d^2 ln(g)/d ln(b)^2=-yL'(y)/(1+L)^3>0. The sign is proved analytically for
all y>0; the script independently differentiates the response and checks
the chain rule. Pure deep MOND and Newtonian gravity give J=0. The RAR and
simple-mu rivals also predict negative J, so the sign alone cannot identify
the exponential law. MOND endpoint limits alone do not imply this convexity.

These are formal corollaries of the specified algebraic response, not two
independent physical postulates. In spherical AQUAL that response is exact
under the usual flux conditions. Applying it to the radial baryonic force
of a disk is an algebraic approximation: it is not an exact general disk
solution of AQUAL/QUMOND, and does not include environmental corrections.

## 3. What was measured

The actual inputs are the valid SPARC master catalogue and 175 original
local rotation-model files, plus the existing master-table parser. All
177 input files are individually hashed in results.json; executable and
documentation hashes are also preserved by the runner. The similarly named
SPARC_table.txt is an HTML 404 page and was not used.

The frozen primary selection keeps 78 galaxies. Each contributes exactly
one triple: minimum and maximum log b among eligible radii, plus the point
nearest their logarithmic midpoint. The endpoints must span at least 0.5
dex, with the middle point genuinely interior. Selection uses baryonic
profiles and the documented quality/radius cuts, not the observed response
or agreement with a kernel. Original indices and all measured/predicted
values are stored for every selected galaxy.

Disk/bulge mass-to-light ratios are .5/.7. The scale a0 and all kernel
parameters are fixed, not fitted to these statistics. The primary sample
uses Q<=2, inclination>=30 degrees, at least six eligible positive-force
radii, and R>=R_disk. Signed gas contributions are retained; a negative
gas contribution alone is not an exclusion.

Coherent multiplication of all g values in a galaxy cancels from D and J.
This removes a common dynamical-acceleration normalization under the stated
catalog rescalings. It does NOT remove radial warps, changes in baryonic
deprojection, mixed gas/stellar mass errors, radial M/L gradients, or a
shift in dimensional b at fixed a0. No universal inclination-free
model-residual claim is made.

## 4. Primary empirical results

RMS residuals are in dex, equally weighted per galaxy. They are descriptive
scores, not chi-square probabilities.

| Fixed response | Two-point RMS D | Three-point RMS J |
|---|---:|---:|
| Requested mu_exp | 0.16664 | 0.08183 |
| RAR exponential | 0.16694 | 0.08067 |
| Simple mu | 0.16921 | 0.08101 |
| Pure deep MOND everywhere | 0.21560 | 0.08092 |
| Newtonian baryons only | 0.50394 | 0.08092 |

For D, the paired mean-squared-residual difference (mu_exp minus rival) has
1999-draw whole-galaxy bootstrap 95% percentile intervals:

- versus RAR: [-0.002566, +0.002276] dex^2 — no clear preference;
- versus pure deep MOND: [-0.026896, -0.010367] dex^2;
- versus Newtonian baryons only: [-0.271898, -0.181555] dex^2.

This is evidence that the transition response is useful relative to those
two limiting baselines, within this design. Newtonian baryons only is not
a fitted dark-halo or full LambdaCDM competitor. Beating it is not a test
against the full dark-matter paradigm. The RAR law was originally calibrated
on SPARC, so this is not independent data confirmation of that law either.

The primary observed mean J is -0.00685 dex, with a resampling interval
[-0.02382, +0.01048]. Predicted means are -0.02757 for mu_exp and -0.02425
for RAR. The mean mu_exp residual is +0.02072 dex, interval
[+0.00406, +0.03776]. That primary conditional offset is not robust enough
to claim new physics or a clean rejection of the full theory.

The median observed finite slope D/log10(b_hi/b_lo) is 0.6395. About 75.6%
of raw selected triples have endpoint slopes between .5 and 1, and 56.4%
have J<0. These fractions are not a certificate that every true force obeys
the inequalities. Six galaxies fall below the slope bound and six above
J=0 by more than two propagated catalog-velocity standard errors. Those
errors exclude baryonic and other systematics; the violations are retained
in the data, not silently removed or advertised as full-theory refutations.

## 5. Robustness, covariance and negative controls

All prespecified sensitivity runs are reported, not only favorable ones.
Intervals below concern mean J_obs-J_exp, in dex.

| Selection / assumption | Galaxies | Mean residual | 95% resampling interval |
|---|---:|---:|---:|
| Primary | 78 | +0.02072 | [+0.00406, +0.03776] |
| Disk M/L=.3 | 76 | +0.00723 | [-0.00993, +0.02512] |
| Disk M/L=.8 | 84 | +0.03312 | [+0.01620, +0.05132] |
| Q=1, inclination>=45 | 52 | +0.01430 | [-0.00436, +0.03244] |
| R>=.5 R_disk | 87 | +0.03699 | [+0.01820, +0.05867] |
| R>=2 R_disk | 70 | +0.00573 | [-0.00981, +0.02230] |
| Alternative a0=1.13e-10 | 78 | +0.01765 | [+0.00094, +0.03464] |
| Gas fraction>=.8 at all three points | 1 | — | No population inference |

Changing M/L can also change the baryon-selected triples and sample; these
runs do not isolate the effect of M/L on a fixed set of physical points.
Neither arbitrarily lowering M/L nor changing the radius cut after seeing
the outputs is a validated rescue. The table demonstrates the fragility
of an interpretation, not a preferred new fit.

A deterministic name-hash split gives 36 and 42 galaxies. The J residual
interval excludes zero in one half but includes it in the other. Both halves
are familiar SPARC data; this is a replication diagnostic, not blinding.

With weights t, the contrast matrix is
C=[[-1,0,1],[t-1,1,-t]]. The joint covariance is calculated as C Sigma C^T;
the two statistics are not treated as independent measurements. Catalog
velocity errors use the first-order log transformation
sigma_log10g=2 sigma_V/(V ln10). Full inter-ring and baryonic covariance is
unavailable. Whole-galaxy bootstrap preserves the paired observed/predicted
contrasts but cannot manufacture those missing uncertainties.

All six implementation controls pass: synthetic exact-law recovery,
common dynamical normalization cancellation, common-mode covariance
cancellation, conditional log-Gaussian noise-variance recovery, a reversed
force mutant that violates the compression bound, and a concave mutant
that violates the predicted J sign. Empirical-to-analytic noise variance
ratios are 0.9671 and 1.0248 for D and J. A within-triple force permutation
raises the RMS to 0.9828 and 0.4489 dex; this checks dependence on pairing,
not independent evidence for the physical law.

## 6. Novelty and the next decisive calculation

The literature search found established logarithmic-slope comparisons,
normalized rotation-curve observables, equal-acceleration branch tests,
and RAR hooks/bends. LITERATURE.md records primary sources and the bounded
search scope. The finite response and Jensen inequalities are formal
corollaries; the combined implementation and empirical comparison are new
work in this directory, not established global priority.

The next useful calculation is to propagate independent photometric/gas
profile uncertainties and a matched disk/external-field solution through
the SAME fixed contrasts. The particularly interesting unresolved quantity
is whether the J offset survives on fixed physical triples after those
corrections. The independent-observation step then needs galaxies with
both measured rotation curves and independently determined baryonic
profiles. Local WALLABY kinematics alone do not supply the latter. Fitting
baryonic profiles from the velocities being tested would be circular.

Fable's concurrent f26 disk-forward work arrived during this study. It was
inspected as a possible next input, not silently incorporated as an exact
AQUAL prediction. Its cached QUMOND templates and differing profiled M/L
require matching source geometry, radii, normalization and numerical
convergence before they can replace the present algebraic predictions.

**Scientific status: useful finite tests implemented; exponential-vs-RAR
selection OPEN; new empirical law NOT ESTABLISHED; relativistic closure
still OPEN.**

## 7. Files, execution and reproducibility

All new files are confined to this directory:

- CONTRACT.md, DERIVATION.md, LITERATURE.md, REPORT.md;
- response_math.py and test_response_math.py;
- empirical.py and test_empirical.py;
- render_results.py and test_render_results.py;
- run_study.py and test_run_study.py;
- results.json, finite_interval_results.png, audit_output.txt,
  computation_manifest.json.

From the repository root, regenerate the study with:

```bash
python3 qwen_claude_field_theory/closure_2026/finite_interval_mond_2026/run_study.py
```

The runner records the exact interpreter, arguments, working directory,
environment, runtime and exit status of each important command in
audit_output.txt and computation_manifest.json. It runs all new unit tests,
the symbolic derivation, the empirical study, the plot, the existing
two_kernel_orbit_shape_2026 regression suite, and its action/orbit script.
Read the manifest for final fresh statuses; a zero runner exit certifies
execution/checks only, never a new physical theory.

During development the tests first failed for missing implementations.
Additional failures exposed an unintended negative-gas exclusion, NumPy
boolean JSON serialization, and a singleton-bootstrap reporting problem;
regression tests were added before correcting them. The first empirical
CLI exited 1 at serialization; the corrected run exited 0. Plotting exited
0; initial font-cache warnings were environmental, not empirical output.
No unrelated working-tree edits were changed.
