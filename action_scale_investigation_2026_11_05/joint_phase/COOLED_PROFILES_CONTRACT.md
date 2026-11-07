# Coupled cooled profiles and radial stability

Base49261f61f1fab308591dc8c50bf5ccc8abdded98. Solve a CONDITIONAL finite
spherical fluid model with the derived excitation cooling shape, central
regularity, a specified smooth mediator-like source, insulated reflecting
outer material boundary, and freely escaping radiation. A rigid boundary is
an explicit confinement assumption, not a vacuum-wall derivation. Cooling,
conductivity, annihilation and gravity coefficients are model inputs, not fits.
Use dimensionless variables. Source strength variation is not an observational
baryonic-mass fit. rho_DE is not inserted into a coefficient.

Solve the steady five-variable radial boundary problem, then a staggered
finite-volume/finite-difference steady discretization of the time-dependent
number, velocity and temperature equations, including perturbed Poisson gravity.
Compute its radial eigenvalues and refine grids (initial24,48,72 cells; may
extend to96 if convergence requires). Gravity continuation0..8 and source
multipliers0.5,1,2 discriminate stable regimes and normalization dependence.
No rotation, nonspherical perturbations, collisionless kinetic stability,
moving boundary, opacity dynamics or proof of physical parameter viability.

Use deterministic SciPy solves, single-thread, bounded runs up to180 seconds;
require positive n,T, subsonic flow, small steady residual, exact discrete
number budget and convergent reported eigenmodes/profiles. Preserve failed
attempts and input hashes. A negative control disables radiative cooling in
the residual while keeping a cooled solution and must fail stationarity.
Do not edit executed scripts; corrections use new files/runs. Only this
investigation changes; push the checked checkpoint, not a false full-theory claim.
