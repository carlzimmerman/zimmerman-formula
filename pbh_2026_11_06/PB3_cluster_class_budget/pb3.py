#!/usr/bin/env python3
"""PB3 (FROZEN_CRITERIA.md 05d916ef99): a uniform-born PBH population (ratio F to baryons) as the cluster / class extra mass.
    python3 pb3.py            -> pb3.json / pb3.out          (budget, models U and I, labels, segregation, millilensing)
    python3 pb3.py --mutate   -> pb3_MUTATE.json / .out      (M1 planted perfect segregation = DX1 O1; M2 F = 0 = GB1 L0; M3 U fails SPARC)
    python3 pb3.py --bullet   -> pb3_bullet.json / .out      (DB1's Bullet machinery, read-only, PBHs on the galaxies)
Read-only use of GB1 (battery), KD1, DX1, SE2, DB1. PBH mass is a component that must be paid for. Adopts nothing.
kappa = 1/2 FITTED; footings never pooled; not theory closed.  1 thread."""
import os, sys, json, math, io
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; BUL = "--bullet" in sys.argv
TAG = "pb3_MUTATE" if MUT else ("pb3_bullet" if BUL else "pb3"); OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
def dump(RES):
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")

# ------------------------------------------------------------------ physical constants (SI)
Gs, MSs, KPCs, Cs = 6.674e-11, 1.989e30, 3.0857e19, 2.998e8
H0 = 70.0e3 / (1e3 * KPCs); RHO_C0 = 3 * H0 ** 2 / (8 * math.pi * Gs)      # h = 0.70, PROVISIONAL convention
T_H = 13.8e9 * 3.156e7; OMB = 0.02166 / 0.70 ** 2                          # BBN D/H Omega_b h^2 (PROVISIONAL, as DB1)

# =================================================================== Bullet mode (DB1 machinery, read-only)
if BUL:
    DB1 = os.path.join(RB, "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read()
    cut = src.index("# ---------- X-COP, own replica"); pre = src[:cut]
    a = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a) == 1
    pre = pre.replace(a, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); cwd = os.getcwd(); os.chdir(DB1); av = sys.argv; sys.argv = [os.path.join(DB1, "db1_fast.py"), "pb3"]
    ns = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_pb3"}
    try: exec(compile(pre, "db1_fast_prefix", "exec"), ns)
    finally: sys.argv = av
    PJ = json.load(open(os.path.join(HERE, "pb3.json")))
    RES = dict(tag=TAG, criteria="05d916ef99", note="DB1 Bullet machinery read-only; PBHs placed on the galaxies (collisionless); kappa = 1/2 FITTED; not theory closed")
    MST, MGJ = ns["MST"], ns["MGJ"]
    P(f"PB3 BULLET. subcluster stars {MST[0]:.3e}, {MST[1]:.3e}; gas {MGJ[0]:.3e}, {MGJ[1]:.3e} Msun (gas/stars {MGJ[0]/MST[0]:.2f}, {MGJ[1]/MST[1]:.2f})")
    k = ns["bullet_row"]("Z", "canonical", 0.0, Rs=[0.0, 0.0])
    ok4 = abs(k["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k["dkappa"][0] + 0.068) < 0.002 and abs(k["dkappa"][1] + 0.111) < 0.002
    RES["KA4"] = dict(row=k, ok=bool(ok4)); P(f"KA4 R = 0: M300 {k['M300'][0]:.3e}, {k['M300'][1]:.3e}; dkappa {k['dkappa'][0]:+.3f}, {k['dkappa'][1]:+.3f} -> {'PASS' if ok4 else 'FAIL'}")
    for f in ("canonical", "alt"):
        Fs = PJ["footings"][f]["U"]["F_SE2"]["X-COP"]
        Rs = [Fs * (MGJ[j] + MST[j]) / MST[j] for j in range(2)]
        b = ns["bullet_row"]("PBH", f, 0.0, Rs=Rs, on="gal"); RES[f] = dict(F=Fs, row=b)
        P(f"[{f}] PBH F {Fs:.3f}: R {Rs[0]:.2f}, {Rs[1]:.2f}; M_PBH {b['Mcb'][0]/1e14:.2f}, {b['Mcb'][1]/1e14:.2f} e14; Bullet {b['label']} ({b['cls']}), "
          f"M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14, Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; dkappa main {b['dkappa'][0]:+.3f}, sub {b['dkappa'][1]:+.3f}")
    os.chdir(cwd); P("kappa = 1/2 FITTED; not theory closed."); dump(RES); sys.exit(0)

# =================================================================== battery (GB1, read-only, as DX1 loads it)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}
    a = sys.argv; sys.argv = [path]
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
GBP = os.path.join(CL, "GB1_all_gates_battery", "gb1.py")
GB = load_prefix(GBP, "# ------------------------------------------------------------------ main", "gb1_lib")
_gs = open(GBP).read(); _i = _gs.index("def short(g, r):"); _j = _gs.index("for cn, mk in CANDS.items():")
exec(compile(_gs[_i:_j], "gb1_short", "exec"), GB)
GBJ = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
KDJ = json.load(open(os.path.join(CL, "KD1_unpinned_kq_dust", "kd1.json")))
DXJ = json.load(open(os.path.join(CL, "DX1_disc_only_exclusion", "dx1.json")))
SEJ = json.load(open(os.path.join(CL, "SE2_step_as_systematics", "se2.json")))
D1P = json.load(open(os.path.join(RB, "DB1_cluster_dark_baryons", "db1_phys.json")))
A0 = GB["A0"]; G, MS = GB["G"], GB["MS"]
RES = dict(tag=TAG, criteria="05d916ef99", note="PBH mass must be paid for; adopts nothing; kappa = 1/2 FITTED; not theory closed", KA={}, footings={})
P(f"PB3 {'MUTATE' if MUT else 'MAIN'}. Uniform-born PBHs (ratio F to baryons). kappa = 1/2 FITTED; not theory closed; footings never pooled.")

_ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), dx="D", pb="SS")
def tag(pts, dx, pb):
    for p in pts: p["feat"]["dx"] = dx; p["feat"]["pb"] = pb
