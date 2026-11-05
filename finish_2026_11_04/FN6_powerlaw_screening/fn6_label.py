#!/usr/bin/env python3
"""FN6_powerlaw_screening labels (criteria 5f0f4a5d99): merges fn6_small_part*.jsonl and fn6_mw_{footing}.jsonl, checks KA1
(p 0, L_MW 2 against FN1b's stored 2 kpc row, exactly) and KA2, and applies the frozen labels per footing; MUTATE beside.
Run: python3 -I -B fn6_label.py. kappa = 1/2 FITTED and held fixed; not theory closed."""
import glob, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
FN1B = os.path.join(REPO, "finish_2026_11_04", "FN1_action_call", "FN1b_fixed_length_static")
PS = [-0.5, -0.25, 0.0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75]; LMWS = [1.0, 1.5, 2.0, 3.0]; FEET = ("canonical", "alt"); GATES = ("T0", "T1", "T2", "T3", "T4")
OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
def jl(pat):
    d = {}
    for fn in sorted(glob.glob(os.path.join(HERE, pat))):
        for ln in open(fn): o = json.loads(ln); d[(o["p"], o["L_MW"])] = o
    return d
def gates(sm, mw, foot):
    """Per gate: 'P', 'F', 'NE' (validation miss, gate not failed) or 'not run'."""
    g = {}
    for t in ("T1", "T2", "T3", "T4"):
        x = sm[t][foot]; g[t] = "F" if not x["ok"] else ("P" if x["evaluable"] else "NE")
    if mw is None: g["T0"] = "not run"
    else: g["T0"] = "F" if not mw["ok"] else ("P" if mw["evaluable"] else "NE")
    return g
def row_label(g):
    f = [t for t in GATES if g[t] == "F"]
    if f: return "FAILS: " + ", ".join(f)
    ne = [t for t in GATES if g[t] in ("NE", "not run")]
    return "NOT EVALUABLE: " + ", ".join(ne) if ne else "ALL FIVE PASS"
P("FN6_powerlaw_screening labels (criteria 5f0f4a5d99); form R; kappa = 1/2 FITTED; not theory closed")
SM = jl("fn6_small_part*of*.jsonl"); MW = {f: jl(f"fn6_mw_{f}.jsonl") for f in FEET}
check("K-grid", len(SM) == 48 and all((p, L) in SM for p in PS for L in LMWS), f"small gates at {len(SM)} of 48 grid points")
# ---- KA1: p = 0, L_MW = 2.0 reproduces FN1b's 2 kpc row, form R, on each gate exactly
s1 = json.load(open(os.path.join(FN1B, "fn1b_small.json"))); ka1 = {}
for foot in FEET:
    o = SM[(0.0, 2.0)]; m = MW[foot].get((0.0, 2.0)); r1 = s1["T1"][foot]["2.0"]["R"]; r4 = s1["T4"][foot]["2.0"]["R"]; r2 = s1["T2"][foot]["2.0"]["R"]; r3 = s1["T3"][foot]["2.0"]["R"]
    mw1 = json.load(open(os.path.join(FN1B, f"fn1b_mw_{foot}.json"))); r0 = mw1["R"]["2.0"]; c0 = mw1["convergence"]["2.0"]["grid_dependent"]
    eq = dict(T1_Q2=o["T1"][foot]["Q2"] == r1["Q2"], T4_Z=o["T4"][foot]["Z"] == r4["Z"] and o["T4"][foot]["worst"] == r4["worst"],
              T2_E1=o["T2"][foot]["E1"] == r2["E1"], T2_fornax=o["T2"][foot]["fornax_U2"] == r2["fornax_U2"],
              T3=all(o["T3"][foot][k] == r3[k] for k in ("rms", "med", "d_rms", "label")))
    if m is not None:
        sm = m["summary"]; eq.update(T0_counts=sm["n_pass"] == r0["n_pass"] and sm["strict"] == r0["strict"] and sm["lines"] == r0["lines"],
                                     T0_floats=all(sm[k] == r0[k] for k in ("K_min_L1", "vc_max")) and sm["best"]["D"] == r0["best"]["D"], T0_flag=m["convergence"]["grid_dependent"] == c0)
    else: eq["T0_counts"] = False
    ka1[foot] = eq
    P(f"  KA1 [{foot}]: T1 Q2 {o['T1'][foot]['Q2']:.6e} (FN1b {r1['Q2']:.6e}); T4 Z {o['T4'][foot]['Z']:.6e} ({r4['Z']:.6e}); T2 E1 {o['T2'][foot]['E1']} ({r2['E1']}), Fornax {o['T2'][foot]['fornax_U2']:.6f} ({r2['fornax_U2']:.6f}); "
      f"T3 d {o['T3'][foot]['d_rms']:+.6f} {o['T3'][foot]['label']} ({r3['d_rms']:+.6f} {r3['label']}); T0 {m['summary']['n_pass'] if m else None} ({r0['n_pass']}), flag {m['convergence']['grid_dependent'] if m else None} ({c0}); equal: {eq}")
    check(f"KA1 [{foot}]", all(eq.values()), f"p 0, L_MW 2 reproduces FN1b's 2 kpc R row exactly on T0-T4 ({sum(eq.values())}/{len(eq)} items equal)")
