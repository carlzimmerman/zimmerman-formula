# Independent audit: auxiliary uniqueness for prescribed clock data

**Verdict: strict convexity gives at most one admissible periodic
auxiliary pair for fixed positive r and fixed geometry. It does not give
global regular existence or uniqueness of the spacetime evolution.**

On one fixed clock slice use proper length d ell and e=d/d ell. Prescribe
r>0 and beta, with positive bounded weights a=exp(2 beta). The period
and spatial metric are fixed; uniform-arclength coordinates simply give
d ell=ell dx. W is the fixed-clock strictly convex hold potential, and
W* its Legendre transform. The exact on-branch constraints are

    eA=W_P(P)/r,
    eP+2P e beta=rA/gamma-1/gamma-r^2.

They are the Euler equations of

    I[A]=integral a [W*(r eA)/r+r A^2/(2 gamma)
                    -(1/gamma+r^2)A] d ell,

with P=(W*)'(r eA). Variation yields
-a^-1 e(aP)+rA/gamma-1/gamma-r^2=0, with the stated signs.

The kinetic term is convex in eA. The positive r A^2/(2 gamma) term
makes the functional strictly convex in A, including its constant mode.
A direct uniqueness proof avoids any assumption about existence:
subtract two periodic solutions and test with Delta A to obtain

    integral (a/r)(W_P(P1)-W_P(P2))(P1-P2) d ell
      +integral (a r/gamma)(A1-A2)^2 d ell=0.

Both integrands are nonnegative. Therefore A1=A2, and the first spatial
constraint and strict monotonicity give P1=P2. This proves uniqueness
throughout the admissible class, not just the small initial IFT ball,
provided the weak derivatives and test pairing are integrable as above.
The result fixes r, beta and the spatial metric; it does not fix them
from the auxiliary equations.

The full-switch obstacle A>=1/r is also convex for prescribed r. The
same functional with this obstacle has multiplier mu in
-a^-1 e(aP)+D_eff-mu=0. Complementarity gives the required sign in the
difference test, so at most one admissible obstacle solution exists as
well. This is a uniqueness statement conditional on membership in the
specified regular class, not a theorem of obstacle regularity.

Existence in a globally Lipschitz, strict-on-branch, cap-separated class
does not follow just from strict convexity. The native W* has linear
growth at large conjugate argument when P has a finite cap; global
minimization may naturally involve relaxed BV profiles rather than the
desired bounded-gradient class. An unconstrained minimizer also need
not satisfy the strict branch margin for arbitrary prescribed r.
Compact coefficient restrictions yield stronger local coercivity but
must be established for the proposed solution. None of these spatial
uniqueness facts supplies temporal source estimates, constraint
propagation across singularities or uniqueness of the coupled weak PDE.

Independent delegated audit of the proposed functional route, 2026-11-06.

For clarity the full-switch difference test is exactly

    0=integral a[(Delta W_P)(Delta P)/r
                +(r/gamma)(Delta A)^2-(Delta A)(Delta mu)] d ell.

For the common obstacle A>=1/r, complementarity gives
(Delta A)(Delta mu)<=0 pointwise. All terms are nonnegative, hence
A and P coincide. Their second spatial equation then also gives
mu1=mu2 a.e. This establishes uniqueness of the entire auxiliary
triple, conditional on existence in the testable periodic regular class.
