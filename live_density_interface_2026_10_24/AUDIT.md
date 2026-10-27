# Numerical and derivation self-audit

## Current superseding audit: LD-17 through LD-19

The final plot exposed grid-scale density combs in the early quadrature.
LD-15 attempted a common gravity/W quadrature but stopped because its cold
test start was over-saturated; LD-16 repaired that start but caught small-u
tail cancellation. Neither failed check is evidence against the mechanism.
LD-17 uses common enclosed-mass quadrature, exact exterior gravity tails,
and the parent's stable W series. Its directional checks at steps1e-4,1e-5,
1e-6 have errors2.06e-9,2.36e-9,3.47e-9. Pure cold bulk curvature is positive
analytically and in the checked finite case. The all-T controls have no empty
inner cells and recover the law to1.8e-8/1.1e-6dex at n64/128.

LD-18 redoes refinement and joint restoration with that corrected action.
The inner law agrees to.000318dex, but errors remain.2318/.3530dex to30/50kpc.
The interpolated boundary44.86755kpc returns to44.86727 after the inward
perturbation but moves to46.12103 after the outward perturbation, with lower
energy. Earlier LD-13 numbers are superseded, not silently overwritten.
Density KKT residuals about.001–.009 preclude an exact equilibrium certificate.
LD-19 rechecks both species' mass-transfer derivatives and the exact all-F
seed Hessian, then renders `current_result.png` from the corrected outputs.

The earlier interpretive notes below remain historical. Their exact controls,
curvatures and figures must not replace the corrected action's results.

The cold-bulk identity follows by differentiating the same W and Newtonian
energy used in the code. Its source is g_b+g_F, not g_b alone. The target law
appears in diagnostics and the independent all-T benchmark only. The grid
extent uses the prior supply radius as a scale; no target enclosed-mass curve
is used for mass initialization, quadrature ownership or optimization. Initial
mass is Plummer-shaped with scale4b, subsequently variable.

The joint energy includes dark self gravity, prescribed baryon potential,
W to infinity, response-dependent phase stiffness, positive barrier, tension,
response-dependent charge and F polytropic energy. No F pressure is added
after minimization. Charge-origin and fluid-closure assumptions are not
microscopic deductions. No observational catalog is newly fitted.

## Numerical hazards found and retained in evidence

* LD-1: softmax suppresses residuals in small mass cells. Reported density
  chemical spread exposes this; several cells also enter the line-search
  saturation continuation and are physically inadmissible.
* LD-2: SLSQP can return success with significant phase residual, and failed
  iterates can violate cap and total mass. Success flag alone is not evidence.
* LD-3: the .97 saturation cap is numerical, not physical. The domain4 state
  hits it and cannot support a material-equilibrium claim. Uniform-grid
  interpolation also did not preserve within-cell density or each species;
  admitted final states can be studied, but the transfer is not a controlled
  restoration test.
* LD-5: linear-in-radius cumulative-mass interpolation to tiny core cells
  produced u about35 at initialization. All three are implementation failures,
  not a physical exclusion. LD-6 fixes volume transfer and tests an exactly
  constant density.
* LD-7: initial feasibility assertion stopped the experiment before any
  minimization. Separate density/phase interpolation did not preserve T mass.
  LD-8 transfers both species in volume, reconstructs q and records any
  explicit initial radial dilation required by subcell saturation resolution.
* Large K puts appreciable gas against the numerical outer edge. Such states
  are confined by the box and are not isolated free-reservoir solutions.

`cap_slack_min` must be read with each model's cap: .97 for LD-2/3 and .9997
for LD-5 onward. The extended exact branch is u<.9999. The inherited
`report.max_u` measures the actual enclosed mass. Do not interpret a cap-active
solution as a prediction at that cap.

LD-1 gradient check error is 5.22e-10; independent gravitational directional
error 1.44e-13. LD-2 direct-mass energy check error is 4.78e-12 and cap Jacobian
absolute directional discrepancy 1.58e-7. These verify implementation
directions, not a whole physical theory or every endpoint limit. Torch 2.8.0
float64 differentiation is used; numpy/scipy versions are in the manifests.

The all-T benchmark gives maximum law errors .00537,.00106,.00141 dex at
n64,128,256. The last two errors are small but not strictly monotonic;
there is no claimed convergence rate or exact finite-grid equality. The
analytic continuum identity is a separate argument. The benchmark's exterior
is converted, so it cannot be sold as the user's requested mechanism.

No independent agent or human review was performed. This is self-review with
directional finite differences, analytic reduction, active-constraint checks,
distinct mesh/domain experiments and preserved numerical failures.
