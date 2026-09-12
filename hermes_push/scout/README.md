# scout/

An always-on bot for a small local model. It does two things, both checkable without trusting the model: it writes candidate Lean
theorems, which the compiler either accepts or rejects, and it writes structured proposals, each of which must name a kill condition
as a number.

## Setup, once
```
./hermes_push/scout/setup_lean.sh          # builds the persistent Lean project (slow the first time)
export AGENT_CMD='hermes --in . --yolo -m <model> -z'
```
`-z` takes the prompt as its argument and runs headlessly, `--in` sets the working directory, `--yolo` lets it use tools without
stopping to ask. Add `--provider` if your model needs one. Pick the model with `hermes model` if you have not already.

## Test one cycle before letting it loop
```
./hermes_push/scout/run_scout.sh 60 1
```
Read what it produced in `PROPOSALS.md` and check `git log -1`. If it wrote outside this folder the driver refuses to commit and
says so; fix the prompt before going further.

## Run it
```
./hermes_push/scout/run_scout.sh 1800       # a cycle every 30 minutes, forever
./hermes_push/scout/run_scout.sh 1800 20    # or twenty cycles and stop
```
Stop it with Ctrl-C, or leave it under `nohup` and kill the process later.

## Or use the agent's own scheduler instead of this loop
The Hermes CLI has `hermes cron`, which survives reboots and keeps a durable history:
```
hermes cron create --name scout --schedule "0 * * * *" --prompt "$(cat hermes_push/scout/CYCLE_PROMPT.txt)"
hermes cron list
hermes cron runs scout
```
Check `hermes cron create --help` for the exact flag names on your version. The loop script and the scheduler do the same thing;
the scheduler is better if you want it to survive a restart, the loop is better if you want to watch it.
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
