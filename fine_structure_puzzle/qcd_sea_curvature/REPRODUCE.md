# FSP-007 evidence and reproduction

The phase contains actual published sea-moment inputs, exact OPE/matching algebra and a controlled chiral/dispersive calculation. It contains no curved-space QCD ensemble simulation or complete physical ratio.

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula` and use fresh output paths. Do not overwrite the archived results.

- `sea_lattice/` records the exact primary table, alpha_ref convention and source-archive inspection, plus any bounded moment/counterexample transform. It does not reproduce the source's underlying lattice extraction.
- `sea_ope/run_audit.py --output <fresh-run-directory>` reproduces the exact tensor, mixing and counterterm checks. `run_003` pins the final inputs. `run_002` completed historically but its declared derivation input changed in the documented revision; it is stale against the live path and is not the authoritative record. `run_001/FAILURE.md` records an address-space-limit launch failure, not a physics failure.
- `coordinator/check_uv.py <fresh-result>` checks mixed-beta conversion, calibration projection and a scalar inverse-moment example. The current execution is `coordinator/run_001`.
- `curved_response/checks/check_trace_cut.py` has an output path relative to its own file. Run only a byte-identical copy in a fresh directory, as `coordinator/reproduce_curved.py` does. This avoids overwriting its original results. The supplementary `coordinator/curved_reproduction_001` is a bounded mathbox-v2 record; the author's custom `checks/MANIFEST.json` is retained with its explicitly stated schema limitations.

The review directories contain source-first derivations, independent algebra or quadrature checks, source screenshots/receipts when used and target hashes. Reexecuting an author's script is distinct from independently deriving its physics.

Validate mathbox-v2 records with the installed tool:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Custom records are not represented as mathbox-v2 passes. The final validation sweep distinguishes current, stale historical and custom records. Numerical quadrature comparisons have finite grids/tolerances; none is an interval certificate or an infrared QCD convergence proof. Source receipts identify exact versions and hashes; temporary PDFs/TeX archives may require reacquisition.
