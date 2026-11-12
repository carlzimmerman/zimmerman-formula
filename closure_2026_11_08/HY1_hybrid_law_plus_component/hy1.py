#!/usr/bin/env python3
"""HY1 (FROZEN_CRITERIA.md 2fbb41123a): the a0 law with kappa free plus the universal cold component at F1A's f,
held where the record puts it (KD1 model P at mu*: a central point mass f_cap R M_b,sys).
    python3 hy1.py sparc     -> parts/sparc.json   (+ parts/sparc_M3.json)      C1, KA2, M1 (kappa 0), M3
    python3 hy1.py battery   -> parts/battery.json (+ parts/battery_M3.json)    C2, C3a, C5, KA1/KA3/KA5/KA6/KA7
    python3 hy1.py kids      -> parts/kids.json                                  C4, KA4, C4 power
    python3 hy1_grade.py     -> hy1.json / hy1.out, hy1_MUTATE.json / hy1_MUTATE.out
Read-only use of QX8 (+ parts), GB1, QX5 (via GB1), KD1/F1A/UA1/KX1/QX8/GB1 JSONs, KX1's prefix (QX10 iter_2, CW6, CFG4).
Each column in its own process, one thread. kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, time, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import warnings; warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
KGRID = [0.0, 0.001, 0.003, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.13, 0.17, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
         0.60, 0.70, 0.85, 1.00, 1.25, 1.50, 2.00]
FCAP = 0.76
F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")))
RF = {f: float(F1A[f]["R_B2"]) for f in FOOTS}                       # 5.4095831638392 / 5.41226812314077
KD1J = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
RKD = {f: float(KD1J["footings"][f]["uniform_f_diag"]["capture_f"]) for f in FOOTS}   # KD1's captured ratio (QX15 R)
CAP = {f: FCAP * RF[f] for f in FOOTS}                                 # f_cap R at F1A's R
RES = {}; WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # bytes on macOS -> GB
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)
def bisect(fun, lo, hi, n=30):
    """edge between lo (fun(lo) = s0) and hi (fun(hi) != s0), n halvings; returns the midpoint."""
    s0 = fun(lo)
    for _ in range(n):
        m = 0.5 * (lo + hi)
        if fun(m) == s0: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
def edges(kg, st, fun):
    out = []
    for a, b, sa, sb in zip(kg[:-1], kg[1:], st[:-1], st[1:]):
        if sa != sb: out.append(dict(between=[a, b], from_=sa, to=sb, edge=bisect(fun, a, b)))
    return out


# ================================================================== C1 SPARC (QX8 per-galaxy rule)
def run_sparc():
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field"))
    a = sys.argv; sys.argv = [a[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a
    GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GK = 4.30091e-6; ACC = 1e6 / Q8.KPC_S                                  # kpc (km/s)^2/Msun ; (km/s)^2/kpc -> m/s^2
    lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
    PRE = {}
    for f in FOOTS:
        rows = []
        for i, q in enumerate(GALS):
            z = np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False); Tn = z["T"]
            Tf = np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])          # (npts, nups)
            R = q["R"]; U = Q8.UPS[None, :]
            VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + U * q["Vdisk"][:, None] ** 2 + 1.4 * U * q["Vbul"][:, None] ** 2
            Mr = np.maximum.accumulate(np.clip(VB2 * R[:, None] / GK, 0, None), axis=0)
            m = q["meta"]; Mtot = np.maximum(Mr[-1], Q8.UPS * m["L36"] * 1e9 + 1.33 * m["MHI"] * 1e9)    # (nups,)
            gd1 = GK * Mtot[None, :] / R[:, None] ** 2 * ACC                                     # per unit ratio, m/s^2
            rows.append(dict(T=Tf, gd1=gd1))
        PRE[f] = rows
    def ev(f, kap, ratio, tmode="T", shape="point"):
        a0 = Q8.FOOT[f] * kap / 0.5; out = []
        for q, pr in zip(GALS, PRE[f]):
            gN = q["GB"] + ratio * pr["gd1"] if shape == "point" else q["GB"] * (1.0 + ratio)
            lg = np.log10(np.maximum(glaw(gN, a0), 1e-300)) + (pr["T"] if tmode == "T" else 0.0)
            out.append(Q8.fit_one(q, lg))
        st = Q8.pooled(out); st["line"] = Q8.line(st); return st
    for f in FOOTS:
        R = {}; RES[f] = R
        ref = Q8J["footings"][f]; rx = ref.get("exact", ref.get("st_ex", {}))
        k0 = ev(f, 0.5, 0.0); d = abs(k0["rms"] - rx["rms"]); du = abs(k0["U_median"] - rx["U_median"])
        R["KA2"] = dict(rms=k0["rms"], U_median=k0["U_median"], qx8_rms=rx["rms"], qx8_U=rx["U_median"], d_rms=d, d_U=du, pass_=bool(d <= 1e-6 and du <= 1e-6))
        P(f"[{f}] KA2 SPARC law-only (kappa 1/2, f 0): rms {k0['rms']:.8f} U {k0['U_median']:.2f} vs QX8 {rx['rms']:.8f} @ {rx['U_median']:.2f}: |d| {d:.1e}/{du:.1e} -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}")
        if not R["KA2"]["pass_"]: continue
        grid = []
        for kap in KGRID:
            sT = ev(f, kap, CAP[f], "T"); s0 = ev(f, kap, CAP[f], "0"); n0 = ev(f, kap, 0.0, "T")
            st = ("PASS" if sT["line"] else "FAIL") if sT["line"] == s0["line"] else "NOT EVALUABLE"
            # eps_max: largest retained fraction passing the line (T carried)
            if not n0["line"]: eps = None
            elif ev(f, kap, CAP[f], "T")["line"]: eps = 1.0
            else:
                lo, hi = 0.0, 1.0
                for _ in range(30):
                    m_ = 0.5 * (lo + hi)
                    if ev(f, kap, m_ * CAP[f], "T")["line"]: lo = m_
                    else: hi = m_
                eps = lo
            ub = ev(f, kap, CAP[f], "T", "uniform")
            row = dict(kappa=kap, status=st, rms=sT["rms"], U_median=sT["U_median"], rms_T0=s0["rms"], U_T0=s0["U_median"],
                       line_T=sT["line"], line_T0=s0["line"], law_only=dict(rms=n0["rms"], U=n0["U_median"], line=n0["line"]),
                       eps_max=eps, f_ret=None if eps is None else eps * CAP[f], uniform_b=dict(rms=ub["rms"], U=ub["U_median"], line=ub["line"]))
            grid.append(row)
            P(f"[{f}] C1 kappa {kap:5.3f}: {st:13s} rms {sT['rms']:.4f} U {sT['U_median']:.2f} (T=0 {s0['rms']:.4f} @ {s0['U_median']:.2f}) | law only {n0['rms']:.4f} @ {n0['U_median']:.2f} {'P' if n0['line'] else 'F'}"
              f" | eps_max {('none' if eps is None else f'{eps:.4f}')} | uniform-b {ub['rms']:.4f} @ {ub['U_median']:.2f} {'P' if ub['line'] else 'F'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
            RES[f]["grid"] = grid; dump("sparc_partial.json", RES)
        R["grid"] = grid
        R["edges"] = edges(KGRID, [r["line_T"] for r in grid], lambda k: ev(f, k, CAP[f], "T")["line"])
        R["edges_law_only"] = edges(KGRID, [r["law_only"]["line"] for r in grid], lambda k: ev(f, k, 0.0, "T")["line"])
        R["edges_uniform_b"] = edges(KGRID, [r["uniform_b"]["line"] for r in grid], lambda k: ev(f, k, CAP[f], "T", "uniform")["line"])
        P(f"[{f}] C1 refined edges (T carried): {R['edges']}; law-only: {R['edges_law_only']}; uniform-b: {R['edges_uniform_b']}")
    dump("sparc.json", RES)
    # M3: f -> 2R, rms move at every kappa (separate output)
    M3 = {}
    for f in FOOTS:
        if not RES[f]["KA2"]["pass_"]: continue
        M3[f] = []
        for r in RES[f]["grid"]:
            s2 = ev(f, r["kappa"], 2 * CAP[f], "T")
            M3[f].append(dict(kappa=r["kappa"], rms_R=r["rms"], rms_2R=s2["rms"], dS=s2["rms"] - r["rms"], U_2R=s2["U_median"], line_2R=s2["line"]))
        P(f"[{f}] M3 C1 dS(kappa): " + ", ".join(f"{x['kappa']:g}:{x['dS']:+.3f}" for x in M3[f]))
    M3["peak_rss_GB"] = rss(); M3["seconds"] = time.time() - T0
    dump("sparc_M3.json", M3)
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("sparc.json", RES)
    if os.path.exists(os.path.join(PARTS, "sparc_partial.json")): os.remove(os.path.join(PARTS, "sparc_partial.json"))
    P(f"sparc done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")


# ================================================================== GB1 battery: C2 X-COP, C3a groups, C5 Solar System
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns

def run_battery():
    from astropy.io import fits
    from scipy.optimize import brentq
    GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    GBJ = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
    UA1J = json.load(open(os.path.join(CL7, "UA1_fragile_rows", "ua1.json")))
    _ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), nodust=True)          # KD1 P4: no dust at the Sun
    G, MS, KPC, XC = GB["G"], GB["MS"], GB["KPC"], GB["XC"]; nu1 = GB["nu_minus_1"]; need = GB["need"]
    R500 = {}
    for name in sorted({z["name"] for z in XC}):
        with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h: R500[name] = float(h[1].header["R500"])
    EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]
    def xeval(a0h, kap, ratio, shape="point"):
        a0 = a0h * kap / 0.5; d = []; xr = []
        for z in XC:
            rm = z["r_kpc"] * KPC; Ml = z["Mb_last"][0]
            Mt = z["M_b"] + ratio * Ml if shape == "point" else z["M_b"] * (1.0 + ratio)
            Mp = glaw(G * Mt * MS / rm ** 2, a0) * rm ** 2 / G / MS
            d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500[z["name"]])
        d = np.array(d); xr = np.array(xr); bins = []
        for lo, hi in zip(EDG[:-1], EDG[1:]):
            m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None))
        mean, rmsv = float(d.mean()), float(np.sqrt((d ** 2).mean())); bok = all(abs(b["mean"]) <= 0.10 for b in bins if b["n"] >= 3)
        return dict(mean=mean, rms=rmsv, bins=bins, bins_ok=bool(bok), gate=bool(abs(mean) <= 0.05 and rmsv <= 0.10 and bok))
    def golden(fun, lo, hi, it=80):
        g = (math.sqrt(5) - 1) / 2; a, b = lo, hi; c, e = b - g * (b - a), a + g * (b - a); fc, fe = fun(c), fun(e)
        for _ in range(it):
            if fc < fe: b, e, fe = e, c, fc; c = b - g * (b - a); fc = fun(c)
            else: a, c, fc = c, e, fe; e = a + g * (b - a); fe = fun(e)
        return 0.5 * (a + b)
    def cand(a0h, kap, ratio, shape="point"):
        a0 = a0h * kap / 0.5
        def c(ft):
            if ft.get("nodust"):
                x = ft["x"]; Fk = (nu1(x * 0.5 / kap) / nu1(x)) if kap > 0 else 0.0
                return dict(b=1.0, F=Fk, T=0.0)
            gN = need(ft, "x") * a0h
            if shape == "point":
                Msys = (ft["r"] / need(ft, "rrM")) ** 2 * a0h / G / MS; gt = gN + G * ratio * Msys * MS / ft["r"] ** 2
            else: gt = gN * (1.0 + ratio)
            return dict(delta=math.log10(glaw(gt, a0) / glaw(gN, a0h)))
        return c
    def step(B, a0h, kap, ratio, fst):
        c = cand(a0h, kap, ratio); return float(np.mean([GB["delta"](c, p["feat"], a0h) for g in B["GR"][fst] for p in g["pts"]]))
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
    def maxd(a, b):
        A, Bb = flat(a), flat(b); m = 0.0; same = A.keys() == Bb.keys()
        for k in A:
            if isinstance(A[k], (int, float)) and not isinstance(A[k], bool) and k in Bb: m = max(m, abs(A[k] - Bb[k]))
            elif k in Bb and A[k] != Bb[k]: same = False
        return m, same
    M3 = {}
    for f in FOOTS:
        a0h = GB["A0"][f]; S, E, X = GB["build"](f, a0h)
        B = dict(f=f, S=S, E=E, X=X, GR={0: GB["groups_pts"](a0h, 0.0), 1: GB["groups_pts"](a0h, 1.0)})
        B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
        R = {}; RES[f] = R; ka = {}
        # KA1 F1A, KA7 KD1 G9a: read exactly
        ka["KA1"] = dict(R_B2=RF[f], chi2_cold_B2=F1A[f]["chi2_cold_B2"], pass_=True)
        g9 = KD1J["footings"][f]["G9a_shape"]["chi2_mu_inf"]; ka["KA7"] = dict(G9a_chi2=g9, pass_=True)
        # KA3 X-COP
        x0 = xeval(a0h, 0.5, 0.0); dX = abs(x0["mean"] - GB["KA20"][f]["X"])
        xk = xeval(a0h, 0.5, RKD[f]); kd = KD1J["footings"][f]["static"]
        dK = max(abs(xk["mean"] - kd["G2 X-COP"]["num"]["mean"]), abs(xk["rms"] - kd["G2 X-COP"]["num"]["rms"]))
        okS, nS = GB["g_sparc"](cand(a0h, 0.5, RKD[f]), B, a0h)
        dS = max(abs(nS["Z"] - kd["G1 SPARC"]["num"]["Z"]), abs(nS["rms"] - kd["G1 SPARC"]["num"]["rms"]))
        need_u = 10 ** brentq(lambda lf: xeval(a0h, 0.5, 10 ** lf, "uniform")["mean"], -4, 4)
        dN = abs(need_u - KD1J["footings"][f]["uniform_f_diag"]["Xcop_f_need"])
        ka["KA3"] = dict(law_mean=x0["mean"], d_law=dX, kd1_xcop=[xk["mean"], xk["rms"]], d_kd1_xcop=dK, kd1_sparc=[nS["Z"], nS["rms"]], d_kd1_sparc=dS,
                         uniform_need=need_u, d_need=dN, pass_=bool(dX <= 1e-6 and dK <= 1e-6 and dS <= 1e-6 and dN <= 1e-4))
        # KA5 groups, KA6 Solar System
        o5, n5 = GB["g_groups"](cand(a0h, 0.5, 0.0), B, a0h); m5, s5 = maxd(n5, GBJ["cands"]["L0"][f]["G3 groups"]["num"])
        st0 = [step(B, a0h, 0.5, 0.0, fs) for fs in (0, 1)]
        ka["KA5"] = dict(maxd=m5, same_keys=s5, step0=st0, pass_=bool(m5 == 0.0 and s5 and all(s == 0.0 for s in st0)))
        o6, n6 = GB["g_ss"](cand(a0h, 0.5, 0.0), B, a0h); m6, s6 = maxd(n6, GBJ["cands"]["L0"][f]["G8 Solar System"]["num"])
        ka["KA6"] = dict(maxd=m6, same_keys=s6, pass_=bool(m6 <= 1e-12 and s6))
        R["KA"] = ka
        for k, v in ka.items(): P(f"[{f}] {k}: {'PASS' if v['pass_'] else 'FAIL'}  " + ", ".join(f"{a}={b}" for a, b in v.items() if a != 'pass_'))
        if not all(v["pass_"] for v in ka.values()): continue
        lo95 = {fs: UA1J["footings"][f]["cells"]["groups"]["post"]["ci95"] for fs in (0, 1)}
        R["UA1_ci95"] = lo95[0]
        rowsX, rowsG, rowsS = [], [], []
        for kap in KGRID:
            xr_ = xeval(a0h, kap, CAP[f]); Fx = golden(lambda F: xeval(a0h, kap, F)["rms"], 0.0, 30.0); xf = xeval(a0h, kap, Fx)
            xu = xeval(a0h, kap, CAP[f], "uniform"); xl = xeval(a0h, kap, 0.0)
            rowsX.append(dict(kappa=kap, status="PASS" if xr_["gate"] else "FAIL", **xr_, F_X=Fx, at_F_X=dict(mean=xf["mean"], rms=xf["rms"], gate=xf["gate"], bins=[b["mean"] for b in xf["bins"]]),
                              uniform_b=dict(mean=xu["mean"], rms=xu["rms"], gate=xu["gate"]), law_only=dict(mean=xl["mean"], rms=xl["rms"], gate=xl["gate"])))
            ci = lo95[0]; s_ = [step(B, a0h, kap, CAP[f], fs) for fs in (0, 1)]; ok = all(ci[0] <= s <= ci[1] for s in s_)
            og, ng = GB["g_groups"](cand(a0h, kap, CAP[f]), B, a0h)
            rowsG.append(dict(kappa=kap, status="PASS" if ok else "FAIL", step_fst0=s_[0], step_fst1=s_[1], ci95=ci, strict_GB1=dict(pass_=bool(og), num=ng),
                              law_only_step=[step(B, a0h, kap, 0.0, fs) for fs in (0, 1)]))
            os_, ns_ = GB["g_ss"](cand(a0h, kap, CAP[f]), B, a0h)
            rowsS.append(dict(kappa=kap, status="PASS" if os_ else "FAIL", cassini_F=ns_["cassini_F"], cassini_use=ns_["cassini_use"], worst_planet_use=ns_["worst_planet_use"]))
            og1, ng1 = GB["g_sparc"](cand(a0h, kap, CAP[f]), B, a0h)
            rowsX[-1]["GB1_G1_reported"] = dict(pass_=bool(og1), Z=ng1["Z"], rms=ng1["rms"])
            P(f"[{f}] kappa {kap:5.3f}: C2 {rowsX[-1]['status']} mean {xr_['mean']:+.3f} rms {xr_['rms']:.3f} bins " + "/".join("-" if b["mean"] is None else f"{b['mean']:+.2f}" for b in xr_["bins"][:3])
              + f" F_X {Fx:.2f} (rms {xf['rms']:.3f}) | C3a {rowsG[-1]['status']} step {s_[0]:+.3f}/{s_[1]:+.3f} in [{ci[0]:+.3f},{ci[1]:+.3f}] strict {ng['fst0']['n_pass']}/{ng['fst1']['n_pass']}"
              f" | C5 {rowsS[-1]['status']} F_cas {ns_['cassini_F']:.3g} | GB1 G1 Z {ng1['Z']:+.3f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        R["C2"] = rowsX; R["C3a"] = rowsG; R["C5"] = rowsS
        R["C2_edges"] = edges(KGRID, [r["gate"] for r in rowsX], lambda k: xeval(a0h, k, CAP[f])["gate"])
        R["C3a_edges"] = edges(KGRID, [r["status"] for r in rowsG], lambda k: "PASS" if all(lo95[0][0] <= step(B, a0h, k, CAP[f], fs) <= lo95[0][1] for fs in (0, 1)) else "FAIL")
        R["C5_edges"] = edges(KGRID, [r["status"] for r in rowsS], lambda k: "PASS" if GB["g_ss"](cand(a0h, k, CAP[f]), B, a0h)[0] else "FAIL")
        P(f"[{f}] edges C2 {R['C2_edges']}; C3a {R['C3a_edges']}; C5 {R['C5_edges']}")
        # c_T and PPN, quoted and scaled (reported)
        R["C5_quoted"] = dict(cT_mass_bound_half={"canonical": 5.1e-32, "alt": 6.2e-32}[f], cT_bound_at_kappa_2_scaled=({"canonical": 5.1e-32, "alt": 6.2e-32}[f]) * (2.0 / 0.5) ** 2,
                              GW170817=3e-15, ppn_gamma_remainder_half=9.8e-14, ppn_beta_remainder_half=1.1e-12)
        dump("battery_partial.json", RES)
        # M3: X-COP rms move at 2R (separate output)
        M3[f] = [dict(kappa=r["kappa"], rms_R=r["rms"], rms_2R=xeval(a0h, r["kappa"], 2 * CAP[f])["rms"]) for r in rowsX]
        for x in M3[f]: x["dX"] = x["rms_2R"] - x["rms_R"]
        P(f"[{f}] M3 C2 dX(kappa): " + ", ".join(f"{x['kappa']:g}:{x['dX']:+.3f}" for x in M3[f]))
    M3["peak_rss_GB"] = rss(); dump("battery_M3.json", M3)
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("battery.json", RES)
    if os.path.exists(os.path.join(PARTS, "battery_partial.json")): os.remove(os.path.join(PARTS, "battery_partial.json"))
    P(f"battery done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")


# ================================================================== C4 KiDS (KX1 machinery)
def run_kids():
    KX = os.path.join(CL7, "KX1_kids_joint_budget", "kx1.py")
    src = open(KX).read(); cut = src.index("# ================================================================ run")
    NS = {"__file__": KX, "__name__": "kx1_lib"}; a = sys.argv; sys.argv = [KX]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "kx1_lib", "exec"), NS)
    sys.argv = a
    KXJ = json.load(open(os.path.join(CL7, "KX1_kids_joint_budget", "kx1.json")))
    BIN, A0K, ACC, G_SI, MS, KPC_M, hot_ratio, glaw_SI = (NS[k] for k in ("BIN", "A0K", "ACC", "G_SI", "MS", "KPC_M", "hot_ratio", "glaw_SI"))
    orig_model = NS["model"]
    def model(B, sel, foot, cell, mult, prof, dM):
        """cell None: KX1's law (kappa 1/2, no sector). cell ('HY', kappa, shape): law at a0(kappa) + dust (mult = f_cap R)."""
        if cell is None: return orig_model(B, sel, foot, None, 0.0, prof, dM)
        _, kap, shape = cell
        s = 10 ** dM; lm = B["lm"] + dM; r = B["r"][sel]; Mb = 10 ** lm
        gN = B["gbar"][sel] * s
        if prof is not None: gN = gN + G_SI * hot_ratio(prof, lm, r) * Mb * MS / (r * KPC_M) ** 2
        if shape == "point": gN = gN + G_SI * mult * Mb * MS / (r * KPC_M) ** 2
        else: gN = gN * (1.0 + mult)
        return glaw_SI(gN, A0K[foot] * ACC * kap / 0.5)
    NS["model"] = model
    budget = NS["budget"]
    def grade(foot, kap, mult, shape="point"):
        rows = []
        for b, B in enumerate(BIN):
            sel = B["win"]; L = budget(B, b, sel, foot, None, 0.0); H = budget(B, b, sel, foot, ("HY", kap, shape), mult)
            W = L["loga"] - H["loga"]; z = (W - L["loga"]) / H["sigma_tot"]
            rows.append(dict(bin=b + 1, lm=B["lm"], E=L["loga"], sig_law=L["sigma_tot"], W=W, sig_tot=H["sigma_tot"], z=z, terms=H["terms"]))
        nk = sum(1 for x in rows if abs(x["z"]) > 2)
        return dict(rows=rows, n_out=nk, status="FAIL" if nk >= 2 else "PASS")
    for f in FOOTS:
        R = {}; RES[f] = R
        g0 = grade(f, 0.5, 0.0); ref = KXJ["grade"][f]["C1"]["rows"]
        d = max(max(abs(x["E"] - r["E"]), abs(x["sig_law"] - r["sig_law"])) for x, r in zip(g0["rows"], ref))
        dW = max(abs(x["W"]) for x in g0["rows"])
        R["KA4"] = dict(maxd=d, max_W_at_law=dW, law_status=g0["status"], z_law=[x["z"] for x in g0["rows"]], pass_=bool(d <= 1e-9 and dW == 0.0))
        P(f"[{f}] KA4 KiDS law (kappa 1/2, f 0) vs KX1 E/sigma: max|d| {d:.1e}, max|W| {dW:.1e}; law two-sided status {g0['status']} (z " + ", ".join(f"{x['z']:+.2f}" for x in g0["rows"]) + f") -> {'PASS' if R['KA4']['pass_'] else 'FAIL'}")
        if not R["KA4"]["pass_"]: continue
        pw = grade(f, 0.5, CAP[f]); R["power_KD1_dust_at_half"] = dict(status=pw["status"], z=[x["z"] for x in pw["rows"]], W=[x["W"] for x in pw["rows"]])
        R["power"] = bool(g0["status"] == "PASS" and pw["status"] == "FAIL")
        P(f"[{f}] C4 power: law {g0['status']}, KD1 dust at kappa 1/2 {pw['status']} (z " + ", ".join(f"{x['z']:+.2f}" for x in pw["rows"]) + f") -> {'POWER' if R['power'] else 'NO POWER'}")
        grid = []
        for kap in KGRID:
            g = grade(f, kap, CAP[f]); u = grade(f, kap, CAP[f], "uniform"); l = grade(f, kap, 0.0)
            grid.append(dict(kappa=kap, status=g["status"], n_out=g["n_out"], rows=[{k: x[k] for k in ("bin", "E", "W", "sig_tot", "z")} for x in g["rows"]],
                             uniform_b=dict(status=u["status"], z=[x["z"] for x in u["rows"]]), law_only=dict(status=l["status"], z=[x["z"] for x in l["rows"]])))
            P(f"[{f}] C4 kappa {kap:5.3f}: {g['status']} z " + ", ".join(f"{x['z']:+.2f}" for x in g["rows"]) + f" | W " + ", ".join(f"{x['W']:+.3f}" for x in g["rows"])
              + f" | uniform-b {u['status']} | law-only {l['status']}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
            RES[f]["grid"] = grid; dump("kids_partial.json", RES)
        R["edges"] = edges(KGRID, [r["status"] for r in grid], lambda k: grade(f, k, CAP[f])["status"])
        P(f"[{f}] C4 edges {R['edges']}")
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("kids.json", RES)
    if os.path.exists(os.path.join(PARTS, "kids_partial.json")): os.remove(os.path.join(PARTS, "kids_partial.json"))
    P(f"kids done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")


if __name__ == "__main__":
    P(f"HY1 {WHICH}. Criteria 2fbb41123a. f_cap R = {CAP['canonical']:.4f} / {CAP['alt']:.4f} (F1A R {RF['canonical']:.6f} / {RF['alt']:.6f}). "
      "kappa = 1/2 FITTED; not theory closed; footings never pooled.")
    {"sparc": run_sparc, "battery": run_battery, "kids": run_kids}[WHICH]()
    P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
