# Review checks and reproduction

Original independently bounded commands, already executed once:

    python3 fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/execute_clean.py
    python3 fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/execute_companion.py

Each wrapper creates its fixed fresh run directory and refuses to overwrite an
existing one. They observed all input hashes before/after, used a 20-second
wall timeout and 10-second CPU limit, made no Git call and requested no
RLIMIT_AS. The completed originals are run_clean_001 and run_companion_001.
Their manifests record actual child argv, software, outputs and bounds.

To rerun just the exact mathematical assertions, choose new, nonexistent
result paths inside this review directory and invoke the respective checked
implementation directly:

    python3 -B fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/check_photon_mass_clean.py fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/reproduce_main_fresh.json
    python3 -B fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/check_companion.py fine_structure_puzzle/qcd_nonborn_vacuum/reviews/photon_mass/reproduce_companion_fresh.json

Those direct commands do not create a new bounded v2 record. For a new bounded
record, retain the scientific implementation/notes unchanged, create a fresh
wrapper and contract selecting a new output directory, declare those exact
new provenance files as inputs and validate its observed v2 manifest. Never
overwrite the completed record or mutate its pinned inputs.

Validation command (replace MANIFEST with either completed manifest path):

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula

Saved validation output also covers the author's original manifest. That
validation was not an independent numerical rerun of the HB current functions;
it verifies the frozen original's recorded inputs/results and schema. The
review independently inspected its transformations, source normalization and
finite-range interpretation.
