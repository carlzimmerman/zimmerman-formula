# Independent precision audit of AFG-001–008

Date: 2026-09-27. Auditor: independently dispatched `proof_precision` agent.
Frozen Git base: `eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`.

**Primary verdict: correct only after a stated restriction.** The exact
moment, convexity and positive-weight inversion arguments hold in the stated
finite, positive-baryonic-acceleration model, with known maps and response.
The necessity claims for correction/linear invariants, when interpreted as
law-independent cancellation for arbitrary luminous-source velocities, require
restriction to the luminous support, or the added assumption that every
retained I_i is strictly positive. A source cell with I_i=0 is permitted in S1 but
cannot carry arbitrary latent x_i=I_i u_i². The supplied disk has I_i>0
everywhere, so this correction changes no reproduced numerical result.

The derivations establish conditional measurement identities and obstructions.
They do not establish physical closure, independent calibration of nuisance
maps, an empirical gravity discrimination, or an observational photon forecast.
The original derivations explicitly make those limitations; this audit found
no justification to strengthen their physical interpretation.

## Independence and artifact identity

The raw parent and stage_02 DERIVATIONS.md files were read before any prior
audit/README verdict narratives. Those narratives were never consulted.
Reconstruction used elementary expansions, linear algebra, a pairwise
convexity identity and direct integration. No literature search or imported
theory was used. No original campaign artifact was modified. The checkout is
dirty and the campaign is untracked; Git alone does not identify the proof.
`read_files_sha256.json` pins all 12 reviewed original code/contract/proof
files. Both successful version-2 run manifests additionally pin those files
before and after execution. There were no applicable AGENTS.md files found in
the inspected ancestry or campaign, and no project-root .mathbox ledger.

The independent program imports no campaign implementation. The separate
reproduction wrapper executes the original four stage_02 modules and is
explicitly shared-code reproduction, not a second independent implementation.

## Claim cards and verdicts

| Claim and exact domain | Verdict | Decisive obligation |
|---|---|---|
| Q closure and mean bias: normalized common nonnegative weights, B>0, a>0, finite second moments | proved as written | E[g²]=E[B²]+aE[B]; Var(g)>=Var(B) follows from F'>1 and independent copies |
| Common-geometry Gaussian raw-moment deconvolution | proved as written | Conditional independent zero-mean Gaussian noise, known common s²; raw m4−6s²m2+3s⁴=E[u⁴] |
| S1–S2 geometry-varying Q identity | proved as written | Finite positive C1 and the same source weights throughout; q=p²r>=0 |
| S3–S6 PSF correction and bias | proved as written for sufficiency/bias; correct only after luminous-support restriction for necessity | Exact expansion plus the counterexample below |
| S7–S8 Poisson covariance and finite variance | conditional on named input | Known exposure/flux normalization, independent Poisson pixels, finite eighth line moments |
| S9–S11 H convexity, strictness and endpoint derivatives | proved as written on finite B_i>0 support | Explicit nonnegative pairwise formula below; strictness requires two distinct B with w_i q_i>0 |
| Constructed a=1 versus E(3) two-moment ambiguity | computationally verified only in the stated example | Independent root/recurrence reproduces both moments and positive widths |
| S12 Gaussian invariance and sixth-moment distinction | proved as written for algebra; finite precision forecast conditional | Sixth-moment expansion; asymptotic variance also needs finite order-12 moments and fixed iid sample size |
| S13–S15 optimal linear estimator | proved as written for an unrestricted formal nuisance x; correct only after support restriction for the physical x=Iu² necessity claim | Restrict D to active columns, then solve one constrained positive quadratic form |
| Common multiplicative width-calibration no-go | proved as written in its specified class | Positive widths on luminous support force h4 orthogonal to the signal |
| S16 positive-weight RAR inversion | proved as written for the finite source model | Strict monotonicity and continuous range (baseline,infinity) |
| Finite positive-weight constrained optimizer | implementation and finite assertion verified in stated range | Original solver/residual/KKT checks reproduced; no exact optimization certificate |
| Q and R distribution-independent spectral lower bounds (14)–(15) | proved as written | Q identity; R pointwise F²>=aB; shared positive weights and specified target mean |
| Lognormal transition numerical examples | implementation and finite assertion independently verified in stated range | 24 roots and direct full-response quadratures, with Q second moment checked afterward |
| M bound transfer | conditional on named input | Exact continuous derivative-majorant definition, same initial value and defined domain; discretized quadrature/interpolation is not itself an exact proof |
| Cached cluster profile numerical claims | out of scope of this proof/computation pass | Inverse algebra inspected; raw FITS profiles and catalog reductions were not independently re-audited here |

