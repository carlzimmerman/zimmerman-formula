# Bounded execution record

The computation-audit run `run_002/manifest.json` completed and validated
against the current input hashes. Its 80 softened-kernel cases have maximum
angular-coefficient absolute discrepancy 3.7026e-14; all endpoint signs are
negative. All 19 scalar-mixture reconstruction checks pass the stated 1e-8
relative tolerance. The coarse lower bounds remain insufficient, as expected.

The first run is retained as `run_001/`: execution failed while serializing
a NumPy boolean to JSON. The only correction was an explicit Python `bool`
cast on the final check flag. This failure is not mathematical evidence.
The successful run pins the corrected script. No physical input changed.

Validation command, from the repository root:

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/KT35_gaussian_closure/analytic/run_002/manifest.json --root "$PWD"
```

The analytic theorem in README is self-reviewed, not independently certified
by these finite floating-point checks.
