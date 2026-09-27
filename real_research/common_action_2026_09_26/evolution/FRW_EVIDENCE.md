# Additional de Sitter/PQ evidence

This addendum preserves the earlier verification.json and its six-run, fourteen-lemma freeze. The current addition comprises two accepted symbolic runs and one separate six-lemma Lean certificate.

| Run | Exact checks | Seconds | Exit |
|---|---:|---:|---:|
| frw_run_001 | 19 | 3.903493 | 0 |
| pq_run_001 | 18 | 1.254948 | 0 |

Both manifests validate with the computation-audit validator. Each job used the explicit Xcode Python 3.9.6 executable, SymPy 1.14.0, a 60-second enforced cap, one-thread settings, and no randomness. No numerical wave-number scan is the basis of the all-q result. The analytic inequalities and their derivation are in FRW_RESULT.md. Frozen action sources and inventory hashes are under frw_snapshots/.

PQBridge20260926.lean compiled successfully with six axiom reports in pq_lean_attempt2.log. The command was:

    /opt/homebrew/bin/lake env lean -j 1 /Users/carlzimmerman/new_physics/zimmerman-formula/real_research/common_action_2026_09_26/evolution/PQBridge20260926.lean

The working directory was:

    /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026

The compile exited 0 in 17.135470 seconds. Its sole warning concerns tactic sequencing style. All six statements use only propext, Classical.choice, and Quot.sound. The source has no admissions or custom axioms. Toolchain: Lean 4.34.0-rc2, commit 6a10ac8c22beadecabdbb0919c2b50214762f91d; mathlib 85e3a25e006c35636f0e53b0e9296caca2685bc0.

- Accepted source SHA-256: 4ce7d94f7b57b3c4eec6fe48d5fa651e3393af0579aa0d2b9575fb020f4303fe.
- Accepted log SHA-256: dd280233a665dce0f8fb8651947870bb4dacfab1490cbeeee6b4c270293b4519.
- Exact metadata, statements, hypotheses, and scope: pq_lean_record.json.

The failed first Lean attempt is preserved verbatim at development_sources/pq_lean_attempt1.lean, with pq_lean_attempt1.log and pq_lean_attempt1.json. Its error-generated sorryAx outputs are rejected evidence; they are absent from the accepted second compile. No source reconstruction or guessed hashes were used.

Combined with the unchanged earlier freeze, evolution now contains eight accepted symbolic manifests with 124 exact checks, plus twenty Lean declarations across two accepted sources. The new proof scope is conditional coefficient/sign/tuning algebra. The ADM derivation, exponential estimates, and future-mode argument are explicit analytic calculations, not claimed as Lean-certified.

The original negative infrared stiffness is retained. The repaired action requires a new projected vacuum potential with a tuned coefficient. Positive nonzero-mode signs and bounded future evolution of each fixed scalar mode do not establish uniform q=0 coercivity, nonlinear global existence, or full coupled-mode closure.
