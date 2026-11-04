# Constitutive response search with fixed baryons and cuts

**Checkpoint: none of the 14 accepted Milky Way model choices passes all four
original cuts.** The coarse t=1.52,p=6,epsilon=.20 case had a conservative
negative-mass upper bound 1.47813e-5 above its 1e-5 gate; it remains diagnostic
and its original JSON correctly flags the failure. The accepted replacement,
`../mw/constitutive_low_recheck_001`, reruns all 1,375 cells at spatial
refinement3 and harmonic order192: zero passes, max vc=217.5226209061 and
negative-mass bound1.19765e-6, passing every numerical gate. Thus there are
14 distinct accepted choices and 19,250 distinct accepted cell-model states;
including the discarded coarse version gives 20,625 population evaluations.
The full solver is applied to every survivor of
the necessary local-speed cut. This finite outcome is distinct from the 36
response instances in the initial Solar screen; those are neither 36 full
Milky Way scans nor six different response families.

The closest tested model is canonical cutoff (t,p,epsilon)=(1.587,6.3,.24),
original cell 1359. It has vc=220.45355 km/s and passes the local-speed cut,
but K0=71.03492 exceeds 70.8 and outer-curve chi-square=62.98577 exceeds
59.8925. Its vertical-profile chi-square is 38.57456 and scale length
h=3.19813 kpc; the strict scale-length condition also fails. The normalized
worst-cut score is D=1.0533899. The coordinator is separately refining this
closest case to assess numerical shifts; the quoted values are the saved
production grid, not certified continuum values.

`MW_CHECKPOINT.json` independently extracts the 14 cases and their count
and pass flags from the sibling `constitutive_grid_001` (4 cases),
`constitutive_continuation_001` (6) and `constitutive_edges_001` (4) records,
and hashes all three source result files. Its raw count/pass extraction does
not certify the numerical gates; its accepted replacement and the historical
exception above must accompany it.
It is a read-only extraction, not a new physical solve. No broader interpolating-function or geometric-response
impossibility follows. Arbitrary response functions, other actions and
geometric constructions remain unexhausted. No additional scan is pending
in this response folder.

This authorized exploratory search changes nu in the KT33 reciprocal energy.
It retains equal source/outer Gaussian widths and a common epsilon. No baryon
profile, a0 footing, Solar external field, physical conversion or observational
cut is adjusted. This folder supplies response functions and Cassini checks;
the sibling MW worker decides whether a candidate survives radial and vertical
forces. A Solar pass is not a joint pass.

## Exact static construction and parameter count

For any stated response nu, define

    H_nu(g) = a0^2 integral_0^(g/a0) t [nu(t)-1] dt,
    U_ph,nu[rho] = -(1/(4 pi G)) integral H_nu(|grad N rho|) d^3x,
    U[rho] = U_N[rho] + U_ph,nu[S_sigma rho].

Hold sigma fixed in a controlled source variation. Then

    H_nu'(g) = g [nu(g/a0)-1],
    Phi = N rho + S_sigma* Phi_ph,nu[S_sigma rho].

This is exactly the previous action architecture with a changed constitutive
function; the outer adjoint remains mandatory. On a finite nonuniform grid its
adjoint is W^-1 S^T W. The explicit response API is import-safe and does not
mutate the original solvers. The ordinary source-assigned sigma=epsilon r_M
still does not define one common unsplit-source law.

Write s(y)=1/(y[sqrt(1/4+1/y)+1/2]) for the simple excess. The initial families
are

    simple:    nu = 1+s,
    power:     nu_n = [1/2+sqrt(1/4+y^(-n))]^(1/n),
    cutoff:    nu = 1+s exp[-(y/t)^p],
    rational:  nu = 1+s/[1+(y/t)^p].

The power family adds one dimensionless shape parameter n. The attenuation
families add two dimensionless shape parameters, t and p. The transition
acceleration t*a0 is an additional fitted/adopted acceleration scale, although
no new dimensional constant independent of a0 is introduced. Epsilon remains
the existing third free model parameter. Choosing 1.5 or 6 does not derive
either number. The two a0 footings are not pooled.

For z=(y/t)^p the explicit derivatives are

    s' = -1/[2 y^2 sqrt(1/4+1/y)],
    nu_cutoff' = exp(-z)[s'-(p z/y)s],
    nu_rational' = s'/(1+z)-s p z/[y(1+z)^2].

For b=1/2+sqrt(1/4+y^(-n)),

    nu_n' = -nu_n y^(-n)/[2 y sqrt(1/4+y^(-n)) b].

