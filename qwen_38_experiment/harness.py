#!/usr/bin/env python3
"""harness.py -- run a task script, capture the tally, append a ledger row skeleton.

Usage: python harness.py runs/t001_slug.py "hypothesis text" [--search N]
The model still fills verdict/key-numbers honestly; this only enforces exit-code truth.
"""
import subprocess, sys, datetime, os

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: python harness.py runs/tNNN_slug.py \"hypothesis\" [--search N]")
    script, hyp = sys.argv[1], sys.argv[2]
    trials = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--search" else "-"
    r = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=3600)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    ok = r.returncode == 0
    print(r.stdout[-2000:])
    verdict = "SCRIPT-GREEN (grade it: CONFIRMED/REFUTED/NULL/CANDIDATE)" if ok else "SCRIPT-RED (fix or mark BLOCKED)"
    row = (f"| {os.path.basename(script).split('_')[0]} | {datetime.date.today()} | {verdict} "
           f"| {hyp} | {tail[0][:60]} | {script} | {trials} | (fill) | (fill) |")
    # T083: DO-NOT-CITE linter -- run before EVERY ledger append (fail-closed, R8).
    linter = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs", "t083_donotcite_linter.py")
    lint = subprocess.run([sys.executable, linter, "--check", row], capture_output=True, text=True)
    sys.stdout.write(lint.stdout or "")
    if lint.returncode != 0:
        sys.stderr.write(lint.stderr or "")
        print("\nLEDGER APPEND BLOCKED: DO-NOT-CITE linter found an R8 retracted phrase in the "
              "new row. Fix the citation or escalate to ESCALATE.md (R10); do NOT append.")
        return 1
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "LEDGER.md"), "a") as f:
        f.write(row + "\n")
    print("\nLEDGER row appended (EDIT the verdict/assumption/risk fields honestly):\n" + row)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
