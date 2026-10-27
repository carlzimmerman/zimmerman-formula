# FSP-006 reproduction and evidence limits

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. Python and already-installed dependencies suffice. No measured alpha or cosmological data are inputs. No QCD ensemble simulation is claimed.

- `proton_compton/compute_response.py --inputs proton_compton/INPUTS.json --output <fresh-output>` (prefix both input and script by `fine_structure_puzzle/qcd_physical_matching/`) transforms six published points using exact rational arithmetic. Its `run_001` is the source-data finite stencil, not a reproduction of the publication's underlying correlator analysis.
- `matching_path/check_matching.py --output <fresh-output>` checks matched insertions and same-theory subtraction algebra, and independently sums the cubic QED_L constant with a stated truncation bound. Precision comparisons do not certify floating roundoff.
- `vacuum_response/` contains its exact algebra check and executed contract; it checks defined regulated identities and asymptotics, with no curved-QCD samples.
- `coordinator/check_finite_radius_v2.py <fresh-output>` checks the exact finite-radius observable. Its `runs/exact-002` supersedes the arithmetic failure in `exact-001`. The old input remains immutable so both manifests remain verifiable.

Each executed contract lists the complete declared code/data inputs. Its corresponding manifest records the actual argv, versions, limits, before/after input hashes and result hash. Commands were chosen by the researchers; manifests are records, not executable instructions to trust automatically. Use a fresh output path when reproducing, never the archived result path.

Validate any manifest with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Source receipts identify exact primary versions and checked equations/tables. Some PDF copies are in temporary source caches; URLs and hashes permit reacquisition, and only the declared numerical table is a computational input. A network fetch error or version mismatch is not a physics result.

The report states what the runs do not establish: the full physical proton derivative, any physical vacuum coefficient, convergence of the QCD curvature limit, commutation with the charge derivative, or an alpha prediction. The independent review and input-freshness records are under `reviews/`.
