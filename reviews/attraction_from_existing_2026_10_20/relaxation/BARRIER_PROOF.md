# Removal of the support constraint by shifted cumulative barriers

20 October 2026. This proves the exact support and isolation statement
for the variational minimum in `SUPPORTED_CONTINUATION.md`. The construction of the
barriers was proposed by the parent lane; the comparison, constants,
units and exterior obstacle inequalities were reconstructed here.
Same equation inputs and pinned source hashes as the other lane files.

Let `h0` be a normalized smooth density, positive on `b<r<a`, vanishing
smoothly at its endpoints, where `b=a/2`. Its cumulative `H0` is zero
below `b`, one above `a`. Let
`j(s)^2=GM0 r0(s)`, where `r0` is the quantile of `H0`, and
`J(s)=integral_0^s j(v)^2 dv`. At the endpoints define
`j(0)^2=GM0 b`, `j(1)^2=GM0 a` by continuity.

Choose `I=[l,u]` with `0<l<b<a<u` and a fixed shift

    0<e<min(b-l,u-a).

For example `l=a/4`, `u=7a/4`, `e=a/8` works. First minimize on the
slightly larger scalar obstacle class `0<=H<=1`, with the same `H1`
regularity and endpoint traces, temporarily dropping `H'>=0`.
The same coercivity, convexity and lower-semicontinuity proof gives a
unique minimizer `H_z`. The monotonicity proof below shows that it is
also the physical monotone minimizer of the continuation. Divide
its energy variation by its positive total mass `z`. The operator is

    L_z(H) = [j(H)^2-GM0 r]/r^3
              -gamma z/(4 pi) (H'/r^2)'
              +R(GzH/r^2),                             (1)
    R(v)=v^2/(a0-v).

For smooth monotone comparison functions define

    Hplus(r)=H0(r+e),   Hminus(r)=H0(r-e).

Their endpoint values are still zero and one on `I`. Define a finite
constant

    M=max_(r in I, sign=+/-)
            [r |H0''(r+sign e)|+2|H0'(r+sign e)|].

It has units of inverse length. Require a positive `z` small enough that

    Gz/l^2<a0,
    gamma z M/(4 pi)
      +G^2 z^2/[l(a0-Gz/l^2)] < GM0 e.                 (2)

Both terms on the left vanish as `z->0`, so this is a nonempty explicit
small-mass condition. Every term in its second line has units of
specific angular momentum squared. No pressure coefficient, source
potential or additional interaction is being selected.

## 1. Supersolution and subsolution inequalities

Where `0<Hplus<1`, the tracer action relation gives
`j(Hplus(r))^2=GM0(r+e)`. Where `Hplus=0`, its endpoint value instead
gives `j(0)^2>=GM0(r+e)`. Consequently, everywhere that `Hplus<1`,

    j(Hplus)^2-GM0 r >= GM0 e.                         (3)

Similarly, wherever `Hminus>0`, including its upper plateau,

    j(Hminus)^2-GM0 r <= -GM0 e.                       (4)

After multiplying (1) by `r^3`, the stiffness term has magnitude at
most `gamma z M/(4 pi)`, because
`r^3(H'/r^2)'=rH''-2H'`. The remainder obeys uniformly on `I`

    0<=r^3 R(GzH/r^2)
       =G^2 z^2 H^2/[r(a0-GzH/r^2)]
       <=G^2 z^2/[l(a0-Gz/l^2)].                       (5)

Thus (2)-(5) prove the obstacle-appropriate inequalities

    L_z(Hplus)>0 where Hplus<1,
    L_z(Hminus)<0 where Hminus>0.                      (6)

No inequality at the other plateau is needed, because the relevant
positive-part comparison vanishes there.

## 2. Weak comparison preserving monotonicity

Let `w=(H_z-Hplus)_+`. The function
`min(H_z,Hplus)=H_z-w` belongs to the enlarged scalar obstacle class,
with the same bounds and endpoints; monotonicity of `H_z` is not yet
needed. The
variational inequality for `H_z` therefore gives
`<L_z(H_z),w><=0`. Equation (6) gives
`<L_z(Hplus),w>>=0`. Subtracting,

    <L_z(H_z)-L_z(Hplus),w> <=0.                       (7)

On the support of `w`, `w'=H_z'-Hplus'` almost everywhere. The left
side of (7) is the sum of

    integral [j(H_z)^2-j(Hplus)^2] w/r^3 dr,
    gamma z/(4 pi) integral (w')^2/r^2 dr,
    integral [R(GzH_z/r^2)-R(GzHplus/r^2)] w dr.

All three are nonnegative; strict monotonicity of `j^2` makes the first
strictly positive if `w` is nonzero. Hence `w=0` and `H_z<=Hplus`.
Apply the same argument to
`v=(Hminus-H_z)_+` and the admissible `max(H_z,Hminus)` to obtain

    Hminus <= H_z <= Hplus.                            (8)

Only weak `H1` variations were used. No smooth free-boundary theorem,
second derivative of `H_z`, or singular IFT is assumed.

## 3. Exact finite support and no endpoint reaction

Equation (8) gives exact equalities, not merely convergence in norm:

    H_z(r)=0 for r<=b-e,
    H_z(r)=1 for r>=a+e.                               (9)

These regions contain neighborhoods of both ends of `I`. Extending
`H_z` by zero/one therefore introduces no boundary stiffness force or
hidden wall work. It is enough to check the global obstacle variation
outside `I`.

There is no hidden monotonicity multiplier: the minimizer of the larger
scalar obstacle class is itself nondecreasing. Here is an elementary
one-dimensional check. Its quadratic gradient coefficient is strictly
positive on `I`, while the reaction is continuous and bounded. The weak
obstacle equation therefore gives a continuously differentiable
minimizer, twice differentiable on the active set; at contact its first
derivative is zero. This regularity can also be checked by integrating
the active equation and observing that a derivative corner at contact
would be lowered by rounding the corner in the quadratic gradient
energy, with only a higher-order change in the bounded potential.

Put `F(r,H)=j(H)^2-GM0r+r^3R(GzH/r^2)`. It strictly increases in `H`
and strictly decreases in `r`, since at fixed `H`, with `v=GzH/r^2`,

    partial_r F=-GM0+r^2[3R(v)-2vR'(v)]<0,
    3R(v)-2vR'(v)=-v^2(a0+v)/(a0-v)^2<=0.

At an active local maximum the equation
`F=gamma z(rH''-2H')/(4 pi)` gives `F<=0`; at an active local
minimum it gives `F>=0`. The same inequalities hold at upper/lower
obstacle contacts by their variational signs. If a downward segment
existed, the endpoint values zero/one would force a local maximum
`r1` followed by a local minimum `r2>r1`, with `H(r1)>H(r2)`.
Monotonicity of `F` in its two arguments would give
`F(r1,H(r1))>F(r2,H(r2))`, contrary to those signs. Thus `H_z'>=0`.
This establishes admissibility without assuming a pressure closure.

For `r<l`, the extension has `H=0`, zero stiffness and remainder
derivative, and

    L_z(0)=GM0(b-r)/r^3>0.

This is the correct lower-obstacle sign. For `r>u`, the extension is
`H=1` and

    r^3 L_z(1)=GM0(a-r)+r^3 R(Gz/r^2)<0.               (10)

Indeed `r^3 R(Gz/r^2)=G^2 z^2/[r(a0-Gz/r^2)]`
decreases strictly with `r` on the admissible branch. It is bounded by
the left remainder bound in (2), which is less than `GM0e`, whereas
`GM0(r-a)>=GM0(u-a)>GM0e`. Thus (10) is the correct upper-obstacle
sign on the whole exterior.

The scalar obstacle variational inequality is local: on its active set
the Euler derivative is zero, on its lower obstacle it is nonnegative,
and on its upper obstacle it is nonpositive. Because (9) gives flat
endpoint neighborhoods, its extension creates no boundary distribution.
The interior scalar obstacle inequality and exterior signs above hence
give the global scalar obstacle variational inequality, including tests
with different traces on `I`. Since `A`, stiffness and full remainder are convex in the
cumulative `H`, and `A` is strictly convex, the extension is the unique
global radial minimizer among normalized monotone cumulatives with
finite admissible energy and the same rank actions. There is no radial
support force in this statement.

An additional exterior spherical baryonic shell and still more exterior
free shell do not spoil the conclusion when their radii exceed `a+e`.
Their potential is constant over the occupied inner support. For an
outward hypothetical variation beyond either exterior shell the ordinary
inward gravitational term only makes the upper-obstacle sign more
negative. Hence the supported inner minimizer remains the correct
rank-action radial minimizer in the full separated shell system.

## 4. Consequence and exact scope

For all sufficiently small masses `z` satisfying (2), the continuation's
energy expansion and curvature apply to an isolated radially supported
inner state, with no artificial annulus reaction. Choose the host
radial branch so `q_n>a+e` and the free stock still farther out. Then
the shape Hessian (4) of the continuation is positive at fixed
occupation; its mixed derivative with the host/free radii vanishes
because their potential is constant through the inner support. Together
with the positive host/free radial Hessians this proves stability of
the retained rank-preserving spherical mechanical directions at each
fixed positive occupation. Empty components have no responder variable.

This does not prove nonspherical collisionless stability, permit angular
action exchange or shell crossing, or supply an S4 conversion trajectory,
microscopic site trace, response-charge receiver, heat bath or transition
rate. These remain the physical gaps. The barriers close the narrower
analytic support/reaction gap only.

Verification is analytic reconstruction of (1)-(10). No scientific
computation or old packet was run or edited. Review provenance is a
parent-suggested construction independently checked in this delegated
lane; it is not blind external review or formal proof certification.
