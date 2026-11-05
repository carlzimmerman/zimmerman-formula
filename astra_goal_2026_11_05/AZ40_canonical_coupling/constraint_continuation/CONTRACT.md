# AZ40 clock constraint and on-shell continuation

Base checkpoint 6a6a3a23a75e5f55dff4d9fcdf53b948b084dab7, following
370846cee6 (mixed block). Owner: this chat. No changes to other action lanes.
Kappa=1/2 FITTED. No action adopted or observational gate inherited.

Target: settle whether zero clock momentum follows from the metric constraints,
and identify which part of the frozen mixed-block energy obstruction survives
imposition of background equations. Full target remains a healthy complete action;
these are explicitly restricted sub-obligations, not substitutes for that goal.

Route C1: derive the scalar quadratic ADM action on the exact P=0,Q=1,
scalar-only flat FRW branch of the independent-clock canonical potential portal.
Take Lstar=0 (the switched stiffness has no ordinary quadratic Hessian at zero),
mu_K>=0, H!=0, nonzero comoving k. Retain lapse, scalar shift, q=delta phi and
sigma=delta tau until constraints are solved. Verify rank, canonical limit,
conserved clock momentum and fixed-momentum Routhian. Reparametrization of a
homogeneous clock is not assumed to remove finite-k perturbations. This does
not establish constraint rank on a charged galaxy or at a switching interface.

Route C2: reconstruct the static Newtonian energy including the longitudinal
Newtonian subtraction, using the canonical scalar with V=C*a(phi)^2, C>0,
a(phi)>0, a_phi nonzero. Compare its Hessian before and after use of the static
scalar equation. Derive an exact sufficient quadratic-energy inequality on
smooth backgrounds and fixed/vanishing perturbation boundaries. Require a
uniform proof of any sign; finite parameter scans are not proofs. A constant
stationary toy source and the sinh portal are special cases, not galaxy fits.

Route C3: follow the nonzero clock momentum through the exactly exponential,
scalar-dominated power-law FRW solution. Reconstruct the time-dependent mode
equation and its long-wavelength leading solutions. This exponential model is
the asymptotic sinh limit, not the exact finite-y dust/sinh branch. Do not
interpret an instantaneous frozen Hamiltonian as a conserved cosmological
energy or establish nonlinear regularity from linear dilution.

Exact checks: direct quadratic ADM expansion; independent lapse/shift/P
elimination; scalar mass identity using background KG/Raychaudhuri; kinetic
rank; Legendre/Routh transforms; exponential cancellation; conformal-time
conversion; derivatives and Schur complements from W; positive-function
factorization of the static second variation; sinh third-derivative ratio.
Negative controls separately reverse induced clock kinetic sign and omit the
on-shell gradient remainder. Both must fail their stated known answers.
No numerical fitting, acceptance tolerances, observational inputs, or heavy jobs.
Symbolic assertions are over real variables in the domains above; logarithms
use s>0. At most60seconds per verification run, one numerical-library thread.

Existing work read: AZ40 MIXED_BLOCK_FINDING; AC1 DERIVATION and exact clock
obstruction; AZC1 ACTION joint convexity; AC2 ACTION and AC3 status. The old
independent-clock caustic counterexample is retained. New sufficient static
energy bounds cannot repair that exact nonlinear branch by themselves.
