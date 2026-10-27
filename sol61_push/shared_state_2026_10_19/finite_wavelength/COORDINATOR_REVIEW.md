# Independent coordinator reconstruction and integration limits

2026-10-19. The coordinator authored the finite-k, mass-dictionary and
nonlinear common-branch notes; those are self-reviewed here and have separate
peer reviews where recorded. The following calculations independently
reconstruct the delegated physical claims. Exact final bytes are pinned in
the packet checkpoint. This review is not an orbital-stability, quantum-gap,
formation or complete original relativistic-theory theorem.

## 1. Full GP plus declared gamma=5/3 baryon minimum

I checked the coercivity exponents directly. The potential near a point is
bounded by ||rho||_(5/3) R^(1/5), and its far part by M/R. Optimizing R yields
D(rho,rho)<=C M^(7/6)(integral rho^(5/3))^(1/2). With the scalar L1/L2
interpolation, gravity is controlled by A^(1/3)+C_b^(1/2), dominated by the
positive scalar contact and baryon internal terms. The scalar Fisher term
is also bounded along a minimizing sequence.

The two rearrangement inputs are explicitly sourced and independently checked
by the mode reviewer. They give a centered radial minimizing sequence for
the unrestricted infimum, rather than assuming that radial minimization proves
an unrestricted result. For radial nonnegative densities the Newton shell
formula gives V(r)<=M/r and uniformly bounds the Coulomb contribution with
one coordinate outside R by 2M²/R. On a compact ball the discarded diagonal
strip contributes at most C M||rho||_(5/3)epsilon^(1/5); a continuous truncated
kernel is weak-measure continuous by finite sums of product test functions.
This establishes gravitational-energy continuity without inventing strong
local density convergence from a weak Lp bound.

The shell no-loss argument handles both species and the zero-core case.
Add exactly the lost masses in a normalized squared smooth annular profile
eta_R. Fisher information of the sum is at most the two Fisher informations;
the added scalar gradient and baryon pressure cost O(R^-2), scalar contact
O(R^-3). Monotone radial rho_b<=C/R³ controls the baryon cross term. Negative
self-gravity of the added total mass is -cG(delta M)^2/R. This gives an
admissible full-mass energy below the weak-limit energy whenever any mass
is missing, contradicting E_limit<=I. The minimum is therefore attained.

I rederived its density Hessian: the Fisher second derivative is
(tau/2)integral rho_d |grad(delta rho_d/rho_d)|²; the scalar and baryon terms
are 2K integral(delta rho_d)² and (5Kb/3)integral rho_b^(-1/3)(delta rho_b)²;
gravity contributes -G D(delta rho_total,delta rho_total). A global minimum
has no negative admissible fixed-mass direction. This proves energetic
stability for the reduced functional, not a positive gap or nonlinear flow
stability. Ideal baryon EOS and fixed state data remain assumptions.

The common-cutoff mixed TF ODE is a stationary subfamily, not independently
certified to be that global minimum. Its finite-GP BVPs are stationary controls.
They cannot be silently relabeled global minimizers or the original physical
benchmark. The TF limiting-set argument is plausible with the stated smooth
recovery sequence and shell tightness; no quantitative mode/edge rate or
unique limiting branch is imported by it.

## 2. Exact common-profile linear source and nonlinear branch

Expanding K_d rho_d²+K_b rho_b² with rho_d=a rho+eta,rho_b=b rho-eta makes
the cross term zero and gives K rho²+K eta²/(ab). The inertia under
xi=a xi_d+b xi_b,zeta=xi_d-xi_b separates into
rho0(|xidot|²+ab|zetadot|²)/2. Variation gives precisely the total and
relative field equations in SHARED_MODES.md. The latter's density equation
is eta_ddot=2K div(rho0 grad eta), with no common-gravity source.

For a normalized relative radial eigenfunction, the dipole angular integral
is sqrt(4pi/3), its density coordinate inertia is R^5/(ab rho_c lambda),
and its source squared is (4pi/3)R^8 J_n². These give
d_d,n²=hbar mu F_n/(2omega_n), F_n=(pi²/3)lambda_n J_n².
The same perturbation has delta rho_b=-delta rho_d pointwise, so every total
mass-source transition vanishes, for all k. Its subsystem strength cannot
be used as the gravitational normalization.