BATT = {}
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0); GRp = {0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}
    U = GB["udgs"](f, a0); Dd = GB["dsphs"](f, a0); K = GB["kids"](a0)
    st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    tag(S, "D", "S"); tag(E, "H", "E"); tag(X, "H", "X"); tag(U, "H", "U")
    for fst in (0, 1):
        for g in GRp[fst]: tag(g["pts"], "H", "G")
    for cls in Dd: tag(Dd[cls], "H", "Dsph")
    for ft in K[0]: ft["dx"] = "H"; ft["pb"] = "K"
    for ft in K[1]: ft["dx"] = "D"; ft["pb"] = "K"
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=Dd, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - GB["KA20"][f][k]) for k in cm)
    RES["KA"][f"KA1b_{f}"] = dict(maxdiff=float(d1), ok=bool(d1 <= 1e-6)); P(f"[{f}] KA1b GB1 L0 class means vs KA20: max|d| {d1:.1e} -> {'PASS' if d1 <= 1e-6 else 'FAIL'}")

# ------------------------------------------------------------------ PBH mass per feature
def masses(ft, a0):
    """(M_b(<r), M_b,tot) in Msun, r in m; None if not computable (b stays 1)."""
    k = ft["pb"]; r = ft["r"]
    if k in ("S", "X", "G", "E"): return ft["Mb"], a0 * (r / ft["rrM"]) ** 2 / G / MS, r
    if k in ("U", "Dsph"):
        if ft.get("Mb") is None: return None
        return ft["Mb"] / 2.0, ft["Mb"], r
    if k == "K": m = ft["x"] * a0 * r ** 2 / G / MS; return m, m, r
    return None
def rvir(Mtot, F, s): return s * (3 * (1 + F) * Mtot * MSs / (4 * math.pi * 200 * RHO_C0)) ** (1 / 3)
def frac_in(r, rv, prof):
    if r >= rv: return 1.0
    if prof == "SIS": return r / rv
    a = rv / 10.0; return (r / (r + a)) ** 2 / (rv / (rv + a)) ** 2
def b_pbh(ft, a0, F, model):
    if F == 0.0 or ft["pb"] == "SS": return 1.0
    if model == "U": return 1.0 + F
    m = masses(ft, a0)
    if m is None: return 1.0
    Menc, Mtot, r = m; prof, s = MODELS[model]
    return 1.0 + F * Mtot * frac_in(r, rvir(Mtot, F, s), prof) / Menc
MODELS = {"I": ("SIS", 1.0), "I_s0.5": ("SIS", 0.5), "I_s2": ("SIS", 2.0), "I_Hern": ("HERN", 1.0)}
def cand(F, model, a0): return lambda ft: dict(b=b_pbh(ft, a0, F, model), F=1.0, T=0.0)
nomass = {f: sum(1 for c_ in BATT[f]["D"].values() for p in c_ if masses(p["feat"], A0[f]) is None) for f in A0}
P(f"dSph points without Ms (b stays 1): canonical {nomass['canonical']}, alt {nomass['alt']}")

