# Independent audit: auxiliary stress and scalar surface current

**Primary verdict: correct only after the quantitative restrictions stated
below.** The auxiliary action and its integration-by-parts sign are correct.
The clock-slice argument excludes a matter Hilbert surface stress under
bounded frame gradients and strong endpoint control. Bounded invariants
r,A,P alone do not suffice. A separate finite-current-measure lemma excludes
scalar surface storage; it is not a consequence of bounded stress alone.

No existence, uniqueness, smooth-data breakdown, or required new physics
is asserted. This is an independent delegated audit of the proposed narrow
extension, using the native action and the earlier measure review.

## 1. Exact auxiliary action, including the active constraint

Let r=sqrt(2X)>0, E=exp(2alpha+2beta), and gamma>0. The full-switch matter
action equals the minimum over Q>=1 of

    Laux=E[U-QD],
    U=r^2/2-V-W+(Q-1-gamma r^2)^2/(2gamma).

The unconstrained minimizer is Q=1+gamma(D+r^2); imposing Q>=1 gives
Q=1+gamma max(D+r^2,0), exactly the native switch.

For differentiable constrained variations use

    Laux=E[U-QD-mu(Q-1)],
    mu>=0, Q>=1, mu(Q-1)=0.

The Q equation is (Q-1-gamma r^2)/gamma-D-mu=0. Hence mu=0 on branch,
and mu=-(D+r^2)>=0 off branch. The multiplier has the units of D; there
is no additional gamma factor in this convention.

Set A=Q/r and Pi=exp(2beta)P. With phi_t=s>0 and v=-phi_x/s,

    E QD=A(phi_t Pi_x-phi_x Pi_t).

Consequently the term -E QD integrates by parts to

    Ltop=Pi(-phi_x A_t+phi_t A_x),

with a plus sign in front of Pi phi_t A_x. The discarded total divergence
is partial_t(A phi_x Pi)-partial_x(A phi_t Pi). It must be treated as a
global divergence of smooth approximants, not silently removed from
piecewise fields while omitting their internal distributional boundary.

The remaining algebraic density is

    E[H(r,A,P,phi)-mu(Ar-1)],
    H=r^2/2-V-W+(Ar-1-gamma r^2)^2/(2gamma).

The topological density has no metric dependence when A and Pi are treated
as independent variables. This statement holds for arbitrary variations
of the two-dimensional base metric h_ab within plane symmetry, not only
its conformal factor: the wedge density has no h_ab dependence.

## 2. On-shell Hilbert stress and the missing frame bound

The redefinitions Q=Ar and P=exp(-2beta)Pi depend on the metric. Their
extra metric-variation terms are proportional to the Q and P equations.
Thus equivalence of Hilbert stresses is an **on-shell identity for smooth
approximants satisfying those equations**, with the KKT term retained.
It is not a license to discard field-redefinition terms in an arbitrary
off-shell or already singular configuration.

For the longitudinal base components, direct metric variation gives

    T_ab=h_ab H+(H_r-mu A)phi_a phi_b/r,
    H_r=r+(Ar-1-gamma r^2)(A-2gamma r)/gamma.

Equivalently the longitudinal kinetic coefficient is

    (H_r-mu A)/r
      =1+[(Q-1-2gamma X)/gamma]*(A/r-2gamma)-mu A/r.

Complementarity has been used in the first term. In the equal transverse
directions,

    T^y_y=T^z_z=H+P W_P.

The topological term contributes no Hilbert stress in these independent
variables. In particular the only potentially unbounded coefficient in
these formulas, after imposing the bounds below, is mu.

However, bounding r,A,P does not bound phi_a phi_b. A scalar gradient can
have fixed timelike norm while its frame components become arbitrarily
large by a boost. Therefore bounded invariant r alone is insufficient.
Require a uniform coordinate/frame gradient bound, for example

    0<s0<=phi_t<=s1, 0<r0<=r<=r1,

in a uniformly nondegenerate bounded conformal metric. Then |phi_x|<phi_t
also bounds phi_x and the longitudinal stress coefficients. This is the
precise restriction missing from an assertion based on invariants alone.

## 3. Clock-slice estimate for A

Variation of Pi in the transformed action gives exactly

    phi_t A_x-phi_x A_t=exp(2alpha) W_P,
    r e^a partial_a A=W_P.

There is no sign reversal. Along a fixed clock slice phi=constant,

    dt/dx=v,
    dA/dx|phi=exp(2alpha)W_P/phi_t.

