# Independent finite heldout implementation review: pre-arithmetic checks

Review the completed `heldout/run_006_final` result, logged selectors, native sigma table, executed sources and
`run_heldout_v4.py`; do not execute the observational harness. Recompute each recorded candidate column from
the original X48 full-precision S9 data and the saved native HO2 log-column table. Compare all logged columns
to relative 1e-12, and all actual branch booleans to the direct strict inequality with their actual pipeline
floor. Require MW selected mass to equal BS1's primary LG sum, all same-L concentration table knots to match
S9 scaling to 1e-12, and all existing normal run checks true. Record observed baseline/cache controls and source
hashes. Independently compare this lane's reconstructed lens support against calibration/lens_support.json.

This is an independent arithmetic/semantics review of the implemented selectors, not independent raw geometry,
MW dynamics or observational reduction. The unchanged-L cache replay checks are author controls; source review
must confirm cache keys omit only quantities that are constant across L. Failed old runs do not supersede a
completed newer manifested source revision. No result is a continuous-L feasibility proof.
