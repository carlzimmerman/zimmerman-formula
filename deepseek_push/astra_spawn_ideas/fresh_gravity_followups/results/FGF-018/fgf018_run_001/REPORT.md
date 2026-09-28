# FGF-018: quoted-error-box continuity signs survive

**Worker outcome: supports_scoped_claim.** All 189 original gas intervals
intersecting 100–1000 kpc retain a lower slope bound above one under the
registered knot-mass error boxes. All 252 original shell/branch evaluations
and all 2268 additional interval-midpoint evaluations have positive force
residual lower bounds. Therefore every one of the 84 cluster/force/normalization/
history combinations retains the conditional steady, source-free, spherical
flow contradiction. This is new robustness information about the full declared
knot boxes, not another check only of the central slopes.

This is an Astra computation by `/root/catalogue_audit`, not a DeepSeek run.
It does not authenticate a likelihood, error coverage, global gravity theory,
observational exclusion, or historical novelty. Separate orchestrator review
must pin the result before promotion.

## Reproducible finite result

The source pin check verifies 27 frozen premises: 21 raw FITS files, redshift
metadata, registered force implementation, original shell and interval tables,
the task proposal and the accepted FGF-012 result hash. The scoped FGF-012
reconciliation accepts relevant unit/interpolation conventions conditionally;
it explicitly leaves covariance and pipeline semantics unresolved. Actual
input hashes and both numerical runs are recorded in version-2 manifests.
No live queue or mutable source-snapshot index is used as an input.

| Cluster | Gas intervals | Lowest box s_min | Lowest tested Delta_min, m/s² | Gas-error multiplier where first strict slope certificate reaches equality |
|---|---:|---:|---:|---:|
| A1795 | 28 | 1.084794410 | 1.620669232e-11 | 1.841555176 |
| A2029 | 27 | 1.126957093 | 3.990486902e-11 | 2.105921961 |
| A2142 | 27 | 1.288677354 | 3.902950429e-11 | 6.365189684 |
| A2319 | 26 | 1.473161569 | 3.762904793e-11 | 10.356751682 |
| A644 | 26 | 1.111455675 | 2.965362548e-11 | 1.685730786 |
| A85 | 27 | 1.230476954 | 2.347721301e-11 | 3.529153842 |
| ZW1215 | 28 | 1.106503915 | 3.502041616e-11 | 1.591752955 |

All original 100, 300 and 1000 kpc shells survive, for Q/R/registered M,
a0=9.3619e-11 and 1.1279e-10 m/s², and the distinct constant-vacuum and H(z)
histories. The smallest tested Delta bounds in the table occur at 1000 kpc
in the alternative-normalization H-scaled M branch. The positive margins
are far larger than the sign guards (1e-10 in s-1 and 1e-20 m/s² in Delta).

The interval table records original gas-knot indices and radii even when the
reported domain clips an interval at 100 or 1000 kpc. The shell table records
all 2520 individual outcomes and both rectangular and available-monotonicity
bounds. There are no failed real-box local certificates and no real-box
counterwitnesses in this domain. The absence of such witnesses here follows
from the positive bounds, not a failed search. No extrapolation or derivative
at a gas knot is used. A single robust interior shell already suffices for
the contradiction; positivity between every pair of sampled force shells is
not claimed or needed.

## What is being bounded

The core relation remains a=kappa c sqrt(G rho_Lambda), with kappa adopted.
The vacuum and H-dependent histories are separately evaluated, not equated.
Gas errors MGAS_LO/HI are treated as magnitudes; stellar MSTAR_LO/HI as mass
endpoints; EM_FORW as a symmetric magnitude. The extrema are determined by
constructing the knot intervals first, then interpolating endpoint masses
log-linearly on each source's own grid. This bounds every positive mass profile
in that knot box under the declared interpolation.

For gas interval endpoint boxes, s_min=ln(L2/U1)/ln(r2/r1). For each interior
shell, Delta_min=G Mh_low/r²-F(G[Mgas_high+Mstar_high]/r²;a), with consistent
solar-mass/kpc-to-SI conversion. These are analytic extremum formulas evaluated
in binary64; no directed-rounding interval arithmetic is claimed. Q and R are
independently evaluated here; M calls the source-pinned registered function.
No independent kernel validation of M is implied.

The central results reproduce the old slopes to 4.885e-14 and force ratios to
1.444e-15. Explicit corner enumeration agrees exactly with interpolation
extrema. As a comparison only, separately interpolating central masses and
error curves changes Delta bounds by at most 2.233077047e-14 m/s². That family
is not silently substituted for the arbitrary-knot-mass family in this proof.

