# Matching the internal-field candidate

Start at [STATUS.md](STATUS.md). The preceding candidate is in
[MP01](../mechanism_parent_2026_10_26/RESULTS.md). This packet leaves all old
evidence immutable and writes only its own files.

Reproduce with a fresh output directory from the repository root:

```sh
python3 physical_completion_2026_10_25/launch.py mechanism_match_2026_10_26/check_match_contract.json mechanism_match_2026_10_26/NEW_MATCH mechanism_match_2026_10_26/check_match.py 120
python3 physical_completion_2026_10_25/launch.py mechanism_match_2026_10_26/static_branch_contract.json mechanism_match_2026_10_26/NEW_STATIC mechanism_match_2026_10_26/static_branch.py 300
python3 physical_completion_2026_10_25/launch.py mechanism_match_2026_10_26/static_newton_contract.json mechanism_match_2026_10_26/NEW_NEWTON mechanism_match_2026_10_26/static_newton.py 300
python3 physical_completion_2026_10_25/launch.py mechanism_match_2026_10_26/static_hessian_contract.json mechanism_match_2026_10_26/NEW_HESSIAN mechanism_match_2026_10_26/static_hessian.py 120
```

The latter two scripts intentionally read their recorded original input states;
to reproduce a fully rerouted chain, create new scripts/contracts with the new
dependency paths. Do not overwrite the original runs. Existing dependencies
and scripts are hash-pinned in the manifests. No commit or push was performed.
