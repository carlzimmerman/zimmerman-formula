#!/usr/bin/env python3
"""Re-run every script of the fine-structure campaign (AH1-AH6 and lanes A-S) with the CORRECT control convention and check exit codes.

Why this exists: the mutation-control invocation differs by script (positional `MUTATE`, `--mutate`, or `--selftest --mutate`), and a script
invoked with the wrong convention silently runs its real path and exits 0.  This runner detects each script's convention from its source,
applies the documented exceptions, and compares against the expected exit codes:

  real run            -> 0   (exception: Q4/q1_numeric_audit.py exits 1 BY DESIGN, its pre-registered 'H1 false' case)
  control             -> 1   (exceptions: AH1, AH2, AH4, AH6 with --mutate exit 0 and print 'control works';
                              Q4/q1 control exits 1 but is uninformative because the real run also exits 1;
                              K's --mutate-s2 exits 0 and changes nothing;  AH5 has no control (exact algebra))

Usage:
  python3 run_all_checks.py --list                 show the manifest and detected conventions, run nothing
  python3 run_all_checks.py                        run everything (parallel; several scripts take many minutes)
  python3 run_all_checks.py --only A_wgc_extremal  run one lane / directory name fragment
  python3 run_all_checks.py --lean                 also compile the Lean certificates (needs `lake` in fable_independent_2026/lean_2026)
Environment: R1_CACHE and Q4_CACHE must point at the downloaded-source caches for the scripts that read them (R1 and Q4 lanes);
those scripts are SKIPPED with a note when the variable is not set.  Scripts write their own .out/.json files in place; this runner
only captures exit codes and writes RUN_ALL_RESULTS.json/.md next to itself.
"""
import os
import re
import sys
import json
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TIMEOUT = 5400

DIRS = [os.path.join(ROOT, "real_research", "alpha_schwinger_2026")]
DIRS += [os.path.join(HERE, d) for d in sorted(os.listdir(HERE))
         if os.path.isdir(os.path.join(HERE, d)) and re.match(r"^[A-Z][0-9]?_", d)]

SKIP_FILES = {"rg_common.py", "bar_lib.py", "tower_lib.py", "clifford_lib.py", "q1_lib.py", "n1_lib.py", "s1_lib.py", "s1_modesum.py",
              "p2_rerun_all.py",                # re-runs everything itself; excluded to avoid recursion
              "run_all_checks.py"}
IN_PROGRESS = set()     # lanes whose agent had not reported when this runner was written (S1 reported and was added back)
NEEDS_ENV = {"r1_chronology.py": "R1_CACHE", "r2_program_history.py": "R1_CACHE", "r5_choice_inventory.py": "R1_CACHE",
             "q5_pajuhaan_checks.py": "Q4_CACHE", "q6_blandino_bleger_checks.py": "Q4_CACHE"}
REAL_EXPECT_OVERRIDE = {("Q4_unaudited_claims", "q1_numeric_audit.py"): 1}
CONTROL_EXPECT_OVERRIDE = {("alpha_schwinger_2026", "ah1_schwinger_ds2.py"): 0, ("alpha_schwinger_2026", "ah2_induced_current_ds2.py"): 0,
                           ("alpha_schwinger_2026", "ah4_induced_current_ds4.py"): 0, ("alpha_schwinger_2026", "ah6_kaluza_klein.py"): 0}
# Scripts whose real run is EXPECTED to fail against the CURRENT repo state by construction:
# p1_consistency.py audits the status document as it stood at commit 087c41203 (hashes, quoted phrases, the wording later corrected);
# the document was revised afterwards, so the audit's string and hash checks no longer match.  Its control still must exit 1.
EXPECTED_DRIFT = {("P_claim_audit", "p1_consistency.py")}
NO_CONTROL = {("alpha_schwinger_2026", "ah5_dimensional_obstruction.py")}
SPECIAL = {("D_calibration_bar", "alpha_bar_checker.py"): (["--selftest"], ["--selftest", "--mutate"])}


def detect(path):
    """Look only at source lines that mention argv (so docstrings that merely describe the other convention do not confuse it)."""
    lines = [l for l in open(path, encoding="utf-8", errors="replace").read().splitlines() if "argv" in l or "add_argument" in l]
    txt = "\n".join(lines)
    pos = re.search(r"""["']MUTATE["']""", txt) is not None
    flag = re.search(r"""["']--mutate["']""", txt) is not None
    if flag and not pos:
        return "--mutate"
    if pos and not flag:
        return "MUTATE"
    if pos and flag:
        return "AMBIGUOUS"
    return None


