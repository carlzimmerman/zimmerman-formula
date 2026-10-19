# Reproduction and evidence scope

From the repository root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_closure/boundary_heat/runs/exact-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The recorded command and limits are in the v2 manifest. Run status is
`completed`; validation returned `valid evidence record`. The result file
contains exact rational contractions for 4-by-4 matrices, no samples, no
frequency sum, no Bessel root fitting, and no target-alpha input. Repeating
the computation requires a new output path and a copied script/contract
with its result destination updated; do not overwrite exact-001.

Primary source PDFs and extracted text were read from temporary paths
recorded in `SOURCE_RECORDS.json`, and hashed there. The repository contains
the exact source locators and hashes, rather than copied full papers.

The hand calculation is in `INDEPENDENT_DERIVATION.md`; the post-comparison
common-PV order-of-limits calculation is a separate immutable addendum.
The finite experiment checks arithmetic and consistency with TE/TM scalar
specialization. It does not authenticate the theorem by execution, prove
uniform remainders, or close the monopole observable.

Self-proofreading covered the new boundary files, normal/Robin sign,
heat-coefficient indexing and multiplicities. No mathematical-token edits
were made after exact-001 pinned the independent derivation.
