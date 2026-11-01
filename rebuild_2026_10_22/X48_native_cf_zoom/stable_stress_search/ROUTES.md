# Stress search routes and evidence boundaries

Base checkpoint: X48-STRESS-2026-10-31-A, revision
`27fb6233147d29c7ec11ee81c9bbea3a2126afa7`, dirty shared checkout.
The authorized target and definition of evidence are in `TARGET.md`.

## E1 Independent entropy polytrope

`P=K rho^2`, with initially zero K and positive compressive heating, has an
independent state and positive dense acoustic stiffness. It supports regular
n=1 cores. Its first failed implication is exact inactivity of previously
heated material after dilution: nonzero K gives nonzero pressure at every
positive density. This motivates E2, rather than disproving entropy stresses.

## E2 Latent memory energy and exact quiet interval

Selected construction: `e=K W(rho)`, `P=K rho^2 h`, with W and h defined in
`DERIVATION.md`. W is constant below rho_q, giving zero stress while retaining
the memory energy. It also supplies a convex entropy-volume energy, a positive
active acoustic coefficient, and finite self-bound spherical equilibria.
The radial free-traction argument gives a positive spectral gap under fixed,
smooth baryons. Independent reconstruction found no algebraic error in those
claims, with the stated boundary and perturbation hypotheses.

The current static finite evidence is `static_verification_inner_shells/`:
eight nonzero Plummer loading cases and 32 comparisons of the 1%, 5%, 10%,
and 50% cold-mass shells. All stress-supported shell radii remain larger than
the defined circular-shell dust reference. The first run in
`static_verification_2026_10_31/` predates the added inner-shell checks and
wording corrections; its source hashes are historical and do not validate
the current files. Current conclusions use the later run.

The existing finite checks do not choose rho_q or tau from data. Exact
inactivity in a declared material domain is not an observed forest result.

## E3 Cold spherical formation discriminator

`collapse.py` implements the same pressure and heating in a staggered
Lagrangian radial model. The pressure work and memory source cancel exactly
in its semidiscrete energy, using the explicitly recorded node weights and
potential. No accepted-state projection or entropy reset is allowed.

The initial explicit integrator stepped outside the positive-volume domain
while encountering the stiff viscous gate. The complete failed source and
attempts are preserved in `formation_explicit_failed_snapshot/`; these are
numerical-domain failures, not physical singularity evidence. A diagnosed
domain-rejection regression and sparse implicit Radau integration address
that failure without changing the material law or tau.

`formation_radau_snapshot/` preserves the successful numerical architecture,
its source, contracts, results, logs, and v2 manifests. At tau=0.5, 64 shells
reach t=8; 128 reach t=3.8634 at the declared wall limit. A tighter-tolerance
64-shell run reaches t=1.2. The 5%-mass mean-density peaks agree at approximately
2.398, and accepted energy errors stay below 1.8e-9 in these runs. This is
evidence for heating and radial bounce over the observed interval.

It is not a stable settled halo: K decreases outward, the remnant pulsates,
and no half-central-density crossing is found. The hydrostatic Schwarzschild
criterion cannot be applied as an exact global eigenmode diagnosis of that
moving remnant, but the entropy ordering blocks a claim that stable formation
has been demonstrated. The next discriminator is an entropy-preserving
rearrangement and its energy-admissible equilibrium, followed by an actual
transport or 3D relaxation calculation. An endpoint alone is not that dynamics.

## E4 Entropy endpoint and exact parcel repair

The first continuous proxy admits an aggregate-energy/entropy consistent
finite sphere, but independent review found that interpolation can lower K
within an original parcel. A positive total entropy change does not certify
the local source condition D_tK>=0 for every original parcel. Historical proxy
snapshots and metadata corrections remain explicitly labeled.

Exact parcel mode repairs that defect: K is constant on each original
equal-mass interval, sorting permutes the histogram exactly, and alpha>=1
increases every parcel's entropy. Hydrostatics restarts at each contact with
continuous pressure and radius. The refined finite evidence in
`exact_parcel_endpoint_snapshot/exact_refined/` constructs an energy-consistent
finite endpoint with alpha approximately 1.41932 and stabilizing entropy
contacts. Its unchanged entropy profile resists a specified Plummer load more
than the circular reference. See `ENTROPY_ENDPOINT.md`.

The endpoint consistency obligation is resolved in the measured N64 finite
model. Actual transport, a resolution-independent positive central entropy
bound, and observed forest separation remain open. Resume with a conserving
transport/kinetic model; the endpoint projection is not an evolution law.

## S History-triggered elastic alternative

Pure shear stress fails an exact homogeneous-collapse test: `F=lambda I`
has zero shear at arbitrarily large compression. Density contrast cannot
replace shear in that example. A more serious alternative stores a
turnaround reference volume and adds volumetric hardening after a finite
compression threshold. A polyconvex candidate can be written with

`W(F)=mu/2[tr(F^T F)-3 J^(2/3)] + h_bulk(J)`,

where `mu=alpha P0>0`, `J=det F`, and
`h_bulk=P0[J^-1+2 ln J-J]` for J<1, zero otherwise. Its bulk pressure is
`P0(J^-1-1)_+^2`, and its active acoustic form is positive. This route avoids
the homogeneous blind spot and has no energy jump when activated at F=I.

No spherical equilibrium, global gravitational stability or forest-history
separation has been established for that solid. It remains an open alternative,
deferred while the entropy construction's more immediate formation test is
resolved. No claim of exhaustion or exclusion is made for nonlinear solids.

## N Overbroad endpoint obstructions

An active finite-K rho-squared core in a Newtonian point-mass potential has
`rho~G Mb/(2K r)`. Therefore resistance cannot mean a baryon-independent
finite-density bound under arbitrary compactification. Smooth finite-depth
baryons and a declared comparison range are essential restrictions.

The earlier instantaneous gradient law has wrong-direction pressure forces
in rising fields, singular equilibria, and unbounded local short-wavelength
growth. Its exact audit remains in `../gravitational_strain/`. Reopening that
closure without changing its force mechanism would repeat the obstruction.
