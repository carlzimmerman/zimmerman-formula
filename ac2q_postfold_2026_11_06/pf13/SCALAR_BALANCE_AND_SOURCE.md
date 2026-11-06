# Compact on-branch scalar balance and the source-map obligation

Restrict the bounded weak class to the native on branch (mu=0). Define
K^a=E h n^a. The scalar equation, using the exact distributional identity
for Lipschitz A,Pi, is

    div K = A_t Pi_x-A_x Pi_t-E(V_phi+W_phi).

Indeed J=K-A curl(Pi), and div(A curl(Pi))=A_t Pi_x-A_x Pi_t.
The mixed second derivatives cancel; products on the right are L-infinity.
Define the compatibility variables b=phi_x and a=phi_t. In conformal coordinates

    m=K^t=exp(2beta) h a/r,
    K^x=-exp(2beta) h b/r,
    b_t-a_x=0,
    m_t+partial_x K^x=F,
    F=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi).

On a compact subluminal hyperbolic neighborhood the Legendre derivative is

    partial m/partial a
      =exp(2beta-2alpha)/r^3 [R a² r-h b²]
      =exp(2beta) [R cosh(theta)²-(h/r)sinh(theta)²]>0.

The second equality uses a=r exp(alpha)cosh(theta),
b=-r exp(alpha)sinh(theta). Thus one can locally invert m for a with b,A,alpha,
beta fixed. This gives a two-component balance with flux (K^x,-a) for (m,b).
Its coefficients still contain unknown A and the metric; its source includes
unknown temporal auxiliary derivatives. It is not yet a closed autonomous
flux f(U) and a prescribed source map G(U).

## Exact theorem test

Colombo–Guerra, *Hyperbolic Balance Laws with a Non Local Source*,
arXiv:0704.2031v1, Theorem 1.2, supplies a local process for an autonomous
strictly hyperbolic C4 flux with genuinely nonlinear or linearly degenerate
fields, and a source map obeying an L1 Lipschitz estimate and a uniform
variation bound on a small-TV state domain. Its setting is the real line.

The retrieved PDF identifies itself as v1 dated 16 Apr 2007 in its arXiv header;
its internal title-page date is November 18, 2018. Both are recorded rather
than silently treating the rendered copy as a different verified version.
Primary source read:
https://arxiv.org/pdf/0704.2031
No full-text local cache or source hash is claimed.

Application to AC2q is NOT verified. There is no established closed source map
on the terminal BV state space here, no proof of its L1 Lipschitz property,
and no equivalence between its entropy process and all Einstein equations.
Treating A,Pi and the metric as arbitrary prescribed coefficients loses the
coupling. Enlarging the state requires dealing with constraints and repeated
advective speeds; it does not automatically meet strict hyperbolicity.
The periodic geometry is an additional adaptation, not the central obstruction.
The theorem cannot select an AC2q continuation simply because the prebreak
system had two acoustic characteristics and a coercive spatial inverse.

## Why a bounded source is not the required estimate

The prebreak bound for u=nA/r and v_aux=nP/r controls the size of F along one
solution. The theorem instead requires a uniform L1 bound for G(U)-G(V) in
terms of ||U-V||L1 over a common state domain. The prebreak estimates for the
expanded system depend on bounded promoted gradients; that domain is lost at
breakdown. No such postbreak source-difference estimate has been proved.

Thus the direct weak equations are now explicit. The missing implication is
closure and well-posedness of their coupled BV evolution, not an inability to
write their scalar divergence. A theorem for a selected scalar balance alone
would still have to pass the full native stress/junction compatibility tests.
