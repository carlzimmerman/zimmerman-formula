#!/usr/bin/env python3
"""next_idea.py -- deterministic dispatcher. Run FIRST every session; do exactly what it says."""
import os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
j = lambda *a: os.path.join(H, *a)


def done_ids():
    p = j("LEDGER.md")
    if not os.path.exists(p):
        return set()
    return {m.upper() for m in re.findall(r"^\|\s*(I\d{3})\s*\|", open(p).read(), re.M | re.I)}


def main():
    if os.path.exists(j("STOP")):
        print("STOP file present. Do nothing and end the session.")
        return 0
    txt = open(j("IDEAS.md")).read()
    ids = [int(x) for x in re.findall(r"\*\*I(\d{3})\s*—", txt)]
    if not ids:
        ids = [int(x) for x in re.findall(r"\*\*I(\d{3})", txt)]
    have = {int(x[1:]) for x in done_ids()}
    # RESERVED: Claude is running these four directly (I001 EFE factorisation,
    # I003 disc corrections, I012 the RAR s-requirement, I037 dust vorticity).
    # Skip them entirely so the local worker never duplicates that work.
    RESERVED = {1, 3, 12, 37}
    # PRIORITY: the roadblock-critical ideas first, so a short night still buys the most.
    # R1 (the 233x gap) and R2 (dust) lead; then screening; then homes; then the rest.
    PRIORITY = ([2, 4, 7, 5, 6, 8, 9, 10, 11, 13, 14, 15]
                + list(range(101, 141))          # screening mechanisms
                + list(range(301, 341))          # dark sector / dust
                + list(range(201, 241))          # alternative homes
                + list(range(16, 26)) + list(range(36, 51)))
    allids = sorted(set(ids))
    rank = {v: k for k, v in enumerate(PRIORITY)}
    todo = sorted([i for i in allids if i not in have and i not in RESERVED],
                  key=lambda i: (rank.get(i, 10**6), i))
    if not todo:
        print("ALL AVAILABLE IDEAS DONE (I001/I003/I012/I037 are reserved for Claude). Write a one-paragraph summary of the ledger to\n"
              f"{j('SUMMARY.md')} and end the session.")
        return 0
    n = todo[0]
    print(f"""DUTY: IDEA I{n:03d}   ({len(have)}/100 done, {len(todo)} left)

1. Read the rules ONCE:            {j('PROTOCOL.md')}
2. Get this idea's spec:           grep -A 6 '\\*\\*I{n:03d}' {j('IDEAS.md')}
3. Write a script:                 {j('runs')}/i{n:03d}_<shortname>.py
   - numbered [ok]/[FAIL] checks, exit 0 only if all pass
   - report BOTH a0 footings for any dimensional number
4. Run it. If it is not producing a number within 20 MINUTES, stop and grade NOT COMPUTED.
5. Write a FULL RESULT FILE to {j('results')}/I{n:03d}_<shortname>.md using the template
   {j('RESULT_TEMPLATE.md')} -- the math written out, a numbers table, why the verdict
   fired, and a mandatory "Against my own result" section. THIS is what gets reviewed;
   a ledger row without it does not count.
6. Append EXACTLY ONE row to {j('LEDGER.md')}:
   | I{n:03d} | what you did | the decisive number | PASS or KILL or PARTIAL or NOT COMPUTED |
7. END THE SESSION. Do not start another idea.

Do not read the other 99 ideas. Do not modify anything outside this folder.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
