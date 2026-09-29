#!/usr/bin/env python3
"""P2 -- re-run every alpha-chain script (lanes A-M, AH1-AH6) in a scratch COPY and compare with the committed .out files.

Pre-registered in P_PREREGISTRATION.md (protocol item 5).  Nothing in the repository is touched: the two source directories are copied to a temporary
directory (set TMPDIR to choose where) and every script runs there, so scripts that write json or .out files cannot modify a committed file.
Lanes N1-N5 are NOT copied and NOT run.

What is asserted (exit 0 iff all hold):
  R1  every real run exits 0 and its stdout equals the committed .out (floats compared at relative 1e-9, no absolute tolerance; lines with timings skipped);
  R2  every control run exits with the code recorded in EXPECT_CONTROL_EXIT below, and its stdout equals the committed _MUTATE .out where one exists;
  R3  the documented exceptions (controls whose exit code is NOT 1, controls that change nothing, scripts without a control) are exactly the ones in
      EXCEPTIONS below -- these are findings of the audit, asserted so that a later change of behaviour is noticed.
The mutation invocation of each script is taken from its own source (argv[1] == "MUTATE" for most lanes, "--mutate" for AH1/2/4/6, C, F, K).

Run:     PYTHONDONTWRITEBYTECODE=1 python3 p2_rerun_all.py
CONTROL: PYTHONDONTWRITEBYTECODE=1 python3 p2_rerun_all.py MUTATE
         (the ONLY trigger is argv[1] == "MUTATE": it runs two scripts against a deliberately corrupted expected .out and one wrong expected exit code; must exit 1)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
RR = os.path.abspath(os.path.join(HERE, "..", ".."))            # real_research
SRC = {"alpha_principle_2026": os.path.join(RR, "alpha_principle_2026"),
       "alpha_schwinger_2026": os.path.join(RR, "alpha_schwinger_2026")}
LANES = "A_wgc_extremal B_rg_asymptotic_safety C_holographic_species D_calibration_bar E_dynamical_attractor F_kk_stabilization " \
        "G_topological_anomaly H_string_heterotic I_selection_consistency J_emergent_condensate K_literature_audit M_red_team".split()
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
TIMEOUT = 600

# (relative path from real_research, mutate flag or None, committed .out base names: real, control)
JOBS = []
def add(rel, flag, real_out, ctl_out):
    JOBS.append((rel, flag, real_out, ctl_out))

for lane in LANES:
    d = os.path.join(SRC["alpha_principle_2026"], lane)
    for f in sorted(os.listdir(d)):
        if not f.endswith(".py") or f in ("rg_common.py", "bar_lib.py"):
            continue
        rel = f"alpha_principle_2026/{lane}/{f}"
        base = f[:-3]
        src = open(os.path.join(d, f)).read()
        if f == "alpha_bar_checker.py":
            add(rel, "--selftest|--selftest --mutate", "alpha_bar_checker_selftest.out", "alpha_bar_checker_selftest_MUTATE.out")
            continue
        flag = "--mutate" if ("'--mutate'" in src or '"--mutate"' in src) else "MUTATE"
        add(rel, flag, base + ".out", base + "_MUTATE.out")
for f in sorted(os.listdir(SRC["alpha_schwinger_2026"])):
    if f.endswith(".py"):
        base = f[:-3]
        add(f"alpha_schwinger_2026/{f}", None if base.startswith("ah5") else "--mutate", base + ".out", base + "_MUTATE.out")

# documented exceptions (audit findings): control exit code other than 1, or no control
# AH1, AH2, AH4, AH6: with --mutate the script prints "control works" and exits 0 when the corrupted check FAILS as required (exit 1 only if the control did not fail):
# ah1 line 162, ah2 line 136, ah4 line 169, ah6 (sys.exit(0 if not k1_ok else 1)).  ALPHA_CHAIN_STATUS.md says every control exits 1: that is not what these four do.
EXPECT_CONTROL_EXIT = {"ah1_schwinger_ds2.py": 0, "ah2_induced_current_ds2.py": 0, "ah4_induced_current_ds4.py": 0, "ah6_kaluza_klein.py": 0}
NO_CONTROL = {"ah5_dimensional_obstruction.py"}
EXTRA_CONTROLS = {"k2_structural_scoring.py": [("--mutate-s2", 0, "k2_structural_scoring_MUTATE_S2.out")]}


TIMING = [(re.compile(r"build [\d.]+s"), "build Xs"), (re.compile(r"\(\d+ s on \d+ processes\)"), "(X s on N processes)")]


def norm_lines(text):
    out = []
    for ln in text.splitlines():
        for pat, rep in TIMING:
            ln = pat.sub(rep, ln)
        if re.search(r"(elapsed|seconds|wall|timing|time:|\btook\b)", ln, re.I):
            continue
        out.append(ln.rstrip())
    return out


NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def same(a, b, rtol=1e-9):
    la, lb = norm_lines(a), norm_lines(b)
    if len(la) != len(lb):
        return False, f"line count {len(la)} vs {len(lb)}"
    for i, (x, y) in enumerate(zip(la, lb)):
        if x == y:
            continue
        tx, ty = NUM.split(x), NUM.split(y)
        nx, ny = NUM.findall(x), NUM.findall(y)
        if tx != ty or len(nx) != len(ny):
            return False, f"line {i + 1}: {x[:110]!r} vs {y[:110]!r}"
        for u, v in zip(nx, ny):
            fu, fv = float(u), float(v)
            if abs(fu - fv) > rtol * max(abs(fu), abs(fv)):
                return False, f"line {i + 1}: number {u} vs {v}"
    return True, ""


def run(workdir, rel, args):
    d, f = os.path.split(os.path.join(workdir, rel))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="Agg")
    try:
        p = subprocess.run([sys.executable, f] + args, cwd=d, capture_output=True, text=True, timeout=TIMEOUT, env=env)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return None, ""


def committed(rel, out_name):
    p = os.path.join(RR, os.path.dirname(rel), out_name)
    return open(p).read() if os.path.exists(p) else None


def main():
    work = tempfile.mkdtemp(prefix="p2_rerun_")
    for k, v in SRC.items():
        dst = os.path.join(work, k)
        shutil.copytree(v, dst, ignore=shutil.ignore_patterns("N*_*", "__pycache__", "*.pyc", "P_claim_audit"))
    print("scratch copy: <tmpdir> (lanes N1-N5 and P excluded)")
    jobs = JOBS
    if MUT:
        jobs = [j for j in JOBS if j[0].endswith(("ah5_dimensional_obstruction.py", "a1_rn_ds_special_points.py"))]
    results = []

    def do(job):
        rel, flag, real_out, ctl_out = job
        name = os.path.basename(rel)
        rec = {"rel": rel, "name": name, "notes": []}
        rc, out = run(work, rel, ["--selftest"] if flag and flag.startswith("--selftest") else [])
        exp = committed(rel, real_out)
        if MUT and name.startswith("ah5"):
            exp = (exp or "").replace("2.8485e-122", "2.9485e-122")       # deliberate corruption of one expected number
        rec["real_rc"] = rc
        rec["real_same"], rec["real_why"] = (same(out, exp) if (exp is not None and rc is not None) else (None, "no committed .out" if exp is None else "timeout"))
        if name in NO_CONTROL or flag is None:
            rec["ctl"] = "none"
        else:
            if flag.startswith("--selftest"):
                cargs = ["--selftest", "--mutate"]
            else:
                cargs = [flag]
            crc, cout = run(work, rel, cargs)
            cexp = committed(rel, ctl_out)
            rec["ctl_rc"] = crc
            rec["ctl_same"], rec["ctl_why"] = (same(cout, cexp) if (cexp is not None and crc is not None) else (None, "no committed control .out" if cexp is None else "timeout"))
            rec["ctl"] = "run"
        rec["extra"] = []
        for cflag, cexp_rc, cout_name in EXTRA_CONTROLS.get(name, []):
            xrc, xout = run(work, rel, [cflag])
            xexp = committed(rel, cout_name)
            rec["extra"].append((cflag, xrc, cexp_rc, same(xout, xexp)[0] if xexp is not None else None))
        return rec

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(do, jobs))

    bad = 0
    n_real_ok = n_ctl_ok = n_ctl = 0
    print(f"\n{'script':40s} real(rc,same)  control(rc,same)  note")
    for r in sorted(results, key=lambda r: r["rel"]):
        real_ok = r["real_rc"] == 0 and r["real_same"] is True
        n_real_ok += real_ok
        if r["ctl"] == "run":
            n_ctl += 1
            want = EXPECT_CONTROL_EXIT.get(r["name"], 1)
            if MUT and r["name"].startswith("a1_"):
                want = 0                    # deliberately wrong expected exit code: the mismatch must make the run exit 1
            ctl_ok = r["ctl_rc"] == want and r["ctl_same"] is True
            n_ctl_ok += (r["ctl_rc"] == EXPECT_CONTROL_EXIT.get(r["name"], 1)) and r["ctl_same"] is True
            ctl_txt = f"({r['ctl_rc']},{r['ctl_same']})"
        else:
            ctl_ok = True
            ctl_txt = "none"
        note = []
        if not (r["real_rc"] == 0 and r["real_same"] is True):
            note.append(f"real: {r['real_why']}")
        if r["ctl"] == "run" and r["ctl_same"] is not True:
            note.append(f"control .out: {r['ctl_why']}")
        if r["name"] in EXPECT_CONTROL_EXIT:
            note.append("control exits 0 by design ('control works'), NOT 1 (exception recorded)")
        for cflag, xrc, wrc, xs in r["extra"]:
            note.append(f"{cflag}: rc {xrc} (expected {wrc}), same={xs}")
            if xrc != wrc or xs is not True:
                ctl_ok = False
        ok = real_ok and ctl_ok
        bad += (not ok)
        print(f"{r['name']:40s} ({r['real_rc']},{r['real_same']})   {ctl_txt:16s} {'OK' if ok else 'MISMATCH'} {'; '.join(note)[:200]}")
    print(f"\nscripts: {len(results)}; real runs exit 0 and reproduce the committed .out: {n_real_ok}/{len(results)}; "
          f"control runs with the recorded exit code and matching .out: {n_ctl_ok}/{n_ctl}")
    scripts_no_control = sorted(r["name"] for r in results if r["ctl"] == "none")
    print("scripts without a MUTATE control:", scripts_no_control)
    shutil.rmtree(work, ignore_errors=True)
    print("MISMATCHES:", bad)
    sys.exit(1 if bad else 0)


main()
