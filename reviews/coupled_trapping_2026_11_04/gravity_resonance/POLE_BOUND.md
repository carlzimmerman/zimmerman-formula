# Coherent pole bound, independent of velocity and detuning

The microphysics package supplies a positive production Gram matrix G and
positive neutral absorptive width matrix Gamma_o for the four degenerate
singlet scalars. Let Gamma_i be any positive incoming-pair width matrix,
Gamma=Gamma_o+Gamma_i, and let H be any Hermitian real-part inverse-propagator
matrix, including detuning and coherent mass mixing. Put

    D=(H+i M Gamma)^-1,
    B=Gamma^-1/2 H Gamma^-1/2.

Then, in positive-semidefinite matrix order,

    D Gamma_o D^dagger <= D Gamma D^dagger
      = Gamma^-1/2 (B^2+M^2 I)^-1 Gamma^-1/2
      <= Gamma^-1/M^2 <= Gamma_o^-1/M^2.

Thus the physical-pair inclusive neutral pole cross section used by this
package obeys

    sigma v = (2/E) Tr[G D Gamma_o D^dagger]
       <= [2/(m M^2)] Tr[G Gamma_o^-1].

The coefficient on the right is exactly the zero-velocity, exactly tuned
tree-pole value, about15742 mu^-2. The looser trace/minimum-width bound is
unnecessary. This is a uniform statement about the stated fixed-coefficient
pole model, not a bound on every annihilation channel or on arbitrary
energy-dependent self-energies. It assumes Gamma_o>0 and positive incoming
widths; medium occupation/inverse reactions require a separate collision
operator. Thermal or real loop mass shifts can be retuned in H without
evading this mathematical bound while these absorptive matrices are fixed.

## Maximally favorable cosmological comparison

Grant that every charged particle is already a scalar, that its mass is
held on the pole at all phases, that this maximum cross section acts at
every relative velocity from the chosen initial temperature onward, and
that all neutral exits are permanently removed. These assumptions favor
depletion more than a real oscillating, momentum-resolved pole history.
Use n for both signs, so dY/dt=-s sigma v Y^2/2. Ignoring every positive
energy source except redshifted initial visible radiation gives

    L_pole <= s_star/(2H_star) sigma_max (1-1/a_final),
    Y_final >= [1/Y_star+L_pole]^-1.

This comparison is independent of an assumed FD velocity shape. The fixed
pole matrices and single pole subspace remain the conditional model input.
It does not exclude additional early scalar/fermion loss channels, changing
microscopic parameters, or a different model. Its purpose is to determine
whether placing the existing protected scalar vacuum on this newly found
pole can by itself erase a substantial heavy relic left after trapping.
