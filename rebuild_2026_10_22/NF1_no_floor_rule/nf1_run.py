#!/usr/bin/env python3
"""NF1_no_floor_rule (see FROZEN_CRITERIA.md): K1, N0, N1, N2, MUTATE through X74's grader. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; FS = "0.034"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92)
names = [f"x74_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.json"]
def grade(tag, on, s=0.0, mut=1.0):
    env = dict(os.environ, CN1_R="1.0", CN1_MODE="off", NF1_ON="1" if on else "0", NF1_S=str(s), NF1_MUT=str(mut), X74_CF=os.path.join(CE1, f"CE1_med_fs{FS}_cf_table.json"), X73_FSTAR=FS, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "nf1_x74.py"], cwd=HERE, env=env, capture_output=True, text=True); open(os.path.join(HERE, f"{tag}.log"), "w").write(p.stdout + p.stderr); out = {}
    for n in names:
        f = os.path.join(HERE, n)
        if os.path.exists(f):
            d = os.path.join(HERE, f"{tag}_{n}"); os.replace(f, d)
            if d.endswith(".json"):
                out = json.load(open(d)); out["x74"]["cf_src"] = os.path.basename(out["x74"]["cf_src"]); json.dump(out, open(d, "w"), indent=1)
    if not out: raise SystemExit(f"NOT DECIDED: {tag} wrote no results (exit {p.returncode}): {p.stderr[-500:]}")
    return out
def sp(o, f): return {t: dict(U=v["U_median"], rms=v["rms"], line=v["line"], act=v["n_active"]) for t, v in o["footings"][f]["sparc"].items()}
def zs(o, f): c = o["footings"][f]["clusters"]["cells"]; return {(hk, k): c[hk][k]["Z"] for hk in c for k in c[hk]}
def preds(o, f): c = o["footings"][f]["clusters"]["cells"]; return {(hk, k): c[hk][k]["pred"] for hk in c for k in c[hk]}
RES = dict(s={"N1": S1, "N2": S2}, runs={}, checks={}); P(f"NF1 no floor, f* {FS}, median eta, f_c conversions; s N1 {S1:.4f}, N2 {S2:.4f}; kappa = 1/2 FITTED; not theory closed")
F1 = json.load(open(os.path.join(RB, "FC1_cold_share_native_eta", f"FC1_med_fs{FS}_x74_results_fs{FS}_nat_s2.7774.json")))
K = grade("NF1_K1", False); dk1 = 0.0
for f in ("canonical", "alt"):
    a, b = sp(K, f), sp(F1, f)
    for t in a: dk1 = max(dk1, abs(a[t]["U"] - b[t]["U"]), abs(a[t]["rms"] - b[t]["rms"]))
    pa, pb = preds(K, f), preds(F1, f); dk1 = max(dk1, max(abs(pa[k] - pb[k]) for k in pa))
ok1 = dk1 <= 1e-9; P(f"K1 floor restored reproduces FC1: max |d| {dk1:.1e}: {'PASS' if ok1 else 'FAIL'}"); RES["checks"]["K1"] = dk1
LAB = {}
for nm, s in (("N0", 0.0), ("N1", S1), ("N2", S2)):
    o = grade(f"NF1_{nm}", True, s); RES["runs"][nm] = {}
    for f in ("canonical", "alt"):
        q = sp(o, f); RES["runs"][nm][f] = dict(sparc=q, groupsZ=o["footings"][f]["groups"]["Z"], failing=o["footings"][f]["failing"]); P(f"  {nm} [{f}] SPARC U {q['A_c2b_refit']['U']:.2f}/{q['B_cfg886_bg']['U']:.2f} rms {q['A_c2b_refit']['rms']:.4f}/{q['B_cfg886_bg']['rms']:.4f} line {all(v['line'] for v in q.values())}; groups Z {RES['runs'][nm][f]['groupsZ']:+.2f}; failing {RES['runs'][nm][f]['failing']}")
    LAB[nm] = all(v["line"] for v in sp(o, "canonical").values())
    if nm == "N0":
        qa, qb = sp(o, "canonical"), sp(o, "alt"); dk2 = max(max(abs(qa[t]["U"] - qb[t]["U"]), abs(qa[t]["rms"] - qb[t]["rms"])) for t in qa); ok2 = dk2 <= 1e-9; P(f"K2 N0 canonical = alt on SPARC: max |d| {dk2:.1e}: {'PASS' if ok2 else 'FAIL'}"); RES["checks"]["K2"] = dk2
        za, zb = zs(o, "canonical"), zs(F1, "canonical"); dz = {k: abs(za[k] - zb[k]) for k in za}; mx = max(dz.values()); dg = abs(o["footings"]["canonical"]["groups"]["Z"] - F1["footings"]["canonical"]["groups"]["Z"]); P(f"K3 N0 vs FC1, clusters max |dZ| {mx:.1e}, groups |dZ| {dg:.1e}"); RES["checks"]["K3"] = dict(clusters=mx, groups=dg); N0U = {t: qa[t]["U"] for t in qa}
M = grade("NF1_MUTATE", True, 0.0, 0.5); qm = sp(M, "canonical"); okm = all(qm[t]["U"] > N0U[t] for t in qm); P(f"MUTATE S x 0.5 raises Upsilon: {[round(N0U[t], 2) for t in qm]} -> {[round(qm[t]['U'], 2) for t in qm]}: {'PASS' if okm else 'FAIL'}"); RES["checks"]["MUTATE"] = bool(okm)
okc = ok1 and ok2 and okm; lab = "FLOOR NOT NEEDED" if LAB["N0"] else "TREND-DEPENDENT" if (LAB["N1"] or LAB["N2"]) else "FLOOR NEEDED"; lab = lab if okc else f"NOT DECIDED ({lab})"; RES["label"] = lab; P(f"LABEL (SPARC only): {lab}")
json.dump(RES, open(os.path.join(HERE, "nf1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nf1.out"), "w").write("\n".join(OUT) + "\n")
