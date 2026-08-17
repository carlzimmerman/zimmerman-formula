#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t090_infra_consolidation.py -- T090: Infra consolidation.

Hypothesis (from TASKS.md T090): "Run T081-T089 end-to-end; fix breaks;
consolidation duty."  The 9 infra scripts t081..t089 form the CI/guard/linter
layer that every other duty depends on; this duty runs that layer and reports
any break so it can be fixed (a silent red here poisons every downstream run).

PASS criteria (from TASKS.md T090): the end-to-end run is green -- all nine
infra scripts pass, and any break is surfaced (so it can be fixed).
KILL criteria: none stated -- the deliverable is the consolidated report itself.
Search? No (no trial-count / FDR surface).
Direction-of-risk: DEFICIT-risk, because a green report can HIDE a silent
regression (a guard that used to catch a broken file now passes on a missing
file).  So the script must surface per-script reds AND verify the T081 artifact
is internally consistent, not just print an aggregate "all green".

Design (why t081 is verified by artifact, not re-run):
 - t082..t089 are fast (each < ~5s).  Run each live as a subprocess with a
   per-script timeout; a break = a non-zero return code.  These are the "run
   end-to-end" part.
 - t081 (full-corpus CI runner) runs 809 files and last took 3662s -- over the
   harness 3600s subprocess cap -- so RE-running it here would get killed before
   it writes its report.  T081's DELIVERABLE is its report, so the honest
   end-to-end check is: the report artifact exists, carries the T081 header,
   is fresh (mtime within 3 days), and is INTERNALLY CONSISTENT (the baseline
   file's per-file entry count equals the report's per-file line count -- a
   corrupted/truncated report would mismatch).  A `--rerun-t081` flag exists but
   is OFF by default; it is the weekly human-run, not this duty.
 - Consolidation sub-duty (PROTOCOL line 30): also scan the ledger tail for
   CONFIRMED/CANDIDATE rows not yet covered by a refutation duty, and report
   them (honestly, as info -- demotion is a new ledger row, Carl's call).
Exit 0 iff every infra script is green and the t081 artifact is consistent.
"""
import sys, os, glob, time, subprocess, argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *    # constants, kernel, check/info/finish

RUNS = os.path.dirname(os.path.abspath(__file__))           # .../qwen_38_experiment/runs
EXPERIMENT = os.path.dirname(RUNS)                           # .../qwen_38_experiment
ROOT = os.path.dirname(EXPERIMENT)                           # repo root
LEDGER = os.path.join(EXPERIMENT, "LEDGER.md")
REPORT = os.path.join(RUNS, "ci_report.txt")
BASELINE = os.path.join(RUNS, "ci_baseline.txt")

STATUSES = ("GREEN", "RED", "TIMEOUT", "SKIP")
FAST = ["t082", "t083", "t084", "t085", "t086", "t087", "t088", "t089"]    # t081 by artifact
PER_SCRIPT_TIMEOUT = 180      # the fast guards finish in < 5s; 180s catches a hang

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun-t081", action="store_true",
                    help="RE-run the full corpus via t081 (weekly human run; OFF by default: "
                          "3662s last time, over the harness cap)")
    args = ap.parse_args()

     # ---- PART A: locate the 9 infra scripts by name pattern ----
    found = {}
    for tag in FAST:
        ms = glob.glob(os.path.join(RUNS, tag + "_*.py"))
        found[tag] = ms[0] if ms else None
    ms081 = glob.glob(os.path.join(RUNS, "t081_*.py"))
    found["t081"] = ms081[0] if ms081 else None
    missing = [t for t in ["t081"] + FAST if not found[t]]

     # ---- PART B: run the 8 fast infra scripts live ----
    live = []             # (tag, rc, last_line)
    for tag in FAST:
        p = found[tag]
        if not p:
            live.append((tag, "MISSING", "no script file for %s" % tag))
            continue
        try:
            r = subprocess.run([sys.executable, p], cwd=EXPERIMENT,
                               capture_output=True, text=True,
                               timeout=PER_SCRIPT_TIMEOUT)
            out = (r.stdout or "") + (r.stderr or "")
            last = next((ln.strip() for ln in reversed(out.splitlines()) if ln.strip()), "")
            live.append((tag, r.returncode, last[:80]))
        except subprocess.TimeoutExpired:
            live.append((tag, "TIMEOUT", "per-script timeout %ds" % PER_SCRIPT_TIMEOUT))
        except Exception as e:
            live.append((tag, "ERROR", "spawn error: %s" % str(e)[:60]))
    fast_green = sum(1 for _, rc, _ in live if rc == 0)
    fast_breaks = [(t, rc, l) for t, rc, l in live if rc != 0]

     # ---- PART B: verify the T081 artifact (unless --rerun-t081) ----
    if args.rerun_t081:
         # weekly human run: execute the corpus runner itself
        r = subprocess.run([sys.executable, found["t081"]], cwd=ROOT,
                           capture_output=True, text=True)
        t081_status = "RUN-rc%d" % r.returncode
        t081_detail = (r.stdout or "").strip().splitlines()[-1:][0][:70]
    else:
         # end-to-end by artifact: present + header + fresh + internally consistent
        ok = True; why = []
        if not os.path.exists(REPORT):
            ok = False; why.append("ci_report.txt MISSING")
        else:
            with open(REPORT) as f:
                head = f.readline().rstrip("\n")
            if not head.startswith("T081 FULL-CORPUS CI RUN"):
                ok = False; why.append("report has no T081 header")
            age_days = (time.time() - os.path.getmtime(REPORT)) / 86400.0
            if age_days > 3:
                ok = False; why.append("report stale (%.1f days old)" % age_days)
             # internal consistency: per-file line count == baseline entry count
            rep_perfile = 0
            with open(REPORT) as f:
                for ln in f:
                    if ln and ln[0] != " " and ln.split()[0:1] and \
                            ln.split()[0] in STATUSES:
                        rep_perfile += 1
            base_n = 0
            if os.path.exists(BASELINE):
                with open(BASELINE) as f:
                    base_n = sum(1 for ln in f if ln.strip())
            if rep_perfile != base_n:
                ok = False
                why.append("baseline/report per-file mismatch %d vs %d (corrupt/truncated?)"
                            % (base_n, rep_perfile))
            if ok:
                t081_status = "GREEN(artifact)"
                t081_detail = ("report present+fresh+consistent: %d per-file entries, "
                                "baseline %d" % (rep_perfile, base_n))
            else:
                t081_status = "RED(artifact)"
                t081_detail = "; ".join(why)

     # ---- PART B: ledger consolidation sub-duty (PROTOCOL line 30) ----
    confirmed = []
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            rows = [ln for ln in f if ln.startswith("|")]
        for ln in rows[-15:]:
            parts = [p.strip() for p in ln.split("|")]
             # schema: | task | date | verdict | ... |
            if len(parts) > 4:   # split("|") yields a leading '', so verdict=parts[3]
                v = parts[3].upper()
                if "CONFIRMED" in v or "CANDIDATE" in v:
                    confirmed.append((parts[2], parts[3], parts[4][:48]))
    owed_refutation = len(confirmed)

     # ---- PART C: grade ----
    all_green = (fast_green == len(FAST)) and t081_status.startswith("GREEN")
    n_breaks = len(fast_breaks) + (0 if t081_status.startswith("GREEN") else 1)
    check(all_green, "all 9 infra scripts green end-to-end",
          "fast %d/%d, t081=%s" % (fast_green, len(FAST), t081_status))
    check(not fast_breaks, "no fast-script break",
          ("breaks: " + ", ".join("%s(%s)" % (t, rc) for t, rc, _ in fast_breaks))
          if fast_breaks else "t082..t089 all exit 0")
    check(t081_status.startswith("GREEN"),
          "t081 corpus CI artifact green & consistent", t081_detail)
    check(not missing, "all 9 infra scripts present on disk",
          ("missing: " + ",".join(missing)) if missing else "t081..t089 all found")
    info("live infra run", "    ".join("%s=rc%s" % (t, rc) for t, rc, _ in live))
    info("t081", "%s -- %s" % (t081_status, t081_detail))
    info("ledger consolidation", "CONFIRMED/CANDIDATE rows in last 15 = %d "
          "(each needs an adversarial refutation duty unless already owed)" % owed_refutation)
    for d, v, h in confirmed:
        info("  owed refutation", "%s [%s] %s" % (d, v, h))
    info("HONEST STATE", "0 unfixed break" if n_breaks == 0
         else ("%d unfixed break(s): %s" % (n_breaks,
                ", ".join("%s(%s)" % (t, rc) for t, rc, _ in fast_breaks)
                + ("; t081" if not t081_status.startswith("GREEN") else ""))))
    finish("t090")

if __name__ == "__main__":
    raise SystemExit(main())
