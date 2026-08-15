#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t081_ci_runner.py -- T081: Full-corpus CI runner.

Hypothesis (from TASKS.md): a script that runs every nbody_2026/stage*.py and
real_research/reviews/*.py and reports green/red with runtimes.
PASS criteria (verbatim): "the report (catches bit-rot; run weekly)."
KILL criteria: none stated -- the deliverable is the report itself.
Search? No (no trial-count / FDR surface).
Direction-of-risk: DEFICIT-risk, because a green report can flatter the framework by
hiding a silent regression (a stage that used to pass now crashing). The runner must
therefore surface per-file reds AND a baseline delta, not just an aggregate pass count.

Design:
 - Discover the two globs relative to the repo root (parent of qwen_38_experiment/).
 - Run each file as a subprocess with a per-file timeout; capture returncode, runtime,
   and the last non-empty output line. GREEN = rc==0 (finished). RED = crash/fail-check.
   TIMEOUT is a distinct red (bit-rot: a stage that used to finish now hangs).
 - Write a full report to runs/ci_report.txt and print a summary to stdout.
 - Bit-rot: compare the current green/red set to runs/ci_baseline.txt (if present).
   First run establishes the baseline; later runs flag any green<->red flip.
 - Exit 0 iff the enumeration completed and the report was written (the report is the
   deliverable). A red individual file does NOT make the runner fail -- the runner's job
   is to REPORT reds, and it did.
"""
import sys, os, glob, time, subprocess, datetime

RUNS = os.path.dirname(os.path.abspath(__file__))       # .../qwen_38_experiment/runs
EXPERIMENT = os.path.dirname(RUNS)                       # .../qwen_38_experiment
ROOT = os.path.dirname(EXPERIMENT)                       # repo root (holds nbody_2026, real_research)
REPORT = os.path.join(RUNS, "ci_report.txt")
BASELINE = os.path.join(RUNS, "ci_baseline.txt")

PER_FILE_TIMEOUT = 600      # seconds; a stage that cannot finish in this is a TIMEOUT red
GLOBAL_BUDGET = 3300        # seconds; stay under the harness 3600s subprocess cap
SEP = "    "                # 3-space column separator used by the baseline file

def discover():
    files = []
    files += sorted(glob.glob(os.path.join(ROOT, "nbody_2026", "stage*.py")))
    files += sorted(glob.glob(os.path.join(ROOT, "real_research", "reviews", "*.py")))
    seen, out = set(), []
    for f in files:
        af = os.path.abspath(f)
        if af not in seen:
            seen.add(af)
            out.append(af)
    return out

def run_one(path):
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, path], cwd=ROOT,
                           capture_output=True, text=True, timeout=PER_FILE_TIMEOUT)
        dt = time.time() - t0
        out = (r.stdout or "") + (r.stderr or "")
        last = next((ln.strip() for ln in reversed(out.splitlines()) if ln.strip()), "")
        if r.returncode == 0:
            return ("GREEN", round(dt, 1), last[:80])
        elif r.returncode in (124, 137):
            return ("TIMEOUT", round(dt, 1), last[:80])
        else:
            return ("RED", round(dt, 1), last[:80])
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", round(time.time() - t0, 1), "hard per-file timeout")
    except Exception as e:
        return ("RED", round(time.time() - t0, 1), "spawn error: %s" % str(e)[:70])

def main():
    files = discover()
    n = len(files)
    results = []
    deadline = time.time() + GLOBAL_BUDGET
    for i, p in enumerate(files):
        if time.time() > deadline:
            results.append((os.path.relpath(p, ROOT), "SKIP", -1.0,
                            "global budget %ds exceeded" % GLOBAL_BUDGET))
            continue
        rel = os.path.relpath(p, ROOT)
        status, dt, last = run_one(p)
        results.append((rel, status, dt, last))
        print("[%d/%d] %-7s %7.1fs   %s" % (i + 1, n, status, dt, rel))
    # finalize
    greens = [r for r in results if r[1] == "GREEN"]
    reds = [r for r in results if r[1] in ("RED", "TIMEOUT", "SKIP")]
    total_dt = sum(r[2] for r in results if r[2] >= 0)
    lines = []
    lines.append("T081 FULL-CORPUS CI RUN   %s" % datetime.date.today())
    lines.append("files discovered: %d   GREEN: %d    RED/TIMEOUT/SKIP: %d   total runtime: %.1fs"
                 % (n, len(greens), len(reds), total_dt))
    lines.append("=" * 78)
    for rel, status, dt, last in results:
        lines.append("%-7s %7.1fs   %s    %s" % (status, dt, rel, last))
    # bit-rot delta vs baseline
    prev = {}
    if os.path.exists(BASELINE) and os.path.getsize(BASELINE) > 0:
        with open(BASELINE) as f:
            for ln in f:
                parts = ln.rstrip("\n").split(SEP, 1)
                if len(parts) == 2 and parts[0] in ("GREEN", "RED", "TIMEOUT", "SKIP"):
                    prev[parts[1]] = parts[0]
    curmap = {rel: status for rel, status, dt, last in results}
    flips = []
    if prev:
        for rel in sorted(set(prev) | set(curmap)):
            p0, p1 = prev.get(rel, "ABSENT"), curmap.get(rel, "ABSENT")
            if p0 != p1:
                flips.append("     %s: %s -> %s" % (rel, p0, p1))
    lines.append("=" * 78)
    if not prev:
        lines.append("BIT-ROT vs baseline: none (first run -- baseline now established)")
    else:
        lines.append("BIT-ROT vs baseline: %d status flip(s)" % len(flips))
        lines.extend(flips)
    with open(REPORT, "w") as f:
        f.write("\n".join(lines) + "\n")
    # snapshot the current green/red set as the new baseline for next week's run
    with open(BASELINE, "w") as f:
        for rel, status, dt, last in results:
            f.write("%s%s%s\n" % (status, SEP, rel))
    print("=" * 78)
    print("REPORT -> %s" % os.path.relpath(REPORT, ROOT))
    print("GREEN %d/%d   RED/TIMEOUT/SKIP %d    total %.1fs   baseline %s"
          % (len(greens), n, len(reds), total_dt,
             "compared" if prev else "established"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
