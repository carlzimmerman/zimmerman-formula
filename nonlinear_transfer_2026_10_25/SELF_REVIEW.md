# Internal claim review

Performed by the implementing primary agent; no independent referee or agent
review is implied. All load-bearing numerical evidence has a bounded-run
contract and source/output manifest. The summary plot reads recorded results.

* Scope checked: one spherical Plummer benchmark, not real-data population
  validation. The user requested all conditions jointly; only local
  preservation, not formation, has passed those tests.
* Force conventions checked: canonical connection, alignment conversion,
  positive edge gradient, scalar source and density-inertia derivative are
  retained. ACTION_CANONICAL is authoritative; earlier conventions have an
  explicit erratum. Carrier angle is unwrapped during evolution.
* Static force check: earlier optimizer success alone was insufficient.
  run_exact_equilibrium is the force-finished preparation. The Hessian claim
  is restricted to its constrained active radial real space.
* Numerical branch checked: accepted u<.9997 uses the exact response, not the
  old u=.98 continuation. Trial continuation above.9999 is not an accepted
  physical branch. Stable tail series evaluates the same potential.
* Transfer checked: no optimizer decrease, rejection, or energy defect is
  counted as escaped power. Work, fixed500kpc flux, outer wave storage and
  absorber energy are separate. Wave-domain comparisons use common radius.
* Convergence checked: the30Myr infall has dt-halving and wave-grid/domain
  controls. The100Myr preservation tests and material spatial continuum do
  not have a full convergence certificate; no global stability claim follows.
* F outlet checked: the local pressure/gradient ledger closes, but positive
  raw flux includes bound-mass advection. Reference subtraction does not
  produce a missing positive cooling channel in this window. It is not a
  theorem ruling out future or nonradial reservoir energy transport.
* Limitations checked: early pilots, cap-limited zero-inertia comparisons,
  numerical minimum-step failures and wall-limited runs are not successful
  full formation trajectories. No late-time impossibility theorem is claimed.
* Success threshold checked: subpercent law preservation and restoring
  boundary response for small disturbances do not certify an attractor from
  all F. The nonlinear compression continuation is explicitly changed physics.

See MANIFEST_AUDIT for current input validation and HANDOFF for routing.