The source xY10 lies in every trial space. Completeness analytically gives
sum F_n=1 and sum F_n/lambda_n=pi²/15. Their preservation in a finite Ritz
space checks implementation and does not alone certify an infinite spectrum.
For f(x)>= (1-x²)/2, the polynomial comparison form proves lambda_(l,1)>=l;
the x trial function gives the quoted upper bound for l=1. I checked the
lower envelope using sin(pi x)>=pi x-(pi x)^3/6 on x<=1/2 and its reflected
version on the other half. The regular singular surface branch, rather than
a fixed-wall condition, is the appropriate fluid mode domain.

The invariant nonlinear common-flow reduction in NONLINEAR_COMMON_BRANCH.md
then follows by direct substitution in both continuity and Euler equations.
The positive composition Hessian does not secretly become a nonlinear
gravity-driven saturator. That conclusion is for the exact common-profile
EOS control, not every unequal-profile GP/baryon equilibrium.

## 3. Actual occupations, response and analytic restriction

For a mass-normalized mode H=(p²+Omega²q²)/2 and source -g c q, its physical
matrix element is d=c/sqrt(2Omega) in hbar=1 units. Completing the square
gives a free-energy shift -g² c²/(2Omega²), independent of the thermal
occupation. The raising/lowering Kubo weights telescope to one, as stated.
Actual Gibbs, shell or pulse populations require their corresponding input
energy/temperature/preparation. They cannot be inserted as extra multiplicative
factors in the harmonic susceptibility. An unrestricted isolated finite-
temperature cluster's scattering volume prevents an unqualified global Gibbs
trace, even after COM removal.

I independently reconstructed the bounded-source theorem. An isolated simple
ground eigenvalue with gap gamma has resolvent norm <=2/gamma on a gamma/2
circle. A bounded perturbation -gD with |g|||D||<gamma/2 gives a convergent
resolvent expansion and analytic rank-one spectral projector. Parity forces
the continued ground energy even and its response odd analytic. The requested
g/(a+|g|) has a nonzero g|g| term and cannot agree near zero. Positive
classical energetic stability alone does not supply the theorem's quantum
gap. Infinite volume, evaporation, critical families and relativistic stress
must retain the note's explicit restrictions.

The cutoff response and error bound were independently differentiated and
checked: its infrared removed weight is at most p_sat epsilon²/(2a²), and its
UV response at most g integral_L^infinity w/Delta. Dividing by the target gives
the two terms in its certificate. The finite-window example is an approximation
of an imposed TLS weight, not an occupation prediction for these modes.

## 4. COM-relative physical first-moment budget

For D_h=sum_i m_i h(x_i-Rcm), differentiation gives
grad_i D=m_i[grad h_i-(sum_j m_j grad h_j)/M]. Position interactions commute
with D; applying the kinetic operator twice gives exactly the weighted
gradient variance in INTERNAL_TRK.md. The common COM kinetic term commutes
with D. Expanding cos(kz) in that variance cancels orders k^0 and k^2;
the first moment is k^4 <A4-A2²/M>/8+o(k^4) with a finite fourth moment.
Replacing <A2²> by the square of a mean is an extra fluid approximation,
explicitly distinguished. The n=1 density moments give
Vz=4/45-8/(3pi²)+20/pi^4=.0240187109363. Combined with the actual static
C, the effective squared frequency is 4.44199525105 GM/R³. It does not set
the source susceptibility to 1/(4piG).

## 5. Root finite controls and integration verdict

Finite-k direct matching agrees with a distinct static-kernel and dynamical
Ritz calculation in the mode lane on the l=1 component. Its l=3 addition and
COM-constrained eigenbasis tail were separately reviewed by the occupation
agent. The mass-gap dictionary was separately reviewed by the mode agent,
including restored hbar and the one-mode/one-object restriction.

Fourier phase, COM constraints, physical vs subsystem sources, scalar matched
contact, baryon closure, TF vs finite-GP branches, occupation vs Kubo weights,
exact vs tested spectra, source parity, units and cutoff claims were proofread.
The bounded source calculations are meaningful partial results; they neither
close the nonlinear dipole theory nor establish all-phase impossibility.