Every positive n,t,p has sqrt(y) nu(y)->1 as y->0 and nu(y)->1 as y->infinity.
The cutoff/rational forms keep nu>=1 and nu'<=0. The additional condition
nu+y nu'>0 is checked numerically on 24,001 logarithmic points from 1e-12 to
1e12. That finite check is not a global proof or a health result for a
relativistic completion. For the sharply attenuated candidate t=1.5,p=6,
the minimum sampled total slope is only 0.027304 near y=1.4791.
Its exact slope can also be written

    d(y nu)/dy = 1+exp(-z)[s^2/(2s+1)-p z s].

This makes the risk from excessive steepness explicit. A positive total
slope does not imply monotone phantom acceleration or nonnegative phantom
density. Both are separate questions.

## Existing work and initial screen

KT13 previously tested eight local unfiltered QUMOND kernels, including n=2,
3 and 6, with the same baryon family. Those power variants lost radial
support; changing nu is not presented as a new idea. The older
FRIED_CHICKEN_SPEC already has an outer-adjoint filtered nu_mono action.
Neither prior record transfers an empirical pass to this changed operator.

The first declared grid has 36 response instances (simple, five power values
including duplicate n=1, and 30 attenuated cases), five epsilon values and two
footings: 360 Cassini rows. All sampled admissibility checks pass. The initial
screen is exploratory 3,000 radial by 80 angular quadrature; its largest
flux/density disagreement is 4.14e-5 in dimensionless q and it is not the
accepted accuracy basis for a marginal candidate.

The first useful low-epsilon candidate is cutoff t=1.5,p=6. It retains
0.998629, 0.915952 and 0.367879 of the simple excess at y=.5,1 and 1.5.
Canonical Cassini ratios to the unchanged ceiling are approximately

| epsilon | ratio | Solar quadrupole cut |
|---|---:|---|
| .15 | 1.11431138 | fails |
| .25 | .763787116 | passes |
| .30 | .961291891 | passes |
| .40 | .333409283 | passes |
| .50 | .035611177 | passes |

On the alternative footing the same candidate fails at .15,.25,.30,.40;
it passes at .50 with ratio .799511654. These values are not monotone in
epsilon, so no passing interval is inferred between rows.

`refine_001` is preserved as a failed evidence record: its criterion required
flux/density agreement below 2e-6 at *every* refinement level, while some
200-node angular rows had 3–4.2e-6 disagreement near the zero-field saddle.
All 400-node fine rows were below 7.5e-7. `refine_002` repeats the same
physical cases and the same tolerances with 400/800 angular nodes and
20,000/40,000 radial nodes, plus expanded domain. It completes with all
checks passing. This is empirical convergence, not interval certification.

The root MW worker reports the full 1,375-cell canonical t=1.5,p=6,
epsilon=.25 screen reaches only 219.49046 km/s (required 219.9); every cell
fails that necessary cut. That is a coordinator-reported result, whose full
provenance belongs to the MW sibling, not a calculation reproduced here.
It motivated a declared bounded continuation of t,p and epsilon in
`contract_continuation.json`. The original failure is not erased.

The continuation examines p=5,6,7, t=1.52,1.55,1.60,1.65,1.70 and six
epsilon values from .18 to .30. All p=7 cases in that rectangle fail the
sampled positive-total-slope condition and are rejected before observational
promotion. No alternative-footing row passes Cassini there. All six canonical
p=6 survivors were refined in `continuation_refine_001`; all accuracy checks
pass and the limiting ratios are

| t | epsilon | abs(Q2)/ceiling |
|---|---:|---:|
| 1.52 | .20 | .981710363398 |
| 1.52 | .22 | .892618344269 |
| 1.52 | .25 | .817554289308 |
| 1.52 | .28 | .978136098845 |
| 1.55 | .22 | .980776790055 |
| 1.55 | .25 | .904100507663 |

A separate 21-point t grid on [1.5,1.7] at p=6 finds one ceiling crossing
at each epsilon .20,.22,.25,.28,.30, and no sampled pass at .18. Refining
those observed brackets gives approximate upper t crossings 1.52591,
1.55623,1.58055,1.52773,1.51482 respectively. These are exploratory
4,000-by-160 quadrature boundaries, not physically precise parameter
determinations, global maxima or proofs against unsampled islands.
They identify what the MW calculation should test next; increasing t beyond
its allowed Solar value to fit the galaxy would fail the same joint law.

