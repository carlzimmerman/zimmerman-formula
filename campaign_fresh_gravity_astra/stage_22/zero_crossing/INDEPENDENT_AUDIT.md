# Independent audit: a local signed Q zero crossing

Reviewer: /root/pressure_extrema. **Accepted conditional local result**, with
the Hölder-regularity justification made explicit below. I inspected the
pinned ROOT_DERIVATION.md only; no new author or metric_intake proof was read.
No numerical computation was run. The reviewed source hash is recorded in
audit_result.json and matches the requested pin.

## Signed static equations and local solution

For the even gradient energy W(|g|,a), differentiation with respect to signed
g gives B=sgn(g)b(|g|,a). Its inverse is exactly
g=sgn(B)sqrt(B²+a|B|). The static phi equation is B_x=C rho; hydrostatic
balance and the chi equation have the signs displayed in (1). Positive rho
makes B strictly increasing. Therefore a crossing initialized at B=0 has
negative B and g to the left and positive B and g to the right. No constant
source subtraction or central sheet has been inserted.

The change of independent variable u=B is legitimate where rho stays positive.
Dividing each static derivative by C rho gives all five equations (2),
including the cancellation of rho in rho_u. For fixed u, differentiation
of |g| with respect to chi gives av/(2sqrt(v²+av)), v=|u|. Its extension
at v=0 is zero and its magnitude is uniformly O(sqrt(v)) on a compact
positive-a box. The other state derivatives of this part remain bounded.

The composed T has order v^(3/2) with bounded smooth dependence on a after
factoring that power. Its chi derivatives therefore have the stated uniform
order. All reciprocal-rho factors are uniformly regular on the selected
positive-density box. Thus the full right-hand side is continuous in u and
uniformly locally Lipschitz in the state. It need not be Lipschitz in u.
The integral-map contraction on a sufficiently small two-sided interval
therefore proves existence and uniqueness of a C1 state solution in u.
Positive x_u gives the monotone C1 inverse and the stated spatial equations.
This proves only the specified nearby regular class, not uniqueness among
arbitrary distributional continuations.

## Asymptotic signs and failure of H2

Continuity, B_x=C rho and chi_x=w give
B=C rho_* x+o(x) and a=a_*+O(x). Hence the signed leading gradient is
sgn(x) k sqrt(|x|), k=sqrt(a_* C rho_*). Integrating on the negative side
also gives a **positive** increase in phi away from its center minimum;
the coefficient2k/3 in (3) is correct. The exact hydrostatic exponential
then gives the displayed density decrease. These estimates improve
B-C rho_* x to O(|x|^(5/2)).

Differentiating the exact expression separately for B>0 and B<0 gives the
same formula

    g_x=[(2|B|+a)C rho+B a_x]/(2|g|).

In particular the a_x term involves signed B. Its leading numerator is
a_* C rho_* and its denominator2k sqrt(|x|), so
g_x=k/(2sqrt(|x|))+O(sqrt(|x|)). The nonzero leading coefficient proves
g_x is not square integrable; this conclusion does not rely on differentiating
an uncontrolled little-o term.

The continuous g is locally absolutely continuous: its classical derivative
on each side is integrable and its one-sided limits agree at zero. It is
Hölder1/2, as may also be seen by writing it as sgn(x)sqrt(|x|) times a
locally Lipschitz nonzero coefficient. Thus phi is C^(1,1/2), is W^(2,p)
for1<=p<2, and is not H2 on any neighborhood of the crossing.

The exact differentiated hydrostatic equation gives

    rho_xx=rho g²/cs^4-rho g_x/cs².

Its leading singular term is -rho_* k/(2cs² sqrt(|x|)), which is nonzero.
The same W^(2,p)-but-not-H2 conclusion follows for rho, and rho is
C^(1,1/2). This is a local crossing result, not a statement about arbitrary
zeros of the field or arbitrary density profiles.

## Explicit justification of the chi Hölder regularity

