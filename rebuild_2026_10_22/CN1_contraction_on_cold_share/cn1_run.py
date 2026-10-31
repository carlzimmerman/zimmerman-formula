#!/usr/bin/env python3
"""CN1 driver (criteria in FROZEN_CRITERIA.md): K1 against FC1, the R grid, labels. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta")
SLOPE = "2.7774425603108597"; FS = "0.034"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def grade(tag, R, mode, mut=False):
    names = [f"x74_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.json"]
    env = dict(os.environ, CN1_R=str(R), CN1_MODE=mode, X74_CF=os.path.join(CE1, f"CE1_med_fs{FS}_cf_table.json"), X73_FSTAR=FS, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    if mut: env["CN1_MUT"] = "1"
    p = subprocess.run(["nice", "-n", "15", sys.executable, "cn1_x74.py"], cwd=HERE, env=env, capture_output=True, text=True); open(os.path.join(HERE, f"{tag}.log"), "w").write(p.stdout + p.stderr); out = {}
    for n in names:
        f = os.path.join(HERE, n)
        if os.path.exists(f):
            d = os.path.join(HERE, f"{tag}_{n}"); os.replace(f, d)
            if d.endswith(".json"):
                out = json.load(open(d)); out["x74"]["cf_src"] = os.path.basename(out["x74"]["cf_src"]); json.dump(out, open(d, "w"), indent=1)
    if not out: raise SystemExit(f"NOT DECIDED: {tag} wrote no results (exit {p.returncode}); see {tag}.log")
    return out
def summ(R, foot):
    F = R["footings"][foot]; s = F["sparc"]; c = F["clusters"]
    return dict(U={k: v["U_median"] for k, v in s.items()}, rms={k: v["rms"] for k, v in s.items()}, sparc=all(v["line"] for v in s.values()), failing=F["failing"], cluster_ok=not c["fails"], cfails=c["fails"], inmall=c["cells"]["h0672"]["G-IN-Mall"]["Z"], t3=c["cells"]["h0672"]["G-MID-T3"]["Z"], gz=F["groups"]["Z"])
P("CN1 contraction on FC1's rule, f* 0.034, median eta; kappa = 1/2 FITTED; footings never pooled; not theory closed"); RES = dict(runs={}, checks={}); good = True
K = grade("CN1_K1", 1.0, "off"); G = json.load(open(os.path.join(FC1, "FC1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))
d = max(abs(K["footings"][f]["sparc"][t][q] - G["footings"][f]["sparc"][t][q]) for f in ("canonical", "alt") for t in G["footings"][f]["sparc"] for q in ("rms", "U_median"))
dc = max(abs(K["footings"][f]["clusters"]["cells"][h][k]["pred"] - G["footings"][f]["clusters"]["cells"][h][k]["pred"]) for f in ("canonical", "alt") for h in G["footings"][f]["clusters"]["cells"] for k in G["footings"][f]["clusters"]["cells"][h])
RES["checks"]["K1"] = max(d, dc) <= 1e-9; good &= RES["checks"]["K1"]; P(f"K1 contraction off reproduces FC1: SPARC {d:.1e}, clusters {dc:.1e}: {'PASS' if RES['checks']['K1'] else 'FAIL'}")
c = K["x74"]["cn1"]; RES["checks"]["K2"] = c["k2a"] < 1e-6 and c["k2b"] < 1e-3; RES["checks"]["K3"] = c["n_bcg"] == 190; good &= RES["checks"]["K2"] and RES["checks"]["K3"]; P(f"K2 identity {c['k2a']:.1e}, closed form {c['k2b']:.1e}: {'PASS' if RES['checks']['K2'] else 'FAIL'}; K3 BCG {c['n_bcg']}: {'PASS' if RES['checks']['K3'] else 'FAIL'}")
Rs = [round(1.0 - 0.05 * i, 2) for i in range(15)]; RSP = {}; RCL = {}
for R in Rs:
    o = grade(f"CN1_R{R:.2f}", R, "blum"); RES["runs"][f"{R:.2f}"] = {f: summ(o, f) for f in ("canonical", "alt")}
    for f in ("canonical", "alt"):
        s = RES["runs"][f"{R:.2f}"][f]; P(f"  R {R:.2f} [{f}] SPARC U {s['U']['A_c2b_refit']:.2f}/{s['U']['B_cfg886_bg']:.2f} rms {s['rms']['A_c2b_refit']:.4f} line {'PASS' if s['sparc'] else 'FAIL'}; G-IN-Mall {s['inmall']:+.2f}; G-MID-T3 {s['t3']:+.2f}; cluster fails {s['cfails']}")
        if s["sparc"] and f not in RSP: RSP[f] = R
        if s["cluster_ok"] and f not in RCL: RCL[f] = R
RES["R_SPARC"] = RSP; RES["R_CL"] = RCL
def rg(x): return "NONE ON GRID" if x is None else "REACHABLE AT MEASURED GAS" if x >= 0.932 else "ONLY AT CEILING" if x >= 0.573 else "OUT OF RECORDED REACH"
def rc(x): return "NONE ON GRID" if x is None else "REACHABLE" if x >= 0.95 else "MARGINAL" if x >= 0.91 else "OUT OF RECORDED REACH"
for f in ("canonical", "alt"):
    s = RES["runs"]["1.00"][f]; lab = "CONTRACTION SURVIVES" if not s["failing"] and s["sparc"] else "CONTRACTION BREAKS"
    RES.setdefault("labels", {})[f] = dict(R1=lab if good else f"NOT DECIDED ({lab})", galaxy=rg(RSP.get(f)), cluster=rc(RCL.get(f))); P(f"LABEL [{f}]: {RES['labels'][f]['R1']} (failing {s['failing']}); R_SPARC {RSP.get(f)} -> {RES['labels'][f]['galaxy']}; R_CL {RCL.get(f)} -> {RES['labels'][f]['cluster']}")
og = grade("CN1_gnedin_R1", 1.0, "gnedin"); RES["runs"]["gnedin_1.00"] = {f: summ(og, f) for f in ("canonical", "alt")}
for f in ("canonical", "alt"):
    s = RES["runs"]["gnedin_1.00"][f]; P(f"  Gnedin R 1 [{f}] SPARC U {s['U']['A_c2b_refit']:.2f}/{s['U']['B_cfg886_bg']:.2f}; G-IN-Mall {s['inmall']:+.2f}; cluster fails {s['cfails']}")
Rg = RSP.get("canonical")
if Rg is not None and Rg != 1.0:
    og2 = grade("CN1_gnedin_Rneed", Rg, "gnedin"); RES["runs"]["gnedin_Rneed"] = {f: summ(og2, f) for f in ("canonical", "alt")}; s = RES["runs"]["gnedin_Rneed"]["canonical"]; P(f"  Gnedin at R {Rg} [canonical] SPARC U {s['U']['A_c2b_refit']:.2f}/{s['U']['B_cfg886_bg']:.2f}; cluster fails {s['cfails']}")
m = grade("CN1_MUTATE", 1.0, "blum", mut=True); RES["checks"]["MUTATE_fails_K2"] = m["x74"]["cn1"]["k2b"] >= 1e-3; P(f"MUTATE (1 - F) closed-form error {m['x74']['cn1']['k2b']:.2e}: {'PASS (fails K2 as required)' if RES['checks']['MUTATE_fails_K2'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "cn1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "cn1.out"), "w").write("\n".join(OUT) + "\n")
