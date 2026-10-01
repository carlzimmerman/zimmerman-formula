# Norm and family conventions for the endpoint proof

The product H1/L2 norms in ROOT_DERIVATION are mathematical norms after a
fixed positive choice of length and component reference units. Equivalently,
use fixed positive dimension-balancing weights for xi,psi,eta. For example,
choose any L_ref>0 and V_ref>0, express x/L_ref, xi/L_ref,
psi/V_ref² and eta as dimensionless variables, then apply the product norm.
This changes coercivity constants but not positivity or existence of a gap.
No chosen reference units select a measured physical scale or numerical bound.
Use the positive kinetic quadratic form for restoring squared-frequency units.

During endpoint continuation, initial ODE data at the left boundary are held
fixed. Total background mass generally changes with d because rho>0 and
integral_0^d rho grows. Fixed mass means perturbations around each equilibrium
preserve that equilibrium's mass. It does not mean the whole length family
has one fixed total mass. Right-wall field values and pressure are induced by
the same continued background, not held numerically fixed as d changes.

The positive gap and post-turn extension size are existential for the selected
regular background. No quantitative width, observed endpoint calibration or
example outside the old short-domain bound has been computed in this pass.
