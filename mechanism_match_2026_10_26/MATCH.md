# Exact matching to regular T/F fields and the finite carrier

The matched model is a new nonrelativistic canonical extension of the inherited
CC model. It is regular in the complex fields, including zero T amplitude.
This matches an interaction to the actual action; it does not derive the new
parameters from the Zimmerman formula or complete relativistic microphysics.

## Variables and normalization

Use the original canonical chart documented in
infall_pump_2026_10_25/ORIGINAL_VARIABLES.md. Write psi_T,psi_F for the regular
complex amplitudes, rho=|psi_T|^2, a for the carrier angle and p_a for its
momentum. The material Berry term is
i sigma(psi* psi_t-psi_t* psi)/2, summed over species. The inherited stiffness
is kappa=sigma^2, so the physical material velocity is sigma grad(arg psi)
in the uncoupled pure-component limit. rho is the inherited mass-density
normalization, not a newly introduced microscopic particle-number density.

Keep the EXACT existing density/gravity/response/F-pressure/binding energy,
carrier gradient and density-dependent inertia Z, plus alignment

    E_align = J |cos(a) psi_T-sin(a) psi_F|^2.

The existing phase in the alternative phi chart is absent in this original
psi chart. Do not retain both versions. Let s be the new real mediator,
P_s its canonical momentum density, and A_s=g1+h s. Define

    D_s psi_T = [grad-i A_s grad chi/sigma] psi_T,
    v_chi = Pi_chi-A_s rho.

The continuum Hamiltonian density, with the inherited nonlocal terms understood
as functionals, adds/replaces only the following sector:

    H = H_inherited_potential_and_carrier
        + kappa (|D_s psi_T|^2+|grad psi_F|^2)/2 + E_align
        + (Pi_chi-A_s rho)^2/2 + c^2 |grad chi|^2/2
        + P_s^2/2 + c^2 |grad s|^2/2 + M^2(s-lambda rho)^2/2.

The old g2 rho connection and old density-dependent scalar-momentum shift are
REPLACED by A_s, not added to it. Every displayed new kinetic/gradient/tracking
piece is nonnegative; inherited gravitational energy need not be positive.
The inherited carrier density force from p_a^2/(2Z[rho]) is unchanged and must
remain in the material equation. Parameters obey g2=h lambda for matching.

## Canonical equations and source

Let j_T=(kappa/sigma) Im(psi_T* D_s psi_T), with j_F the ordinary F current.
The exact phase/alignment equations give

    rho_T,t+div j_T=Gamma,
    rho_F,t+div j_F=-Gamma,
    Gamma=(2J/sigma) Im[psi_T*(cos^2(a)psi_T-sin(a)cos(a)psi_F)].

Here psi_T* denotes complex conjugation, not a new independent amplitude.
No reaction rate is inserted. Define q=A_s rho. The scalar equations are

    chi_t=Pi_chi-q,
    Pi_chi,t=c^2 lap chi-div(A_s j_T),
    chi_tt-c^2 lap chi=-[q_t+div(A_s j_T)].

Thus

    S = A_s Gamma+h[rho s_t+j_T.grad s].

At s=lambda rho this becomes
g1 Gamma+g2[2rho Gamma-rho^2 div v_T], wherever a velocity description exists.
The current/amplitude equations themselves remain regular at rho=0 and do not
divide by rho. Total mass is conserved and the scalar shift charge is
Q=int Pi_chi. With closed boundaries both are exactly conserved by continuous
Hamiltonian evolution.

The mediator equations are

    s_t=P_s,
    P_s,t=c^2 lap s-M^2(s-lambda rho)
           +h[rho chi_t+j_T.grad chi].

At FIXED s and Pi_chi, the new material chemical potential is

    Delta mu_T = -A_s chi_t-M^2 lambda(s-lambda rho).

There is no separate old g2 density derivative of the edge connection at fixed
s. That old force is recovered from mediator response/chain differentiation;
adding it independently double counts. The spatial covariant square supplies
the full j_T, mediator spatial work and scalar current companions.

## Exact finite-grid dictionary implemented in matched.py

Use a_T,i=sqrt(V_i)psi_T,i on the inherited material grid and the existing
linear material-to-wave interpolation P. Canonical scalar momenta in the code
are INTEGRATED, so

    v_chi = [Pchi-P^T((g1+h s_i)|a_T,i|^2)]/V_wave,
    s_dot = Ps/V_material.

