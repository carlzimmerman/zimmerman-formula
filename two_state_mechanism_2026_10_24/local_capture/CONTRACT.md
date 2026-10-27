# Local capture with independent particle transport

Checkpoint LOCAL-CAPTURE-2026-10-24; base Git revision
0fc9bade547ad11b2c1685815cefc82b130fff31. Prior collective-pump result failed.
User authorizes construction and tests, not a claim of established physics.

Main obligation: local collisions can prepare T from initially F, after which
T and F follow different forces and transport independently. Use one law and
global parameter set across all mass/size profiles and initial kinematics.
Do not identify a phase or interaction parameter by an object name.

Three discriminators: (1) exact finite collision energy/momentum/angular-
momentum accounting, including the reverse event; (2) local circulation
measurement versus noisy nonrotating and boosted/rotated controls; (3) live
3D particle transport, formation, free retention and acceleration diagnostics.

Hamiltonian: softened 3D Newtonian pair gravity plus the parent's spherical-
average T field energy W_full. The latter is evaluated about the total center
of mass and differentiated including that center's dependence on every
position. This preserves translation/rotation invariance but is NOT a full
3D polarization-field theory. Numerical softening=.2 initial baryon scale;
repeat selected cases at half softening. T particles feel the field force;
F particles have no individual field charge. A common center-reaction term
appears for all particles from this particular monopole approximation.

A reaction is a local baryon/medium packet encounter. Change only the medium
packet's T/F state at fixed positions. Compute the exact finite field-energy
change Delta. Pay Delta by a central pair impulse, conserving total momentum,
angular momentum and energy. Require incoming normal relative kinetic energy
K >= max(Delta,0)+B. B=beta*C_pair*abs(Delta) is an assumed activation barrier,
not extra energy permanently inserted in the final state. C_pair is the mean
of the local circulation statistic before/after the proposed impulse, making
the barrier symmetric under exact reversal. Negative Delta accelerates the
outgoing pair. No unaccounted radiation or conversion reward is allowed.

Compute circulation from a local affine fit to baryon velocities, with
isotropic ridge regularization, finite-sample curl-noise subtraction and
centered residual dispersion. No global rotation flag enters reactions.
The finite-neighbor estimator and compact neighbor encounter kernel are
numerical coarse-graining assumptions; they are not microscopic cross sections.
Encounter rate=10 sqrt(G rho_b), the same in both directions. Optional baryon
pair cooling uses central restitution .5 and deposits lost kinetic energy in
an explicit receiver Q. This permits dissipative assembly without an energy
leak. No cool/reaction event depends on object name.

Initial conditions: same four numeric masses/scales as the parent, initial
size factor 3, all medium initially F. Baryon rotation input f=0,.95 and
flattening z/x=1,.25 are crossed with every profile. Initial tangential energy
is held fixed; medium velocities start unordered in all cases. Both species
move independently in 3D. Initial baryon radii sample truncated Plummer,
medium radii sample the parent's finite 5.364-baryon-mass reservoir. These
are synthetic initial conditions, not observations or equilibrium galaxies.

Pilot/scan: 32 packets per component, 256 radial quadrature cells (two Gauss
points each), seeds 11 and selected repeats 29, beta=0,4,20, up to 8 initial
dynamical times. Bound individual run budgets; report unfinished cases.
Refine timestep/event interval and packet count separately where informative.
Initial packet mass ratio and finite phase quanta are numerical limitations.

Numerical gates: central-event invariants <1e-10 scaled; independent force
finite differences <1e-4 relative; total-energy error <1e-3 over a trajectory;
momentum/angular momentum drift <1e-8 scaled. Hamiltonian substeps adapt by
energy error, but energy is never projected or corrected after integration.
Reject saturation-domain reaction proposals and refine Hamiltonian steps near
the wall; report an unresolved wall rather than clipping the potential.

Illustrative joint target: rotating systems reach >=95% T and <=.05-dex RAR
residual, while low-rotation systems retain >=90% initial medium as snapshot-
bound F. All profiles receive both kinematics, including counterfactuals.
These thresholds are not measured dwarf/cluster mass requirements. Binding is
instantaneous, not asymptotic. A successful softened monopole calculation
would still require field completion, resolution convergence and real data.
