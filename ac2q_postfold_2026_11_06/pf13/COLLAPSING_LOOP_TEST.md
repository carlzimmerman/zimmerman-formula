# A collapsing-loop test for the proposed lower-order inverse map

This tests the naive proposal to treat the differentiated auxiliary inverse as
an L1-Lipschitz source on arbitrary small-BV lower-field profiles. It is not a
pair of native spacetime solutions and not a proof of AC2q nonuniqueness.

The exact prebreak inverse has its first row

    e u=a_coeff u+b_coeff v_aux+f K+f0,
    f=(W_P/r²)(1+c²),    K=e theta+omega(e).

On a regular compact chart, coefficients and the connection are bounded. A
smooth lower-field path in a shrinking proper interval can make r and theta
execute a small closed loop. Keep A,P at their common local values up to O(width),
as their bounded spatial constraints require. Their two spatial ODEs can be
integrated locally along the chosen profile. In the limit, integrating the
first inverse row across the loop gives the contribution

    Delta u = integral_loop f(r;A0,P0) d theta.

Bounded zeroth-order terms integrate to zero with the width, provided the usual
uniform L1-to-Linfinity inverse bound and bounded path variation are retained.
The O(width) change in A,P gives a vanishing error against the bounded variation
of theta. The identity therefore probes the principal derivative forcing.

Take a rectangular loop: change r from r1 to r2, increase theta by delta_theta,
return r to r1, and decrease theta. Its contribution is exactly

    delta_theta [f(r2)-f(r1)].

Smooth corners approximate this value. The loop can have arbitrarily small
fixed total variation and stay in the compact domain. Shrinking its support
makes its lower-field L1 distance from the constant endpoint profile tend to
zero, without removing this derivative-forcing impulse.

The one-form f dtheta is not generally exact. For a concrete local check set
r0=1, gamma=1/10, A0=11/10 (so D0=0), and W_P(P0) nonzero. Differentiation at
fixed A,P gives

    R0=91/10,    c0²=10/91,
    partial_r c²=7911/8281,
    partial_r f=-(10471/8281) W_P(P0) != 0.

Thus sufficiently small loops around this state have a nonzero impulse. The
case P0=0 makes this particular first-row test vanish; it does not turn the
one-form into an identity on a neighborhood containing nonzero P.

## What the test establishes and what it does not

Smooth profiles with the same strong L1 lower-field limit and bounded small
variation need not give the same limit for this differentiated inverse forcing.
The ordinary coefficient bounds and coercive inverse estimate do not by
themselves establish the source-difference estimate required by a BV semigroup
theorem. A reformulation could move such terms into a conservative principal
flux, or a stronger native compactness condition could constrain the paths.
Neither option is ruled out by this test.

This is a local operator/compactness counterexample, not a completed periodic
ADM data construction or an actual time-dependent native evolution. No claim
is made that either loop is dynamically produced from the fixed incoming packet,
that every full coupled source combination inherits this impulse, or that an
alternative correctly chosen conservative state cannot avoid it. The test
identifies why promoting the already differentiated inverse to a lower-order
L1-Lipschitz source is not justified on the unrestricted BV profile space.
