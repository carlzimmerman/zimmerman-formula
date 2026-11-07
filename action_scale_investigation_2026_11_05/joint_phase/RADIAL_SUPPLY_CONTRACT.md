# Radial source and energy transport

Base ce5bb4fcd4f019e48c2938a804792d8593d07d15. Continue the same target:
a finite stable flat-rotation halo and coefficient1/2 without calibration.
Use the actual ballistic mediator source J=j exp(-r/l)/r^2. For a trial
inverse-square material tail integrate continuity exactly; include injected
momentum and relative kinetic energy in the fluid moments. Derive the heat flux
needed for a leading isothermal subsonic tail and its finite-boundary budgets.
Check whether conduction with positive conductivity can supply that flux without
large temperature gradients, and whether a no-flow or no-heat-flow interval is
possible. Exact symbolic checks within60 seconds/one thread; preserve a control
omitting source momentum in total energy conservation. No global PDE stability,
actual luminosity or unconstrained fitted normalization. Only this investigation
changes; push verified results on the existing branch.
