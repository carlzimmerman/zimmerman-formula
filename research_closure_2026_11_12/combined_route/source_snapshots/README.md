# Source revisions

Each `combined_constraints_vN.py` is byte-identical to the input SHA-256 in `constraints_run_00N/manifest.json`. Version2 added exact-simple-kernel scalar environmental matching; version3 corrected the mean-density-equivalent catchment-radius label after independent review. The two earlier manifests remain unchanged and correctly fail a *live input* freshness check, because their input path was subsequently revised. Original bytes and all results are preserved. Use `constraints_run_003` as current evidence. No run record was rewritten.
