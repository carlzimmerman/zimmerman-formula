# Approved review → implementation plan

The user requested a rewrite implementing the preceding review and termination of the running process. Preserve historical research, leave services disabled, and implement locally without purchasing model calls or restarting research during validation.

Design (corrected after the user's explicit clarification): local Qwen must autonomously generate **and run** Python, repair errors, push doors and generate/run Lean proofs. Human review is not a prerequisite for these steps. A v2 evidence ledger and unique attempt directories isolate legacy scores. Persistent constructive, counterexample and referee roles share recorded attempts. Generated Python runs in a restricted scratch sandbox with pinned real inputs and controls. The referee freezes each next door's hypothesis/checks before coding and reviews its execution afterward. A machine-proposed Lean target is frozen before proof generation. Separate execution validity, hypothesis outcome, formal checking and optional independent publication review.

Implementation sequence:

1. Stop/disable launch agents, verify PID absent, snapshot old source. Keep the original ledger and generated scripts intact.
2. Write regression tests for immutable evidence, stale/changed contracts, dependency scheduling, control crashes, partial failures, malformed results, exact Lean targets, axiom rejection and absent proofs. Run against missing/old behavior to observe failure.
3. Implement v2 contract validation, append-only evidence storage, separate review records, persistent role scheduling and current-verifier status.
4. Replace execution with a hash-pinned generated-evaluator protocol: successful process completion, complete named booleans, positive and negative controls, preserved output and autonomous bounded repairs. Main failure is a scientific rejection, not an infrastructure error. Generated checks may advance a candidate to a further door but cannot establish scientific truth by themselves.
5. Replace Lean certification with a frozen statement/preamble, proof-only generation, restricted tactic input, pinned project/toolchain, explicit axiom inspection and immutable source/output. Compilation of unrelated declarations cannot pass.
6. Integrate the local Qwen model adapter (optional remote referee explicitly off by default), persistent attempts and bounded retries, CLI run/status/replay/review, and initial research obligations. Remove automatic known-result insertion, arbitrary score ranking and automatic Ollama restart. Update watcher and launch instructions. Add narrowly scoped Git ignore exceptions for source/tests/contracts only.
7. Run all tool tests plus offline CLI/replay checks and actual Lean positive/negative fixtures. Inspect the complete diff. Keep services disabled and document remaining limitations.

Review focus: no invalid control may pass; no evidence link can silently change; a failed target cannot be masked by diagnostics; a proof cannot select its own theorem; model-written review cannot automatically become an accepted premise. Registry entries require explicit provenance; no unproved kappa selector is invented to populate the queue.

Implemented and verified on 2026-09-21: 29 regression tests passed with canned model responses, actual sandboxed Python execution and the installed Lean compiler. Offline plan/status/watcher commands, Python syntax and shell syntax checks passed. The first scheduled obligation is kappa normalization. Both launchd services remain disabled, no orchestrator process was found, and the new ledger contains zero research attempts and zero API spend. Historical scripts and ledger are preserved. Live Qwen generation has not been exercised during this stopped-state validation.
