# Full nonlinear fields: preservation supported, formation not solved

Read STATUS.md and ACTION_CANONICAL.md. Use the latter's corrected force
conventions rather than the earlier ambiguous ACTION display. Development
contract text is clarified in CONTRACT_ERRATUM.md. All frozen evidence remains
unchanged. Parent: front_dynamics_2026_10_25/HANDOFF.md.

The exact constant-current model now has genuinely free densities, common and
relative material phases, independent finite-inertia carrier, moving material
boundary and reciprocal scalar waves. It retains the inertia-density force,
positive material gradients and all spatial connection effects. There is no
assigned infall-to-wave efficiency. The actual source is g1 Gamma.

Keep these results separate:

* Force-finished actual benchmark: law error0.7094%, filled transition,
  R56.3437kpc, density KKT3.07e-7. The earlier stable L-BFGS state was not
  chemically converged; run_exact_equilibrium fixes that.
* Active radial restoring Schur complement: k=.00041127513Eunit/kpc²,
  after relaxing density and both real phase fields at fixed mass. Not a
  continuum/global/nonradial theorem.
* Released boundary disturbances +/-0.5kpc complete100Myr, preserve the law
  at about0.71%, filled transition and predominantly F exterior, and exhibit
  restoring oscillations. They are not completely settled attractors.
* True20% core dilation has actual scalar work and converged500kpc flux.
  By30Myr only0.2425% of initial excess energy has passed that sphere;
  law error17.3293%, density rebound1.9711. Time halving and wave-grid/domain
  controls agree. This is not adequate cooling in that window, nor a late-time
  no-go. Full long runs become stiff; the zero-inertia comparison hits the cap
  near69.89Myr. Do not identify that comparison with finite-carrier evolution.
* All-F seeds convert small structures and emit waves but do not form the law.

The original source-grid bound from FD was not converged. Do not promote it
to a theorem against all bulk or nonlinear transfer. Conversely, actual
nonlinear feedback being allowed does not imply adequate transfer.

## Existing F outlet checked after the main STATUS

run_reservoir_flux repeats the verified fine-time infall with an explicit
F internal+gradient energy balance outside100.756kpc. Its boundary flux,
gravity work and alignment work close to2.36e-13Eunit. Raw outward energy
flux9.41011e-6 accompanies F mass flux-2.54358e-5Mb. With benchmark chemical
potential-.3934501, reference-subtracted excitation flux is-5.97612e-7.
This does not establish positive outgoing sound/wind cooling in this window.
Neither quantity is a general unbound gravitational escape invariant.
See run_reservoir_interpret/results.json for exact scope. Nonradial and later
reservoir transport remain outside this test.

## Current continuation

compression_current_2026_10_25 derives and tests a density-weighted current
that does have a pure-T compression source. This is changed EFT physics,
not a consequence already established by the formula. Its force audit passes,
but its actual early partial runs do not repair the law. Added inertia,
consistent fast-sector kinetics, resolved escaping spectrum and actual
nonlinear cascade are the remaining issues. Read that phase's HANDOFF.

The summary figure is evidence_summary.png/pdf; make_summary_figure.py plots
recorded results only. ARTIFACT_INDEX.json and MANIFEST_AUDIT.json identify
inputs and evidence. Use fresh output folders for reproductions, e.g.

    python3 physical_completion_2026_10_25/launch.py nonlinear_transfer_2026_10_25/flux_infall_fine_contract.json NEW_INFLOW nonlinear_transfer_2026_10_25/flux_infall_fine.py 300
    python3 physical_completion_2026_10_25/launch.py nonlinear_transfer_2026_10_25/restoring_contract.json NEW_STIFFNESS nonlinear_transfer_2026_10_25/restoring_audit.py 300

This phase has no new real-data or universal-population result. All files are
local; no index, unrelated work, commit or remote was changed. Observed initial
HEAD b5e95b9c9e84fc745e8cef6a18cffe71b584c75f. Manifests record their own HEAD
and source hashes because concurrent work may advance it.
