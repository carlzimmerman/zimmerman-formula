#!/usr/bin/env python3
"""CFG530 analysis (FROZEN_CRITERIA.md): reproduction control, stability, r(k) = P/P_S0 per run, fixed-box resolution convergence
(N256 vs N512, per box, per footing), box-size check at matched cell size and RMIN against the NSEED realization floor, the L200 512^3
growth gate (CFG361 cuts), cap / percolation table, MUTATE law consistency.  Reads the run JSONs, cfg530_profiles.json,
cfg530_s0reuse.json, cfg530_identity.json.  Writes cfg530_analysis.out and cfg530_results.json."""
import os, sys, json, math, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
sys.path.insert(0, HERE)
from run_530 import jobspec, result
W527 = os.path.join(EXT, "cfg527_work")
S0_411 = os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")
TOL_R, TOL_LR = 0.05, 0.05
KS = (1.0, 2.0, 4.0)
L_, OUT = [], {"lane": "CFG530", "date": "2026-10-09",
               "settings": "kappa = 1/2 FITTED; footings never pooled; a0 flat; nu_mono; CFG527 engine unchanged; cold energy MASS required; not theory closed"}
def P(s=""): print(s); L_.append(s)
ld = lambda p: json.load(open(p)) if p and os.path.exists(p) else None
f3 = lambda x: "  -  " if x is None else f"{x:.3f}"
kq = lambda L, N: math.pi * N / (4 * L)                                  # k_Nyq / 4

def run_json(run):
    if run == "S0_L200_N512":
        s = ld(os.path.join(HERE, "cfg530_s0reuse.json"))
        return ld(S0_411) if s and s.get("reuse") else ld(result(run))
    return ld(result(run))
def at_k(k, pr, x): return float(pr[np.argmin(np.abs(k - x))])
def ratio(d, d0, n="z0"):
    k = np.array(d["snap"][n]["k"]); return k, np.array(d["snap"][n]["P"]) / np.interp(k, np.array(d0["snap"][n]["k"]), np.array(d0["snap"][n]["P"]))

prof = ld(os.path.join(HERE, "cfg530_profiles.json")) or {"runs": {}, "phys_pairs": {}}
PR = prof["runs"]
def coreR(run):
    a = PR.get(run)
    if not a or "core_R" not in a or a["n_scored"] < 20: return None
    return a["core_R"][0]

# ---------------------------------------------------------------- controls
P("CFG530: fixed-box resolution study of the CFG527 law-respecting engine (imported unchanged).")
P("kappa = 1/2 FITTED; footings never pooled; a0 flat; cold energy MASS still required; not theory closed.\n")
eng = os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_pm.py")
OUT["engine_sha256"] = hashlib.sha256(open(eng, "rb").read()).hexdigest()
P(f"engine cfg527_pm.py sha256 {OUT['engine_sha256']}")
idn = ld(os.path.join(HERE, "cfg530_identity.json")); OUT["statistic_identity"] = idn
P(f"statistic identity (CFG527 core R reproduced to 1e-12): {'PASS' if idn and idn['pass'] else 'FAIL/PENDING'}")
s0r = ld(os.path.join(HERE, "cfg530_s0reuse.json")); OUT["s0_512_reuse"] = s0r
P(f"S0 L200 N512 = CFG411 S0 N512 reused: {s0r and s0r['reuse']} (zi exact {s0r and s0r['b']}, z0 re-measure {s0r and s0r['c']})")

