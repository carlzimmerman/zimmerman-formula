# AZ2 derivation and result

κ = ½ FITTED; not theory closed

**PASS: survives these operator gates only. Empirical rows NOT EVALUABLE on both footings.**

For A=I-div(D grad) with periodic or zero-flux boundary conditions, integrate Au=rho to obtain integral u=integral rho. The weak form is <v,Au>=integral vu+grad v.D.grad u. Positive symmetric D makes this symmetric and coercive. For a negative minimum of u with rho>=0, the elliptic maximum principle forbids Au>=0; the discrete version is an M-matrix. Constants are fixed. These arguments allow bounded positive tensor D, not just a scalar.

The numerical check is an orthogonal finite-volume implementation: B is a periodic edge gradient; A=I+B^T diag(D_face) B. The constant-coefficient Fourier eigenvalue is 1+4D sin²(pi/N)/h². results.json records mass error 3.33e-16, reciprocity error 2.78e-17, minimum density 0.6040 and known-answer error 1.55e-15. The nonconservative mutation I+diag(D_point) B^T B fails mass by 0.0357591 and reciprocity by 0.0103013. No a0 enters these identities, so the canonical and alt results coincide algebraically, not through pooling data.

**What the action does and does not give.** For prescribed D and source rho,
J[u]=integral (u²/2+grad u.D.grad u/2-rho*u)
has Au=rho as its Euler equation. This is an auxiliary elliptic energy, not a covariant gravitational action. If D=D(Phi), varying the gravity field adds (grad u).(delta D).(grad u)/2; omitting that term would change the theory. If D depends on Hessians, integration by parts produces further derivatives and stability needs a new calculation. If D=D(u), even the u equation changes. Nothing here establishes requirement 12/E1.

Unlike a Gaussian, this resolvent has Fourier transfer 1/(1+D k²), with a slower ultraviolet tail. KT25 or KT28 Cassini/SPARC labels cannot transfer. A heat semigroup exp(div D grad) is another conservative option, but replacing the resolvent with it would be another lane and does not fix the choice of D.

The candidate is useful as a reusable construction: a local differential operator can define a nonlocal smoothing solution while respecting mass and reciprocity. It is incomplete as gravity. The next calculation is the coupled variation with a regular tidal D, followed by the solar external-field solution; no empirical pass is inherited.
