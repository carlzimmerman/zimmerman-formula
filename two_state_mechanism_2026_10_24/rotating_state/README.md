# Rotating dynamical state and conservative energy transport

**The medium now evolves from colliding, rotating wave packets with an explicit
energy-carrying exterior. The tests do not establish disk-selective tethering
or retained free mass in dwarfs and clusters.** The useful result is a constraint:
equal-mass equal-state carriers stay neutral; mass asymmetry can expel lighter
countercharges and produce outward electric support, but it does so without
rotation as well.

## What changed

[Derivation](DERIVATION.md) and [solver](experiment.py) evolve both charged fields
in 3D with their self-gravity, Coulomb interaction, and a common stationary central
baryon potential. Initial conditions are two equal wave packets with incoming
velocities and optional transverse orbital motion. They are not assigned galaxy
classes, disks, tether fractions or equilibrium temperatures.

The equations have no friction or fitted cooling rate. Wave energy and matter
can leave the measured central region and enter the explicitly evolved exterior.
The full Hamiltonian includes both regions and their interactions. This realizes
an energy-transport channel compatible with gravitational cooling; the short
runs do not demonstrate irreversible relaxation or a late-time cooled state.
Photon cooling is not evolved, and no photon luminosity is silently subtracted.
A dipole-radiation estimate is derived separately from the same charge matching.

This still assumes coherent Bose fields. It does not derive coherence from a
mixed quantum state, thermalize the medium, or evolve baryonic cooling. The
baryon potential is static and included in the conserved energy. The periodic
box and Newtonian/electrostatic limit are not a causal isolated galaxy model.

## Reduction from symmetry

Imposing species-exchange symmetry fixes epsilon=m_minus/m_plus=1. When both
species start in the same field state, their equations preserve equality:

psi_plus(t)=psi_minus(t), rho_charge(t)=0, electric_force(t)=0.

This holds during rotation, infall and wave emission, not just linear response.
The simulations reproduce it to roundoff. It rules out repulsive electric
tether formation along this symmetric route. It does not rule out asymmetric
initial states or other microscopic interactions. Equal masses with a small
initial displacement develop some charge separation but no selected support
fraction in these short tests. The sole remaining microscopic mass is still
undetermined; coherence, density and velocities are state assumptions.

## What the asymmetric runs show

Twelve main runs vary h=.5/1, transverse speed0/.5, and three shared conditions:
equal masses and fields; equal masses with a .05 initial displacement of the
negative component; and epsilon=.1 with no displacement. The phase gradients
are mass-weighted so both species have the same prescribed bulk velocities.
All runs last one dimensionless time unit; none is a completed galaxy assembly.

At h=.5, epsilon=.1, in the larger L=24 box:

| Diagnostic | No orbital rotation | With orbital rotation |
|---|---:|---:|
| Change in core mass (total initial dark mass=1) | -.00340 | -.02412 |
| Change in core energy (dimensionless) | -.48427 | -.49471 |
| Positive mass in illustrative electric-support window | 96.43% | 95.02% |
| Mass near outer box edge | .148% | .152% |

Core energy decreases while energy enters the exterior, and the lighter
countercharge spreads. The electric-support window is .5 to1.5 times the inward
gravity projection. **It is not a tether fraction:** it does not establish
stable trajectories, local capture, an internal tether state, or the acceleration
relation. Its large value occurs in both rotating and nonrotating runs, so this
result provides no rotation-specific formation mechanism. With the matched
positive charge-to-mass ratio, loss of countercharge also tends to make positive
self-repulsion cancel positive self-gravity; that alone is not a baryon tether.

Likewise, exterior mass is not automatically escaped or gravitationally bound
free mass. No justified bound-free retention classifier has been derived for
these time-dependent quantum fields. The core/exterior potential-energy split
is an explicit half-self-energy convention, not a unique local energy density.

## Verification and limitations

