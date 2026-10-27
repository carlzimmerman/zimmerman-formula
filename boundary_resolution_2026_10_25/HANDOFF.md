# Handoff — boundary drift controlled in a conditional effective model

## Current result

The working route separates three roles: positive phase volume energy holds
finite radius, negative constant per-T-particle binding favors inward mass,
and weak ordinary material stiffness keeps the transition filled. Narrowing
the phase wall at fixed leading response tension prevents its forces from
spoiling the tested inner law. No target-law penalty or fixed dark density is
used. Total dark mass stays 5.364 Mb and all phase variables remain free.

The effective energy is the inherited compatible response + gravity + F gas +
response-weighted phase barrier/stiffness, plus

    integral r^2 q(B-epsilon rho) dr
    + kappa/2 integral r^2 |grad sqrt(rho)|^2 dr.

Working parameters: beta=4, ell=2.12132034 kpc, K_F=30, C=.95,
B=.001, epsilon=.3, material length=.25 kpc. No interface charge, density
activation gate, completed-square cross coupling or extra area stress enters.
These are new phenomenological feasibility choices, not derived microscopic
constants. Mb=6e10 Msun and baryonic Plummer b=3 kpc are the single tested
baryon template. rM=9.45225971 kpc and Eunit=Mb*a0*rM.

Evidence:

- Wall h=.25, .125, .0625 kpc gives R=56.3185013, 56.3334644,
  56.3368207 kpc. Last difference .00336 kpc, preceding difference .01496.
- Enlarging the free domain 50% changes R by .000452 kpc.
- Doubling core and exterior cells changes R by -.000670 kpc; half-cell wall
  shift changes R by -.000193 kpc. These independent grid checks pass.
- Maximum actual law error on 1.5--50 kpc is .6123%; at 50 kpc about +.2044%.
  It is an approximate match, not an exact identity in the finite-kappa model.
- No empty transition cells; total density monotone from 15 kpc through 1.2 R.
  At h=.125, the old 17--43 kpc gap contains 2.72609642 Mb. Inside 50 kpc is
  4.81336638 Mb versus the exact-law budget 4.80157935 Mb.
- Beyond 1.2 R, .11470142 Mb remains mobile with T fraction 1.43e-15.
- Both conservative +/-1 kpc joint species displacements return to the same
  boundary at both h=.25 and .125. Largest final discrepancy 1.01e-8 kpc is a
  solver residual, not a claim of physical precision or dynamical timescale.
- Relaxed local radial stiffness ~4.27e-4 Eunit/kpc^2 is positive. The full
  phase Hessian including endpoint variables is positive on the active
  fixed-mass radial tangent; active material cells have m>1e-8 Mb. Endpoint
  and force tests, not a coarse Hessian alone, support this result.
- Full-Hessian finite-difference relative error <=2.49e-7. Local species
  potentials agree with independent differences to 2.56e-11. The all-F seed
  coefficient is independently checked and positive in the outer reservoir
  on this candidate density; independent formation has NOT been simulated.

Final extraction/figure: `run_report_checked/results.json` and
`run_report_checked/boundary_result.png`. Interpretation and complete run
ledger: `README.md`. All force derivations: `DERIVATION.md`.

## Preserve the implementation and evidence

Working class `LatentStiff` in `latent_stiff.py` inherits the grid from Compact,
the constant B/epsilon terms from Latent, and the fully rebuilt equivalent
energy from SmoothLatent. `latent_smooth.py` deliberately bypasses old density
gates, supplied-charge capacity and extra surface/cross terms. It uses
rho^(5/3)*abs(cos(pi*x/2))^(10/3) for the F gas so its AD Hessian is finite at
pure T. Calling a different parent's energy may silently reintroduce a rejected
interaction. `latent_verify.model(h,domain)` is the working constructor.

