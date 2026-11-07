#!/usr/bin/env python3
"""DX1 (FROZEN_CRITERIA.md 367d5b823a): perfect disc-only exclusion as an ORACLE BOUND, graded on GB1 G1-G8.
    python3 dx1.py            -> dx1.json / dx1.out
    python3 dx1.py --mutate   -> dx1_MUTATE.json / .out   (inverted oracle: must FAIL G1 on both footings)
Read-only use of GB1 (loaders, features, gate functions) and KD1 (f_cap, SPARC_f_max). Not a candidate; adopts nothing.
kappa = 1/2 FITTED; footings never pooled; not theory closed.  1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, ".."))
MUT = "--mutate" in sys.argv; TAG = "dx1_MUTATE" if MUT else "dx1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
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
A0 = GB["A0"]
RES = dict(tag=TAG, criteria="367d5b823a", note="ORACLE BOUND, not a candidate; kappa = 1/2 FITTED; not theory closed", KA={}, footings={})
P(f"DX1 {'MUTATE (inverted oracle)' if MUT else 'MAIN'}. ORACLE BOUND, not a candidate. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ battery copy with the oracle tag (D = disc set, H = hot set)
_ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), dx="D")             # the Sun sits in the MW disc
def tag(pts, t):
    for p in pts: p["feat"]["dx"] = t
BATT = {}
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0); GRp = {0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}
    U = GB["udgs"](f, a0); Dd = GB["dsphs"](f, a0); K = GB["kids"](a0)
    st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    tag(S, "D"); tag(E, "H"); tag(X, "H"); tag(U, "H")
    for fst in (0, 1):
        for g in GRp[fst]: tag(g["pts"], "H")
    for cls in Dd: tag(Dd[cls], "H")
    for ft in K[0]: ft["dx"] = "H"                                                      # early (red) lenses
    for ft in K[1]: ft["dx"] = "D"                                                      # late (blue) lenses
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=Dd, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - GB["KA20"][f][k]) for k in cm); um = float(np.mean([u["D"] for u in U])); d2 = abs(um - st["meanE"] / math.log(10))
    RES["KA"][f"KA1_{f}"] = dict(maxdiff=float(d1), udg_diff=float(d2), ok=bool(d1 <= 1e-6 and d2 <= 1e-9))
    P(f"[{f}] KA1 L0 class means max|d| {d1:.1e}, UDG |d| {d2:.1e} -> {'PASS' if RES['KA'][f'KA1_{f}']['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ bounds
def O(fon, imf, inverted=False, lg_disc=False):
    def c(ft):
        on = ft["dx"] == ("D" if inverted else "H")
        if lg_disc and ft.get("lg_field"): on = inverted
        b0 = GB["b_imf"](ft) if imf else 1.0
        return dict(b=b0 * (1.0 + (fon if on else 0.0)), F=1.0, T=0.0)
    return c
def grade(cand, f):
    a0 = A0[f]; B = BATT[f]; return {g: GB["run_gate"](fn, cand, B, a0, fills) for g, fn, fills in GB["GATES"]}
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

for f in A0:
    a0 = A0[f]; FO = {}
    diag = KDJ["footings"][f]["uniform_f_diag"]; fon = float(diag["capture_f"]); FO["f_on"] = fon; FO["kd1_need"] = diag
    # KA2 / KA3: f_on = 0 reproduces GB1 L0 and L1
    ok2, d2 = same(grade(O(0.0, False), f), GBJ["cands"]["L0"][f]); ok3, d3 = same(grade(O(0.0, True), f), GBJ["cands"]["L1"][f])
    RES["KA"][f"KA2_{f}"] = dict(ok=ok2, maxdiff=d2); RES["KA"][f"KA3_{f}"] = dict(ok=ok3, maxdiff=d3)
    P(f"[{f}] KA2 O1(f_on 0) = gb1 L0: max|d| {d2:.1e} -> {'PASS' if ok2 else 'FAIL'};  KA3 O2(f_on 0) = gb1 L1: max|d| {d3:.1e} -> {'PASS' if ok3 else 'FAIL'}")
    # KA4: KD1's SPARC_f_max by the same bisection
    U_ = lambda fr: (lambda ft: dict(b=1.0 + fr, F=1.0, T=0.0)); lo, hi = 0.0, 10.0
    for _ in range(60):
        m_ = 0.5 * (lo + hi); lo, hi = (m_, hi) if GB["g_sparc"](U_(m_), BATT[f], a0)[0] else (lo, m_)
    d4 = abs(lo - diag["SPARC_f_max"]); RES["KA"][f"KA4_{f}"] = dict(ok=bool(d4 <= 1e-9), value=lo, diff=d4)
    P(f"[{f}] KA4 SPARC_f_max {lo:.6f} vs KD1 {diag['SPARC_f_max']:.6f}: |d| {d4:.1e} -> {'PASS' if d4 <= 1e-9 else 'FAIL'}")
    RES["footings"][f] = FO

ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all"] = bool(ka_ok)
if not ka_ok:
    P("KA FAIL: stop; nothing graded.")
else:
    for f in A0:
        FO = RES["footings"][f]; fon = FO["f_on"]
        P(f"[{f}] f_on = KD1 capture {fon:.5f}; KD1 needs: SPARC <= {FO['kd1_need']['SPARC_f_max']:.3f}, X-COP {FO['kd1_need']['Xcop_f_need']:.2f}, "
          f"groups {FO['kd1_need']['groups_fst0_f_need']:.2f}/{FO['kd1_need']['groups_fst1_f_need']:.2f}, E {FO['kd1_need']['ell_f_need']:.2f}, "
          f"bright M31 {FO['kd1_need']['dsph_bright M31_f_need']:.2f}, MW classical {FO['kd1_need']['dsph_MW classical_f_need']:.2f}, UDG {FO['kd1_need']['udg_f_need']:.1f}")
        bounds = {"MUTATE_inverted": O(fon, False, inverted=True)} if MUT else {"O1": O(fon, False), "O2": O(fon, True)}
        FO["rows"] = {}
        for bn, c in bounds.items():
            row = grade(c, f); FO["rows"][bn] = row
            for g, r in row.items():
                txt = GB["short"](g, r) if r["num"] is not None else f"missing {r['missing']}; bracket {r['bracket']['reading'] if r['bracket'] else '-'}"
                if r["num"] is None and r["bracket"]:
                    nums = [GB["short"](g, dict(o, status='PASS' if o['ok'] else 'FAIL')) for o in r["bracket"]["runs"] if o.get("num") is not None]
                    txt += " | " + " ; ".join(nums)
                P(f"[{f}] {bn} {g:17s} {r['status']:10s} {txt}")
        if not MUT:   # reported: LG field moved to the disc set (O1 only)
            for p in BATT[f]["D"]["LG field"]: p["feat"]["lg_field"] = True
            r6 = GB["run_gate"](GB["g_dsph"], O(fon, False, lg_disc=True), BATT[f], A0[f], []); FO["reported_O1_LGfield_in_D"] = r6
            P(f"[{f}] reported O1 with LG field in D: G6 {r6['status']} {GB['short']('G6 dSph classes', r6)}")
            for p in BATT[f]["D"]["LG field"]: p["feat"].pop("lg_field")
    if MUT:
        bites = all(RES["footings"][f]["rows"]["MUTATE_inverted"]["G1 SPARC"]["status"] == "FAIL" for f in A0)
        RES["MUTATE_bites"] = bool(bites); P(f"MUTATE inverted oracle: {'G1 FAILS both footings -> BITES' if bites else 'NO BITE (bound has no power)'}")
    else:
        labs = {}
        for bn in ("O1", "O2"):
            fails = sorted({g.split()[0] for f in A0 for g, r in RES["footings"][f]["rows"][bn].items() if r["status"] == "FAIL"})
            nvs = sorted({g.split()[0] for f in A0 for g, r in RES["footings"][f]["rows"][bn].items() if r["status"] == "NO VERDICT"})
            labs[bn] = ("BOUND FAILS (" + ", ".join(fails) + ")" + (f"; NO VERDICT ({', '.join(nvs)})" if nvs else "")) if fails else \
                       (f"BOUND NOT GRADABLE ({', '.join(nvs)})" if nvs else "BOUND PASSES ALL STATIC GATES")
            P(f"LABEL {bn}: {labs[bn]}")
        RES["labels"] = labs
P("G9 CMB lensing + growth: CARRIED from KD1 at mu_K* (PASS, chi2 8.56), not re-run.")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
