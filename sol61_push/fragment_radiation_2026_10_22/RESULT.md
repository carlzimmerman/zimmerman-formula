# Nonradial particles, ejecta and field radiation

FR-20261022. This is the final bounded pass requested before the user went to bed. The model now permits unconstrained three-dimensional material motion, separate clumps, crossing streams and escape, with time-dependent nonlinear polarization and phase fields. **The joint core-mass selection and observational explanation is still not established.**

The useful new finding is strongly mass-dependent field-energy export without corresponding material shedding in the matched short runs. It points toward a cooling-time mechanism, not evidence of a selected mass.

## What changed

The previous three-width Gaussian restriction is removed. Each particle has three independent coordinates and velocities. The exact logarithmic W, finite polarization inertia and finite-inertia phase field are evolved reciprocally with the particles. Field velocities alone are damped in an exterior sponge; matter is neither damped nor removed. The initial fields are solved in static equilibrium to avoid interpreting startup ringing as radiation.

This is the full spatial evolution of the **passive cold-matter/P/χ sector** under the declared discretization. It does not include driven X fields, live baryons, expanding cosmology or a completed covariant parent action. The Cartesian particle mesh and periodic gravity require refinement. Spatial freedom does not by itself make a simulation converged.

The discrete particle forces are energy derivatives. Independent tests verify deposition, particle/P/χ gradients, and a signed local field-energy flux identity. The nine preliminary checks pass; short-run energy errors decrease by approximately four when the time step halves. Matter crossings are allowed rather than reflected or merged by an imposed shell rule.

## Matched initial masses: export grows much faster than inventory

All three quiet triaxial seeds use the same geometry, modest spin and field parameters, with initial masses Mstar,2Mstar,4Mstar. Mstar=1.09523e7 solar masses. The matched interval18t0 is217.3Myr.

| Initial mass/Mstar | Absorbed field energy, simulation units | Absorbed/|initial finite-box total energy| | Final fraction inside2ell0 | Far-outward ejecta candidates |
|---:|---:|---:|---:|---:|
| 1 | 3.006e-7 | 0.000401 | 1.000 | 0 |
| 2 | 4.927e-6 | 0.001666 | 1.000 | 0 |
| 4 | 6.999e-5 | 0.006026 | 1.000 | 0 |

The energy-plus-absorption accounting error is below6.1e-8 in these runs. The heavy frozen-source control absorbs only1.34e-14, showing that the measured moving-source export is not ordinary initialization ringing. Particle, grid and box repeats change heavy-cloud absorption by3.5%,6.4% and3.2%, respectively.

Four times the initial mass produces about233 times the absorbed field energy in this finite interval, while the material inventory remains fourfold. The factor is an observed comparison, not a fitted universal law. Relative to initial finite-box total-energy magnitude, the heavy seed loses about15 times the fraction lost by the light seed.

There is a simple structural reason to investigate this trend. In a weak-field expansion with the **same prescribed source trajectory**, h scales linearly with source mass, whereas the phase source h²/2 scales quadratically. Its radiative field amplitude then scales quadratically and its energy flux quartically. The actual runs have different trajectories and include nonlinear polarization, so three mass points do not verify an exact M⁴ law. They do support looking at mass-dependent cooling efficiency and formation time. Faster cooling does not select a mass unless it also determines a reproducible material partition.

## No robust fragment population in the matched interval

At fixed linking distances0.5 and1ell0, all the material belongs to one connected group in each matched run. At0.25ell0, the heavy run's largest group contains99.3%; only tiny groups of individual or few particles sit outside it. These are connectivity statements, not proof of self-binding.

A revealing detector control: the **unevolved frozen seed** is split by the shortest link into seven components each exceeding5% of total mass, even though no physical fragmentation has occurred. At the longer links it is one group. Thus a claim based only on a short-link clump count could manufacture a fragment population from particle sampling. No such count is promoted to a core mass function here.

The candidate-ejecta test requires radius>2.5ell0, outward motion and positive isolated softened Newtonian specific energy. It finds none in the matched interval. This is not a proof that all matter stays bound forever; the potential is time dependent and field contributions can change escape energies. A persistent separated-core census needs substantially more than instantaneous connectivity or escape labels.

