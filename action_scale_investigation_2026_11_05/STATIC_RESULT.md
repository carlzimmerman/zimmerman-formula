# Exact radial equations for the single-clock density portal

Candidate equations, not a solved or stable physical system. See
SINGLE_CLOCK_RESULT.md for the action. Kappa remains FITTED.

Use a positive constant V and phi=q t, q>0, in a static region with
ds^2=-N(r)^2 dt^2+B(r)^2 dr^2+r^2 dOmega^2, N,B>0. Choose the positive
radial polarization branch P^r=p/(K B), 0<p<a0(N), with

    X=q^2/(2N^2), rho=X+V, a0^2=b rho,
    d=p'+2p/r, W=W(p,a0(N)), K=4pi G, M^2=1/(8pi G).

The scalar is shift-symmetric because V is constant. On this static ansatz
the diagonal metric has zero shift; the scalar has no radial gradient.
The reduced equations below are those of the static ansatz. A fully
covariant check of the off-diagonal and scalar equations is still needed
before an ansatz solution is promoted to a full solution.

After dropping a radial boundary term, the action per unit solid angle
and coordinate time is

    Lr = M^2 [N B+N/B+2r N'/B]
          + N B r^2 [X-V-W] + r^2 p N'/K
          - gamma N r^2 d^2/(2 K^2 B).

Independent variation gives:

    0 = M^2[B-1/B+2r B'/B^2]
          - B r^2[rho+W+N W_N] -(r^2 p)'/K
          - gamma r^2 d^2/(2K^2 B),

    0 = M^2[N-(N+2rN')/B^2]
          + N r^2[X-V-W] + gamma N r^2 d^2/(2K^2 B^2),

    0 = r^2 N'/K - N B r^2 W_p
          + gamma r^2/K^2 (N d/B)'.

The portal's lapse derivative is essential. For s=p/(a0-p),

    N W_N = b X/K [s+s/(1+s)-2log(1+s)] > 0.

The strict sign assumes q,p>0. Holding a0 fixed while varying N would omit
this term and would solve a different theory. The unscreened algebraic
polarization equation is A=K W_p=p/(1-p/a0), A=N'/(NB).

## GR benchmark scope clarification

The symbolic Schwarzschild-de Sitter check tests the two metric equations
after their polarization contributions and q are set to zero:
N^2=B^-2=1-2m/r-V r^2/(3M^2), on a static region where this is positive.
It is an Einstein-sector sign/normalization benchmark ONLY. At q=0 the
normalized scalar clock is undefined; it is a formal q->0 limit of these
metric equations. Moreover p=0 with N' nonzero does not satisfy the
polarization equation when P.A is retained. Thus this is NOT an exact
uncharged solution of the entire coupled candidate. STATIC_CONTRACT.md's
benchmark wording is restricted to this explicit interpretation; no
numerical threshold or algebraic equation has been changed.

## First-order form for a finite-shell existence diagnostic

At positive gamma, write n=N'/N. The four ODEs are

    n = [M^2(B^2-1)+B^2 r^2(X-V-W)
                          +gamma r^2 d^2/(2K^2)]/(2M^2 r),
    N' = N n,
    B' = B^2/(2M^2 r) [B r^2(rho+W+N W_N)+r^2 d/K
                       +gamma r^2 d^2/(2K^2 B)-M^2(B-1/B)],
    p' = d-2p/r,
    d' = K B^2/gamma * p/(1-p/a0) - K B/gamma*n
                         -(n-B'/B)*d.

A finite-shell boundary solve would test only those chosen boundaries;
it would not establish matching to an actual galaxy or cosmology. Next
obligations: verify the remaining covariant equations and perform a frozen
finite-shell solve before perturbing its charged background. Keep b free.

Evidence: static_branch.py exact Euler-Lagrange differentiation, explicit
Einstein boundary term, portal derivative and metric-sector GR benchmark.
The omitted-NW_N mutation must fail the lapse identity. Self-review only;
full covariance and physical background claims remain conditional.
