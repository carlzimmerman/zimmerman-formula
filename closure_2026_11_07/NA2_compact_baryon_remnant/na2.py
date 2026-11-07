#!/usr/bin/env python3
"""NA2 (FROZEN_CRITERIA.md, b313324efd on origin): late-formed compact baryonic objects (CBOs, 1e2-1e7 Msun, no particle,
inside the BBN budget) as the hot-system half, a SEPARATE cause, under the plain a0 law per footing.
    python3 na2.py            -> na2.json / na2.out            (a) budget, (b) one rule, (c) dynamics, (d) shape + Bullet
    python3 na2.py --mutate   -> na2_MUTATE.json / .out        (M1-M5)
Read-only use of QX7 iter_5/iter_7 (X-COP, groups), GB1 battery, KD1, PB2, PB3, DB1 (phys + Bullet), SE2, eRASS1 on disk.
Does not touch the CMB wall. Adopts nothing. kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math, io, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
np.seterr(all="ignore"); TRAPZ = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22"); PBH = os.path.join(REPO, "pbh_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "na2_MUTATE" if MUT else "na2"; OUT = []
RES = dict(tag=TAG, criteria="b313324efd (origin; local bf4b0178aa)", note="Adopts nothing. Does not touch the CMB wall. kappa = 1/2 FITTED; not theory closed.")
def P(s=""): print(s, flush=True); OUT.append(s)
def RSS(stage): RES.setdefault("rss_MB_by_stage", {})[stage] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
def dump(tag=TAG):
    RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6   # macOS: bytes
    json.dump(RES, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
def _term(sig, frm):
    RES["interrupted"] = "SIGTERM"; dump(TAG + "_partial"); sys.exit(3)
signal.signal(signal.SIGTERM, _term)


# ------------------------------------------------------------------ Bullet child (separate process keeps each RSS under 1 GB): DB1 machinery read-only, as PB3 --bullet
def bullet_child(etas):
    DB1 = os.path.join(RB, "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read(); pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "na2"]
    BNS = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_na2"}; so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), BNS)
        o = dict(KA5=BNS["bullet_row"]("Z", "canonical", 0.0, Rs=[0.0, 0.0]))
        for f, e in etas.items(): o[f] = BNS["bullet_row"]("CBO", f, 0.0, Rs=[e, e], on="gal")
    finally: sys.stdout = so
    o["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("NA2CHILD " + json.dumps(o, default=float)); sys.exit(0)
if "--bullet-child" in sys.argv: bullet_child(json.loads(sys.argv[sys.argv.index("--bullet-child") + 1]))
# ------------------------------------------------------------------ QX7 iter_5 prelude (X-COP / groups machinery), as iter_7 loads it
I5 = os.path.join(CL6, "QX7_unified_cold_switch", "iter_5_host_hydrostatic", "qx7_iter5.py")
s5 = open(I5).read(); s5 = s5[:s5.index("# ---- K1:")]
argv0, sys.argv = sys.argv, [I5]; _so = sys.stdout; sys.stdout = io.StringIO()
NS = {"__file__": os.path.abspath(I5), "__name__": "iter5_reused"}
try: exec(compile(s5, I5, "exec"), NS)
finally: sys.argv = argv0; sys.stdout = _so
A0, XC, GR, XPROF, glaw, KPC, MS, G, pl_profile, DATA = (NS[k] for k in ("A0", "XC", "GR", "XPROF", "glaw", "KPC", "MS", "G", "pl_profile", "DATA"))
FCAP, RR = NS["FCAP"], NS["R"]
I7J = json.load(open(os.path.join(CL6, "QX7_unified_cold_switch", "iter_7_collisionless_remnant", "qx7_iter7.json")))
P(f"NA2 {'MUTATE' if MUT else 'MAIN'}: CBOs 1e2-1e7 Msun, one formation rule, plain law per footing. f_cap {FCAP}, R {RR:.3f}. kappa = 1/2 FITTED; not theory closed.")

# X-COP shapes, each normalised to 1 at Mb_last's radius (constant beyond), as iter_7's XGAS
SH = {}; XINFO = {}
for name in sorted({z["name"] for z in XC}):
    p_ = os.path.join(DATA, "xcop", name)
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); r500 = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy()
    gr = np.array(gas["RADIUS"], float) * r500; gM = np.array(gas["MGAS"], float); ok = np.isfinite(gM) & (gM > 0) & (gr > 0); fg = pl_profile(gr[ok], gM[ok])
    sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); ok = np.isfinite(sM) & (sM > 0) & (sr > 0); fs = pl_profile(sr[ok], sM[ok])
    hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); ok = np.isfinite(hM) & (hM > 0) & (hr > 0); fh = pl_profile(hr[ok], hM[ok])
    Mlast, tl = next(z["Mb_last"] for z in XC if z["name"] == name)
    fx, _ = XPROF[name]
    def norm(fun, tl=tl):
        t = float(fun(np.array([tl]))[0]); return lambda r_m, fun=fun, t=t, tl=tl: np.where(np.asarray(r_m, float) / KPC > tl, 1.0, fun(np.asarray(r_m, float) / KPC) / t)
    SH[name] = dict(gas=norm(fg), stars=norm(fs), hse=norm(fh), baryon=lambda r_m, fx=fx, Ml=Mlast: np.asarray(fx(np.asarray(r_m, float)), float) / Ml)
    XINFO[name] = dict(r500=r500, Mlast=Mlast, tl=tl, fg=fg, fs=fs, fh=fh, s500=float(fs(np.array([r500]))[0] / fg(np.array([r500]))[0]),
                       eta_conv=float(Mlast / fs(np.array([tl]))[0]))
BIN_EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]

def x_eval(f, shape, F, mobs=None):
    a0 = A0[f]; d = []; xr = []
    for i, z in enumerate(XC):
        rm = z["r_kpc"] * KPC; md = F * XINFO[z["name"]]["Mlast"] * float(SH[z["name"]][shape](np.array([rm]))[0])
        Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS
        Mo = z["M_obs"] if mobs is None else mobs[i]; d.append(math.log10(Mo / Mp)); xr.append(z["r_kpc"] / XINFO[z["name"]]["r500"])
    d = np.array(d); xr = np.array(xr); bins = []
    for lo, hi in zip(BIN_EDGES[:-1], BIN_EDGES[1:]):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None))
    mean, rms = float(d.mean()), float(np.sqrt((d ** 2).mean()))
    binok = all(abs(b["mean"]) <= 0.10 for b in bins if b["n"] >= 3)
    return dict(mean=mean, rms=rms, bins=bins, bins_ok=bool(binok), gate=bool(abs(mean) <= 0.05 and rms <= 0.10 and binok), d=d.tolist())
def golden(fun, lo, hi, it=80):
    g = (math.sqrt(5) - 1) / 2; a, b = lo, hi; c, e = b - g * (b - a), a + g * (b - a); fc, fe = fun(c), fun(e)
    for _ in range(it):
        if fc < fe: b, e, fe = e, c, fc; c = b - g * (b - a); fc = fun(c)
        else: a, c, fc = c, e, fe; e = a + g * (b - a); fe = fun(e)
    return 0.5 * (a + b)
def fit_x(f, shape, mobs=None): return golden(lambda F: x_eval(f, shape, F, mobs)["rms"], 0.0, 30.0)

def g_eval(f, shape, F, fst):
    a0 = A0[f]; npass = 0; dl = []; per = []
    for gp in GR:
        p0, p1 = gp["pts"][0], gp["pts"][1]; Mbt = gp["g5"] * (1 + fst)
        fg = pl_profile([p0["r_kpc"], p1["r_kpc"]], [p0["M_gas"] * (1 + fst), p1["M_gas"] * (1 + fst)]); ok = True; row = []
        for p in gp["pts"]:
            Mb = p["M_gas"] * (1 + fst); rm = p["r_kpc"] * KPC
            md = F * Mbt * (1.0 if shape == "point" else min(float(fg(np.array([p["r_kpc"]]))[0]) / Mbt, 1.0))
            Mp = glaw(G * (Mb + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; x = math.log10(p["M_obs"] / Mp); dl.append(x); row.append(round(x, 4))
            ok &= abs(x) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
        npass += ok; per.append(row)
    dl = np.array(dl); return dict(n_pass=int(npass), ssq=float((dl ** 2).sum()), median=float(np.median(dl)), r2500_med=float(np.median([r[0] for r in per])), r500_med=float(np.median([r[1] for r in per])))
def fit_g(f, shape, fst): return golden(lambda F: g_eval(f, shape, F, fst)["ssq"], 0.0, 30.0)

# ------------------------------------------------------------------ GB1 battery (read-only, as PB3 loads it)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]; so = sys.stdout; sys.stdout = io.StringIO()
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a; sys.stdout = so
    return ns
GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
KDJ = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
PB3J = json.load(open(os.path.join(PBH, "PB3_cluster_class_budget", "pb3.json")))
PB2J = json.load(open(os.path.join(PBH, "PB2_fmax_window", "pb2_fmax_results.json")))
SEJ = json.load(open(os.path.join(CL6, "SE2_step_as_systematics", "se2.json")))
D1P = json.load(open(os.path.join(RB, "DB1_cluster_dark_baryons", "db1_phys.json")))
RSS("after_iter5_prelude"); BATT = {}
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0); BATT[f] = dict(S=S, E=E, X=X, GR={0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}, U=GB["udgs"](f, a0), D=GB["dsphs"](f, a0))
P("battery loaded: " + ", ".join(f"{f}: SPARC {len(B['S'])}, X-COP {len(B['X'])}, ell {len(B['E'])}, UDG {len(B['U'])}, M31 {len(B['D']['bright M31'])}, LG {len(B['D']['LG field'])}" for f, B in BATT.items()))

# ------------------------------------------------------------------ section-2 amounts (frozen) and KA4
AMT = {"canonical": dict(XCOP=4.1786, SPARC_cap=0.3257, groups=(1.2320, 3.4640), M31=1.64, UDG=23.6, LG=0.0),
       "alt": dict(XCOP=3.7833, SPARC_cap=0.1937, groups=(0.9323, 2.8646), M31=1.50, UDG=20.2, LG=0.0)}
ka4 = True
for f in A0:
    u = KDJ["footings"][f]["uniform_f_diag"]
    ka4 &= abs(u["Xcop_f_need"] - AMT[f]["XCOP"]) <= 1e-4 and abs(u["SPARC_f_max"] - AMT[f]["SPARC_cap"]) <= 1e-4
    ka4 &= abs(u["groups_fst1_f_need"] - AMT[f]["groups"][0]) <= 1e-4 and abs(u["groups_fst0_f_need"] - AMT[f]["groups"][1]) <= 1e-4
    ka4 &= all(PB3J["footings"][f]["U"]["intervals"].get(k) is not None for k in ("SPARC", "X-COP", "groups_fst0", "groups_fst1", "ellipticals", "bright M31", "Coma UDGs"))

# ------------------------------------------------------------------ (b) machinery: S1 over bins, S3 leave-one-class-out
def lg_field_interval(f):
    hi = SEJ["footings"][f]["cells"]["LG field"]["post"]["ci95"][1]; return [0.0, 10 ** (2 * hi) - 1.0]
def class_points(f):
    B = BATT[f]; iv = PB3J["footings"][f]["U"]["intervals"]; C = {}
    fs = lambda ft: 1.0 - (ft["fgas"] if ft.get("fgas") is not None else 0.0)
    def q(ft, dwarf):
        Mb = ft["Mb"]; r = ft["r"] / KPC * 1e-3   # r in Mpc... use kpc below
        rk = ft["r"] / KPC; Sig = (Mb / (2 * math.pi * rk ** 2) if dwarf else Mb / (math.pi * rk ** 2)) / 1e6   # Msun/pc^2
        return dict(fstar=max(fs(ft), 1e-3), Mb=Mb, Sigma=Sig, v=ft["v"])
    C["SPARC"] = ([q(p["feat"], False) for p in B["S"]], iv["SPARC"])
    C["X-COP"] = ([q(p["feat"], False) for p in B["X"]], iv["X-COP"])
    for fst in (0, 1): C[f"groups_fst{fst}"] = ([q(p["feat"], False) for g in B["GR"][fst] for p in g["pts"]], iv[f"groups_fst{fst}"])
    C["ellipticals"] = ([q(p["feat"], False) for p in B["E"]], iv["ellipticals"])
    C["bright M31"] = ([q(p["feat"], True) for p in B["D"]["bright M31"]], iv["bright M31"])
    C["Coma UDGs"] = ([q(p["feat"], True) for p in B["U"]], iv["Coma UDGs"])
    C["LG field"] = ([q(p["feat"], True) for p in B["D"]["LG field"]], lg_field_interval(f))
    return C
KEYS = ("fstar", "Mb", "Sigma", "v")
HOT = ("X-COP", "groups_fst0", "groups_fst1", "Coma UDGs")
def s1(C, key, conv, groups_fst):
    """bins of 0.2 dex in log q; intervals per point (per-star: F interval / f_*). Returns conflicts list."""
    bins = {}
    for cls, (pts, iv) in C.items():
        if cls.startswith("groups") and cls != f"groups_fst{groups_fst}": continue
        for p in pts:
            lo, hi = iv; fsr = p["fstar"] if conv == "star" else 1.0
            bins.setdefault(math.floor(math.log10(p[key]) / 0.2), []).append((cls, lo / fsr, hi / fsr))
    conf = []; mids = {}
    for b, L in sorted(bins.items()):
        lo = max(x[1] for x in L); hi = min(x[2] for x in L); cl = sorted({x[0] for x in L})
        if len(cl) >= 2 and lo > hi:
            gap = math.log10(lo / hi) if hi > 0 else float("inf")
            lo_c = max(L, key=lambda x: x[1])[0]; hi_c = min(L, key=lambda x: x[2])[0]
            conf.append(dict(bin=[round(b * 0.2, 2), round(b * 0.2 + 0.2, 2)], classes=cl, need_lo=lo, from_=lo_c, allow_hi=hi, from_hi=hi_c, gap_dex=gap))
        elif lo <= hi: mids[b] = (cl, lo, hi)
    return conf, mids, bins
def s3(C, key, conv, fst):
    out = {}
    for k in C:
        if k.startswith("groups") and k != f"groups_fst{fst}": continue
        Ck = {c: v for c, v in C.items() if c != k}; conf, mids, _ = s1(Ck, key, conv, fst)
        qk = np.median([p[key] for p in C[k][0]]); lq = math.log10(qk)
        xs = np.array(sorted((b * 0.2 + 0.1, math.sqrt(max(lo, 1e-6) * hi) if hi > 0 else 0.0) for b, (cl, lo, hi) in mids.items()))
        if len(xs) == 0: out[k] = "UNCONSTRAINED BY OTHERS"; continue
        dist = 0.0 if xs[0, 0] <= lq <= xs[-1, 0] else min(abs(lq - xs[0, 0]), abs(lq - xs[-1, 0]))
        if dist > 0.5: out[k] = "UNCONSTRAINED BY OTHERS"; continue
        Fp = float(np.interp(lq, xs[:, 0], xs[:, 1])); lo, hi = C[k][1]; fsr = np.median([p["fstar"] for p in C[k][0]]) if conv == "star" else 1.0
        out[k] = "PASS" if lo / fsr <= Fp <= hi / fsr else f"FAIL (pred {Fp:.3g} vs [{lo/fsr:.3g}, {hi/fsr:.3g}])"
    return out

# ------------------------------------------------------------------ (c) machinery
TH = 13.8e9 * 3.156e7; MSs = 1.989e30
MGRID = [10 ** (2 + 0.25 * i) for i in range(21)]
def dyn_points(f):
    B = BATT[f]; a0 = A0[f]; Am = AMT[f]
    def pts(L, F, dwarf):
        o = []
        for p in L:
            ft = p["feat"]; Mb = ft["Mb"]
            if Mb is None: continue
            r = ft["r"]; sig = (ft["sigma"] if ft.get("sigma") else ft["v"] / math.sqrt(2)) * 1e3
            Min = Mb / 2 if dwarf else Mb; rho = F * Mb / 2 / (4 / 3 * math.pi * r ** 3) * MSs
            gN = G * (1 + F) * Min * MS / r ** 2; nu = glaw(gN, a0) / gN
            o.append(dict(r=r, sig=sig, rho=rho, nu=nu))
        return o
    return {"X-COP": pts(B["X"], Am["XCOP"], False), "groups": pts([p for g in B["GR"][0] for p in g["pts"]], Am["groups"][1], False),
            "bright M31": pts(B["D"]["bright M31"], Am["M31"], True), "Coma UDGs": pts(B["U"], Am["UDG"], True),
            "LG field @ SPARC cap (reported)": pts(B["D"]["LG field"], Am["SPARC_cap"], True)}
def lnL(r, sig, M): return max(1.0, math.log(r * sig ** 2 / (G * M * MSs)))
def t_heat(p, M): return p["sig"] ** 3 / (8 * math.pi * G ** 2 * M * MSs * p["rho"] * lnL(p["r"], p["sig"], M))
def t_df(p, M): t = 1.17 * p["r"] ** 2 * math.sqrt(2) * p["sig"] / (G * M * MSs * lnL(p["r"], p["sig"], M)); return min(t, t / p["nu"])
MP, KB, C_ = 1.6726e-27, 1.380649e-23, 2.998e8
def xray_ratio(f, F, M, eps_fixed=None):
    """median over X-COP clusters of L_acc(<R500) / L_brems(<R500); CBOs on the stars' shape at amount F x Mb_last."""
    out = []
    for name, I in XINFO.items():
        r = np.logspace(math.log10(10.0), math.log10(I["r500"]), 300)       # kpc
        Mg = I["fg"](r); rho = np.gradient(Mg, r) / (4 * math.pi * r ** 2) * MSs / (KPC ** 3)   # kg/m^3
        s = -np.gradient(np.log(np.maximum(rho, 1e-60)), np.log(r)); s = np.clip(s, 0.3, None)
        kT = 0.6 * MP * G * I["fh"](r) * MSs / (r * KPC * s)                # J
        Ms_ = I["fs"](r); Ms_ = np.minimum(Ms_ / I["fs"](np.array([I["tl"]]))[0], 1.0) * F * I["Mlast"]
        rc = np.gradient(Ms_, r) / (4 * math.pi * r ** 2) * MSs / (KPC ** 3); n_c = np.maximum(rc, 0) / (M * MSs)
        cs2 = 5 / 3 * kT / (0.6 * MP); v2 = 3 * kT / (0.6 * MP)
        Md = 4 * math.pi * 0.25 * G ** 2 * (M * MSs) ** 2 * rho / (cs2 + v2) ** 1.5
        Medd = 1.26e31 * M / (0.1 * C_ ** 2); md = Md / Medd
        eps = np.full_like(md, eps_fixed) if eps_fixed is not None else 0.1 * np.minimum(1.0, md / 0.01)
        Lacc = TRAPZ(n_c * eps * Md * C_ ** 2 * 4 * math.pi * (r * KPC) ** 2, r * KPC)
        T = kT / KB; ne = rho / (1.17 * MP) * 1e-6; ni = rho / (1.30 * MP) * 1e-6       # cm^-3
        Lb = TRAPZ(1.4e-27 * np.sqrt(T) * ne * ni * 1.2 * 1e-7 * 1e6 * 4 * math.pi * (r * KPC) ** 2, r * KPC)   # erg/s/cm^3 -> W/m^3
        out.append(Lacc / Lb)
    return float(np.median(out))
