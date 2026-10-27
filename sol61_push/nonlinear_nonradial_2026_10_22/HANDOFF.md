# NS-20261022 continuation handoff

Base c9039eccdcc6949c19b77e01b8025c630fceda51; predecessor nonradial_transport_2026_10_22. Original goal OPEN. Own directory only; no commit/push, manuscript edits, delegation or newly initialized ledger.

Read RESULT.md, DERIVATION.md and AUDIT.md first. Final numeric repeats are in verify_run/result.json and finalcheck_run/result.json.

New durable results:
- Exact nonlinear logarithmic P-field solver in3D using convex dual; no guessed pairwise saturation. Matched compact sources break quadratic mass similarity by54.6% initially and53.3% on refinement.
- Gaussian radius support across masses0.5,1,2,4Mstar; radius extrema repeat within1.78% in grid and0.144% in box. Widths at finest fixed box are0.2757,0.3263,0.3879,0.4612ell0. These are Gaussian widths, not earlier core-boundary radii.
- Restricted triaxial affine dynamics with spin reaches a nonlinear rebound for4Mstar; time/grid repeats check bulk axes. No fragments, ejection, radiation or evolving baryons; no final selected mass follows from fixed inventory.
- Energy/M decreases across restricted supported profiles; their separated half-mass pairs cost energy. General passive stationary no-interior-mass-minimum identity does not require spherical symmetry and survives saturation. It does not exclude dynamical mass selection.
- Exact quasistatic phase elimination adds nonlocal quartic dual. Probes include phase gradient, but heavy phase excess changes25.3% on doubling box, failing5% gate. No finite-inertia radiation simulated.
- Unpumped homogeneous linear response is unchanged to first order. No joint dwarf/rotation/cluster/growth test or covariant cosmology is supplied.

Known limitations/failures:
- Original static run serialization failed; rerun retained with only JSON scalar fix. One weak-source residual1.25e-5 fails declared1e-5 gate.
- Six initial affine cases hit resolution guard. Later heavy runs extend only that case; do not claim converged endpoints for all masses/spins.
- Restricted Gaussian kinetic/shape model and finite box are not a full kinetic matter calculation. Three evolving widths cannot fragment.
- Fixed-χ well energies are not lower bounds for arbitrary relaxed-phase fragments. Energy exclusions apply only to the stated endpoint profiles and energy budgets.

Routes and dispositions:
1. Saturation breaking scaling: resolved within quasistatic source regime; nonlinear radius/rebound supported. Do not repeat quadratic mass scans as a selector.
2. Passive binding selecting mass: excluded on the declared differentiable stationary branch, including arbitrary shapes. Dynamic selection remains OPEN.
3. Full nonradial partition with live fields: OPEN, deferred at this checkpoint. Needs kinetic closure through crossings, spatial fragmentation degrees, reciprocal baryon response, exterior radiation/charge accounting and phase-domain convergence. Resume by constructing that missing matter/field model rather than interpreting affine rebound as fragmentation.
4. Observational preservation: OPEN; needs selected settled profiles and center-of-mass phase-space/abundance before any new fitting claim.

Exact reproduction commands are recorded in each manifest's argv. Validate manifests with computation-audit/scripts/validate_manifest.py MANIFEST --root . . Completed execution does not turn false interpretation gates into passes. CHECKPOINT_SHA256.txt pins final artifacts. No active jobs should remain after final verification.