# ------------------------------------------------------------------ class shifts (dex)
dl = lambda c, pts, a0: np.array([GB["delta"](c, p["feat"], a0) for p in pts])
def shifts(c, B, a0):
    sS = float(dl(c, B["S"], a0).mean()); o = {"SPARC": sS}
    o["X-COP"] = float(dl(c, B["X"], a0).mean()); o["ellipticals"] = float(dl(c, B["E"], a0).mean())
    o["Coma UDGs"] = float(dl(c, B["U"], a0).mean())
    for fst in (0, 1): o[f"groups_fst{fst}"] = float(np.mean([GB["delta"](c, p["feat"], a0) for g in B["GR"][fst] for p in g["pts"]]))
    Ee, Ll = B["K"]; o["KiDS"] = float(np.mean([GB["delta"](c, e, a0) - GB["delta"](c, l, a0) for e, l in zip(Ee, Ll)]))
    for cls in ("bright M31", "MW classical", "LG field"): o[cls] = float(np.median(dl(c, B["D"][cls], a0))) - sS
    return o
SE = {f: SEJ["footings"][f]["cells"] for f in A0}
GRADED = ("ellipticals", "KiDS", "X-COP", "groups_fst0", "groups_fst1", "bright M31", "Coma UDGs")
def se_cell(f, k): return SE[f]["groups" if k.startswith("groups") else k]["post"]
def inside(f, k, d): lo, hi = se_cell(f, k)["ci95"]; return bool(lo <= d <= hi)

def grade(c, f):
    a0 = A0[f]; B = BATT[f]; return {g: GB["run_gate"](fn, c, B, a0, fills) for g, fn, fills in GB["GATES"]}
