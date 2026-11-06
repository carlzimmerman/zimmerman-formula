# PF14 — native equations constrain the ambiguity; full evolution remains open

**The derivative-forcing loop is not an independently selectable native source
in the bounded compactness class. It does not establish a need for new physics.**
Full weak existence and uniqueness from the incoming packet are nevertheless
not proved. The results below distinguish these two questions.

## The original source has a unique conditional limit

[Native compactness](NATIVE_COMPACTNESS.md) and
[independent audit](review/COMPACTNESS_AUDIT.md) use

    A_t Pi_x-A_x Pi_t = partial_t(A Pi_x)-partial_x(A Pi_t).

Uniform Lipschitz bounds and uniform convergence of A,Pi fix this Jacobian's
limit, despite merely weak convergence of their derivatives. It cannot retain
an arbitrary delta source. With strong clock-gradient compactness, uniform
spacetime BV control, and strong C1 metric convergence with the limit retaining the declared
second-derivative regularity, all native
weak equations pass to the limit. The full switch also passes under the bounded
multiplier hypothesis: strong Q and weak multiplier convergence preserve KKT.

This is conditional sequential closure, not a construction of a postbreak
sequence. It removes one purported freedom; it does not show two different
histories must coincide. PF13's one-time differentiated-forcing test remains
valid but cannot be promoted into native source nonuniqueness.

## Auxiliary uniqueness is distinct from evolution uniqueness

[Auxiliary reconstruction audit](review/AUXILIARY_UNIQUENESS_AUDIT.md) proves
at most one admissible periodic auxiliary pair for a prescribed clock profile
and geometry, including the full-switch obstacle. Strict convexity and the
complementarity sign give the result. This is not a theorem that a global
regular auxiliary solution exists for arbitrary large data, and the prescribed
clock and geometry are not determined by that spatial uniqueness argument.

[Local existence and stability](review/AUXILIARY_RECONSTRUCTION.md) also hold
on branch near homogeneous data, even for merely measurable prescribed clock
and area profiles. In a common compact class the auxiliary values satisfy

    ||delta A||infinity+||delta Pi||infinity
      <=C(||delta r||L1+||delta area||L1+|delta length|).

No derivatives of the prescribed profiles enter this estimate. If their time
variation is L1-Lipschitz, auxiliary spacetime Lipschitz regularity follows.
That time regularity has not been proved after breakdown. The theorem therefore
resolves spatial reconstruction, not the coupled temporal source problem.

## Small BV jumps are excluded without smooth interface traces

[BV jump exclusion](BV_JUMP_EXCLUSION.md) and
[independent audit](review/BV_JUMP_AUDIT.md) strengthen the prior regular-corner
result. In the on-branch bounded weak class, near a fixed D0=0 background with
0<gamma r0²<=1/10, the clock gradient cannot have a nonzero BV jump part.
The neighborhood includes auxiliary and metric coefficients as well as the
acoustic state. Smooth interface curves and auxiliary derivative traces are
not needed.

The Jacobian source is bounded, so scalar-base, compatibility and full stress
Rankine–Hugoniot conditions hold at approximate jumps. Small nonzero jumps must
have timelike acoustic speed. Exact normal constitutive convexity makes those
flux conditions incompatible. Weak Bianchi is justified in the stated
C1/W2,1 metric class, rather than assumed for arbitrary singular metrics.
[Approximate-jump source check](BV_SOURCE_CHECK.md).

## What is still missing

A BV field without jumps may retain continuous non-Lipschitz behavior or a
Cantor derivative part. The no-jump result does not exclude these possibilities
or prove they arise. We have not proved a native construction from the terminal
data, uniform compactness for such a construction, or a uniqueness estimate for
two full coupled histories. Concentration limits outside the stated bounds also
remain open.

Thus the forcing-path ambiguity itself is constrained by the original equations
and auxiliary reconstruction. It is not evidence that an extension is forced.
The previously proved strong breakdown and excluded shock/sheet repairs remain;
the universal survival-versus-extension question still requires a full weak
existence/nonexistence and selection theorem.

R1 is resolved conditionally on the explicit compactness class. R2 rules out
small BV jumps in the declared neighborhood. R3 remains open: prove existence
and uniqueness or nonexistence of the remaining no-jump weak evolution. A
promising precise next obligation is to control continuous/Cantor clock
variation in the coupled equations, rather than assign a free loop impulse.
These wider proof obligations are deferred, not claimed exhausted.

Research base 857b7495d1. Analytic proofs and independent reviews are recorded;
no new evolution simulation or physical regularizer was introduced. This is a
partial research checkpoint, not universal scientific closure.
