# Spatial expanding-action discretization and initial state

SE-20261023, base142d9d8ccd50aceb78e9bd4fa20c120116029738, follows expanding_polarization_2026_10_23. Use the same reduced preferred-frame action and imposed matter-only background. This is its3D spatial extension, not a covariant parent or numerical integration of the homogeneous Friedmann constraint.

## Geometry, masses and canonical variables

Let A=a/a_i=(t/t_i)^(2/3), H=2/(3t), with dimensionless physical time in units t0. The comoving coordinates are normalized so that A=1 at the initial slice. A periodic cube has constant coordinate side L=L_com/[(1+z_i)ell0]. Physical gradients are grad/A. Two independent particle species carry constant masses m_c and m_b; physical density scales as their deposited coordinate density divided by A³. Subtract each species' actual mean in the Poisson source, and the cold mean in the mismatch field. No mass is removed or reassigned to a core population.

Define particle canonical velocity variables pi=A² xdot and field momentum variables Q=A³ Pdot, V=A³ chidot (the constant eta,b factors are left in the force equations). With forward lattice gradient and its negative-adjoint divergence,

 e=delta rho_c-div P/A, h=e/chi,
 Laplacian Phi=A²(delta rho_c+delta rho_b).

TSC weights w_i(x) sum to one. The exact particle force is the derivative of the discretized action:

 pidot_c=-sum_i (Phi_i+h_i) grad_x w_i,
 pidot_b=-sum_i Phi_i grad_x w_i.

Field momentum equations are

 Qdot=-(A³/eta)[P/(1-|P|)+grad h/A],
 Vdot=(A³/b)[h²/2-alpha(chi-1)+d Laplacian chi/A²].

No moment or shape restriction remains: particles have independent3D coordinates; P has three spatial components on the lattice; chi varies over all cells. The finite grid still cuts off short wavelengths and TSC softens forces. The lattice is not continuously rotation/translation invariant.

A time-dependent canonical kick-drift-kick scheme uses endpoint forces and exact EdS drift integrals:

 integral_t^u A^-2 dt=3 t_i^(4/3)(t^-1/3-u^-1/3),
 integral_t^u A^-3 dt=t_i²(1/t-1/u).

The highest lattice linear-field frequency controls dt, together with Hdt<=.015. The field domain |P|<.985,chi>.1 is guarded without physically evolving beyond it. No sponge or material damping is present. Expansion damping is already encoded in the canonical variables.

## Energy and expansion work

Let T_m=sum m pi²/(2A²), T_f=vol sum(eta Q²+b V²)/(2A³), U_g=A³ vol sum(delta rho_total Phi)/2,

 U_W=A³ vol sum W,
 U_chi=A³ vol sum alpha(chi-1)²/2,
 U_grad=A vol sum d|grad chi|²/2,
 U_e=A³ vol sum e²/(2chi),

where vol=dx³/(4pi). The Hamiltonian is the sum of these terms. At fixed canonical variables and particle positions its explicit ln A derivative is

 W_A=-2T_m-3T_f-U_g+3(U_W+U_chi+U_e)+U_grad
       +A³ vol sum h[-3delta rho_c+div P/A].

Along the exact flow dH_mode/dlnA=W_A. The code integrates this work and measures the residual normalized to the largest sum of absolute energy components encountered, avoiding cancellation in the initial perturbation energy. This is a numerical conservation test, not a cooling or radiation measurement. A negative Hamiltonian of a periodic perturbation is not a certificate of a localized bound object.

## Action-based low-excitation preparation

At fixed matter density and expansion factor, minimize the positive field energy over P and chi>0. The mismatch term e²/(2chi) is a jointly convex perspective of a square; W is strictly convex in the open unit ball; alpha(chi-1)² is strictly convex and the spatial chi-gradient term is convex. Thus in the finite periodic discretization there is at most one minimizer, subject to these domain conditions. At a stationary solution the discrete maximum principle implies chi>=1. This is a deterministic instantaneous minimum-energy prescription, not a quantum vacuum, inflationary state or cosmological attractor theorem.

Using h as a dual variable, set G=(alpha-d Laplacian/A²)^-1. The minimization solved numerically is

 F[h]=sum[ h²/2+s-log(1+s)-delta rho_c h+h² G(h²)/8 ],
 s=|grad h|/A.

Recover P=-(grad h/A)/(1+s), chi=1+G(h²)/2. The residual checks the stationary equation. The fields' initial velocities are H_i times the derivative of this stationary solution along the stated matter displacement and A variation. That tangent is computed with symmetric differences in lnA, and checked against a tenfold change in difference step. It avoids arbitrarily setting field velocities to zero, but when expansion is fast it need not equal a physically attained cosmological state.

Matter starts on a quiet particle lattice with displacement in each direction

 xi_j=-delta_i sin(k Q_j)/(3k), k=2pi/L,
 x_j=Q_j+xi_j, xdot_j=H_i xi_j.

At first order the contrast is delta_i[cos(kQ_x)+cos(kQ_y)+cos(kQ_z)]/3. This is a declared smooth test seed, not an inferred primordial power spectrum. Nonlinear deposition and evolution generate other spatial modes. Earlier-start tests use delta_i=.001*1101/(1+z_i), holding the dust-reference final amplitude fixed. They are different preparation histories, not guaranteed representations of the same cosmological solution.

## Mass labels and core requirements

The nominal mass1.095e7Msun defines R_L through total reference matter density, and L_com=2pi R_L=.2537Mpc. Hence total box mass is6pi² times that nominal mass; cold box mass is approximately5.47e8Msun. Neither the box mass nor particle mass is a predicted core mass.

The candidate detector uses periodic FoF with link .2 times initial mean particle separation and requires at least32 cold particles. Such membership is only a density/connectivity candidate. A bound-core certificate additionally needs adequate physical resolution, persistence and isolated matter-plus-field binding/escape accounting in the expanding background. No saved state contains a32-particle candidate, so no candidate binding-energy calculation is reported. This does not exclude objects missed by this resolution or detector.

At z10 the box spans23.06kpc. A0.3215kpc radius has only .223 cells at n16. Merely obtaining four cells per such radius requires about287 cells per axis, before stronger force, profile, mass and box-size convergence requirements. The inherited radius is a target benchmark, not a proof of the radius of any primordial object. At sufficiently early epochs a fixed-radius object may also be too large for the physical periodic box; cell count alone is never enough.
