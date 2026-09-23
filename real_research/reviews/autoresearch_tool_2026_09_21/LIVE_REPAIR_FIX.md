# Live-response repair correction — 2026-09-21

The first live run produced 11 invalid attempts under verifier `obligations-v2.1`. Actual local-model responses exposed a defect absent from the original canned fixtures: the orchestrator froze check metadata before checking that negative-control names were a subset of the required names. This prevented correction of invalid specifications. Several repairs also repeated entire JSON answers, and the initial repair prompt accumulated all previous replies.

Under `obligations-v2.2`:

- The scientific hypothesis and assumptions are frozen immediately after parsing. Check names are frozen only after protocol validation; a valid specification cannot be weakened during execution repairs.
- Local model requests explicitly request JSON format. Duplicate/malformed output is still rejected, not silently salvaged. Completion reason and token count are retained when the server provides them.
- Repair calls receive the latest failed response and actual logs, rather than a growing sequence of all failed answers. Both initial and door repairs use the same explicit experiment protocol.
- Control failures name exactly which checks violated positive/negative expectations. Prompts clarify the common predicate, input perturbations, counterexample orientation, manifest access and Python boolean serialization.
- Running status is written before model generation, so the watcher does not show stale stopped state during the first call.

Six regression tests exercise these cases, including real sandboxed Python execution, preservation of the scientific claim, and refusal to change a valid target after a runtime error. Four new regressions failed before the fix; the two target-preservation cases already passed. All 35 orchestrator tests passed afterward, including actual Lean compilation. Existing evidence remains immutable; verifier-specific counters distinguish the fixed run from historical failures.

The user authorized relaunch; the launchd loop restarted as PID 68209. Live validation is recorded below when available. This work changes research plumbing, not a physical claim or theorem.

Live validation: the first v2.2 local Qwen response (`b980070fc36d4362bb1b26bfcbc56f0d`) and its repair (`5894355ab71e400391023b983be45c47`) both parsed successfully, preserved the frozen specification, and ran generated Python in all three modes. The repair changed the actual program and received the prior control diagnostics. Both candidates still failed substantive control expectations and were retained as invalid, with no door or Lean promotion. This confirms that execution and repair are operating; it does not establish that the model can solve the research problem. No scientific acceptance threshold was relaxed.

The second live repair (`2c084274aa824dafa8187527fee2b0f2`) subsequently passed the execution protocol. Manual inspection found that it inverted its predicate in negative mode and did not establish its stated selector hypothesis. The automatic referee rejected it (`ad8b37e9be37489caf429c4685c603bf`), and the recorded chain ended `halted_by_referee` with zero surviving doors (`3973c62240e6476ea0bcd386ff5346f6`). Thus the live generate → run → repair → referee path completed, and a superficially passing script was not promoted to a Lean attempt or scientific result. Continuous scheduling remains enabled.