The source states that T_x is continuous and O(sqrt(|x|)) and concludes
T in C^(1,1/2). That growth statement **alone** would not imply Hölder
regularity. In this model the required stronger conclusion follows from
the constitutive composition, as follows; no change of equation is needed.

For v=|B| and r=sqrt(v²+av), the analytic Q expansion gives

    T(r,a)=v^(3/2) F(v,a),

where F is smooth on a sufficiently small nonnegative-v box with a bounded
away from zero. This follows by factoring r³/a from the odd power series
of T and using r²=v(v+a). Initially the spatial equations already give
rho in C1, B in C2, chi in C2 and a in C2. Thus B', a' and the composed
smooth coefficients are locally Lipschitz. On the two sides,

    T_x=(3/2)sgn(B)sqrt(v) B' F
         +v^(3/2)(F_v sgn(B) B'+F_a a').

The first term extends as a Hölder1/2 function and the remaining terms
are at least Hölder1/2. All tend to zero at the crossing. Hence T is
indeed C^(1,1/2). The equation chi_xx=(U'-T)/J then gives chi_xx in
C^(1,1/2), and therefore chi in C^(3,1/2). Its center value is
chi_xx(0)=U'(chi_*)/J. The stronger C4 property is not established or claimed.

This additional reconstruction closes the abbreviated Hölder inference in
the source; it is not inferred solely from an O(sqrt(|x|)) bound.

## Weak equations, finite energy and Hessian

B is C1 and satisfies B_x=C rho with no jump. Its distributional derivative
has no delta component. The other displayed fields/fluxes have sufficient
local regularity for integration by parts without an extra crossing boundary
source. Hydrostatic pressure is continuous and differentiable. The static
energy is finite because W=O(|x|^(3/2)), while the chi gradient/potential,
fluid and interaction terms are locally bounded. The action does not contain
a phi_xx-squared term, so phi not being H2 does not imply infinite energy.

For signed gradients, W_gg=A=b_r, W_gchi=-q_s and W_chichi=-S, where
q_s=sgn(g)(|g|A-b) and S=2T-|g|q. These signs and the m=U''-S term agree
with (5). In flux coordinates
A=2sqrt(B²+a|B|)/(a+2|B|) and q_s=aB/(a+2|B|), including the negative side.
All these second derivatives are continuous and vanish at the crossing.
Thus the even energy is C2 there, although its strictly positive spatial
quadratic lower bound degenerates.

The fluid tangent d=-(rho xi)_x lies in L2 for H1 displacement because rho
and rho_x are bounded and rho stays positive. Every term in (5) is bounded
as a quadratic form on H1_0 triples. Smooth-direction second variations are
legitimate with this C2 field energy and positive density; the equilibrium
chemical potential removes mass-preserving higher density variations. No
division by the vanishing A or smooth-H2-background inverse is justified by
this Hessian statement, and none is used.

## Exact norm obstruction and scope

With psi_delta=sqrt(delta) f(x/delta), its derivative L2 norm is constant
and its L2 norm squared is delta² times that of f. Setting xi=eta=0 removes
the matter and mixed terms. The remaining positive integral is bounded by
sup A on the support times the fixed derivative norm, which tends to zero
as O(sqrt(delta)). Therefore no positive uniform lower bound by the standard
product H1 norm can hold. Fixed positive dimensional reference weights do
not alter this countersequence.

Every nonzero test in that sequence has positive energy, since A>0 except
at a single point. The argument proves neither a negative direction nor
the loss of an L2 kinetic gap; its L2 norm is also shrinking. A weighted
closed-form, transmission or spectral theory remains a separate problem.
The positive time kinetic term is not a ghost criterion failure, and no
nonlinear stability or ill-posedness result follows.

The construction supplies induced local wall/mass data rather than a
prescribed boundary-value family or an extension of FGF034 through its
excluded zero-gradient set. It retains signed MOND source balance but gives
no observed mass discrepancy, physical metric/photon completion, RAR/M or
filtered-MONO transfer, evolving-H solution, literal vacuum identity or
physical-theory closure. Both positive reference normalizations and frozen
history comparisons remain separate conditional choices.
