#!/usr/bin/env python3
"""PZ1, SCALING ONLY: LC1's lc1_x74.py route, read only, with CN1's contraction scaled by a measured f_Q; rule with floor, CE1's ng 64 table; one 10^12 number carried across SPARC's masses. Not a run of version N. Raw outputs in cache_sparc/.
    python3 pz1_sparc.py 0.872 [0.8 ...]; the first call at 0.872 must reproduce LC1. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); CE1 = os.path.join(REB, "CE1_converged_eta_grade"); LC1 = os.path.join(REB, "LC1_live_contraction"); CA = os.path.join(HERE, "cache_sparc"); os.makedirs(CA, exist_ok=True); FS, SL = "0.034", "2.7774425603108597"; S = f"fs0.034_nat_s2.7774"
DR = "import os; p = os.path.join(%r, 'lc1_x74.py'); exec(compile(open(os.path.join(%r, 'lc1_x74.py')).read(), p, 'exec'), {'__file__': p, '__name__': '__main__'})" % (HERE, LC1)
def run(fq):
    env = dict(os.environ, CN1_R="1.0", CN1_MODE="blum", LC1_FQ=str(fq), X74_CF=os.path.join(CE1, "CE1_A4_med_fs0.034_cf_table.json"), X73_FSTAR=FS, X73_SLOPE=SL, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "-c", DR], cwd=HERE, env=env, capture_output=True, text=True); open(os.path.join(CA, f"fq{fq}.log"), "w").write(p.stdout + p.stderr); f = os.path.join(HERE, f"x74_results_{S}.json")
    if not os.path.exists(f): raise SystemExit(f"no results at f_Q {fq}: see cache_sparc/fq{fq}.log")
    d = json.load(open(f))
    for q in os.listdir(HERE):
        if q.startswith("x74_"): os.replace(os.path.join(HERE, q), os.path.join(CA, f"fq{fq}_{q}"))
    return {k: {t: (v["U_median"], v["rms"]) for t, v in d["footings"][k]["sparc"].items()} for k in d["footings"]}
L = json.load(open(os.path.join(LC1, f"lc1_fq0.872_x74_results_{S}.json"))); base = {k: {t: (v["U_median"], v["rms"]) for t, v in L["footings"][k]["sparc"].items()} for k in L["footings"]}
OUT = ["PZ1, SCALING ONLY: LC1's route, rule with floor, CE1's ng 64 table, one 10^12 number carried across SPARC's masses; not version N; kappa = 1/2 FITTED; not theory closed"]; good = True
for fq in sys.argv[1:]:
    r = run(fq); OUT.append(f"f_Q {fq}: " + "; ".join(f"{k}: " + ", ".join(f"{t} U {u:.3f} rms {s:.4f}" for t, (u, s) in v.items()) for k, v in r.items()))
    if fq == "0.872":
        d = max(abs(a - b) for k in r for t in r[k] for a, b in zip(r[k][t], base[k][t])); good = d <= 1e-6; OUT.append(f"K7 reproduces LC1's own result at 0.872: max |d| {d:.1e}: {'PASS' if good else 'FAIL'}")
    print(OUT[-1], flush=True)
open(os.path.join(HERE, "pz1_sparc.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if good else 1)
