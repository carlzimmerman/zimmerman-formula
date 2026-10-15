# Reproduce this checkpoint

Run from the repository root with Python, SymPy and mpmath available. Actual versions, commands, source hashes and execution bounds are recorded in the individual manifests. No large simulation or observational pipeline is required.

To repeat the implemented exact/finite assertions without changing their recorded output files, choose a fresh scratch directory and run:

```bash
python3 sol61_push/multicurrent_continuation_2026_10_15/remnant/check_remnant.py /tmp/mc-remnant-repeat.json
python3 sol61_push/multicurrent_continuation_2026_10_15/conversion/check_conversion.py /tmp/mc-conversion-repeat.json
python3 sol61_push/multicurrent_continuation_2026_10_15/modes/check_two_current.py --output /tmp/mc-modes-repeat.json
python3 sol61_push/multicurrent_continuation_2026_10_15/modes/check_jeans_surrogate_v2.py --output /tmp/mc-jeans-repeat.json
python3 sol61_push/multicurrent_continuation_2026_10_15/halo_health/check_profile_domain.py --output /tmp/mc-halo-repeat.json
python3 sol61_push/multicurrent_continuation_2026_10_15/boundary/check_boundary.py /tmp/mc-boundary-repeat.json
```

Use different scratch filenames if these already exist. Expected assertions: remnant 13 exact/parameter controls and nine quadratures; conversion 52 exact checks; principal modes sixteen identities and 72 rational cases; separate finite-frequency surrogate five identities and four examples; halo profile eleven identities, ten radial samples and three witnesses; boundary four identities and four limit controls. Read the proof domains before transferring any result to a physical model.

The authoritative recorded runs are `remnant/run_v1`, `conversion/run_v4`, `modes/run_exact`, `modes/run_jeans_v2`, `halo_health/run_exact` and `boundary/run_v1`. The lane reproduction files give the full bounded-runner commands. If the Mathbox computation-audit skill is installed, its `scripts/validate_manifest.py MANIFEST --root REPOSITORY` checks each record against current input and output bytes. A valid manifest verifies provenance, not the mathematical interpretation.

The conversion `run`, `run_v2` and `run_v3` records are superseded drafts. Their input hashes may differ from the final report/code; do not treat their earlier successful exits as freshness validation of current files. The failed first Jeans surrogate run and its original script are retained separately; the revision factors an expression before symbolic substitution without changing the mathematical assertion or tested family.

`inputs/` contains immutable copies of the actual project sources used here, including sources that were untracked at the base checkpoint. Their original locations and hashes are in `inputs/source_manifest.json`. Relative links inside those raw snapshots retain their original source-document context; use the manifest when resolving them. They are inputs, not newly audited empirical evidence.

The primary-source record links the exact external preprint version. Its full text is only an ignored local cache and is not needed for the direct algebraic computations. The claims that rely on its variational framework are distinguished from the project's newly derived conditional equations in `literature/SOURCE_CHECK.md`.