In steady spherical source-free flow, conventional inertia and gas density
rho=s M/(4 pi r³) imply u du/dr=(1-s)u²/r. Euler balance with outward-decreasing
additional scalar pressure gives u du/dr=Delta+gnt, gnt>=0. The tested box
forces the first expression nonpositive and the second strictly positive.
This rules out that conditional flow family, including u=0. Nonsteady,
nonspherical, sourced, differently interpolated or differently calibrated
gas profiles remain outside the statement. No gas equilibrium solution or
boundary condition is constructed.

## Monotonicity is checked without using an empty family

All original gas central profiles are positive and strictly increasing; every
gas knot lower bound is positive, and each entire gas box admits globally
monotone profiles. Imposing gas monotonicity leaves all 189 strict slope
certificates intact. Stars have some nonmonotone central samples, but their
quoted boxes admit monotone profiles. All 21 gas/star/hydro boxes admit
monotone profiles on the native knots required to interpolate 100–1000 kpc.

There is one important limitation outside that restricted domain: **A644's
full raw hydrostatic-equivalent mass box admits no globally nondecreasing
profile**. At zero-based hydro knot 76, r=1029.140747 kpc, its lower mass is
4.78695750893568e14 solar masses. At knot 99, r=3000 kpc, its upper mass is
1.63240935948288e14 solar masses. Their difference, 3.1545481494528e14 solar
masses, precludes global monotonicity. These two radii are outside 100–1000
kpc; the first nevertheless supplies the upper bracketing knot for 1000 kpc.
The restricted support through that first knot is feasible.

The main rectangular certificates use M_FORW as the hydrostatic-equivalent
pressure-force input, without imposing globally monotone hydro mass. They
remain nonvacuous. The main table's `monotone_delta_min_m_s2` applies only
available nonempty full-support monotone envelopes; for A644 hydro it retains
the original bound, as the code and derivation state. It must not be read as
a claim that the empty all-profile, full-support monotone family is physically
admissible. The supplementary support audit exposes this distinction directly.

## Adversarial and exact controls

Exact rational controls test strict slope bounds above, at and below one.
A further four-knot synthetic profile has radii (1,2,4,8), lower masses
(1,2,3,6), upper masses (2,4,8,10), and witness masses (1,3,4,8). It lies
inside every box and is positive and strictly increasing, but its middle
slope is ln(4/3)/ln 2, between zero and one. Thus the implementation's failed
local-certificate interpretation has a constructive control. This is synthetic,
not a perturbation of an actual cluster or a steady-flow solution.

For each real interval the supplementary exact-algebra diagnostic scales both
gas error magnitudes by lambda. Setting its rectangular lower slope to one
gives lambda_crit=(M2-q M1)/(err_low2+q err_high1), q=r2/r1. The table lists
the first crossing per cluster; all 189 crossings have positive endpoint
masses and forward-check to 2.221e-16. The smallest factor is 1.591752955 for
ZW1215. These factors are not sigma values, likelihood errors or calibrated
new parameter boxes. At equality s=1, Delta>0 still contradicts Euler; this
is the boundary of the deliberately strict s>1 certificate, not a physical
escape threshold. Values beyond it may remove a local slope certificate but
do not repair the other shells or equations.

## Execution, artifacts and remaining gap

Setup began 2026-09-27T19:30:52Z. The main numerical process started
2026-09-27T19:35:44.442835Z and completed in 0.762726 s. The supplementary
manifest records its separate actual start and duration. Both runs enforce
120 s wall, 110 s per-process CPU and 1 MiB logs; one numerical-library thread
is cooperative. No memory or affinity limit is claimed. There is no random
sampling, download, installation, service, commit, or scientific failed run.

`numeric_001/` contains all interval/shell certificates, branch summary,
profile-box audit and checks. `numeric_002/` contains monotonic-support evidence,
all error-inflation crossing diagnostics and exact synthetic witness. Both
manifests validate against current input/output bytes. Exact launch argv,
actual bounds, result contract, validation outputs and artifact hashes are
preserved. This task wrote only its assigned result directory.

Mathematical proofreading self-review covered the authored derivations and
this report: no mathematical-token corrections were required. In particular,
the strict certificate boundary s=1 is distinguished from the Euler sign
obstruction, and failed inequalities are not labeled physical repairs.

The remaining empirical implication is whether these quoted knot intervals,
interpolation derivatives and M_FORW interpretation describe admissible joint
local density/pressure reconstructions with authenticated coverage and shared
errors. A discriminating next task would audit the underlying profile and
error-generation semantics/covariance, including A644's nonmonotone outer
hydro reduction. Repeating central slopes or enlarging a grid would not settle
that gap. Correlated subsets contained in the declared boxes inherit the
certificate, but unsupported claims about probability or systematic errors
outside those boxes do not.
