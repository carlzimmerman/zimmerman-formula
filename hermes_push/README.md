# hermes_push

An independent research sandbox for a local agent. The agent's system prompt is `PROMPT_HERMES.md`; the state of the programme it must start from is
`CONTEXT_DIGEST.md`; every push is logged in `FINDINGS_HERMES.md` and backed by a script in this folder; algebra goes into `lean/HermesLean.lean`.

Launch (any local agent framework): give it the repository root as working directory, restrict WRITE access to `hermes_push/`, paste
`PROMPT_HERMES.md` as the system prompt, and open with: "Read hermes_push/CONTEXT_DIGEST.md, then choose the highest-value push from the list in
the prompt, state its kill condition, and begin." Run `python3 hermes_push/harness.py` before each commit (commit guard).
