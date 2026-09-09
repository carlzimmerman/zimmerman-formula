# IC45: independent angular transmission and an inactive-clock acceleration

Base: daf4bcd52360e68ae44faba6934a896a39ef7a39.
Previous goal turn: verified progress (IC44).
Full relativistic gravity target: **OPEN**.

## 1. Close the omitted angular-equation audit first

IC44 explicitly did not certify the independent angular equation. IC33 varied
independent radial and angular metrics, but its exported flow then pinned w.
That flow must not be used unmodified on the inactive side.

ic45_unpinned_angular.py reconstructs the pre-isotropy spherical action using
the same IC30 coefficients and the IC33 metric parametrization. It varies
a_r and b_t before setting both to Q, retaining w(r), w_r and w_rr. The spatial
Ricci expression is checked against the independently computed Christoffel
curvature in IC30. The isotropic action agrees with IC30 up to the explicitly
computed curvature boundary derivative. The trace equation agrees exactly
with IC30's Q Euler equation, including the time derivative of its momentum.

The independent traceless metric combination yields shear evolution, now
without imposing w=wc. For IC44's common-field, C1-metric interface, its
jump is exactly

    V [shear_r] + K([S_rr]+2[w_rr]+[Q_rr])/4 = 0,
    V=Rdot+beta, K=2m exp(S+2w-2Q).

Substituting IC44's independently computed six-equation solution gives zero.
No angular equation was assigned from the trace or set to zero in advance.
This closes that PARTICULAR omission; it is not full gravitational closure.
The new script also exports the unpinned Q, q and shear flow expressions for
a subsequent two-phase evolution solver.

## 2. Derive the inactive response from the same constraints

On the initial IC41 collar w=wc and w_t=0, but do not require w_tt=0 on the
inactive side. Preserve the original action coefficients, fluids, initial
profile and exponential kernel. Write the gravitational constraints as

    C=-E_S/J, W=E_w/J, J=r^2 exp(3Q).

The active side obeys C=0 and lambda=-W, where lambda=eta exp(S)ell in the
regular activated bulk. The inactive side obeys C=W=0.

Let A=S_tt and B=w_tt. Differentiating twice at the initial slice gives

    active:   C_S A_plus + F_C = 0,
    inactive: C_S A_minus + C_w B + F_C = 0,
              W_S A_minus + W_w B + F_W = 0.

Here each subscripted object is a spatial differential operator, not just an
ordinary derivative. The source functions F_C,F_W are evaluated by IC40/41's
canonical time engine before supplying A or B. Inactive operator coefficients
are obtained by differentiating the actual unpinned action. On this slice the
principal two-by-two coefficient matrix is

    K [[1-u^2,   2-u^2],
       [-(2-u^2), -(4-u^2)]],  u=(S+2w)/(S+w),

with determinant K^2 u^2. Thus the coupled local second-order spatial system
can be solved on the same regular chart, rather than artificially pinning B.
Exceptional u=0 is excluded, not resolved by this calculation.

The ordinary matter terms are transformed from the physical metric, not
introduced as new clock-dependent forces. For a barotropic fluid with index
w_f and barred-frame coefficient c at wc, set n=1-3w_f. Through quadratic
spatial gradient order, the density per barred J is

    h0 = exp(S+n(w-wc)) c j^(1+w_f),
    hg = exp(S-2Q-n(w-wc)) j g^2/[2(1+w_f)c j^w_f].

This follows by substituting physical current exp(-3w)j and physical gradient
norm exp(-2Q-2w)g^2 into the minimally coupled Hamiltonian and its physical
volume/lapse factors. The executable checks that change of variables and
both variations. Thus matter adds h0+hg to C and -n(h0-hg) to W. Initially
g=0, so it adds n h0 to C_w's zeroth-order coefficient and -n^2 h0 to W_w's.
O(g^4) terms do not affect this second-time calculation at initial g=0.
This is not an exact all-gradient fluid Hamiltonian or a new full Ward proof.

## 3. A negative control prevents false closure

First set A_plus(0)=A_plus,r(0)=0 at the interface. Impose equal A_minus
boundary values and B(0)=B_r(0)=0, as required by the chosen initial common
traces. Solving the coupled inactive system gives a nonzero clock acceleration
and excellent bulk constraint residuals:

    maximum normalized second-constraint coefficient residual: 1.86e-41,
    lambda_tt at the active edge: -90.1336284725464,
    necessary interface residual: 2779.67250481583.

