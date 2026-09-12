# scout/

An always-on bot for a small local model. It does two things, both checkable without trusting the model: it writes candidate Lean
theorems, which the compiler either accepts or rejects, and it writes structured proposals, each of which must name a kill condition
as a number.

## Setup, once
```
./hermes_push/scout/setup_lean.sh          # builds the persistent Lean project (slow the first time)
export AGENT_CMD='<your local model's non-interactive command>'
```

## Run it
```
./hermes_push/scout/run_scout.sh 1800       # a cycle every 30 minutes, forever
./hermes_push/scout/run_scout.sh 1800 20    # or twenty cycles and stop
```
Each cycle produces exactly one output, verifies it if it is Lean, appends it to `PROPOSALS.md`, and commits only files under
`hermes_push/scout/`. The driver refuses to commit if the agent touched anything outside that folder.

## Triage, when you feel like it
Read `PROPOSALS.md`. Entries marked CERTIFIED are theorems and can be lifted into the main Lean file. Entries marked PROPOSED are
questions; mark each `taken`, `rejected: <reason>`, or `duplicate of <entry>`. The value of the loop is in that triage, not in the
volume it produces.

## Why this shape
A small model cannot be trusted to judge physics, so it is never asked to. The Lean compiler is ground truth for the first output,
and a human is ground truth for the second. The failure mode to watch for is a model that weakens theorems until they compile;
`SCOUT.md` forbids it explicitly and a trivial CERTIFIED entry should be rejected on sight.
