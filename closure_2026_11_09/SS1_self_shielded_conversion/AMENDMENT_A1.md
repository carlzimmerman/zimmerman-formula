# SS1 AMENDMENT A1 (before any script or number; committed alone)

Criteria b5adc7a90b. Two corrections found while writing the solver, before it ran. No gate, line, constant, halo rule or
label rule changes.

1. **Integrator.** Section 1 said "implicit (backward-Euler, sub-stepped)". The rate per shell is bounded (0 < P_esc <= 1 in
   units of Gamma0), so the system is not stiff and a first-order scheme would cost accuracy at the KA1 level. The radial
   peeling is integrated with classical RK4 at d tau = 0.0025 (1,796 steps to tau 4.49); the convergence check stays as frozen
   (halving the step changes no retained mass by more than 1e-4).

2. **KA2 as frozen cannot hold for the right reason.** In a top-hat sphere the shells inside 0.25 R500 carry the geometric
   factor (R500^2 - r^2), between 0.9375 and 1 of the central value, so they drain at slightly different rates and
   rhobar(<0.25 R500) does not track the central density exactly: the central shell departs from the reduced ODE at the
   percent level by physics, not by code. KA2 becomes: (a) graded, the solver with the geometric factor held at R500^2 for
   every shell (a test switch) on a top-hat sphere reproduces the reduced ODE at x0 1.35, 1.80, 3.20 to 1e-4 (this tests the
   integrator and the rhobar coupling); (b) reported, the true top-hat central shell against the reduced ODE.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
