# Why source variation does not yet construct the native weak evolution

## A quantitative smoothing test

Take a compact interval or periodic slice in the continuous subclass. Let
X contain U=(m,b), A and the conformal metric coefficients appearing in the
PF13 flux, let eta_epsilon be a nonnegative standard mollifier, and write
X_epsilon=eta_epsilon*X. On a compact flux domain with bounded second
state derivatives, define

    R_epsilon=f(X_epsilon)-(f(X))*eta_epsilon.

For continuous BV X the chain rule gives

    partial_x R_epsilon(x)
      =integral eta_epsilon(x-y)
        [Df(X_epsilon(x))-Df(X(y))] D_x X(dy).

If omega is the modulus of continuity of X, then

    ||partial_x R_epsilon||L1
       <=C omega(2 epsilon) TV(X).                     (1)

This tends to zero. The same estimate integrated in time applies when a
common spatial continuity modulus and integrable slice TV are available.
Spacetime convolution on an interior compact cylinder yields the analogous
statement. Thus continuous BV native scalar fields can be approximated by
smooth fields with small L1 scalar-balance residuals. This is consistent with
the previous weak closure result, not a solution construction from initial data.

Trying to differentiate the residual to estimate TV requires another spatial
derivative. Standard mollifier estimates, with locally Lipschitz Df on the
compact domain and a sufficiently smooth flux for this displayed bound, give
only an upper bound of the scale

    ||partial_x^2 R_epsilon||L1
       <= C omega(C epsilon) TV(X)/epsilon.            (2)

For example ||partial_x X_epsilon||infinity is bounded by
C omega(C epsilon)/epsilon, while its L1 norm is bounded by TV(X).
Differentiating the integral in (1), using cancellation and these bounds,
gives (2). Merely continuous or Holder fields do not make this bound vanish.
This is failure of an available bound to close the argument, not proof that
the actual native residual necessarily diverges. In particular, (1) cannot
be silently used as the derivative-residual bound needed for a TV estimate.

A stability process in L1 would let small residuals serve a different purpose,
but existence and native consistency of that process are exactly unproved.
Smoothing an already existing weak solution is not a construction of one;
smoothing the constraints does not preserve them exactly at finite epsilon.

## Exact source check: autonomous uniqueness is insufficient

Bressan–De Lellis, *A Remark on the Uniqueness of Solutions to Hyperbolic
Conservation Laws*, arXiv:2305.17203v1 (header 26 May 2023; internal date
30 May 2023), Theorem 1.1, PDF page 3, concerns an autonomous strictly
hyperbolic conservation law with C2 flux. A solution continuous in L1, lying
in the established small-total-variation semigroup domain, and obeying Liu
admissibility at its approximate jumps must equal that semigroup trajectory.
For a continuous solution the jump condition is vacuous.

Primary source inspected:
https://arxiv.org/pdf/2305.17203
No local full-text cache or source hash is claimed.

This theorem does not directly apply to AC2q's flux with unknown metric and
auxiliary coefficients and its native derivative-dependent source. The new
source-variation estimate is a bound along one solution, not a closed source
map with an L1 difference bound. Nor has a native semigroup domain been
constructed. Thus this theorem identifies a possible structural route but
cannot supply the missing AC2q existence or uniqueness claim.

## Native difference estimate still needed

Subtracting the two balances gives

    partial_t delta U+partial_x delta f=(delta S,0),
    S=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi).

Instantaneous auxiliary reconstruction controls differences of A,Pi for
prescribed clock/geometry. It does not control differences of A_t,Pi_t by
||delta U||L1. The source-variation estimate in SOURCE_VARIATION.md bounds
individual rates and their spatial variation, not those temporal differences.
Likewise, bounding each source separately cannot imply an L1 contraction.

A native weak construction must produce uniform outgoing compactness/TV,
retain all Einstein constraints, and identify the nonlinear limit. A uniqueness
argument must then compare full coupled solutions. Neither follows from (1),
from the one-solution source estimate, or from absence of BV jumps. These are
separate unproved implications, not evidence that a physical extension is
already necessary.
