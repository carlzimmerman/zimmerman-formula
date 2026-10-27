# Joint phase and material energy

Use the parent normalization r_M=sqrt(G M_b/a0), energy M_b a0 r_M,
dimensionless enclosed masses in M_b and radii in r_M. The radial volume
measure is r²dr; density below absorbs 4pi. Baryons are a prescribed Plummer
profile. No dark density is supplied by the target law during optimization.

Let rho_T=q rho, rho_F=(1-q)rho, q=sin²(pi x/2), and
u(r)=M_T(<r)/r². The tested energy is

E = E_grav + integral r²[W(u)+beta C s(x) F(u)]dr
  + ell²/2 integral r² F(u) (x')²dr
  + tau J + k/I + K/(gamma-1) integral r² rho_F^gamma dr,

W=-log(1-u)-u, F=u²/(1-u), s=sin²(pi x)/pi², gamma=5/3,
J=integral r²|q'|dr, I=integral r²F(u)|q'|dr.
Absolute values are regularized as stated in code. The total available mass
is fixed, but each density cell and phase fraction can change. Q²/2=k is
supplied interface charge. C=.95 is prescribed independently of the galaxy
law; this avoids using a law-derived velocity gate to claim law emergence.

The Newtonian gravity energy is integral rho Phi_b dV + .5 integral rho
Phi_dark dV. Its functional derivative is Phi_b+Phi_dark, including both
halves of dark self interaction. LD-1 through LD-14 used a symmetric point-shell
kernel, 1/max(r_i,r_j), with .5 shell self energy. The plot audit exposed
incompatible high-frequency curvature between this and the midpoint W
quadrature. The current LD-17/18 implementation instead uses

E_grav=-sum_i vol_i [.5(A m)_i²+g_b,i(A m)_i]
       -M²/(2R)-M/sqrt(R²+b²),

with exactly the same enclosed-mass operator A and volume weights as W.
The last two terms are the exact exterior self/cross gravitational tails.
Pure cold-T bulk curvature is then
A^T diag(vol[1/(1-u)²-1]) A, positive for 0<u<1, plus the positive
W-minus-gravity tail curvature. This fixes a numerical inconsistency without
adding physical density stiffness or altering the continuum action. The
small-u W series from the original model is retained in the tensor code,
avoiding cancellation in the infinite-tail integration.
The W tail to infinity is retained. The response-stiffness exterior has
zero infimum capacity at infinity. No attained exterior field profile is
claimed; physical candidates must have negligible phase at the box boundary.

## All material and conversion forces come from this energy

Write mu_c=delta E/delta rho at fixed q and
mu_q=(1/rho) delta E/delta q at fixed rho, with spatial derivatives treated
variationally. The two species chemical potentials are

mu_T=mu_c+(1-q)mu_q,  mu_F=mu_c-q mu_q.

The nondissipative species forces per mass are -grad mu_T and -grad mu_F
when the pressure enthalpy is included in mu_F. Equivalently, separate its
pressure gradient from the nonthermal force. Local conversion at equilibrium
requires the conversion variation to vanish where both phases coexist;
pure-phase endpoints require one-sided stability, not merely E_x=0.

The F energy adds h_F=gamma K rho_F^(gamma-1)/(gamma-1)=(5/2)K rho_F^(2/3)
to mu_F, zero directly to mu_T, and P_F=K rho_F^(5/3)>=0. At fixed total
density its conversion contribution is -rho h_F delta q. It is retained in
the phase gradient: pressure cannot be added afterward without this term.
This is a stipulated fluid closure. A nonnegative collisionless distribution
function and an entropy-production/heat-transport law are not supplied.

For the charge term, delta E_Q=-k delta I/I² and
delta² E_Q=2k(delta I)²/I³-k delta² I/I². Its mass derivative includes
-k/I² integral F'(u)|q'| delta M_T dr. Thus changing interior T mass changes
the wall energy even when that cell is not in the wall. The phase derivative
also contains the local derivative of |q'| and every u(q) dependence.
Tension contributes tau delta J. The gradient energy contributes both its
ordinary phase flux and the derivative of F(u) under density/conversion.
Torch automatic differentiation retains all these mixed contributions; the
directional checks compare against independent energy differences.

In discrete coordinates E_x/(m h') is the conversion potential away from
pure endpoints. Endpoint ratios or limiting second variations are needed;
division by a vanishing h' is not a physical force. Density stationarity on
the simplex requires mu_c=lambda in occupied cells and mu_c>=lambda in empty
cells. Reporting only the softmax gradient m_i(mu_c-lambda) can conceal a
finite residual in a nearly empty cell; direct-mass KKT residuals are retained.

## Exact cold-bulk implication: the law is an output

In a pure T region separated from the interface, gradients and s vanish.
The interface charge contributes a spatially constant chemical offset below
its support. Therefore the T material equation reduces to

0=d(Phi+mu_W)/dr = g_b+g_F+u - u/(1-u).

Here mu_W(r)=integral_r^infinity W'(u(s))ds and W'=u/(1-u).
Consequently u²/(1-u)=g_b+g_F. With total gravity g=g_b+g_F+u,

g²/(1+g)=g_b+g_F,
g=[g_b+g_F+sqrt((g_b+g_F)²+4(g_b+g_F))]/2.

Restoring dimensions gives g²/(a0+g)=g_b+g_F. This is the desired original
galaxy law exactly when g_F is negligible. The derivation uses the Euler
equation, not an imposed density curve. It is conditional on a pure cold
interior and vanishing interface-force gradient there. An almost-pure
average q is not enough, as the previous charged-interface work demonstrated.
Non-negligible free matter, finite phase gradients or thermal T pressure
change this implication and must be measured, not discarded.

LD-4 independently optimizes an all-T cold bulk with no charge/tension/gas
terms from an unrelated Plummer mass profile. It checks this normalization
and continuum implication, while deliberately failing the outer-free task.

## Boundary restoration after density relaxation

At fixed density, tension gives -2tau R for a sharp spherical unit wall.
Response charge adds k I'(R)/I(R)², but I depends on the actual relaxed mass,
not automatically the baryonic enclosed mass. The full derivative also has
bulk, gravity, pressure and gradient terms from E above.

If m_*(x) is a constrained, locally stable density minimum, the relaxed
phase Hessian is the Schur complement

H_relaxed=H_xx-H_xm H_mm^(-1) H_mx,

where H_mm is restricted to the active mass-conserving tangent space.
It can be less stiff than the frozen-density Hessian. Density relaxation
does not by itself prove restoration. For a translating wall with direction
v=dx/dR, F_R=-v^T E_x at relaxed mass, and at full stationarity its local
stiffness is v^T H_relaxed v (when the translation and active set are smooth).
If H_mm is unstable, the state already fails material stability. Direct
displacement and re-minimization tests are needed to detect mesh pinning and
changes of active set that this local expression can miss.

The finite runs are energy relaxation, not physical-time evolution. They
neither create net interface charge from Q=0 nor derive K, tau, beta or
charge abundance from the original normalization. Baryon reaction and live
baryon evolution remain outside this controlled spherical test.

## Charge-free pressure-driven seed instability (LD-11)

Set k=tau=0. Around the all-F state x=0 at fixed nonzero density,
q=(pi²/4)x²+O(x⁴), u=O(x²), W=O(x⁴), and both the barrier
and response-stiffness contributions are O(x⁶) for a uniformly scaled
smooth perturbation. Gravity has no phase variation. The F pressure energy
instead gives

E[x]-E[0]=-(pi²/4) integral rho h_F x² dV + O(x⁴).

Thus its phase Hessian is negative in any occupied region with K>0:
H_xx=-(pi²/2) diag(m h_F) at x=0. Infinitesimal T seeds lower
energy without a preloaded charge or negative bulk binding term. This is
a local formation instability in the stipulated fluid energy, not a proof
that its endpoint is a finite core. The system may still convert all bound
matter, collapse into a different phase profile, or stop at a numerical
boundary. LD-11 explicitly tests the endpoint and keeps the free-exterior
requirement. Physical heat/entropy transfer in actual conversion is still
not derived from this dissipative minimization.
