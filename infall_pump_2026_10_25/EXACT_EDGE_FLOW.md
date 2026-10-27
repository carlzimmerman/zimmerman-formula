# Exact nonlinear transport flow, including scalar backreaction

Work in ORIGINAL_VARIABLES.md. For one T edge, put masses mi,mj, cell volumes
vi,vj, d=chi_j-chi_i, h=g1+g2(mi/vi+mj/vj)/2. Its energy is

 H_edge=kappa*w/2 |exp(-i*h*d/sigma)psi_j/sqrt(vj)
                                      -psi_i/sqrt(vi)|^2.

Use the generating function

 F=d [g1(mj-mi)/2+g2(mj^2/vj-mi^2/vi)/4] = d C.

F_mj-F_mi=h*d. Therefore z_s=exp(-i F_ms/sigma)psi_s removes the edge phase.
The conjugate scalar momentum in z coordinates is Pi_z=Pi_psi-F_chi.
H_edge is now the bare positive rank-one quadratic hopping matrix

 (kappa*w/2) (1/sqrt(vi),-1/sqrt(vj))^T
                     (1/sqrt(vi),-1/sqrt(vj)).

Evolve z with its EXACT two-by-two unitary exponential. chi is constant under
this sub-Hamiltonian. Transform back using the NEW endpoint masses. Then

 Delta Pi_left=-Delta C, Delta Pi_right=+Delta C.

Deposit these impulses with the original adjoint interpolation. Physical pi
also changes by -deposit(Delta q)/wave_volume. This supplies BOTH the density
chemical-potential companion and the scalar force; it is not frozen-density
hopping. Total material mass and sum Pi are conserved. Disjoint edges commute,
even if their deposited momenta share wave nodes, because chi stays fixed.
For g2=0 the Pi impulse exactly transports g1*m and the bulk physical pi kick
vanishes, recovering the conserved-current boundary-term limit.

## Full Hamiltonian partition

A = original density/response/gravity/F-pressure/carrier-gradient potential
    +J(mi_T cos^2 alpha+mi_F sin^2 alpha)+p_alpha^2/(2Z).
    Species masses are constant in this flow. Solve the tridiagonal implicit
    carrier midpoint at these masses; advance material phases with the SAME
    midpoint density derivatives, including derivative of Z. This is midpoint
    in density/phase variables, and is self-adjoint. No carrier relaxation.
B = -J sin(alpha)cos(alpha)(psi_T^*psi_F+c.c.).
    Exact local sigma_x rotation. Re(psi_T^*psi_F) is constant, so
    Delta p_alpha=2J cos(2alpha) Re(psi_T^*psi_F) dt exactly. Pi stays fixed;
    physical pi compensates the actual q change.
C_even,C_odd = exact edge flows above, including bare F hopping.
D = free physical scalar wave at fixed material masses, with canonical matter
    phase advance exp[i q'(rho) Delta chi/sigma]. CN preserves the quadratic
    wave energy; no source or damping is inserted in this Hamiltonian step.

Symmetric A/2,B/2,C_even/2,C_odd/2,D,C_odd/2,C_even/2,B/2,A/2 is second order.
Its symmetric triple composition is fourth order for fixed smooth finite
discretizations. Negative Hamiltonian substeps are allowed. Exterior absorption
is handled separately by positive exact half steps on physical pi. Every
intermediate physical cap must pass. This is a different time integrator of
the same action; it requires component force audits and actual time refinement.

The material-to-wave work of B and C is evaluated from the actual impulse,
sum wave_volume*pi_average*Delta pi, with separate conversion and transport
ledgers. Independently compare it with wave-energy change and actual outgoing
flux. A numerical full-energy defect is never attributed to radiation.

Fast carrier phases can remain underresolved even when midpoint is stable.
The new factorization removes a root bottleneck; it does not waive refinement
or establish galaxy formation by algebra alone.
