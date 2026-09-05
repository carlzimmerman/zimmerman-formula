# Comparable-mass force and three-frequency study

Target T-B only: the exact inverse exponential constitutive law in the
double-filter action of `../smoothed_onset_action_2026/REPORT.md`. Baryonic
Newtonian gravity is unsmoothed. No covariant completion is claimed.

Two independent numerical assertions: (1) differentiating the reduced
nonlinear action for two Gaussian-filtered point sources reproduces the
predicted compact-pair force, with momentum conservation and mass-ratio
controls; (2) spectral derivatives of the external-field linear pair
potential approach the three-frequency identity derived in the report.
The calculations may falsify either proposed asymptote.

Use G=a0=xi=1 in nonlinear quadrature; total mass is epsilon. Gaussian
source-filter width is one, not an extra softening of Newtonian gravity.
COM positions are x1=-(1-f)d e and x2=f d e, masses f M and (1-f)M.
The relative coordinate is x2-x1. Subtract the constant external flux before
integrating the internal force. Fixed-total-mass energy differences are used
in isolation, not two separate logarithmically divergent self energies.

Domain: compact pairs d/xi<=0.3 for core tests; isolated filtered deep field
for the square-root-mass asymptote. The frequency identity additionally needs
linear response about a constant nonzero external Newtonian gradient,
isotropic filtering and near-circular equatorial orbits of small inclination.
Nonlinear external-field response, unequal masses and finite oscillation
amplitudes can violate that identity and must not be silently discarded.

Float64 Gauss-Legendre quadrature, exact SymPy identities, deterministic
inputs, no fitted constants. Resolution studies and finite-difference action
checks are required. Anisotropy or finite separation can invalidate an
asymptote without invalidating the parent action. Finite agreement is not a
continuum error certificate. No observed orbital frequencies or catalogue
likelihoods are supplied; empirical significance and priority remain OPEN.
Scripts must exit nonzero if their declared checks fail, and record all
input bounds, software versions, hashes and actual results.
