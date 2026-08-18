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
    todo = [i for i in sorted(set(ids)) if i not in have]
    if not todo:
        print("ALL 100 IDEAS DONE. Write a one-paragraph summary of the ledger to\n"
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
5. Append EXACTLY ONE row to {j('LEDGER.md')}:
   | I{n:03d} | what you did | the decisive number | PASS or KILL or PARTIAL or NOT COMPUTED |
6. END THE SESSION. Do not start another idea.

Do not read the other 99 ideas. Do not modify anything outside this folder.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
