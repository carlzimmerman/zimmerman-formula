# Independent audit: collapsing-loop derivative forcing

**Verdict: proved as the stated local derivative-forcing/compactness
counterexample.** It is useful evidence against the naive unrestricted
BV inverse-as-source argument. It is not a counterexample to full native
evolution or to every possible closed conservative reformulation.

Reviewed `pf13/COLLAPSING_LOOP_TEST.md`, SHA256
`c75900b7c5b39b6a3e249687672fdb04c3f542e73864aa19c023cebdab6b28af`.
Independent delegated audit, 2026-11-06.

The reviewed smooth first inverse row has derivative forcing
f e(theta), where f=(W_P/r^2)(1+c^2); the remaining connection and
zeroth-order terms are bounded on the retained compact inverse domain.
If u,v_aux remain uniformly bounded by the L1-forcing inverse estimate,
integration over a proper interval of length epsilon gives

    u_right-u_left=integral f dtheta+o(1).

The local spatial constraints for A,P have bounded right sides, so their
variation across that interval is O(epsilon), even when r,theta vary
rapidly with bounded total variation. Their changes contribute o(1) to
the displayed integral. This argument requires precisely the retained
bounded inverse response; it does not assert such a response in an
arbitrary singular or noncoercive domain.

At fixed A,P, the exterior derivative of f dtheta is
f_r dr wedge dtheta. A rectangular path with r-levels r1,r2 and theta
increment delta_theta has integral

    delta_theta [f(r2)-f(r1)].

Shrinking its support in physical space leaves that path integral fixed
while the lower-field L1 perturbation tends to zero. The variation can
be fixed arbitrarily small, and rounded smooth paths retain a nonzero
integral. Hence this forcing has a nonzero distributional impulse whose
value is not specified by the strong L1 endpoint limit. The phenomenon
is stronger than merely observing that differentiation is unbounded in
L1: the impulse survives integration through the first-order inverse row.

Direct Python3/SymPy differentiation of the declared H at
r=1, gamma=1/10, A=11/10 gives exactly

    R=91/10,
    c^2=10/91,
    (c^2)_r=7911/8281,
    f_r/W_P=-10471/8281.

All constants and the fixed-A derivative convention pass. A nonzero
small P0 is allowed locally and makes W_P nonzero while preserving the
compact margins. The particular first-row witness vanishes at P0=0;
the actual file explicitly acknowledges this limitation.

The response statement is local and conditional on the retained inverse
bounds. It does not finish a periodic constraint construction. In
particular the constant local endpoint values of A,P need not themselves
be a global constant solution of their spatial equations when W_P!=0.
This does not affect the local path test; it prevents treating it as a
completed periodic-data or spacetime counterexample.

The result establishes failure of L1-continuity for this differentiated
forcing on the unrestricted small-BV profile class. To conclude failure
of an entire proposed source G would additionally require defining that
G, identifying its full response and ruling out cancellations or a
conservative change of variables. The candidate explicitly does not
make that stronger claim. The right consequence is that the previous
coefficient/coercivity bounds alone cannot verify the semigroup source
hypothesis; another closure/compactness argument is required.
