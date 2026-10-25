# Better molecular spectrum and nonequilibrium assembly

**The refined radiative model still does not make a substantial charged molecular
component in the disk proxy.** It gives a useful reduction: within the isolated,
optically thin reaction network, changing density or waiting longer cannot
circumvent a bound set by atomic versus molecular capture rates. No rotating
self-gravitating galaxy or acceleration relation has been demonstrated.

## Spectrum and rates

The same Coulomb parent contains positive heavy X, negative light C, neutral
A=XC and positive molecular ions T=X2C. All leftover countercharges are counted.
At fixed heavy/light mass ratio100, the electronic basis is enlarged systematically
in prolate coordinates. Nuclear bound states and energy-normalized scattering
states then determine the physical electric dipole strengths and radiative rates.
No binding energy, capture radius, forward rate or inverse rate is independently
fitted to galaxy labels.

- At R=2 a_D the electronic ground potential is -0.602634214494 E_H at the
  largest checked basis. The previous two-orbital well depth was only .06483 E_H.
- The refined ground molecular dissociation energy is **.08099565 E_H**, versus
  .04810609 previously. There are **23 bound (v,J) levels**, versus15 previously.
  The nuclear domain120 to240 a_D preserves the count. No u,J=0 bound level is
  found in these domains; higher J adds a positive centrifugal potential.
- Halving the radial step .02 to .01 and doubling continuum energy samples
  changes the total formation rate by at most **0.023%** over T=1e-7 to .08 E_H.
  Changing the electronic order, tail join and scattering match together changes
  it by at most **0.008%**; this combined test is not an independent error budget.
- An independent finite-box normalization agrees with the ground-channel
  scattering dipole strength to **0.077%** at four tested positive energies.
  These checks do not bound every narrow resonance or all physical corrections.
- The small basis fails at R=120: a tiny algebraic eigen-residual does not prove
  physical convergence. Curves are used through R=40, followed by the hydrogenic
  polarization tail with a continuity-matched higher-order term. R=32 is tested.

This supersedes numerical spectrum-dependent conclusions of the old LCAO parent;
it does not change its archived inputs. Born-Oppenheimer, finite-mass, nuclear
spin/exchange and relativistic uncertainties remain. At alpha=.15/.2, characteristic
uncomputed relativistic corrections are of order2.25%/4%, larger than grid errors.

## Actual finite-age assembly, with explicit photon energy

Each bound level has its own population. Starting from ionized X and C, evolve
X+C -> A+photon and A+X -> T_b+photon for10 Gyr. Thermal energy changes by the
incident kinetic energy of each reaction; emitted binding plus kinetic energy
enters an explicit escaped-radiation ledger. Temperature evolves with the particle
count. There is no imposed thermal equilibrium, ground-state relaxation or thermostat.
The same dipole determines photodissociation; thermal Milne reciprocity is checked.
The parcel itself has no incoming radiation and assumes outgoing photons escape.

The four profiles are the previous two dwarf, disk and cluster **mass/radius
proxies**, using common microphysics and a common ionized initial condition.
There is no galaxy-type conditional in the equations. There is also no rotation,
live gravity, spatial transport, predicted morphology or demonstrated tether orbit.
A charged molecule is a candidate carrier, not an established galactic tether.

The initial39 common parameter choices, 156 trajectories, all fail at least one
shared applicability screen. In particular, photon opacity invalidates free escape
throughout that mass range. They are not physical formation predictions.
An18-point extension to larger constituent mass yields12 common choices passing
the stated weak-plasma, classical, dilution, temperature and optical-depth screens.
**None meets the inherited80% disk / <=20% others molecular-mass screen.**

The largest disk fraction among these12 occurs at shared alpha=.15 and light
mass3.16228e8 eV (mass ratio100):

| Input profile | Charged molecular mass fraction after10 Gyr |
|---|---:|
| Small dwarf proxy |1.53418e-7|
| Large dwarf proxy |1.19947e-6|
| Disk proxy |**2.91619e-4 = 0.02916%**|
| Cluster proxy |2.23428e-4|

At this point the disk proxy is mostly neutral atoms (atomic count .99823);
the cluster retains bare positive fraction .78233. Non-molecular mass includes
neutral atoms: it must not all be called unbound fundamental matter. Molecular
charge-to-mass is lower than bare X, so this chemistry does not switch repulsion on.

Across all228 main/extension trajectories, maximum energy-ledger error is
2.13e-13 E_H per initial pair (maximum relative initial-energy error3.79e-9);
net-charge error is1.12e-16 charges per pair. Tightening the ODE tolerance100-fold
changes the four fractions at the best eligible point by at most0.00051%.

## A parameter reduction from reaction competition

Write t for molecular count per initial pair and c for free countercharge.
If k_T/k_A<=r over the temperature trajectory, conservation and the two reaction
stoichiometries imply

    t <= r log(1/c),  c >= t,  hence t <= r W(1/r).

Density, common alpha³ normalization and elapsed age cancel. Bounding every
cubic interval of the actual rate interpolant gives, for1e-8<=T<=.05 E_H,
r<=.00582390 and a **charged molecular mass cap4.415%**, at any density and age
within this network. This is much weaker than the actual finite-age results but
still below80%. It rules out rescuing this implemented path merely by tuning
its density or duration. It is a numerical-interpolant bound, not an exact
Coulomb theorem; see [derivation and scope](BOUND.md).

## What remains unresolved

The optically thin boundary is inappropriate for many otherwise interesting
parameters. A coupled photon population with photo-recycling is the next necessary
transport test there. The present kinetic bound does not apply to recycling.
Collisional dissociation, dissociative recombination T+C -> 2A, excited atomic
states, neutral molecules, nuclear spin statistics and nonthermal velocity
structure are also missing. Passing the stated gates does not prove these
omissions are negligible. This is a controlled test of one radiative path,
not a complete physical prediction or a no-go theorem for collective media.

The mass ratio, charge coupling and constituent mass are still hypotheses; none
is derived from first principles. No fit to the galaxy acceleration relation has
been performed. The previous effective critical band has not been derived from
this molecular population.

[Equations and assumptions](KINETICS.md) · [Electronic derivation](ELECTRONIC.md) ·
[Audit](AUDIT.md) · [Handoff](HANDOFF.md) · [Provenance validation](VALIDATION.json)