def flat(x, p=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items(): o.update(flat(v, p + "/" + k))
        return o
    if isinstance(x, (list, tuple)):
        o = {}
        for i, v in enumerate(x): o.update(flat(v, p + f"[{i}]"))
        return o
    return {p: x}
def same(row, ref):
    dmax = 0.0; ok = True
    for g in row:
        a, b = flat(dict(num=row[g]["num"], br=row[g]["bracket"])), flat(dict(num=ref[g]["num"], br=ref[g]["bracket"]))
        ok &= (a.keys() == b.keys()) and row[g]["status"] == ref[g]["status"]
        for k in a:
            if k in b and isinstance(a[k], (int, float)) and not isinstance(a[k], bool): dmax = max(dmax, abs(a[k] - b[k]))
            elif k in b: ok &= a[k] == b[k]
    return bool(ok and dmax <= 1e-12), float(dmax)

# =================================================================== MUTATE
if MUT:
    allok = True
    for f in A0:
        a0 = A0[f]; fon = float(KDJ["footings"][f]["uniform_f_diag"]["capture_f"])
        O1 = lambda ft: dict(b=1.0 * (1.0 + (fon if ft["dx"] == "H" else 0.0)), F=1.0, T=0.0)
        ok1, d1 = same(grade(O1, f), DXJ["footings"][f]["rows"]["O1"])
        P(f"[{f}] M1 planted perfect segregation (f_on {fon:.5f}) vs DX1 O1: max|d| {d1:.1e}, statuses equal -> {'HOLDS' if ok1 else 'BROKEN'}")
        for m in ["U"] + list(MODELS):
            ok2, d2 = same(grade(cand(0.0, m, a0), f), GBJ["cands"]["L0"][f]); allok &= ok2
            P(f"[{f}] M2 F = 0 model {m:7s} vs GB1 L0: max|d| {d2:.1e} -> {'HOLDS' if ok2 else 'BROKEN'}")
        Fst = json.load(open(os.path.join(HERE, "pb3.json")))["footings"][f]["U"]["F_SE2"]["X-COP"]
        ok3, n3 = GB["g_sparc"](cand(Fst, "U", a0), BATT[f], a0)
        P(f"[{f}] M3 model U at F* {Fst:.3f}: SPARC G1 {'PASS' if ok3 else 'FAIL'} Z {n3['Z']:+.4f} rms {n3['rms']:.4f} -> {'BITES' if not ok3 else 'NO BITE'}")
        RES["footings"][f] = dict(M1=dict(ok=ok1, maxdiff=d1), M3=dict(sparc_pass=bool(ok3), num=n3)); allok &= ok1 and not ok3
    RES["MUTATE_all"] = bool(allok); P(f"MUTATE: {'all hold / bite' if allok else 'SOMETHING BROKEN'}"); P("kappa = 1/2 FITTED; not theory closed."); dump(RES); sys.exit(0 if allok else 1)

# =================================================================== KA1 (DB1), KA2 (KD1 needs under U), KA3 (SE2 table)
am = D1P["amounts_300kpc"]; ka1 = {k: am[k]["cb_over_gas"] for k in ("P1G|canonical", "P1G|alt", "P3|canonical", "P3|alt")}
ok = abs(ka1["P1G|canonical"] - 4.82) < 0.005 and abs(ka1["P1G|alt"] - 4.36) < 0.005 and abs(ka1["P3|canonical"] - 5.44) < 0.005 and abs(ka1["P3|alt"] - 4.82) < 0.005
RES["KA"]["KA1_DB1"] = dict(values=ka1, range=[min(ka1.values()), max(ka1.values())], ok=bool(ok))
P(f"KA1 DB1 M_cb/M_gas at 300 kpc: P1G {ka1['P1G|canonical']:.2f} / {ka1['P1G|alt']:.2f}, P3 {ka1['P3|canonical']:.2f} / {ka1['P3|alt']:.2f}; range {min(ka1.values()):.2f}-{max(ka1.values()):.2f} -> {'PASS' if ok else 'FAIL'}")
SE2TAB = {"canonical": {"ellipticals": (0.067, -0.201, 0.271), "KiDS": (0.085, -0.087, 0.233), "X-COP": (0.440, 0.372, 0.484), "groups": (0.232, 0.078, 0.362),
                        "bright M31": (0.228, -0.213, 0.685), "Coma UDGs": (1.120, 0.541, 1.718)},
          "alt": {"ellipticals": (0.050, -0.218, 0.252), "KiDS": (0.084, -0.085, 0.235), "X-COP": (0.408, 0.341, 0.451), "groups": (0.194, 0.041, 0.324),
                  "bright M31": (0.219, -0.225, 0.676), "Coma UDGs": (1.075, 0.472, 1.673)}}
d3 = max(abs(round(v, 3) - w) for f in A0 for k, t in SE2TAB[f].items() for v, w in zip([SE[f][k]["post"]["median"]] + SE[f][k]["post"]["ci95"], t))
RES["KA"]["KA3_SE2"] = dict(maxdiff=float(d3), ok=bool(d3 <= 1.0e-3 + 1e-12)); P(f"KA3 SE2 medians / ci95 vs RESULT.md table (3 dp): max|d| {d3:.1e} -> {'PASS' if d3 <= 1.001e-3 else 'FAIL'}")

def need_F(fn, target=0.0, lo=-4.0, hi=4.0):
    g = lambda lf: fn(10 ** lf) - target
    try: return 10 ** brentq(g, lo, hi)
    except ValueError: return None
def resid_fns(f, model):
    a0 = A0[f]; B = BATT[f]; c = lambda F: cand(F, model, a0)
    R = {"X-COP": lambda F: GB["g_xcop"](c(F), B, a0)[1]["mean"], "ellipticals": lambda F: GB["g_ell"](c(F), B, a0)[1]["mean"],
         "Coma UDGs": lambda F: GB["g_udg"](c(F), B, a0)[1]["mean"]}
    for fst in (0, 1): R[f"groups_fst{fst}"] = (lambda fst: lambda F: float(np.mean([p["D"] - GB["delta"](c(F), p["feat"], a0) for g in B["GR"][fst] for p in g["pts"]])))(fst)
    for cls in ("bright M31", "MW classical"): R[cls] = (lambda cls: lambda F: float(np.median([p["D"] - GB["delta"](c(F), p["feat"], a0) for p in B["D"][cls]])))(cls)
    return R
def sparc_max(f, model):
    a0 = A0[f]; lo, hi = 0.0, 10.0
    if not GB["g_sparc"](cand(hi, model, a0), BATT[f], a0)[0]:
        for _ in range(60):
            m_ = 0.5 * (lo + hi); lo, hi = (m_, hi) if GB["g_sparc"](cand(m_, model, a0), BATT[f], a0)[0] else (lo, m_)
        return lo
    return None   # passes at 10: no bound in range

kd_keys = {"X-COP": "Xcop_f_need", "ellipticals": "ell_f_need", "Coma UDGs": "udg_f_need", "groups_fst0": "groups_fst0_f_need", "groups_fst1": "groups_fst1_f_need",
           "bright M31": "dsph_bright M31_f_need", "MW classical": "dsph_MW classical_f_need"}
GRID = np.concatenate([[0.0], np.logspace(-3, 3, 121)])
for f in A0:
    a0 = A0[f]; B = BATT[f]; FO = {}; diag = KDJ["footings"][f]["uniform_f_diag"]
    for model in ["U"] + list(MODELS):
        M = {}; R = resid_fns(f, model)
        M["F_raw"] = {k: need_F(fn) for k, fn in R.items()}
        M["SPARC_F_max"] = sparc_max(f, model)
        # SE2 needs: class shift = SE2 posterior median
        sh = lambda F: shifts(cand(F, model, a0), B, a0)
        M["F_SE2"] = {k: need_F(lambda F, k=k: sh(F)[k], se_cell(f, k)["median"]) for k in GRADED}
        # grid: SPARC pass + T_SE2 per class
        rows = []
        for F in GRID:
            s_ = sh(F); okS = GB["g_sparc"](cand(F, model, a0), B, a0)[0]
            rows.append(dict(F=float(F), SPARC=bool(okS), **{k: inside(f, k, s_[k]) for k in GRADED}, shifts=s_))
        M["grid"] = rows
        def interval(k):
            Fs = [r["F"] for r in rows if r[k]]; return [min(Fs), max(Fs)] if Fs else None
        M["intervals"] = {k: interval(k) for k in ("SPARC",) + GRADED}
        allF = [r["F"] for r in rows if r["SPARC"] and all(r[k] for k in GRADED)]
        sxF = [r["F"] for r in rows if r["SPARC"] and r["X-COP"]]
        M["all_intersection"] = [min(allF), max(allF)] if allF else None; M["SPARC_XCOP_intersection"] = [min(sxF), max(sxF)] if sxF else None
        # F* (X-COP anchor) and per-class labels
        Fst = M["F_SE2"]["X-COP"]; M["F_star"] = Fst
        if Fst is not None:
            s_ = sh(Fst); okS, nS = GB["g_sparc"](cand(Fst, model, a0), B, a0)
            M["at_F_star"] = dict(shifts=s_, SPARC=dict(ok=bool(okS), **nS), inside={k: inside(f, k, s_[k]) for k in GRADED})
            if model != "U":
                fr = {}
                for key, pts in (("SPARC", B["S"]), ("X-COP", B["X"]), ("ellipticals", B["E"]), ("Coma UDGs", B["U"]), ("groups_fst0", [p for g in B["GR"][0] for p in g["pts"]]),
                                 ("bright M31", B["D"]["bright M31"]), ("MW classical", B["D"]["MW classical"]), ("KiDS early", [dict(feat=e) for e in B["K"][0]]), ("KiDS late", [dict(feat=l) for l in B["K"][1]])):
                    v = [(b_pbh(p["feat"], a0, Fst, model) - 1.0) / Fst for p in pts if masses(p["feat"], a0) is not None]
                    fr[key] = float(np.median(v)) if v else None
                M["S4_factor_at_F_star"] = fr
        FO[model] = M
        P(f"[{f}] model {model:7s} SPARC F_max {M['SPARC_F_max'] if M['SPARC_F_max'] is None else round(M['SPARC_F_max'], 4)}; F* (X-COP on SE2 median) {Fst if Fst is None else round(Fst, 4)}")
        P(f"[{f}]   F raw need: " + ", ".join(f"{k} {v:.3g}" if v is not None else f"{k} none" for k, v in M["F_raw"].items()))
        P(f"[{f}]   F SE2 need: " + ", ".join(f"{k} {v:.3g}" if v is not None else f"{k} none" for k, v in M["F_SE2"].items()))
        P(f"[{f}]   F intervals (grid): " + "; ".join(f"{k} {('[%.3g, %.3g]' % tuple(v)) if v else 'EMPTY'}" for k, v in M["intervals"].items()))
        P(f"[{f}]   SPARC & X-COP: {M['SPARC_XCOP_intersection']}; all graded: {M['all_intersection']}")
        if Fst is not None:
            a = M["at_F_star"]; P(f"[{f}]   at F*: SPARC {'PASS' if a['SPARC']['ok'] else 'FAIL'} Z {a['SPARC']['Z']:+.3f} rms {a['SPARC']['rms']:.3f}; shifts " +
                                  ", ".join(f"{k} {a['shifts'][k]:+.3f}{'(in)' if a['inside'].get(k) else ('(OUT)' if k in GRADED else '')}" for k in a["shifts"]))
            if "S4_factor_at_F_star" in M: P(f"[{f}]   S4 infall factor [M_PBH(<r)/M_b(<r)]/F medians: " + ", ".join(f"{k} {v:.3g}" for k, v in M["S4_factor_at_F_star"].items() if v is not None))
    # KA2: model U needs = KD1 needs
    dmax = 0.0
    for k, kk in kd_keys.items():
        a, b = FO["U"]["F_raw"][k], diag[kk]
        dmax = max(dmax, abs(a / b - 1) if (a is not None and b is not None) else (0.0 if a is None and b is None else 1.0))
    dS = abs(FO["U"]["SPARC_F_max"] / diag["SPARC_f_max"] - 1); ok2 = dmax <= 1e-6 and dS <= 1e-6
    RES["KA"][f"KA2_{f}"] = dict(maxrel=float(dmax), sparc_rel=float(dS), ok=bool(ok2))
    P(f"[{f}] KA2 model U needs vs KD1: max rel {dmax:.1e}, SPARC_f_max rel {dS:.1e} -> {'PASS' if ok2 else 'FAIL'}")
    RES["footings"][f] = FO

RES["KA_all"] = all(v["ok"] for v in RES["KA"].values()); P(f"KA all: {'PASS' if RES['KA_all'] else 'FAIL'}")

# ------------------------------------------------------------------ labels
def class_label(f, model, k):
    a = RES["footings"][f][model].get("at_F_star")
    if a is None: return "FAILS"
    if k == "SPARC": return "REPRODUCED" if a["SPARC"]["ok"] else "FAILS"
    return "REPRODUCED" if a["inside"][k] else "FAILS"
LAB = {}
for model in ["U"] + list(MODELS):
    per = {}
    for k in ("SPARC", "ellipticals", "KiDS", "X-COP", "groups", "bright M31", "Coma UDGs"):
        fl = {}
        for f in A0:
            if k == "groups":
                g0, g1 = class_label(f, model, "groups_fst0"), class_label(f, model, "groups_fst1")
                fl[f] = g0 if g0 == g1 else "BRACKETED"
            else: fl[f] = class_label(f, model, k)
        per[k] = fl["canonical"] if fl["canonical"] == fl["alt"] else f"SPLIT ({fl['canonical']} / {fl['alt']})"
    ov = {}
    for f in A0:
        M = RES["footings"][f][model]
        ov[f] = "PATTERN REPRODUCED" if M["all_intersection"] else ("PARTIAL" if M["SPARC_XCOP_intersection"] else "FAILS")
    LAB[model] = dict(per_class=per, overall_per_footing=ov, overall=ov["canonical"] if ov["canonical"] == ov["alt"] else f"SPLIT ({ov['canonical']} / {ov['alt']})")
    P(f"LABEL model {model:7s}: overall {LAB[model]['overall']}; per class " + ", ".join(f"{k} {v}" for k, v in per.items()))
RES["labels"] = LAB; RES["label"] = LAB["I"]["overall"]
P(f"PB3 LABEL (model I primary): {RES['label']}")

# ------------------------------------------------------------------ mass budget summary
BUD = {}
for f in A0:
    FO = RES["footings"][f]; nU = FO["U"]["F_SE2"]; Fx = nU["X-COP"]
    need_factor = {k: (v / Fx if v is not None else None) for k, v in nU.items()}
    allow = {k: FO["U"]["intervals"][k] for k in GRADED}
    BUD[f] = dict(F_XCOP_U=Fx, f_of_total=Fx / (1 + Fx), Omega_PBH=Fx * OMB, need_factor_vs_XCOP=need_factor,
                  SPARC_allowed_factor=FO["U"]["SPARC_F_max"] / Fx, M_PBH_over_Mgas_300kpc_XCOP=None)
    # X-COP: F per total baryons -> per gas, X-COP median gas fraction at the GB1 points
    fg = float(np.median([p["feat"]["fgas"] for p in BATT[f]["X"]])); BUD[f]["M_PBH_over_Mgas_XCOP"] = Fx / fg; BUD[f]["XCOP_fgas_median"] = fg
    mx = max(v for k, v in need_factor.items() if v is not None); mn = BUD[f]["SPARC_allowed_factor"]
    BUD[f]["spread_needed_UDG_over_SPARC"] = need_factor["Coma UDGs"] / mn if need_factor["Coma UDGs"] else None
    P(f"[{f}] BUDGET (U): X-COP needs F {Fx:.3f} (f = {Fx/(1+Fx):.3f} of baryons+PBH; Omega_PBH = {Fx*OMB:.3f} at Omega_b {OMB:.4f}); M_PBH/M_gas {Fx/fg:.2f} (X-COP fgas {fg:.3f}) vs DB1 4.4-5.4")
    P(f"[{f}]   needed factor vs X-COP (SE2 needs): " + ", ".join(f"{k} {v:.3g}" for k, v in need_factor.items() if v is not None) + f"; SPARC allows <= {mn:.3f}; spread UDG/SPARC {BUD[f]['spread_needed_UDG_over_SPARC']:.0f}x")
RES["budget"] = BUD

# S4b (frozen): baryon expulsion epsilon each class would need, model I at F*: delivered local ratio D = F* x S4 factor,
# needed U-equivalent ratio N = U's SE2 need (SPARC: U's F_max); F_local = D / (1 - eps).  eps < 0 means PBHs must be REMOVED.
EPS = {}
for f in A0:
    MI = RES["footings"][f]["I"]; fac = MI["S4_factor_at_F_star"]; Fst = MI["F_star"]; nU = RES["footings"][f]["U"]["F_SE2"]; o = {}
    for k, nk in (("SPARC", None), ("X-COP", "X-COP"), ("ellipticals", "ellipticals"), ("groups_fst0", "groups_fst0"), ("Coma UDGs", "Coma UDGs")):
        N = RES["footings"][f]["U"]["SPARC_F_max"] if k == "SPARC" else nU[nk]; D = Fst * fac[k]
        o[k] = dict(delivered=D, needed=N, eps=1 - D / N, note="upper bound (allowed max)" if k == "SPARC" else "")
    EPS[f] = o
    P(f"[{f}] S4b model I at F* {Fst:.3f}: delivered / needed local ratio and expulsion eps: " + ", ".join(f"{k} {v['delivered']:.3g}/{v['needed']:.3g} eps {v['eps']:+.3f}" for k, v in o.items()))
RES["S4b_expulsion"] = EPS
# post-freeze diagnostic (reported only, no label): intersection of every graded class except the Coma UDGs
PFD = {}
for f in A0:
    for model in ["U"] + list(MODELS):
        rows = RES["footings"][f][model]["grid"]
        Fs_ = [r["F"] for r in rows if r["SPARC"] and all(r[k] for k in GRADED if k != "Coma UDGs")]
        PFD[f"{f}|{model}"] = [min(Fs_), max(Fs_)] if Fs_ else None
P("POST-FREEZE (reported only): all graded classes except Coma UDGs intersect at F: " + "; ".join(f"{k} {v}" for k, v in PFD.items()))
RES["post_freeze_all_but_UDG"] = PFD

# ------------------------------------------------------------------ segregation processes S1, S2 (representative systems; Newtonian; order of magnitude)
Fs = RES["footings"]["canonical"]["I"]["F_star"] or RES["footings"]["canonical"]["U"]["F_SE2"]["X-COP"]
SYSR = {"SPARC disc": (10.0, 150.0, 5e10), "dSph": (0.3, 10.0, 1e7), "Coma UDG": (3.0, 25.0, 1e8), "elliptical": (10.0, 250.0, 3e11),
        "group": (100.0, 400.0, 3e13), "cluster": (300.0, 1000.0, 1e14)}
MGRID = [1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
SEG = dict(F_used=Fs, systems={})
P(f"SEGREGATION S1/S2 at F = {Fs:.3f} (canonical model I F*), SIS spheroid to r_vir, Newtonian, t_H 13.8 Gyr")
for nm, (rk, vk, Mb) in SYSR.items():
    r = rk * KPCs; v = vk * 1e3; rv = rvir(Mb, Fs, 1.0); Mp_tot = Fs * Mb
    Menc = Mp_tot * min(r / rv, 1.0); rho = Mp_tot * MSs / (4 * math.pi * rv * r ** 2) if r < rv else 0.0
    out = dict(r_kpc=rk, v_kms=vk, Mb=Mb, r_vir_kpc=rv / KPCs, M_PBH_tot=Mp_tot, M_PBH_in_r=Menc, rows={})
    for Mh in MGRID:
        lnL = lambda rr: max(math.log(rr * v ** 2 / (Gs * Mh * MSs)), 1.0)
        rs = r
        for _ in range(50): rs = math.sqrt(T_H * Gs * Mh * MSs * lnL(rs) / (1.17 * v))
        tdf = 1.17 * r ** 2 * v / (Gs * Mh * MSs * lnL(r))
        N = Menc / Mh; trel = 0.1 * N / max(math.log(N), 1.0) * r / v if N > 1 else 0.0
        evap = 1 - math.exp(-0.045 * T_H / trel) if trel > 0 else 1.0
        theat = v ** 3 / (Gs ** 2 * rho * Mh * MSs * lnL(r)) if rho > 0 else float("inf")
        out["rows"][f"{Mh:.0e}"] = dict(t_df_Gyr_at_r=tdf / 3.156e16, r_sink_kpc=rs / KPCs, sunk_frac=min(rs / rv, 1.0), N_in_r=N, t_rel_Gyr=trel / 3.156e16,
                                        evap_frac=evap, t_heat_stars_Gyr=theat / 3.156e16)
    SEG["systems"][nm] = out
    P(f"  {nm:10s} r {rk:g} kpc v {vk:g} km/s M_b {Mb:.0e}: r_vir {rv/KPCs:.0f} kpc, M_PBH(<r) {Menc:.2e} (of {Mp_tot:.2e})")
    for Mh, rw in out["rows"].items():
        P(f"     M {Mh}: t_df(r) {rw['t_df_Gyr_at_r']:.3g} Gyr, r_sink {rw['r_sink_kpc']:.3g} kpc (sunk {rw['sunk_frac']:.2g}), N(<r) {rw['N_in_r']:.3g}, "
          f"t_rel {rw['t_rel_Gyr']:.3g} Gyr, evaporated {rw['evap_frac']:.2g}, star heating time {rw['t_heat_stars_Gyr']:.3g} Gyr")
# disc heating (Lacey-Ostriker form) at the solar circle of a MW-like disc: sigma^2 = 8 pi G^2 rho M lnL t / v
r = 8 * KPCs; v = 220e3; Mb = 6e10; rv = rvir(Mb, Fs, 1.0); rho = Fs * Mb * MSs / (4 * math.pi * rv * r ** 2)
dh = {}
for Mh in MGRID:
    lnL = max(math.log(r * v ** 2 / (Gs * Mh * MSs)), 1.0); s2 = 8 * math.pi * Gs ** 2 * rho * Mh * MSs * lnL * T_H / v; dh[f"{Mh:.0e}"] = math.sqrt(s2) / 1e3
Mmax = None
for lM in np.linspace(2, 9, 701):
    Mh = 10 ** lM; lnL = max(math.log(r * v ** 2 / (Gs * Mh * MSs)), 1.0)
    if math.sqrt(8 * math.pi * Gs ** 2 * rho * Mh * MSs * lnL * T_H / v) / 1e3 > 40.0: Mmax = Mh; break
SEG["disc_heating_MW_8kpc"] = dict(rho_PBH_Msun_pc3=rho / MSs * (KPCs / 1e3) ** 3, sigma_kms=dh, M_where_sigma_exceeds_40=Mmax)
P(f"  disc heating at 8 kpc (MW-like, rho_PBH {rho / MSs * (KPCs/1e3)**3:.3g} Msun/pc^3): sigma after t_H " + ", ".join(f"{k} {v:.3g}" for k, v in dh.items()) + f" km/s; exceeds 40 km/s at M >= {Mmax:.2g}")
RES["segregation"] = SEG

# ------------------------------------------------------------------ millilensing / granularity (order of magnitude; a prediction, not graded)
ML = {}
for f in A0:
    a0 = A0[f]; Fx = RES["footings"][f]["U"]["F_SE2"]["X-COP"]; c = cand(Fx, "U", a0); rows = []
    for p in BATT[f]["X"]:
        ft = p["feat"]; gN = ft["x"] * a0; gp = gN * 10 ** GB["delta"](c, ft, a0) * GB["glaw"](gN, a0) / gN
        Mb = ft["Mb"]; Mp = Fx * Mb; Meff = gp * ft["r"] ** 2 / G / MS
        rows.append(dict(r_kpc=ft["r"] / KPCs, M_PBH=Mp, M_eff=Meff, share=Mp / Meff))
    sh = float(np.median([r_["share"] for r_ in rows])); Mp300 = float(np.median([r_["M_PBH"] for r_ in rows]))
    Deff = 1e6 * KPCs; tab = {}
    for Mh in MGRID:
        thE = math.sqrt(4 * Gs * Mh * MSs / (Cs ** 2 * Deff)) * 206265e6   # micro-arcsec
        tab[f"{Mh:.0e}"] = dict(N_per_cluster=Mp300 / Mh, theta_E_uas=thE, astrometric_jitter_uas=thE * math.sqrt(sh))
    ML[f] = dict(points=rows, kappa_share_median=sh, M_PBH_median=Mp300, per_mass=tab)
    P(f"[{f}] MILLILENSING: X-COP points r {np.median([r_['r_kpc'] for r_ in rows]):.0f} kpc (median), M_PBH {Mp300:.2e} Msun, PBH share of the law's lensing mass {sh:.2f}")
    for Mh, t in tab.items(): P(f"[{f}]   M {Mh}: N {t['N_per_cluster']:.2g} per cluster, theta_E {t['theta_E_uas']:.3g} uas, astrometric jitter ~{t['astrometric_jitter_uas']:.3g} uas")
RES["millilensing"] = ML
P("kappa = 1/2 FITTED; not theory closed. PBH mass is a component that must be paid for.")
dump(RES)
