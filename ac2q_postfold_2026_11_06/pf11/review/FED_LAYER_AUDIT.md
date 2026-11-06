# Independent audit: scalar charge coupled to surface energy

**Verdict: proved under the stated regular Israel/surface-conservation
class and an initially vanishing clock-slice charge.** The two balances
force a homogeneous surface-energy ODE. They exclude positively fed
combined concentration from zero initial charge without assuming finite
total variation of the interior scalar current. They do not exclude
arbitrary singular geometry, irregular traces, or all weak continuations.

Independent delegated derivation, 2026-11-06. Audited input: the parent's
PF11 candidate message beginning "positively fed layer may be excluded".
No PF11 input file existed at first inspection. This report is confined
to the new review directory and does not alter earlier arguments.

## Class and exact conventions

Retain the matched PF10 class without its finite-J hypothesis: smooth
native full-switch layers; r>=r_min; cap and potential/source bounds;
uniform clock convergence; regular transverse clock intersections and
strong uniform same-clock Pi matching; positive common regular outer A;
finite total stress measures; identified regular outer stress and current
traces; and a compact timelike interface. The earlier spatial/coarea
argument then gives bounded positive A and vanishing multiplier mass.
Regular side-current traces converge as required by the clock-slab
balance, and the initial slice charge converges to zero.

In addition impose the genuine Einstein junction class: a continuous
nondegenerate limiting metric with bounded approximating first derivatives,
regular piecewise outer metric traces sufficient for Israel and Codazzi,
identified native outer Einstein equations, and the resulting intrinsic
surface stress-conservation law with no unaccounted surface force. A
bare assertion that connection coefficients are bounded is not a
replacement for that conservation law or for these geometric hypotheses.

Let T be the future unit tangent to the interface and N the unit normal
pointing from the minus side to the plus side. Write [f]=f_plus-f_minus,
s for proper interface time, a=exp(2 beta_Sigma) for transverse area per
coordinate area, and tau=phi_Sigma(s). Put v=d tau/ds>0. It is sufficient
that a,v are positive with bounded inverses and W1,infinity regularity
on each compact interval. More generally the final ODE only needs
integrable logarithmic derivatives plus the stated trace identities.

The scalar current throughout is the fixed before-topological-IBP native
representative audited in PF10. Write j=J/E in a regular orthonormal frame.
No total-variation bound on this current inside the layer is assumed.

## 1. Constitutive measures and the equation of state

Finite transverse stress and bounded A,P imply a uniform r^4 measure
bound. Terms of degree at most three in r have vanishing integral over
the shrinking layer by Holder's inequality and its vanishing volume.
The exact constitutive expressions therefore have surface parts

    H_surface=(gamma/2) m,
    (r h)_surface=2 gamma m,
    (T_perp)_surface=(gamma/2) m,
    (tr_base T)_surface=-gamma m,

where m is the nonnegative r^4 concentration measure per proper interface
volume. Multiplier mass vanishes, and bounded P W_P has no surface part.
These leading terms are independent of the unbounded clock boost.

Normal no-dipole and symmetry remove longitudinal normal components, so
the surface tensor has longitudinal part sigma T_a T_b. Planar symmetry
gives equal transverse pressure p. Its base trace is -sigma. Consequently

    sigma=gamma m,    p=gamma m/2=sigma/2.

These statements initially hold as measure identities. They do not
assume m already has a density in s, nor that separate boosted stress
terms have finite measures. Only the total stress measure is used.

## 2. Scalar charge identifies that density

The exact slice charge is

    Q_epsilon(tau)=integral exp(2 beta)
                    r(3-2Ar+2 gamma r^2) d ell.

The clock-slab balance with converging regular side fluxes and convergent
initial charge gives a finite absolutely continuous limit q(tau), and
q>=0. This is obtained from the scalar equation and boundary fluxes;
there is no hidden uniform upper slice-charge assumption.

Coarea and the exact clock contraction give the limiting measure identity

    q(tau) d tau=2 gamma a(s) m(ds).

