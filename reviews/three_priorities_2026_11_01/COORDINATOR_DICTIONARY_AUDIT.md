# TP01 independent reconstruction of the dictionary

Scope: the positive, aligned, isolated spherical algebra and the declared
scalar external-field approximation. This is a coordinator reconstruction
from the two raw equations, not independent physical validation or a new
formal certificate. The full nonspherical field equation is not replaced
by this scalar approximation.

Write x=g/a0 and y=gN/a0, with a0>0 and x,y>0.

## S: simple mu

The action kernel mu(x)=x/(1+x) gives

    y=x²/(1+x),
    x=(y+sqrt(y²+4y))/2.

Consequently x-y=x/(1+x) is strictly between zero and one. Its Newtonian
excess tends to one, not one half. The logarithmic slope is

    n_S=d ln x/d ln y=(1+x)/(2+x),
    d n_S/d ln y=x(1+x)/(2+x)³.

Differentiating the last expression with respect to x gives a numerator
2+2x-x². Thus its unique positive maximum occurs at x=1+sqrt(3),
which corresponds exactly to y=2.

For a nonnegative scalar external field e and source b, the scalar model
x mu(x+e)=b gives

    x²+(e-b)x-b(1+e)=0.

For b>0 its two roots have negative product, hence exactly one positive
root; for b=0 the nonnegative root is x=0. This quadratic is not the B
model's cubic.

## B: squared excess

The separate equation x²=y²+y gives

    x=sqrt(y²+y),
    mu_B(x)=2x/(1+sqrt(1+4x²)),
    n_B=(2y+1)/(2(y+1)),
    d n_B/d ln y=y/(2(y+1)²).

The curvature maximum occurs at y=1. Rationalizing x-y gives
y/(sqrt(y²+y)+y), which lies below 1/2 and tends to 1/2 as y grows.
For positive x and x+e, squaring the B scalar external-field equation
gives (x²-b²)(x+e)=b x; endpoint equivalences must be checked separately
instead of dividing by x or x+e at zero.

## Separation and certificate scope

The exact point x=1,y=1/2 satisfies S and violates B, since
1 differs from 3/4. Both equations have the same leading deep-MOND
relation x~sqrt(y), so deep-limit agreement does not select between them.
Theorems assuming affine squared excess certify B. They do not certify
S curvature, Newtonian excess, or the S external-field equation.

Audit outcome: the S/B equivalence is refuted; the separate positive-domain
identities above follow by direct algebra. A corrected summary can keep
all existing numerical S fits while marking B certificates as separate.
