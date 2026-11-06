# Independent audit: absence of small BV clock-gradient jumps

**Verdict: proved in the declared compact on-branch neighborhood and
regular metric class.** The neighborhood must include the common frozen
coefficient A near its background value, as well as the acoustic state.
It excludes the jump part, not the Cantor part or all nonsmooth evolution.

Reviewed `pf14/BV_JUMP_EXCLUSION.md`, SHA256
`250fd7cb35b4a5abf6e934ef27846e857176d1834e2ad284d616df0e4a50e375`.
Independent delegated audit, 2026-11-06.

## Bounded forcing and weak Bianchi

On the compact on branch, dphi in BV and continuous Lipschitz A,Pi
make K=E h n and the algebraic stress T locally BV. The native scalar
equation gives div K in L-infinity, because its Jacobian source is a
product of bounded first derivatives. Compatibility gives curl(dphi)=0.

For g in C1 intersect W2,1 locally, smooth local approximations converge
in C1 and W2,1, preserving nondegeneracy on compact subsets. Their
connections converge uniformly and their Einstein tensors converge in
L1. In the smooth contracted Bianchi identity every connection-times-
Einstein term therefore converges in L1, while the divergence converges
distributionally. Hence the limiting Einstein tensor satisfies weak
Bianchi. Imposing all Einstein equations gives covariant div T=0.
The connection terms are bounded here, so the coordinate stress
divergence has no singular part. No arbitrary product of a discontinuous
connection with a surface stress has been introduced.

## Approximate jump identities

At H1-almost every point of the spacetime BV jump set of dphi, the jump
parts of these distributional identities give RH for K, compatibility
and T. The continuous A,P and metric freeze to common values in the
two half-space traces. This uses BV jump measures, not smoothness of a
jump curve and not normal/tangential derivative traces of Pi.

With U=(m,b), m=exp(2 beta)h phi_t/r and b=phi_x, the frozen-coefficient
flux is F=(K^x,-phi_t). The positive-R compact Legendre inversion makes
the change of state locally injective. A jump with spatial normal zero
would force [U]=0 and hence no clock-gradient jump. Otherwise normalize
the normal to (-V,1); then [F]=V[U].

For a nonzero small jump, [U] is an eigenvector of the averaged Jacobian
integral_0^1 DF(U_-+z[U]) dz. In a sufficiently small neighborhood of
the fixed low-u background (including A), this real two-by-two matrix
has separated real eigenvalues near the two simple acoustic speeds.
Thus V is nonzero and subluminal. A local orthonormal normalization
handles the common metric factors. Both clock velocities in its rest
frame have the same nonzero sign, and the common proper tangential
clock slope s satisfies gamma s^2<1/3, with the strict PF12 margin.
The neighborhood may depend on the fixed positive u0<=1/10.

## Direct stress obstruction without Pi derivative traces

In that rest frame let w be the clock-flow velocity, B=sA, and
r=s sqrt(1-w^2). Define f(w)=H(r(w),A=B/s), retaining or omitting the
common potential constants consistently. Direct differentiation gives

    f'=-s h n_N,    T_NN=f-w f'.

The normal K flux condition is continuity of h n_N, because E has the
same frozen value. Stress RH includes continuity of T_NN. Thus the two
endpoints obey equal f' and equal w f'-f. No original-current trace of
Pi is needed: its divergence has already become a bounded Jacobian in
the equation for K.

The exact PF12 third derivative makes f' strictly convex on positive
w (strictly concave on negative w) when gamma s^2<1/3 and B>0. Distinct
same-sign endpoints cannot satisfy both equalities. Consequently their
w values coincide. Common s fixes r; the frozen frame then fixes the
clock gradient itself. This contradicts a nonzero approximate jump.
The clock-gradient BV jump part therefore vanishes.

## Limits

This does strengthen the regular-corner exclusion to rectifiable BV
jump sets in the stated weak class. It neither assumes nor proves that
the terminal packet must develop a jump in every weak continuation.
Continuous non-Lipschitz fields and Cantor derivative parts are not
excluded by this argument. No entropy uniqueness theorem, postbreak
existence construction, or universal singular exclusion follows.

Revised-file follow-up: read the complete final file, SHA256
`6134a4d96ae072081448cd0e34167e5beaf5fe5c7b0364e6d1e0936876653132`.
It explicitly includes the common auxiliary/metric coefficients,
particularly A, in the small neighborhood and includes the direct
f=H normal-current/stress identities. Verdict for that revision: proved
as written in the stated C1 intersect W2,1 metric and compact BV class.
