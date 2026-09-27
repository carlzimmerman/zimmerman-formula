# CD26-3 reconstruction evidence

Accepted computation: `run1/manifest.json`, 21 exact symbolic identities,
six numerical algebraic roundtrips and six declared synthetic epochs. The
60 s wall / 55 s CPU / one-thread runner completed in 1.098556 s. Python
3.9.6, SymPy 1.14.0; execution and input/output hashes are in the manifest.
No random sampling or observational fitting was performed.

Accepted illustration: `plot_run2/manifest.json`. The PNG and PDF were
visually inspected: labels and curves are readable, and the second-panel
legend no longer intersects the constant-pressure reference curve.
`plot_run1` is superseded for that layout reason; its original script is
retained as `plot_attempt1.py`. The old manifest refers to the then-current
script path and is excluded from accepted-current-input validation.

Accepted formalization: `lean_attempt3_record.json` and `lean_attempt3.log`,
exit 0 in 75.87397 s. Six declarations in `InversePressure20260926.lean`
compiled with only `propext`, `Classical.choice` and `Quot.sound`.
Source SHA256:
`70cb19253890254b06eb8bbe74f59bfeee3c816012cb45d0f2094b5202fe31f3`.
The compiler emitted three non-fatal linter warnings about tactic style
and a redundant explicit nonzero hypothesis. There are no proof holes or
custom axioms in the accepted source.

Attempts 1 and 2 failed on the derivative lemma's proof-script conversion,
not on a numerical physics test. Their logs, records and exact failed
source snapshots are retained. Both contain a `sorryAx` consequence of
failed elaboration and are explicitly excluded from certification. Attempt
3 discharges the real-instance equality produced by `convert` as well as
the polynomial derivative equality. Failed attempts are not counted as
separate mathematical results.

The formal scope is six conditional derivative/algebra statements. The
complete continuum integration theorem, background field equations,
action-to-stress interpretation, data fit and full gravity theory are not
formalized here. Independent review is recorded in the spectral-inverse
route's `RECONSTRUCTION_REVIEW.md`. The root `verify_evidence.py` reconciles
current accepted source bytes, logs and axiom dependencies across routes.
