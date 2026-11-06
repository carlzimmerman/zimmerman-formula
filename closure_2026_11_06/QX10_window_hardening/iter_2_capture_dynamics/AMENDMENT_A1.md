# QX10 iter_2 Amendment A1 (before any iter_2 number): where the time-dependent run starts

Committed before any iter_2 script exists. Kappa = 1/2 FITTED; not theory closed.

The frozen run starts at z_c = 3 from a cold uniform sphere. On the chosen cells the Jeans length at z = 3 is
lambda_J(3) = lambda_0 (Omega_DE(3)/Omega_DE(0))^p ~ 1e-6 lambda_0, i.e. parsecs (C1: about 5 pc). The cold collapse
therefore builds a core of order a parsec, and an explicit Lagrangian code needs time steps of about 1e3 yr there:
about 1e8 steps to reach z = 0. That is not feasible, and the frozen text did not foresee it.

Change, stated now:
- Collapse phase (z = 3 until the core first reaches 10 kpc): not run. For a barotropic fluid (p = K(t) rho^2) the
  equilibrium at given K and retained mass is unique and keeps no memory of how the mass arrived. Cold infall in a
  bound host loses no mass. So this phase only sets the retained mass, which the frozen text already fixes
  (M_d = f_cap R M_b). This is an argument, not a run, and the README will say so.
- Heating phase (graded for D-consistency): the run starts at z_s, the redshift at which lambda_J(z_s)/2 = 10 kpc,
  from the static A equilibrium at K(z_s) in the host. It is evolved explicitly to z = 0 with the frozen code, the frozen
  shell counts (200 / 400), the convergence line and the D-consistency line. If lambda_J(0)/2 < 10 kpc, z_s = 0 and
  the run is trivial (reported).
- The time-dependent run's initial state is checked: at t = z_s with K frozen, it must stay static to 1 % in
  M_d(<R_ref) over 5 sound-crossing times (KA4, new).
Everything else in FROZEN_CRITERIA.md is unchanged.
