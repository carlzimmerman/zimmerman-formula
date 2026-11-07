#!/usr/bin/env python3
"""EN1 (FROZEN_CRITERIA.md eae8892550): shock-entropy field sigma (gas adiabat, cooling off, shocks only) in the
khronon sector; rho_x inside the AQUAL source, b = 1 + M_x(<r)/M_b(<r). Variants V-frac-L, V-frac-S, V-dens-L, one
constant each, fixed on X-COP mean f = KD1's Xcop_f_need. Graded on GB1 G1-G8 (read-only) and the f table.
    python3 en1.py            -> en1.json / en1.out
    python3 en1.py --mutate   -> en1_MUTATE.json / .out   (sigma -> present kT; must FAIL)
kappa = 1/2 FITTED; footings never pooled; not theory closed.  1 thread."""
import os, sys, json, math, glob
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.optimize import brentq
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, "..")); REPO = os.path.dirname(CL)
MUT = "--mutate" in sys.argv; TAG = "en1_MUTATE" if MUT else "en1"; OUT = []
PROXY = "T" if MUT else "K"
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
KD1 = json.load(open(os.path.join(CL, "KD1_unpinned_kq_dust", "kd1.json")))
A0, G, MS, PC, KPC = GB["A0"], GB["G"], GB["MS"], GB["PC"], GB["KPC"]
DATA = os.path.join(REPO, "real_research", "data"); XT = os.path.join(REPO, "_external_data", "xcop_thermo_2026_11_02")
MSUN_G, KPC_CM, MP_G, MU_E = 1.989e33, 3.0857e21, 1.6726e-24, 1.155
def ne_of(rho_msun_kpc3): return rho_msun_kpc3 * MSUN_G / KPC_CM ** 3 / (MU_E * MP_G)     # cm^-3
RES = dict(tag=TAG, criteria="eae8892550", proxy=PROXY, note="kappa = 1/2 FITTED; not theory closed", KA={}, footings={})
P(f"EN1 {'MUTATE (sigma -> present kT)' if MUT else 'MAIN (sigma = shock adiabat K)'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

def lint(x, xp, yp):  # log-log interpolation, held at the ends
    return float(np.exp(np.interp(math.log(x), np.log(xp), np.log(yp))))

# ------------------------------------------------------------------ X-COP profiles (proxy sources, read-only)
XPROF = {}
def xprof(name, sz=False):
    key = (name, sz)
    if key in XPROF: return XPROF[key]
    d = os.path.join(XT, name)
    with fits.open(os.path.join(d, f"{name}_temperature.fits")) as h:
        X = h["XRAY"].data.copy(); Z = h["XSZ"].data.copy(); R5 = float(h["XRAY"].header["R500"]); T5 = float(h["XRAY"].header["T500"])
    spf = [p for p in glob.glob(os.path.join(d, "spectral_results_*.fits")) if os.path.basename(p).lower() == f"spectral_results_{name.lower()}.fits"][0]
    with fits.open(spf) as h: Sp = h[1].data.copy()
    assert len(Sp) == len(X), name
    x = np.asarray(X["RW_X"], float); kT = np.asarray(Sp["KT"], float); o = np.argsort(x); x, kT = x[o], kT[o]
    if sz:
        xz = np.asarray(Z["RW_SZ"], float); kz = np.asarray(Z["T_SZ"], float) * T5; m = xz > x[-1]
        x = np.concatenate([x, xz[m]]); kT = np.concatenate([kT, kz[m]])
    with fits.open(os.path.join(DATA, "xcop", name, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg5 = h[1].header["R500"]
    with fits.open(os.path.join(DATA, "xcop", name, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    gr = np.asarray(gas["RADIUS"], float) * rg5; gM = np.asarray(gas["MGAS"], float)
    ok = np.isfinite(gM) & (gM > 0); gr, gM = gr[ok], gM[ok]
    slope = np.gradient(np.log(gM), np.log(gr)); rho = slope * gM / (4 * math.pi * gr ** 3)      # Msun/kpc^3
    sr = np.asarray(st["RADIUS"], float); sM = np.asarray(st["MSTAR"], float); oks = np.isfinite(sM) & (sM > 0); sr, sM = sr[oks], sM[oks]
    XPROF[key] = dict(R5=R5, x=x, kT=kT, gr=gr, gM=gM, rho=rho, sr=sr, sM=sM)
    return XPROF[key]
def x_sigma(q, r, proxy):
    T = lint(r / q["R5"], q["x"], q["kT"])
    if proxy == "T": return T
    rho = lint(r, q["gr"], np.maximum(q["rho"], 1e-300)); return T * ne_of(rho) ** (-2.0 / 3.0)
def x_Mb(q, r):
    ms = lint(r, q["sr"], q["sM"]) if r >= q["sr"][0] else q["sM"][0] * (r / q["sr"][0]) ** 3
    return lint(r, q["gr"], q["gM"]) + ms
def xcop_point(name, r_kpc, proxy, sz=False):
    """returns (unit integrals): grid of sigma and dM_b and dV on [0, r] with the inner hold rule."""
    q = xprof(name, sz); rin = max(q["gr"][0], 1e-3); rr = np.geomspace(rin, r_kpc, 600)
    sig = np.array([x_sigma(q, t, proxy) for t in rr]); Mb = np.array([x_Mb(q, t) for t in rr])
    return dict(sig=sig, Mb=Mb, rr=rr, Mb_r=Mb[-1])
def ratio_grid(gp, variant, c):
    sig, Mb, rr = gp["sig"], gp["Mb"], gp["rr"]
    if variant == "V-dens-L":
        Mx = c * (sig[0] * 4 / 3 * math.pi * rr[0] ** 3 + np.trapz(sig * 4 * math.pi * rr ** 2, rr))
    else:
        g = sig * c if variant == "V-frac-L" else np.log1p(sig / c)
        Mx = g[0] * Mb[0] + np.trapz(g, Mb)
    return float(Mx / gp["Mb_r"])

# ------------------------------------------------------------------ groups, ellipticals (proxy sources)
def group_point(gp_raw, j, fst, proxy):
    s = math.log(gp_raw["g5"] / (gp_raw["pts"][0]["M_gas"])) / math.log(gp_raw["R5"] / gp_raw["R25"])
    R = (gp_raw["R25"], gp_raw["R5"]); Mg = (gp_raw["pts"][0]["M_gas"], gp_raw["g5"])
    if proxy == "T": K = (gp_raw["kT"], gp_raw["kT"])
    else: K = tuple(gp_raw["kT"] * ne_of(s * Mg[i] / (4 * math.pi * R[i] ** 3)) ** (-2 / 3) for i in (0, 1))
    k = math.log(K[1] / K[0]) / math.log(R[1] / R[0]); r = R[j]; Kr = K[j]; Mr = Mg[j] * (1 + fst)
    rr = np.geomspace(r * 1e-4, r, 800); sig = Kr * (rr / r) ** k; Mb = Mr * (rr / r) ** s
    return dict(sig=sig, Mb=Mb, rr=rr, Mb_r=Mr, K=Kr, s=s, k=k)
FUK = {}
for l in open(os.path.join(DATA, "cfg57_gas_sources", "fukazawa2006_table4.tsv")):
    if l.startswith("#") or l.startswith("name"): continue
    t = l.rstrip("\n").split("\t")
    def num(z):
        try: return float(z.split("+-")[0])
        except ValueError: return float("nan")
    FUK[t[0]] = dict(ne10=num(t[4]) * 1e-3, kTo=num(t[8]))
def ell_point(name, r_kpc, Mb_r, proxy):
    fk = FUK.get(name)
    if fk is None or not (np.isfinite(fk["ne10"]) and np.isfinite(fk["kTo"])): return None
    sg = fk["kTo"] if proxy == "T" else fk["kTo"] * fk["ne10"] ** (-2 / 3)
    rr = np.geomspace(r_kpc * 1e-4, r_kpc, 400); Mbg = Mb_r * np.interp(rr, [0, r_kpc], [0, 1])  # only Mb_r is used (uniform sigma)
    return dict(sig=np.full_like(rr, sg), Mb=Mbg, rr=rr, Mb_r=Mb_r, K=sg)
def ratio_uniform(gp, variant, c):
    sg = gp["sig"][0]; rr = gp["rr"]
    if variant == "V-dens-L": return float(c * sg * 4 / 3 * math.pi * rr[-1] ** 3 / gp["Mb_r"])
    return float(sg * c if variant == "V-frac-L" else math.log1p(sg / c))

# ------------------------------------------------------------------ battery (GB1, read-only) + EN features
_ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), EN=("zero",))
VARIANTS = ("V-frac-L", "V-frac-S", "V-dens-L")
BATT = {}; KA2 = []; KA3 = dict(ell_missing=[], grp_bad=0, xcop_bad=0)
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0); GRp = {0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}
    U = GB["udgs"](f, a0); Dd = GB["dsphs"](f, a0); K = GB["kids"](a0)
    st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    for p in S: p["feat"]["EN"] = ("zero",)
    assert len(X) == len(GB["XC"])
    for p, z in zip(X, GB["XC"]):
        gp = xcop_point(z["name"], z["r_kpc"], PROXY); p["feat"]["EN"] = ("grid", gp); p["name"] = z["name"]; p["r_kpc"] = z["r_kpc"]
        p["Kval"] = gp["sig"][-1]; KA3["xcop_bad"] += int(not (np.isfinite(gp["sig"]).all() and gp["sig"][-1] > 0))
        if f == "canonical":
            q = xprof(z["name"]); rin = q["gr"][0]; rr = np.geomspace(rin, z["r_kpc"], 2000)
            Mrec = q["gM"][0] + np.trapz([4 * math.pi * t ** 2 * lint(t, q["gr"], np.maximum(q["rho"], 1e-300)) for t in rr], rr)
            KA2.append(abs(Mrec / lint(z["r_kpc"], q["gr"], q["gM"]) - 1))
    for p in E:
        r_kpc = p["feat"]["r"] / KPC; gp = ell_point(p["name"], r_kpc, p["feat"]["Mb"], PROXY)
        if gp is None:
            p["feat"]["EN"] = None
            if f == "canonical" and p["name"] not in KA3["ell_missing"]: KA3["ell_missing"].append(p["name"])
        else: p["feat"]["EN"] = ("unif", gp); p["Kval"] = gp["K"]
    for fst in (0, 1):
        for gpr, graw in zip(GRp[fst], GB["GR"]):
            for j, p in enumerate(gpr["pts"]):
                gp = group_point(graw, j, fst, PROXY); p["feat"]["EN"] = ("grid", gp); p["Kval"] = gp["K"]
                if not (np.isfinite(gp["K"]) and gp["K"] > 0 and gp["s"] + gp["k"] > 0 and 3 + gp["k"] > 0): KA3["grp_bad"] += 1
    for p in U: p["feat"]["EN"] = None
    for c_ in Dd.values():
        for p in c_: p["feat"]["EN"] = None
    for ft in K[0] + K[1]: ft["EN"] = None
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=Dd, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - GB["KA20"][f][k]) for k in cm)
    RES["KA"][f"KA1_means_{f}"] = dict(maxdiff=float(d1), ok=bool(d1 <= 1e-6))
    P(f"[{f}] KA1 L0 class means vs QX20 KA dict: max|d| {d1:.1e} -> {'PASS' if d1 <= 1e-6 else 'FAIL'}")
