# Reproduce the finite hard-proton package

From the project root, with an unused output directory:

```bash
python3 fine_structure_puzzle/qcd_hard_vacuum/hard_proton/run_audit.py --output fine_structure_puzzle/qcd_hard_vacuum/hard_proton/run_reproduction
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_hard_vacuum/hard_proton/run_reproduction/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The launcher invokes the installed real bounded v2 runner with the exact
artifact dependency list in COMPUTATION_CONTRACT.json. Wall limit30s,
CPU15s, log1MiB, one requested numerical-library thread; no RLIMIT_AS,
CPU-affinity request, random sampling or installation. The source PDFs
and complete TeX remain only in the hashed /tmp locations in
SOURCE_RECEIPTS.json. The literal selected table inputs are durable in
INPUTS.json and suffice to reproduce the reported finite transformation.
Source PDFs must be reacquired at exact version URLs if their independent
authentication is to be repeated after /tmp expires. No source PDF is
required by the child command after extraction; source receipt hashes
authenticate identity, not physical accuracy.

Read run.status and current input hashes before using an output. Successful
execution proves only the finite assertion described by the contract;
it does not establish full proton matching, continuous band interpolation
accuracy, a QCD OPE remainder bound, a continuum limit or R(alpha).
