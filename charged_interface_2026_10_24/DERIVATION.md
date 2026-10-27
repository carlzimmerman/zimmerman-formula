# Charged interface: forces and limits

These are new effective postulates tested against the existing model, not
consequences of the Zimmerman normalization or a microscopic carrier theory.
The inherited units, galaxy profiles, cold density, W potential, C gate,
and tail treatment are in the snapshotted code. No galaxy data were refitted.
The original density is granted so that preserving its actual force balance
is a necessary test, rather than counting the imposed acceleration curve.

## Independent charge and its cost

Introduce a shift-symmetric interface field theta with
L_theta = chi(q,grad q,u) [theta_dot^2-c_theta^2 |grad theta|^2]/2.
Its canonical density p=chi theta_dot obeys charge conservation, Q=int p.
Minimizing int p^2/(2chi) at fixed Q gives p=Q chi/I, I=int chi,
and E_Q=Q^2/(2I)=k/I. This conserves Q, not T particle number.
The positive charge block and spatial theta energy do not supply charge
production. A zero-charge homogeneous reservoir cannot create a nonzero
net Q under this action. The tested initial Q is a supplied resource.
The global minimum in p allows redistribution between disconnected walls;
actual charge transport can be slower or topologically restricted. We have
not simulated that transport or established formation from free initial data.

For any variation z,
delta E_Q=-k delta I/I^2,
delta^2 E_Q=2k(delta I)^2/I^3-k delta^2 I/I^2.
The fixed-Q phase Hessian is the relaxed-charge Schur complement where
chi>0. Its positive finite-grid eigenvalues are local energetic evidence,
not a proof of full coupled continuum stability.

CI-1 uses chi proportional to |grad q|. CI-4 through CI-8 use
chi proportional to F(u)|grad q|, F(u)=u^2/(1-u).
u is computed from the actual enclosed T mass, including when mass varies.
The regularized discrete capacity is
I=sum_faces r_f^2 F(u_f) [sqrt((Dq)^2+(delta dr)^2)-delta dr].
The zero-gradient subtraction keeps the pure phases charge-free.
The implementation uses an algebraically stable equivalent expression.

## Phase, mass, and reciprocal forces

Write A for the linear enclosed-T-mass map at fixed total cell masses,
J_u=A diag(h'), J_q=D diag(h'), u=Aq, q=h(x).
With s_delta the regularized absolute value,
I_x=J_u^T[r_f^2 F' s_delta]+J_q^T[r_f^2 F s_delta'].
I_xx contains the two corresponding second derivatives, both h'' terms,
and both mixed J_u^T diag(r_f^2 F' s_delta') J_q terms. These are retained.
The exact implemented Hessian is 2k I_x I_x^T/I^3-k I_xx/I^2.

At fixed Eulerian q, the response charge adds the mass potential
mu_u,Q= -k/I^2 A^T[r_f^2 F'(u_f) s_delta(Dq)]/m.
CI-6 also adds E_tau=tau J, J=sum r_f^2 s_delta(Dq). It has no direct
fixed-q density derivative, but does contribute to the conversion derivative.
No charge or tension term is dropped when evaluating the phase gradient.

Define mu_q=E_x/(m h') and mu_c=q mu_u, including the inherited bulk,
barrier, gradient and infinite-tail terms appropriate to each variant.
The species potentials, obtained by independently varying rho_T and rho_F,
are mu_T=mu_c+(1-q)mu_q and mu_F=mu_c-q mu_q.
Both accelerations are -grad mu_i. The code uses nonsingular endpoint ratios
(1-q)/h' and q/h'. A spatially constant charge contribution to mu_u below
an isolated wall changes conversion energy but leaves pure-interior force
unchanged. It need not be constant across the wall; that force is tested too.

The phase equation in a positive reference metric is M xdot=-E_x.
Thus E_dot=-E_x^T M^-1 E_x<=0. Optimization recovery is only an energetic
basin test. It supplies neither a physical timescale nor a formation history.
Variations of baryon inputs also act reciprocally through the inherited
C functional (delta E=beta integral s F delta C), gravity and any externally
specified normalization. The added chi has no separate explicit baryon
dependence in physical variables with a0 held fixed. C and baryons are
prescribed here; their live response has not been solved.

## Radius and contrast are different modes

For a single sharp unit wall with chi=|grad q|, J=I=R^2 in the absorbed
spherical normalization. The isolated surface energy is tau R^2+k/R^2,
with radial force -2tau R+2k/R^3. At R^4=k/tau its radial stiffness is
8tau>0. This is an actual restoring force, but not sufficient: allowing
contrast a gives J=I=a R^2, leaving a degeneracy along fixed a R^2.
Fragmentation and amplitude changes must remain in the field problem.

For response charge the corresponding surface force is
f_R=-2tau R+k I'/I^2, with stiffness
K_R=2tau+k(2 I'^2/I^3-I''/I^2), plus the parent energy derivatives.
For a unit wall along the granted galaxy-law mass profile, R^2 F(u(R))
equals normalized enclosed baryon mass. This identity applies along that
specific profile, not arbitrary variations of density or contrast.
At fixed profile shape, small contrast gives I proportional to a^3,
so fixed Q penalizes erasing contrast more strongly than plain area charge.

## Matter equilibrium discriminator

A stable phase profile is not necessarily a stationary material galaxy.
With calculated g_eff=g0+dmu_i/dr, spherical stationary kinetic stresses
obey (r^2 P_r)'=-r^2 rho_i g_eff+2r P_t. Both P_r and P_t must be
nonnegative; P_t includes any streaming contribution. If P_r(R)=0,
P_r(r)<=r^-2 integral_r^R s^2 rho_i g_eff ds=U_i(r).
A negative U_i excludes every such kinetic support, not just isotropy.
This bound allows arbitrary radial/tangential anisotropy and is stronger
than the isotropic Jeans check. It assumes no additional confining traction
or material stress beyond the energetic forces already differentiated.
Changing the total density and solving its coupled equilibrium could change
this result, but would then require independently recovering the galaxy law.

All derivations and numerical audits here are self-reviewed, not independently
reviewed. Finite-difference phase, Hessian and species-mass checks are recorded
in the run outputs. No universal exclusion of interface interactions follows.