RES["KA"]["KA2_mgas_reconstruction"] = dict(maxrel=float(max(KA2)), ok=bool(max(KA2) <= 1e-2))
P(f"KA2 X-COP M_gas from the derived density: max rel |d| {max(KA2):.2e} (line 1e-2) -> {'PASS' if max(KA2) <= 1e-2 else 'FAIL'}")
ka3ok = KA3["ell_missing"] == ["NGC6482"] and KA3["grp_bad"] == 0 and KA3["xcop_bad"] == 0
RES["KA"]["KA3_proxies"] = dict(KA3, ok=bool(ka3ok))
P(f"KA3 proxies: ellipticals without a proxy {KA3['ell_missing']} (expected ['NGC6482']); groups bad {KA3['grp_bad']}; X-COP bad {KA3['xcop_bad']} -> {'PASS' if ka3ok else 'FAIL'}")

def ratio(ft, variant, c):
    en = ft.get("EN", "absent")
    if en is None: raise GB["Missing"]("sigma_shock")
    if en == "absent": raise RuntimeError("feature without EN tag")
    if en[0] == "zero": return 0.0
    if en[0] == "unif": return ratio_uniform(en[1], variant, c)
    return ratio_grid(en[1], variant, c)
def EN(variant, c):
    def cand(ft):
        if c == 0: return dict(b=1.0, F=1.0, T=0.0)
        return dict(b=1.0 + ratio(ft, variant, c), F=1.0, T=0.0)
    return cand
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
def grade(cand, f):
    a0 = A0[f]; B = BATT[f]; return {g: GB["run_gate"](fn, cand, B, a0, []) for g, fn, _ in GB["GATES"]}

