# The neutral coherent branch cannot stabilize merely by increasing density

The earlier explicit-mediator calculation found negative compressibility at
three densities. Here an analytic parameterization extends that conclusion to
the entire minimum-composition neutral coherent branch of the same model.
This is a restriction on a state and a mean-field functional, not on all possible
cold matter. It does not solve the finite-temperature problem.

## Functional and assumptions

Take a=b=A real, r negative, x=A^2, g=gs+gc0>0, h>0 and delta>0.
The spatially uniform energy density, excluding common rest energy, is

    E = delta r^2 + 2 h r x + g x^2,
    n = 2 x + 2 r^2.

The omitted terms include mediator self-repulsion, thermal and quantum corrections,
and gradients. The previous fixed-n composition calculation established a unique
interior minimum for this functional. Its stationarity equations are

    mu = g x + h r,
    (delta - 2 mu) r = -h x.

Define H=h^2, D=delta-2mu, t=D-delta, B=H-gD. For the attractive regime H>g delta,
parameterize delta<D<H/g, so t,B are positive. Stationarity gives

    mu = -t/2,
    x = D t/(2B),
    r^2 = H t^2/(4B^2),
    n(D) = D t/B + H t^2/(2B^2).

These formulas give positive occupations, neutral charge, and the required
negative mediator phase. They reconstruct the unique fixed-n composition minimum.

## Exact obstruction

Differentiating the rational expression gives

    dn/dD = [(2D-delta) B + g D t]/B^2
            + H t (B+g t)/B^3 > 0.

Every term is positive on the stated interval. Also n tends to zero at its lower
endpoint and to infinity at its upper endpoint. Continuity and strict monotonicity
therefore cover every finite n>0 exactly once. Since dmu/dD=-1/2,

    dmu/dn = -1/[2 (dn/dD)] < 0.

The energy derivative identity dE/dD=mu dn/dD independently checks the chemical
potential convention. The pressure simplifies to

    P = mu n - E = mu x < 0.

Thus this branch has neither positive compressibility nor a finite-density
zero-pressure saturation point. Searching higher densities within this same
functional cannot produce a stable homogeneous bulk reservoir. Negative pressure
alone is not a universal instability criterion; the negative derivative is the
separate compressibility obstruction. Surface or finite-mode effects are absent.

At the assigned benchmark H/(g delta)=1.25e8. The formal n-to-infinity limit is
mu=(delta-H/g)/2=-0.124999999 eV. That limit is a mathematical property of the
truncated nonrelativistic functional, not a controlled physical prediction at
arbitrary density. Unmodeled operators and nonrelativistic validity must be assessed
before such extrapolation. The sign result applies wherever this branch and
functional are a justified description.

## Verification and its scope

check.py verifies five exact rational identities with SymPy: atomic stationarity,
mediator occupation, dn/dD, pressure, and dE/dD=mu dn/dD. It also inverts n(D) and
compares chemical potential, pressure and n*dmu/dn to all three previous rows.
All nine comparisons pass; the largest relative discrepancy is below 1.3e-9.
The numerical predecessor used finite differences for the chemical derivative.
The bounded run and hashes are in run/manifest.json.

BranchSign.lean proves two conditional algebraic sign theorems: pressure is
negative and the displayed inverse slope is negative under the positivity
hypotheses. It does NOT formalize differentiation, endpoint limits, global
branch coverage, the physical field equations or empirical particle existence.
The derivative identities are checked by symbolic algebra separately. Its actual
compiler result, command, source hash and runtime are in lean_verification.json.
No extra axioms or admitted proofs are introduced in this file.

## Consequence for creation research

The few-pair preparation proposal is not invalidated by a bulk coherent-state
obstruction. However, increasing that population into the tested coherent medium
has no stable bulk endpoint in the assigned functional. The ideal thermal capacity
study also prevents assuming a dilute classical thermal pressure without checking
quantum statistics. It does not establish the state of the interacting system.

A genuine continuation must change the physical state or derive missing physics:
a conserving interacting finite-temperature or nonequilibrium response calculation,
or independently justified additional interactions. Adding a free repulsive term
just to obtain a desired result would define a new model, not validate this one.
None of these calculations yet identifies the optical carrier with the repo's
cosmological component, establishes a production apparatus, or supports propulsion.
The original cold-energy creation objective remains open.
