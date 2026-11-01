#!/usr/bin/env python3
"""OP3 (FROZEN_CRITERIA.md): LC1's contraction on the native profile, SPARC. Drives ZN2's grader with op3_x.py added; ZN2's files read only."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN2_native_profile_sparc_groups"); ZG = os.path.join(ZD, "zn2_grade.py"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"
if "--worker" in sys.argv:
    T = open(ZG).read(); a = "TX = TX.replace(A, INJ + MY + A)"; assert T.count(a) == 1; T = T.replace(a, 'TX = TX.replace(A, INJ + MY + open(os.environ["OP3_X"]).read() + A)').replace("HERE = os.path.dirname(os.path.abspath(__file__)); RB =", f"HERE = {ZD!r}; RB =", 1)
    exec(compile(T, ZG, "exec"), {"__file__": ZG, "__name__": "__main__"}); sys.exit(0)
TD = tempfile.mkdtemp(); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def run(j):
    lab, mp, fq, mb = j; WD = os.path.join(TD, re.sub(r"\W", "_", lab)); os.makedirs(WD); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, ZN2_OUT=o, ZN2_WD=WD, ZN2_SHAPES=os.path.join(ZD, "zn2_low_shapes.json"), ZN2_MAP=mp, ZN2_RX="1", ZN2_K1="", ZN2_TAGS="1e10,1e11,1e12,1e13,1e14", OP3_X=os.path.join(HERE, "op3_x.py"), OP3_FQ=str(fq), OP3_MB=str(mb), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED {lab} exit {p.returncode}: {p.stdout[-400:]} {p.stderr[-1500:]}")
    return lab, json.load(open(o))
J = [("K1 frozen f_Q 0", "tot", 0.0, 1), ("PRIMARY frozen map f_Q 0.872", "tot", 0.872, 1), ("frozen map f_Q 1", "tot", 1.0, 1), ("FC1 map f_Q 0.872", "fc1", 0.872, 1), ("MUTATE frozen f_Q 0.872 M_b x 2", "tot", 0.872, 2)]
with ThreadPoolExecutor(3) as ex: RR = dict(ex.map(run, J))
for lab, R in RR.items():
    s = R["sparc"]; P(f"{lab}: " + "; ".join(f"[{t[:1]}] rms {s[t]['rms']:.4f} U {s[t]['U_median']:.2f} {'PASS' if s[t]['line'] else 'FAIL'}" for t in s) + f"; groups Z {R['groups']['Z']:+.2f}"); P("   by V_flat U/dV: " + "; ".join(f"{k} (n {v['n']}) {v['U']:.2f}/{v['dV']:+.1f}" for k, v in R["bins3"].items()))
s = RR["PRIMARY frozen map f_Q 0.872"]["sparc"]; L = all(s[t]["line"] for t in s); U = min(s[t]["U_median"] for t in s); V = "CONTRACTION KEEPS THE LINE" if L else "BREAKS IT (U low)" if U < .5 else "FAILS HIGH"
k = RR["K1 frozen f_Q 0"]["sparc"]; P(f"VERDICT: {V}. K1 U {[round(k[t]['U_median'],3) for t in k]} rms {[round(k[t]['rms'],4) for t in k]} against 0.84/0.81, 0.0829/0.0800"); json.dump(dict(verdict=V, runs=RR), open(os.path.join(HERE, "op3_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "op3.out"), "w").write("\n".join(OUT) + "\n")