P("\nREP: reproduction of CFG527 256^3 (|d s8|/s8 and max|dP/P| <= 1e-8 at every snapshot)")
REP = {}
for run, ref in (("REPcan_L100", "canonical_N256_L100"), ("REPalt_L100", "alt_N256_L100"), ("REPcan_L200", "canonical_N256"), ("REPalt_L200", "alt_N256")):
    a = run_json(run); b = ld(os.path.join(W527, f"cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_{ref}_drawSHELL.json"))
    if not (a and b): REP[run] = None; P(f"  {run}: PENDING"); continue
    ds = max(abs(a["snap"][n]["sigma8"] / b["snap"][n]["sigma8"] - 1) for n in b["snap"])
    dp = max(float(np.max(np.abs(np.array(a["snap"][n]["P"]) / np.array(b["snap"][n]["P"]) - 1))) for n in b["snap"])
    REP[run] = dict(d_sigma8_rel=ds, max_dP_rel=dp, pass_=bool(ds <= 1e-8 and dp <= 1e-8))
    P(f"  {run}: |d s8|/s8 {ds:.2e}, max|dP/P| {dp:.2e} -> {'PASS' if REP[run]['pass_'] else 'FAIL'}")
rep_ok = all(v and v["pass_"] for v in REP.values())
OUT["REP"] = REP; OUT["REP_pass"] = rep_ok

# ---------------------------------------------------------------- per-run table
RUNS = [f"{r}_L{L}_N{N}" for L in (100, 200) for N in (128, 256, 512) for r in ("LRcan", "LRalt")] + \
       [f"{r}_L100_N{N}" for N in (128, 256) for r in ("BXcan", "BXalt")] + ["MUTA_L100_N256"]
T = {}
P("\nPer run, z = 0, vs matched S0 (same L, N, NSEED 512).  r(k) at resolved bins (k <= k_Nyq/4); cap/percolation; core R (CFG526).")
P(f"{'run':16s} {'kq':>5s} {'s8 r':>6s} {'k=0.3':>6s} {'k=1':>6s} {'k=2':>6s} {'k=4':>6s} {'max|P-1|k<=1':>12s} {'coreR':>6s} {'nsc':>4s} "
  f"{'q_max':>6s} {'capM':>5s} {'capE':>5s} {'shell':>5s} {'big':>5s} span stable")
for run in RUNS:
    s = jobspec(run); L, N = int(s["L"]), s["N"]
    d = run_json(run); d0 = run_json(f"S0_L{L}_N{N}")
    if not (d and d0): T[run] = None; P(f"{run:16s} PENDING"); continue
    k, pr = ratio(d, d0); kmax = kq(L, N); z0 = d["snap"]["z0"]; snaps = list(d["snap"].values())
    rk = {str(x): (at_k(k, pr, x) if x <= kmax * 1.0001 else None) for x in (0.3, 1.0, 2.0, 3.0, 4.0, 8.0)}
    m1 = k <= 1.0
    fin = all(all(math.isfinite(v[x]) for x in ("sigma8", "e_sum", "src_sum") if v.get(x) is not None) and bool(np.all(np.isfinite(v["P"])))
              and v.get("finite", True) for v in snaps)
    kny2 = math.pi * N / (2 * L); pny2 = at_k(k, pr, kny2)
    pc = (PR.get(run) or {}).get("perc", {})
    T[run] = dict(L=L, N=N, foot=s["foot"], kq=kmax, s8=z0["sigma8"] / d0["snap"]["z0"]["sigma8"], r=rk,
                  pdev_k1=float(np.max(np.abs(pr[m1] - 1))), k_at_pdev_k1=float(k[m1][np.argmax(np.abs(pr[m1] - 1))]),
                  P_at_kNy2=pny2, stable=bool(fin and pny2 <= 2.0),
                  q_max_z0=z0.get("q_max"), q_max_all=max((v.get("q_max") or 0.0) for v in snaps),
                  cap_n_z0=z0.get("cap_n"), cap_mass_frac_z0=z0.get("cap_mass_frac"), cap_e_removed_z0=z0.get("cap_e_removed_frac"),
                  cap_mass_frac_max=max((v.get("cap_mass_frac") or 0.0) for v in snaps), cap_e_removed_max=max((v.get("cap_e_removed_frac") or 0.0) for v in snaps),
                  shell_frac_z0=z0.get("shell_frac"), n_shell_empty_max=max((v.get("n_shell_empty") or 0) for v in snaps), n_catch_z0=z0.get("n_catch"),
                  comp_in_edge_z0=z0.get("comp_in_edge"), perc=pc or None,
                  core_R=coreR(run), n_scored=(PR.get(run) or {}).get("n_scored"),
                  law_consistent_core=(None if coreR(run) is None else abs(math.log10(coreR(run))) <= 0.1),
                  all_scored_within_0p1=(None if run not in PR or "per" not in PR[run] else
                                         all(abs(math.log10(p["R"][0])) <= 0.1 for p in PR[run]["per"] if p["n"] >= 1) and abs(math.log10(PR[run]["core_R"][0])) <= 0.1),
                  runtime_s=d.get("runtime_s"))
    t = T[run]
    P(f"{run:16s} {kmax:5.2f} {t['s8']:6.4f} {f3(rk['0.3']):>6s} {f3(rk['1.0']):>6s} {f3(rk['2.0']):>6s} {f3(rk['4.0']):>6s} {t['pdev_k1']:12.3f} "
      f"{f3(t['core_R']):>6s} {str(t['n_scored']):>4s} {f3(t['q_max_z0']):>6s} {f3(t['cap_mass_frac_z0']):>5s} {f3(t['cap_e_removed_z0']):>5s} "
      f"{f3(t['shell_frac_z0']):>5s} {f3(pc.get('largest_mass_share')):>5s} {str(pc.get('spanning'))[:1]:>4s} {t['stable']}")
