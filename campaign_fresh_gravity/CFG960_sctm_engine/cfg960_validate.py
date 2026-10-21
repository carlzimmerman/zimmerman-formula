#!/usr/bin/env python3
"""CFG960 validation analysis (FROZEN_CRITERIA.md section 2, commit 6fc440225).  Reads the 128^3 run JSONs in
_external_data/cfg960_work/{VS0,VK,VC,VSC,VSA,VMU}/ (copied to runs_128/), cfg960_law.json and cfg960_scorek.json; grades
V-K, V-IC, V-MASS, V-MOM, V-N1, V-LAW, V-SCORE, V-MEM, reports the PREVIEW (NOT A VERDICT) and the SCT diagnostics.
  nice -n 10 python3 cfg960_validate.py            -> cfg960_validate.out / cfg960_validate.json
  nice -n 10 python3 cfg960_validate.py --mutate   -> cfg960_validate_MUTATE.out / _MUTATE.json (V-MUT; exit 1 when both teeth bite, 2 otherwise)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, glob, math, re, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg960_work"); RUNS = os.path.join(HERE, "runs_128")
MUT = "--mutate" in sys.argv
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def load(job, pat):
    f = sorted(glob.glob(os.path.join(W, job, pat)))
    return (json.load(open(f[0])), f[0]) if f else (None, None)
def peak_time_l(job):
    lg = os.path.join(W, job, "engine.log")
    if not os.path.exists(lg): return None
    m = re.findall(r"(\d+)\s+maximum resident set size", open(lg).read())
    return int(m[-1]) / 1e9 if m else None
def at(F, S, key, qs=(0.3, 0.5, 1.0), field="P_grav", sfield="P"):
    k = np.array(F["snap"][key]["k"]); r = np.array(F["snap"][key][field]) / np.array(S["snap"][key][sfield])
    return {str(q): float(np.exp(np.interp(math.log(q), np.log(k), np.log(r)))) for q in qs}

VS0, fS0 = load("VS0", "cfg654cmb_cfg650_na_S0_*.json")
J = {j: load(j, "cfg960sctm_*.json") for j in ("VK", "VC", "VSC", "VSA", "VMU")}
R = dict(lane="CFG960", stage="validation 128^3", criteria="FROZEN_CRITERIA.md 6fc440225", gates={}, preview={}, diagnostics={}, files={})
P("CFG960 validation at 128^3 (L 100 Mpc/h, NSEED 128, seed 359, native_cmb, lean, 1 thread). kappa = 1/2 FITTED; footings never pooled; not theory closed.")
for j, (d, f) in list(J.items()) + [("VS0", (VS0, fS0))]:
    R["files"][j] = os.path.basename(f) if f else None
    if d is not None: P(f"  {j}: {os.path.basename(f)}; engine sha256 {d.get('engine_sha256', 'CFG654 engine run()')[:16]}...; runtime {d.get('runtime_s', float('nan')):.0f} s")

if MUT:
    F, f1 = J["VMU"]; G, f2 = J["VSC"]
    P("\nV-MUT (planted wrong body mass: painted body mass x 0.5) vs VSC:")
    if F is None or G is None:
        P("  runs missing"); sys.exit(2)
    rat = {key: at(F, G, key, field="P_grav", sfield="P_grav") for key in ("z0", "z0.5", "z1")}
    dz0 = {q: abs(v - 1) for q, v in rat["z0"].items()}
    pe = max(abs(b["painted_err"]) for b in F["book"])
    t1 = all(v >= 0.01 for v in dz0.values()); t2 = pe >= 1e-3
    R["gates"]["V-MUT"] = dict(P_grav_MU_over_VSC=rat, abs_dev_z0=dz0, tooth_Pk=t1, painted_err_max=pe, tooth_mass=t2, BITES=bool(t1 and t2))
    P(f"  P_grav,MU/P_grav,VSC at z0 k 0.3/0.5/1: " + "/".join(f"{v:.4f}" for v in rat["z0"].values()) + f" -> |dev| >= 0.01 at all three: {'bites' if t1 else 'DOES NOT BITE'}")
    P(f"  z0.5: " + "/".join(f"{v:.4f}" for v in rat["z0.5"].values()) + "; z1: " + "/".join(f"{v:.4f}" for v in rat["z1"].values()))
    P(f"  mass monitor max |painted - book|/N = {pe:.4e} -> {'bites' if t2 else 'DOES NOT BITE'}")
    P(f"V-MUT -> {'BITES (exit 1 by design)' if t1 and t2 else 'DOES NOT BITE (exit 2)'}")
    json.dump(R, open(os.path.join(HERE, "cfg960_validate_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg960_validate_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if t1 and t2 else 2)

# ---- V-K
K, _ = J["VK"]; mx = 0.0; per = {}
for z in VS0["snap"]:
    for q in ("P", "P_grav"):
        a = np.array(VS0["snap"][z][q]); b = np.array(K["snap"][z][q]); d = float(np.max(np.abs(b / a - 1))); per[f"{z}.{q}"] = d; mx = max(mx, d)
fld = {}
for z in VS0["snap"]:
    fa = glob.glob(os.path.join(W, "VS0", f"*_{z}_mesh256.npz")); fb = glob.glob(os.path.join(W, "VK", f"*_{z}_mesh256.npz"))
    if fa and fb:
        A, B = np.load(fa[0]), np.load(fb[0]); fld[z] = bool(np.array_equal(A["dpart"], B["dpart"]) and np.array_equal(A["dgrav"], B["dgrav"]))
okK = mx <= 1e-6 and set(VS0["snap"]) == set(K["snap"])
R["gates"]["V-K"] = dict(PASS=okK, max_rel=mx, per_quantity=per, fields_bit_identical=fld, domains_final=K.get("domains_final"))
P(f"\nV-K VK (conversion off: births/labels/merges active, nothing converts, M3 off) vs VS0: max |dP/P| over {len(per)} quantities = {mx:.3e} (line 1e-6) -> {'PASS' if okK else 'FAIL'}")
P(f"    density and gravitating mesh fields bit-identical at: " + ", ".join(f"{z} {v}" for z, v in fld.items()) + f"; VK domains {K.get('domains_final')}")
# ---- V-IC
ic = {j: bool(np.array_equal(np.array(J[j][0]["snap"]["zi"]["P"]), np.array(VS0["snap"]["zi"]["P"]))) for j in ("VK", "VC", "VSC", "VSA", "VMU") if J[j][0]}
R["gates"]["V-IC"] = dict(PASS=all(ic.values()), per_run=ic); P(f"V-IC zi particle P(k) bit-identical to VS0: {ic} -> {'PASS' if all(ic.values()) else 'FAIL'}")
# ---- V-MASS / V-MOM
mass = {}; mom = {}
for j in ("VC", "VSC", "VSA"):
    F = J[j][0]; b = F["book"]
    me = max(abs(x["mass_err"]) for x in b); pe = max(abs(x["painted_err"]) for x in b); md = max(abs(x["mean_delta_g"]) for x in b)
    mass[j] = dict(mass_err=me, painted_err=pe, mean_delta_g=md, PASS=bool(me <= 1e-12 and pe <= 1e-10 and md <= 1e-5))
    Pb = np.array([x["P"] for x in b]); Pa = np.array([x["Pabs"] for x in b])
    drift = np.max(np.abs(Pb - Pb[0]) / Pa[:, None], 0); ev = max(x["ev_dP"] / max(x["Pabs"], 1e-300) for x in b)
    mom[j] = dict(drift_per_component=drift.tolist(), event_rel_max=ev, final_rel=((Pb[-1] - Pb[0]) / Pa[-1]).tolist())
evK = max(x["ev_dP"] / max(x["Pabs"], 1e-300) for x in K["book"])
okM = all(v["PASS"] for v in mass.values())
okP = max(mom["VC"]["drift_per_component"]) <= 1e-5 and all(v["event_rel_max"] <= 1e-12 for v in mom.values()) and evK <= 1e-12
R["gates"]["V-MASS"] = dict(PASS=okM, per_run=mass); R["gates"]["V-MOM"] = dict(PASS=okP, per_run=mom, VK_event_rel_max=evK,
    note="graded on VC (M3 off); VSC/VSA drift reported only (U12: M3 moves source mass without moving particles)")
for j, v in mass.items(): P(f"V-MASS {j}: max |sum w + sum M_c - N|/N {v['mass_err']:.2e} (1e-12); |painted - M_c|/N {v['painted_err']:.2e} (1e-10); |mean delta_g| {v['mean_delta_g']:.2e} (1e-5) -> {'PASS' if v['PASS'] else 'FAIL'}")
for j, v in mom.items(): P(f"V-MOM {j}: max |P_book - P_book,0|/P_scale per component " + ", ".join(f"{x:.2e}" for x in v["drift_per_component"]) + f"; event algebra max {v['event_rel_max']:.2e}" + ("  [graded: line 1e-5 / 1e-12]" if j == "VC" else "  [reported only, M3 on]"))
P(f"V-MOM VK event algebra max {evK:.2e}; -> {'PASS' if okP else 'FAIL'}")
# ---- V-N1
n1 = {}
for j in ("VSC", "VSA"):
    F = J[j][0]; rr = {}
    for key in ("z1", "z0.5", "z0"):
        r = np.array(F["snap"][key]["P_grav"]) / np.array(VS0["snap"][key]["P"]); rr[key] = [float(r[0]), float(r[1])]
    k01 = [float(F["snap"]["z0"]["k"][0]), float(F["snap"]["z0"]["k"][1])]
    gro = {key: float(F["snap"][key]["P_grav"][0] / F["snap"]["zi"]["P_grav"][0] / (F["snap"][key]["D"] / F["snap"]["zi"]["D"]) ** 2) for key in ("z1", "z0.5", "z0")}
    ok1 = all(abs(x - 1) <= 0.03 for v in rr.values() for x in v); ok2 = all(abs(v - 1) <= 0.05 for v in gro.values()) if j == "VSC" else True
    n1[j] = dict(k_lowest=k01, Pgrav_over_S0_lowest2=rr, fundamental_growth_over_D2=gro, PASS=bool(ok1 and ok2))
    P(f"V-N1 {j}: P_grav/P_S0 at k {k01[0]:.4f}/{k01[1]:.4f}: " + "; ".join(f"{z} {v[0]:.4f}/{v[1]:.4f}" for z, v in rr.items()) + " (3%)"
      + (f"; fundamental P_grav growth / native D^2: " + ", ".join(f"{z} {v:.4f}" for z, v in gro.items()) + " (5%)" if j == "VSC" else "") + f" -> {'PASS' if n1[j]['PASS'] else 'FAIL'}")
R["gates"]["V-N1"] = dict(PASS=all(v["PASS"] for v in n1.values()), per_run=n1)
# ---- V-LAW, V-SCORE
for g_, fn, key in (("V-LAW", "cfg960_law.json", "V_LAW_PASS"), ("V-SCORE", "cfg960_scorek.json", "V_SCORE_PASS")):
    p = os.path.join(HERE, fn)
    if os.path.exists(p):
        d = json.load(open(p)); R["gates"][g_] = dict(PASS=bool(d[key]), file=fn, maxrss_gb=d.get("maxrss_gb"), worst=d.get("worst"))
        P(f"{g_}: from {fn} -> {'PASS' if d[key] else 'FAIL'}")
    else:
        R["gates"][g_] = dict(PASS=False, missing=True); P(f"{g_}: {fn} missing -> NOT EVALUATED")
# ---- V-MEM
mem = {j: peak_time_l(j) for j in ("VS0", "VK", "VC", "VSC", "VSA", "VMU")}
for g_, fn in (("LAW", "cfg960_law_time.txt"), ("SCOREK", "cfg960_scorek_time.txt")):
    p = os.path.join(W, fn)
    if os.path.exists(p):
        m = re.findall(r"(\d+)\s+maximum resident set size", open(p).read()); mem[g_] = int(m[-1]) / 1e9 if m else None
okmem = all(v is not None and v < 1.0 for v in mem.values())
R["gates"]["V-MEM"] = dict(PASS=okmem, peak_rss_gb=mem); P("V-MEM peak RSS (GB, /usr/bin/time -l): " + ", ".join(f"{k} {v:.3f}" if v else f"{k} n/a" for k, v in mem.items()) + f" -> {'PASS' if okmem else 'FAIL'}")
allg = all(v.get("PASS") for k, v in R["gates"].items())
R["all_gates_pass"] = bool(allg); P(f"\nALL validation gates (V-K, V-IC, V-MASS, V-MOM, V-N1, V-LAW, V-SCORE, V-MEM): {'PASS' if allg else 'NOT ALL PASS'}  (V-MUT: cfg960_validate_MUTATE.out)")
# ---- PREVIEW
P("\nPREVIEW 128^3, NOT A VERDICT (domain floor ~1e12 h^-1 Msun at 128^3; k = 1 at the support limit): P_grav / P_VS0 at k 0.3 / 0.5 / 1")
for j, lab in (("VSC", "SCT-M canonical (= SC1x at 128^3)"), ("VSA", "SCT-M alt (= SC2x at 128^3)"), ("VC", "SCT-M canonical, M3 off")):
    F = J[j][0]; pv = {key: at(F, VS0, key) for key in ("z0", "z0.5", "z1")}; R["preview"][j] = pv
    P(f"  {lab}: " + "; ".join(f"{z}: " + "/".join(f"{v:.3f}" for v in pv[z].values()) for z in ("z0", "z0.5", "z1")))
# ---- diagnostics
for j in ("VC", "VSC", "VSA"):
    F = J[j][0]; dg = {}
    for key in ("z1", "z0.5", "z0"):
        s = F["snap"][key]; b = s["book"]; bd = (s.get("sct") or {}).get("bodies", {})
        dg[key] = dict(n_dom=b["n_dom"], n_bodies=b["n_bodies"], conv_frac=b["conv_frac"], pend_frac=b["pend_frac"], lab_frac=b["lab_frac"],
                       re_dx_median=bd.get("re_dx_median"), re_dx_max=bd.get("re_dx_max"), n_point=bd.get("n_point"), n_fallback=bd.get("n_fallback"),
                       n_cap=bd.get("n_cap"), n_points=bd.get("n_points"))
    ev = F["events"]; tot = dict(births=sum((e["refresh"] or {}).get("n_births", 0) for e in ev), labelled_majority_peaks=sum((e["refresh"] or {}).get("n_insitu_peaks", 0) for e in ev),
        accreted_particles=sum((e["refresh"] or {}).get("n_accreted", 0) for e in ev), merges_bound=sum((e["merges"] or {}).get("n_merge_bound", 0) for e in ev),
        merges_coalescence=sum((e["merges"] or {}).get("n_merge_coal", 0) for e in ev))
    R["diagnostics"][j] = dict(per_snapshot=dg, totals=tot, domains_final=F.get("domains_final"), timing_s=F.get("timing_s"), runtime_s=F.get("runtime_s"))
    P(f"  {j}: " + "; ".join(f"{z}: dom {v['n_dom']} bodies {v['n_bodies']} conv {v['conv_frac']:.3f} pend {v['pend_frac']:.3f} r_e/dx med {v['re_dx_median'] if v['re_dx_median'] is None else round(v['re_dx_median'], 2)} max {v['re_dx_max'] if v['re_dx_max'] is None else round(v['re_dx_max'], 2)}" for z, v in dg.items()))
    P(f"      totals {tot}; final {F.get('domains_final')}; timing (s) " + ", ".join(f"{k} {v:.0f}" for k, v in F.get("timing_s", {}).items()))
os.makedirs(RUNS, exist_ok=True)
for j in ("VS0", "VK", "VC", "VSC", "VSA", "VMU"):
    for f in glob.glob(os.path.join(W, j, "*.json")):
        if os.path.basename(f) != "job.json":                       # copied with absolute local paths made relative (no home paths in the repo)
            txt = open(f).read().replace(EXT, "<EXT>").replace(os.path.abspath(os.path.join(HERE, "..", "..")), "<REPO>").replace(os.path.expanduser("~"), "~")
            open(os.path.join(RUNS, f"{j}__" + os.path.basename(f)), "w").write(txt)
json.dump(R, open(os.path.join(HERE, "cfg960_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg960_validate.out"), "w").write("\n".join(OUT) + "\n")
