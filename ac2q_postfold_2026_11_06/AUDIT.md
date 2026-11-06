# PF01/PF02 self-audit

Primary claim audited: DERIVATION.md section 4, nonexistence of a nontrivial
same-direction, finite, positive-charge stationary planar corner satisfying
all three variational corner conditions when 0<=gamma*s^2<1/3, continuous
P and phi, bounded sources, and no concentrated stress defect.

**Primary verdict: proved as written under those explicit restrictions
(internal derivation; self-review, not independently certified).**

The broader claim "the full covariant AC2q theory necessarily fails after a
fold" is **incomplete**. The missing implication is either a full-action
breakdown theorem in its admissible domain plus exclusion of every native
continuation, or a directly controlled full-action counterexample. Neither
finite principal-system evolution nor the restricted corner theorem supplies it.

## Dependency and obligation audit

| obligation | disposition | evidence / restriction |
|---|---|---|
| Actual on-branch action, including X and gamma X D.P | passed | AC7 README pinned by exact-run manifest |
| Spatial covector constraint | passed | P^mu=P e^mu, n.e=0, e.e=1 |
| D.P and P.A contractions | passed | direct metric/tetrad symbolic checks |
| Integration by parts at discontinuity | conditional on stated class | continuous P; distributional product P dC defined; no added surface functional |
| Scalar time slope | passed | s>0, same tangential derivative of continuous phi; gamma*s^2 bound in interface frame |
| P conjugate jump | passed | bounded W_P gives no delta; on-branch fixes A>0 |
| Scalar current jump | passed | variation at fixed s makes current proportional to L_v; bounded sources |
| Momentum flux | conditional on stated class | no singular metric/layer/oscillatory stress; stationarity |
| Partial Legendre transform | passed | k=-A, f=L+A d; checked current envelope and stress reduction separately |
| Strict convexity | passed analytically | f''' expression, 0<(3-2v^2)(1-v^2)<3, epsilon<1/3 |
| Contradiction | passed analytically | equal f' endpoints imply strict integral defect |
| v<0, equal states | passed | reflection; equal v fixes d; epsilon=0 only formal clock limit |
| Opposite flow signs, switch crossing, unbounded fields | out of scope | no exclusion claimed |
| W flux-cap domain | conditional only on finite admissible W | P value continuous within |KP|<a0; no candidate full trajectory constructed |
| Transfer to dynamical Einstein equations | not addressed | singular surface terms and metric evolution remain open |
| Formation from smooth full-action initial data | not addressed | principal-system breaking does not supply this |
| Uniqueness of weak solutions | not addressed | different weak formulations are not nonuniqueness of one formulation |

The decisive proof is the explicit third derivative and its integral, not the
finite fixtures or a source citation. Numerical root-pair fixtures include 13
pairs; two of the 15 proposed parameter sets have no two-branch minimum inside
the positive-charge interval. They are reported, not counted as successful pairs.

## Numerical audit

PF01 uses first-order Rusanov flux, periodic grids, adaptive explicit CFL 0.4;
no density clipping. A nonpositive density raises an error. The Euler branch
uses m=qv, the potential branch uses v; both flux Jacobians have speeds v±sqrt(q).
The analytic prebreak reference is inverted by monotone Newton iteration; maximum
recorded characteristic residual is at floating-point precision. A separate
Riemann calculation is based on explicit RH algebra, with an independent scalar
root solve for the momentum branch. Riemann boundaries cannot reach the shock
region in the benchmark's duration. No random samples are used.

Averages in the numerical initialization are midpoint values rather than exact
cell averages; this O(dx^2) error is dominated by the first-order method and is
not a high-order certification. Numerical convergence supports the finite claim;
it does not prove convergence or uniqueness for arbitrary data. The uniform
initial mean q is a local principal-model fixture, not a periodic solution of
the cosmological constraints. The Poisson primitive is a diagnostic, not evolved
gravity. Signed-charge dynamics and the switch are not in this experiment.

PF01 main: 37/37 checks. Wrong-pressure mutation fails precisely four RH tests.
PF02 main: 21/21 checks. Reversed-defect mutation fails precisely 13 pair tests.
All four manifests validate against current source hashes; failed mutation runs
are valid records of intentionally failing controls. No model success is inferred
from these check counts. The affine-expansion control is an analytic sign check,
not a separately evolved numerical solution.

## Adversarial corrections retained

1. AC10's J=1e-3 event is not proof of J=0; positive native pressure can create
   shocks first. Earlier blanket wording about a true fold is not inherited.
2. Shock solvers in different variables do not prove nonuniqueness of a fixed
   distributional system. The current report states the distinct weak laws.
3. Small canonical corrections were not simply dismissed near a singularity;
   the exact stationary reduction retains them. Time-dependent boundary layers
   remain outside that reduction.
4. The formal s=0 fixture is not an admissible physical clock. Positive-s proof
   and fixtures carry the claim.
5. A need for post-break completion is not a proof that a new fitted constant,
   a new particle, or any particular operator is necessary.

Proofread in self-review mode: DERIVATION.md and this report. Definitions and
sign conventions checked locally; no independent reviewer or external theorem
certificate. Raw derivation and source hashes are preserved for such a review.

## PF03 follow-up audit

The new time-dependent flat action follows from the same geometric identity as
PF02. Direct differentiation gives the currents; the 2x2 Fourier determinant
provides an orthogonal check on eliminating P. The original expected B sign
error is retained in native001 and corrected only in the v2 expectations. A
direct Taylor expansion verifies the correction (NATIVE_DYNAMICS.md). This does
not alter PF01 or PF02. Corrected run: 21/21; removing mixing C fails precisely
the on/off independent-root tests. Gravity and a globally sourced background
are outside this check; no global regularity conclusion follows from the symbol.
Proofread this new note in self-review mode; no independent certification.
