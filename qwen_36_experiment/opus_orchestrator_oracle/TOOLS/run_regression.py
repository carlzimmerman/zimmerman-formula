#!/usr/bin/env python3
"""run_regression.py -- re-run every committed self-checking script and report which fail.

The corpus CLAIMS to be self-verifying. This makes that true and checkable in one command.
Run it before any commit and after any pull.

    python3 qwen_36_experiment/opus_orchestrator_oracle/TOOLS/run_regression.py            # the mi_* corpus
    python3 .../run_regression.py --glob 'real_research/reviews/mi_r_*.py' --timeout 300
    python3 .../run_regression.py --quick                                                  # skip the slow ones
"""
import argparse, glob, os, re, subprocess, sys, time

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
SLOW = {"mi_circular_dS_response_2026.py", "mi_auxfield_exact_circular_2026.py",
        "mi_composite_operator_2026.py", "mi_disformal_completion_2026.py"}
HELD = re.compile(r"(\d+)\s*/\s*(\d+)\s+checks held")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="real_research/reviews/mi_*_2026.py")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(REPO, a.glob)))
    if a.quick:
        files = [f for f in files if os.path.basename(f) not in SLOW]
    if not files:
        sys.exit(f"no files matched {a.glob}")

    fails, tot_ok, tot_all, t0 = [], 0, 0, time.time()
    print(f"regression over {len(files)} script(s), timeout {a.timeout}s\n")
    for f in files:
        b = os.path.basename(f)
        t = time.time()
        try:
            r = subprocess.run([sys.executable, f], capture_output=True, text=True,
                               timeout=a.timeout, cwd=REPO)
            code, out = r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            code, out = -9, "TIMEOUT"
        m = HELD.search(out)
        checks = f"{m.group(1)}/{m.group(2)}" if m else "-"
        if m:
            tot_ok += int(m.group(1)); tot_all += int(m.group(2))
        tag = "ok  " if code == 0 else "FAIL"
        print(f"  [{tag}] {b:<52} {checks:>9}  {time.time()-t:6.1f}s")
        if code != 0:
            fails.append((b, code, out.strip().splitlines()[-6:]))

    print(f"\n  {len(files)-len(fails)}/{len(files)} scripts exit 0"
          f"   |   {tot_ok}/{tot_all} individual checks held"
          f"   |   {time.time()-t0:.0f}s total")
    if fails:
        print("\n  FAILURES:")
        for b, code, tail in fails:
            print(f"    --- {b} (exit {code})")
            for l in tail:
                print(f"        {l[:150]}")
        sys.exit(1)
    print("  corpus is self-verifying.")


if __name__ == "__main__":
    main()
