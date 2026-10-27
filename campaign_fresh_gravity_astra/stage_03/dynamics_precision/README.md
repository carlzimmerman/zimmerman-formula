# DP1 dynamics checkpoint: a conservative survivor, with quantified missing dynamics

The radial Q/R laws do **not** determine a dynamical theory. This lane proves
the exact curl condition, constructs a conditional conservative nonspherical
extension, and progresses that construction through conservation and linear
time evolution. The resulting family retains an unconstrained kinetic
coefficient. Neither this mathematical survivor nor its static variational
form is a relativistic or empirical completion.

## Earned results

1. Direct pointwise vector rescaling is refuted by an exact harmonic vacuum
   tidal field. At the witness point its dimensionless curl is
   0.1414213562373095 for Q and 0.1841347188415585 for R. Small-loop integration
   reproduces both and converges as the loop shrinks.
2. Under newly declared single-scalar, local, isotropic first-gradient
   assumptions, W'(g)=F^{-1}(g) produces a conservative Gauss-law field. It
   recovers the registered radial law for spherical sources; no equality with
   pointwise rescaling is asserted outside that symmetry. Strict convexity
   gives uniqueness of a bounded-domain weak static solution with prescribed
   Dirichlet data; ellipticity degenerates at zero field.
3. Adding K phi_t²/(8 pi G c²), K>0, gives an explicit preferred-frame dynamical
   family. Its energy/momentum exchanges cancel those of universally coupled
   smooth matter. On a nonzero uniform-gradient background the field modes have
   positive quadratic energy and a hyperbolic principal symbol. This is not
   nonlinear/global or coupled matter stability.
4. Exact static predictions are independent of K. K=2 and K=8 are both
   analytically sufficient to keep these field characteristics <=c for Q and R,
   but their response times differ by exactly 2. Even in this restricted family,
   at least one independent kinetic coefficient remains missing. More general
   gradient-dependent kinetic coefficients leave a whole function unmeasured.
5. A **further restricted** Lorentz-invariant, first-derivative one-scalar P(X)
   action fixes the time coefficient to mu. Its radial characteristic speed
   squared is c² d log B/d log g, strictly between c² and 2c² for both laws.
   This conflicts with an explicitly imposed metric-light-cone condition;
   it is not a general acausality or relativistic-completion no-go. At B=a,
   the speeds are 1.15470c (Q) and 1.18761c (R). The static law also leaves the
   timelike X<0 branch unspecified.
6. A prescribed time-dependent a contributes W_a a_dot/(4 pi G) to energy
   balance. For the separate a proportional to H prescription, its deep-limit
   value is +(3/2)H Omega_m W/(4 pi G); a physical scale sector must supply the
   opposite exchange. A constant vacuum a has no such explicit source.

Detailed hypotheses, algebra, boundary conditions and non-claims are in
`DERIVATION.md`. Both 9.3619e-11 and 1.1279e-10 m/s² are carried; no M-law or
literature mechanism was substituted. No historical novelty is claimed.
STANDING's prior curl warning and empirical exclusions remain in force.

## Finite verification

`run_002` is the accepted run: **26 checks passed**, exit 0, manifest validated
against the repository root. Numerical arithmetic is binary64, not interval
certified. The analytic bounds have separate proofs in the derivation.

The 1,601-point derivative/symbol grid spans 1e-8 <= B/a <= 1e8. Four loop sides
range from 0.02 to 0.0025. A ten-cycle oblique wave is evolved with 1,000, 2,000
and 4,000 steps for each law and each K; continuum error decreases by about 4
on step doubling, and relative drift in the exact discrete quadratic energy
stays below 3.3e-13 on the finest runs. That discrete invariant is correctly
distinguished from the continuum energy of the numerical trajectory.

The finite R maximization on 0.01 <= sqrt(B/a) <= 30 gives
lambda_parallel=1.0335355992704114 at B/a=6.634121653662062. This is not a
certified global maximum. The global analytic sufficient bound is K=2.
The positive K=1 crossing is B/a=2.5396382821881645, above which K=1 violates
the chosen speed bound for R. For Q the exact sharp constant bound is K>=1.

