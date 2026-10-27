# Coordinator Schwinger computation

Current code is schwinger_check_v2.py, contract schwinger_contract_v2.json, saved run schwinger_run_002. All 78 finite checks pass; see the bounded manifest for exact argv, versions, caps and hashes. The result compares full positive spectra, corrected eta/F sums and massive Green images, with analytic tail bounds plus declared floating tolerances. These support the hand derivation; they are not a physical QCD calculation or interval certification.

The initial run also completed. Its recorded image-tail bound could round to zero below binary64 range; v2 records a conservative positive floor 1e-280. Its scripts/contract/run remain preserved. No physics formula or tested comparison changed.

From the repository root, repeat with the installed computation-audit run_experiment.py, a new output directory, these three inputs: schwinger_check_v2.py, SCHWINGER_CLAIM.md and ../CONTRACT.md (all paths repository-relative as in the saved manifest). Command:

```sh
python3 fine_structure_puzzle/qcd_prediction/coordinator/schwinger_check_v2.py --output /tmp/fsp3_schwinger_new.json
```

Validate the saved record without rerunning:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/coordinator/schwinger_run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

SOURCES.json records exact primary versions and temporary PDF hashes. Full papers are not copied into this directory. METRIC_RESPONSE.md and SUSCEPTIBILITY_TO_VACUUM.md are analytical work, not extra executed experiments.
