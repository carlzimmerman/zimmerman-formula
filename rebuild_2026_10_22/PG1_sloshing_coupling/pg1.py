#!/usr/bin/env python3
"""PG1 (FROZEN_CRITERIA.md): ER1's path with the sloshing factor on the budget. eps FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN2_native_profile_sparc_groups"); ZG = os.path.join(ZD, "zn2_grade.py"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"
if "--worker" in sys.argv:
    T = open(ZG).read(); a = "TX = TX.replace(A, INJ + MY + A)"; assert T.count(a) == 1; T = T.replace(a, 'TX = TX.replace(A, INJ + MY + open(os.environ["OP3_X"]).read() + A)').replace("HERE = os.path.dirname(os.path.abspath(__file__)); RB =", f"HERE = {ZD!r}; RB =", 1)
    exec(compile(T, ZG, "exec"), {"__file__": ZG, "__name__": "__main__"}); sys.exit(0)
TD = tempfile.mkdtemp(); R = {}
def run(j):
    lab, fq, eps, bh, mult = j; WD = os.path.join(TD, re.sub(r"\W", "_", lab)); os.makedirs(WD); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, ZN2_OUT=o, ZN2_WD=WD, ZN2_SHAPES=os.path.join(ZD, "zn2_low_shapes.json"), ZN2_MAP="tot", ZN2_RX="1", ZN2_K1="", ZN2_TAGS="1e10,1e11,1e12,1e13,1e14", OP3_X=os.path.join(HERE, "pg1_x.py"), OP3_FQ=str(fq), OP3_MB="1", ER1_EPS="" if eps is None else str(eps * mult), ER1_BH="1" if bh else "0", PG1_MULT="0.01" if lab.startswith("MUT") else "1", PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED {lab} exit {p.returncode}: {p.stdout[-400:]} {p.stderr[-1500:]}")
    D = json.load(open(o)); print(lab, D["sparc"]["A_c2b_refit"]["U_median"], D["tilt"], flush=True); return lab, D
J = [(f"SN_e{e_}", .872, e_, False, 1) for e_ in (.01, .03, .1, .2, .285, .46, .7, 1.0, 1e3, 1e-12)] + [("MUT_e0.285", .872, .285, False, 1)]
with ThreadPoolExecutor(2) as ex:
    for lab, D in ex.map(run, J):
        R[lab] = {k: D.get(k) for k in ("sparc", "groups", "bins3", "tilt", "pg1F")}; json.dump(R, open(os.path.join(HERE, "pg1_results.json"), "w"), default=float)