# ------------------------------------------------------------------ KA1 (constant 0 = GB1 L0, every row)
for f in A0:
    row0 = grade(EN("V-frac-L", 0), f); dmax = 0.0; okk = True
    for g in row0:
        a, b = flat(row0[g]["num"]), flat(GBJ["cands"]["L0"][f][g]["num"])
        okk &= (a.keys() == b.keys()) and row0[g]["status"] == GBJ["cands"]["L0"][f][g]["status"]
        for k in a:
            if isinstance(a[k], (int, float)) and not isinstance(a[k], bool) and k in b: dmax = max(dmax, abs(a[k] - b[k]))
    RES["KA"][f"KA1_rows_{f}"] = dict(maxdiff=float(dmax), ok=bool(okk and dmax <= 1e-12))
    P(f"[{f}] KA1 constant 0 vs gb1.json L0 on G1-G8: max|d| {dmax:.1e}, statuses equal {okk} -> {'PASS' if okk and dmax <= 1e-12 else 'FAIL'}")
KA_OK = all(v["ok"] for v in RES["KA"].values()); RES["KA_all"] = bool(KA_OK)
if not KA_OK:
    P("KA FAIL: stop; nothing graded.")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

# ------------------------------------------------------------------ fix the constant on X-COP, grade
def mean_ratio(pts, variant, c):
    v = [ratio(p["feat"], variant, c) for p in pts]; return float(np.mean(v))