## The apparent radius coincidence is not an attractor

At18t0 the light and heavy half-mass radii are nearly equal,0.667 and0.655ell0. Looking only at that snapshot would suggest size regulation. Over the last third of the same runs, however, the light radius ranges0.385–0.667ell0 and the heavy radius0.655–0.905ell0. Their respective means are0.493 and0.813ell0. The clouds are at different phases of an oscillation. A universal radius has not been demonstrated, and a universal mass certainly does not follow.

## Radiation, tails and angular momentum need separate accounting

The signed flux contains P and χ contributions. In the heavy run, integrated χ flux through the control cube is+1.271e-4 while P flux is-9.435e-5. The latter is net inward over this interval. Their sum and the exterior absorber need not agree at finite time because field energy is also stored between the control surface and sponge. Calling all field adjustment outward radiation would be incorrect.

Doubling the box changes the χ control-surface flux by24.5%, failing the predeclared20% flux-repeat gate, even though total absorption changes only3.2%. The phase tail is not quantitatively converged. Final material CDF changes are0.0474 for particle refinement,0.0579 for spatial refinement and0.0170 for the larger box. The spatial CDF repeat narrowly fails the declared0.05 precision gate. Small energy errors therefore do not justify precision density or stellar-dispersion fits.

Material angular momentum can transfer to fields. An instrumented repeat includes canonical orbital and intrinsic field angular momentum and the angular momentum removed by the sponge. Its maximum relative total discrepancy is about0.99%. This is a discretization/boundary diagnostic, not an exact rotational invariant of the Cartesian periodic grid. The instrumented repeat leaves the trajectories and energies unchanged.

## What this means for observations

- Dwarf fits: no persistent selected core mass or converged formed profile. At0.5ell0 the heavy matched seed retains about four times the enclosed mass of the light seed; equal-looking overall sizes would not preserve the same inner gravitational support. A new stellar fit is not certified.
- Rotation curves: the same couplings and conserved total material mass protect neither the inner force nor the time-dependent baryonic response. No live galaxy has been evolved here.
- Clusters: no abundance or distribution of bound moving cores follows from these one-cloud experiments. Neither a lensing profile nor a cluster excess is predicted.
- Growth: the unpumped homogeneous linearization is unchanged by the nonlinear terms, but the simulation is not cosmological. Finite core abundance, averaged phase shifts, outgoing field stress and cosmological transport remain absent. There is no joint growth pass.

The longer and deliberately perturbed runs are recorded in postcheck_run/result.json and the continuation notes. They test whether the short result merely reflects insufficient time or exact seed symmetries. No result from them should be inferred from the three matched snapshots above.


## Final longer and perturbed tests

The quiet heavy seed and a seed with added mixed azimuthal displacements were each evolved to60t0=724.5Myr. Neither reached the matter boundary or field-domain guard. Both retain all material inside2ell0 and have no candidate ejecta. At linking distance0.5ell0 their largest connected groups contain99.9% and100% of the mass. At the shortest link they still have only one component above5%; its fraction is95.4% or95.5%. These are not observed cores; they are the declared finite connectivity diagnostics.

The two seeds export0.7516% and0.7499% of their respective initial total-energy magnitudes. In the quiet run, export during42–60t0 is only5.91% of that during0–18t0. A constant early-time cooling rate extrapolation is therefore contradicted by this run. The energy export weakens substantially as the source evolves.

The final heavy material is extended and dynamically active. After removing the best-fitting affine velocity field, about51.3% of its particle kinetic energy remains; the perturbed seed gives52.0%. This is non-affine motion, not a direct thermodynamic temperature measurement. It illustrates a material energy channel that the previous three-width approximation could not represent. No precise phase-space equilibrium is claimed.

**Final assessment:** a mass-dependent cooling transient is a useful lead; a universal core-mass attractor is unsupported. These initial conditions do not turn a fourfold inventory into a canonical remnant by fragmentation or ejection within the tested interval. This is finite evidence, not a no-go theorem for other initial conditions, longer times, driven fields or baryonic environments. The original dwarf/rotation/cluster/growth explanation remains open. Per the user's final-pass request, no further runs are left active.
