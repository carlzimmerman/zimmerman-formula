# Symbolic representation mismatch in the first normalization run

The first run failed one assertion because it compared expression trees:
`-u**2*(2*u-3)` versus `u**2*(3-2*u)`. Their simplified difference is exactly
zero. All other assertions passed. This is an implementation comparison
error, not a failed mathematical inequality or a changed criterion.

normalization.py and evidence/normalization remain unchanged. The separate
normalization_v2.py changes only this assertion to test the simplified
difference against zero. The corrected run and its mutation have separate
manifests. No domain, coefficient, expected result or threshold changes.
