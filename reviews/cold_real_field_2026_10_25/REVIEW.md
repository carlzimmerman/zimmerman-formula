# Self-review and validation

This is a same-author audit, not independent review.

- Differentiating U gives (40x^3-48x+d)x tan(q/2)/2 as implemented.
- The radial face-flux operator is the negative volume-weighted derivative of
  the discrete gradient energy, including the half-cell outer boundary.
- Energy includes 4pi; the compactness integral excludes it, compensated by
  kappa=8pi G D_mass L^2/c^2. Physical masses multiply the energy including4pi
  by D_mass L^3. No double counting of4pi in packing.
- Snapshot reconstruction independently agrees with total and core energies
  within1e-9 relative tolerance for all eight follow-up cases.
- Successful run and follow-up stderr logs are empty. The ledger-sign mutation
  exits unsuccessfully with 'Energy ledger failed 0.123966', as intended.
- All three bounded-run manifests validate (including the expected failed
  mutation). They pin scripts, logs and declared summaries; supplemental
  raw_artifact_hashes.json pins individual case data and snapshots. Compiled
  host-specific executables are omitted from version control and regenerated.
- Preserved finite duration, fixed matter, spherical symmetry, weak metric,
  unrefined formation controls and final-time packing limitations in REPORT.
- No nonradial stability, general-relativistic collapse, cosmological lifetime,
  population selection, exact cold stress mapping, or galaxy-law success is
  inferred. Overlap is a conditional packing obstruction for the tested
  snapshots, not a theorem excluding all dense field states.
- Current benchmark inputs are reused as conditional requirements; this turn
  did not acquire new observations or repeat their correlated-error analysis.
