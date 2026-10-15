# Reproduce and validate this phase

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`. The recorded
runtime is Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0 and, for ODE controls,
NumPy 1.26.2/SciPy 1.11.4. Each manifest names its own dependencies and limits.
Only listed artifacts are pinned; a dirty shared HEAD is not a source bundle.

The [audit table](AUDIT.md) selects authoritative versions. Each route's
REPRODUCE.md supplies its runner command and explanation. Use a new output
directory when repeating; leave the original proofs, inputs and runs immutable.
No repeated calculation is needed merely because the same pinned result is
quoted in a new synthesis.

Validate an authoritative record with the Mathbox validator:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/vacuum_core_round3_2026_10_15/critical_interface/run_v1/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Repeat that command for the other current versions in AUDIT.md. Success checks
current input/output integrity, not the proof's interpretation. A hash-valid
failed process remains a failed process. Three historical records deliberately
fail current-input validation; AUDIT.md and verification_observation.json give
the preserved exact draft paths and their matching recorded hashes.

For a new joined-model execution, follow
[critical_interface/REPRODUCE.md](critical_interface/REPRODUCE.md). Expected:
37 exact identities/inequalities, contraction below 10^-6, radial coefficients
above .56 and .45 and current-plus-wall Rayleigh bound above .5. Existence and
positivity over all admissible radial functions follow from the proof's
uniform contraction and inequalities, not from checking sample profiles.

The Lorentz run tests a true physical polarization; its independent full
matrix check is in action_join/LORENTZ_AUDIT_REPRODUCE.md. The finite-stiffness
source uses exact Bernstein coefficients on [0,1]. The stiff-core IVPs are
floating diagnostics with stated tolerances, not interval enclosures. The
negative soft-core family has an analytic rational bound independent of the
displayed high-precision trial quadrature.

The root verification observation also checks every input snapshot's SHA-256,
JSON readability and referenced current document paths. Historical copied
proofs retain their original relative-link context and are source evidence,
not live navigation. The external empirical lane is assessed from pinned
repository records in EMPIRICAL_DEPENDENCY.md; this phase does not rerun or
alter its empirical statistics.