OUT["runs"] = T

# ---------------------------------------------------------------- 1. resolution convergence
P("\n1. Fixed-box resolution convergence (N256 vs N512; |dr| <= 0.05 at resolved k in {1, 2, 4}; |d log10 core R| <= 0.05 dex)")
CONV = {}
for foot, tag in (("canonical", "LRcan"), ("alt", "LRalt")):
    CONV[foot] = {}
    for L in (100, 200):
        a, b, c = (T.get(f"{tag}_L{L}_N{N}") for N in (128, 256, 512))
        box = {"items": [], "trend": {}}
        for x in KS:
            box["trend"][str(x)] = [None if t is None else t["r"][str(x)] for t in (a, b, c)]
        box["trend"]["coreR"] = [None if t is None else t["core_R"] for t in (a, b, c)]
        if b is None or c is None:
            box["verdict"] = "PENDING"; CONV[foot][L] = box; continue
        bad = []
        for x in KS:
            if x <= kq(L, 256) * 1.0001:
                dv = c["r"][str(x)] - b["r"][str(x)]; box["items"].append({"k": x, "r256": b["r"][str(x)], "r512": c["r"][str(x)], "d": dv, "pass": abs(dv) <= TOL_R})
                if abs(dv) > TOL_R: bad.append(f"k = {x:g}: r {b['r'][str(x)]:.3f} -> {c['r'][str(x)]:.3f} (d {dv:+.3f})")
        if b["core_R"] is None or c["core_R"] is None:
            box["R_item"] = "NOT EVALUABLE"; box["verdict"] = "NOT EVALUABLE (core R)" if not bad else "NOT CONVERGED"
        else:
            dl = math.log10(c["core_R"]) - math.log10(b["core_R"]); box["R_item"] = {"R256": b["core_R"], "R512": c["core_R"], "dlog": dl, "pass": abs(dl) <= TOL_LR}
            if abs(dl) > TOL_LR: bad.append(f"core R {b['core_R']:.3f} -> {c['core_R']:.3f} (d log {dl:+.3f})")
            box["verdict"] = "CONVERGED" if not bad else "NOT CONVERGED"
        box["failing"] = bad; CONV[foot][L] = box
    vs = [CONV[foot][L]["verdict"] for L in (100, 200)]
    CONV[foot]["verdict"] = ("NOT CONVERGED" if "NOT CONVERGED" in vs else "CONVERGED" if all(v == "CONVERGED" for v in vs)
                             else "PENDING" if "PENDING" in vs else "NOT EVALUABLE")
    P(f"  [{foot}] {CONV[foot]['verdict']}")
    for L in (100, 200):
        bx = CONV[foot][L]
        P(f"    L{L}: {bx['verdict']}" + (f" -- {'; '.join(bx.get('failing', []))}" if bx.get("failing") else ""))
        for x in KS:
            P(f"      r(k={x:g}) N128/256/512: " + " / ".join(f3(v) for v in bx["trend"][str(x)]))
        P(f"      core R  N128/256/512: " + " / ".join(f3(v) for v in bx["trend"]["coreR"]))