def window(f, Fx, Mlist=MGRID):
    D = dyn_points(f); rows = {}
    for M in Mlist:
        r = {}
        for cls, L in D.items():
            th = float(np.median([t_heat(p, M) for p in L])) / TH; td = float(np.median([t_df(p, M) for p in L])) / TH
            ok = td >= 1.0 and (th >= 1.0 if cls in ("bright M31", "Coma UDGs") or cls.startswith("LG") else True)
            r[cls] = dict(t_heat_over_tH=th, t_DF_over_tH=td, ok=bool(ok))
        xr = xray_ratio(f, Fx, M); r["X-COP"]["Lacc_over_Lbrems"] = xr; r["X-COP"]["ok"] = bool(r["X-COP"]["ok"] and xr <= 0.1)
        r["X-COP"]["Lacc_over_Lbrems_eps0.1"] = xray_ratio(f, Fx, M, eps_fixed=0.1)
        rows[f"{M:.3g}"] = r
    need = ("X-COP", "groups", "bright M31", "Coma UDGs")
    allowed = {c: [m for m, r in rows.items() if r[c]["ok"]] for c in list(need) + ["LG field @ SPARC cap (reported)"]}
    win = [m for m, r in rows.items() if all(r[c]["ok"] for c in need)]
    return rows, allowed, win

