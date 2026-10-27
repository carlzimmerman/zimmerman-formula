# Self-audit scope

This checkpoint is self-reviewed; no independent referee verdict is claimed.
The source paper's Zenodo link was not accessible through the web tool in this
turn. The implemented starting law comes from the repository's preceding
local_capture checkpoint. The 3D closure, fixed reaction range and cross section
are explicit proposals here, not claims about what that paper established.

Checks and distinctions:

- The full vector sum depends on 3D positions. A same-radius/different-shape
  energy test rules out accidental use of only enclosed spherical mass.
- The Gaussian Coulomb quadratic term includes self-energy and the infinite
  exterior. Its derivative is analytic. The higher-order term is finite-box
  quadrature, with its own analytic gradient. Six component finite differences
  test the total tether gradient. A separate one-packet all-space radial integral
  checks normalization and the spherical limit.
- Mesh refinement, box expansion and symmetry perturbations have separate outputs.
  Small force-gradient error alone is not mesh convergence. The tested smooth
  fixtures do not establish convergence for every possible high-z configuration.
- Quasistatic curl-free u is a model assumption. Solving its nonlinear energy
  is not equivalent to minimizing over all fields of the same divergence. This
  potentially consequential distinction is stated in DESIGN and DERIVATION.
- The finite quadrature breaks momentum/rotation symmetry. Measured live seeded-T
  drift is reported rather than projected away. Energy conservation refers to
  the discretized Hamiltonian, not exact conservation of the continuum problem.
- There is no vorticity estimate built from distant neighbors. Actual geometric
  support enforces 0.1kpc. Swept checks prevent an endpoint-only sampler from
  blindly stepping across a narrow encounter; motion and hazard limits have
  interval controls. Curved trajectories and sequential-event rates still have
  finite integration/splitting error.
- Separate tests verify production collide() really changes state while including
  the finite field jump and Q. Its deliberately huge Bernoulli interval is only
  an algebraic fixture and is excluded from live statistics. Two initially seeded
  T trajectories exercise nonzero field transport, also excluded from formation.
- Event bookkeeping is energy/P/L conservative in the stated Newtonian receiver
  closure. The closure omits radiative absorption, recoil and gravity of heat.
- Each mass/size is crossed with f=0,.95, and with shape1,.25 in the main suite.
  Reaction and force functions do not read a profile name/index or rotation label.
  Gaussian width sigma=b is numerical smoothing, not a universal microscopic
  length. Its scale relative to the capture range is a serious unresolved issue.
- The fixed h and cross section differ from the prior expanding-neighbor model;
  removing its vorticity barrier and changing its cooling range also changes the
  physics. Results must not be called a clean comparison of field geometry alone.
- An initially empty field that remains empty can pass energy checks vacuously.
  That is why nonzero-field controls and a forced production capture are separate.
- Few/no events and n=64/128 do not establish local-density or continuum convergence.
  Initial central-density bounds quantify the sampling problem; they do not claim
  32 local partners are a physical threshold for a binary reaction.
- Observed residuals are nonspherical, nonequilibrium radial-force diagnostics,
  not a SPARC fit, equilibrium rotation-curve prediction, or proof that a possible
  continuum completion cannot preserve the RAR.
- Free binding uses the instantaneous Newtonian potential and the assumed 5.364Mb
  reservoir. Neither that reservoir nor observed dwarf/cluster mass requirements
  are derived or fitted here.

Provenance: bounded runner contracts capture exact source inputs and results.
Check each run status, trajectory status, output count, stderr and input hashes;
a schema-valid manifest by itself establishes no physical claim. The independent
analysis consumes completed outputs and their manifests, and does not treat
partial files from ongoing runs as final evidence.

Further interpretation limits: "capture" means F->T conversion here, not a
proved permanent bond to the encountered baryon. T is the field-sourcing state;
no explicit spring endpoint or molecular bound-state spectrum has been derived.
The coefficient quoted in cm²/g multiplies incoming normal flux in a volume
kernel. Averaging that normal flux over isotropic encounter normals gives |v|/4;
therefore its numerical value must not be compared directly with an empirical
isotropic total scattering cross section without matching normalization and
microphysics. No such empirical comparison is made.
