# Gaussian-source limit of the STF quadrupole

Claim: fix eta>0 and lambda>0. Let the Solar source be a normalized spherical
Gaussian of dimensionless width sigma, with the same fixed external field
and the KT37 action. Include both smooth-core contacts from DERIVATION.md.
Then its STF quadrupole tends, as sigma decreases to zero, to the exterior
point-field Green integral with zero origin contacts.

This proves the stated Gaussian regularization limit for this observable.
It does not define the nonlinear action on a distributional Hessian, assert
regulator independence, or give a uniform estimate as lambda also tends to
zero. The lambda=0 control is separately the inherited QUMOND calculation.

## Angular cancellation estimates

At a fixed radius put h=lambda^2(gp^2+2gt^2), so z=x+h and derivatives below
are with respect to x, holding h fixed. The simple-Q primitive has, for
sufficiently large z,

```
|R^(j)(z)| <= c_j z^(-j-1/2), j=1,2,3,4.
```

These follow by differentiating its explicit algebraic/asinh expression;
the lower-order logarithmic terms decay faster than the displayed powers.
Since 0<=x<=z,

```
|C_xx| <= C z^-5/2,
|C_xxx| <= C z^-7/2,
|D_xx| <= C lambda^2 z^-5/2.
```

The constant C can be enlarged independently of x and h once z is above
a fixed threshold. For an angular function J(x0+v mu), Rodrigues' identity
and integration by parts yield

```
integral P_l(mu) J(x0+v mu) dmu
 = v^l/(2^l l!) integral (1-mu^2)^l J^(l)(x0+v mu) dmu.
```

Using v=2eta g, b=-2(g C_2+eta C_3), and d=2D_2 therefore gives

```
|b| <= C[eta^2 g^3 sup|C_xx|+eta^4 g^3 sup|C_xxx|],
|d| <= C eta^2 g^2 sup|D_xx|.
```

Here C_l and D_l mean the unnormalized angular Legendre integrals. These
estimates preserve the angular cancellations that are lost by bounding the
vector or tensor norm before its STF projection.

## Uniform small-radius bound

Write s=r/sigma and g=sigma^-2 f(s), where

```
f(s)=P(3/2,s^2/2)/s^2.
```

This positive smooth function satisfies f(s)~c s/3 at zero and f(s)~s^-2
at infinity. Also f'(s)-f(s)/s=O(s^2) at zero and is O(s^-3) at infinity.
It follows, with constants independent of L>=1, that

```
integral_0^L s^4/f(s)^2 d(log s) <= C L^8,
integral_0^L s^6/f(s)^4 d(log s) <= C L^14,
integral_0^L s^3 |f'(s)-f(s)/s|/f(s)^3 d(log s) <= C L^6.
```

The origin integrands are O(s^2); the stated large-s powers give the
upper bounds. Positivity and continuity handle the intervening compact
interval.

Take any sufficiently small radius delta and any sigma<=delta, and put
L=delta/sigma>=1. The enclosed Gaussian mean density decreases radially,
so for r<=delta,

```
gt=g/r >= P(3/2,L^2/2)/delta^3
          >= P(3/2,1/2)/delta^3.
```

Thus z>=2lambda^2 gt^2 is uniformly large on this entire core once delta
is small enough. We may use the derivative and angular bounds above. Since
z>=2lambda^2g^2/r^2, integration of the Green integrands gives

```
|q_A,flux(core)|
 <= C[eta^2 delta^8/lambda^5+eta^4 delta^14/lambda^7],
|q_B,flux(core)| <= C eta^2 delta^6/lambda^3.
```

For example, the B integrand is bounded by
C eta^2 |gp-gt| r^3/(lambda^3 g^3); rescaling r=sigma s and using the
third integral bound produces sigma^6 L^6=delta^6. The two A terms use
the first and second integral bounds similarly.

These estimates are uniform for all sigma<=delta. The exterior point field
g=r^-2 obeys the same small-delta orders directly. Therefore neither core
can retain a finite hidden STF contribution in the shrinking limit.

The smooth-core contacts also vanish uniformly as sigma tends to zero:
k=c/(3sigma^3), z0>=3lambda^2 k^2, and the displayed derivative bounds give

```
|q_A,contact|+|q_B,contact| <= C eta^2 sigma^6/lambda^3.
```

## Exterior convergence

Fix delta>0. On r>=delta, the Gaussian enclosed mass and its radial
derivatives tend to the point-field expressions uniformly on every compact
interval. The coefficients C,D are smooth there because lambda>0 and the
radial Hessian norm is nonzero. At sufficiently large r, g<=eta/2, hence
z>=eta^2/4 and all required coefficient derivatives are bounded uniformly.
The angular estimates then bound the A and B integrands by constant multiples
of r^-7 and r^-9 respectively, against d(log r). Gaussian g<=r^-2, and
|gp|+|gt|<=C r^-3 uniformly: the density term is bounded using
s^3 exp(-s^2/2)<=C. These are integrable uniform tails.

Dominated convergence therefore applies on r>=delta. Sending sigma to zero
there, then sending delta to zero using the uniform core estimates and
vanishing contacts, proves the claim. Outer surfaces vanish under the same
large-radius estimates.

This is an analytic companion to the finite-core numerical checks. It was
self-derived after the first numerical run; independent review of this new
limit argument remains appropriate. The previously pinned derivation remains
unchanged, and no claim for every possible source regulator has been added.
