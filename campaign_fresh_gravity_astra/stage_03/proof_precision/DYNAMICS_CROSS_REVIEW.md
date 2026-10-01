# Independent cross-review of DP1 signs and characteristic speeds

Review date: 2026-09-27. This is a bounded cross-lane review requested by the
parent after the AFG-001–008 audit. Reviewed only raw
`stage_03/dynamics_precision/DERIVATION.md`, SHA256
`41ad39d1521e7d5b5d974e320478faecd944df8d4608b4869a566624244af3ae`.
The file was live when first reviewed; the parent subsequently reported the
dynamics lane finalized it with this same hash, and a final local hash check
agreed. The verdict applies to these exact bytes, not to later edits. The
reviewed text is preserved as `DP1_reviewed_snapshot.md`.
No dynamics code, numerical results or verdict-summary document was used.

**Primary verdict: proved as written**, for the following narrowly scoped
identities and principal-symbol claims under the author's smoothness,
constant-a/K, uniform-background and boundary-flux assumptions. This does not
audit the bounded-domain existence theorem, empirical viability, numerical
wave simulation, or any global nonlinear evolution claim.

## Energy and momentum signs

Write C=4 pi G, f_i=mu partial_i phi, and
K phi_tt/c²−partial_i f_i=−C rho. Direct differentiation gives

    partial_t e_f + div S_f
      = phi_t [K phi_tt/c²−div f]/C = −rho phi_t,

with e_f=[K phi_t²/(2c²)+W]/C and S_f=−phi_t f/C, as stated.
Continuity implies

    partial_t(rho phi)+div(rho v phi)
      = rho phi_t+rho v dot grad phi.

Combining with the matter kinetic work term −rho v dot grad phi cancels all
interaction sources. Matter with additional pressure/internal energy requires
its corresponding matter energy and stress fluxes; the specified purely
kinetic matter model uses the displayed work law.

For the proposed p_i=−K phi_t phi_i/(C c²), differentiate the stress
T_ji=[mu phi_j phi_i+delta_ji(K phi_t²/(2c²)−W)]/C. The terms proportional
to phi_t phi_it cancel, and W_i=mu phi_j phi_ji cancels the gradient-product
term. The remainder is

    partial_t p_i + partial_j T_ji
      = [div f−K phi_tt/c²] phi_i/C = +rho phi_i.

Thus it exactly cancels the matter force density. The minus sign in the field
momentum and plus sign in its source are both correct with the author's
acceleration=−grad phi convention.

When a=a(t), differentiating W adds W_a a_dot/C to the energy balance;
there is no extra time-derivative constitutive term in the displayed field
equation because its time kinetic coefficient is constant. Implicit inversion
g=F(b(g,a),a) gives b_a=−F_a/F_B<0, hence W_a<0 at g>0. In the deep regime
W_a a_dot=−(a_dot/a)W. With a_dot/a=−3H Omega_m/2, the stated injection
+3H Omega_m W/(8 pi G) has the correct sign and factor.

## Hessian and characteristic speeds

For W'(g)=b(g), radial differentiation gives the two spatial Hessian
eigenvalues b/g and b'. Therefore a plane-wave perturbation about a constant
nonzero gradient obeys

    omega² = (c²/K)|k|²[mu sin²(theta)+b' cos²(theta)].

Both coefficients are positive for Q and R. The derived Q values are

    mu=sqrt(u/(u+1)), b'=2sqrt(u²+u)/(2u+1).

Consequently b'>mu, b'<1, and sup b'=1, so the sharp constant-K bound is
K>=1. The supremum need not be attained for the bound to be necessary.

For R let d=1−exp(−t), t=sqrt(B/a). Direct differentiation gives

    F_B=(d−t exp(−t)/2)/d²,
    mu=d, b'=d²/(d−t exp(−t)/2).

The denominator is positive because exp(t)>1+t/2. Further b'>mu and
F_B>1/2 is equivalent to 1−exp(−2t)>t exp(−t), or 2sinh(t)>t.
Thus b'<2 and K=2 suffices. b'>1 is equivalent to
t>2(1−exp(−t)), exactly as stated; K=1 indeed fails for some backgrounds.
Changing K from 2 to 8 halves a fixed-mode frequency and doubles its response
time while preserving every exactly static solution.

For P(X)=W(sqrt(X)), 2P'=b/g=mu on X>0. Expanding about a static uniform
gradient gives kinetic coefficient mu and the same spatial Hessian. Thus
c_perp²=c² and c_parallel²/c²=b'/mu. These ratios simplify to

    Q: 2(u+1)/(2u+1),
    R: [1−t/(2(exp(t)−1))]^(−1).

For finite u,t>0 both lie strictly between 1 and 2. The restricted scalar
principal cone therefore exceeds the chosen metric light cone along the
gradient. Hyperbolicity on these backgrounds survives; neither global
causality nor full relativistic gravity is decided by this calculation.

## Supplementary local sign checks

At the proposed vacuum point, b_N=a(1,2,0)/sqrt(5) and
grad B=a(1,4,0)/(sqrt(5)L), giving
(grad B cross b_N)_z=−2a²/(5L). Both nu derivatives are negative, so the
displayed positive Q/R curls have the correct sign and normalization.
Differentiating the explicit W_Q primitive returns
(sqrt(a²+4g²)−a)/2, as required.

All checked algebra closes. The unresolved dynamical input K and possible
timelike kinetic branch remain genuine freedom of the stated construction;
these signs and speeds do not establish observational viability or select a
physical completion.