# =================================================================== MUTATE
if MUT:
    allok = True
    for f in A0:
        R = RES.setdefault(f, {})
        # M1: planted star-traced truth at F = 3
        mob = [glaw(G * (z["M_b"] + 3.0 * XINFO[z["name"]]["Mlast"] * float(SH[z["name"]]["stars"](np.array([z["r_kpc"] * KPC]))[0])) * MS / (z["r_kpc"] * KPC) ** 2, A0[f])
               * (z["r_kpc"] * KPC) ** 2 / G / MS for z in XC]
        F1 = fit_x(f, "stars", mob); e1 = x_eval(f, "stars", F1, mob); ok1 = abs(F1 / 3.0 - 1) <= 0.02 and e1["gate"]
        # M2: planted gas-traced truth at f_cap R
        F0 = FCAP * RR
        mob2 = [glaw(G * (z["M_b"] + F0 * XINFO[z["name"]]["Mlast"] * float(SH[z["name"]]["gas"](np.array([z["r_kpc"] * KPC]))[0])) * MS / (z["r_kpc"] * KPC) ** 2, A0[f])
                * (z["r_kpc"] * KPC) ** 2 / G / MS for z in XC]
        F2 = fit_x(f, "stars", mob2); e2 = x_eval(f, "stars", F2, mob2); ok2 = not e2["gate"]
        # M3 / M4: planted rule on key Mb
        C = class_points(f); med = np.median([p["Mb"] for p in C["SPARC"][0]])
        Ft = lambda q: 10 ** (0.3 * math.log10(q / med))
        C3 = {c: (pts, [min(Ft(p["Mb"]) for p in pts) / 1.2, max(Ft(p["Mb"]) for p in pts) * 1.2]) for c, (pts, iv) in C.items()}
        C4 = {c: (pts, [iv[0] * (10 if c in HOT else 1), iv[1] * (10 if c in HOT else 1)]) for c, (pts, iv) in C3.items()}
        c3 = [s1(C3, "Mb", "baryon", fst)[0] for fst in (0, 1)]; c4 = [s1(C4, "Mb", "baryon", fst)[0] for fst in (0, 1)]
        ok3 = all(len(c) == 0 for c in c3); ok4 = all(len(c) > 0 for c in c4)
        # M5: M_c = 1e9 in UDGs and bright M31
        rows, allowed, win = window(f, AMT[f]["XCOP"], [1e9]); r9 = rows["1e+09"]
        ok5 = (not r9["Coma UDGs"]["ok"]) and (not r9["bright M31"]["ok"])
        R.update(M1=dict(F_fit=F1, gate=e1["gate"], mean=e1["mean"], rms=e1["rms"], holds=bool(ok1)), M2=dict(F_fit=F2, gate=e2["gate"], mean=e2["mean"], rms=e2["rms"], bins=e2["bins"], bites=bool(ok2)),
                 M3=dict(conflicts=[len(c) for c in c3], holds=bool(ok3)), M4=dict(conflicts=[len(c) for c in c4], bites=bool(ok4)), M5=dict(row=r9, bites=bool(ok5)))
        P(f"[{f}] M1 planted stars F=3: fit {F1:.4f}, X-COP {e1['mean']:+.4f}/{e1['rms']:.4f} gate {e1['gate']} -> {'HOLDS' if ok1 else 'NO POWER'}")
        P(f"[{f}] M2 planted gas F={F0:.3f}: stars fit {F2:.3f}, {e2['mean']:+.4f}/{e2['rms']:.4f}, bins " + ", ".join(f"{b['mean']:+.3f}" if b['mean'] is not None else "-" for b in e2["bins"]) + f" gate {e2['gate']} -> {'BITES' if ok2 else 'NO BITE'}")
        P(f"[{f}] M3 planted rule (key Mb): empty bins {[len(c) for c in c3]} -> {'HOLDS' if ok3 else 'FALSE CONFLICT'}; M4 planted step x10 hot: empty bins {[len(c) for c in c4]} -> {'BITES' if ok4 else 'NO BITE'}")
        P(f"[{f}] M5 M_c 1e9: UDG t_heat/t_H {r9['Coma UDGs']['t_heat_over_tH']:.3g}, t_DF/t_H {r9['Coma UDGs']['t_DF_over_tH']:.3g}; M31 {r9['bright M31']['t_heat_over_tH']:.3g}, {r9['bright M31']['t_DF_over_tH']:.3g} -> {'BITES' if ok5 else 'NO BITE'}")
        allok &= ok1 and ok2 and ok3 and ok4 and ok5
    RES["MUTATE_all"] = bool(allok); P(f"MUTATE: {'all hold / bite' if allok else 'SOMETHING FAILED -> NO VERDICT'}"); P("kappa = 1/2 FITTED; not theory closed.")
    P(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB"); dump(); sys.exit(0 if allok else 1)

# =================================================================== known answers
RSS("after_battery"); KA = {}
i7 = I7J["rows"]["2.154"]["gas"]
for f in A0:
    e = x_eval(f, "gas", FCAP * RR); b = x_eval(f, "baryon", FCAP * RR); z0 = x_eval(f, "gas", 0.0)
    KA[f"KA1_gas_{f}"] = dict(mine=[e["mean"], e["rms"]], ref=[i7[f]["X_mean"], i7[f]["X_rms"]], ok=bool(abs(e["mean"] - i7[f]["X_mean"]) <= 1e-3 and abs(e["rms"] - i7[f]["X_rms"]) <= 1e-3))
    ref = I7J["K2"]["mine"][0 if f == "canonical" else 1]
    KA[f"KA1_baryon_{f}"] = dict(mine=[b["mean"], b["rms"]], ref_mean=ref, ok=bool(abs(b["mean"] - ref) <= 1e-3 and abs(b["rms"] - (0.082 if f == "canonical" else 0.087)) <= 1e-3))
    KA[f"KA2_{f}"] = dict(mine=z0["mean"], ref=0.4675 if f == "canonical" else 0.4345, ok=bool(abs(z0["mean"] - (0.4675 if f == "canonical" else 0.4345)) <= 1e-3))
surv = [c["cls"] for c in D1P["classes"] if c["survives"]]
am = D1P["amounts_300kpc"]; cg = [am[k]["cb_over_gas"] for k in ("P1G|canonical", "P1G|alt", "P3|canonical", "P3|alt")]
KA["KA3_DB1"] = dict(survivors=surv, cb_over_gas=[min(cg), max(cg)], ok=bool(len(surv) == 1 and "black hole" in surv[0].lower() and 4.3 <= min(cg) and max(cg) <= 5.5))
KA["KA4_amounts"] = dict(ok=bool(ka4))
KA5_PENDING = True
RES["KA"] = KA; KA_ok = all(v["ok"] for v in KA.values()); RES["KA_all"] = bool(KA_ok)
for k, v in KA.items(): P(f"  {k}: {'PASS' if v['ok'] else 'FAIL'}  " + json.dumps({kk: vv for kk, vv in v.items() if kk != 'ok'}, default=lambda x: round(float(x), 4))[:200])
if not KA_ok:
    P("KNOWN ANSWER FAILED: stop, nothing graded."); RES["label"] = "NO VERDICT (known answer failed)"; dump(); sys.exit(2)

# =================================================================== (d) shape
RSS("after_KA_bullet_exec"); SHAPE = {}
for f in A0:
    o = {}
    for shp in ("stars", "hse", "gas", "baryon"):
        Fx = fit_x(f, shp); e = x_eval(f, shp, Fx); o[shp] = dict(F=Fx, **{k: v for k, v in e.items() if k != "d"})
    for shp in ("point", "gas"):
        for fst in (0, 1):
            Fg = fit_g(f, shp, fst); o[f"groups_{shp}_fst{fst}"] = dict(F=Fg, **g_eval(f, shp, Fg, fst))
    o["X_gate"] = o["stars"]["gate"]; o["G_gate"] = bool(o["groups_point_fst0"]["n_pass"] >= 16 and o["groups_point_fst1"]["n_pass"] >= 16)
    o["eta_X"] = float(np.median([o["stars"]["F"] * I["eta_conv"] for I in XINFO.values()]))
    SHAPE[f] = o
    for shp in ("stars", "hse", "gas", "baryon"):
        s = o[shp]; P(f"[{f}] X-COP {shp:6s} F {s['F']:.3f}: mean {s['mean']:+.4f} rms {s['rms']:.4f}; bins " + ", ".join(f"{b['lo']}-{b['hi']}:{b['mean']:+.3f}({b['n']})" if b["mean"] is not None else f"{b['lo']}-{b['hi']}:-" for b in s["bins"]) + f" -> {'PASS' if s['gate'] else 'FAIL'}{'  [graded]' if shp == 'stars' else ''}")
    for shp in ("point", "gas"):
        P(f"[{f}] groups {shp:5s}: " + "; ".join(f"fst{fst} F {o[f'groups_{shp}_fst{fst}']['F']:.3f} pass {o[f'groups_{shp}_fst{fst}']['n_pass']}/20 med R2500 {o[f'groups_{shp}_fst{fst}']['r2500_med']:+.3f} R500 {o[f'groups_{shp}_fst{fst}']['r500_med']:+.3f}" for fst in (0, 1)) + ("  [graded]" if shp == "point" else ""))
# Bullet with CBOs on galaxies at eta_X (child process) + KA5 from the same child
import subprocess
cp = subprocess.run([sys.executable, os.path.abspath(__file__), "--bullet-child", json.dumps({f: SHAPE[f]["eta_X"] for f in A0})], capture_output=True, text=True)
line = [l for l in cp.stdout.splitlines() if l.startswith("NA2CHILD ")]
if cp.returncode != 0 or not line: P("bullet child failed: " + cp.stderr[-500:]); RES["label"] = "NO VERDICT (bullet child failed)"; dump(); sys.exit(2)
BC = json.loads(line[0][9:]); k0 = BC["KA5"]; RES["bullet_child_peak_rss_MB"] = BC["child_peak_rss_MB"]
KA["KA5_bullet"] = dict(M300=k0["M300"], dkappa=k0["dkappa"], ok=bool(abs(k0["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k0["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k0["dkappa"][0] + 0.068) < 0.002 and abs(k0["dkappa"][1] + 0.111) < 0.002))
P(f"  KA5_bullet: {'PASS' if KA['KA5_bullet']['ok'] else 'FAIL'}  M300 {k0['M300'][0]:.4g}, {k0['M300'][1]:.4g}; dkappa {k0['dkappa'][0]:+.4f}, {k0['dkappa'][1]:+.4f} (child peak RSS {BC['child_peak_rss_MB']:.0f} MB)")
RES["KA_all"] = bool(all(v["ok"] for v in KA.values()))
if not KA["KA5_bullet"]["ok"]: P("KNOWN ANSWER FAILED: stop."); RES["label"] = "NO VERDICT (known answer failed)"; dump(); sys.exit(2)
for f in A0:
    b = BC[f]; SHAPE[f]["bullet"] = b
    P(f"[{f}] Bullet, CBOs on galaxies, eta_X {SHAPE[f]['eta_X']:.2f}: {b['label']} ({b['cls']}); M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; dkappa {b['dkappa'][0]:+.3f}, {b['dkappa'][1]:+.3f}; d_gal {b['d_gal'][0]:.0f}, {b['d_gal'][1]:.0f} kpc vs d_gas {b['d_gas'][0]:.0f}, {b['d_gas'][1]:.0f}")
RES["shape"] = SHAPE

# =================================================================== (a) amount and budget
RSS("after_shape_bullet"); BUD = {}
d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
z = np.array(d["BEST_Z"], float); pc = np.array(d["PCONT"], float); mg = np.array(d["MGAS500"], float) * 1e11; m5 = np.array(d["M500"], float) * 1e13
RHO_B = 0.02166 * 2.775e11   # Msun / Mpc^3, h-free (BBN D/H, PROVISIONAL as DB1/PB3)
sX = float(np.mean([I["s500"] for I in XINFO.values()]))
def census(f, zmax=0.10, pcmax=0.5, area=20626.0, h=0.70, sG=1.0):
    sel = (z >= 0.02) & (z <= zmax) & (pc <= pcmax) & np.isfinite(mg) & (mg > 0) & np.isfinite(m5)
    Dh = 2.998e5 / (100 * h); V = area / 41252.96 * 4 / 3 * math.pi * ((Dh * zmax) ** 3 - (Dh * 0.02) ** 3)
    hs = (h / 0.70) ** 2.5            # catalogue gas masses at h 0.70 -> M_gas ~ D^2.5
    cl = sel & (m5 >= 1e14); gr = sel & (m5 >= 1e13) & (m5 < 1e14)
    Mb_cl = mg[cl].sum() / hs * (1 + sX); Mb_gr = mg[gr].sum() / hs * (1 + sG)
    Fx, Fg = AMT[f]["XCOP"], AMT[f]["groups"][1]
    B1 = ((1 + Fx) * Mb_cl + (1 + Fg) * Mb_gr) / (RHO_B * V)
    return dict(N_cl=int(cl.sum()), N_gr=int(gr.sum()), V_Mpc3=V, hostbaryons_over_rhob=(Mb_cl + Mb_gr) / (RHO_B * V), cbo_over_rhob=(Fx * Mb_cl + Fg * Mb_gr) / (RHO_B * V), B1=B1)
for f in A0:
    Am = AMT[f]; c0 = census(f)
    br = {"area13116": census(f, area=13116.0), "pcont0.2": census(f, pcmax=0.2), "h0.67": census(f, h=0.67), "h0.74": census(f, h=0.74), "zmax0.05": census(f, zmax=0.05), "groups_s0": census(f, sG=0.0)}
    worst = max([c0["B1"]] + [v["B1"] for v in br.values()])
    per = {"X-COP": Am["XCOP"], "groups (upper)": Am["groups"][1], "bright M31": Am["M31"], "Coma UDGs": Am["UDG"], "SPARC cap": Am["SPARC_cap"], "LG field": Am["LG"]}
    prov = dict(DB1_census_hot_gas_share=[0.04, 0.10], cbo_share=[0.04 * Am["XCOP"] * (1 + sX), 0.10 * Am["XCOP"] * (1 + sX)])
    BUD[f] = dict(per_class_F=per, progenitor_over_now={k: 1 + v for k, v in per.items()}, census=c0, brackets=br, B1_worst=worst, B1_pass=bool(worst <= 1.0), provisional=prov, s_XCOP=sX)
    P(f"[{f}] (a) eRASS1 lower bound: {c0['N_cl']} clusters + {c0['N_gr']} groups, V {c0['V_Mpc3']:.3g} Mpc^3; host baryons {c0['hostbaryons_over_rhob']:.4f} of rho_b(BBN), CBOs {c0['cbo_over_rhob']:.4f}; "
      f"B1 {c0['B1']:.4f} (worst bracket {worst:.4f}) -> {'not excluded (lower bound)' if worst <= 1 else 'DEAD'}; PROVISIONAL DB1 census reading: CBO share {prov['cbo_share'][0]:.2f}-{prov['cbo_share'][1]:.2f} of cosmic baryons")
RES["budget"] = BUD

# =================================================================== (c) dynamics
RSS("after_budget"); DYN = {}
for f in A0:
    rows, allowed, win = window(f, SHAPE[f]["stars"]["F"])
    fb_cbo = BUD[f]["census"]["cbo_over_rhob"]; prov_hi = BUD[f]["provisional"]["cbo_share"][1]
    fa = PB2J["footings"][f]["factors"]; rep = {}
    for M in ("100.0", "1000.0", "10000.0", "100000.0", "1000000.0", "10000000.0"):
        fw = lambda k: (fa[k][M][1] if fa[k].get(M) and fa[k][M][1] is not None else None)
        rep[M] = dict(D1=fw("D1"), D3=fw("D3"), D4=fw("D4"), X1=fw("X1"), L3=fw("L3"),
                      discs_at_cap_ok=all(v is None or v >= AMT[f]["SPARC_cap"] for v in (fw("D1"), fw("D3"), fw("D4"), fw("X1"))),
                      L3_ok_lowerbound=(fw("L3") is None or fw("L3") >= fb_cbo), L3_ok_provisional_hi=(fw("L3") is None or fw("L3") >= prov_hi))
    DYN[f] = dict(rows=rows, allowed=allowed, window=win, empty=bool(len(win) == 0), reported_PB2=rep, fb_cbo_lowerbound=fb_cbo)
    P(f"[{f}] (c) allowed M_c per class: " + "; ".join(f"{c}: {('%s-%s' % (v[0], v[-1])) if v else 'NONE'}" for c, v in allowed.items()))
    P(f"[{f}] (c) window (all needing classes): {('%s-%s (%d grid pts)' % (win[0], win[-1], len(win))) if win else 'EMPTY'}")
    for m in ("100", "1e+04", "1e+05", "1e+06", "1e+07"):
        r = rows[m]; P(f"      M_c {m}: UDG t_heat {r['Coma UDGs']['t_heat_over_tH']:.3g} t_DF {r['Coma UDGs']['t_DF_over_tH']:.3g}; M31 {r['bright M31']['t_heat_over_tH']:.3g}, {r['bright M31']['t_DF_over_tH']:.3g}; "
                     f"groups t_DF {r['groups']['t_DF_over_tH']:.3g}; X-COP t_DF {r['X-COP']['t_DF_over_tH']:.3g}, L_acc/L_brems {r['X-COP']['Lacc_over_Lbrems']:.3g} (eps 0.1: {r['X-COP']['Lacc_over_Lbrems_eps0.1']:.3g})")
    P(f"      reported PB2 FW at the SPARC cap (discs carry {AMT[f]['SPARC_cap']}): " + "; ".join(f"{float(M):.0e} {'ok' if v['discs_at_cap_ok'] else 'closed'} (D4 {v['D4']})" for M, v in rep.items()))
    P(f"      reported L3 (CONDITIONAL z_f >= 2) at f_b,cbo lower bound {fb_cbo:.3f} / provisional {prov_hi:.2f}: " + "; ".join(f"{float(M):.0e} {v['L3']:.3g} {'ok' if v['L3_ok_lowerbound'] else 'closed'}/{'ok' if v['L3_ok_provisional_hi'] else 'closed'}" for M, v in rep.items()))
RES["dynamics"] = DYN

# =================================================================== (b) one formation rule
RSS("after_dynamics"); RULE = {}; spread = {}
for f in A0:
    C = class_points(f); o = {}
    for key in KEYS:
        for conv in ("baryon", "star"):
            r = {}
            for fst in (0, 1):
                conf, mids, _ = s1(C, key, conv, fst)
                r[f"fst{fst}"] = dict(n_empty=len(conf), widest=max(conf, key=lambda c: c["gap_dex"]) if conf else None, conflicts=conf[:40])
                if not conf: r[f"fst{fst}"]["S3"] = s3(C, key, conv, fst)
            dead = any(r[k]["n_empty"] > 0 for k in r)
            s3ok = (not dead) and all(all(v == "PASS" for v in r[k]["S3"].values()) for k in r)
            r["status"] = "S1 DEAD" if dead else ("S3 PASS" if s3ok else "S3 FAIL / UNCONSTRAINED")
            o[f"{key}|{conv}"] = r
            w = r["fst0"]["widest"]
            P(f"[{f}] (b) key {key:6s} per {conv:6s}: {r['status']}; empty bins {r['fst0']['n_empty']}/{r['fst1']['n_empty']}" + (f"; widest {w['bin']} {w['classes']} need >= {w['need_lo']:.3g} ({w['from_']}) vs <= {w['allow_hi']:.3g} ({w['from_hi']}), gap {w['gap_dex']:.2f} dex" if w else ""))
    one = any(v["status"] == "S3 PASS" for v in o.values())
    Am = AMT[f]; sp = Am["UDG"] / Am["SPARC_cap"]
    RULE[f] = dict(keys=o, one_rule=bool(one), spread_UDG_over_SPARCcap=sp, spread_XCOP_over_SPARCcap=Am["XCOP"] / Am["SPARC_cap"])
    P(f"[{f}] (b) ONE RULE {'EXISTS' if one else 'NONE'}; spread needed UDG/SPARC-cap {sp:.0f}x, X-COP/SPARC-cap {Am['XCOP']/Am['SPARC_cap']:.1f}x, M31 vs LG field {Am['M31']} vs 0")
RES["rule"] = RULE

# =================================================================== labels
LAB = {}
for f in A0:
    rows_fail = []
    if not SHAPE[f]["X_gate"]: rows_fail.append("X-COP shape")
    if not SHAPE[f]["G_gate"]: rows_fail.append("groups shape")
    if SHAPE[f]["bullet"]["label"] != "PASS": rows_fail.append("Bullet")
    for c in ("X-COP", "groups", "bright M31", "Coma UDGs"):
        if not DYN[f]["allowed"][c]: rows_fail.append(f"{c} dynamics")
    if not BUD[f]["B1_pass"] or DYN[f]["empty"]: L = "DEAD (" + ", ".join((["budget B1"] if not BUD[f]["B1_pass"] else []) + (["empty M_c window"] if DYN[f]["empty"] else [])) + ")"
    elif rows_fail: L = "FAILS (" + ", ".join(rows_fail) + ")"
    elif not RULE[f]["one_rule"]: L = "CONSISTENT, NOT PREDICTIVE"
    else: L = "SURVIVES (scoped)"
    LAB[f] = dict(label=L, rows_failed=rows_fail, one_rule=RULE[f]["one_rule"])
    P(f"[{f}] LABEL: {L}; one rule: {'yes' if RULE[f]['one_rule'] else 'NO'}")
RES["labels"] = LAB
order = ["NO VERDICT", "DEAD", "FAILS", "CONSISTENT", "SURVIVES"]
worst = min(LAB.values(), key=lambda v: order.index(v["label"].split(" ")[0].rstrip(",")))
RES["label"] = "canonical: " + LAB["canonical"]["label"] + " | alt: " + LAB["alt"]["label"] + " | overall: " + worst["label"].split(" (")[0] + " (MUTATE in na2_MUTATE.json)"
P("LABEL LINE: " + RES["label"]); P("Does not touch the CMB wall. kappa = 1/2 FITTED; not theory closed.")
P(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB"); dump()
