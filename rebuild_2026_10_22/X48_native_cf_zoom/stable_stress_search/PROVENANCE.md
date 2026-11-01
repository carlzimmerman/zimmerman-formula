# Stress experiment provenance

The current static evidence is
[`static_verification_inner_shells/manifest.json`](static_verification_inner_shells/manifest.json),
with `run.status=completed`. Its code, definitions, target, test inputs and
results are hash-pinned. The earlier static run is historical after the
inner-shell extension and wording corrections; use the current record for
freshness checks.

The formation experiments were executed in isolated temporary snapshots by
a delegated worker and copied byte-for-byte into this directory:

- `formation_radau_snapshot/` corresponds to original root
  `/private/tmp/x48_collapse_radau_gohdk647`.
- `formation_explicit_failed_snapshot/` corresponds to original root
  `/private/tmp/x48_collapse_audit_scznwd3i`.

Each contains the actual material/collapse source and finite contracts used,
not only numerical results. Relative source and result hashes validate with
the corresponding preserved snapshot as `--root`. Commands in those manifests
retain the original temporary absolute paths as execution provenance; for a
fresh reproduction use the copied source with a fresh output directory and
replace the original snapshot root in the recorded argv. Do not replay output
paths over the preserved evidence.

The formation material source hash is
`4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390`.
The Radau collapse source hash is
`14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf`.
The failed explicit source is preserved with its own different hash. The
exact rejected trial vectors are retained in
`formation_explicit_failed_snapshot/gate_trial_diagnostic.json`.

Final endpoint evidence is
`exact_parcel_endpoint_snapshot/exact_refined/manifest.json`, validated with
the preserved exact snapshot as root. Original snapshot root:
`/private/tmp/x48_exact_parcels_cv2ep7h1`. It retains actual RK45 source,
formation input bytes, contracts, tests, and initial/refined results.
Endpoint source SHA256:
`d52a0840f601ceb89389b0b6b7b01fd48a498d40bca3f481917e177f0e97df29`.
Refined result SHA256:
`5b6b783d15775d9df087db4fb32a42708ce499eb01b5ea3f1ebd38a066f98519`.
The formation input is byte-identical to the preserved N64 Radau result.

`entropy_endpoint_snapshot/` and root-level `endpoint_verification/` are
historical continuous-proxy evidence. Their known method/cap metadata
corrections and pointwise entropy limitation are in `ENTROPY_ENDPOINT.md`.
Do not refresh current source hashes into those old records to conceal the
implementation change.

Read both layers of status. The N128 Radau runner completed and saved a valid
record, but `result.json` says `wall_limit`; only its actually reached interval
is numerical evidence. Execution success does not turn a resource-limited
formation attempt into a completed physical experiment.
The refined formation contract retained a broad assertion mentioning t=8;
its actual command, bounds and result reach only t=1.2. All refinement claims
here use that shorter observed interval, not the overbroad assertion text.

Validation example from the repository root:

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/static_verification_inner_shells/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula

python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/formation_radau_snapshot/n64_tau05/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/formation_radau_snapshot
```

No production X48 job, frozen criterion, existing grade, or cosmological
likelihood was changed. New lane files and bounded evidence are uncommitted.
