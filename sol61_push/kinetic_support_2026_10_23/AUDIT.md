# Numerical and scope audit

The initial /tmp/ks_probe.json was an unmanifested exploratory BVP execution. Its result is not used as load-bearing evidence; the family/refinement runs reproduce the calculation under bounded, hashed manifests. A copy is retained as exploratory_probe.json. No pre-execution hashes are invented for the probe.

All16 family BVP solves converge in their stated domain; box/tolerance refinement repeats the fiducial solution. No protected-denominator Newton excursion is interpreted as a physical solution. Accepted P values remain well below1. BVP convergence is checked with independent integrated Jeans/virial identities. Finite outer-boundary tails limit the energy-per-mass identity residual, explicitly reported.

Spectrum and spectrum_v2 use the same second variation. The latter adds the analytically required translation test rather than changing the force law. The original negative dipole eigenvalues are retained. An identified translation null direction is projected out only after reporting overlap and unprojected curvature. No exact continuum spectral theorem is claimed from finite matrices.

The growth contract initially inherited overly broad BVP metadata despite executing the archived growth script. Its numbers are retained but not relied on under that label. growth_v2 repeats with an explicit ballistic-displacement assertion and exclusions. This is not a cosmological-growth simulation.

3D dynamics reuse the inherited solver through particle_base.py, with no sponge. All trials commit complete successful states. Failed trial states are not used. The finite periodic box and particle sampling differ from the isolated continuum BVP. Paired particles cancel centroid/momentum sampling error, but do not exactly cancel angular momentum; no total angular-momentum conservation certificate is claimed. Nonradial motion, crossing, live fields and arbitrary particle trajectories are allowed. There is no live baryonic gas or cosmological expansion.

Timesteps use round(end/dt), so endpoint times differ slightly (40.002 versus39.999 in the time repeat). Comparisons must acknowledge that small time mismatch. Shape/radius histories are used rather than treating a single final radius as equilibrium proof. New dynamics_v2 adds only the configurable box size. Periodic-field energy accounting is appropriate to those runs; it is not an isolated energy-at-infinity escape certificate.

The family mass and occupancy parameters are supplied. No fitted galaxy mass, fragment detection threshold, particle deletion, universal mass claim or population normalization is hidden in the solver. All stability evidence is local or finite-time. Observational preservation, abundance, assembly and full coupled cosmological growth remain open.

Final validation: all18 manifests validate against current inputs and outputs and all recorded processes completed. This verifies provenance, not the unproved formation or observational claims. All figure panels were visually inspected. No active experiment remains.
