# Exact six-photon-mass annihilator

This companion is algebraic and was written after the frozen filter run.
No computation in this worker's manifest executes a six-mass data stencil.

Let `s_j=4^j s0`, i.e. `lambda_j=2^j lambda0`, for j=0,...,5. Define weights

    (w0,w1,w2,w3,w4,w5)=(-1024,1984,-1240,310,-31,1).

They are the coefficients of

    Q(E)=(E-1)(E-2)(E-4)(E-8)(E-16).

The sum `sum_j w_j f(s_j)` annihilates every linear combination of
`1,s^(1/2),s,s^(3/2),s^2`. On `c_log s^2 log(s)` it gives exactly

    c_log s0^2 log(4) 16 Q'(16)
      =c_log s0^2 log(4) 322560.

Thus the no-fit estimator is

    c_hat(s0)=sum_j w_j f(4^j s0)/(322560 log(4) s0^2),
    C_hat_NB=-d/(128pi^2 M^4)-c_hat/2.

If the canonical full response has the expansion specified in DERIVATION.md,
the limit as s0->0 returns its logarithmic coefficient. Analytic higher terms
and higher half-integer terms cause a finite-s0 remainder; it is not an exact
finite-grid physical extraction. The six masses span a factor 32, and their
signed weights amplify noise. A covariance matrix/shared samples are needed
for a reliable uncertainty calculation. Very small lambda also demands much
larger volume; fixed finite-volume zero-mode artifacts cannot be ignored.

This removes neither the matching obligations nor f(0). It is a concrete
data-admission design, not a new measured coefficient or an alpha solution.