The local energy/momentum check uses the explicit smooth manufactured potential
in the script at (t,x,y)=(0.6,0.4,0.7), K=2, c=4 pi G=1, with difference steps
0.002,0.001,0.0005. The scale is either 1 or 1+0.1 sin(0.3t). The source is
defined from the field equation and is not a claimed matter solution.
At the finest step, energy residuals are <5.18e-11 and momentum residuals
<3.63e-9. Omitting the explicit variable-scale exchange leaves energy residuals
-0.00902856446 (Q) and -0.00871958844 (R), over eight orders larger than the
correct residual. The separate E(z) table evaluates z=0,0.5,1,2,3.

## Preserved failed run

`run_001` stopped at a wrongly chosen test threshold: its code demanded the R
maximum exceed 1.04, whereas the claim only requires it exceed 1. The computed
value was 1.0335355992704114, so the test expectation was wrong. The corrected
check tests the stated strict inequality, while the numerical value remains
fully reported. This was not a mathematical counterexample to the derivation.

The exact failed script is retained as `failed_threshold_snapshot.py`, hash
`f79faa65af2947f17242305375400af16cb679a74e6f6629a8458c34a29f52e2`, matching
run_001's input record. Run_001's original live code path has since changed,
so a current-input freshness check against it would correctly report staleness.
It is preserved as a failure, not promoted to accepted evidence.

## Provenance and reproduction

Repository base: `eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`; shared checkout
dirty. All writes from this lane are beneath this directory. Exact file hashes
are required because the campaign itself is untracked. Accepted input hashes:

| Input | SHA256 |
|---|---|
| campaign_fresh_gravity_astra/CONTRACT.md | db5420f2d60310a6110c90d5354e0416b09e6f764ef48c833d098e29e7d30ebc |
| campaign_fresh_gravity_astra/stage_03/CONTRACT.md | f4e4a7bd8c7b4dceea48f8af0af1ce31f121d82a66fde57876ba3ff78020c05b |
| STANDING.md | 660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63 |
| DERIVATION.md | 41ad39d1521e7d5b5d974e320478faecd944df8d4608b4869a566624244af3ae |
| check_dynamics.py | ce72322a13d030f8675be1b99da98db8d9538651c2805481b2eb1dc60122ab60 |

Accepted results hash:
`bf9d8e2ed1e3ccc12adf2f4f9ea398923800d7319217786d52522321e5b00ad6`.
The version-2 manifest also pins the executed argv, actual Python/numpy/scipy
versions, unchanged inputs, output hashes, start time, runtime, CPU cap and
cooperative numerical-library thread cap. There is no random sampling.

From the repository root, a direct recheck preserving accepted results is:

```sh
python3 campaign_fresh_gravity_astra/stage_03/dynamics_precision/check_dynamics.py /tmp/DP1-recheck.json
```

The full accepted provenance command and limits are recorded in
`run_002/manifest.json`; the companion computational contract is
`computation_contract.json`. A fresh bounded rerun must use a fresh output
directory and pass its results path as the script argument. The manifest was
checked with the installed computation-audit `validate_manifest.py` and
`--root /Users/carlzimmerman/new_physics/zimmerman-formula`.

Self-review covered the full derivation and finite script. The coordinator
reports that the independent proof lane differentiated the energy, momentum,
scale-exchange and characteristic formulas at the exact DERIVATION hash above;
it did not audit the functional-analytic existence argument or this computation.
The statement in the derivation that no independent audit was performed
**within this lane** is literal; the cross-lane audit is separate evidence.
Final math proofreading was confined to this lane's new derivation and report.
No mathematical-token corrections were needed after the accepted run.

The next implication is specific: select the physical time/metric coupling and
an independently constrained kinetic law, then calculate source response and
lensing from that same action. No extra precision in static radial fits can
identify the demonstrated missing K by itself.