def fix_const(f, variant, Xpts=None):
    X = Xpts if Xpts is not None else BATT[f]["X"]; fneed = KD1["footings"][f]["uniform_f_diag"]["Xcop_f_need"]
    if variant in ("V-frac-L", "V-dens-L"): return fneed / mean_ratio(X, variant, 1.0), fneed
    return math.exp(brentq(lambda ls: mean_ratio(X, variant, math.exp(ls)) - fneed, -30, 30, xtol=1e-14)), fneed
# reported diagnostic (post-freeze addition, reporting only): per-point uniform f need vs the proxy, within hosts
def f_need_pt(p, a0):
    g = lambda lf: p["D"] - GB["delta"](lambda ft: dict(b=1 + 10 ** lf, F=1.0, T=0.0), p["feat"], a0)
    try: return 10 ** brentq(g, -4, 4)
    except ValueError: return float("nan")
RES["within_host_need_vs_proxy"] = {}
for f, a0 in A0.items():
    B = BATT[f]; rows = []
    for x in GB["NS"]["XS"] if "NS" in GB else (0.1, 0.2, 0.3, 0.5, 0.7):
        pts = [p for p in B["X"] if abs(p["r_kpc"] / xprof(p["name"])["R5"] - x) < 1e-6]
        rows.append(dict(cls="X-COP", x=x, f_need_med=float(np.median([f_need_pt(p, a0) for p in pts])), proxy_med=float(np.median([p["Kval"] for p in pts]))))
    for j, lab in ((0, "R2500"), (1, "R500")):
        pts = [g["pts"][j] for g in B["GR"][0]]
        rows.append(dict(cls="groups f*0", x=lab, f_need_med=float(np.median([f_need_pt(p, a0) for p in pts])), proxy_med=float(np.median([p["Kval"] for p in pts]))))
    RES["within_host_need_vs_proxy"][f] = rows
    P(f"[{f}] reported: within-host uniform f need vs proxy {PROXY} (medians): " + "; ".join(f"{r['cls']} {r['x']}: need {r['f_need_med']:.2f}, {PROXY} {r['proxy_med']:.3g}" for r in rows))
