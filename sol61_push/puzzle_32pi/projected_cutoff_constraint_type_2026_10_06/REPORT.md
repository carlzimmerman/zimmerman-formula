# Finite vacuum moment versus everywhere elliptic relative lapse

For the actual projected-acceleration action, a positive MOND boost with finite vacuum kernel moment cannot retain the deep-branch elliptic relative-lapse spatial row at every field magnitude, assuming a smooth globally invertible spherical source map. This is a new conditional constraint-type obstruction. The physical nonlinear-Poisson force operator can remain elliptic while this gravitational relative-lapse row changes type. No time instability, complete coupled constraint classification or all-MOND no-go follows.

Base 67e981cf7888172c584868ae80a178492af40fa1. This uses the exact nonlinear ADM relative-lapse principal tensor and the actual projected NR source dictionary, not the old difference-connection operator or QUMOND's field equation. Claude p57 supplies a declared example kernel, not a selected cutoff.

## Uniform statement and proof

For n>=3 spatial dimensions, the actual interaction invariant is I=h^{ij}r_i r_j/a0², h positive, r=ln(N/L), and m=M_I. The relative-lapse Hessian principal tensor is a positive prefactor times

m h^{ij}+2M_II(h grad r)^i(h grad r)^j/a0².

Its transverse eigenvalue is m and longitudinal eigenvalue is d_parallel=m+2I M_II=m+x dm/dx, x=sqrt I. This is a spatial constraint symbol, not a physical time-kinetic matrix. The mixed common/relative block also contains the previously derived transport operators B,B*, and neither these nor the relative spatial preservation rows are eliminated here.

The spherical projected source equations give y=mu(x)x, mu=1−2m, physical g/a0=(1−m)x. Matching a prescribed visible spherical nu(y)>1 gives

x(y)=(2nu−1)y=y+b(y), b(y)=2y(nu−1)>0.

Assume x is C1 on y>0 with x'(y)>0 and the matched action is differentiable there. Then

mu+x mu'=dy/dx=1/x'(y)>0,
m=(1−y/x)/2=b/(2x)>0,
d_parallel=(1−dy/dx)/2=(x'−1)/(2x')=b'/[2(1+b')].

Thus force ellipticity does not imply relative-lapse ellipticity. An everywhere nonnegative longitudinal relative coefficient would require b'>=0 everywhere. If b is nonnegative, positive somewhere and has a finite positive moment

J=int_0^infinity(nu−1)d(y²)=int_0^infinity b(y)dy<infinity,

that is impossible: choose a point b(y0)>0. A nondecreasing b would satisfy b(y)>=b(y0) for all y>=y0 and force J to diverge. Hence there is a point with b'<0; by continuity there is a negative-derivative interval. At such an interior point nonnegative b must be positive, and the assumed x'>0 makes d_parallel<0 while m>0. The relative spatial row is mixed there in n>=3. The deep law nu~y^(-1/2), with its differentiable asymptotic, gives b' positive near zero, so a longitudinal zero/type boundary lies between the deep and negative intervals.

The conclusion applies even without a pointwise b(infinity)=0 hypothesis; finite positive integral and differentiability suffice. It requires a nonnegative boost. Sign-changing kernels, non-smooth/multibranch maps, different covariant operators or a full constrained resolution are separate routes. This is not the old horizon/one-pi obstruction, nor simply freedom to add a vacuum constant: it ties finiteness of the UV-normalized kernel moment to a specific generic-source gravitational constraint symbol.

## Claude cutoff: exact global source-map gate

Take p57's nu=1+e, e=[sqrt(1+1/y)−1]/[1+(y/T)²], T>0. Let s=sqrt(1+1/y)>1, t=T² and D=t+y². Differentiation gives

x'=1+t(s−1)²/(sD)−4t y²(s−1)/D².

Multiplying by sD²/y^4 gives the quadratic

P=(s²−s+1)u²+(−3s²+4s+1)u+s, u=t/y²=t(s²−1)².

The discriminant is (s−1)(9s³−19s²−5s−1). The cubic has exactly one root s0>1. For s>s0, the two positive roots u_minus,u_plus bound precisely the interval with x'<0. Their cutoff values T_plus/minus=sqrt(u_plus/minus)/(s²−1) form a continuous family; its union is (0,Tcrit), with the endpoint Tcrit giving an isolated zero of x'. Tcrit is the unique interior maximum of T_plus. Eliminating t between P(s,t)=0 and its derivative at fixed t gives, apart from the excluded s=1 and −1,

R(s)=45s^8−132s^7+62s^6−24s^5+12s^4−20s^3−6s²−1=0.

Exact Sturm root counts give exactly one R-root above1, s*=2.45661008410…, on the upper-root branch. Checking its position above s0, the nonzero upper-branch derivative at the birth and its zero limit at infinity fixes the unique global maximum. Numerically,

Tcrit=0.20863684329757…, y*=0.19861237062816….

For T>Tcrit the entire spherical x-map has strictly positive derivative and a smooth inverse; for T<Tcrit it folds. At equality it is still monotone with an isolated zero derivative, so the inverse is not smoothly regular there. This threshold does not select T=128.915. All larger T values form a continuous admitted source-map family.

## Exact radial constraint crossing

For the same kernel, b'=0 simplifies without a numerical minimizer to

T²=(3s+1)/[(s−1)^3(s+1)^2].

The right side decreases strictly from infinity to zero on s>1. Consequently every T has exactly one positive-y crossing of d_parallel, provided the source map is globally regular. On the small-y side d_parallel is positive and on the large-y side it is negative. At the declared p57 T=128.915 the crossing, m and relative coefficients are recorded at full precision in the bounded result; both sides are also checked. This field scale is distinct from the cutoff T and from the fold threshold above.

The example's vacuum moment is finite because b~2sqrt(y) near0 and b~T²/y² at infinity. With the usual vanishing endpoint normalization of the eliminated action, A=J; that optional normalization still leaves T free. The mixed spatial constraint appears for every positive finite cutoff, including the target-sized one, rather than selecting a preferred member. A full mixed transport/relative-force reduction could change the physical interpretation of this row; it must be done before treating this as a viable model exclusion.

## Evidence and next question

checks.py reconstructs the source derivative, principal identity, polynomial/discriminant/resultant, exact Sturm counts and monotonic crossing function; bounded high-precision roots provide the p57 example. Controls conflate force and lapse ellipticity, equate finite moment with a chosen cutoff, or erase derivative response. The proof above carries the uniform claim; bounded computations are corroboration. No covariance/DOF theorem follows from the counts. The next uncertain implication is whether the coupled nonlinear constraints resolve or obstruct this spatial type change on an admitted sourced background.
