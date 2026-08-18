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
    # read ALL idea files, and remember which file each id lives in
    import glob as _glob
    srcs = sorted(_glob.glob(j("IDEAS*.md")))
    txt, home = "", {}
    for _f in srcs:
        _t = open(_f).read()
        txt += _t
        for _m in re.finditer(r"^\*\*I(\d{3})\s*—", _t, re.M):
            home[int(_m.group(1))] = _f
    ids = sorted(home.keys())
    have = {int(x[1:]) for x in done_ids()}
    # I001/I003/I012/I037 are DELIBERATELY LEFT IN, and run FIRST, even though Claude is
    # also running them directly. That is the point: two independent attempts at the four
    # roadblock-critical ideas, with no knowledge of each other, is a blind cross-check.
    # Agreement raises confidence; disagreement localises an error in one of them.
    RESERVED = set()
    PRIORITY = ([1, 3, 12, 37, 2, 4, 7, 5, 6, 8, 9, 10, 11, 13, 14, 15]
                + list(range(101, 141))          # screening mechanisms
                + list(range(301, 341))          # dark sector / dust
                + list(range(201, 241))          # alternative homes
                + list(range(16, 26)) + list(range(36, 51)))
    allids = sorted(set(ids))
    rank = {v: k for k, v in enumerate(PRIORITY)}
    todo = sorted([i for i in allids if i not in have and i not in RESERVED],
                  key=lambda i: (rank.get(i, 10**6), i))
    if not todo:
        print(f"ALL {len(ids)} IDEAS DONE. Write a one-paragraph summary of the ledger to\n"
              f"{j('SUMMARY.md')} and end the session.")
        return 0
    n = todo[0]
    print(f"""DUTY: IDEA I{n:03d}   ({len(have)}/{len(ids)} done, {len(todo)} left)

1. Read the rules ONCE:            {j('PROTOCOL.md')}
2. Get this idea's spec:           grep -A 8 '\\*\\*I{n:03d}' {home[n]}
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
