# Candidate: coupled balance forbids feeding an initially empty matched layer

## Class and definitions

Retain PF10's full-switch smooth approximants, continuous nondegenerate regular
planar metric, strictly timelike interface, r>=r_min, cap/source bounds, bounded
positive anchored A, uniform clock convergence and strong same-clock Pi matching.
Retain finite total stress measures and identified regular outer native fields.
DO NOT assume a finite measure bound on the full scalar current. Instead retain
the clock-slab theorem's regular convergent outer side fluxes and finite initial
slice charge. Require the usual gravitational thin-shell limit: regular one-sided
metric derivatives and the Israel junction relation and regular outer Einstein/Codazzi constraints
with a common regular induced metric. These imply intrinsic surface-energy
conservation. Uniformly bounded metric first derivatives remove quadratic
curvature surface mass; regular one-sided traces identify the remaining jump.
We do not infer convergence of arbitrary interior connection/stress products
from bounded metric derivatives alone.

Use proper interface time s, transverse area a(s)=exp(2beta_Sigma)>0, clock
speed v(s)=dphi_Sigma/ds>0 and tau=phi_Sigma. For the differential calculation first take a,v C1 and positive. The
nonactivation argument below only needs a positive C1, v positive continuous,
local upper/lower bounds, and the stated integrable outer fluxes. The regular
outer traces of A and Pi are common; their tangential derivatives are common.
Normal orientation N points from minus to plus. T is the future unit tangent.
J_N below denotes the physical scalar-current normal component (density divided
by the spacetime volume factor). There are no additional matter surface sectors.

## 1. Forced surface equation of state

The PF10 slice argument gives vanishing multiplier mass, uniform bounded A and
Pi, and no need for upper r or boost bounds. Transverse stress supplies bounded
r^4 mass. On a shrinking strip, Holder inequalities remove lower powers r^k,
k<4. The leading invariant quantities are therefore

    H ~ gamma r^4/2,
    2H-r H_r+mu ~ -gamma r^4,
    T_perp ~ gamma r^4/2.

Let m be the r^4 surface measure per proper interface volume. No-normal-dipole
stress conservation implies S(N,.)=0. Planar symmetry leaves surface energy
sigma and two equal pressures p. The longitudinal trace is -sigma, so

    sigma=gamma m,    p=gamma m/2=sigma/2.

This permits all cancellations in the boosted total stress. It does not assume
separate bounds on positive and negative boosted constituents.

## 2. Charge is fixed by the same stress amplitude

The clock-slab identity gives

    q(tau) d tau = 2 gamma a(s) m(s) ds.

Regular side fluxes and finite initial slice charge make q absolutely continuous;
regular v>0 then makes m, sigma ordinary locally integrable densities. Hence

    q=2a sigma/v.

The scalar balance with no concentrated explicit source is

    dq/ds = -a [J_N].

This is a moving-domain identity for each smooth approximant, followed by the
specified side-flux and initial-charge limit. No interior current compactness
or product limit phi J is used.

## 3. Native outer stress/current relation

At a regular outer point, the exact auxiliary current and Hilbert stress obey

    T(N,T) = -v J_N + v A (dPi/ds)/a.

For example in a local orthonormal rest chart J_N=(h-mu A)n.N+A Pi_s/a,
and T(N,T)=-(h-mu A)(n.N)v. These are on-shell native identities.
Since A,Pi and their tangential traces agree on both sides, the topological
term cancels in the jump:

    [J_N]=-[T(N,T)]/v.

Writing f=[T(N,T)] gives the scalar balance dq/ds=a f/v.
This conclusion does not assume f or the scalar flux jump vanishes.

## 4. Full coupled energy balance and the homogeneous amplitude equation

The tangential projection of the Einstein/Bianchi thin-shell balance gives

    (a sigma)' + p a' = a f,

where prime now means d/ds. The sign convention agrees with a static flat
interface: sigma'=[T^x_t]. The p a' term is transverse pressure work.
Combining this with q=2a sigma/v and q'=a f/v yields

    2(a sigma)' - 2a sigma v'/v = (a sigma)' + p a',
    sigma' = (2v'/v-a'/(2a)) sigma,
    (sigma sqrt(a)/v^2)'=0.

Thus any existing layer in this class has

    sigma(s)=C v(s)^2/sqrt(a(s)),    C>=0.

If its initial slice charge tends to zero, then sigma(s0)=0 and C=0.
Consequently q, m, sigma, p and f vanish throughout the connected regular
interval. A positive flux mismatch cannot grow such a layer from an empty
state: it contradicts the other coupled equations.

## 5. Continuous clock-speed extension at birth

Write y=a sigma. Scalar balance and integrable outer fluxes make q absolutely
continuous; surface energy makes y absolutely continuous (p=y/(2a)). We have
q=2y/v>=0. On any open component where q>0, the quotient v=2y/q is locally
absolutely continuous. The previous differentiation therefore holds almost
everywhere there, giving q/(v sqrt(a))=2C on that component. If q vanishes at
its left endpoint, continuity and the positive local bounds on a,v imply C=0,
contradicting q>0. Starting from q(s0)=0, no positive component can activate.
Thus a divergence in v' alone at birth does not reopen the escape if v remains
continuous, positive and locally bounded. No globally imposed v' bound is
needed for this argument.

## 6. Logical limits

The zero initial slice charge is stronger than simply declaring no spacetime
current measure. It follows at a bounded smooth incoming slice when the strip
shrinks and the incoming fields stay bounded there. Carrying that condition to
an interface born exactly at a singular endpoint still requires a controlled
limit at birth; an uncontrolled nonzero initial defect is outside this theorem.

A pre-existing sheet with C>0 is not excluded by this necessary balance. It is
not constructed by it either: the remaining junction and polarization equations
must still hold. Its arbitrary constant here is not a same-data nonuniqueness
example. The calculation eliminates positive feeding from zero; it does not
construct any outgoing solution or establish global weak-solution uniqueness.
Loss of matching, cap/clock control, regular geometry, initial-charge control,
or the specified smooth-approximation framework remains outside this claim.