RES["KA1"] = ka1
p0 = json.load(open(os.path.join(HERE, "fn6_small_part0of3.json"))); ka2ok = p0["checks"]["KA2"]["ok"]; RES["KA2"] = p0.get("KA2")
check("KA2", ka2ok, p0["checks"]["KA2"]["msg"])
for nm in ("V2", "V3R", "K-HALF-dwarfs"): check(nm, p0["checks"][nm]["ok"], p0["checks"][nm]["msg"])
sm_fail = sorted({c for fn in glob.glob(os.path.join(HERE, "fn6_small_part*of*.json")) for c in json.load(open(fn))["failed_checks"]})
mw_fail = sorted({c for f in FEET for c in (json.load(open(os.path.join(HERE, f"fn6_mw_{f}.json")))["failed_checks"] if os.path.exists(os.path.join(HERE, f"fn6_mw_{f}.json")) else ["missing"])})
check("K-runs", not sm_fail and not mw_fail, f"failed checks inside the runs: small {sm_fail or 0}, Milky Way {mw_fail or 0}")
# ---- per point and per footing
TAB = {}; LAB = {}
for foot in FEET:
    TAB[foot] = {}; passing = []; ne_pts = []
    for p in PS:
        for L in LMWS:
            g = gates(SM[(p, L)], MW[foot].get((p, L)), foot); lb = row_label(g); TAB[foot][f"{p}|{L}"] = dict(gates=g, label=lb)
            if lb == "ALL FIVE PASS": passing.append((p, L))
            elif lb.startswith("NOT EVALUABLE"): ne_pts.append((p, L))
    ka_ok = all(ka1[foot].values()) and ka2ok
    lab = "NOT EVALUABLE" if not ka_ok else ("WINDOW" if passing else "NO POWER-LAW LENGTH PASSES")
    LAB[foot] = dict(label=lab, passing=passing, n_passing=len(passing), n_grid=48, not_evaluable_points=ne_pts, would_be=("WINDOW" if passing else "NO POWER-LAW LENGTH PASSES"))
    P(f"\n== [{foot}] label: {lab}" + (f" (the grid alone would read {LAB[foot]['would_be']})" if lab == "NOT EVALUABLE" else "") + f"; passing points {len(passing)} of 48: {passing}; NOT EVALUABLE points {ne_pts}")
    P("  p \\ L_MW  " + " | ".join(f"{L:>22.1f}" for L in LMWS))
    for p in PS:
        cells = []
        for L in LMWS:
            g = TAB[foot][f"{p}|{L}"]["gates"]; f_ = [t for t in GATES if g[t] == "F"]; n_ = [t for t in GATES if g[t] in ("NE", "not run")]
            cells.append(("PASS" if not f_ and not n_ else "F " + ",".join(f_) if f_ else "NE " + ",".join(n_)) + ("" if g["T0"] != "not run" or f_ == [] else " (T0 not run)"))
        P(f"  {p:+.2f}     " + " | ".join(f"{c:>22s}" for c in cells))
RES["table"] = TAB; RES["labels"] = LAB
# ---- MUTATE (mass shuffle), beside
MU = {}
for fn in sorted(glob.glob(os.path.join(HERE, "fn6_small_mutate_s*.jsonl"))):
    seed = fn.split("_s")[-1].split(".")[0]; sm_ = jl(os.path.basename(fn)); info = json.load(open(fn.replace(".jsonl", ".json"))).get("mutate", {})
    for foot in FEET:
        mw_ = jl(f"fn6_mw_{foot}_mutate_s{seed}.jsonl")
        for pt, o in sm_.items():
            g = gates(o, mw_.get(pt), foot); MU.setdefault(f"{pt[0]}|{pt[1]}", {}).setdefault(foot, {})[seed] = dict(gates=g, label=row_label(g), Sun_gets=info.get("Sun_gets"), MW_gets=info.get("MW_gets"),
                                                                                                       dw=o["T2"][foot]["E1"], sparc_d=o["T3"][foot]["d_rms"], Q2x=o["T1"][foot]["x_ceiling"], Z=o["T4"][foot]["Z"],
                                                                                                       T0_n=(mw_[pt]["summary"]["n_pass"] if pt in mw_ else None))
if MU:
    P("\n== MUTATE (masses shuffled among the 181 systems before L is assigned), beside")
    for k, v in MU.items():
        for foot in FEET:
            rs = sorted(v.get(foot, {}).items()); surv = [s for s, r in rs if r["label"] == "ALL FIVE PASS"]
            P(f"  ({k.replace('|', ', ')}) [{foot}]: survives {len(surv)} of {len(rs)} shuffles; " + "; ".join(f"s{s} {r['label'].replace('FAILS: ', 'F ')} (dw {r['dw']}, SP d {r['sparc_d']:+.3f})" for s, r in rs))
RES["mutate"] = MU
RES["failed_checks"] = FAILS
P(f"\nfailed checks: {FAILS if FAILS else 0}")
open(os.path.join(HERE, "fn6_label.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "fn6_label.json"), "w"), indent=1, default=float)