Assume metric bounds, uniform cap separation, regular bounded hold-law
parameters and field values, and the clock bounds above. Then the right
side is uniformly bounded. Bounded A at one boundary of each clock-slice
crossing gives a uniform interior A bound. No bound on A_t is needed.

Here "incoming A" means boundary data anchored on the same spacelike
clock characteristic; it is not causal initial data for an evolution
equation. Its bound must be assumed or independently obtained from the
outer solution. A layer cannot be claimed to control this boundary value
by the estimate itself.

For a fixed shrinking strip the crossing x-length is O(width). For a
moving timelike strip require uniformly transverse clock crossings, e.g.
|interface speed|<=1-delta and the stated regularity, so the same estimate
holds. Coordinate transformation (t,x)->(phi,x) has Jacobian phi_t;
the upper and lower bounds ensure uniformly controlled measure conversion.
Bounded oscillations of phi derivatives do not destroy this Jacobian
control, even though their second derivatives may be large.

With bounded A,r, Q=Ar is bounded. The algebraic switch relation then
immediately bounds D_+=max(D,0). It does not directly bound D_-.

## 4. The negative branch and vanishing multiplier mass

The sharp divergence identity along a clock slice is

    dPi/dx|phi=(E r/phi_t) D, Pi=exp(2beta)P.

The coefficient c=E r/phi_t has uniform positive lower and upper bounds.
Since D_+ is bounded, the positive variation of Pi along one crossing is
O(width). Therefore

    integral (dPi/dx|phi)_- dx
      =integral (dPi/dx|phi)_+ dx-(Pi_right-Pi_left)
      <=C width+|Pi_right-Pi_left|,
    integral D_- dx<=c_min^(-1)[C width+|Pi_right-Pi_left|].

Require strong endpoint matching along the same clock slices, uniformly
on compact interface portions, so the Pi difference tends to zero.
Strong endpoint P matching and locally uniform continuous metric limits
give that property. Uniform convergence of endpoint values to a common continuous
interface trace is sufficient: crossing times differ by O(width), and
the continuous trace is uniformly continuous on compact portions. Merely
having a continuous weak limit of P is not sufficient. An appropriately
strong L1 trace version could replace uniform control, but needs its own
quantified estimate.

Uniform bounds for the clock-coordinate Jacobian convert this estimate
to vanishing spacetime L1 mass of D_- in the layer.
Since 0<=mu=max(-D-r^2,0)<=D_-, the multiplier has vanishing L1 mass.

All bounded terms in the Hilbert stress integrate to zero on a shrinking
strip; the remaining mu terms do as well. Therefore there is **no matter
Hilbert surface-stress measure** in this class. The result allows fast
temporal variation but relies on the stated smooth on-shell approximation,
frame bounds, regular metric coefficients, cap separation, anchored A bound,
regular crossings, and strong P endpoint matching.

This Pi estimate does not require bounds on P_t or on metric derivatives
inside the matter estimate. Uniform metric-derivative control is a separate
sufficient restriction when excluding gravitational concentration/effective
stress; the absence of a matter surface stress must not be promoted to
absence of gravitational defects without that separate argument.

This does not assert pointwise bounded stress on the off branch: mu may
be large locally. The conclusion there is vanishing integrated stress,
not a uniform supremum estimate.

## 5. Stress bounds alone do not control scalar current

The topological scalar current in the auxiliary representation is

    Jtop^t=Pi A_x, Jtop^x=-Pi A_t.

Clock-slice estimates do not separately bound A_t or the analogous fast
temporal derivatives of Pi. Thus the Hilbert-stress proof alone cannot
discard a scalar current defect. Small-amplitude rapid loops are not
excluded merely by uniform field convergence; no such loop is asserted
here to solve the full native equations.

The scalar currents of the original and integrated auxiliary forms also
differ by an identically divergence-free improvement:

    Joriginal-Jaux=(-partial_x(A Pi), partial_t(A Pi))

on using the auxiliary field equations for the redefinition. One should
not identify their surface components without checking the relevant limit.
The next argument deliberately uses the exact original scalar current.

## 6. Additional scalar finite-measure lemma

Assume the original scalar currents have locally uniformly bounded total
variation as spacetime measures and converge weak-*. Assume phi converges
locally uniformly, has a common C1 timelike interface trace, and its
tangential derivative along the interface is strictly positive. Assume
the explicit scalar source converges as a bounded function (or as a
finite measure with separately specified surface part). These are
additional compactness/source hypotheses, not automatic consequences
of the preceding Hilbert-stress estimate.

