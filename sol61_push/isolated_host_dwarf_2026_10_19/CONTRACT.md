# Matched isolated and host dwarf: finite experiment

User-authorized on 19 October 2026. Base checkout `d8611577f599b7919a894c91a15b4ec7a75f0bc8`; pre-existing dirty files are outside this new directory.

## Question and exact model

Does one specified initially diffuse, rotating cold-carrier cloud develop a resolved central concentration in isolation, and how does a prescribed host change its mass, energy and vector angular momentum?

Use the original prepared dilute Phi/X daughter-carrier **Newtonian kinetic reduction**, MASTER_COLD_ENERGY_EQUATIONS.md lines 183–195 and 493–511: collisionless live stars, a cold distribution with elastic C22, and Poisson gravity of the real stellar and cold mass. Use the revised threshold cross section 0.3 cm²/g, u*=0.02, r_lambda=2, with the documented below-resonance velocity dependence. Record the maximum sampled resonance variable. No X sources are initially present, no production calculation is claimed, and no polarization/galaxy-law force is added.

This is an actual specified subsystem, **not the complete canonical polarization framework**. CFG541's profile-deficit settling drift has unassigned energy/J losses and is excluded. CFG654's target-phantom shell draw, CFG747's fixed core, and the distinct ARGON action are excluded. No target density, thermostat, prescribed cold core, cooling drag, reflecting wall or particle deletion enters evolution.

## Scenario inputs, fixed before production runs

- Units pc, Msun, Myr, SI-derived G=0.004498638185693768.
- Stellar mass 574272.9377001019 Msun, the saved CFG853 Draco SFH mass. Cold mass =53.64 times this mass: the historical generous f_ret=0.1 inventory, an assumption rather than measured stock.
- Cold positions: uniform ellipsoid with semiaxes 2000,1600,1200 pc, rotated 37 degrees in xy. Antithetic samples give zero initial centre of mass. This is diffuse initial material, not a selected equilibrium or native cosmological initial condition.
- Live stars: antithetic Plummer positions with scale 193.22 pc and truncation 1500 pc. Stars may already be concentrated; the cold component is not.
- Cold initial 2K/|W_vir|=0.2; ten percent of its kinetic energy is ordered rotation around (1,1,2)/sqrt(6); the random part has its net rotation removed. Stellar velocities have 2K/|W_vir|=1. Both populations have zero bulk velocity in the initial dwarf frame. These are prepared scenario inputs, not inferred distribution functions.
- Host comparison: spherical static Plummer potential with real mass 6e11 Msun, scale 10000 pc. Initial dwarf centre (80000,0,0) pc, tangential speed 0.65 times the local circular speed. The isolated run uses the identical relative particle phase-space arrays.
- Full 3D mutual softened gravity; Plummer epsilon=40 pc. One process/thread, low scheduling priority, no existing run modified. No stars or cold particles are discarded, even after stripping.
- Baseline 2048 equal-mass cold particles and 256 equal-mass stellar particles; 10 Gyr; leapfrog dt=2 Myr in isolation and 0.5 Myr around the host. Check half timestep, doubled particle count, and smaller collision support; collisionless controls distinguish C22 from gravity. Individual experiments may be shortened only as explicitly labelled timing/validation pilots.
- Central-impulse finite-support scattering kernel h=200 pc preserves pair energy, momentum and angular momentum. Incoming-angle weighting reproduces the isotropic contact differential kernel in a locally uniform gas. Finite support, particle noise and finite timestep require checks; this is not an exact continuum Boltzmann solution.

## Measurements and conservation

Record every 100 Myr: cold M(<100,300,1000 pc), half-mass radius, radial cumulative profile, shell densities, central stellar velocities, all particle positions/velocities at initial/final epochs, and fixed initial/final-core membership budgets. Use a stellar shrinking-sphere centre; also report its offset from the total centre of mass.

For all original dwarf members, E=K+U_self+U_host, E_int=K_COM-frame+U_self, and E_orb=M V_COM²/2. Use half of cross-population potential in each species' energy account. Record all three components of J_int, J_orb and their sum. Accumulate host work and torque separately in the same integrator. A fixed host is a prescribed external source: it has no evolved response or newly measured absorbed heat. No radiative energy channel exists in this elastic reduction.

At every kick accumulate the host torque about the origin and about the dwarf COM. Track host work into internal and orbital motion. Log collision changes of K and vector J directly. Normalize numerical energy errors by initial **dwarf internal binding**, not the much larger orbital host binding; normalize torque closure by M R_cloud sigma, not near-zero net spin.

Report final-core, outer and stellar energy/J shares, distinguishing fixed membership transfer from material entering/leaving an aperture. Changing aperture membership is not itself cooling. A compact density peak is not automatically a mass-dominant core, and stellar velocity inflation is not automatically extra bound mass.

## Decision rules and limits

A resolved concentration candidate requires at least 64 cold particles inside 300 pc, M300/Mcold >=0.1, and persistence throughout the final Gyr. A **100-pc core** requires additional radial resolution and density-shape evidence; the 300-pc condition alone is not sufficient. For a physical formation claim require mass-profile stability under timestep and particle refinement (20 percent at resolved radii), energy closure <1 percent of initial internal binding, and explained J flux with negligible numerical collision torque. Report nonconvergence or insufficient resolution as inconclusive, not absence of a core.

The finite experiment can establish behavior for these inputs and numerical scales only. Failure does not exclude other assembly histories, initial spin, abundances, inelastic/coherent physics or the unclosed full theory. A fixed host does not model cold capture from a live host reservoir, gas stripping, feedback or cosmological accretion. Finite-N gravitational relaxation and finite-softening suppression must be distinguished from C22 evolution.

## Numerical pilot refinement, before production

The 1-Gyr Ncold256/Nstar32 pilot passed intrinsic work/torque closure but the host case at dt=2 Myr had maximum total energy error 0.113 times the dwarf's initial internal binding (the error is dominated by the much larger orbital host energy). It failed the 1-percent energy gate. Production host dt is reduced to 0.5 Myr and its half-step check to 0.25 Myr; physical parameters and concentration criteria are unchanged. The coarse pilot is retained and is not scientific formation evidence. Its manifests pin historical code/config hashes; current-file hash validation is required for production runs.
