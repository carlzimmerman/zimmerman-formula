# Atomic recombination evidence

Read REPORT.md for the exact hypotheses and candidate-action implications.
Final standard computation record: runs/atomic_lab_v2_sources/manifest.json.
Source verification: sources.json pins primary URLs, exact arXiv versions and
PDF/extracted-text hashes; the CAMB snapshot has an exact content hash but
its upstream commit is unknown.

The sources/ directory is a local reference cache and is not included in the
Git deliverables. A source-audit or fully pinned run on another checkout must
restore the matching cached PDFs/text/CAMB snapshot first, then verify every
hash in sources.json and the execution contract. Current master or rebuilt
PDF downloads may differ; a mismatch requires a newly audited source record,
not silent substitution. The numerical laboratory is not a multilevel solver.

The initial runs/atomic_lab/ retains the earlier source-registry revision;
use the v2_sources record for validation against current artifacts.
