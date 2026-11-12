# FINAL5 forward correction: corrected signal (2026-11-12)

`corrected_signal.py` is a byte-identical copy of the corrected calculation another session wrote for FINAL5
(projection through the gas shell, a two-dimensional beam, flux units). It is placed here, beside the lane, so that
the lane's own `final5_signal.py` and its outputs stay exactly as first committed.

Run here by the lead session: `python3 corrected_signal.py corrected_signal.json` and the same with `--mutate`
(`corrected_signal_MUTATE.json`); the `.out` files are the captured standard output. The first JSON is byte-identical
to the other session's own run.

Independent check: `reviews/codex_corrections_audit_2026_11_12/C4_gas_signal_and_combined_route.md` (grade CORRECT;
the auditor recomputed the signal in SI on both footings and matched these numbers to four digits). The gas shell is
one example profile; no detection significance is assigned.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
