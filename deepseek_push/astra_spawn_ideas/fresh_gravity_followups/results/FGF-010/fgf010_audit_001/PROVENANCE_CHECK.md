# Read-only provenance check

Actual argv:

```json
[
  "python3",
  "/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py",
  "campaign_fresh_gravity_astra/stage_04/scale_dynamics/run_001/manifest.json",
  "--root",
  "/Users/carlzimmerman/new_physics/zimmerman-formula"
]
```

Observed output: `valid evidence record; mathematical interpretation requires review`.

All seven candidate intake hashes matched before raw-proof review and again
at completion. This validates source/result provenance, not an independent
reproduction of the candidate numerical experiments. No new numerical
experiment or parameter sweep was run; this audit uses exact algebra and
explicit exact negative controls. No new computational manifest is applicable.
The author reports 21 passing checks; those outputs were read, not rerun.