“Proved as written” above refers to each normalized mathematical claim, not to
the whole physical research program. S7–S8 do not follow from merely finite
fourth moments: for example symmetric Student-type tails with finite fourth
but infinite eighth moment preserve S3 while giving an infinite fourth-moment
estimator variance. The Gaussian/uniform numerical examples have all required
moments.

## Dependency graph

1. Pointwise static Q law + circular geometry u²=qg -> intrinsic fourth moment
   -> S2 scale identity. Leaves: adopted law and dynamical/geometry assumptions.
2. Source-conditional line moments + velocity-independent known spatial response
   -> S3 expansions -> adjoint cancellation -> S4/S6 -> Q estimator, or the
   separately inverted RAR map. Leaves: known I, B, q, P, s², k, units and rest frame.
3. Independent Poisson arrivals + fixed exposure normalization + finite eighth
   moments -> covariance -> S8 variance -> finite design covariance C.
4. Unrestricted nuisance cancellation on luminous support + signal normalization
   + positive-definite C -> S15 restricted-class optimum. Numerical solver
   accuracy/rank cutoffs remain computation leaves.
5. Unknown common Gaussian variance -> elimination using m2 -> H(a) -> pairwise
   convexity -> possible two roots. Known fourth/sixth moment expansions -> J6;
   finite twelfth moments + iid delta method -> asymptotic precision only.
6. Shared weighted target mean + Q moment closure, or R pointwise bound ->
   spectral lower bound. The lognormal family is an optional example, not a
   dependency of the universal bounds.

No circular implication was found. A universal law or calibrated map is an
assumption at the leaves; agreement with moments cannot prove the leaf itself.

## Exact counterexample and corrected necessity statement

Take one recorded beam and two source cells:

    P = [1 1], I = (1,0), s² = (1/25,4/25), l4 = 1, l2 = 1/25.

Then alpha=(1,1) and delta=s² alpha−P^T l2=(0,3/25). Full S5 fails,
and s² alpha is not in row(P). Nevertheless

    sum_i I_i delta_i u_i² = 0

for every physical source velocity. Correction is exact. This is a rational
counterexample, not numerical rank sensitivity. It satisfies I_i>=0 and can
have a strictly positive Q denominator (choose q_1=B_1=1).

Let A={i:I_i>0}. For arbitrary unconstrained velocities u_A², the exact
necessary and sufficient correction is

    (P^T l2)_A = (s² alpha)_A,

equivalently diag(I)(s² alpha−P^T l2)=0. Solvability is membership of
(s² alpha)_A in row(P_A). For necessity, x_A=I_A u_A² ranges over an open
positive orthant; a nonzero residual on A cannot annihilate every x_A.
This makes precise the positivity perturbation argument in the original text.
It deliberately enlarges the physical circular-model family. If q_i=0 then
u_i²=q_i F(B_i;a)=0 even when I_i>0; arbitrary variations of that coordinate
are not physical. Restricting only by this geometry permits an active set
{i:I_i>0 and q_i>0}. Restricting further to a common Q/R scale imposes additional
relations between the remaining coordinates. Necessity for that smaller
family must be derived from its actual allowed span, not inferred from the
open-orthant argument. The three quantifiers—every formal x in R^n, every
unconstrained luminous-source velocity, and every physical circular-law
configuration—are distinct. The original S14 is unconditionally correct for
the first quantifier; the support-corrected statement addresses the second;
neither is a universal necessity result for the third.

The optimizer analogue uses

    D_A = (P_A; 6 P_A S_A),
    d = (0, P[I q²B]).

Existence requires d not in col(D_A), equivalently N_A^T d != 0, with
N_A spanning ker(D_A^T). In the counterexample choose q_1=B_1=1:
the full D has columns (1,6/25)^T and (1,24/25)^T, so its nullspace is zero.
The active D has only the first column. The estimator h=(-6/25,1) obeys
D_A^T h=0 and d^T h=1, hence recovers a exactly. The unrestricted full-column
criterion would incorrectly say no physical invariant exists.

