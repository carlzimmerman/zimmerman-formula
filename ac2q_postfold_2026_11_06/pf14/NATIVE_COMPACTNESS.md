# Conditional sequential closure of the bounded on-branch weak equations

Consider PF13 weak solutions on a common spacetime domain. Restrict to a compact
strict on-branch domain Q=Ar>1, so mu=0. Assume uniform Lipschitz bounds for
phi,A,Pi, uniform nondegenerate compact metric bounds with strong C1 metric
convergence, and strong local L1 convergence of dphi. To conclude membership in PF13's
metric class, also assume the limiting metric is C1 with locally integrable
second weak derivatives. Strong C1 convergence alone does not guarantee that
last property; distributional Einstein convergence itself uses only C1. Assume a uniform local spacetime BV bound on dphi to keep the limit in the
declared BV class. Together with its L-infinity bound this supplies local
strong L1 compactness for a subsequence. This is an estimate to be proved
for a construction, not an assertion that such postbreak solutions exist.

After a subsequence the Lipschitz auxiliary fields converge locally uniformly,
and their derivatives converge weak-* in L-infinity to the derivatives of their
limits. Uniform compact clock bounds give strong L1 convergence of r and n;
continuity of all constitutive functions gives strong L1 convergence of H,h,
and the total Hilbert stress. Strict on-branch margins pass almost everywhere.

## The apparent derivative source has a fixed limit

For Lipschitz A,Pi, in distributions,

    F_top=A_t Pi_x-A_x Pi_t
         =partial_t(A Pi_x)-partial_x(A Pi_t).

The products on the right converge distributionally: A converges uniformly
and dPi weak-*, with uniform derivative bounds. Thus

    F_top,k -> F_top in distributions.

In fact the Jacobians are uniformly bounded functions, so no surface delta can
remain in this source. Their limit is the Jacobian of the limiting fields, not
a path-dependent independent measure. No strong convergence of dA or dPi is
needed for this statement. The topological current itself also converges as a
bounded distribution, because it is A times a derivative of Pi.

The two auxiliary equations pass by the same strong-times-weak argument:
dphi is strongly L1 and uniformly bounded, whereas dA,dPi are bounded weak-*.
The scalar base current E h n converges strongly L1 and the explicit bounded
sources converge strongly. Therefore the scalar divergence equation passes.
The algebraic stress converges strongly; strong C1 metric convergence makes
quadratic connection terms converge, while curvature derivatives pass
distributionally. Consequently all Einstein equations pass as well.

This proves conditional sequential closure of the full on-branch bounded weak
system. It does not supply a family on the other side of breakdown, nor the
uniform estimates or uniqueness of its possible limits.

## Relation to PF13's loop

PF13 showed noncontinuity of the *differentiated inverse forcing* on arbitrary
one-time lower-field BV profiles. That remains true. It is not a freedom to add
an arbitrary source to a convergent bounded native spacetime solution. The
original Jacobian identity fixes the source in the compactness class above.
Different candidate histories would have to solve the actual equations and
produce different fields; assigning an impulse to the expanded inverse is not
a construction of them.

Removing the auxiliary Lipschitz bounds, strong clock-gradient convergence,
strict branch margin, or metric compactness requires another closure theorem.
Weak convergence alone does not justify passing nonlinear obstacle relations;
the following extension uses strong convergence of Q, not merely weak D.

## Full-switch extension with a bounded multiplier

Retain the same strong clock-gradient and auxiliary/metric compactness, drop the
strict on-branch condition, and impose uniform L-infinity bounds for mu_k>=0.
Take mu_k weak-* to mu. Then Q_k=A_k r_k converges strongly L1, is uniformly
bounded, and Q>=1. Strong-times-weak passage gives

    mu_k(Q_k-1) -> mu(Q-1)=0.

Thus the KKT relation is preserved. The auxiliary equation passes with
D_k=(Q_k-1)/gamma-r_k²-mu_k weak-*. The scalar base current and stress contain
mu only linearly times strongly convergent bounded coefficients, so these
terms pass weak-* too. The remaining terms converge strongly as above. All
full-switch weak equations therefore pass distributionally, provided the limit
metric retains the stated curvature class. This argument does not need to
apply max to a merely weakly convergent D. It supplies no multiplier bound for
an unbounded layer and no existence theorem.
