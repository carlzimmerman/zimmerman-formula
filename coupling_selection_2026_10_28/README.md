# CS28: deriving the remaining couplings

First result: three selection routes have been tested in DERIVATION.md.
The original one-loop flow has no physical interior fixed ray, and its
radiative vacuum runs away from the Gaussian UV regime. Under the stated
operator hypotheses a unitary SCFT with both Yukawa interactions nonzero
is also excluded. A conditional SU(6) normalization fixes h/lambda but
leaves lambda^4 in B/V. No numerical ratio has been predicted.

`run_verified/result.json`: 15 named checks pass, including nine finite
one-loop trajectories. The version-2 manifest validates with current input
and output hashes. The cutoff max(h^2,lambda^2,g^2)=4 is an arbitrary
diagnostic exit surface, not a physical perturbativity boundary.

The first run (`run/`) failed because SymPy structural expression equality
was used instead of checking an expanded polynomial difference. A minimal
reproduction gave structural equality false and expanded difference zero.
The fix changes only the identity checker, not any equation or parameter.
That initial manifest pins the pre-fix script and is retained as historical
failed evidence; it is not current-input validation and supports no claim.

Reproduce the verified result with the documented contract:

```bash
python3 coupling_selection_2026_10_28/check_selection.py /tmp/cs28-result.json
```

For full bounded-run provenance use computation-audit's run_experiment.py,
the inputs listed in contract.json, a fresh output directory and a result
path inside that directory. All mathematical and external-source scopes
are explicit in DERIVATION.md and SOURCES.md.
