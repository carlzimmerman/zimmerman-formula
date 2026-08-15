#!/usr/bin/env python3
"""next_duty.py -- deterministic dispatcher.  The worker runs this FIRST every session
and follows the printed instruction exactly.  Priority: blind-referee > promote-pursued >
interpret-seed > seeded tasks > numbered tasks.  Seeds auto-replenish every ~6 duties.
"""
import glob, os, re, subprocess, sys

H = os.path.dirname(os.path.abspath(__file__))
j = os.path.join


def ledger_tasks():
    txt = open(j(H, "LEDGER.md")).read()
    return re.findall(r"^\|\s*(t\d+|T\d+|seed\d+|idea\d+)", txt, re.M), txt


def main():
    if os.path.exists(j(H, "STOP")):
        print("STOP file present. Do nothing and end the session.")
        return 0
    for d in ("seeds/pending", "seeds/interp", "seeds/refereed", "seeds/promoted"):
        os.makedirs(j(H, d), exist_ok=True)

    interps = sorted(glob.glob(j(H, "seeds/interp/interp_*.md")))
    refereed = {os.path.basename(p).replace("ref_", "interp_") for p in
                glob.glob(j(H, "seeds/refereed/ref_*.md"))}
    for p in interps:
        if os.path.basename(p) not in refereed:
            print(f"""DUTY: BLIND REFEREE.  Read ONLY this file: {p}
Do NOT read the seed, the ledger, TASKS.md, or any other context -- you are the blind
check.  Grade the idea: PURSUE (falsifiable with in-repo data/scripts, survives 2 minutes
of your own arithmetic, not an obvious tautology or a retracted claim) or DISCARD (say
why in one sentence).  Write your grade + reason to
{p.replace('/interp/', '/refereed/').replace('interp_', 'ref_')}
then append one LEDGER.md row (task id = the seed number, verdict = PURSUE or DISCARD)
and END THE SESSION.""")
            return 0

    pursued = [p for p in glob.glob(j(H, "seeds/refereed/ref_*.md"))
               if "PURSUE" in open(p).read().upper()]
    promoted = open(j(H, "TASKS_SEEDED.md")).read() if os.path.exists(j(H, "TASKS_SEEDED.md")) else ""
    for p in pursued:
        sid = os.path.basename(p)[4:8]
        if f"S{sid}" not in promoted:
            print(f"""DUTY: PROMOTE.  The blind referee passed idea {sid}.  Read {p} and
{j(H, f'seeds/interp/interp_{sid}.md')} and write a full task spec (Hypothesis / Method /
PASS / KILL, FDR pre-registration if it is a search) appended to
{j(H, 'TASKS_SEEDED.md')} with the id S{sid}.  Then END THE SESSION.""")
            return 0

    pending = sorted(glob.glob(j(H, "seeds/pending/seed_*.txt")))
    done, ltxt = ledger_tasks()
    if not pending and len(done) % 6 == 5:
        subprocess.run([sys.executable, j(H, "idea_seed.py"), "--n", "2"], capture_output=True)
        pending = sorted(glob.glob(j(H, "seeds/pending/seed_*.txt")))
    if pending:
        p = pending[0]
        sid = os.path.basename(p)[5:9]
        print(f"""DUTY: INTERPRET.  Read ONLY this seed: {p}
Decipher it charitably into ONE concrete, falsifiable hypothesis about the framework
and/or the Standard-Model numbers (state the exact quantities, the exact test, and what
would kill it).  <= 40 lines.  Write it to {j(H, f'seeds/interp/interp_{sid}.md')}
then MOVE the seed file to seeds/promoted/ (mv) and END THE SESSION.  Do not test it
yourself -- a separate blind session referees it.""")
        return 0

    m = re.findall(r"\*\*S(\d{4})", promoted)
    started = set(re.findall(r"^\|\s*S(\d{4})", ltxt, re.M))
    for sid in m:
        if sid not in started:
            print(f"""DUTY: SEEDED TASK S{sid}.  Get the spec:  grep -A 14 "S{sid}" {j(H, 'TASKS_SEEDED.md')}
Then follow the normal task protocol (script in runs/, harness, grade, ledger row).""")
            return 0

    nums = sorted(int(x[1:]) for x in {d.lower() for d in done if d.lower().startswith("t")})
    nxt = 81
    for cand in list(range(81, 91)) + list(range(1, 81)) + list(range(91, 131)):
        if cand not in nums:
            nxt = cand
            break
    print(f"""DUTY: TASK T{nxt:03d}.  Get the spec:  grep -A 14 "T{nxt:03d}" {j(H, 'TASKS.md')}
Follow the normal protocol (PROTOCOL.md small-context mode): script in runs/, run via
harness.py, grade honestly, append the ledger row, END THE SESSION.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
