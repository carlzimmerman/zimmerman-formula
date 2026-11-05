# Exact derivation and self-audit

The full nonlinear theorem is not established here. The result concerns
an implication used in X3: bounded modal growth and c²>=0 do not alone
provide the norm estimate needed for nonlinear evolution.

## Frozen equations and their norms

At mu_K=0, linearizing the PN equations in a local patch gives

    delta rho = partial_x delta P,
    partial_x^2 delta Phi = K delta rho,
    partial_t delta rho = -rho0 partial_x delta v,
    partial_t delta v = K M delta P - partial_x delta Phi
                       - gamma Theta partial_x delta rho.

Here M is the longitudinal W Hessian and Theta is the branch stiffness.
For exp(ikx), elimination of P and Phi gives U_t=B(k)U, U=(delta rho,delta v),

    B = -i [[0, k rho0], [C/k + gamma Theta k, 0]],
    C=K(M-1),   B^2=-rho0(C+gamma Theta k^2) I.

This retains H4's Poisson feedback, not just its decoupled dispersion.
The background coefficients are frozen locally. A spatially constant
negative rho0 together with constant M is not asserted to be an exact
periodic full-v3s background. In particular periodic P cannot have a
nonzero mean divergence. This is a local-symbol test, not such a solution.

For the main soft branch, rho0=-1/2, C=1, Theta=0, let Omega=sqrt(1/2).
Then, at time t,

    exp(tB) = cosh(Omega t) I + sinh(Omega t) B/Omega.

Its upper-right entry is i k sinh(Omega t)/(2 Omega). Therefore its
Euclidean operator norm is at least the magnitude of this entry and
is asymptotic to that magnitude as k tends to infinity. At every fixed
t>0 it has no k-uniform bound on equal-order density/velocity Sobolev norms.
The principal matrix [[v0,rho0],[0,v0]] has only one eigenvector when
rho0 is nonzero. Its eigenvalues being real is not diagonalizability.

This is polynomial frequency amplification, not an exponentially increasing
growth rate. It refutes that particular inference from bounded eigenvalues.
It does not show failure of continuous dependence in every topology, nor
prove nonlinear ill-posedness for constrained v3s data.

There is an immediate repair at the frozen level. Conjugate by
D=diag(1/k,1), or equivalently use delta P=delta rho/(ik) and delta v.
Then D B D^-1 has constant entries -i rho0 and -i C, independent of k.
Consequently the propagator is uniformly bounded in polarization/velocity
variables. In density language the estimate controls rho in H^s with v
in H^(s+1). The gravitational constraint also supplies its own inverse
derivative. No finite calculation chooses which nonlinear function-space
formulation is appropriate; that choice is part of the missing proof.

For the positive stiff control rho0=1/2, gamma Theta=1, the real matrix
inside -ikB/k is A_k=[[0,1/2],[1+1/k²,0]]. The positive symmetrizer
H_k=diag(1+1/k²,1/2) satisfies H_k A_k=A_k^T H_k. Its energy is conserved,
so the Euclidean propagator norm is <=sqrt(2+2/k²)<1.5 for k>=8. The
main linear-in-k diagnostic must fail on this control and does.

Both a0 footings merely set separate positive unit scales here. With
L_ref=24pc, T=sqrt(L_ref/a0), P_unit=a0/K and rho_unit=a0/(K L_ref),
the displayed equations are dimensionless. Gamma=1 in the positive-stiff
control corresponds to L_star=sqrt(2)L_ref; that illustrative control is
not a claim about CQ7's allowed interval. The main soft result is independent
of gamma and L_star. M=2 is an illustrative allowed Hessian, not fitted to
a system. No physical galaxy lifetime is inferred from T.

## Nonlinear characteristic truncation

For the pressureless principal subsystem

    rho_t + (rho v)_x = 0,     v_t + v v_x = 0,

write X(a,t)=a+t v0(a), J=1+t v0'(a). While J>0,

    v(X(a,t),t)=v0(a),     rho(X(a,t),t)=rho0(a)/J.

The script applies partial_x=J^-1 partial_a and
partial_t|x=partial_t|a-v0 J^-1 partial_a. Both residuals vanish exactly.
For v0=-sin(a), rho0=-1/2, J=1-t cos(a)>0 on0<=t<1, and its first zero
is at t=1,a=0. Density diverges there. For uniform v0=1, J=1 forever.

This verifies finite-time breakdown of this principal truncation and the
importance of an initial-gradient/lifespan condition. It is not a failure
of local existence before that time, and it omits v3s's W/Poisson forces.
It therefore cannot be advertised as a full-action caustic counterexample.

## Static and moving-interface route

AZ34's exact sequence has bounded switched energy and an unbounded H(div)
norm. It defeats the asserted coercive direct-method step. It is not a
sequence of solutions, so it does not establish that solutions develop
jumps or that a minimizer fails to exist. Strict convexity supplies only
conditional uniqueness in a specified admissible space.

The next static lemma is existence and a trace theorem in a precisely
defined relaxed space allowing the controlled positive divergence but not
assuming an unavailable full-divergence bound. To obtain evolution, one
must then prove regularity and source dependence of that leaf solution map,
propagate the constraints and cap/timelike margins, and control a moving
D.P=0 interface where the action is C1 but not C2. The frozen polarization
repair is promising input, not that theorem.

## Adversarial self-review

- Checked the Poisson sign independently: Phi=-K rho/k² and P=rho/(ik)
  produce the lower matrix entry -i K(M-1)/k.
- The numerical matrix tests retain self-gravity and agree with exact
  shear, zero-time,50-digit and separate time-stepping checks.
- A Jordan block in density variables is not transferred to all variables;
  the explicit polarization conjugation prevents that overclaim.
- Characteristic blowup is restricted to its stated truncation and does
  not count as an on-shell v3s counterexample.
- No nonlinear existence theorem is inferred from the successful finite
  checks. This is self-review, not independent-agent review.

Kappa = 1/2 FITTED; not theory closed.
