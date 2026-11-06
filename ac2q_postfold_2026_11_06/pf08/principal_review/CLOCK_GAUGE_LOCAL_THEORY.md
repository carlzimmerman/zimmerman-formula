# Clock-gauge local-theory audit: structural route, not yet a theorem

**Verdict: incomplete, with no principal derivative-loss obstruction found
in the proposed mixed formulation.** A tailored local-existence and
continuation proof remains necessary. The native hold-law regularity blocks
an automatic invocation of a smooth, equal-regularity high-Sobolev theorem;
it does not establish illposedness.

## 1. Exact clock-gauge system

Use

    ds^2=-r^(-2)d tau^2+L^2 dx^2+exp(2beta)(dy^2+dz^2),
    n=r partial_tau, e=L^(-1)partial_x,
    a=e(log r), K=div_2 n, B=n(beta), E_beta=e(beta).

The acceleration is -a, and [n,e]=-a n-Ke on the constraint surface.
With the notation and on-branch conditions of RIEMANN_SOURCES.md,

    n(r)=-r c^2 K+S,
    n(L)=LK, n(beta)=B,
    n(A)=r u, n(P)=r v,
    n(E_beta)=-a B-B E_beta,
    n(B)=-a E_beta+(-3B^2+E_beta^2-T_ee/M)/2.

The last sign follows from
G_ee=-2[n(B)+a E_beta]-3B^2+E_beta^2. The mixed Einstein equation uses
the native on-shell T_ne=0. Additional matter flux requires its explicit
terms and cannot be silently omitted.

The promoted gradient block is

    n(a)+c^2 e(K)=a(c^2-1)K-e(c^2)K+e(S)/r-2aS/r,
    n(K)+e(a)=a^2-K^2+R_base/2.

The spatial principal matrix is [[0,c^2],[1,0]], symmetrized, for example,
by diag(1,c^2). Positive lower/upper bounds for r,c,L supply the usual
strict principal margins. The base curvature is the algebraic expression
proved in RIEMANN_SOURCES.md.

## 2. Why the nonlocal source has the expected order

The spatial system for u,v has first-order coercive operator and forcing
algebraic in a,K and the bounded lower-order fields. On a controlled
periodic slice it is spatial order minus one. The exact identities for
e(u),e(v) then express these derivatives algebraically in the same fields
and a,K, with no derivative of a or K.

In particular e(S), after substituting e(r)=ra, e(A)=W_P/r,
e(P)=D-2P E_beta, e(B)=(K-B)E_beta and the u,v equations, contains no
e(a) or e(K). Thus it does not alter the displayed principal matrix.
This is stronger than an unproved claim that an arbitrary nonlocal term
is lower order. Its nonlinear mapping/regularity estimates still have to
be established in the actual solution space.

## 3. Constraints that must be propagated

The promoted system is not automatically the full native system unless
at least the following constraints remain zero:

    C_a=e(log r)-a,
    C_beta=e(beta)-E_beta,
    C_A=e(A)-W_P/r,
    C_P=e(P)-D+2P E_beta,
    C_mom=e(B)-(K-B)E_beta,
    C_H=e(E_beta)-KB-(B^2-3E_beta^2)/2+T_nn/(2M).

The algebraic switch/auxiliary relation and on-branch/clock/cap margins
also remain part of the domain. For example direct commutation gives
n(C_beta)=C_mom-B C_a-K C_beta, illustrating the coupled propagation problem.
The equations for u,v were designed by differentiating C_A,C_P, but a
proof must derive the full residual system, including off-constraint
terms, and show uniqueness of its zero solution. Full Einstein constraint
propagation requires the native matter equations and the Bianchi identity;
it cannot be inferred merely from the two promoted gradient equations.

The periodic inverse also depends on the actual slice and coefficients.
Uniform invertibility is supplied by the earlier coercivity margins, but
continuous/Lipschitz dependence in the chosen function spaces remains a
required local-theory estimate.

## 4. Native hold-law regularity

For constant a0 and Khold,

    W_P=Khold P/(1-Khold |P|/a0),
    W_PP=Khold/(1-Khold |P|/a0)^2.

W is C2 at P=0. W_PP is locally Lipschitz inside the cap but not C1
at zero. The expanded e(S) contains W_PP(P) factors without a universal
vanishing prefactor at every zero of P. For a generic transverse zero,
the cusp has local regularity like |x|, which is not H^s for s>=3/2.
Thus a naive claim that all expanded coefficients/sources are smooth
enough for an arbitrary equal-regularity H^s theory above the usual
one-dimensional classical threshold is unjustified.

This is an obstruction to that off-the-shelf proof strategy, not to the
native dynamics. Possible alternatives include a mixed regularity theory
(for example r with two spatial derivatives and promoted a,K with one),
an intrinsic frame-energy formulation, or a Lipschitz/characteristic
construction. Constraints may supply the extra derivative of r, and
the elliptic inverse may supply an extra derivative of u,v. The principal
speed depends smoothly on r,A, not directly on W_PP. These are useful
features but must be proved compatible with nonlinear estimates,
uniqueness, constraint propagation and continuation.

In clock coordinates, L may have less regularity than r. A proof should
not assume coordinate characteristic speeds are Lipschitz solely from
an H1 bound on every variable. Frame-energy estimates with the natural
L dx measure, or a controlled arclength coordinate, may handle this
without introducing an artificial derivative-loss claim. No such full
construction is supplied by the structural audit alone.

## 5. Outstanding theorem obligations

1. Select a precise finite-regularity classical/strong solution class
   consistent with the native hold law; prove local existence, uniqueness
   and continuous dependence for the hyperbolic–spatial-inverse system.
2. Prove the nonlinear inverse's estimates and parameter dependence in
   that class, with constants depending on the declared compact margins.
3. Derive and close propagation of all promoted/geometric/matter constraints.
4. Establish a continuation criterion sufficient for the conditional
   localized-packet argument, without assuming the very gradient bound
   that the Riccati calculation is intended to contradict.
5. Apply the result to the already audited local auxiliary/ADM packet
   family at its actual finite regularity. No C-infinity regularity at
   generic P zeros is claimed.

Until these obligations are discharged, RIEMANN_SOURCES.md remains a
conditional formation route. Failure to have proved this theorem is
not a demonstrated failure of predictivity or evidence of nonexistence.
Nothing here supplies singular admissibility or postbreak uniqueness.

Independent delegated analytic audit, 2026-11-06. No numerical experiment
or external local-existence theorem was treated as the missing proof.
