#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
run_chain -- assemble the first-principles derivation chain from its lanes (FP0, FP1, ...) into one status ledger.

For every lane FPn_*.py in this directory it reads the committed outputs (or, with --rerun, re-executes the lane and its
MUTATE control), and checks the chain's contract:
  * the main run's verdict line "N/M checks pass; load-bearing failures: K" and its exit code;
  * the MUTATE control exists and FAILS (rc = 1): a lane whose control does not flip proves nothing;
  * the lane's own ledger entries (link, status, basis), where status is one of
    DERIVED / POSTULATED / FITTED / CONSTRAINT / OPEN / FAILS.
It writes CHAIN_STATUS.md (the ledger in one table, lane by lane) and exits 1 if any lane breaks the contract.

Usage (from the repository root):
  python3 real_research/derivation_chain_2026/run_chain.py            # collect from the existing outputs
  python3 real_research/derivation_chain_2026/run_chain.py --rerun    # re-execute every lane (main + MUTATE) first
  python3 real_research/derivation_chain_2026/run_chain.py --only FP0 # one lane
"""
import os, re, sys, glob, json, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
STATUSES = ("DERIVED", "POSTULATED", "FITTED", "CONSTRAINT", "OPEN", "FAILS")


def lanes(only=None):
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "FP[0-9]*_*.py"))):
        stem = os.path.basename(p)[:-3]
        tag = stem.split("_", 1)[0]
        if only and tag not in only:
            continue
        out.append((tag, stem, p))
    return sorted(out, key=lambda t: (int(re.sub(r"\D", "", t[0]) or 0), t[1]))


def run(path, mutate, timeout=1800):
    stem = os.path.basename(path)[:-3]
    outp = os.path.join(HERE, stem + ("_MUTATE" if mutate else "") + ".out")
    env = dict(os.environ, MUTATE="1" if mutate else "0")
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, path], cwd=os.path.dirname(os.path.dirname(HERE)), env=env,
                           capture_output=True, text=True, timeout=timeout)
        txt, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        txt, rc = f"TIMEOUT after {timeout}s\n", 124
    open(outp, "w").write(txt + f"rc={rc}\n")
    return rc, time.time() - t0


def read_out(stem, mutate):
    p = os.path.join(HERE, stem + ("_MUTATE" if mutate else "") + ".out")
    if not os.path.exists(p):
        return None
    t = open(p, errors="replace").read()
    rc = re.findall(r"^rc=(\d+)", t, re.M)
    verdict = re.findall(r"(\d+)/(\d+) checks pass; load-bearing failures: (\d+)", t)
    return dict(rc=int(rc[-1]) if rc else None, verdict=verdict[-1] if verdict else None,
                traceback="Traceback (most recent call last)" in t)


def read_json(stem, mutate):
    cands = [f"{stem}_results{'_MUTATE' if mutate else ''}.json"]
    if mutate:
        cands.append(f"{stem}_MUTATE_results.json")
    for c in cands:
        p = os.path.join(HERE, c)
        if os.path.exists(p):
            try:
                return json.load(open(p))
            except Exception:
                return None
    return None


def main():
    args = sys.argv[1:]
    rerun = "--rerun" in args
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    rows, ledger, broken = [], [], []
    for tag, stem, path in lanes(only):
        if rerun:
            for mut in (False, True):
                rc, dt = run(path, mut)
                print(f"  ran {stem}{' MUTATE' if mut else ''}: rc={rc} ({dt:.0f}s)", flush=True)
        m, mu = read_out(stem, False), read_out(stem, True)
        j = read_json(stem, False) or {}
        problems = []
        if m is None:
            problems.append("no main output")
        elif m["traceback"]:
            problems.append("main run crashed (Traceback)")
        elif m["verdict"] is None:
            problems.append("main run has no verdict line")
        if mu is None:
            problems.append("no MUTATE output")
        elif mu["rc"] != 1 or mu["traceback"]:
            problems.append(f"MUTATE control did not flip cleanly (rc={mu['rc']}, traceback={mu['traceback']})")
        if problems:
            broken.append((stem, problems))
        v = m["verdict"] if m and m["verdict"] else ("?", "?", "?")
        rows.append((tag, stem, f"{v[0]}/{v[1]}", v[2], m["rc"] if m else None, mu["rc"] if mu else None,
                     "; ".join(problems) or "ok"))
        for e in j.get("ledger", []) or []:
            st = str(e.get("status", "")).upper()
            ledger.append((tag, e.get("link", ""), st if st in STATUSES else f"?{st}", e.get("what", ""), e.get("basis", "")))

    lines = ["# The first-principles derivation chain -- status ledger", "",
             f"Assembled by `run_chain.py` on {time.strftime('%Y-%m-%d %H:%M')}. A lane counts only if its main run has a verdict "
             "and its MUTATE control flips (rc = 1). Status meanings: DERIVED (varied out of the chain above it, with a script), "
             "POSTULATED (an input), FITTED (a constant set by data), CONSTRAINT (a derived requirement on a lower link), "
             "OPEN (owed), FAILS (derived and contradicted by data).", "",
             "## Lanes", "", "| lane | checks | load-bearing failures | main rc | MUTATE rc | contract |", "|---|---|---|---|---|---|"]
    lines += [f"| {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |" for r in rows]
    lines += ["", "## Links", "", "| lane | link | status | what | basis |", "|---|---|---|---|---|"]
    lines += [f"| {t} | {k} | {s} | {w} | {b} |" for t, k, s, w, b in ledger]
    counts = {s: sum(1 for x in ledger if x[2] == s) for s in STATUSES}
    lines += ["", "Totals: " + ", ".join(f"{s} {n}" for s, n in counts.items()), ""]
    open(os.path.join(HERE, "CHAIN_STATUS.md"), "w").write("\n".join(lines))
    print("\n".join(lines))
    if broken:
        print("\nCONTRACT BROKEN:")
        for s, p in broken:
            print(f"  {s}: {'; '.join(p)}")
    print(f"\n  {len(rows)} lanes, {len(ledger)} links; contract broken in {len(broken)}; wrote CHAIN_STATUS.md")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
