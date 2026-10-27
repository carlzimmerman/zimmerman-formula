# Test the surviving short-range route rather than assume it works

A classical one-zone relaxation exposure is X=C*rho*sigma*t, where C is an
unspecified common transport cross section per total mass. Let the diagnostic
processed fraction be1-exp(-X). This fraction is NOT a condensate or tether
fraction. A common C can give disk>=.8 and all other inputs<=.2 exactly when
min_{i!=disk} rate_disk/rate_i >= ln5/[-ln(.8)]=7.2126.
The density/velocity recipe and common10Gyr age are the same for all objects.
The interval for C is computed, not fit separately per class. C is an extra
physical parameter, not derived from the earlier matched Coulomb interaction.

However the intended Bose-state application cannot ignore occupations. In an
explicit schematic Bose-enhancement proxy, replace the collision rate by
C*rho*sigma*(1+N), N=n*(sqrt(2*pi)*hbar/(m*sigma))³. This is a common
phase-space estimate, NOT a solved quantum Boltzmann collision integral. It
can be wrong for particular angular/energy distributions or nonequilibrium
states. We test its implication, not assert its universality.

For the positive species n=rho/[(1+epsilon)*m], common epsilon=.1 and m.
For an ideal equilibrium gas the degeneracy screen is N_disk>=zeta(3/2).
Writing R=N_smallest_dwarf/N_disk, the exposure ratio is
Gamma_disk/Gamma_dwarf = (rho_disk*sigma_disk)/(rho_dwarf*sigma_dwarf)
                       * (1+N_disk)/(1+R*N_disk).
R>1 makes this decrease with N_disk. Thus its maximum in the screened
condensed regime occurs at N_disk=zeta(3/2). The resulting bound is below
7.2126: no C meets both requested processed-fraction screens in this proxy.
This analytic statement covers any common positive mass within the same
assumptions, beyond the finite scan. The screen does not address negative
species kinetics, self-consistent thermalization or actual condensation.

Outcome: a classical short-range gate can select the dense disk input, but
identifying that processed state with the proposed Bose medium is unsupported
and fails under this standard schematic enhancement prescription. A different
internal phase or a full nonequilibrium collision integral remains open. This
is not a theorem excluding self-interacting or superfluid dark matter.
