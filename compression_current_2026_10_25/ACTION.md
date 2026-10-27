# Density-weighted current: explicit changed hypothesis

Let rho=|psi_T|² and q(rho)=g1 rho+g2 rho². Use a positive canonical action
with time coupling q(rho) chi_t and covariant spatial derivative

    D_i psi_T=[partial_i-i(g1+g2 rho)partial_i chi/sigma]psi_T.

Keep the full square kappa |D_i psi_T|²/2. The canonical Hamiltonian has
scalar kinetic energy [Pi_chi-q(rho)]²/2 and positive material/spatial field
terms. At rest chi is constant, relaxed Pi_chi=q(rho), and the old real
static energy is recovered exactly. Its restoring Schur complement remains
the old one. This is a kinetic coupling, not a static density gate or force
chosen to cancel a galaxy-law residual.

For the physical T current j_T and conversion Gamma,

    div[(g1+g2 rho)j_T]
      =g1 Gamma+g2[2rho Gamma-rho² div v_T].

Thus conserved pure-T compression is a source. The equality uses
rho_t+div(rho v_T)=Gamma. It is a continuum identity, not a prescribed source.

## Canonical transformed coordinates

Set psi_T=exp{i[g1+2g2 rho]chi/sigma} phi_T. The time one-form becomes
canonical up to -g2 d(rho²chi)/dt. The local alignment phase is

    beta=[g1+2g2 rho]chi/sigma.

The T spatial derivative becomes

    grad phi_T+i(g2/sigma)[rho grad chi+2chi grad rho]phi_T.

This gradient term is essential; omitting it would violate the current and
energy identities. F remains an independent canonical field. The full energy
is a sum of the old potential, positive spatial/material squares, independent
carrier kinetic energy and scalar kinetic/gradient energy. The shift symmetry
acts nonlinearly on phi_T, and its conserved charge is

    Q=integral Pi_chi dV+g1 M_T+g2 integral rho² dV.

## Discrete positive completion and force dictionary

On the existing radial matter grid write a_s,i=sqrt(vol_i) phi_s,i,
rho_i=|a_T,i|²/vol_i, chi_i=P_i chi_wave. For each edge i,j=i+1 set

    b_ij=(g2/sigma)[2rho_j chi_j-2rho_i chi_i
                         -(rho_i+rho_j)(chi_j-chi_i)/2].

Use exact kinetic energy kappa w_ij |exp(i b_ij)phi_T,j-phi_T,i|²/2.
The alignment uses beta_i=(g1+2g2rho_i)chi_i/sigma. These define all forces
by ordinary derivatives, including their quadratic terms.

Let D_ij=kappa w_ij Im[phi_T,i* exp(i b_ij)phi_T,j]. Then the additional
T chemical potentials at the edge are

    mu_i += D_ij(g2/sigma)(-chi_j/2-3chi_i/2)/vol_i,
    mu_j += D_ij(g2/sigma)(3chi_j/2+chi_i/2)/vol_j.

The corresponding scalar energy gradients are

    H_chi,i += D_ij(g2/sigma)(-3rho_i/2+rho_j/2),
    H_chi,j += D_ij(g2/sigma)(3rho_j/2-rho_i/2).

If Gamma_i is the actual local alignment mass-conversion rate, alignment adds

    mu_T,i += 2g2 chi_i Gamma_i/vol_i,
    H_chi,i += (g1+2g2rho_i)Gamma_i.

All gradients deposit to the wave grid by P^T. The extra density force from
carrier inertia remains required, exactly as in NT. Wave exchange is
-integral chi_t H_chi, with compression and conversion contributions recorded
separately. No lost optimizer energy is counted as radiation.

Summing the edge scalar gradients gives
2g2(rho_j-rho_i)D_ij/sigma. This equals the weighted charge change from its
material edge current dm_i/dt=-D_ij/sigma, dm_j/dt=+D_ij/sigma. Together with
alignment this proves the semidiscrete shift identity. For a midpoint method,
using endpoint-average rho in these coupling weights also preserves the
quartic discrete charge through the exact mass increment product rule.

The new interaction starts beyond quadratic order about rho_T=0, so the old
outer-F linear conversion margin is unchanged. This is not a nonlinear
no-nucleation result. The normal F EOS, microscopic coefficient and population
constraints remain open even if one radial experiment succeeds.
