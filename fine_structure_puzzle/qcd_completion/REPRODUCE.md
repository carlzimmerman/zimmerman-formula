# Reproducing FSP-004 evidence

Every executable mathematical run has a pre-execution JSON contract and an immutable v2 manifest recording its exact argv, software, enforced resource bounds, input hashes and output hashes. Read the run status before using the result. A validated launch-failed record is not a successful mathematical calculation.

The current contact calculation can be checked without execution:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_completion/anomaly_contact/run-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

For a fresh execution, use the bounded runner with the same contract and execution artifacts and a NEW output directory; change both its --result argument and the child script's --output argument to that directory. Never reuse a run directory or alter the executed contract/script to improve an old result. The exact original command is recorded in the manifest. The installed runner is beside the validator above as run_experiment.py; --help documents its options.

Route-specific instructions and scientific assertions:

- `angular_modes/REPORT.md`, contracts and `runs/angular-003/manifest.json`: exact ghost operator/determinants plus independent matrix-ODE checks.
- `angular_modes/transverse_followup/`: full Cartesian vector operator, self-dual intertwiner, mixed-wall finite determinant, and separate asymptotic calculations. Use the current completed records named in its report and phase checkpoint, not superseded exploratory runs.
- `closed_dual_qcd/REPRODUCE.md`: compact topology sums, S3 determinant/metric derivative, Coulomb cancellation and matching sensitivities. Its microscopic stiffness identification has a separate correction in `normalization_bridge/REPORT.md`; the finite computations are in independently declared effective parameters.
- `vacuum_matching/REPORT.md`, `runs/matching-002/manifest.json` and `runs/screened-001/manifest.json`: primary-source algebra/GPY integrals and the screened exterior. These do not independently recompute the published all-mode caloron Green function.
- `anomaly_contact/contract.json` and `run-001/manifest.json`: canonical normalized flux/singlet identities. The gauge-group measure is established by source/hand derivation, not by inserting it into a numerical sum.
- `reviews/contact/`, `reviews/vector/` and `reviews/neutral_matching/`: independent derivations and review coverage. An exact algebra audit and an independently repeated numerical ODE are different checks; reports identify which was done.
- `normalization_bridge/` and `reviews/kernel_rank/`: primary-source/analytic proofs with separate source and input receipts. No numerical assertion count substitutes for these arguments.
- `higher_angular/REPORT.md`, `runs/general-j-001/manifest.json` and `runs/exterior-001/manifest.json`: fixed-J angular algebra and exact exterior resummation. Finite exact checks support, but do not replace, the universal-J derivations. The full uniform core connection and joint UV sum remain open.
- `far_field/` and `reviews/far_field/ADJUDICATION.md`: the original `bulk-002` checks the strict-3D/harmonic-first tower prescription. The independent `pv-001` algebra checks the finite four-dimensional electric matching term missing from that initial interpretation. Read the dated correction as well as the preserved original raw derivation; a validated original run does not resolve an untested regulator interchange.
- `reviews/regulator_adjudication/SCOPED_VERDICT_v1.md`: a third independent analytic PV, dimensional and local oscillator derivation, saved before target reads. No executable experiment is claimed for this lane.

Full primary PDFs/text remain in the local temporary paths recorded in source receipts, not in tracked programme files. Exact version, content hash and formula locator authenticate the used source; a future clone must reacquire those exact bytes or explicitly re-audit a changed source. An unavailable original theorem remains conditional unless another checked primary proof supplies the exact required arrow.

`reviews/VALIDATION_001.json` is an intermediate observation while workers were active. The assessed checkpoint names the final current records. Likewise `reviews/ANCESTOR_FRESHNESS_001.json` is preserved as a path-resolution error in the verifier; `ANCESTOR_FRESHNESS_002.json` correctly resolves the historical inventory relative to the programme and verifies all 441 non-navigation ancestors unchanged. No physics verdict depends on the erroneous first check.

Final records are in `reviews/MANIFEST_VALIDATION.json`, with 26 executable
records validated and their real statuses retained. CHECKPOINT.json selects
18 current completed records; the other completed angular run is superseded.
`reviews/INPUT_FRESHNESS.json` rechecks the 441 ancestors, and
`reviews/LOCAL_INVENTORY_FRESHNESS.json` checks the five frozen lane inventories.
The two far-field correction notices postdate their original review freeze;
`reviews/far_field/POST_NOTICE_FRESHNESS.json` verifies the notices alone
account for those report hash changes and pins the current bytes.
