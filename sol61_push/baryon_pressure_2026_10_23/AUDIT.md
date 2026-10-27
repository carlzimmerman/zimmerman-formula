# Audit and scope

Primary verdict: **computationally verified only in the stated range** for the accepted numerical diagnostics; **incomplete** for the requested stable, selected bound-core population and observational preservation. Review is self-review, not an independent solver or reviewer.

## Dependency chain

Inherited preferred-frame action -> ideal-gas material extension -> local Compton source with fixed electron fraction -> radial numerical evolution -> resolution/work/positivity checks -> candidate structure -> full-action binding -> selected masses/population -> dwarf/rotation/growth/lensing tests. Only the first numerical/structural links are addressed. Primordial gas/field/metric initial conditions and chemical abundances remain assumptions.

## Checks and retained failed routes

- Preliminary barotropic force finite differences converge under step refinement; final errors5.18e-8 and1.91e-8. Explicit thermal work agrees within1.54e-13. Uniform-pressure forces are below1e-13. Mean-temperature interpolation and no-Compton A^-2 limit pass. These validate the declared closure, not exact gas thermodynamics.
- Both equal-seed barotropic branches stop at gas shell crossing. Their recorded final arrays can include an interrupted trial, so only last completed diagnostic rows are used. No post-crossing mass profile is inferred from those arrays. Initially homogeneous baryons reachz10 without crossing.
- Finite-volume shock test conserves gas mass and energy to roundoff and does not decrease integrated entropy. Homogeneous spherical pressure balance is exact in the test. The shock test is a finite invariant check, not comparison with an independent exact Riemann solution. Its entropy increment is not retained as a scalar (outputnull), but the sign check is retained.
- Original `hydro.py` passes discrete potential-work checks but fails local positivity in strong collapse. At the recorded failing cell, internal energy2.63e-6 has derivative-0.003205, while using the local momentum-consistent gravitational power gives+2.75e-5. The original update removed internal energy spuriously. Its base/fine/time runs are **not** accepted as completed formation evidence.
- Corrected `hydro_v2.py` uses the same centered gravitational acceleration in momentum and energy. The independent source check gives residual6.66e-16 for zero gravity-induced internal-energy change. This forfeits exact finite-grid potential-work matching; the discrepancy is measured instead. No temperature/pressure floor rescues a failed run.
- Base/fine gas runs reachz10 with positive density and pressure and conserve mass to approximately 4.1e-13. Relative full work-plus-heat defects are .001276 and .0006576; halving the timestep barely changes the defect while spatial refinement nearly halves it. This is predominantly a spatial source/flux error, not exact energy conservation. The cold aperture mass agrees to1.04%; the peak does not converge.
- Absolute full-box energy defects at z=10 are2.00e-5 and1.03e-5 in inherited units. They are comparable to the isolated Newtonian candidate binding energy. Therefore the apparently small global relative errors are inadequate for certifying localized binding, even before adding the field-energy/tail obligations.
- The continued nonradiative z=8 run reaches its endpoint but fails the declared .005 work threshold (.01086). Its endpoint is exploratory only. Earlier saved rows can be used with their own accuracy bounds; at z=9.527 the residual is.001022. No late stable-core claim uses the failed endpoint.
- Homogeneous gas control stays homogeneous to~1e-14 and matches the independently integrated mean temperature at z=10 to~1.5e-8 fractionally. This checks background heating/cooling and the expansion convention, not recombination physics.
- Full dynamical linear density/temperature campaign exceeds its300s bound and produces no result. `linear_quasi.py` explicitly eliminates the fast polarization mode algebraically; its result is an approximation, not a successful rerun of the full dynamics. The tolerance repeat agrees to1.27e-11. The old full-field growth deficit is not repaired by this approximation.
- `corrected_check.py` failed only on NumPy-bool JSON serialization; `corrected_check_v2.py` corrects output serialization. Preserve both records. Finite quasistatic determinant identities and inherited G-mass-length-time normalization pass.

- Molecular-rich cooling runs reach z=10 at both resolutions. The continuation stops at the fit-domain boundary near z=8.920; its .0267 work residual also fails. The last saved state is valid before the rejected trial, but the endpoint is not accepted as a precise physical prediction. The earlier z=9.527 row remains a finite diagnostic with its own .00104 residual.
- The smooth-baryon matched-total-mode control uses cold amplitude .05/f_c and zero initial baryonic displacement, matching only first-order total matter displacement. It reaches z=10 with aperture mass 64,422 and peak22.09; it is not a full transfer-function or field-state match.

## Physical exclusions

Residual xe is prescribed and uniform; gas starts neutral with equal-density or homogeneous-baryon sensitivity seeds. Radiation-era expansion, baryon-photon transfer, relative streaming, spatial ionization, molecular abundance evolution, UV background, metals, stellar feedback, rotation, 3D fragmentation and relativistic lensing are absent. Molecular cooling is a fixed-abundance sensitivity with a limited fit range, not a reaction-network solution. Bound-core survival/populations cannot be inferred from a negative Newtonian energy or a chosen fixed aperture.

## Provenance

Every bounded run retains its own code/data hashes, argv, software versions, status and result checks. Process `completed` does not imply physical acceptance. Earlier HYDRO_CONTRACT.md describes the original conservative flux-energy source; DERIVATION.md and this audit explicitly document the corrected local-power source, pinned by each `hydro_v2.py` hash. Cooling metadata is supplemented by COOLING_CONTRACT.md; the code hash fixes the abundance and switch. No historical manifest was rewritten. VALIDATION.txt checks all current input/output hashes, including failed/timeout runs.

## Final review

Self-reviewed the new derivation, result, handoff and source notes for notation, signs, units and claim scope. Routine prose/spacing corrections only; no proof gap was relabeled as a proofreading correction. All new Python files parse. All26 run manifests validate against current input and output hashes, including the serialization failure and the timed-out dynamical linear campaign. This provenance result does not turn failed scientific checks into passes. No independent full-solver validation or observational likelihood test was performed.
