# Independent review of the coupled ADM solver

Scope: read-only review of `evolve_adm_v2.py` and `adm_initial_v2.py`,
followed by the separately contracted diagnostic in `review_linear/`.
No implementation edits were made by this reviewer. This is not a claim
of nonlinear convergence, global regularity, or a physical shock.

## Canonical audit

Write v=exp(lambda+2 beta), M=Mpl^2 and
F=-D+X-V-W-gamma D^2/2-2 gamma D X. Before imposing the spatial gauge,
the gravitational momenta are

    p_lambda = -2 M v Ky
    p_beta   = -2 M v (Kx+Ky).

The gravitational kinetic Hamiltonian density is

    Hk=(p_lambda^2-2 p_lambda p_beta)/(4 M v).

Integrating the spatial curvature action by parts on the periodic domain
gives the Lagrangian density

    Lsp=M exp(-lambda+2 beta)(2 N_x beta_x+N beta_x^2).

The shift imposes p_lambda,x=p_lambda lambda_x+p_beta beta_x.
The lapse equation is

    Hk/v + M exp(-2 lambda)(2 beta_xx+3 beta_x^2-2 lambda_x beta_x)
      = -D-X-V-W-gamma D^2/2+2 gamma D X.

At uniform lambda this is exactly the code's h and algebraic X solve.
With T=1+gamma(D+2X), variation of proper polarization P gives

    exp(-lambda) (N T)_x - N W'(P)=0.

The derivative of X with respect to P is

    X_P=[(-1-gamma D+2 gamma X) D_P-W'(P)]/(1-2 gamma D),

which agrees with the analytic Newton Jacobian. Proper P is held fixed in
the metric variations. The resulting evolution equations in uniform lambda
are

    beta_t = -N p_lambda/(2 M v)+w beta_x
    p_lambda,t = N Hk+N v(F-F_D D)-Lsp+(w p_lambda)_x
    p_beta,t = 2 N Hk+2 N v F+2 Lsp
      -[2 M exp(-lambda+2 beta)(N_x+N beta_x)
         +2 N exp(2 beta) P F_D]_x+(w p_beta)_x.

These match the implementation, including signs and factors. The gauge
requires w_x=mean(rate)-rate, rate=N(p_lambda-p_beta)/(2 M v).
The code stores w_s=k w, so its theta derivatives are consistent.

## Cancellation-free homogeneous linearization

For the M=1 constant-V fixture set lambda=beta=B, v=exp(3B), N=v,
H=Bdot. The background equations are

    H^2=v^2(X+V)/3, Hdot=V v^2, X=s^2/(2v^2).

For a nonzero coordinate Fourier wavenumber k_mode define Q^2=k_mode^2
exp(-2B), c=1-2 gamma X, and relative lapse perturbation n=delta N/N.
Let b=delta beta. The linear momentum constraint gives
delta p_lambda=-4 H b. The linear polarization equation gives

    delta D=-Q^2 c n/(K+gamma Q^2).

The Hamiltonian constraint then gives n=A delta h, where

    A=(K+gamma Q^2)/[2 X(K+gamma Q^2)+c^2 Q^2],
    delta h=(H/v^2)delta p_beta+(8H^2/v^2-2Q^2)b.

The native canonical equations reduce on this constraint surface to

    bdot=H n,
    delta p_beta,dot=(-8H^2+2v^2 Q^2)n+(-8Vv^2+2v^2 Q^2)b.

Set U=A H/v^2 and Z=A(8H^2/v^2-2Q^2), so n=U delta p_beta+Zb.
Differentiating this expression and using the background equations cancels
the large Q^2 terms in the n coefficient. The b coefficient becomes

    2 A H Q^2(Hdot/H^2-3)=-A s^2 Q^2/H.

Thus the independently usable two-variable system is

    bdot=H n
    ndot=(Adot/A+Hdot/H-6H)n-(A s^2 Q^2/H)b.

Reconstruct the canonical momentum through

    delta p_beta=v^2 n/(A H)-(8H-2v^2 Q^2/H)b.

The principal frequency squared is A s^2 Q^2>0 in this homogeneous
fixture. The native variables contain Q^4 entries and strong cancellations.
Freezing their coefficients and interpreting instantaneous eigenvalues
without accounting for the time-dependent constraint transformation can
give a false instability diagnosis. This derivation does not establish
stability of the finite-amplitude inhomogeneous evolution.

## Executed benchmark

`review_linear/CONTRACT.md` was written before execution; `COMMAND.txt`,
`run.py`, and `result.json` preserve the command, executable test, and raw
numerical output. Odd n=31, k=128, Fourier mode 4, b(0)=1e-12, n(0)=0,
t_final=.01. Native RK4 was compared against DOP853 on the reduced system.

At dt=.000625 the projected beta perturbation is 9.8692079283e-13,
against reference 9.8692045870e-13. Maximum beta field error divided by
initial amplitude is 2.51e-5; momentum residual is 1.02e-13. At half dt,
these are 3.25e-5 and 1.19e-13. The reduced system predicts lapse amplitude
-3.6843988729e-11 and p_beta amplitude 7.3227084462e-6; native results
agree closely (full precision in JSON).

This confirms local linear consistency and the derived cancellation-free
equations. It does not demonstrate temporal convergence: this tiny-amplitude
test is dominated by floating-point subtraction and native constraint
tolerance. It does not reproduce or explain the later finite-amplitude
breakdown. The diagnostic suppresses RuntimeWarning messages from NumPy
matrix products (also observed on finite small arrays in this environment);
exceptions remain recorded as failures, and all reported outputs are finite.

## Actionable numerical findings

1. On even grids the real first-derivative matrix annihilates the alternating
   Nyquist vector, and Dxx=Dx@Dx also annihilates it. `inverse_theta` silently
   drops this mode. Therefore the uniform-lambda gauge equation is not
   satisfied if rate develops a Nyquist component. Track
   max|mean(rate)-rate-Dtheta(w_s)|. It is about 4e-17 initially at n=32
   and 1e-16 at n=64. Odd-grid failures reported by the implementer exclude
   this as the sole cause of the observed breakdown. Changing Dxx alone
   would not fix the shift solvability issue.
2. The momentum constraint is diagnosed but has no failure threshold or
   stopping condition, despite the contract's constraint-failure rule.
   A separately declared momentum-reconstruction experiment can discriminate
   constraint-violating growth from dynamics on the constraint surface;
   it is not by itself proof of continuum convergence.
3. The algebraic lapse denominator 1-2 gamma D has no explicit singular-
   branch guard. Monitor its margin and prevent discrete branch crossing.
   No evidence here identifies this as the cause of present failure.
4. The spectral-tail stop means underresolution. Its message should not
   describe it as a "resolved pre-break stop."
5. The inhomogeneous collocation scheme does not preserve continuum product
   rules exactly. Aliasing can source momentum drift; this review has not
   isolated it as the primary cause. The reduced benchmark provides a
   concrete control before more expensive nonlinear diagnostics.

Recommendation: retain the failed runs, use explicit gauge and momentum
residual stop criteria, and compare constraint-reconstructed diagnostics and
the reduced linear control under matched refinement. None of the evidence
supports interpreting grid-sensitive termination as a physical shock.
