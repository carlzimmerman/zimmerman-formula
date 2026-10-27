# Independent run transition

`run_001` exited with status `failed` at the final conformal-scalar anomaly sanity check. Earlier heat, spectral, metric and combined-charge assertions had returned, but no results file was produced. The failing assertion used exact equality between rounded mpmath values at `xi=1/6`; this is an inappropriate floating-point equality test, not a mathematical counterexample.

The only script change was to replace that equality by `abs(a2(1/6)+1/90)<1e-53` at 55 decimal digits. The original bytes were recovered and their hash checked against `run_001/manifest.json`; they are retained in `historical_inputs/independent_checks_run001.py`. The old manifest remains unchanged. Its original input path now points to the corrected live script, so validation against the live project marks that historical input stale; the historical snapshot retains its exact executed bytes.

`run_002/manifest.json`, with `status=completed`, is the authoritative fresh finite computation record and validates with `--root`. No author results were overwritten, and no author script was imported.
