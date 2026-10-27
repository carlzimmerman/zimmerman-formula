# A reduced cosmological completion and nonlinear test

XP-20261023. Base revision6bec89a36197ce50a3100b6ede5c02d019a3ad94. This is an explicit action on a prescribed FLRW background, with a preferred foliation. It is a consistent reduced cosmological model in the sense of variational forces, conserved material masses and an expansion-work identity. It is NOT a uniquely derived covariant parent, a self-consistent Friedmann solution including field stress, or a constraint/hyperbolicity certification. These distinctions limit all predictions below.

## Completion choices

Let A(t) denote the cosmological scale factor (to distinguish it from the phase-potential coefficient alpha). Work on a periodic comoving volume with x coordinates. P denotes physical orthonormal spatial components in the preferred cosmological frame. Time derivatives of those components define the kinetic term. Physical gradients are D=A^-1 grad_x. Field coefficients and the inherited physical length ell0 are constant. Conserved cold and baryonic masses have physical densities rho_c,b=A^-3 rho_com,c,b. The homogeneous cold reference is the actual conserved cold mass divided by the physical periodic volume: bar rho_c=M_c/(A³ V_com). It is not an independently adjustable time-dependent source. Position variations preserve that mean.

Using the inherited dimensionless normalization (Poisson equation D²Phi=rho_total-bar rho_total and field action divided by4pi), choose

 S = integral dt {sum_i m_i A² |xdot_i|²/2
 + (1/4pi) integral d³x A³ [ eta |Pdot|²/2 + b chidot²/2
 - |D Phi|²/2 - Phi(delta rho_b+delta rho_c)
 - W(|P|) - e²/(2chi) - alpha(chi-1)²/2 - d |Dchi|²/2 ]},

 e=delta rho_c-D.P, W(p)=-p-log(1-p), |P|<1,
 eta=.005, b=d=.125, alpha=.005.

Here densities include the inherited4pi factor, so sum m_i corresponds to integral rho d³r/(4pi). Matter-potential coupling in the integral is equivalent to particle coupling, with only the homogeneous gravitational source subtracted. The rotational mediator is set to its homogeneous scalar-sector value zero; this is not a model of rotating galaxies. Baryons are pressureless in this test.

A lapse N can be restored by dt->Ndt and every velocity->velocity/N. This gives time-reparametrization covariance of the reduced externally specified-background action. It does NOT supply a gravitational lapse constraint or a physical clock sector. Physical-vector kinetic choices different from the one written can add H-dependent terms; they are different completions and are not claimed equivalent.

## Variational equations

For a cold particle,

 xddot+2H xdot=-A^-2 grad_x(Phi+h), h=e/chi.

For a baryonic particle replace Phi+h by Phi. The field equations are

 eta(Pddot+3H Pdot)=-partial_P W-Dh,
 b(chiddot+3H chidot)=e²/(2chi²)-alpha(chi-1)+d D²chi,
 D²Phi=delta rho_b+delta rho_c.

Thus the2H matter drag and3H field drag follow from the same volume-weighted action. They were not added as independent phenomenological damping. In a static background A=1 the displayed scalar-sector action reduces to the inherited local model. This reduction alone does not certify the galaxy fits or relativistic lensing.

## Action-based one-mode restriction

Take one planar mode with density contrasts delta_b,c cos(kx), longitudinal P=p sin(kx), and homogeneous chi. Keep the matter displacement action to quadratic order; retain the exact spatial average Wbar(p)=<W(|p sin theta|)>. Define q=k ell0/A, J_b,c=4piG bar rho_b,c t0², E=J_c delta_c-q p. Up to a common positive volume normalization the reduced Lagrangian is

 L=A³ [ J_b delta_bdot²/(4q²)+J_c delta_cdot²/(4q²)
 + eta pdot²/4 + b chidot²/2
 + (J_b delta_b+J_c delta_c)²/(4q²)
 - Wbar(p) - E²/(4chi) - alpha(chi-1)²/2 ].

Dots here use dimensionless physical time t/t0. Gravity has been eliminated by its Poisson equation. The factor1/4 in the mismatch energy is the spatial average of cos² times1/2. Likewise the average polarization kinetic coefficient is eta/4. The exact derivative is

 Wbar'(p)=<p sin²theta/[1-|p sin theta|]>.

The Euler-Lagrange equations are

 delta_bddot+2H delta_bdot=J_b delta_b+J_c delta_c,
 delta_cddot+2H delta_cdot=J_b delta_b+J_c delta_c-q² E/chi,
 eta(pddot+3H pdot)=-2Wbar'(p)+q E/chi,
 b(chiddot+3H chidot)=-alpha(chi-1)+E²/(4chi²).

The field nonlinearity is retained exactly within this projection. Nonlinear W produces spatial harmonics in the full theory; this variational restriction projects them away. In particular the cos2kx phase mode and matter fragmentation are absent. It can test an early response and its approximation limits, not establish a three-dimensional core.

For the imposed EdS clock, Ht0=H0 t0 sqrt(Omega_m) A^-3/2, using N=ln A changes the matter friction to .5 delta_N and field friction to1.5 field_N. This follows from dlnH/dN=-1.5. A thermal/radiation-era treatment is not supplied.

## Energy exchanged with expansion

Let T_m be the material kinetic term, T_f the field kinetic term, U_g=-A³(J_b delta_b+J_c delta_c)²/(4q²), U_W=A³Wbar, U_chi=A³ alpha(chi-1)²/2 and U_e=A³E²/(4chi). The mode Hamiltonian is

 H_mode=T_m+T_f+U_g+U_W+U_chi+U_e.

It is not conserved on an external expanding background. At fixed canonical coordinates and momenta, differentiating with respect to ln A gives the exact work identity

 dH_mode/dN = -2T_m-3T_f-U_g+3(U_W+U_chi+U_e)
 + A³ E[-3J_c delta_c+q p]/(2chi).

The last term is essential: both physical density and physical wavenumber change. Treating the homogeneous reference as a fixed physical density would alter it and the model. The numerical evolution integrates this work alongside the equations and checks H_mode(N)-H_mode(N_i)-integral work dN. Expansion work is not outward field radiation or a cooling measurement. Backreaction on the scale factor would require the missing gravitational sector and its stress variation.

## Initial states and stopping criteria

Each matter mode starts with delta_b=delta_c=delta_i and delta_b,N=delta_c,N=delta_i at z1100. Two field preparations are compared:

1. Unpolarized: p=p_N=0,chi=1,chi_N=0.
2. Joint stationary fields at the instantaneous initial density:2Wbar'=q E/chi and alpha(chi-1)=E²/(4chi²), with zero field velocities.

The second is not cosmologically demonstrated adiabatic preparation. Small density contrast can imply a sizeable initial phase displacement. That extra stored field energy must be acknowledged; it is not generated during the simulated history. Quadratic-W controls use the identical initial field data, not independently retuned equilibrium.

Evolution stops at either matter contrast magnitude .3, |p|=.95, chi=.05, or z10. A negative-contrast limit is not collapse. A positive-contrast limit is still only the boundary of this perturbative-matter model. Neither is a core detection. No primordial spectrum or ensemble probability is assumed by these single-mode initial amplitudes.
