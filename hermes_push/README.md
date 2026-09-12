# hermes_push

An independent research sandbox for a local agent. The agent's system prompt is `PROMPT_HERMES.md`; the state of the programme it must start from is
`CONTEXT_DIGEST.md`; every push is logged in `FINDINGS_HERMES.md` and backed by a script in this folder; algebra goes into `lean/HermesLean.lean`.

Launch (any local agent framework): give it the repository root as working directory, restrict WRITE access to `hermes_push/`, paste
`PROMPT_HERMES.md` as the system prompt, and open with: "Read hermes_push/CONTEXT_DIGEST.md, then choose the highest-value push from the list in
the prompt, state its kill condition, and begin." Run `python3 hermes_push/harness.py` before each commit (commit guard).

## The loop
`LOOP.md` is the iteration protocol (session ritual, the target shape, the kill order, eight morph operators, anti-loop rules, stop conditions);
`SCORECARD.md` is the shape we want with thresholds and the best so far; `CANDIDATES.md` is the registry (dead lines listed so they are never
re-run); `STATE.md` is the persistent hand-off between sessions. `run_loop.sh N` drives N sessions non-interactively once `AGENT_CMD` points at
your agent's CLI; each session is one iteration and is committed if the guard passes. The agent must never call anything a complete theory:
STOP-GREEN produces `COMPLETE_CANDIDATE.md` (a candidate that passes the scorecard, assumptions listed), STOP-NOGO produces a certified no-go.