OUT["convergence"] = {f: {str(k): v for k, v in d.items()} for f, d in CONV.items()}

# ---------------------------------------------------------------- 2. box-size effect
P("\n2. Box-size check at matched cell size and RMIN 1.56 (P1: BX L100/N128 vs L200/N256; P2: BX L100/N256 vs L200/N512)")
BOX = {}
for foot, bx, lr in (("canonical", "BXcan", "LRcan"), ("alt", "BXalt", "LRalt")):
    # realization floor: REP (NSEED 256 = CFG527) vs study (NSEED 512) at N256, same box
    F = {}
    for L in (100, 200):
        rep = run_json(f"{'REPcan' if foot == 'canonical' else 'REPalt'}_L{L}"); st = T.get(f"{lr}_L{L}_N256")
        s0rep = ld(os.path.join(EXT, "cfg521_work", "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L100.json")) if L == 100 \
            else ld(os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"))
        if rep is None or st is None or s0rep is None: continue
        k, pr = ratio(rep, s0rep)
        for x in KS:
            if x <= kq(L, 256) * 1.0001:
                F.setdefault(str(x), []).append(abs(at_k(k, pr, x) - st["r"][str(x)]))
        r527 = ld(os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_profiles.json"))["runs"][f"{lr}_L{L}"]["core"]["R"][0]
        if st["core_R"] is not None:
            F.setdefault("coreR", []).append(abs(math.log10(r527) - math.log10(st["core_R"])))
    F = {k: max(v) for k, v in F.items()}
    res = {"floor": F, "pairs": {}}
    exceed_tol, exceed_both, evaluated = [], [], {}
    for pname, A_, B_ in (("P1", f"{bx}_L100_N128", f"{lr}_L200_N256"), ("P2", f"{bx}_L100_N256", f"{lr}_L200_N512"),
                          ("P2b(RMIN differs)", f"{lr}_L100_N256", f"{lr}_L200_N512")):
        a, b = T.get(A_), T.get(B_)
        if a is None or b is None: res["pairs"][pname] = "PENDING"; continue
        items = []
        for x in KS:
            if x <= min(a["kq"], b["kq"]) * 1.0001:
                dv = a["r"][str(x)] - b["r"][str(x)]; fl = F.get(str(x))
                items.append({"item": f"r(k={x:g})", "L100": a["r"][str(x)], "L200": b["r"][str(x)], "d": dv, "floor": fl})
        if a["core_R"] is not None and b["core_R"] is not None:
            dl = math.log10(a["core_R"]) - math.log10(b["core_R"])
            items.append({"item": "log10 core R", "L100": a["core_R"], "L200": b["core_R"], "d": dl, "floor": F.get("coreR")})
        res["pairs"][pname] = items
        if pname.startswith("P2b"): continue
        evaluated[pname] = True
        for it in items:
            tol = TOL_LR if it["item"].startswith("log") else TOL_R
            if abs(it["d"]) > tol:
                exceed_tol.append(f"{pname} {it['item']} d {it['d']:+.3f}")
                if it["floor"] is not None and abs(it["d"]) > 2 * it["floor"]:
                    exceed_both.append(f"{pname} {it['item']} d {it['d']:+.3f} (2F {2 * it['floor']:.3f})")
    if exceed_both: v = "YES"
    elif "P1" not in evaluated: v = "PENDING"
    elif exceed_tol: v = "NOT SEPARABLE"
    elif "P2" not in evaluated: v = "PENDING (P1 says NO)"
    else: v = "NO"
    res.update(verdict=v, exceed_tol=exceed_tol, exceed_tol_and_2F=exceed_both); BOX[foot] = res
    P(f"  [{foot}] BOX-SIZE EFFECT: {v}" + (f" -- {'; '.join(exceed_both or exceed_tol)}" if (exceed_both or exceed_tol) else ""))
    P(f"      realization floor F (NSEED 256 vs 512, same box, N256): " + ", ".join(f"{k} {v:.3f}" for k, v in F.items()))
    for pn, items in res["pairs"].items():
        if items == "PENDING": P(f"      {pn}: PENDING"); continue
        P(f"      {pn}: " + "; ".join(f"{it['item']} L100 {it['L100']:.3f} vs L200 {it['L200']:.3f} (d {it['d']:+.3f})" for it in items))
OUT["box_size"] = BOX

# ---------------------------------------------------------------- 3. growth gate L200 512^3
P("\n3. Growth gate L200 512^3 (CFG361 cuts at z = 0, k <= 1, vs S0 N512 = CFG411 reused)")
G = {}
for foot, run in (("canonical", "LRcan_L200_N512"), ("alt", "LRalt_L200_N512")):
    t = T.get(run)
    if t is None: G[foot] = {"verdict": "PENDING"}; P(f"  [{foot}] PENDING"); continue
    v = "FAIL" if abs(t["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(t["s8"] - 1) <= 0.05 and t["pdev_k1"] <= 0.10 else "TENSION")
    G[foot] = {"verdict": v, "sigma8_ratio": t["s8"], "max_dev_k_le_1": t["pdev_k1"], "k_at_max": t["k_at_pdev_k1"],
               "vs_256": "CONFIRMED" if v == "GROWTH OK" else "NOT CONFIRMED"}
    P(f"  [{foot}] {v}: sigma8 ratio {t['s8']:.4f}, max|P/P_S0 - 1| (k <= 1) {t['pdev_k1']:.3f} at k = {t['k_at_pdev_k1']:.3f} "
      f"-> CFG527 256^3 GROWTH OK {G[foot]['vs_256']} at 512^3")
OUT["growth_L200_512"] = G

# ---------------------------------------------------------------- 4. MUTATE + stability
P("\n4. Controls")
mu = T.get("MUTA_L100_N256")
mu_fail = None if mu is None or mu["all_scored_within_0p1"] is None else (not mu["all_scored_within_0p1"])
OUT["MUTATE_fails_law"] = mu_fail
P(f"  MUTATE (CFG521 old draw SC + MIX-A, L100 N256): core R {f3(mu and mu['core_R'])} -> "
  + ("must fail law consistency: OK (fails)" if mu_fail else ("PENDING" if mu_fail is None else "law-consistent -> R items NOT DIAGNOSTIC")))
st = {r: t["stable"] for r, t in T.items() if t is not None and not r.startswith("MUTA")}
OUT["stability"] = st
P(f"  stability (NOFILT runs): {'all STABLE' if all(st.values()) else 'UNSTABLE: ' + ', '.join(r for r, v in st.items() if not v)} ({len(st)} runs)")
P(f"  REP reproduction: {'PASS' if rep_ok else 'FAIL/PENDING'}")
OUT["physical_radius_pairs"] = prof.get("phys_pairs")
json.dump(OUT, open(os.path.join(HERE, "cfg530_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg530_analysis.out"), "w").write("\n".join(L_) + "\n")
