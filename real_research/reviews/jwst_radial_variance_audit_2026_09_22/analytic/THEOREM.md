# Analytic counterexample to the radial extension of the uniform variance floor

This is a theorem conditional on the specified transport process. It does not
establish a new law of nature, literature novelty, or measured JWST behavior.

## Process and assertion

Photons start at the center of a unit sphere and move at speed one. Collisions
have rate k(s)=A/(a+s), where s=|x|^2, a=1/64 and A=8/log(65). The outgoing
direction is drawn from the unpolarized Thomson kernel about the incoming
direction, independently at each collision. There is no absorption. All
photons, including unscattered ones, count. Let T be first escape, Z=x_T dot u_T
and D=T-Z. Then

    E[D]=4,
    Var(D) <= 11/9 + (512/(65 log(65)))^2/11
              + 64/(3 log(65)^2)*(log(65)-64/65)
           < 273/50 = 5.46 < 32/5 = (2/5)*(E[D])^2.

The non-strict upper expression is approximately 5.45102291178808. It is an
upper bound, not the exact variance (the independent simulations give about
4.7). This disproves the extension of the uniform-model floor to all bounded,
continuous radial opacities, even within this smooth strictly positive family.
The uniform theorem itself is unaffected.

## Generator and explicit majorant

Set z=x dot u. In the interior, 0<=s<=1 and z^2<=s. The free-flight generator
is 2z partial_s+partial_z. Thomson scattering gives K1=1, Kz=0 and
Kz^2=3s/10+z^2/10. Thus L=2z partial_s+partial_z+k(s)(K-1).
These angular moments follow by integrating the normalized cosine density
3(1+mu^2)/8 and the uniform azimuth; E[mu]=0 and E[mu^2]=2/5.

Define

    F(s)=(A/2) log((1+a)/(s+a)), m(s,z)=F(s)-z,
    c=20/9, b(s)=-2F(s)-(2/3)s k(s), B1=k(1)^2/11,
    J(s)=A^2[log((1+a)/(s+a))+a/(a+1)-a/(a+s)],
    q(s)=B1+(c-1)(1-s)+F(s)^2+J(s)/3,
    U(s,z)=q(s)+b(s)z+c z^2.

All functions are smooth and bounded on the compact physical domain because
a>0. Direct differentiation yields F'=-k/2, J'=-s k^2 and
q'=1-c+kb/2. Consequently

    Lm=-1,
    LU+2m=-(4/3)(k+s k')z^2
          =-4 A a z^2/[3(a+s)^2] <= 0.

One can verify every coefficient before taking the sign: those of z^0,z^1,z^3
are zero, and that of z^2 is the displayed nonpositive rational function.
At the outgoing boundary, 0<=z<=1,

    m(1,z)=-z,
    U(1,z)-z^2=(11/9)[z-3k(1)/11]^2 >= 0.

This inequality holds on the entire boundary, not just sampled angles.
Removing B1 subtracts B1 from the boundary expression and leaves its generator
unchanged. At z=3k(1)/11, which lies strictly between zero and one for this
profile, the boundary expression is then -B1<0. This is the negative control.

## Stopping argument

Let M=A/a bound the collision rate. From any interior position and direction
the straight-line distance to escape is at most two. The conditional probability
of no collision before that escape is at least exp(-2M)>0. By the Markov property,
P(T>2n)<=(1-exp(-2M))^n. In particular T is finite almost surely and E[T^2]<infinity.
This bound is extremely loose numerically, but suffices for integrability.

The process t+m(s_t,z_t), stopped at T, has zero drift. Apply Dynkin's formula
at T wedge n and pass to the limit: m is bounded, and T is integrable. At escape
the process equals T-Z=D; at the center it equals F(0)=4. Hence E[D]=4.

For G(t,s,z)=t^2+2t m(s,z)+U(s,z), its space-time generator is LU+2m<=0.
Dynkin's formula at T wedge n therefore gives E[G(T wedge n)]<=U(0,0).
Since m and U are bounded, the absolute value of the stopped G is bounded by
T^2+2||m|| T+||U||, an integrable random variable. Dominated convergence gives
E[G(T)]<=U(0,0). At escape G(T)=D^2+[U(1,Z)-Z^2]>=D^2. Thus

    E[D^2] <= U(0,0).

The initial direction is immaterial by spherical symmetry. At any finite
stopping horizon bounded rates also ensure finitely many collisions almost
surely, justifying the piecewise deterministic generator calculation.

## Exact central bound

F(0)=4 and J(0)=A^2[log(65)-64/65]. Substitution gives

    U(0,0)=16+11/9+(512/(65 log(65)))^2/11
             +64/(3 log(65)^2)[log(65)-64/65].

The executable audit encloses log(65)=6log(2)+log(65/64) using rational partial
sums of log((1+x)/(1-x)) at x=1/3 and x=1/129. After N terms, the positive tail
is bounded above by 2x^(2N+1)/[(2N+1)(1-x^2)]: bound each denominator in the
tail below by 2N+1 and sum the remaining geometric series. For rational
l<log(65)<h, both terms in the central expression are bounded above using
A<8/l and log(65)-64/65<h-64/65; all factors are positive. Exact fraction
arithmetic at N=16 and N=20 verifies U(0,0)<1073/50<112/5. Subtracting 16
gives the asserted variance bound. Displayed decimals do not certify it.

## Audit and remaining scope

verify.py independently differentiates the explicit functions and checks the
generator, boundary square, integral primitive, negative boundary witness and
rational enclosures. It does not implement optional stopping; the argument
above supplies that mathematical implication. The candidate supersolution was
suggested in the prior handoff. Qwen's nominal passing records ce309f80 and
8080c757 used placeholder booleans and remain invalid evidence. Their failures
do not refute this separately checked calculation.

No common upper bound on opacity across different clouds is assumed here;
the single profile has a finite bound. Extension to other profiles, sharpness,
and literature novelty require separate work. See ../SOURCES.md and the new
analytic literature note; numerical verification is archived separately.