The common-width-calibration no-go survives the correction: if S_A is
invertible, demanding cancellation for every nearby multiplier forces
P_A^T h4=0; the signal lies in the span of P_A, so h4^T c=0. Thus it cannot
also satisfy normalization. This remains a no-go only for fixed linear
estimators cancelling every supported latent vector and every such multiplier.

## Independent derivations of the load-bearing steps

For an individual source, expand E[(u+epsilon)^4] conditionally on the source.
Zero first and third noise moments give u⁴+6s²u²+k. Applying P and l4 and
subtracting l2 times the similarly expanded second moment gives S4 directly.
This needs P to act linearly on the relevant line moments with the same
source response; a velocity-dependent response requires a different operator.

For a Poisson point process with intensity N times a unit-normalized joint
source/pixel/velocity distribution, an estimator is N^(-1) sum phi(J,V).
Its variance is E[phi²]/N, without subtracting E[phi]². Taking
phi=l4_J V⁴−6l2_J V² gives S8, including the negative cross term. For a fixed
number N of iid photons the subtraction E[phi]²/N is required. The width
ambiguity precision calculation correctly uses the latter iid covariance.
If luminosities are dimensional or throughput loses photons, the meaning of N
must be adjusted consistently: a fixed exposure factor is not automatically
the expected detected count. The published synthetic I sums to one and P has
unit column sums, so no normalization mismatch occurs in those runs.

For convexity set c_i=w_i q_i>=0, g_i=sqrt(B_i(B_i+a)) and
t_i=1/(B_i+a). Direct differentiation yields the stronger explicit identity

    H''(a) = (3/2) sum_{i<j} c_i c_j g_i g_j (t_i−t_j)².

This proves nonnegativity and exactly identifies strictness. A finite support
with at least two distinct positive B values carrying c>0 is strictly convex.
Expanding g at a=0 and at infinity gives exactly S11. A zero asymptotic slope
does not imply a finite flat interval in the strictly convex case; the stated
nonincreasing conclusion remains valid. The affine one-B zero-slope exception
is correctly retained in the proof.

For RAR, write t=sqrt(B/a). Then dt/da=−t/(2a), and

    dF/da = B exp(−t)t / [2a(1−exp(−t))²] > 0.

Finite nonnegative coefficients alpha I q² with at least one positive entry
give strict monotonicity of their weighted F² sum. At a down to zero the
baseline is sum alpha I q²B²; at a to infinity, F²/a tends B and the sum
diverges. This proves existence/uniqueness for every target strictly above the
baseline. It does not identify a for signed alpha, unknown maps, or an observed
noisy target below the physical baseline. Binary64 may round exponentially
small changes to zero near the Newtonian limit; that is numerical conditioning,
not a failure of exact strict monotonicity.

For the Q bound the target mean squared is b²+a_today b, while the actual
second moment is b²+Var(B)+E a_today b. Their ratio gives (14), with strict
inequality under E>1 and the target mean condition because constant B cannot
satisfy that mean. For R, 1−exp(−t)<=t implies F²>=aB, giving (15).
These are acceleration-distribution bounds with identical nonnegative weights.
They cannot be applied unchanged to the signed-source optimized estimator or
to a geometry-varying observed line ratio that no longer equals <g²>/<g>².

## Numerical results and provenance

Independent run: `run_003/results.json` and `run_003/manifest.json`.
It uses rational arithmetic for the support counterexample, a Gaussian moment
recurrence derived by integration by parts, direct quadrature of actual
one-photon polynomials for two PSF cells under Gaussian/uniform broadening,
and direct integration of the full Q/R response against a normal density.
The latter uses integration extents 20 and 24, independently of the original
baryon-plus-phantom decomposition.

The independently reconstructed ambiguity has
B=(0.008571665531663905,0.8571665531663905), weights (.9,.1), common
m2=0.493808155332989 and m4=0.766396782574311. Width variances are
0.283956278498687 and 0.1; J6 values are −0.0467698175428901 and
−0.112873394103189. The larger-variance fixed-model iid delta-method threshold
is 22950.1039199 photons. This calculation supplies no nuisance-fitting,
background, systematic-calibration or finite-sample error guarantee.

