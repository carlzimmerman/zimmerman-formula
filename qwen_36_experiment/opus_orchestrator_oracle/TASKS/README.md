# TASKS — the systematic work queue

Point the local model here. One task per cycle, top of `QUEUE.md` first.

    1. read QUEUE.md, pick the first task with status OPEN
    2. read TASKS/<that file>.md          <- the only task file you read
    3. read ../02_HOUSE_RULES.md and ../04_FRAMEWORK_FACTS.md
    4. write the script from ../05_SCRIPT_TEMPLATE.py, RUN it
    5. do ../06_VERIFY_PROTOCOL.md
    6. append to ../LEDGER.md, set the status in QUEUE.md, commit, STOP

`../TOOLS/` holds two things you should use every cycle:
- **`mi_constants.py`** — the single source of truth. `import` it; never retype a constant. It exists because
  this folder once produced four different values of a₀. Run it standalone: it must print 15/15.
- **`run_regression.py`** — re-runs every committed self-checking script. Run `--quick` before each commit.

Four kinds of task here:
- **M-tasks** are modified-inertia physics. They carry the corpus's constraints and every one is
  script-decidable. Read `../04_FRAMEWORK_FACTS.md` first or you will contradict a theorem.
- **D-tasks** load actual data. Nothing in this folder ever has — a review grepped for `loadtxt|read_csv|
  Rotmod` across the whole of `qwen_36_experiment/` and found nothing. D01 closes that and the rest build on it.
- **E-tasks** are engineering: the OOM fix, the regression runner, a rules linter. Cheap, and each prevents a
  whole class of error rather than answering one question.
- **W-tasks** are unrelated and deliberately wacky. Pure exploration, no framework rules apply beyond
  "the script must be able to fail." They exist to keep the loop productive when an M-task is blocked,
  and because a few of them are genuinely instructive about what data can and cannot determine.

Rules that apply to BOTH: every check must be able to fail; refine once and report the shift; state what
would falsify the claim. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic anywhere.
