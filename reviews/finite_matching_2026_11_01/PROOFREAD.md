# Final mathematical prose check

The coordinator checked README.md, ORDER_AND_STATE.md,
CURRENT_PULLBACK_AUDIT.md and HANDOFF.md against the saved finite-order
pressure/current records and the independent derivation reviews.

- X/Xmin uses each scheme's own zero-charge minimum; Q is fixed using the
  inherited one-loop minimum. These two minima are not interchanged.
- Every occurrence of e=.01/.03 denotes a trial coupling; the dimensional
  regulator in derivations is epsilon. Loop factors and squared-mass versus
  mass arguments are stated in the APIs and source dictionary.
- The pressure equations use the theta charge, vacuum-subtracted energy
  and pressure, the positive small-frequency root, and the fixed-charge
  curvature. Zero sound speed is not called small equation-of-state pressure.
- The current is the angular two-derivative coefficient. The radial kinetic
  action, finite-frequency gap and gapless dynamics are not claimed matched.
- Numerical root/step differences are distinguished from perturbative error
  bounds, and no all-orders or all-states conclusion is stated.
- The actual massive-threshold check excludes and separately lists exact
  tree zero modes. The earlier reference-gap diagnostic is not described as
  the smallest gap.

The algebra reviewer separately corrected a forced notation typo in its
scalar-determinant audit: the two bubble vertices are H_theta, not the
second-derivative seagulls H_thetatheta. This does not change any code or
computed result. No scientific correction to the active finite graph,
current, Legendre or pressure code was required by the final cross-reviews.
The initial failed cancellation-normalization assertion remains preserved
with its exact original script and result.
