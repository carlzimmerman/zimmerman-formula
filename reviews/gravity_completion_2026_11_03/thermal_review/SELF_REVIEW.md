# Review provenance and self-review

Applied `mathbox:computation-audit` for the two finite runs and
`mathbox:proofread-math` in self-review mode to this directory's mathematical
prose. Scope: CONTRACT.md, REVIEW.md, and the cosmological equations and
output interpretation in release_gate.py /entropy_control.py.

- Routine proofreading: units, definitions of a_rec and comoving rest mass,
  pressure and entropy conventions reviewed; clarified the explicitly
  nonnegative-potential hypothesis in the kination discussion.
- Mathematical-token corrections: none claimed as proofreading. Refined
  spinodal input numbers replaced earlier grid estimates after the pinned
  static output became available; this was an evidence update.
- Numerical controls: spectrum CW trace agreement <=1.6e-10 relative;
  positive excess; visible high-temperature entropy domain; physical
  nearby hidden g_s; spinodal release passes even the generous maximal
  entropy-heating scenario. Both v2 run manifests report completed and
  validate against current input hashes.
- Residual limitations: global one-loop valley potential; false-root static
  data supplied by thermal worker rather than independently reproduced
  here; no gauge-invariant/ring-resummed transition; no collision or capture
  trajectory; conditional number diagnostic only. No bound on arbitrary
  large-field kination or a new SM energy portal.
- Main independent conclusion: an isolated-release energy obstruction does
  not exclude the specified xi=.02 thermal route. The pressure inequality
  is necessary only under its explicit post-release averaged-w hypothesis.

Validation commands:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/gravity_completion_2026_11_03/thermal_review/run_release_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/gravity_completion_2026_11_03/thermal_review/run_entropy_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Both returned: valid evidence record (run status: completed).