Raw metadata caveat: the inherited `model` string says "no ... extra stiffness"
and `density_stiffness_length_kpc` is 0 because the parent L is disabled. The
actual subclass adds material stiffness and reports `material_length_kpc=.25`.
These raw files are retained unchanged. See `MODEL_METADATA_CORRECTION.json`.
The code and the complete force audit include the added stiffness; it is never
legitimate to infer a cold zero-stiffness bulk-law proof from the old label.

The final postprocessed Hessians are in each run's aggregate `results.json`;
force-only raw checkpoint files are written before those fields are attached.
BR-24 stops on this distinction. BR-26 retrieves the correct aggregate records.
Do not fabricate missing checkpoint Hessians or modify their recorded hashes.

Mesh transfers MUST use actual old and new edges reconstructed from their
midpoints, as in `surface_checked.transfer_species`. The earlier quadratic-grid
transfer is invalid on these grids. `joint_recovery.moved` conservatively moves
both species and then frees them; it does not pin the new boundary.

Use `fast_complete.finish`. Its active mass set includes microscopic cells
with negative KKT forces, and its phase set includes tail variables. Earlier
fast_solve/fast_finish/fast_active variants have explicit known omissions.
Optimizer energy stopping is insufficient: inspect density KKT, projected
phase gradient, cap and mass constraint before interpreting a trial. Negative
endpoint Hessian directions can be missed by a zero first derivative; test
phase curvatures/full phase Hessian too.

All 26 manifests are validated in `MANIFEST_AUDIT.json`. They include numerical
failures and timeouts; a valid record is not evidence that its physics passed.
Never edit a hashed input or result. Add a distinct script, contract and fresh
output directory for changed models, solvers or corrections. BR-20/21/25 used
600-second limits; other trials 300 seconds, with one thread. No jobs remain
running from this investigation.

## Do not repeat these routes as if untested

- Coarse-grid positive local wall Hessian without refinement and finite joint
  recovery. The manufactured response-wall force error reached 86.7% on n 96.
- Unweighted area stress alone: finite radius but insufficient inward mass.
- Density-gated chemical binding: overshoots chemical potential in activation
  band; sub-percent apparent law can hide lower-energy neighboring walls.
- Stiffness of that same density-activation field: supports an unwanted shell.
- Global/coupled material stiffness alone: material support versus bulk-law
  error, with boundary still free to drift if no independent restoring term.
- Constant volume cost alone: B=.001 retains a cavity; B=.003 fills it but
  shrinks the boundary and gives poor law. It needs independent weak support.
- Modifying force after minimization or imposing the target density: not an
  equilibrium construction. The new working model does neither.
- Treating timeouts, active-set bugs or nonfinite AD Hessians as physical no-go
  results. Their scripts and logs are retained in the run ledger.

The immutable earlier material_interface and transition_force directories were
already pushed in commit 436a05d71e2632c61e52a50dfa6f6ad5c833b0f8 on the separate
branch codex/interface-transition-research-2026-10-24. This directory and later
redistribution/gradient investigations remain local. No unrelated files or Git
index state were changed during this turn.

## What remains unproved

The boundary-drift question has a conditional numerical answer in the tested
spherical system. It is not a completed fundamental theory. To promote it,
derive a physical source and thermodynamic receiver for epsilon, B and kappa;
then test multiple baryon masses/profiles with common physical coefficients,
actual formation with energy accounting, and nonspherical/dynamical stability.
The exact cold law is the zero-material-force pure-T limit; finite kappa and
small inner F admixture leave the measured ~.61% residual here. Do not erase
that residual or claim the law extends through the entire outer wall or to
infinity. A finite mass reservoir cannot sustain that asymptotic law to infinity.

Scaling matters: a fixed dimensionless epsilon corresponds to specific binding
energy epsilon*a0*rM, which depends on Mb. It is not automatically a universal
particle binding constant. B multiplies energy per volume, whereas model.B is
also the Python name of the mass quadrature matrix; use `volume_cost` for the
phase coefficient. Preserve those units and distinctions in future work.