The final bounded shape discriminator uses p=6,6.1,...,6.6; 11 t values on
[1.5,1.75]; and epsilon=.24,.25,...,.30. It requires a sampled minimum
total slope above .01 and a Solar ratio at most .99, then refines observed
upper-t crossings. The largest retained t is approximately 1.587165 at
p=6.3, epsilon=.24 (sampled slope .01913); at epsilon=.25 it is 1.581582
(slope .01656). Values p>=6.4 produce no feasible edge in this tested
grid/root procedure. This is a finite search result, not a theorem over
all attenuation shapes or all parameter values. The final suggested MW
points are rounded inward. `final_refine_001` evaluates the exact four
points selected for the final MW discriminator on both fixed footings:

| t | p | epsilon | Canonical Solar ratio | Alternative Solar ratio |
|---|---:|---:|---:|---:|
| 1.587 | 6.3 | .24 | .989471762314 | 3.307260650785 |
| 1.5815 | 6.3 | .25 | .989734569943 | 3.140206891498 |
| 1.564 | 6.2 | .26 | .989963452826 | 2.926623851981 |
| 1.543 | 6.1 | .27 | .989730547956 | 2.744794202963 |

All four pass the unchanged canonical Cassini ceiling and fail the
alternative one. Every accuracy check passes using 400/800 angular nodes,
20,000/40,000 radial nodes and an expanded domain. The largest ceiling-ratio
spread is below 5.4e-10; the largest flux/density q discrepancy across all
levels is below 8.65e-7, under the unchanged 2e-6 criterion. This Solar
result does not assert that any of the final four pass the MW.

## Exact global constitutive certificates

The finite admissibility qualification above applies to the initial general
screen. Two subsets now have stronger exact results. For p=6 and every
t>=3/2, `MONOTONICITY_PROOF.md` reduces global positivity of d(y nu)/dy
to one compact interval. `monotonicity_exact.py` verifies 4,959 exact rational
enclosures there with a uniform lower bound 23487/1000000. Analytic head
and tail estimates and monotonicity in t extend positivity to every y>0.

For exact p=63/10 and every t>=3163/2000=1.5815, the analogous
`FRACTIONAL_MONOTONICITY_PROOF.md` and `monotonicity_fractional.py` verify
4,961 exact rational compact intervals with lower bound 12671/1000000,
again completed by analytic tails. Rational root enclosures are checked by
exact integer powers; exponential bounds use elementary inequalities and
exact fraction powers. The certificates use no floating transcendental
arithmetic. Both runs completed and their manifests validate.

Independent reviewer `cassini_sign_route` found the fractional proof and code
sound, but identified a stale p=6 convention string in the fractional run's
contract; its assertion, bounds, proof and executable correctly use p=63/10.
The pinned historical contract is preserved. `PROVENANCE_CLARIFICATION.md`
states the exact correction and distinguishes the original run from the
reviewer's fresh replay under a corrected contract in the sibling area.
That replay completed and validated at
`../universal_length/fractional_review_001/manifest.json`, reproducing the
exact output. `../universal_length/FRACTIONAL_REVIEW.md` records the
independent verdict proved as written for the exact rational parameters.

These are mathematical statements about the stated constitutive family,
separate from finite accuracy of the response implementation. They establish
nu>1, nu'<0 and monotonic total spherical response; they do not establish
global well-posedness, dynamical or relativistic health. The independent review
and corrected-contract replay have their own provenance, separate from the
original computation.

## Verification and provenance

`test_response.py` verifies the exact simple control, explicit derivatives,
energy-primitive derivatives, low/high limits, scalar/array behavior, the
original Cassini result, and zero external field. The first recorded red test
failed because the new implementation was absent. A subsequent primitive
finite-difference check initially used an inappropriate *relative* criterion
where the cutoff makes its derivative around exp(-123); it was replaced by
the declared mixed absolute/relative criterion before the recorded screen.
No physical acceptance threshold was changed by that correction.

The Cassini implementation separately evaluates the flux and density forms,
including the outer-kernel derivative and boundary term. It imports only
analytic Gaussian helpers and physical constants from KT33. Newtonian exact
zero and plain-QUMOND controls are included in the refinement runs. Signed
quadrupoles remain in every JSON rather than being discarded for grading.

Each scientific run has a bounded v2 manifest with input hashes before/after,
Git state, software, actual command, timing, one-thread limit and log cap.
The stale fractional-contract convention is explicitly disclosed above;
schema and hash validation alone do not detect that semantic inconsistency.
Finite quadrature and sampled constitutive admissibility also remain finite
evidence. New runs must use fresh output directories.

No cluster, dwarf, SPARC, lensing, cosmological, relativistic health or common
source-composition success is claimed. No retired particle/cold sector is
reopened. No old file or result was edited and no commit was made.
