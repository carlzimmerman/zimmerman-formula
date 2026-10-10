#!/usr/bin/env python3
"""CFG539 Stage 2 analysis (FROZEN_CRITERIA.md): T4 growth (CFG361 cuts at every (L, N)), small-scale r(k), T1 law statistic (+ direction, fill),
T3 origin census, convergence 128 -> 256, mobility robustness, MUTATE-S, controls, verdict per class and footing.
  python3 cfg539_analysis.py compute     heavy stage: profile caches (cfg539_profiles.compute) + T3 census caches, for every finished run
  python3 cfg539_analysis.py             -> cfg539_analysis.out, cfg539_results.json"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg539_profiles as PR
EXT = PR.EXT; W539 = PR.W539; W530 = PR.W530
LINES = []
def P(s=""):
    print(s); LINES.append(s)
T = 10 ** -0.1
inside = lambda v: v is not None and abs(math.log10(v)) <= 0.1
BOXES = [(100, 128), (100, 256), (200, 128), (200, 256)]
FT = {"canonical": "can", "alt": "alt"}

def s0_json(L, N):
    b = os.path.join(W530, "runs", f"S0_L{L}_N{N}", f"cfg527_S0_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N{N}" + (f"_L{L}" if L != 200 else "") + "_drawSHELL.json")
    return json.load(open(b))
def lr_json(foot, L, N):
    tag = "LRcan" if foot == "canonical" else "LRalt"
    d = os.path.join(W530, "runs", f"{tag}_L{L}_N{N}")
    if not os.path.isdir(d): return None
    f = [x for x in os.listdir(d) if x.startswith("cfg527_RES") and x.endswith(".json")]
    return json.load(open(os.path.join(d, f[0]))) if f else None
def run_json(name):
    p = PR.RUNS[name][7]
    return json.load(open(p)) if os.path.exists(p) else None

def growth(js, s0, L, N):
    a, b = js["snap"]["z0"], s0["snap"]["z0"]
    k = np.array(a["k"]); r = np.array(a["P"]) / np.array(b["P"])
    kny = math.pi * N / L
    m = k <= min(1.0, kny / 4)
    s8 = a["sigma8"] / b["sigma8"]; mx = float(np.max(np.abs(r[m] - 1)))
    v = "GROWTH OK" if abs(s8 - 1) <= 0.05 and mx <= 0.10 else ("FAIL" if abs(s8 - 1) > 0.2 else "TENSION")
    def at(kk):
        if kk > kny / 2 + 1e-9: return None
        return float(r[int(np.argmin(np.abs(k - kk)))])
    stab_r = float(r[int(np.argmin(np.abs(k - kny / 2)))])
    finite = all(np.all(np.isfinite(np.array(js["snap"][s]["P"]))) and math.isfinite(js["snap"][s]["sigma8"]) for s in js["snap"])
    return {"sigma8_ratio": s8, "max_abs_r_minus_1": mx, "k_at_max": float(k[m][int(np.argmax(np.abs(r[m] - 1)))]), "kmax_cut": min(1.0, kny / 4),
            "verdict": v, "r": {str(kk): at(kk) for kk in (0.3, 0.5, 1.0, 2.0, 4.0)}, "r_kNyq2": stab_r,
            "stable": bool(finite and stab_r <= 2.0)}

def t3_census(name):
    """origin of the settled (drifted) cold energy, from the z = 0 positions and the cumulative settling displacement D (EOM A)."""
    out = os.path.join(PR.PROF, f"t3_{name}.json")
    if os.path.exists(out): return json.load(open(out))
    L, N, foot, eom, edge_on, mob, npz, jsp = PR.RUNS[name]
    mod = PR.load_engine(name); z = np.load(npz)
    pb = z["pos_b"].astype(np.float64); pc = z["pos_c"].astype(np.float64); Dc = z["Dacc"].astype(np.float64)
    mesh = mod.Mesh(N); dta = mod.dta_table()
    dtot, db, dc = mod.deposit2(mesh, pb, pc); del pb
    D = json.load(open(jsp))["snap"]["z0"]["Delta_ta"]
    edge = mod.in_cover(mesh, dtot, D, None, 1.0, "FLAT", foot)
    catch, _ = mod.in_cover(mesh, dtot, D, 1.0, 1.0, "FLAT", foot, want_fret=True)
    dx = L / N
    def cell(p):
        i = np.floor(p / dx).astype(np.int64) % N; return (i[:, 0] * N + i[:, 1]) * N + i[:, 2]
    dn = np.sqrt((Dc ** 2).sum(1)) / dx; drift = dn > 0.5
    fe = edge.ravel()[cell(pc)]; orig = (pc - Dc) % L; oc = cell(orig)
    oe = edge.ravel()[oc]; ocat = catch.ravel()[oc]
    m_in = drift & fe
    res = {"n_cold": int(pc.shape[0]), "frac_drifted": float(drift.mean()),
           "frac_drifted_ending_in_edge": float(m_in.sum() / max(drift.sum(), 1)),
           "returned_frac": float((drift & ~fe).sum() / max(drift.sum(), 1)),
           "in_edge_origin_outside_edge": float((m_in & ~oe).sum() / max(m_in.sum(), 1)),
           "in_edge_origin_shell": float((m_in & ~oe & ocat).sum() / max(m_in.sum(), 1)),
           "in_edge_origin_outside_catch": float((m_in & ~ocat).sum() / max(m_in.sum(), 1)),
           "in_edge_origin_inside_edge": float((m_in & oe).sum() / max(m_in.sum(), 1)),
           "cold_frac_in_edge": float(((1.0 + dc) * edge).sum() / (1.0 + dc).sum()),
           "baryon_frac_in_edge": float(((1.0 + db) * edge).sum() / (1.0 + db).sum()),
           "mean_drift_cells_drifted": float(dn[drift].mean()) if drift.any() else 0.0}
    json.dump(res, open(out, "w")); return res

def finished():
    return [n for n, v in PR.RUNS.items() if v[3] in ("A", "C", "OFF") and os.path.exists(v[7])]

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "compute":
    try: os.nice(10)
    except OSError: pass
    for L, N in BOXES:
        for ft in ("can", "alt"):
            PR.compute(f"S0{ft}_L{L}_N{N}")
    for n in finished():
        if PR.RUNS[n][3] == "OFF": continue
        PR.compute(n)
        if PR.RUNS[n][3] == "A" and PR.RUNS[n][1] == 256:
            t3_census(n)
    sys.exit(0)

# ============================================================== analysis
def law(name):
    L, N = PR.RUNS[name][0], PR.RUNS[name][1]
    if not os.path.exists(os.path.join(PR.PROF, f"N{N}", f"cfg526_{name}.npz")): return None
    res, h = PR.analyse(name)
    d = np.load(os.path.join(PR.PROF, f"N{N}", f"cfg526_{name}.npz"))
    info = json.loads(str(d["info"])); K = json.loads(str(d["K"]))
    out = {"n_scored": res["n_scored"], "u": info.get("unfilled_frac"), "cold_frac_in_edge": info.get("cold_frac_in_edge"), "K": K}
    if h is not None:
        out.update(core_R=res["core"]["R"][0], core_D_law=res["core"]["D_law"][0], core_D_eng=res["core"]["D_eng"][0],
                   per=[(p["R_cells"], p["n"], p["R"][0] if p["R"] else None) for p in res["per"]])
    return out

def kcheck(lw):
    sh = lw["K"].get("shared", {}); bad = [k for k, (a, b) in sh.items() if abs(a - b) > 1e-3 * max(abs(b), 1e-12)]
    return (len(bad) == 0 and lw["K"]["pk_z0_check"] <= 1e-6), bad

RES = {"runs": {}, "S0": {}, "controls": {}, "verdict": {}}
P("CFG539 Stage 2: two-species PM, cold energy obeying a candidate equation of motion (no extra source term), seed 359, NSEED 512, z = 0")
P("kappa = 1/2 FITTED; footings never pooled; a0 flat; nu_mono; cold energy MASS still required; not theory closed. Matched S0 = CFG530's.")

# controls: OFF identity
idok = True; idd = {}
for L in (100, 200):
    a = run_json(f"OFF_L{L}_N128"); b = s0_json(L, 128)
    if a is None: idok = None; continue
    ds = max(abs(a["snap"][s]["sigma8"] / b["snap"][s]["sigma8"] - 1) for s in a["snap"])
    dp = max(float(np.max(np.abs(np.array(a["snap"][s]["P"]) / np.array(b["snap"][s]["P"]) - 1))) for s in a["snap"])
    idd[L] = [ds, dp]; idok = idok and ds <= 1e-6 and dp <= 1e-5
P(f"\nControl OFF identity (two-species code path, EOM off, vs CFG530 S0 128^3): {idd} -> {'PASS' if idok else ('PENDING' if idok is None else 'FAIL')}")
RES["controls"]["OFF_identity"] = {"pass": idok, "diffs": idd}
idc = PR.identity_check(); stat_ok = abs(list(idc.values())[0] - list(idc.values())[1]) <= 1e-12
P(f"Control statistic copy identity (CFG526 analyse vs patched, CFG530 LRcan_L200 N256): {idc} -> {'PASS' if stat_ok else 'FAIL'}")
RES["controls"]["stat_identity"] = {"pass": stat_ok, "values": idc}

# S0 law per footing
for L, N in BOXES:
    for foot, ft in FT.items():
        lw = law(f"S0{ft}_L{L}_N{N}")
        RES["S0"][f"{ft}_L{L}_N{N}"] = lw

P("\nGrowth (z = 0, vs matched S0; CFG361 cuts over k <= min(1, k_Nyq/4)) and law statistic per run:")
P(" run                        sig8r   max|r-1| (k)    verdict    r(0.5)  r(1)   r(2)   r(4)   stab  | coreR (S0)        n   u (S0)          dir  fill  law0.1 | LR-bookkeeping max|r-1|, coreR")
order = [f"{e}{ft}{sfx}_L{L}_N{N}" for e in ("A", "C") for sfx in ("", "_NOEDGE", "_mob0.5", "_mob2") for ft in ("can", "alt") for L, N in BOXES]
for name in order:
    js = run_json(name)
    if js is None: continue
    L, N, foot = PR.RUNS[name][0], PR.RUNS[name][1], PR.RUNS[name][2]
    g = growth(js, s0_json(L, N), L, N)
    lw = law(name); s0l = RES["S0"].get(f"{FT[foot]}_L{L}_N{N}") or {}
    row = {"growth": g, "law": lw, "settle": {k: v for k, v in js["snap"]["z0"].items() if k.startswith("drift") or k.startswith("settle_")},
           "z0_diag": {k: js["snap"]["z0"].get(k) for k in ("unfilled_frac", "cold_frac_in_edge", "cold_over_baryon_in_edge", "mass_frac_in_catch")}}
    zc = js["snap"]["z0"]
    if "P_c" in zc:
        k = np.array(zc["k"]); mlow = k <= 0.2
        row["T6_Pc_over_Pb_maxdev_k02"] = float(np.max(np.abs(np.array(zc["P_c"])[mlow] / np.array(zc["P_b"])[mlow] - 1)))
    lr = lr_json(foot, L, N)
    if lr is not None and "_NOEDGE" not in name and "_mob" not in name:
        gl = growth(lr, s0_json(L, N), L, N); row["LR_bookkeeping"] = {"max_abs_r_minus_1": gl["max_abs_r_minus_1"], "r": gl["r"], "verdict": gl["verdict"]}
    if lw is not None and "core_R" in lw and s0l and "core_R" in s0l:
        row["T1"] = {"direction": abs(math.log10(lw["core_R"])) < abs(math.log10(s0l["core_R"])),
                     "fill": (lw["u"] is not None and s0l.get("u") is not None and lw["u"] <= 0.5 * s0l["u"]),
                     "law_consistent": (lw["n_scored"] >= 20 and inside(lw["core_R"]) and all(inside(r) for _, n, r in lw["per"] if n >= 1)),
                     "law_consistent_10halo": (lw["n_scored"] >= 10 and inside(lw["core_R"]) and all(inside(r) for _, n, r in lw["per"] if n >= 1)),
                     "S0_core_R": s0l["core_R"], "S0_u": s0l.get("u")}
        row["K_ok"], row["K_bad"] = kcheck(lw)
    RES["runs"][name] = row
    f = lambda v: "  -   " if v is None else f"{v:6.3f}"
    t1 = row.get("T1", {})
    P(f" {name:26s} {g['sigma8_ratio']:.4f}  {g['max_abs_r_minus_1']:.3f} ({g['k_at_max']:.2f})  {g['verdict']:9s}  {f(g['r']['0.5'])} {f(g['r']['1.0'])} {f(g['r']['2.0'])} {f(g['r']['4.0'])} "
      f"{'ok' if g['stable'] else 'UNST'}  | "
      + (f"{lw['core_R']:.3f} ({t1.get('S0_core_R', float('nan')):.3f})  {lw['n_scored']:3d} {lw['u']:.3f} ({(t1.get('S0_u') or float('nan')):.3f})  "
         f"{'Y' if t1.get('direction') else 'n'}    {'Y' if t1.get('fill') else 'n'}    {'Y' if t1.get('law_consistent') else ('y10' if t1.get('law_consistent_10halo') else 'n')}"
         if lw and "core_R" in lw else "   (law pending / no scored halos)")
      + (f" | {row['LR_bookkeeping']['max_abs_r_minus_1']:.3f}" if "LR_bookkeeping" in row else ""))

# T3 census
P("\nT3 origin census (EOM A, 256^3; masks at z = 0):")
for name in [n for n in RES["runs"] if n.startswith("A") and n.endswith("N256")]:
    p = os.path.join(PR.PROF, f"t3_{name}.json")
    if os.path.exists(p):
        c = json.load(open(p)); RES["runs"][name]["T3"] = c
        P(f"  {name:26s} drifted {c['frac_drifted']:.3f} of cold particles (mean {c['mean_drift_cells_drifted']:.2f} cells); of drifted ending in edge "
          f"({c['frac_drifted_ending_in_edge']:.3f}): origin outside edge {c['in_edge_origin_outside_edge']:.3f} (shell {c['in_edge_origin_shell']:.3f}, "
          f"outside catchment {c['in_edge_origin_outside_catch']:.3f}); returned (drifted, now outside edge) {c['returned_frac']:.3f}; "
          f"cold/baryon fraction in edges {c['cold_frac_in_edge']:.4f}/{c['baryon_frac_in_edge']:.4f}")

# verdicts
def conv(cls, ft):
    items = {}; ev_R = False; ok = True
    for L, kk in ((100, "1.0"), (200, "0.5")):
        a, b = RES["runs"].get(f"{cls}{ft}_L{L}_N128"), RES["runs"].get(f"{cls}{ft}_L{L}_N256")
        if a is None or b is None: items[L] = "PENDING"; ok = None; continue
        ra, rb = a["growth"]["r"][kk], b["growth"]["r"][kk]
        dr = None if ra is None or rb is None else abs(rb - ra)
        it = {"k": float(kk), "r128": ra, "r256": rb, "dr": dr, "pass_r": dr is not None and dr <= 0.05}
        la, lb = a.get("law") or {}, b.get("law") or {}
        if la.get("n_scored", 0) >= 10 and lb.get("n_scored", 0) >= 10 and "core_R" in la and "core_R" in lb:
            dl = abs(math.log10(lb["core_R"]) - math.log10(la["core_R"])); it.update(dlogR=dl, pass_R=dl <= 0.05); ev_R = True
        else:
            it.update(dlogR=None, pass_R=None)
        items[L] = it
        if ok is not None:
            ok = ok and it["pass_r"] and (it["pass_R"] in (True, None))
    if ok is not None and not ev_R: return "NOT EVALUABLE", items
    return ("PENDING" if ok is None else ("PASS" if ok else "FAIL")), items

P("\nVerdicts (per class, per footing; frozen rules):")
for cls in ("A", "C"):
    for foot, ft in FT.items():
        why = []; pend = []
        runs = {f"L{L}_N{N}": RES["runs"].get(f"{cls}{ft}_L{L}_N{N}") for L, N in BOXES}
        for k_, r in runs.items():
            if r is None: pend.append(f"{k_} not run"); continue
            if not r["growth"]["stable"]: why.append(f"{k_} UNSTABLE (INVALID run)")
            if r["growth"]["verdict"] != "GROWTH OK": why.append(f"T4 {k_} {r['growth']['verdict']} (max|r-1| {r['growth']['max_abs_r_minus_1']:.3f}, sigma8 {r['growth']['sigma8_ratio']:.4f})")
        for L in (100, 200):
            r = runs.get(f"L{L}_N256")
            if r is None: continue
            t1 = r.get("T1")
            if t1 is None: pend.append(f"T1 L{L} law pending"); continue
            if not t1["law_consistent"]: why.append(f"T1(a) L{L} not law-consistent (core R {r['law']['core_R']:.3f}, n {r['law']['n_scored']})")
            if not t1["direction"]: why.append(f"T1(b) L{L} core R {r['law']['core_R']:.3f} not closer to 1 than S0 {t1['S0_core_R']:.3f}")
            if not t1["fill"]: why.append(f"T1(c) L{L} u {r['law']['u']:.3f} > 0.5 x S0 {t1['S0_u']:.3f}")
        if foot == "canonical":
            for L in (100, 200):
                r = runs.get(f"L{L}_N256")
                if r is None: continue
                if cls == "A":
                    c = r.get("T3")
                    if c is None: pend.append(f"T3 L{L}")
                    elif c["in_edge_origin_outside_edge"] < 0.5: why.append(f"T3 L{L} only {c['in_edge_origin_outside_edge']:.2f} of settled from outside the edge")
                else:
                    s0l = RES["S0"].get(f"can_L{L}_N256") or {}
                    if r.get("law") and s0l.get("cold_frac_in_edge") is not None and r["law"]["cold_frac_in_edge"] is not None:
                        if not r["law"]["cold_frac_in_edge"] > s0l["cold_frac_in_edge"]: why.append(f"T3 L{L} no net inflow into edges")
        cv, citems = conv(cls, ft)
        if cv == "FAIL": why.append("convergence 128->256 FAIL " + json.dumps({k: {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in it.items()} for k, it in citems.items() if isinstance(it, dict)}))
        elif cv in ("PENDING", "NOT EVALUABLE"): pend.append(f"convergence {cv}")
        rob = None
        if cls == "A" and foot == "canonical":
            base = RES["runs"].get("Acan_L200_N256"); rob = {}
            for mb in ("0.5", "2"):
                r = RES["runs"].get(f"Acan_mob{mb}_L200_N256")
                if base is None or r is None or not r.get("law") or not base.get("law") or "core_R" not in r["law"] or "core_R" not in base["law"]:
                    pend.append(f"robustness mob{mb}"); continue
                dm = abs(r["growth"]["max_abs_r_minus_1"] - base["growth"]["max_abs_r_minus_1"]); dl = abs(math.log10(r["law"]["core_R"] / base["law"]["core_R"]))
                same = r["growth"]["verdict"] == base["growth"]["verdict"]; okr = same and dm <= 0.05 and dl <= 0.05
                rob[mb] = {"d_maxr": dm, "dlogR": dl, "same_T4": same, "pass": okr}
                if not okr: why.append(f"robustness mob{mb}: coefficient acts as a knob (d max|r-1| {dm:.3f}, d logR {dl:.3f}, same T4 {same})")
        ms = None
        if cls == "A" and foot == "canonical":
            ms = {}
            for L in (100, 200):
                r = RES["runs"].get(f"Acan_NOEDGE_L{L}_N256")
                if r is None or not r.get("law") or "core_R" not in r["law"]: pend.append(f"MUTATE-S L{L}"); continue
                ms[L] = {"T4": r["growth"]["verdict"], "max_r": r["growth"]["max_abs_r_minus_1"], "core_R": r["law"]["core_R"]}
            dist = any(v["T4"] != "GROWTH OK" or v["core_R"] > 10 ** 0.1 for v in ms.values()) if ms else None
            ms["distinguishable"] = dist
        if idok is False or not stat_ok:
            v = "INVALID"
        elif why:
            v = "NOT VIABLE"
        elif pend:
            v = "INCONCLUSIVE"
        else:
            v = "VIABLE (T2 INHERITED, not emergent)" if cls == "A" else "VIABLE (T2 INHERITED)"
        RES["verdict"][f"{cls}_{foot}"] = {"verdict": v, "failing": why, "pending": pend, "convergence": [cv, citems], "robustness": rob, "MUTATE_S": ms}
        P(f"  [{cls} {foot}] {v}")
        for w_ in why: P(f"      - {w_}")
        for w_ in pend: P(f"      ~ {w_}")
        if ms: P(f"      MUTATE-S (no edge): {json.dumps(ms)}")
        if rob: P(f"      robustness: {json.dumps(rob)}")
        P(f"      convergence: {cv} {json.dumps(citems, default=lambda o: round(o, 3) if isinstance(o, float) else o)}")

open(os.path.join(HERE, "cfg539_analysis.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg539_results.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating,)) else (bool(o) if isinstance(o, np.bool_) else str(o)))
