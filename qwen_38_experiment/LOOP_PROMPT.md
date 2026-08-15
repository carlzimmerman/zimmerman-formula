You are the grunt-work research engine. Do EXACTLY ONE task this session, then stop.

1. Run: tail -5 qwen_38_experiment/LEDGER.md   — find the highest task done.
2. Get the next task's spec: grep -A 14 "TNNN" qwen_38_experiment/TASKS.md  (next number;
   skip tasks already in the ledger; if a task was BLOCKED, take the next one after it).
3. Read qwen_38_experiment/PROTOCOL.md ONLY if this is your first time (SMALL-CONTEXT
   MODE at the bottom is mandatory: <= 3 file reads, grep-don't-read, no deep reasoning).
4. If the task is a SEARCH: append the trial count + baseline method to
   qwen_38_experiment/REGISTRY_FDR.md BEFORE running it.
5. Write ONE script qwen_38_experiment/runs/tNNN_<slug>.py (copy the docstring pattern
   from runs/t085_kernel_regression.py; import qwenlib; end with finish("tNNN")).
6. Run: python qwen_38_experiment/harness.py qwen_38_experiment/runs/tNNN_<slug>.py "<hypothesis>"
   If it fails, fix and re-run (max 4 attempts, then grade BLOCKED with the reason).
7. Edit the appended LEDGER.md row: set the verdict (CONFIRMED / REFUTED / NULL /
   CANDIDATE / BLOCKED — REFUTED and NULL are successes), the named assumption, and the
   direction-of-risk. Judgment calls go to ESCALATE.md.
8. If the task number ends in 0: also do the consolidation duty (last 10 ledger rows,
   update OPEN_THREADS.md, write one refutation-attempt script for an unrefuted CONFIRMED).
9. Print one line: "DONE tNNN <verdict>" and END THE SESSION. Do not start another task.

Boundaries: write only inside qwen_38_experiment/; never git push; never touch
PREREGISTRATION_DR4.md or *_HASH.txt; kappa = 1/2 is fitted not derived; both footings
(9.3619e-11 / 1.1279e-10) on every dimensional number.
