# Continuum and nuclear dynamics, continuation 2026-10-26

Base evidence: research commit68fc240da2d2455e83c386d24f278969c0ecbe12.
Goal remains physical finite scattering/assembly rates coupled to photon recycling,
with charge/energy conservation and shared microscopic parameters across profiles.
A fixed-nuclei elastic calculation alone does not satisfy this goal.

Route1: build public UKRmol+3.3.0 inner/3.3.0.1 outer, run its H2+ Coulomb
continuum test, inspect unitary K/S matrices and basis/outer-radius dependence.
Then replace target orbitals at varied R, keeping electron exchange and nuclear
charge+1. Require explicit numerical comparisons, not only executable exit0.

Route2: use actual S(R,E) to compute nuclear matrix elements/frame transformation
at mass ratio100. Resolve thresholds and closed-channel elimination. Fixed-nuclei
unitarity is not evidence of zero dissociative recombination; a valid nuclear
outgoing-flux treatment is required for that rate.

Route3: check whether existing published state-resolved scattering data or code
can supply the missing continuum/nuclear dependencies at our mass ratio.
Ordinary hydrogen rates may benchmark a method but cannot silently become
mass-ratio100 rates. Fitted 2D model potentials cannot replace the Coulomb parent.

Only validated reaction probabilities feed the prior finite-rate/photon adapter.
Record incomplete steps without manufacturing physical halo trajectories.
