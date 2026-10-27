# FR-20261022 final-pass handoff

User requested one final swing before bed. This pass is finished; original theory objective remains OPEN. No further work or automation scheduled. No active runs, commits, pushes, manuscript changes or subagents.

Base f1803b025624a5bf494d76cb13308431128f2634; predecessor nonlinear_nonradial_2026_10_22. Own directory only. Read RESULT.md, DERIVATION.md, AUDIT.md and postcheck_run/result.json.

New evidence:
- Freely moving3D particles with exact logarithmic P, time-dependent finite-inertia χ, reciprocal energy-derived forces, field-only absorber, exact signed local current, no matter damping/removal. Arbitrary particle crossings and spatial fragmentation are allowed. No affine shape restriction.
- Mass1,2,4 runs to18t0=217Myr retain all matter within2ell0 and show no candidate ejecta. Long-link connectivity remains one material group. No persistent bound core catalogue has been established.
- Fourfold mass exports233times the field energy of reference mass at fixed elapsed time. Weak prescribed-history χ source is quadratic in mass, so quartic phase radiation is a plausible diagnostic explanation, not a fitted universal law. Export does not remove cold material charge.
- Real export beats frozen-source control by billions; heavy total absorption repeats within6.4% across particle/grid/box checks. Signed P flux is negative while χ flux is positive; do not count all field response as outgoing radiation.
- Spatial CDF difference0.0579 fails0.05 precision gate. χ flux changes24.5% with box, failing20%. No precision dwarf profile or radiation rate claim.
- Canonical field+matter+sponge angular momentum discrepancy about0.99%; lattice/periodic effects remain. Material spin alone is not the total angular momentum.
- Heavy quiet and mixed-azimuthal perturbed seeds to60t0=724.5Myr retain one extended connected structure and no ejecta candidates. Export is about0.75% of the finite-box initial total-energy magnitude. Late18t0 interval exports only5.91% of the early equal interval; cooling burst weakens. Do not extrapolate the initial rate indefinitely.
- About51–52% final particle kinetic energy remains after subtracting the best affine velocity fit. This is non-affine motion, not a certified temperature or equilibrium pressure.
- Frozen initial particles falsely appear as seven>5%-mass groups at the shortest FoF link. A detector-generated mass function would be spurious. A final-time radius coincidence likewise fails a time-history check.

Observations: no selected remnant mass/distribution, live baryons, dwarf/rotation refit, cluster abundance/lensing or cosmological formation calculation. The unpumped linear kernel is unchanged only in its original perturbative regime.

Route dispositions:
- Full spatial passive mechanism: tested within stated finite range; no mass selection found. Open for physically different initial histories/drive/baryons and longer/converged cosmological evolution, not globally refuted.
- Cooling interpretation: transient export robust qualitatively; exact long-tail flux/profile requires domain and spatial refinement. No permanent-radiation-at-infinity theorem.
- Population prediction: open; a persistent self-bound finder must include nonadditive fields and survive sampling controls. A FoF label is insufficient.

If the user resumes: start from the demonstrated cooling stall and retained active matter, not from an assumed universal remnant or a new repetition of affine collapse. First decide which physical input could change material partition (external supply/drive/baryons/initial phase space), then demand matched nonradial runs and validated binding diagnostics. More of the same mass grid is not automatically a new route.

Reproduction argv and full input/output hashes are in twelve bounded manifests. Validate with computation-audit/scripts/validate_manifest.py MANIFEST --root . . CHECKPOINT_SHA256.txt pins deliverables. False interpretation gates are preserved separately from successful execution.