TABLE = {}
for variant in VARIANTS:
    RES[variant] = {}
    for f, a0 in A0.items():
        B = BATT[f]; c, fneed = fix_const(f, variant); cand = EN(variant, c); row = grade(cand, f)
        diag = KD1["footings"][f]["uniform_f_diag"]
        fp = dict(SPARC=mean_ratio(B["S"], variant, c), Xcop=mean_ratio(B["X"], variant, c),
                  groups_fst0=mean_ratio([p for g in B["GR"][0] for p in g["pts"]], variant, c),
                  groups_fst1=mean_ratio([p for g in B["GR"][1] for p in g["pts"]], variant, c),
                  ell_6=mean_ratio([p for p in B["E"] if p["feat"]["EN"] is not None], variant, c))
        Xper = [dict(name=p["name"], x=round(p["r_kpc"] / xprof(p["name"])["R5"], 3), K=p["Kval"], f=ratio(p["feat"], variant, c),
                     D=p["D"], res=p["D"] - GB["delta"](cand, p["feat"], a0)) for p in B["X"]]
        # reported: ellipticals on the six with a proxy; with QX26 IMF
        E6 = [p for p in B["E"] if p["feat"]["EN"] is not None]
        e6 = float(np.mean([p["D"] - GB["delta"](cand, p["feat"], a0) for p in E6]))
        imfc = lambda ft: dict(b=GB["b_imf"](ft) + ratio(ft, variant, c), F=1.0, T=0.0)
        e6i = float(np.mean([p["D"] - GB["delta"](imfc, p["feat"], a0) for p in E6]))
        e6_l0 = float(np.mean([p["D"] for p in E6]))
        # reported: Coma UDG sigma needed at the frozen constant
        un = diag["udg_f_need"]; Kx = [p["Kval"] for p in B["X"]]
        if variant == "V-frac-L": sig_need = un / c
        elif variant == "V-frac-S": sig_need = c * math.expm1(un)
        else: sig_need = float(np.median([un * (u["feat"]["Mb"] / 2) / (c * 4 / 3 * math.pi * (u["feat"]["r"] / KPC) ** 3) for u in B["U"]]))
        ne_need = (8.6 / sig_need) ** 1.5 if PROXY == "K" else None
        # reported: SS ambient bound for V-dens
        AU_KPC = 1.495978707e11 / KPC
        ss_sig_max = (1e-10 / (c * 4 / 3 * math.pi * AU_KPC ** 3)) if variant == "V-dens-L" else None
        FO = dict(const=c, const_name={"V-frac-L": "1/sigma_* (per keV cm^2)", "V-frac-S": "sigma_* (keV cm^2)", "V-dens-L": "lambda (Msun/kpc^3 per keV cm^2)"}[variant],
                  Xcop_f_target=fneed, f_pred=fp, f_need=diag, rows=row, xcop_points=Xper, ell6_mean_res=e6, ell6_mean_res_imf=e6i, ell6_L0=e6_l0,
                  udg_sigma_need=sig_need, udg_ne_need_cm3_at_8p6keV=ne_need, Xcop_K_range=[float(min(Kx)), float(max(Kx))], ss_vdens_sigma_max_1em10Msun_in_1AU=ss_sig_max)
        if True:   # reported: X-COP with T_SZ beyond the X-ray range (constant re-fixed by the same rule)
            Xsz = [dict(D=p["D"], feat=dict(p["feat"], EN=("grid", xcop_point(p["name"], p["r_kpc"], PROXY, sz=True)))) for p in B["X"]]
            csz, _ = fix_const(f, variant, Xsz); rs = np.array([p["D"] - GB["delta"](EN(variant, csz), p["feat"], a0) for p in Xsz])
            FO["xcop_sz_reading"] = dict(const=csz, mean=float(rs.mean()), rms=float(np.sqrt((rs ** 2).mean())))
        RES[variant][f] = FO
        P(f"\n[{f}] {variant}: constant {FO['const_name']} = {c:.6g} (X-COP mean f -> {fneed:.4f}; check {fp['Xcop']:.4f})")
        for g, r in row.items(): P(f"[{f}] {variant} {g:17s} {r['status']:10s} {GB['short'](g, r)}")
        P(f"[{f}] {variant} f pred / need: SPARC {fp['SPARC']:.3f} / <= {diag['SPARC_f_max']:.3f}; X-COP {fp['Xcop']:.3f} / {diag['Xcop_f_need']:.3f}; "
          f"groups f*0 {fp['groups_fst0']:.3f} / {diag['groups_fst0_f_need']:.3f}, f*1 {fp['groups_fst1']:.3f} / {diag['groups_fst1_f_need']:.3f}; "
          f"ellipticals (6) {fp['ell_6']:.3f} / {diag['ell_f_need']:.3f}; UDG NV / {diag['udg_f_need']:.1f}; dSph NV / {diag['dsph_bright M31_f_need']:.2f}, {diag['dsph_MW classical_f_need']:.2f}")
        P(f"[{f}] {variant} X-COP per point (x, K, f, residual): " + "; ".join(f"{q['name']} {q['x']} K{q['K']:.0f} f{q['f']:.2f} {q['res']:+.3f}" for q in Xper))
        P(f"[{f}] {variant} reported: ellipticals (6 with proxy) mean residual {e6:+.4f} (L0 {e6_l0:+.4f}; with QX26 IMF {e6i:+.4f}; line 0.15)")
        P(f"[{f}] {variant} reported: Coma UDGs would need sigma {sig_need:.4g} keV cm^2" + (f" (at kT 8.6 keV: n_e <= {ne_need:.3g} cm^-3)" if ne_need else "") +
          f"; X-COP graded K range {min(Kx):.4g}-{max(Kx):.4g}")
        P(f"[{f}] {variant} reported: X-COP with T_SZ beyond the X-ray range: mean {FO['xcop_sz_reading']['mean']:+.4f} rms {FO['xcop_sz_reading']['rms']:.4f}")
        if ss_sig_max is not None: P(f"[{f}] {variant} reported: SS ambient sigma that puts 1e-10 Msun inside 1 AU: {ss_sig_max:.3g} keV cm^2")
    sts = {f: {g: RES[variant][f]["rows"][g]["status"] for g in RES[variant][f]["rows"]} for f in A0}
    fails = sorted({g.split()[0] for f in A0 for g, s in sts[f].items() if s == "FAIL"}); nvs = sorted({g.split()[0] for f in A0 for g, s in sts[f].items() if s == "NO VERDICT"})
    lab = ("PASSES ALL STATIC GATES" if not fails and not nvs else (f"FAIL ({', '.join(fails)})" + (f"; NO VERDICT ({', '.join(nvs)})" if nvs else "")) if fails else f"NOT GRADABLE ({', '.join(nvs)})")
    ftab = all(sts[f][g] == "PASS" for f in A0 for g in ("G1 SPARC", "G2 X-COP", "G3 groups", "G4 ellipticals", "G5 Coma UDGs", "G6 dSph classes"))
    RES[variant]["label"] = lab; RES[variant]["passes_f_table"] = bool(ftab); RES[variant]["statuses"] = sts
    P(f"LABEL {variant}: {lab}; f table: {'PASS' if ftab else 'NOT PASSED'}; G9 carried FAIL (rho_x = 0 before shocks; QX15 baryons-only control)")
if MUT:
    MJ = None; RES["MUTATE_bites"] = {v: bool(any(s == "FAIL" for f in A0 for s in RES[v]["statuses"][f].values())) for v in VARIANTS}
    mp = os.path.join(HERE, "en1.json")
    if os.path.exists(mp):
        MJ = json.load(open(mp)); RES["separates"] = {v: sorted({f"{f}|{g}" for f in A0 for g, s in MJ[v]["statuses"][f].items() if s == "PASS" and RES[v]["statuses"][f][g] == "FAIL"}) for v in VARIANTS}
        RES["reverse_separates"] = {v: sorted({f"{f}|{g}" for f in A0 for g, s in MJ[v]["statuses"][f].items() if s == "FAIL" and RES[v]["statuses"][f][g] == "PASS"}) for v in VARIANTS}  # post-freeze reporting addition
    P(f"MUTATE bites (>= 1 FAIL): {RES['MUTATE_bites']}; separates (main PASS, MUTATE FAIL): {RES.get('separates', 'main json not found')}")
    P(f"reported (post-freeze addition): reverse (main FAIL, MUTATE PASS): {RES.get('reverse_separates', 'main json not found')}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
