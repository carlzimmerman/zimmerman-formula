#!/usr/bin/env python3
"""CN1 POST-RESULT, reported only: FC1's grader with the gravity-only baryon response (X39's Blumenthal + BCG) on clusters and none on SPARC. Median and CE1's 68 % ends, both f*.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; OUT = []
A4 = "--A4" in sys.argv; PRE = "CE1_A4" if A4 else "CE1"; TAG = "CN1b_A4" if A4 else "CN1b"
def P(s): print(s, flush=True); OUT.append(s)
T = open(os.path.join(HERE, "cn1_x74.py")).read(); a = 'sub("""        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)'; assert T.count(a) == 1
b = 'if a_ and ETA_USE["v"] == ETA and CN1_MODE != "off":\n            M2 = M200 * MSUNE'; assert T.count(b) == 1; T = T.replace(b, 'if False:\n            M2 = M200 * MSUNE'); W = os.path.join(HERE, "cn1b_x74.py"); open(W, "w").write(T)
def grade(tag, k, fs):
    names = [f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json"]
    env = dict(os.environ, CN1_R="1.0", CN1_MODE="blum", X74_CF=os.path.join(CE1, f"{PRE}_{k}_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "cn1b_x74.py"], cwd=WD, env=env, capture_output=True, text=True); open(os.path.join(WD, f"{tag}.log"), "w").write(p.stdout + p.stderr); out = {}
    for n in names:
        f = os.path.join(WD, n)
        if os.path.exists(f):
            d = os.path.join(HERE, f"{tag}_{n}"); os.replace(f, d)
            if d.endswith(".json"):
                out = json.load(open(d)); out["x74"]["cf_src"] = os.path.basename(out["x74"]["cf_src"]); json.dump(out, open(d, "w"), indent=1)
    if not out: raise SystemExit(f"NOT DECIDED: {tag} wrote no results (exit {p.returncode})")
    return out
WD = HERE; RES = {}
import shutil
WD = os.path.join(RB, "_cn1b_work"); os.makedirs(WD, exist_ok=True)   # a temporary sibling folder, so the running grid's outputs are untouched; removed at the end
T2 = T.replace('HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)', f'HERE = {WD!r}; REB = {RB!r}'); open(os.path.join(WD, "cn1b_x74.py"), "w").write(T2); os.remove(W)
for fs in ("0.034", "0.0615"):
    for k in ("med", "p16", "p84"):
        o = grade(f"{TAG}_{k}_fs{fs}", k, fs); RES[f"{k}_fs{fs}"] = {}
        for f in ("canonical", "alt"):
            F = o["footings"][f]; s = F["sparc"]; c = F["clusters"]["cells"]; z = {hk: {kk: v["Z"] for kk, v in c[hk].items()} for hk in c}; w = max(((kk, hk, zz) for hk in z for kk, zz in z[hk].items()), key=lambda t: abs(t[2]))
            RES[f"{k}_fs{fs}"][f] = dict(U={t: v["U_median"] for t, v in s.items()}, failing=F["failing"], groupsZ=F["groups"]["Z"], worst=w, inmall=z["h0672"]["G-IN-Mall"], t3=z["h0672"]["G-MID-T3"], m3=z["h0672"]["G-OUT-M3"], out_all=z["h0672"]["G-OUT-all"])
            r = RES[f"{k}_fs{fs}"][f]; P(f"  f* {fs} {k} [{f}] SPARC U {r['U']['A_c2b_refit']:.2f}/{r['U']['B_cfg886_bg']:.2f}; groups Z {r['groupsZ']:+.2f}; G-IN-Mall {r['inmall']:+.2f}; G-MID-T3 {r['t3']:+.2f}; G-OUT-M3 {r['m3']:+.2f}; G-OUT-all {r['out_all']:+.2f}; worst {w[0]} {w[2]:+.2f}; failing {r['failing']}")
json.dump(RES, open(os.path.join(HERE, f"{TAG.lower()}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG.lower()}.out"), "w").write("\n".join(OUT) + "\n"); shutil.rmtree(WD, ignore_errors=True)
