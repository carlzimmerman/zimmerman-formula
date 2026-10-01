# Scoped audit and continuation

Primary verdict for the full gravity objective: **incomplete**. The exact
measurement propositions are proved under the stated scalar-law, source-map
and response assumptions. Their empirical applicability is conditional.
Reviewer: same assistant, with separate algebraic and numerical checks.

## Claim dependency and audit

`Q identity -> geometry-weighted moment -> spatial response correction ->
Poisson covariance -> constrained scale estimator` is the first chain.

`Common Gaussian convolution -> width elimination -> convex inverse map ->
two-scale counterexample -> sixth-moment separation` is the second.

`Spatial correction + nonnegative effective source weights -> increasing RAR
fourth-moment map -> unique positive RAR scale` is the third.

| Obligation | Status | Scope |
|---|---|---|
| Dimensions, signs, weights | Passed | q=p²r; unnormalized flux moments; one scale per system |
| Radius/projection variation | Passed | Known maps; no projection division |
| Symmetric broadening | Passed | Finite known moments; third noise moment zero |
| Independent line integration | Passed | Gaussian and uniform cases; later independent GH quadrature |
| PSF correction necessity/sufficiency | Passed | Linear correction for all latent second moments |
| Noise covariance | Passed | Poisson exposure-normalized moments; analytic derivation plus Monte Carlo |
| Unknown-width identifiability | Refuted in general | Explicit positive-width two-scale example; full spectra remain different |
| Convexity of H | Passed | Squared-sum inequality; single-B affine/zero-slope exception identified |
| Optimized linear estimator | Passed as a constrained formulation | Finite solves tested for feasibility, KKT stationarity and objective bounds |
| Exact invariant after coarsening | Absent for tested varying-width map | Nuisance rank stable across three numerical cutoffs; not a global inverse-problem no-go |
| RAR uniqueness | Passed | Nonnegative effective source weights, positive source sensitivity |
| Empirical/relativistic closure | Not addressed | No real spectra, action, stability or lensing computation |

The constrained-optimizer audit checks its objective lies between the
unconstrained optimum and the original feasible inverse, and checks that the
gradient is represented by an equality multiplier plus nonnegative active
inequality multipliers. This is a finite floating-point KKT check, not an exact
symbolic optimization certificate.

No new theoretical paper was used. No historical novelty statement is earned.
The source field, intensity, geometry and noise maps are explicit synthetic
inputs. Dark energy versus H scaling and both dimensional normalizations remain
separate. The Q estimator was deliberately tested on RAR data as a wrong-law
control, then replaced by an actual RAR inversion for that branch.

## Failure accounting

All four bounded stage runs completed and validated. A preliminary exploratory
root bracket for a different two-population contrast did not enclose a root;
no scientific result was taken from that failed bracket. The saved example
uses a bracket that does enclose the root and independently integrates both
line profiles. No post-run scientific input was modified.

Two mathematical failures are retained as results, rather than patched away:
the second/fourth-moment scale ambiguity and loss of a universal exact linear
invariant after coarsening with varying width. The large noise of the original
inverse is also retained alongside the improved estimator. No adverse empirical
observation was removed or refitted in this stage.

## Exact remaining implications

1. **Measurement applicability:** obtain a source/line data product and its
   independently calibrated spatial and spectral responses. The cached rotation
   tables used in the parent stage do not carry the requisite fourth/sixth
   moments. Evaluate the response-matrix rank and calibration uncertainty
   before treating a scale estimate as a gravity test.
2. **Joint inference:** source-map uncertainty, inclination, distance, emissivity
   selection, noncircular motion, background and temperature must enter the same
   likelihood. None is allowed an arbitrary per-object correction simply to
   force agreement. Spatial second moments or full spectra may break the toy
   degeneracy even when a single integrated second/fourth pair cannot.
3. **Physical completion:** the moment relations assume the scalar force law.
   They do not show how that law follows from conserved relativistic dynamics
   or how it produces the extra cluster response at matched baryonic field.
   The source-budget requirement established in the parent stage is unchanged.

The useful next mathematical route is a joint scale/width response-rank analysis
using spatial moments, followed by a synthetic full-spectrum fit with uncertain
source maps. It must compare against the exact degeneracy before making a
claim of identification. A real-data result awaits the measurement inputs above.
No background computation or scheduled continuation is running after this
checkpoint; the preserved scripts and contracts supply the next starting point.
