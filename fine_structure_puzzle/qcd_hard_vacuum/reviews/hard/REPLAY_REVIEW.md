# Administrative-input replay review

Mechanical companion to the frozen independent hard review; checked 2026-10-19T18:11:49.620286+00:00. No new scientific computation was performed.

**Verdict: replay provenance verified.** The new completed replay uses the original calculate_hard.py and INPUTS.json. Its result is byte-identical to the reviewed author result, SHA-256 `92b8af4610fa44bf7c338c52c105eefda0a07a60391457742ccb8e71dff84e6e`. The scientific restrictions and scope in REVIEW.md continue to govern it.

The exact original contract has 15 execution artifacts. The replay replaces only `fine_structure_puzzle/HANDOFF.md` with `fine_structure_puzzle/checkpoints/FSP-009_navigation/HANDOFF.md.snapshot.txt` and declares TRANSLATION.md as the sixteenth artifact. The claim identifier and one additional non-claim describe this administrative translation; all mathematical assertions, domain, bounds, conventions, source descriptions, software and randomness fields are unchanged. The original and replay mathematical command argv differ only in the destination result path.

The snapshot SHA-256 `734fc41a38581b536713e688248d941a0d8e453152d104a9d1213ed45f481705` equals both before/after hashes of the original manifest's declared HANDOFF input and both replay hashes of the snapshot. Every other original execution artifact remains byte-identical and matches both manifests' before/after hashes. All 34 frozen author-file pins and all 14 artifacts in the original independent review index remain unchanged; that index itself is pinned in REPLAY_PINS.json.

Current installed-v2-validator checks with `--root .` give the expected outcomes: the original author manifest fails current-input validation because the live HANDOFF path has advanced to FSP-010; the replay manifest validates with completed status. The original record is retained unchanged as a historically completed run with a stale administrative input path. No original manifest, contract or earlier review validation was refreshed. The earlier independent scientific review remains applicable to identical source, proof, code, data and output, while its old successful current-path-validation statement is a dated observation superseded by this explicit provenance companion.

The replay supplies no new physics, source extraction, uncertainty estimate or full-QCD result. It repairs current reproducibility of the previously reviewed finite assertion through an immutable administrative snapshot. Exact file hashes and observed validator output are in REPLAY_PINS.json.
