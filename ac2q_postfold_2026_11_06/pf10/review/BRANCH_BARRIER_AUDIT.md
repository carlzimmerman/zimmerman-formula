# Independent audit: variable-A hyperbolic branch barrier

**Verdict: refuted as stated; the proposed R has an incorrect constant.
A restricted barrier is valid for A_star>sqrt(6 gamma), not merely
A_star>2 sqrt(gamma).** In the homogeneous D=0 low branch, the sufficient
range is gamma r0^2<2-sqrt(3), rather than the entire interval (0,1).

Target audited: the parent's candidate message using
R=6 gamma r^2-6Ar+2+A^2/gamma. No native field counterexample or weak
continuation is claimed below. The counterexample is to the asserted
universal constitutive hyperbolicity barrier.

## Exact derivatives and counterexample

For the declared action,

    H=r^2/2-V-W+(Ar-1-gamma r^2)^2/(2 gamma),
    h=r+(Ar-1-gamma r^2)(A-2 gamma r)/gamma,
    R=H_rr=3+A^2/gamma-6Ar+6 gamma r^2
          =6 gamma (r-A/(2 gamma))^2+3-A^2/(2 gamma).

The additive 3 includes the canonical kinetic contribution 1 and the
additional 2 from differentiating the -1 in the square. At the proposed
crossing r=A/(2 gamma), h=r but R=3-A^2/(2 gamma). Consequently the
claimed strictly elliptic point requires A^2>6 gamma.

An exact counterexample to the proposed larger range is

    gamma=1, r0=1/sqrt(2), A0=3/sqrt(2), D0=0.

Then u=gamma r0^2=1/2<1, A0>2 sqrt(gamma), and

    R=6(r-3/(2sqrt(2)))^2+3/4>0

for every r. Moreover h(r0)=r0>0 and h_r=R>0, so h stays positive for
every r>=r0. Q=A0 r>1 along this increasing-r path. Thus c^2=h/(rR)
stays positive along a continuous on-branch constitutive path to arbitrary
r: the proposed barrier is absent. This path is not an exactly fixed-A
native nonconstant solution; the polarization equations still have to be
solved. It refutes the stated barrier inference, not the equations.

## Correct restricted variable-A statement

If the common outer value satisfies A_star>sqrt(6 gamma), then bounded
W_P, r>=r_min and eA=W_P/r give A=A_star+O(epsilon) throughout each
shrinking clock crossing. For sufficiently thin layers,

    A_min>sqrt(6 gamma),    A<=A_max.

Assume the incoming endpoint satisfies r<A/(2 gamma). Along any smooth
crossing the function F=r-A/(2 gamma) is continuous. To reach
r>A_max/(2 gamma), it must vanish somewhere. At that point,

    Q=A^2/(2 gamma)>3,
    h=r>0,    R=3-A^2/(2 gamma)<0.

The state is strictly on branch and the physical scalar principal
speed squared is negative. Off-branch Q=1 cannot bypass this crossing:
at an off state r=1/A<A/(2 gamma), since A^2>6 gamma>2 gamma.
Therefore an everywhere-hyperbolic smooth layer in this restricted class
has r<A_max/(2 gamma). This is a topological path argument with variable
A; it does not impose A constant as a field equation.

For D0=0, A0=1/r0+gamma r0 and

    A0^2/gamma=u+2+1/u,    u=gamma r0^2.

On 0<u<1, A0^2>6 gamma is equivalent to u<2-sqrt(3).
The endpoint is below A0/(2 gamma) because u<1. The strict margin is
important: equality gives R=0 at fixed A, but arbitrarily small variation
of A can remove the zero. The present uniform variable-A argument uses
the strict inequality.

## Why the speed is a coupled principal obstruction

The argument needs the high-frequency principal symbol of the native
system, not an exactly frozen-A nonlinear wave. At any fixed smooth
strict-on state, the scalar/clock principal equations in a locally
orthonormal frame are

    R n(delta r)+h e(delta theta)+lower-order terms=0,
    n(delta theta)+e(delta r)/r+lower-order terms=0.

The exact scalar equation additionally contains
r D_r n(delta A)+(W_P/r)n(delta P). The spatial constraints linearized
at that state have leading derivative parts

    e(delta A)=algebraic terms in delta r,delta P,delta theta,metric,
    e(delta P)=D_r delta r+(r/gamma)delta A+other algebraic terms.

For a nonzero spatial frequency k and temporal frequency of order k,
these give delta A,delta P of order 1/k relative to the leading matter
amplitudes, with finite coefficients at that fixed smooth point. Their
time derivatives therefore enter the scalar equation at order zero,
whereas n(delta r) and e(delta theta) enter at order k. At the barrier
D_r=0, the n(delta A) coupling also vanishes directly. This is a local
principal calculation; it asserts no uniform high-frequency approximation
across a singular sequence.

The Einstein equations have wave principal parts with algebraic matter
stress. At a non-null scalar characteristic their metric response has
two fewer high-frequency derivatives; connection terms do not change
this scalar principal polynomial. In particular an imaginary scalar
speed cannot coincide with the real gravitational null characteristic.
The scalar characteristic determinant is therefore

    R omega^2-(h/r) k^2=0,

giving c^2=h/(rR). At h>0,R<0 it has nonreal characteristic frequencies
and the clock-time Cauchy formulation is not hyperbolic. Coupling to the
finite-stiffness polarization and to gravity does not repair that local
principal sign. This is the precise sense in which crossing loses the
reviewed hyperbolic Cauchy predictivity; it is not a theorem forbidding
every mixed-type classical or weak field configuration.

## Consequence and boundary of the result

Within the corrected range, an everywhere-hyperbolic smooth matched layer
has a uniform upper r bound. The previously audited boost-only trace
lemma then excludes its finite timelike stress defect without requiring
finite scalar-current variation, provided that lemma's metric, stress,
trace, cap, label and no-dipole assumptions all remain in force.

This does not remove the finite-current assumption in the full PF10
theorem for arbitrary states, nor cover the low-branch interval
2-sqrt(3)<u<1. It does not exclude mixed-type excursions by the native
equations alone and supplies no weak-solution selection rule.

Independent delegated audit, 2026-11-06. Direct symbolic differentiation
with Python3/SymPy returned:

    R = A**2/gamma - 6*A*r + 6*gamma*r**2 + 3
    h at vertex = A/(2*gamma)
    R at vertex = -A**2/(2*gamma) + 3
    counterexample minimum R = 3/4

The derivative formulas above also reproduce the earlier checked
D0 identity R0=1+(1/r0-gamma r0)^2/gamma.
