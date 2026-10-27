# LD-1: joint density, conversion and interface equilibrium

Base revision 2ce8f3c2b80cefac2ac466cbebf3a7391dd6996a. Prior charged-interface
results are inputs, not rerun. Target: a finite restoring interface, a free
outer phase and the original galaxy acceleration law emerging from mobile
mass. Neither the target density nor acceleration is an optimization penalty.

Three distinct obligations/routes: (A) derive the cold-interior force law and
source-contamination condition; (B) minimize one joint gravitational, phase,
charge, tension and free-phase kinetic energy with both density and phase
mobile; (C) falsify any apparent solution by mesh/domain changes, different
law-independent initial densities and boundary displacements. C depends on B.

This first model adds a stipulated free-phase polytropic energy with gamma=5/3
and nonnegative coefficient K. T is cold; F pressure is P_F=K rho_F^gamma.
K is an explicit new closure parameter, not derived by the galaxy formula.
Total available dark mass is 5.364 M_b, held fixed across radial transport
and conversion; neither phase mass is conserved. Supplied interface charge
is conserved as in CI. This is dissipative energy relaxation, not a physical
formation timescale or a net-charge production mechanism.

Large-disk Plummer baryons M_b=6e10,b=3kpc, canonical a0. Radial grid extends
to 2 or 4 times the old supply radius, but does not use old density. Gate C=.95
constant, avoiding target-law kinematics in the optimization. ell=30kpc,
beta20 and1000, response charge k100,120 and tension tau.1,1 from CI. Initial
dark profiles are normalized Plummer shapes of independently chosen sizes.
Outer phase is never pinned. Finite-domain mass accumulation invalidates
an isolated-halo interpretation and triggers domain extension.

Success requires stationarity for BOTH density and phase; q_inner>=.95,
q_outer<=.05 where appreciable mass is present, finite interface, <.05 dex
actual total-gravity error against the original baryonic galaxy law on
.5b..5b, low source contamination, and refinement/displacement confirmation.
Positive finite Hessian alone is not restoration. No success is a real-data
fit, distribution-function proof, or microscopic derivation.

Every force is differentiated from the same energy. Gravity includes dark
self gravity and baryon potential. F pressure enters conversion as well as
transport. The density simplex enforces positive mass and a fixed total, not
a spatial density prior. Floating point, spherical symmetry and prescribed
baryons are explicit limitations. Runs touching the analytic saturation
continuation u>=.98 are invalid for physical interpretation.
