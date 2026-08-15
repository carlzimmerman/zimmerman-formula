# ESCALATE — decisions that belong to Carl. Append; never resolve yourself.

## 2026-08-15 — PROMOTE S0001 is a dispatcher false-positive (ref_0001 was DISCARD, not PASS)
- next_duty.py dispatched `DUTY: PROMOTE ... The blind referee passed idea 0001`.
- This is FALSE. seeds/refereed/ref_0001.md line 3 = `GRADE: DISCARD`
  (reason: structurally unfalsifiable; "shared C" is a degrees-of-freedom tautology;
  the exact test needs f_wall/f_Q0, which the interp defers to other seeds).
- Root cause: the `pursued` filter in next_duty.py is a bare substring test:
      pursued = [p for p in glob("seeds/refereed/ref_*.md")
                 if "PURSUE" in open(p).read().upper()]
  ref_0001.md line 23 = `WHY NOT PURSUE: PURSUE requires ...` — the token "PURSUE"
  appears in the DISCARD prose, so the naive `in` test classifies a DISCARD as PURSUE.
- Action taken: PROMOTE REFUSED. S0001 was NOT written to TASKS_SEEDED.md
  (would launder a DISCARDED idea; violates the honest-grading rule that DISCARD
  is a terminal success). TASKS_SEEDED.md left non-existent.
- DECISION FOR CARL: key the `pursued` filter off the verdict field, not a substring,
  e.g. `re.search(r"^\s*GRADE:\s*PURSUE", txt, re.M)` (or match the GRADE token).
  Until fixed, every ref_*.md whose prose mentions "PURSUE" will keep re-dispatching
  a bogus PROMOTE (loop will re-issue S0001 each session because S0001 never lands in
  TASKS_SEEDED.md). Recommend also adding a guard: skip PROMOTE if the GRADE field
  is not PURSUE, and log the mismatch.
- Note: this is the first of the T101-T120 MM-programme pipeline; the bug is generic
  and will recur for any future ref whose prose contains "PURSUE"/"PURSUE" as a word.

## 2026-08-15 (re-occurrence) — SAME bogus PROMOTE S0001 re-dispatched, still refused
- next_duty.py re-issued `DUTY: PROMOTE ... passed idea 0001` (this session).
  Cause unchanged: the `pursued` substring filter still matches ref_0001.md's
  "WHY NOT PURSUE:" prose. The fix above is still PENDING Carl's action.
- Action taken: PROMOTE REFUSED again. S0001 still NOT written to TASKS_SEEDED.md.
- CONSEQUENCE: the loop is STUCK on this one re-issued duty; it cannot advance to the
  T101-T120 work until the filter is fixed or a real GRADE:PURSUE ref exists.
- I did not modify next_duty.py myself: per this file's rule ("decisions that belong
  to Carl ... never resolve yourself") the filter fix is Carl's call, not the worker's.
- RESOLVED (frontier model, 2026-08-15): the pursued-filter bug the worker correctly refused and escalated was fixed in next_duty.py (strict GRADE-field parsing, commit pushed). The worker's refusal was the CORRECT action and is noted with approval.
