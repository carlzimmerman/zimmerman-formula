# 2026-11-03 — post-result provenance correction

κ = ½ FITTED; not theory closed

The first manifest failed validation because declared_results was empty, although CRITERIA required JSON verdicts. Preserve it as manifest_first_invalid.json and its result as results_first.json. Explicitly declare results.json for the repeat. No equation, threshold, data or label changes. This fixes future provenance; it does not retroactively validate the first manifest. The earlier max_cores=1 was not enforced CPU affinity on macOS; correct it to null. Numerical-library thread settings were supplied in the command.
