# Cold-energy common-action checkpoint

The full theory remains open. The main new result is an explicit alternative
three-field matter action that admits the near-threshold source, a protected
classical energy floor and a bound-fragment branch in the same equations.
It also has a locally compressible dense phase. Actual energy/charge/J export,
galaxy selection, force normalization and observational closure remain open.

- [Latest stability and Claude accounting results](LATEST_ADDENDUM.md)
- [Equations, mechanism and exact completion boundary](EQUATIONS_AND_MECHANISMS.md)
- [Target, hypotheses and routes](TARGET.md)
- [Original vs extended carrier-action audit](CARRIER_ACTION_AUDIT.md)
- [Gravity/action source dictionary](GRAVITY_ACTION_AUDIT.md)
- [Actual radiation and charge-flux channels](ASYMPTOTIC_FLUX_AUDIT.md)
- [Full homogeneous modes and conditional stability argument](BULK_MODES.md)
- [Claude CFG932 provisional arrival audit](CLAUDE_CFG932_ARRIVAL.md)
- [Explicit mass/energy receiver repair](MASS_LEDGER_REPAIR.md)
- [Executable next discriminating test](NEXT_TEST.json)
- [Failed homogeneous-phase run and repair](FAILED_RUN_002.md)

Completed evidence: run_001 (common-action branch,43 checks) and run_003
(corrected homogeneous phase,19 checks). run_002 is retained with status
failed. The later bulk calculation contributes35 more passed checks in
`bulk_run_001/repaired_run/`; its failed syntax-error launch is preserved.
The source receipts distinguish current local bytes from committed
source revisions; none of these finite checks is a claim of full completion.

The exact argv, versions, limits, input/output hashes and Git observation are
stored in each runner-v2 manifest. To verify provenance without rerunning:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/cold_completion_2026_10_20/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/cold_completion_2026_10_20/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Re-execution uses the recorded runner arguments with a **fresh output directory
and matching result path**; do not replace an existing result or execute an
arbitrary command obtained from an external evidence record. The two root
scripts consume only their declared local dependencies. New physical couplings
require a new contract; no historical benchmark automatically transfers.
