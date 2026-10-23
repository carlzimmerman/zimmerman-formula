# Physical support and nonradial dynamics

**Finite, physically supported equilibrium cores exist in a controlled realization of the current action. A perturbed member survives long 3D evolution, but cosmological formation, selected masses and observational preservation are not established.** The supported profile no longer tracks the radial grid as in the preceding collapse runs. Supplying its phase-space distribution remains a substantial new initial-condition assumption.

## 1. Support from the particle action

The continuum particle dynamics admit stationary isotropic distributions f(E). A velocity-space waterbag gives p=K rho^(5/3) without adding a new force or changing an action coupling. K specifies its fine-grained phase-space occupancy. Coupling this distribution to the exact logarithmic polarization and relaxed phase yields sixteen finite spherical equilibria over K=.01,.025,.05,.1 and masses0.5,1,2,4 times1.09523e7Msun. All BVP solves converge; maximum integrated mass discrepancy is4.1e-5 and max|P|=.184. The stationary energy cutoffs are negative.

The fiducial mass1.09523e7Msun, K=.05 equilibrium has half-mass radius approximately0.6975kpc. Enlarging the outer domain from24 to48ell and tightening the mesh/tolerance changes the dimensionless radius from1.58370015 to1.58369898, under one part per million. Independent Jeans and total-virial identities agree to3.0e-6 and5.5e-6 relative across the family. This is an equilibrium resolution result, not a formation result or a new dwarf fit.

## 2. Nonradial stability tests

The density-energy Hessian includes relaxed polarization AND phase response. Radial fixed-mass and nonspherical l2–8 curvatures are positive in the tested discretizations. A bound covers all higher angular orders (l>=6 for this fiducial profile). The small negative l1 curvature decreases from-0.001435 to-0.000304 under refinement and overlaps the analytic translation direction by more than0.999997; the orthogonal dipole complement is positive. The exact isolated translation mode is neutral. These checks support local energetic stability, but are not a rigorous nonlinear Vlasov-field stability theorem.

Live-field 3D particle runs start with a5% canonical triaxial distortion and evolve all coordinates freely. There is no matter damping or field sponge. The supported cloud survives120t0=1.449Gyr, about17.5 reference dynamical times. During the last quarter its half-mass radius stays within roughly0.713–0.736kpc. Maximum relative energy errors across the finite runs are below4.8e-7.

At40t0, halving timestep changes the half-mass radius by0.0047%; quadrupling particle number by0.234%; refining48^3 to64^3 at4096 particles by0.950%; and enlarging the box16 to24ell at fixed cell size by1.362%. Corresponding radial CDF distances are.0039,.0249,.0161,.0264. Thus bulk profiles are considerably better behaved than the preceding collapsing cusp.

Limits matter: the BVP is isolated and continuum, while the 3D dynamics use a periodic box and sampled particles. The innermost0.25ell contains only24 particles in the64^3 endpoint, so a fully resolved central 3D density or precision dwarf profile is not certified. Periodic radiation can return; these are not isolated escape/radiation tests. There are no live baryons, expansion or cosmological initial conditions.

## 3. Formation and mass selection still fail their gates

The same distribution, canonically expanded by1.5 in position and compressed in velocity, does collapse and rebound in3D. But it keeps undergoing large breathing oscillations: in the final quarter of the1.449Gyr run its half-mass radius ranges about0.672–0.959kpc. A conveniently chosen final radius would falsely suggest settling. This test does not establish a stable remnant formed from collapse.

There is also a stronger analytic constraint. Extending the earlier passive virial identity to fixed-occupancy kinetic support gives, along a differentiable isolated stationary branch,

    mu M-E = -(4/3)T-4J-2Z-H+2B-D < 0,
    d(E/M)/dM < 0.

The logarithmic field potential makes2B-D nonpositive. This derivation does not assume spherical symmetry. **Adding this physical support does not create an interior energy-per-mass minimum that selects one mass.** It does not exclude selection by formation, supply, escape or other kinetic constraints. The sixteen numerical equilibria satisfy the identity within9.3e-5 including finite-boundary errors. PROOF_AUDIT.md records the hypotheses and self-review.

At K=.05, supported masses5.48,10.95,21.90,43.81 million Msun have half-mass radii about0.789,0.697,0.623,0.564kpc. These are a family of input masses, not a predicted mass function. A long-lived member can be chosen; its abundance or dwarf occupation cannot be inferred from that choice.

## 4. Cosmology, dwarf fits and rotation curves

A conditional primordial check exposes a new constraint. If the same K=.05 occupancy is supplied homogeneously at recombination, its one-dimensional velocity dispersion is about57km/s at z1100. Its ballistic EdS comoving displacement to z0 is.0883Mpc, over twice the earlier.04038Mpc seed scale. Across K=.01–.1 the displacements are.0395–.1249Mpc. The freely streaming density kernel is nearly unity at k1/Mpc, but strongly altered at the dwarf-seed wave number. This is a diagnostic without gravitational deflection, NOT a full coupled growth forecast or a claimed exclusion. Generating dispersion after collapse avoids this particular primordial assumption, but then the mechanism and its mass dependence remain to be derived.

The previous approximately4.4% quasistatic large-scale growth deficit is not repaired by this calculation. Dwarf fits, rotation curves, cluster populations and lensing have not been refitted or certified. A core with a~0.7kpc half-mass radius redistributes matter inside galaxy scales; preserving total mass or unchanged action parameters does not guarantee the old forces/fits. No cosmological population is introduced by hand.

## Decision and next gate

The physical-support route is now supported by a resolved continuum equilibrium, nonradial energy tests and finite-time 3D survival. The larger goal remains open. The first missing implication is **formation of the required dispersion and a settled mass partition from justified cosmological initial conditions**, with gas and open-boundary energy/matter transport. The current dilation experiment does not supply it. A follow-up must change those formation inputs rather than repeat a near-equilibrium survival run and call it mass selection.

Evidence: DERIVATION.md, PROOF_AUDIT.md, AUDIT.md; analysis/result.json and analysis/summary.png; each bounded run's manifest contains exact argv and hashes. Numerical validation is self-review, not an independent replication. No manuscript edits, commits, publication or scheduled jobs.
