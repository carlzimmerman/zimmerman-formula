# What the density-weighted current does to the existing restoring force

This is an active finite-grid equilibrium statement, not a stability theorem
for the moving infall trajectory. The inherited run_restoring in NT relaxes
density and both real phase/composition fields at fixed total mass. Its active
radial Hessian is positive and its boundary Schur complement is

 k_R=0.00041127513 Eunit/kpc^2,
 delta F_R=-k_R delta R.

At a coherent real equilibrium with chi=pi=p_alpha=0 the CC operator changes
NONE of that density/carrier energy. Density/carrier fluctuations are even
under time reversal, whereas material phases, chi and canonical momenta form
the complementary quadratic block. There is no quadratic density/phase cross
term at this background. The latter block is manifestly nonnegative:

 Q_phase = kappa/2 sum_edges w sqrt(rhoTi rhoTj)(Delta thetaT+b_chi)^2
          +kappa/2 sum_edges w sqrt(rhoFi rhoFj)(Delta thetaF)^2
          +J sum_cells cos(alpha)sin(alpha)aT aF
                         (thetaT-thetaF+beta_chi)^2
          +sum p_alpha^2/(2Z)+sum wave_volume*pi^2/2
          +c^2/2 sum wave_weights(Delta chi)^2.

b_chi and beta_chi are the EXACT linear spatial and alignment phases in the
existing CC action, including every density-dependent companion. Coefficients
are nonnegative on the inherited coherent branch. The global shift symmetry
gives a neutral gauge direction, not negative stiffness.

Therefore eliminating/relaxing this phase-field block cannot erase the
inherited positive radial restoring potential. It changes the dynamical
inertia and radiation memory, not the static restoring coefficient. Enforcing
fixed GLOBAL shift charge on a density perturbation can add a nonnegative
field-momentum cost; a free large exterior can carry compensating charge at
arbitrarily small energy. No outer material radius or conversion fraction is
fixed by this argument.

Thus the same model still HAS a finite restoring equilibrium compatible with
the law and a filled transition. It does not follow that infall reaches that
equilibrium, that a finite energetic trajectory is restoring, that all inactive
or nonradial modes are stable, or that the active Hessian is continuum certified.
The new quadratic energy audit checks the displayed block independently; the
old positive density Hessian and Schur complement remain inherited evidence.
