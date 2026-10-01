# Self-review and research handoff

Date: 2026-09-27. Reviewer: same assistant, separate adversarial pass; not an
independent-agent review. Base checkpoint/revision and disjoint write scope are
in CONTRACT.md. No executable `.mathbox` ledger was present at the root.

## Normalized claim and verdict

**Primary proof verdict: proved as written** for the restricted mathematical
statements below, with the exact assumptions in DERIVATIONS.md. The application
to real unresolved galaxies is **conditional on the measurement model**.
The requested complete gravitational/empirical explanation is **incomplete**.

Claim objects: positive random variables B with finite second moments;
nonnegative normalized weights; constant a>0 within each average; the specified
scalar static relation; and, for the spectral map, circular elements with
common r and nonzero projection p and independent known Gaussian broadening.
Infinite-variance distributions and unmatched weights are excluded.

| Claim / dependency | Review status | Evidence and limit |
|---|---|---|
| Q moment closure and sign | Passed | Average the pointwise polynomial; variance identity and F'>1; derivative independently symbolic |
| Gaussian line-moment inversion | Passed | Direct fourth-power expansion and continuous line-profile quadrature |
| Q distribution-free hiding bound | Passed | Exact second moment minus the specified squared mean; nonnegative Var(B) |
| R distribution-free hiding bound | Passed | 1-exp(-t)=integral_0^t exp(-s) ds <= t, then square and average |
| Universal R concavity | Failed as a proposed extension | Positive Jensen gap for equal weights at B/a=9 and 11; do not transfer Q sign theorem |
| Wrong variance-correction sign | Failed control, as intended | Does not recover the input a₀; saved in bounds results |
| Lognormal deep-limit hiding formula | Passed for exact deep law | Analytic Gaussian moment and independent quadrature |
| Applying deep formula to full transitions | Restricted | AFG-002 solves Q/R exactly; fourth moment can be dominated by the non-deep tail |
| Q/R/M inverse budgets | Finite verification passed | Inverse/forward relative errors <=2.4e-14 on 121 tested accelerations per kernel |
| Observational calibration / significance | Not addressed | No joint distance, inclination, M/L, temperature, pressure or covariance likelihood |
| Instrument-model applicability | Conditional | No raw spectra, PSF/LSF or matched baryonic weighting supplied to these calculations |
| Relativistic / cosmological closure | Not addressed | No new covariant action, lensing solver, perturbation or Boltzmann calculation |
| Historical novelty | Not addressed by design | No literature search requested or performed |

No external theorem is a proof leaf. The static kernels, scales and cached data
are inherited inputs, not new theorems. Basic calculus/variance/Gaussian moment
steps are derived in the notes. The M numerical implementation follows the
existing L340 definition; its theoretical dynamics are not copied into a new
claimed construction.

## Computational provenance and failure accounting

* `run_001`: computation reached JSON serialization, then failed on a NumPy
  integer count. Reproduced the specific int64 serialization failure; converted
  the count at its source. This run has no scientific result artifact.
* `run_002`: completed empirical/synthetic run. NumPy, SciPy, SymPy, Astropy,
  Python versions, inputs, bounds and results recorded in its v2 manifest.
* `run_transition_001`: completed full-Q/R lognormal root calculations, 24
  cells. Direct Q second-moment identity independently checks quadrature;
  Gaussian integration range expanded from ±12 to ±14 with relative change
  below 1e-8. The analytic baryonic moments include the full tail.
* `run_bounds_001`: completed separate algebraic checks of all 24 cells and
  two false-rule controls. Written inequalities supply the universal reasoning.

The initial runner launch also rejected an absolute output path before starting
the run; switching its output argument to project-relative addressed that CLI
requirement. No mathematical failure was relabelled as an environment issue.
Earlier failed-run input freshness is intentionally superseded by the repaired
run; completed evidence inputs remain pinned and unchanged.

FITS units were inspected directly: hydro/gas masses in Msun, stellar masses in
M_sun; hydro and stellar radii in kpc; gas radii decoded from each file's R/R500
and its own header R500. Shared NFW mass columns agree to <0.1% median per
cluster after that conversion. They are used solely for the unit alignment
check, not as a new assumed dark halo or mass model in the MOND calculation.
Five clusters lacking their own stellar profiles were excluded rather than
imputed. No profile is extrapolated. Central hydrostatic mass remains a
model-dependent inferred acceleration.

## Research decision and next work

**Keep the measurement-moment route open.** It has a new exact conditional
prediction, not a completed observational test. The first missing input is a
spatially resolved spectral cube or equivalent line profiles with PSF/LSF,
noise covariance and a baryonic map that can be passed through the same weights.
A filename search under `real_research/data` for spectra, datacubes and PSF/LSF
found no matching files; the cached rotation tables do not contain fourth line
moments. This is a bounded search, not proof that no such data exist anywhere.

Executable next package when those inputs are available:

1. Select one system or a matched stack with geometry constrained independently;
   freeze the masks, projection, systemic velocity and brightness weights.
2. Predict the *full observed spectrum* for Q and R separately, on both a₀
   normalizations and vacuum/H branches. Convolve with measured PSF and LSF.
3. Inject spectra with realistic noise and spatially varying broadening. Recover
   the raw second/fourth moments; reject the estimator if calibration creates a
   gravity-like signal comparable to the predicted separation.
4. Test the bound after marginalizing those nuisance parameters. Count a failure
   of the spectral geometry as failure of this measurement application, not as
   falsification of the general core framework.

**Keep the source-budget route open, with a concrete target.** At 300 kpc a
measurement explanation for the canonical R cluster median must reduce the
hydrostatic-equivalent acceleration to about 31% of its present value at fixed
baryons. Changing baryons instead requires about six times the catalogued
source inside the kernel. A new mechanism must explain the cluster/galaxy
difference at matched B and predict lensing and dynamical tracers together.
Do not substitute an arbitrary object-by-object a₀ or cite the Newtonian
missing mass as a MOND calculation. A same-cluster lensing/thermal-pressure/
galaxy-kinematic forward likelihood is the next discriminating empirical input.

**Do not promote the hidden-evolution construction to a new gravity theory.**
Lognormal heterogeneity is an illustrative distribution. Its covariance is
not derived from dynamics. A physical completion must produce that structure,
the requisite line shape and a conserved field/matter evolution while retaining
the galaxy fits. No calculation here earns those claims.

## Proofreading / presentation review

Definitions, branch labels, raw versus central moments, units, conditional
claims and numerical tables checked. No inherited source was edited. The
final notes distinguish a source inside the MOND kernel from an additive
Newtonian component, a scalar response average from solving a clumpy field,
and a common-geometry idealization from a real beam. No unresolved typographic
mathematical-token correction is being silently carried as a proof repair.