All 24 (z,q,kernel) transition cases passed independent mean/root checks and
the lower bounds. At z=3, q=.01, Q gives CV=21.89085518, K=9.274978109 and
bound 4.530329194; R gives CV=21.04810308, K=9.002912400 and bound
4.134598888. At q=.1 the respective K are 77.95342063 and 42.21078896.
The Q second moment was checked against q² exp(S)+E q after the independent
quadrature. These remain finite binary64 checks, not certified interval bounds.

Shared-code reproduction: `reproduction_001/results.json` and its manifest.
All four original stage_02 modules and assertions pass. Reproduced values:

| Quantity | Value |
|---|---:|
| Poisson analytic sigma, 5000 expected photons | 0.184920860699028 |
| Poisson empirical sigma, 400 realizations | 0.186240545214536 |
| Empirical/analytic variance ratio | 1.01432389470102 |
| Direct scale-1 sigma at width .4, 10000 photons | 0.0463558259838671 |
| Direct scale-1 sigma at width 1 | 373.833336879394 |
| Optimized Q scale-1 sigma at width 1 | 0.422194135919161 |
| Positive-weight RAR local sigma at width .4 | 0.0457528936416493 |
| Positive-weight RAR local sigma at width 1 | 0.641620583802946 |
| Coarse varying-width D smallest/largest singular value | 0.00182974456559374 |

The rank is 32 at each of 1e-10, 1e-12 and 1e-14 relative cutoffs. This is a
robust finite numerical observation, not an exact determinant certificate.
The width-1 PSF condition number is about 7.02e9, explaining the sensitivity of
the direct inverse. Constrained optimality is supported by finite residual/KKT
checks, not an exact minimizer proof for the floating solution.

The original scripts assert noiseless recovery and their scoped finite controls.
They do not certify real-instrument calibration or replace full nuisance
likelihoods. RAR inversion error bars are local delta-method quantities, and
the optimizer's covariance was designed under Q at a=1 as disclosed.

## Failed audit runs retained transparently

`run_001` failed an audit-script absolute tolerance of 2e-15 when two equal
convexity formulas differed by 5.33e-15 at magnitude 13.00086. The script was
corrected to a scaled 1e-14 tolerance; its exact failed version is retained as
`independent_checks_v1_failed.py`. This was an overly strict binary64 check,
not a counterexample to convexity.

`run_002` then failed strict floating monotonicity at very small a where the
RAR correction is below binary64 resolution. The tested grid was restricted
from [1e-8,1e8] to the resolvable [1e-3,1e8] range; the exact proof above
still covers every a>0. Its failed version is retained as
`independent_checks_v2_failed.py`. Failed manifests retain original hashes;
their former execution path now names the corrected script, so failed-input
freshness must be checked against the archived version, not the current file.
Both failures are explicitly audit-check issues and not silently erased.

Successful manifests were validated using the installed computation-audit
`validate_manifest.py` with `--root` set to this repository. Actual commands,
Python/numpy/scipy versions, dirty Git state, runtime, fixed RNG seed for the
reproduction, output hashes and cooperative one-thread cap are recorded there.

## Supplemental exact map-rescaling check

At the parent's request, independently substituted both laws into
F(cB;ca)=cF(B;a), c>0. It holds exactly for Q and RAR. Thus
(B,a,q)->(cB,ca,q/c) preserves u²=qF(B;a) and, if signs, I, P and conditional
broadening stay fixed, preserves the entire modeled spectrum. This confirms
the algebraic symmetry only. It requires the simultaneous map rescalings to
be admissible nuisance changes; real mass, distance, radius, inclination and
photometric constraints may couple or break them. No empirical plausibility
claim follows from the symmetry alone. This paragraph checks the stated
identity, not the parent's new implementation or its result files.

## Exact remaining gaps and next check

The minimum required proof correction is to restrict every physical latent
necessity/rank statement to I>0 support. No rerun of the strictly luminous
synthetic disk is needed to repair that hypothesis. Finite variance claims
should explicitly require eighth moments (twelfth for the J6 delta method)
and a consistent known flux/exposure normalization.

The strongest safe conclusion is an exact, conditional measurement test for
each separately specified static law, with an explicit two-moment ambiguity
and scoped linear-estimator calibration obstruction. The cheapest useful next
check is joint identification with externally constrained baryonic, geometry
and width nuisance parameters, including the exact rescaling direction above.
More noiseless synthetic recovery with the same fixed maps cannot close that
gap. The broader gravity program still needs common dynamics, lensing,
cosmology, conservation, stability and a calibrated data likelihood.