- All 22 evolution runs completed: 12 main, six timestep/grid checks and four
  box probes (the latter include two repeated reference runs).
- Main scan worst energy error: 2.71e-6 relative to the initial absolute energy
  components. Species-number error: 8.0e-15.
- Core plus exterior energy agrees with total energy within 1.78e-15.
- In the rotating equal-mass displaced-state refinement, dt=.01/.005/.0025
  gives energy errors2.45e-7 /6.13e-8 /1.53e-8. Wavefunction differences fall
  by a factor4, as expected for second-order splitting.
- Independent functional Hamiltonian derivative: 2.42e-11 relative discrepancy;
  forward/backward step return discrepancy: 1.13e-15.
- Enlarging the asymmetric h=.5 box from16 to24 at fixed spacing changes the
  support diagnostic by about .10 percentage point and reduces edge mass from
  approximately1.7% to.15%. This is a sensitivity check, not an infinite-box limit.
- **Spatial convergence of core mass is not established.** In the equal-mass
  rotating check, the sharp spherical core mask gives final mass .7816 on32³
  versus .8097 on48³. Mask quadrature and evolution errors have not been separated.
- Angular momentum is recorded, not assumed exactly conserved: the periodic
  gravitational kernel and Cartesian discretization are not continuously
  rotation invariant. Rotating equal-mass runs drift by about9e-5; some light
  countercharge runs drift as much as.052. These are not validated angular-
  momentum-conserving isolated-halo calculations.

No damping, energy rescaling, or per-step normalization was used. Main and
refinement energy/number checks are sampled every five full steps. The light
species reaches the edge in some runs; periodic re-entry precludes treating
exterior transfer as asymptotic escape. The h=1 unequal-mass runs have about
4.9% mass in the outer region and are especially unsuitable for escape claims.

## One common microscopic mass: mapping audit

h=hbar/[m*sqrt(G*(5.364*M_b)*b)] is computed from the same m for every input.
At m=1e-22 eV/c², h is13.30, .3991, .009408 and .00002304 for the four historical
mass-size inputs. The dimensionless h=.5/1 tests therefore cannot be presented
as those four objects with a common particle mass.

Across482 common mass/epsilon points, none meets both the stated32³-grid
rotation-resolution margin and the nonrelativistic quantum-gradient condition
in all four objects. These are only necessary numerical conditions. This is a
limitation of this grid/test design, **not exclusion of those physical masses**.
A population-separation claim would require a method resolving the common
physical parameters and the full environmental state, with live baryons.

The illustrative coherent dipole estimate at epsilon=.1 gives energy losses
per dynamical time of roughly4.94e-15,4.94e-12,1.40e-8,9.50e-7 for those inputs,
assuming acceleration difference v_vir²/b. It is not a universal bound or an
actual emitted luminosity. In the exact symmetric state the dipole vanishes.
Neither the estimate nor matter-wave transport supplies a derived capture rate.

## Research status

Rotation and conservative energy transport have been added to a specified
mean-field state. A formed, thermally selected, disk-tethered state has not.
The exact symmetric route fails to generate electric tethering; the asymmetric
route shows charge separation without the desired rotation selectivity in the
tested range. Required tether/free populations, cluster retention, and the galaxy
acceleration relation remain unestablished. Adding a tunable cooling coefficient
would conceal rather than resolve these missing physics.

Evidence (all completed, source hashes validated):
- [Main results](run_state/results.json), [manifest](run_state/manifest.json)
- [Refinement](run_refine/results.json), [manifest](run_refine/manifest.json)
- [Hamiltonian and box checks](run_probe/results.json), [manifest](run_probe/manifest.json)

Contracts/manifests retain exact commands, bounds and hashes. Scripts accept
`--output <new.json>`; use the recorded bounded-runner command and a fresh output
directory for provenance-bearing reruns. The refinement adds `--refine`.
No prior code, paper, manuscript or published claim was changed.
