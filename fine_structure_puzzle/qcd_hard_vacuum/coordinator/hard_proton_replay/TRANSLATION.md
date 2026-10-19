# Exact administrative-input replay

The final FSP010 navigation update changes live HANDOFF.md. The original hard_proton/run_001 manifest declared the then-live FSP009 handoff as an input, so it is now a retained completed record with stale live administrative input. Its scientific code, source data, proof and output remain unchanged. No old manifest or contract is edited.

This new contract replaces only that execution-artifact path by checkpoints/FSP-009_navigation/HANDOFF.md.snapshot.txt, whose bytes match the old input SHA734fc41a38581b536713e688248d941a0d8e453152d104a9d1213ed45f481705 exactly. The original calculate_hard.py, INPUTS.json and every other science input are reused byte-identically. The same actual mathematical command writes a fresh result below this folder. A separate result-byte comparison and review will establish the replay rather than updating old evidence hashes. The newly added note is a declared interpretation input, not a changed physics premise.

The old ancestry-pins file remains a historical map to its original root path; its old handoff hash is resolved to the preserved snapshot in the final provenance assessment. The calculation reads only its numerical INPUTS.json. No numerical alpha, mass, source fit or cutoff prescription is changed. No address-space cap is requested on macOS.
