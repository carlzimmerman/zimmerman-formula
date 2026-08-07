# TASKS — the systematic work queue

Point the local model here. One task per cycle, top of `QUEUE.md` first.

    1. read QUEUE.md, pick the first task with status OPEN
    2. read TASKS/<that file>.md          <- the only task file you read
    3. read ../02_HOUSE_RULES.md and ../04_FRAMEWORK_FACTS.md
    4. write the script from ../05_SCRIPT_TEMPLATE.py, RUN it
    5. do ../06_VERIFY_PROTOCOL.md
    6. append to ../LEDGER.md, set the status in QUEUE.md, commit, STOP

Two kinds of task here:
- **M-tasks** are modified-inertia physics. They carry the corpus's constraints and every one is
  script-decidable. Read `../04_FRAMEWORK_FACTS.md` first or you will contradict a theorem.
- **W-tasks** are unrelated and deliberately wacky. Pure exploration, no framework rules apply beyond
  "the script must be able to fail." They exist to keep the loop productive when an M-task is blocked,
  and because a few of them are genuinely instructive about what data can and cannot determine.

Rules that apply to BOTH: every check must be able to fail; refine once and report the shift; state what
would falsify the claim. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic anywhere.