Direct contraction of the original normal and temporal current formulas
gives the exact identity

    J_phi^a phi_a = E B(1-2gamma D)              on branch,
    J_phi^a phi_a = E B(1+2gamma B)             off branch,
    B=r^2.

On branch D=(Q-1)/gamma-B, so with bounded B and metric the absolute
contraction is bounded by C(1+Q). The polarization-measure lemma controls
the possible surface mass of Q, since Q is dominated by the nonnegative
normal polarization-current measure in a regular conformal metric.
Alternatively, under sections 3–4, Q is uniformly bounded directly.
Thus the contraction has no surface measure in either route.

Use the exact smooth-family product identity

    div(phi J_phi)=J_phi^a phi_a+phi div J_phi.

Uniform phi convergence and current total-variation bounds justify passage
of phi J_phi to phi times the current measure. They avoid any unjustified
multiplication of weakly convergent phi gradients with current measures.
The same reasoning applies to the source product.

In a fixed-interface chart write the surface current as
j^t(t)delta(x),j^x(t)delta(x). Absence of a dipole source first gives
j^x=0. Scalar balance gives

    [J_phi^x]+partial_t j^t=r_surface.

The product identity's delta coefficient is

    phi_Sigma[J_phi^x]+partial_t(phi_Sigma j^t)
       =phi_Sigma r_surface,

because its contraction has no surface mass. Subtracting phi_Sigma times
the scalar balance gives

    (d phi_Sigma/dt) j^t=0.

The positive trace derivative forces j^t=0, even for signed finite
surface measures. For a moving timelike interface, use
j^x-xidot j^t=0 and the tangential derivative
d phi_Sigma/dt=phi_t+xidot phi_x=phi_t(1-xidot v)>0; the same subtraction
works. A C1 trace is used to multiply/differentiate arbitrary singular
surface measures. A merely almost-everywhere differentiable trace would
need further analysis at singular support points.

Thus scalar surface storage is excluded in this **additional finite-current-
measure class**. With no source surface part, the usual scalar normal-flux
jump vanishes. A nonzero finite source part can cause a jump but cannot
supply storage under the same product argument. Nonmeasure currents,
unbounded total variation, dipoles, null/degenerate trace limits, or loss
of uniform phi convergence remain outside this conclusion.

## 7. Implications and remaining obligations

The combined estimates remove polarization storage, scalar storage, and
matter Hilbert surface stress in their explicitly intersected class. They
supply necessary ingredients for applying ordinary regular-corner
matching, together with the full metric equations and regular outer
traces. They do not show that every sequence reaching steepening remains
in this class, nor construct any alternative outside it.

In particular one must retain the precise normal-stress matching condition
used by PF02, verify it from the full coupled equations for the intended
limit, and not equate an arbitrary reduced canonical stress with Hilbert
stress without accounting for improvements. The regular time-dependent
corner proof already establishes its obstruction when those matching
conditions hold. These new estimates are not a smooth-data breakdown
theorem or a proof that an extension to the action is necessary.

## Audit status

| Obligation | Status |
| --- | --- |
| Auxiliary minimization and KKT sign/normalization | passed |
| Topological integration-by-parts sign | passed |
| On-shell stress equivalence under metric-dependent redefinition | passed for smooth approximants satisfying P/Q equations |
| Bounded invariants alone imply bounded stress | failed; frame-gradient bound required |
| Clock-slice A bound | passed with bounded anchored data, source and crossings |
| Negative-branch multiplier has vanishing mass | passed with strong endpoint matching and metric/clock bounds |
| Hilbert stress alone excludes scalar storage | not established and not used |
| Scalar product-identity exclusion | passed with additional uniform current-measure and trace hypotheses |
| All weak limits, unique continuation, or necessary new physics | out of scope |

Independent proof audit, 2026-11-06. No simulations or sampling were used
as proof. All estimates are conditional analytic statements about the
specified approximation family.

Inspected source SHA-256 revisions:

    time_layer_review/REVIEW.md b571291f1874e227fd3aef34c386d99ea40fe63c678e0bbc0a61a1bed00c9f7b
    time_layer_review/POLARIZATION_MEASURE.md f4bf69c4be2f44775079ff1f0edb5b63c6f5ecb788660c61a255a45e2deabc09
    AC7_charge_switch/README.md 6627a35733c1700445d35e1dc1dc1125f6d1bc35e18d159ffe88b633f4d037e6
