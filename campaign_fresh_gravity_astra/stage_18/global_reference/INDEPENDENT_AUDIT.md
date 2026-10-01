# Independent audit: autonomous global reference coordinate

Reviewer: /root/pressure_extrema. **Accepted conditional analytic result.**
I inspected ROOT_DERIVATION.md and the separately attributed
BOUNDARY_ADDENDUM.md, and independently checked their variations, signs and
functional argument. I did not read the new author proof or other independent
audit outputs. No numerical execution, equilibrium construction or spectrum
was performed. No source correction is required.

The linked-boundary obligation was explicitly supplied to root by another
auditor before this addendum. My verification below is a check of that
attributed correction/clarification, not a claim of independent discovery.

## Energy and equilibrium

Because W_lambda=-T, the field Lagrangian contributes +integral T/C to
the lambda variation. The driver equation is therefore
I lambda_ddot+V'=integral T/C. Multiplication by lambda_dot shows that its
energy derivative exactly cancels the original fields' reference-work term
-lambda_dot integral T/C. Original fixed Dirichlet and impermeable walls
give zero physical boundary flux. This proves conservation of the stated
global autonomous action, not a local driver stress tensor.

At a static equilibrium the same driver equation becomes the independent
condition V'=integral T/C. The Q inverse has b_a<0 for positive g and a,
so T=-a integral b_a dv>0 for g>0. On a nonzero-field regular slab its
integral is positive. An identically constant V cannot support that static
equilibrium even though the action conserves energy and I>0. The proof does
not incorrectly assign unstable eigenvalues to this nonexistent equilibrium.
For other V the equilibrium condition must first be met by the actual state.

## Mixed Hessian and retained matter dynamics

Q homogeneity gives W_chi=-T, T_g=q and T_chi=2T-gq=S. Consequently
W_gchi=W_glambda=-q and W_chichi=W_chilambda=W_lambdalambda=-S.
The new second-variation terms are exactly

    -2q s psi'/C -2S s eta/C -S s²/C.

U depends on chi only, whereas V supplies V''s². Thus the signs of ell
and k in equation (5) are correct. The rho phi interaction has no explicit
lambda dependence, so it supplies no direct xi-s mixed derivative. Its
xi-psi term and fluid response remain in Q0 and therefore in the solution z.

The inherited isothermal matter expression is consistent with
delta rho=-(rho xi)' and e''=c_s²/rho: its second variation gives
c_s²((rho xi)')²/rho, and the interaction contributes
-2(rho xi)'psi. Zero displacement traces impose the first-order mass
constraint. Acceptance of the total Hessian is conditional on a genuine
equilibrium and the stated inherited fixed-wall action/constraint conventions.
No instantaneous field elimination or omitted wall compatibility term was used.

## Continuous Schur criterion

Assume, as the proof explicitly does, that Q0 is continuous, symmetric and
coercive on the fixed-unit space X=H1_0(0,d)^3. This is a substantive
antecedent and is not supplied for an arbitrary V-equilibrium by energy
conservation. Smooth bounded coefficients make ell continuous on X.
Coercivity and continuity make the a0 norm equivalent to the complete X
norm, so the unique representing element z exists.

From a0(z,u)=ell[u], Cauchy-Schwarz gives
ell[u]²<=Q0[z] Q0[u], with equality at u=z when z is nonzero. Hence
beta=Q0[z]=ell[z]=sup ell[u]²/Q0[u]; all are zero if ell=0. Expansion of
Q0[u+s z] verifies equation (6) with Delta=k-beta, including its plus sign.

The triangular change (u,s)->(u+s z,s) and its inverse are bounded.
Thus Delta>0 gives full coercivity. Delta=0 gives precisely the kernel
span{(-z,1)} and a nonnegative form; a nonzero initial velocity along that
zero-frequency mode can produce linear drift in the linearized system.
For Delta<0, (-z,1) is a negative direction. Any two-dimensional subspace
contains a nonzero vector with s=0, on which Q0 is positive; the negative
index is therefore exactly one. A zero value of an indefinite quadratic
form is not being confused with its operator kernel.

The spectral interpretation requires the regular operator assumptions stated
in the proof. In particular rho and the kinetic weights must be uniformly
positive and bounded on the closed interval. Under that regular-slab reading,
N is equivalent to L2^3 plus the scalar-coordinate norm, and the form-domain
embedding is compact. The cross term satisfies, for epsilon>0,

    2|s ell[u]| <= epsilon Q0[u]+(beta/epsilon)s².

Choosing epsilon<1 proves a lower bound by a multiple of -N, and adding a
sufficient multiple of N yields a norm equivalent to H1_0^3 times R. The
form is therefore closed and lower bounded with compact resolvent. Its
negative spectral count equals the form index: exactly one negative
squared-frequency mode for Delta<0, exactly one zero mode for Delta=0,
and a positive gap for Delta>0. No numerical frequencies have been computed.

Finite I>0 changes the kinetic norm and rates but cannot change this form
index or the sign criterion Delta. No uniform positive rate bound as I tends
to infinity is claimed. The singular I=0 constraint problem is correctly
excluded, and cannot be used to remove a degree of freedom from this argument.

## Dynamical theta variables and their domain

The dynamical point transformation theta=chi+lambda gives
pi_theta=sigma(theta_t-lambda_dot)/C and
P_lambda=I lambda_dot-integral pi_theta. Substituting
delta chi=delta theta-delta lambda in the old canonical one-form confirms
the sign of the global momentum shift. Solving for velocities yields the
positive kinetic Hamiltonian (7), including the square of
P_lambda+integral pi_theta. For finite positive I and sigma the kinetic form
is nondegenerate. In velocity variables, zero kinetic energy forces both
lambda_dot=0 and theta_t=0.

This is a time-independent point transformation on dynamical coordinates.
The full Legendre transform retains the same total Hamiltonian energy;
there is no residual prescribed-protocol energy correction. The construction
adds exactly one global canonical pair relative to the diagnostic system.
It has not established a gauge redundancy or any physical gravitational
degree-of-freedom count.

The original zero chi perturbation traces transform to
zeta(0)=zeta(d)=s. These linked traces must be part of the configuration/form
domain. Imposing independent zero theta traces would change the model and
remove allowed variations rather than demonstrate equivalence.

## Attributed boundary addendum

Integrating the original scale equation gives

    d/dt integral pi_theta
      =J[theta_x]/C+integral(T-U')/C.

Subtracting this identity from I lambda_ddot=integral T/C-V' yields exactly

    P_lambda_dot=integral U'/C-V'-J[theta_x]/C.

The same sign follows from the transformed variational boundary term
-J[theta_x delta theta]/C. Linked variations have delta theta=delta lambda
at both walls, so this contributes -J[theta_x]/C to the global equation.
Combining it with the integrated theta equation recovers the original driver
equation. Omitting the term would add a spurious +J[theta_x]/C force.
No equal-wall-gradient assumption follows from Dirichlet values, and none
is needed for the correct formula. This is a domain effect of the same
coordinate change, not an extra physical wall interaction.

## Scope and remaining obligation

The conservation, no-equilibrium obstruction and conditional Schur result
are valid for the explicit Q diagnostic extension. The analysis has not
selected physical I,V, supplied a qualifying equilibrium or checked Delta
for one. It supplies no local covariant reservoir, metric/photon coupling,
scale-vacuum interpretation, cosmological history or two-gravitational-DOF
construction. Both reference normalizations remain separate hypotheses,
and frozen H comparisons remain distinct from evolving H trajectories.
RAR, registered M and operative filtered MONO are not covered by this Q
action audit. No empirical or full-theory closure follows.