def manifest():
    rows = []
    for d in DIRS:
        lane = os.path.basename(d)
        if lane in IN_PROGRESS:
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".py") or f in SKIP_FILES:
                continue
            path = os.path.join(d, f)
            key = (lane, f)
            if key in SPECIAL:
                real_args, ctl_args = SPECIAL[key]
                conv = "--selftest --mutate"
            else:
                real_args = []
                conv = detect(path)
                ctl_args = [conv] if conv else None
            rows.append(dict(lane=lane, dir=d, file=f, convention=conv if conv else ("none" if key in NO_CONTROL else "UNDETECTED"),
                             real_args=real_args, ctl_args=None if key in NO_CONTROL else ctl_args,
                             real_expect=REAL_EXPECT_OVERRIDE.get(key, 0), ctl_expect=CONTROL_EXPECT_OVERRIDE.get(key, 1),
                             env=NEEDS_ENV.get(f)))
    return rows


def run(row, args, env):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, row["file"]] + args, cwd=row["dir"], env=env, capture_output=True, timeout=TIMEOUT)
        return p.returncode, time.time() - t0
    except subprocess.TimeoutExpired:
        return "timeout", time.time() - t0


def one(row):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if row["env"] and not os.environ.get(row["env"]):
        return dict(row, real=None, ctl=None, status="SKIPPED (set %s)" % row["env"], secs=0.0)
    if row["convention"] in ("UNDETECTED", "AMBIGUOUS"):
        return dict(row, real=None, ctl=None, status=row["convention"] + " convention (add to the runner)", secs=0.0)
    real, t1 = run(row, row["real_args"], env)
    ctl, t2 = (None, 0.0) if row["ctl_args"] is None else run(row, row["ctl_args"], env)
    drift = (row["lane"], row["file"]) in EXPECTED_DRIFT
    ok_real = (real == row["real_expect"]) or (drift and real == 1)
    ok_ctl = True if row["ctl_args"] is None else (ctl == row["ctl_expect"])
    return dict(row, real=real, ctl=ctl, status=("OK (expected drift)" if drift and ok_real and ok_ctl else "OK") if (ok_real and ok_ctl) else "MISMATCH", secs=t1 + t2)


def main():
    rows = manifest()
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
        rows = [r for r in rows if only in r["lane"] or only in r["file"]]
    if "--list" in sys.argv:
        print(f"{len(rows)} scripts")
        for r in rows:
            print(f"  {r['lane']:34s} {r['file']:44s} control: {r['convention']:20s} real->{r['real_expect']} control->{r['ctl_expect']}"
                  + (f"  needs {r['env']}" if r["env"] else ""))
        return 0
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) - 2)) as ex:
        results = list(ex.map(one, rows))
    bad = [r for r in results if not r["status"].startswith("OK") and not r["status"].startswith("SKIPPED")]
    md = ["# Campaign re-run (run_all_checks.py)", "", "| lane | script | control convention | real | control | status | secs |", "|---|---|---|---|---|---|---|"]
    for r in results:
        md.append(f"| {r['lane']} | {r['file']} | {r['convention']} | {r['real']} | {r['ctl']} | {r['status']} | {r['secs']:.0f} |")
    md.append("")
    md.append(f"{len(results)} scripts; OK {sum(1 for r in results if r['status'].startswith('OK'))}; skipped {sum(1 for r in results if r['status'].startswith('SKIPPED'))}; "
              f"problems {len(bad)}")
    open(os.path.join(HERE, "RUN_ALL_RESULTS.md"), "w").write("\n".join(md) + "\n")
    json.dump([{k: v for k, v in r.items() if k not in ("dir",)} for r in results], open(os.path.join(HERE, "RUN_ALL_RESULTS.json"), "w"), indent=1)
    print("\n".join(md[-1:]))
    for r in bad:
        print("  PROBLEM:", r["lane"], r["file"], r["status"], "real", r["real"], "ctl", r["ctl"])
    if "--lean" in sys.argv:
        ldir = os.path.join(ROOT, "fable_independent_2026", "lean_2026")
        for f, want in (("AH3_alpha_nogo.lean", 0), ("AH3_alpha_nogo_MUTATE.lean", 1), ("AH7_dimensional_obstruction.lean", 0),
                        ("AH7_dimensional_obstruction_MUTATE.lean", 1)):
            p = subprocess.run(["lake", "env", "lean", f], cwd=ldir, capture_output=True, timeout=1800)
            print(f"  lean {f}: exit {p.returncode} (expected {want}) {'OK' if p.returncode == want else 'MISMATCH'}")
            bad = bad if p.returncode == want else bad + [f]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
