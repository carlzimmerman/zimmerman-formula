#!/usr/bin/env python3
"""SP3 native (FROZEN_CRITERIA.md): one cell of ZN2's grader through OP3's worker, read only. Each cell cached, so the sweep resumes. kappa = 1/2 FITTED, unused; not theory closed.
  sp3_native.py MAP MAPN FQ [MB] [DELTA]    run one cell, print its row"""
import json, os, re, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN2_native_profile_sparc_groups"); OP3 = os.path.join(RB, "OP3_contraction_on_native"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; CD = os.path.join(HERE, "cells"); os.makedirs(CD, exist_ok=True)
def cell(mp, mapn, fq, mb=1, delta=0.0):
    o = os.path.join(CD, f"{mp}_{mapn}_f{fq:g}_m{mb:g}_d{delta:+.4f}.json")
    if os.path.exists(o): return json.load(open(o))
    WD = tempfile.mkdtemp(dir=os.path.join(HERE, "cache_native") if os.path.isdir(os.path.join(HERE, "cache_native")) else None); t = o + ".tmp"
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, ZN2_OUT=t, ZN2_WD=WD, ZN2_SHAPES=os.path.join(ZD, "zn2_low_shapes.json"), ZN2_MAP=mapn, ZN2_RX="1", ZN2_K1="", ZN2_TAGS="1e10,1e11,1e12,1e13,1e14", OP3_X=os.path.join(HERE, "sp3_x.py"), SP3_OP3X=os.path.join(OP3, "op3_x.py"), OP3_FQ=str(fq), OP3_MB=str(mb), SP3_MAP=mp, SP3_DELTA=str(delta), SP3_TABLES=os.path.join(HERE, "sp3_tables.json"), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(OP3, "op3.py"), "--worker"], cwd=WD, env=env, capture_output=True, text=True); shutil.rmtree(WD, ignore_errors=True)
    if not os.path.exists(t): raise SystemExit(f"NOT DECIDED {mp} {mapn} {fq}: exit {p.returncode}: {p.stdout[-600:]} {p.stderr[-1800:]}")
    os.replace(t, o); return json.load(open(o))
if __name__ == "__main__":
    a = sys.argv[1:]; r = cell(a[0], a[1], float(a[2]), float(a[3]) if len(a) > 3 else 1, float(a[4]) if len(a) > 4 else 0.0); s = r["sparc"]; x = r["sp3"]; print(a, [(round(s[t]["U_median"], 3), round(s[t]["rms"], 4)) for t in s], "tilt", x["tilt"], "LT", x["lt"], "groups", round(r["groups"]["Z"], 2), "bins", x["binsU"]["A_c2b_refit"], "below", r["stat"])