Here m(ds) denotes the concentration measure per transverse proper area.
Uniform phi convergence and bounded r^4 mass justify pushing the measure
to the common clock trace; no strong convergence of clock gradients is
required. Lower-order r terms vanish as above. Since d tau=v ds with
v positive and regular, m is in fact absolutely continuous. Writing its
density as m(s) now gives

    q(phi_Sigma(s))=2 gamma a(s)m(s)/v(s)
                  =2 a(s)sigma(s)/v(s).

Thus q0=0 implies the initial sigma trace is zero. Initial absence of a
spacetime current measure alone would not supply this slice condition.

## 3. Outer stress/current identity, including its factor

At either regular outer trace put b=N(phi), so

    n=(v/r)T-(b/r)N,
    k=r h-mu Q,
    T(N,T)=k b v/r^2.

The exact specified scalar current gives

    j_N=-k b/r^2+(A/a) partial_s Pi.

Therefore the outer identity is

    T(N,T)=-v j_N+(A v/a) partial_s Pi.

The factor v on the Pi term is essential in the pointwise formula.
The candidate's jump relation is nevertheless correct: a,v,A and the
tangential derivative of the common regular Pi trace agree on both
sides. Strong matching plus regular outer traces are used here; weak
value matching without regular tangential traces is insufficient.
Taking the jump gives

    [T(N,T)]=-v[j_N].

This calculation uses neither a measure limit nor a bound for the
interior scalar current.

The outward-normal sign convention in the clock-slab balance gives

    d q/d tau= -a[j_N]/v,
    d q/ds= -a[j_N]=a[T(N,T)]/v.

The factor a is the transverse coordinate-area weight; the factor 1/v
converts proper interface time into the clock label for the first line.

## 4. Independent surface energy balance

Israel/Codazzi and the regular native outer Einstein equations give

    (a sigma)' + p a'=a[T(N,T)],

where primes now mean d/ds. The sign can be checked in a flat fixed-area
frame: T^{0N}=-T(N,T), and total energy conservation gives
sigma'=-[T^{0N}]=[T(N,T)]. The p a' term is the work of the two equal
transverse pressures; a'/a is the total transverse expansion, so there
is no additional factor of two.

The use of Israel/Codazzi is substantive. One must not obtain this law
merely by replacing the weak product Gamma_epsilon T_epsilon by a
chosen limiting Gamma times S. The regular junction geometry and its
outer Einstein equations supply the surface law independently. Uniform
bounded first derivatives rule out a quadratic gravitational surface
concentration; regular outer traces provide the common intrinsic
geometry and the Israel jump. Unidentified bulk or geometric defects
would require an additional term and fall outside this argument.

## 5. Homogeneous ODE and zero-charge consequence

Set Y=a sigma. Differentiating q=2Y/v and using the scalar balance gives

    2Y'-2Y v'/v=a[T(N,T)].

The independent energy balance gives the same right side as Y'+p a'.
With p=sigma/2=Y/(2a), eliminate that flux to obtain

    Y'=2Y v'/v+Y a'/(2a),
    sigma'=(2v'/v-a'/(2a)) sigma.

Thus the general solution on a regular connected interval is

    sigma(s)=C v(s)^2/sqrt(a(s)),
    q(phi_Sigma(s))=2C v(s)sqrt(a(s)).

An initially vanishing slice charge fixes C=0. Hence sigma=p=m=0 and
there is no r^4 surface concentration or total matter surface stress.
In particular positive inward scalar feed cannot generate a new layer
from zero within this class: it would violate the independent surface
energy balance and the exact common-trace stress/current identity.
The outer flux then matches as a consequence, rather than being imposed
in advance. Nonzero pre-existing layer charge would leave C undetermined
by this argument and is not excluded by the ODE alone.

## Scope of the closure

This closes the positively fed escape left by the scalar-only PF10 slab
balance for the regular matched Einstein junction class with zero initial
slice charge. It neither assumes finite interior J variation nor derives
such a bound. It also does not select outgoing field data or prove a
native post-breakdown solution exists.

