#!/usr/bin/env python3
"""FC1_cold_share_native_eta (criteria 061b2e2a1a): route E's full grader with S_cold = f_c eta Sigma_coll(M/f_c), f_c = R_nat/(1+R_nat).
    python3 fc1_grade.py          # K1-K4, graded runs, variant, MUTATE (cluster masses at ng 48)
    python3 fc1_grade.py --A4     # same grade on CE1's A4 tables; outputs FC1_A4_*
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade")
A4 = "--A4" in sys.argv; PRE = "CE1_A4" if A4 else "CE1"; TAG = "FC1_A4" if A4 else "FC1"
SLOPE = "2.7774425603108597"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def table(k, fs): return os.path.join(CE1, f"{PRE}_{k}_fs{fs}_cf_table.json")
def grade(tag, mode, k, fs):
    names = [f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json"]
    env = dict(os.environ, FC1_MODE=mode, X74_CF=table(k, fs), X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "fc1_x74.py"], cwd=HERE, env=env, capture_output=True, text=True)
    open(os.path.join(HERE, f"{tag}.log"), "w").write(p.stdout + p.stderr); out = {}
    for n in names:
        f = os.path.join(HERE, n)
        if os.path.exists(f):
            d = os.path.join(HERE, f"{tag}_{n}"); os.replace(f, d)
            if d.endswith(".json"):
                out = json.load(open(d)); out["x74"]["cf_src"] = os.path.basename(out["x74"]["cf_src"]); json.dump(out, open(d, "w"), indent=1)   # no local path in the record
    if not out: raise SystemExit(f"NOT DECIDED: run {tag} wrote no results (exit {p.returncode}); see {tag}.log")
    return out
def summ(R, foot):
    F = R["footings"][foot]; s = F["sparc"]; cells = F["clusters"]["cells"]; zs = [(k, hk, c["Z"]) for hk in cells for k, c in cells[hk].items()]
    w = max(zs, key=lambda t: abs(t[2])); return dict(verdict=F["verdict"], failing=F["failing"], groupsZ=F["groups"]["Z"], sparc_line=all(v["line"] for v in s.values()),
        U={k: v["U_median"] for k, v in s.items()}, rms={k: v["rms"] for k, v in s.items()}, worst=dict(key=w[0], cell=w[1], Z=w[2]), inmall={hk: cells[hk]["G-IN-Mall"]["Z"] for hk in cells}, midt3={hk: cells[hk]["G-MID-T3"]["Z"] for hk in cells})
def ok(s): return s["sparc_line"] and not s["failing"]
def line(tag, s): return f"  {tag}: {'PASS' if ok(s) else 'FAIL'}; SPARC U {s['U']['A_c2b_refit']:.2f}/{s['U']['B_cfg886_bg']:.2f} rms {s['rms']['A_c2b_refit']:.4f}; groups Z {s['groupsZ']:+.2f}; worst {s['worst']['key']} {s['worst']['Z']:+.2f}; G-IN-Mall {s['inmall']['h0672']:+.2f}; G-MID-T3 {s['midt3']['h0672']:+.2f}; failing {s['failing']}"
P(f"{TAG}: route E grader, cold share of native eta; kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("" if A4 else " [cluster masses ng 48]"))
RES = dict(checks={}, runs={}, labels={}); good = True
if not A4:
    K = grade("FC1_K1", "none", "med", "0.034"); G = json.load(open(os.path.join(CE1, "CE1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))
    d = max(abs(K["footings"][f]["sparc"][t][q] - G["footings"][f]["sparc"][t][q]) for f in ("canonical", "alt") for t in G["footings"][f]["sparc"] for q in ("rms", "U_median"))
    dc = max(abs(K["footings"][f]["clusters"]["cells"][h][k]["pred"] - G["footings"][f]["clusters"]["cells"][h][k]["pred"]) for f in ("canonical", "alt") for h in G["footings"][f]["clusters"]["cells"] for k in G["footings"][f]["clusters"]["cells"][h])
    RES["checks"]["K1"] = max(d, dc) <= 1e-9; good &= RES["checks"]["K1"]; P(f"K1 factor 1 reproduces CE1 (SPARC rms/U, cluster preds, both footings): SPARC {d:.1e}, clusters {dc:.1e}: {'PASS' if RES['checks']['K1'] else 'FAIL'}")
for fs in ("0.034", "0.0615"):
    for k in ("med", "p16", "p84"):
        R = grade(f"{TAG}_{k}_fs{fs}", "cold", k, fs); RES["runs"][f"{k}_fs{fs}"] = {f: summ(R, f) for f in ("canonical", "alt")}
        if k == "med" and fs == "0.034":
            x = R["x74"]; fc = x["fc1"]
            d3 = [abs(fc["S_over_Scoll"][str(l)] - fc["F"] * x["eta"][f"1e{l}"]) for l in (12, 13, 14)]
            RES["checks"]["K2"] = max(fc["k2"]) <= 1e-9; RES["checks"]["K3"] = max(d3) <= 1e-3; RES["checks"]["K4"] = abs(fc["f_c_bgA"] - fc["f_c"]) <= 0.01; good &= RES["checks"]["K2"] and RES["checks"]["K3"] and RES["checks"]["K4"]
            P(f"K2 solve_r0 scale identity max {max(fc['k2']):.1e}: {'PASS' if RES['checks']['K2'] else 'FAIL'}")
            P(f"K3 S/Sigma_coll at nodes {[round(fc['S_over_Scoll'][str(l)], 3) for l in (12, 13, 14)]} vs f_c x table, max |d| {max(d3):.1e}: {'PASS' if RES['checks']['K3'] else 'FAIL'}")
            P(f"K4 f_c {fc['f_c']:.5f}; background A 1-fb {fc['f_c_bgA']:.5f}, B {fc['f_c_bgB']:.5f}: {'PASS' if RES['checks']['K4'] else 'FAIL'}"); RES["fc1"] = fc; RES["eta_table"] = x["eta"]
        for f in ("canonical", "alt"): P(line(f"f* {fs} {k} [{f}]", RES["runs"][f"{k}_fs{fs}"][f]))
for f in ("canonical", "alt"):
    med = [ok(RES["runs"][f"med_fs{fs}"][f]) for fs in ("0.034", "0.0615")]; ends = [ok(RES["runs"][f"{k}_fs{fs}"][f]) for fs in ("0.034", "0.0615") for k in ("p16", "p84")]
    L = "COLD-SHARE PASS" if all(med) and all(ends) else "KNIFE EDGE" if all(med) else "F*-DEPENDENT" if any(med) else "COLD-SHARE FAIL"
    if not good: L = "NOT DECIDED (" + L + " before a failed check)"
    RES["labels"][f] = L; P(f"LABEL [{f}]: {L}" + ("" if A4 else " [cluster masses ng 48]") + f"; median per f* {med}; ends {ends}")
P("Reported, not graded: factor on S only")
for fs in ("0.034", "0.0615"):
    R = grade(f"{TAG}_Sonly_fs{fs}", "sonly", "med", fs); RES["runs"][f"Sonly_fs{fs}"] = {f: summ(R, f) for f in ("canonical", "alt")}
    for f in ("canonical", "alt"): P(line(f"S only f* {fs} [{f}]", RES["runs"][f"Sonly_fs{fs}"][f]))
if not A4:
    R = grade("FC1_MUTATE", "mut", "med", "0.034"); m = summ(R, "canonical"); b = RES["runs"]["med_fs0.034"]["canonical"]
    Gm = R["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-IN-Mall"]["pred"]; Gb = json.load(open(os.path.join(HERE, "FC1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-IN-Mall"]["pred"]
    RES["checks"]["MUTATE"] = m["U"]["A_c2b_refit"] > b["U"]["A_c2b_refit"] and Gm < Gb; P(f"MUTATE factor 0.5: SPARC U {b['U']['A_c2b_refit']:.3f} -> {m['U']['A_c2b_refit']:.3f}; G-IN-Mall pred {Gb:.3f} -> {Gm:.3f}: {'PASS' if RES['checks']['MUTATE'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, f"{TAG.lower()}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG.lower()}.out"), "w").write("\n".join(OUT) + "\n")