For edge(i,j), A_e=g1+h(s_i+s_j)/2,
U_e=exp[-i A_e(chi_j-chi_i)/sigma], and
D_e=kappa w_e Im(psi_i* U_e psi_j). The extra scalar gradient is
(+A_e D_e/sigma,-A_e D_e/sigma) deposited by P^T. Each endpoint receives
-h D_e(chi_j-chi_i)/(2sigma) in the mediator Hamiltonian gradient.
The local mediator gradient also contains
V_i M^2(s_i-lambda rho_i)-h |a_T,i|^2 chi_t,i and the mediator gradient energy.
The material derivative contains Delta mu_T a_T, with the inherited potential,
alignment, hopping and carrier-inertia derivatives all retained.

This defines an actual regular finite-dimensional Hamiltonian, not merely a
source prescription. The full force dictionary is tested by independently
differencing this Hamiltonian in every canonical variable class.

## Exact old-action restriction and its limits

On the surface s=lambda rho, P_s=0, subtract ONLY the new positive mediator
gradient energy. The Hamiltonian is exactly the old CC Hamiltonian in its
original chart, at any field values. The chart map back to the older code is

    psi_T=exp[i(g1+2g2 rho)chi/sigma] phi_T,
    Pchi=V_wave*pi+P^T(g1 m_T+g2 m_T^2/V_material).

The restriction is not a dynamical invariant manifold. Its force is a pullback:
differentiate s=lambda rho as well as psi. That chain term recovers the old
g2 density-force companions. Testing equality of energies alone is insufficient.
At finite M, s evolves and need not equal lambda rho, so the old trajectory is
not a solution of the new model.

## Nonlinear elimination fixes an omitted companion

In the Lagrangian, write s=lambda rho+d and D0 for the OLD CC derivative.
Let j0=(kappa/sigma)Im(psi_T* D0 psi_T) and B=rho chi_t+j0.grad chi.
Neglect mediator derivatives only for this algebraic low-frequency reduction.
The d-dependent part of L is exactly

    -M^2 d^2/2+h d B-kappa h^2 rho |grad chi|^2 d^2/(2sigma^2).

Therefore

    d = h B/[M^2+kappa h^2 rho |grad chi|^2/sigma^2],
    Delta L_eff = alpha B^2/[2(1+alpha kappa rho |grad chi|^2/sigma^2)],
    alpha=h^2/M^2.

The denominator is compulsory. MP01's alpha Y^2/2 is recovered only to the
appropriate small-field-gradient order. The Schrödinger spatial square must
not be replaced by a linear current term when doing the exact match. Mediator
derivative corrections and heavy homogeneous initial data remain separate.

## Static and causality implications

At zero velocities and constant chi the mediator minimizes

    E_s=1/2 int [c^2|grad s|^2+M^2(s-lambda rho)^2].

The finite-grid minimizer solves
(M^2 diag V+c^2 L)s=M^2 lambda m_T. It gives a positive extra density-gradient
energy and force. The old profile is generally not stationary. The numerical
static experiment therefore re-minimizes ALL material densities/compositions
and the independent carrier, keeping total mass and the exterior free.
Optimizer energy decrease is not counted as radiation or a time history.

For a uniform pure-T low-frequency hydrodynamic patch, define
A=1+alpha rho^2 and the uncoupled material frequency Omega_k. The two light
branches satisfy

    A omega^4-[A Omega_k^2+c^2 k^2+g2^2 rho^3 k^2]omega^2
                   +Omega_k^2 c^2 k^2=0.

In the acoustic regime Omega_k^2 approximately c_T^2 k^2, the fluid cone
condition is alpha >= g2^2 rho/[c^2(1-c_T^2/c^2)]. This is conditional on a
stable acoustic closure, not a theorem about the actual nonlocal galaxy.

The ACTUAL inherited quantum-gradient term has
Omega_k^2=c_T^2 k^2+kappa k^4/4 in that local approximation. It produces an
unbounded large-k speed. Consequently the exact matched Schrödinger model is
NOT a globally causal relativistic completion. A finite-resolution solver does
not remove this continuum fact. MP01's relativistic-fluid claim cannot be
transferred to the full field model by identifying symbols alone.

The matching resolves the field/currents/forces dictionary. Microscopic
parameters, relativistic short-distance dynamics, actual transfer of the broad
mass-redistribution mode into radiation, and joint galaxy formation remain
unresolved physical obligations.