The proof does not cover irregular tangential Pi/A traces, failure of
side-current convergence, singular or degenerate interface geometry,
nonintegrable logarithmic derivatives of v or a, cap/source concentration,
r approaching zero, unmatched polarization, null interfaces, unidentified
bulk defects, or failure of the regular Israel conservation law. Those
are distinct exclusions from the theorem's hypotheses, not demonstrated
native continuations. No universal weak-nonexistence conclusion follows.

## Actual-file audit and one forced correction

Subsequently read `pf11/FED_LAYER.md`, SHA256
`dfd460d176d86feee132612a879eb3b52d9246dec0861e4236e7567a8a05e57e`.
The substantive argument agrees with this independent derivation. Its
Section 2 contains a time-variable typo: the displayed
`dq/ds=-a[J_N]/v` must be `dq/ds=-a[J_N]`, or equivalently
`dq/dtau=-a[J_N]/v`. Section 3 and the final amplitude ODE already use
the correct `dq/ds=a f/v`. The verdict for that exact file is correct
after this forced correction; the error does not change its final ODE.

The geometric assumption in that file explicitly requires the
gravitational thin-shell limit and intrinsic surface-energy conservation.
Read its assertion about bounded first derivatives and common regular
tangential traces within that Israel/identified-outer-Einstein setting;
do not detach it into a generic theorem about products of weak measures.

## Verified extension to continuous positive clock speed at birth

The zero-birth conclusion does not need a global bound on v'. Suppose
a is positive C1, v is positive continuous with local upper/lower bounds,
f is locally integrable, and the two limiting balances above hold with
q absolutely continuous. The measure identity gives y=a sigma=qv/2.
Energy conservation then implies

    y'=a f-(a'/(2a))y,

so y has an absolutely continuous representative. On any open connected
component of {q>0}, the identity v=2y/q makes v locally absolutely
continuous. The previous calculation is therefore valid almost
everywhere on that component and yields

    q/(v sqrt(a))=constant.

If the component has a left endpoint where q=0, continuity of q,v,a and
their positive finite bounds force this constant to be zero, contradicting
q>0 on the component. If q(s0)=0, every hypothetical positive component
has such an endpoint, including one beginning immediately after s0.
Hence q remains zero throughout the connected regular interval.

This establishes the proposed continuous-v birth extension without
assuming differentiability of v at the zero-charge endpoint. It does
not permit v to vanish or diverge there, nor drop the limiting scalar
and energy balances or the initial slice-charge limit. A common bounded
smooth prebreak slice makes Q_epsilon=O(epsilon) and supplies q0=0 when
the same approximating solutions and controlled side balances connect
that slice to the interval. An uncontrolled corner exactly at birth
without this incoming approximation/charge control remains outside.

## Final corrected-file review

Read the full revised `pf11/FED_LAYER.md` and verified SHA256
`520988144ef75ab9ddd89e6d617ddaf6415bceb36ea657c5f9ee657592e2c2b7`.
**Verdict for this exact revision: proved as written in its stated
regular matched thin-shell class.** The proper-time scalar balance is
corrected; the continuous-positive-v extension and the Codazzi-based
geometric qualification are both included and pass.

To make the latter implication explicit, take the conventional spacelike
normal extrinsic curvature and Einstein normalization M. Israel gives

    S^i_j=-M([K^i_j]-delta^i_j[K]).

Outer Codazzi, the common intrinsic metric/connection, and the native
outer Einstein equations give

    D_i S^i_j=-[T_Nj].

For the induced metric -ds^2+exp(2 beta_Sigma)(dy^2+dz^2), its time
component is exactly (a sigma)'+p a'=a[T(N,T)]. Sufficient classical
regularity is piecewise C2 outer metrics, common regular induced metric,
and extrinsic-curvature traces with the tangential regularity needed for
Codazzi; weaker regularity is permissible when these identities hold
distributionally. Uniformly bounded approximating first metric
derivatives and regular identified outer traces isolate the Israel
surface term: quadratic first-derivative terms have vanishing strip
mass. This reasoning does not claim convergence of arbitrary interior
connection-times-stress products. The corrected candidate appropriately
requires the Israel relation and outer Codazzi constraints themselves.

No extra finite-current assumption or globally bounded v' has entered
this final review. The initial slice-charge and regular-side-flux limits
remain indispensable hypotheses.