This is NOT a passing join. At these initial data, w_t=0 and the first-time
canonical fields coincide as functions on both sides, so q_tt also coincides.
The time-squared coefficient of IC44's [q_r]=-lambda/(2V) therefore requires
lambda_tt=0 at this initial boundary. The control violates it despite
preserving both bulk constraints. The failed control is retained.

## 4. Solve the boundary equations and retain the inactive motion

Next determine A_plus(0), A_plus,r(0) from the existing action-derived lapse
operator so that the first two edge coefficients of W_tt vanish. The second
cancellation is an additional boundary choice here, not a proof that every
boundary-preservation condition follows. The computed values are

    A_plus(0)   = 0.221251471912060884805218296633167,
    A_plus,r(0) = 6.18373926036182023755282376889783.

Then solve the inactive coupled system with those common lapse data and
B(0)=B_r(0)=0. The inactive clock does not remain pinned:

    d_r^6 w_tt(0) = 60538315324.7957974856235378490576

in the repository's normalized model units. This large high spatial derivative
is not itself a stability result or an observable acceleration prediction.

At 60 decimal digits, acceleration degree eight:

    maximum normalized second-constraint coefficient residual: 2.20e-61,
    unpinned/pinned initial operator comparison error: 7.65e-61,
    necessary second-interface residual: 0 at working precision.

The degree-six, 40-digit run gives the same common coefficients with a maximum
relative/floor-one discrepancy of 2.78e-32. These are floating high-precision
checks, not interval enclosures or exact zeros.

The first robust nonzero inactive response is the sixth spatial derivative.
Do not claim exact sixth-order onset from the rounded IC41 root: smaller
nonzero lower coefficients remain recorded. If the lower W_tt jets vanished
exactly, the leading operator balance would give

    B^(6)(0) = -(1-u0^2) W_tt^(4)(0)/(K0 u0^2).

The computed response is the new content: earlier calculations used a pinned
w on the whole initial collar. It is not obtained by altering mu or fitting
new action coefficients.

## 5. What is and is not established

Established in the stated radial regular chart:

- Independent angular variation does not reject IC44's local transmission.
- Both inactive constraints admit the computed second-time response.
- Arbitrary bulk-compatible boundary acceleration can fail the moving join.
- The tested boundary solve removes that particular failure while allowing
  nonzero inactive-clock acceleration.

NOT established: a finite-time two-phase solution, all higher boundary
preservation conditions, regularity at u=0 or V=0, the full three-dimensional
Dirac algebra, k=0 treatment, PPN, stability/causality, cosmology or empirical
success of this completion. No claimed Kepler-grade prediction is produced.

Next unavoidable step: use the exported unpinned gravitational flow and the
physical-frame matter action to advance BOTH phases with the moving boundary,
solve the coupled lapse/clock constraints at each step, and independently
check boundary residuals without projecting them away. Lambda must be
computed from the active W equation; its exceptional-limit scaling must not
be supplied by hand. The present second-time tangent is an initial ingredient
for that calculation, not a substitute for it.

## Verification, provenance and attribution

All four new Python files ran. The IC40-45 suite has 34 passing tests
(exit 0, 78.482 s); the existing IC33 angular suite has four passing tests
(exit 0, 51.860 s). The four scientific --strict runs deliberately exit 2
(full theory OPEN); their bounded runners return 1. No Python exception is
being reinterpreted as a scientific pass. Six manifests validate their
input/output hashes. run_index.json records exact commands and file inventory.
New-module tests first failed when implementation was absent; additional
branch controls were then run against the implemented alternatives.

Mathbox computation/proof audit kept the independent angular identity,
finite Taylor evidence and missing global evolution distinct. This is a
self-audit, not a fresh-agent or Lean certificate. Self-proofreading covered
this note; no proofreading-driven mathematical-token changes. Lean/lake were
previously checked and unavailable; no install or formal certificate is claimed.

Credit Carl Zimmerman for the framework and primordial-clock direction; L44's
activation suggestion remains credited in IC39. No technical novelty/priority
claim is made. IC42's bounded-multiplier failure, IC44's negative controls and
concurrent Fable work are untouched.
