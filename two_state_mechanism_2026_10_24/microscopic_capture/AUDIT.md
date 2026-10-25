# Self-review, 2026-10-24

Primary verdict: **conditional microscopic channel derived and computationally
verified in the stated finite range; requested tether completion incomplete**.
Review is by the implementing agent, not an independent audit.

Claim card: distinguishable X,C with opposite unit gauge charges, minimal
Coulomb interaction, nonrelativistic E1 transitions, ground-state truncation,
degeneracy ratio1, Maxwellian relative velocities; establish spectrum and related
forward/reverse rates, then test a specified fixed-temperature environmental
screen. No arbitrary galaxy switch or capture energy appears in these rates.

Dependency chain: chosen Hamiltonian -> Coulomb spectrum; published continuum
matrix element -> photo cross section; phase-space balance -> inverse cross
section; Maxwell/Planck integrals -> detailed-balance identity; prescribed
density/temperature/time -> finite exposure screen. The prescribed environment
is not a solution of the microscopic or gravitational equations.

| Obligation | Verdict |
|---|---|
| Ground-state hydrogen spectrum and threshold | Checked by the 4-test suite and recorded numeric result |
| Normalization/factors of 2 in inverse rates | Checked by independent thermal balance and speed-space integral |
| Radiative energy | Checked through binding+thermal+escaped-energy ledger; leading NR theory only |
| Rates across micro masses | Analytic scaling plus numerical unit test |
| Discretization | Quadrature cross-check and parcel tolerance refinement |
| Finite screen coverage | Exactly 61 x 31 x 4 profile values, no random sampling |
| Rotation | Common-flow counterfactual invariant; no live morphological evolution |
| Full atomic kinetics | Not addressed: impact ionization, excited states, plasma transport |
| Field completion | Gauge identification refuted; simple scalar route has wrong weak-field force sign |
| Population separation and galaxy acceleration relation | Not established |

Model clarification: the no-annihilation statement in DERIVATION.md assumes
separate conserved X and C species numbers in the chosen minimal theory, not
merely opposite charges or arbitrary distinguishability. They are not a
particle/antiparticle pair of one field. This assumption leaves the implemented
Hamiltonian, spectrum and radiative rates unchanged.

The photo cross section uses the Coulomb continuum (not plane-wave Born final
states). It is leading dipole order; the reduced-mass substitution does not claim
all finite-mass recoil corrections. The largest T/(mu*c²) in the environmental
screen is 2.04721e-4, and alpha_D<=.1. The abundance density uses mX+mC, ignoring
the small binding mass defect at the same leading nonrelativistic order. These
approximations cannot be presented as exact relativistic energy conservation.

The implemented beta vanishes for Tgamma=0 because there are no incoming photons;
that does not mean the microscopic inverse amplitude is zero. The Planck-bath
test evaluates it at nonzero temperature and includes stimulated emission.
Thermal balance itself does not show equilibrium is reached in galaxies.

Only the ground-state radiative channel is computed; the complete Coulomb theory
also permits other transitions. Neither the zero-success scan nor the opacity
screen excludes the full theory. In particular, evolving density/temperature,
different initial distributions or cosmological radiation can change the exposure
ordering. The structural gauge-charge mismatch survives those modifications if
the same U(1) is still identified with the existing positive T-only source field.

Both bounded runs completed with empty stderr and valid manifests. The figure
was inspected visually. Raw inputs of these runs were not edited afterward.
The test-driven cycle initially failed on the absent atomic module; all 4 tests
pass with the completed module. No prior simulation source has been modified.
