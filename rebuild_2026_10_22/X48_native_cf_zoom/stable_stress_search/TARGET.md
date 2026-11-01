# Stable nonbarotropic stress target for X48

Checkpoint: X48-STRESS-2026-10-31-A. Base Git revision:
`27fb6233147d29c7ec11ee81c9bbea3a2126afa7` (dirty shared checkout).
The previous exact-gradient pressure audit is in `../gravitational_strain/`.
This search adds a separate candidate; no frozen X48 dynamics or jobs change.

The user requests a stable nonbarotropic stress that is inactive in the
Lyman-alpha forest, supports finite halo cores, resists baryonic contraction,
and uses `P0=a0^2/(8 pi G)` as a stress scale. The user explicitly permits
additional material scales and history variables. The acceleration scale is
an input normalization, not a coefficient derived from a microscopic parent.

## Target and evidence standards

Seek a positive-energy constitutive construction with an exactly stress-free
open domain, positive active acoustic stiffness, finite regular spherical
core equilibria, and quantitative resistance to smooth baryonic loading at
fixed cold mass. Treat the following obligations separately:

1. Conservation and entropy production of the proposed evolution.
2. Local short-wavelength and radial equilibrium stability, with explicit
   treatment of entropy gradients and long-wavelength Jeans growth.
3. Exact inactivity on the defined cold/low-density domain. Identification of
   that domain with the observed forest is an additional empirical test.
4. Finite cores and fixed-mass equilibrium continuation under a smooth,
   finite-depth baryon potential. A Newtonian point mass is a separate limit.
5. Formation from cold initial data and maintenance of a halo envelope.
6. Covariant completion, cosmology, mergers and observations.

Analytic identities and finite equilibrium calculations may settle parts of
1--4. They do not automatically settle 5--6. A single stable equilibrium is
not a halo formation calculation. Resistance means a measured weaker shell
response than a specified pressureless adiabatic reference, not invariant
central density under arbitrarily compact or massive baryons.

## Route portfolio

| Route | Mechanism and discriminator | Disposition at launch |
|---|---|---|
| E | Independent entropy coefficient, shock energy conversion, and a pressure-free density interval with latent memory energy. Differentiate the energy, check acoustic and thermodynamic convexity, continue fixed-mass cores under smooth baryon loading. | Active primary construction. |
| S | History-triggered volumetric and shear elastic hardening. Check objective convex energy and homogeneous spherical contraction before equilibrium calculations. | Independent alternative under analysis. |
| N | Falsify overbroad targets using isotropic collapse for shear-only stress, a singular baryon potential for polytropes, and exact versus empirical forest gates. | Active obstruction route. |

Read-only delegated derivations use this base and have no shared write scope.
The coordinator owns this target, synthesis, numerical equilibrium experiment
and shared status. Later delegated implementation scopes are disjoint.

## Proposed finite experiment

Use a declared constant-entropy equilibrium branch of the selected energy
law, solve spherical Euler-Poisson hydrostatics to its pressure-free boundary,
and preserve cold mass while adding Plummer baryons. Compare the half-mass
radius with circular-orbit shell contraction for the same initial profile.
Check a refined solve and the positive radial pulsation quadratic form.
These dimensionless experiments do not run a production X48 zoom or fit data.

The candidate equations, exact bounds, scripts and run contract must be
written before the bounded evidence run. Preserve unsuccessful constructions
and distinguish proof, conditional analysis and finite numerical evidence.
