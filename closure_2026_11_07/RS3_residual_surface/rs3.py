#!/usr/bin/env python3
"""RS3 (criteria 8158e4645f, amendments A1 5123eda762, A2 ce2859f5b4): the residual surface. RS3 = the brief's RS1.
Does any monotone function of TWO frozen local variables carry the required uniform extra-mass fraction f
(y = log10(1+f)) across every class, discs and field dwarfs at f = 0, inside the measured errors?
    python3 rs3.py            -> rs3.json / rs3.out          (KA1-KA4, main + pericentre reading, LOO table)
    python3 rs3.py --mutate   -> rs3_MUTATE.json / .out      (M1 shuffled labels, M2 Newtonian f)
Read-only use of GB1 (loaders, features, gates), KD1 (f table), SE2 (shifts, widths, admissibility), EV1 (x_e),
X1 / LW1 / S1 rows, RC3 colours, LVD gas. One thread; SIGTERM -> checkpoint and exit 3; rerun resumes.
Adopts nothing. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv, re, signal, resource, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np, warnings
from scipy.optimize import nnls, brentq
warnings.simplefilter("ignore", RuntimeWarning)          # free isotonic (reported only) overflows on near-singular nodes

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "rs3_MUTATE" if MUT else "rs3"; OUT = []
CKPT = os.path.join(HERE, TAG + "_ckpt.json")
def P(s=""): print(s, flush=True); OUT.append(s)
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
T_START = time.time()

# ------------------------------------------------------------------ GB1 library, read-only (as SE2 / KD1 load it)
GBP = os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"); _src = open(GBP).read()
_cut = _src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GBP, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(_src[:_cut], "gb1_lib", "exec"), NS); sys.argv = _a
A0, G, MS, KPC, PC, CC = NS["A0"], NS["G"], NS["MS"], NS["KPC"], NS["PC"], NS["C"]
glaw, delta, b_imf, tail_phi = NS["glaw"], NS["delta"], NS["b_imf"], NS["tail_phi"]
SP, EL, XC, GR, UROWS, X1R, R1 = NS["SP"], NS["EL"], NS["XC"], NS["GR"], NS["UROWS"], NS["X1R"], NS["R1"]
assert abs(A0["canonical"] - 9.3603e-11) / 9.3603e-11 < 1e-4 and abs(A0["alt"] - 1.1312e-10) / 1.1312e-10 < 1e-4
LSTAR = NS["LSTAR"]; assert LSTAR == {"canonical": 21.7, "alt": 22.9}

SE2 = json.load(open(os.path.join(CL6, "SE2_step_as_systematics", "se2.json")))
KD1 = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
EV1 = json.load(open(os.path.join(CL6, "EV1_environment_reread", "readings.json")))["systems"]
PERI = 3 ** (2 / 3); TAU_LINE = 0.375; LN10 = math.log(10)
CLASSES = ("SPARC", "ellipticals", "X-COP", "groups", "bright M31", "Coma UDGs", "LG field")
TARGET0 = ("SPARC", "LG field")
VARS = ("gN", "gobs", "rho_b", "Mb", "r_rhalf", "depth", "sigma", "Sigma_b", "x_e", "f_gas", "colour", "rho_b_rhoDE")
LINEAR = ("f_gas", "colour")
PAIRS = list(itertools.combinations(VARS, 2))
ORIENT = ((1, 1), (1, -1), (-1, 1), (-1, -1))
RES = dict(tag=TAG, criteria="8158e4645f", amendment_A1="5123eda762", amendment_A2="ce2859f5b4", lane="RS3 = the brief's RS1",
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.", KA={}, footings={})
P(f"RS3 residual surface {'MUTATE' if MUT else 'MAIN'} (RS3 = the brief's RS1). kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ side inputs: SPARC V_flat, RC3 colours, LVD gas
VFLAT = {}
for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: VFLAT[t[0]] = float(t[15])
    except ValueError: continue
def nname(s):
    s = s.upper().replace(" ", ""); m = re.match(r"^([A-Z]+)0*(\d.*)$", s)
    return (m.group(1) + m.group(2)) if m else s
RC3 = {}
_hdr = None
for ln in open(os.path.join(DATA, "rc3_devaucouleurs1991_colors.tsv")):
    if ln.startswith("#") or not ln.strip(): continue
    c = ln.rstrip("\n").split("\t")
    if _hdr is None: _hdr = [h.strip() for h in c]; continue
    d = dict(zip(_hdr, c)); bv = (d.get("B-VT") or "").strip()
    try: bv = float(bv)
    except ValueError: continue
    for k in ("name", "altname"):
        nm = (d.get(k) or "").strip()
        if nm: RC3.setdefault(nname(nm), bv)
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv", "lvd_dwarf_local_field_distant.csv"):
    p_ = os.path.join(DATA, "dsph", fn)
    if os.path.exists(p_):
        for r in csv.DictReader(open(p_)): LVD.setdefault(r["name"], r)

# ------------------------------------------------------------------ helpers
def rho_de(a0): return 4 * a0 ** 2 / (G * CC ** 2)           # OQ1: a0^2 / (kappa^2 c^2 G), kappa 1/2
def gmean(a): a = np.asarray(a, float); return float(np.exp(np.mean(np.log(a))))
def dlaw_mean(q, gN, b, a0): return float(np.mean([math.log10(glaw(q * bb * g, a0) / glaw(g, a0)) for g, bb in zip(gN, b)]))
def y_of(Dbar, gN, b, a0):
    """y = log10(1 + f) solving mean_points log10(g_law((1+f) b gN)/g_law(gN)) = Dbar (KD1's f, per system)."""
    h = lambda lq: dlaw_mean(math.exp(lq), gN, b, a0) - Dbar
    return brentq(h, -40.0, 40.0, xtol=1e-14, rtol=1e-14, maxiter=500) / LN10
def jac(Dbar, gN, b, a0): return (y_of(Dbar + 0.01, gN, b, a0) - y_of(Dbar - 0.01, gN, b, a0)) / 0.02
def rhalf_from(r, M, Mtot):
    """half-mass radius of a cumulative profile (monotone envelope), log-log interpolation; inward M ~ r."""
    o = np.argsort(r); r = np.asarray(r, float)[o]; M = np.maximum.accumulate(np.asarray(M, float)[o]); h = 0.5 * Mtot
    if M[0] >= h: return float(r[0] * h / M[0])
    i = int(np.argmax(M >= h)) if np.any(M >= h) else len(M) - 1
    if M[i] < h: return float(r[-1])
    return float(math.exp(np.interp(math.log(h), [math.log(M[i - 1]), math.log(M[i])], [math.log(r[i - 1]), math.log(r[i])])))
def cell(f, c): return SE2["footings"][f]["cells"][c]
def sysw(f, c): p, r = cell(f, c)["post"]["sd"], cell(f, c)["raw_stat_only"]["sd"]; return math.sqrt(max(p * p - r * r, 0.0))
def pvars(gN, gobs, Mb_ms, r_m, depth, a0):
    Mk = Mb_ms * MS; rho = 3 * Mk / (4 * math.pi * r_m ** 3)
    return dict(gN=gN, gobs=gobs, rho_b=rho, Mb=Mb_ms, depth=depth, Sigma_b=Mk / (math.pi * r_m ** 2), rho_b_rhoDE=rho / rho_de(a0))
def agg(pl):
    return {k: gmean([p[k] for p in pl]) for k in pl[0]}

# ------------------------------------------------------------------ rows per footing
def build_rows(f, a0, peri=False):
    S, E, X = NS["build"](f, a0); rows = []; anchor = SE2["footings"][f]["anchor"]
    # SPARC: target y = 0; sigma = rms over galaxies of the galaxy-mean exact-field residual (D - T_geom)
    k = 0; sp = []
    for g in SP:
        n = len(g["R"]); pts = S[k:k + n]; k += n
        D = np.array([p["D"] for p in pts]); T = np.array([p["feat"]["Tgeom"] for p in pts])
        gN = [p["feat"]["x"] * a0 for p in pts]; Mb = [p["feat"]["Mb"] for p in pts]; r = [p["feat"]["r"] for p in pts]
        rh = rhalf_from(r, Mb, Mb[-1])
        pl = [pvars(gN[i], glaw(gN[i], a0) * 10 ** D[i], Mb[i], r[i], pts[i]["feat"]["depth"], a0) for i in range(n)]
        v = agg(pl); v["r_rhalf"] = gmean(np.array(r) / rh)
        vf = VFLAT.get(g["name"], 0.0); v["sigma"] = (vf if vf > 0 else float(g["V"][-1] / 1e3)) / math.sqrt(2)
        v["x_e"] = EV1["SPARC:" + g["name"]][f]["x_e_noclu"]; v["f_gas"] = float(np.mean([p["feat"]["fgas"] for p in pts]))
        v["colour"] = RC3.get(nname(g["name"]))
        sp.append(dict(cls="SPARC", name=g["name"], ex=float(np.mean(D - T)), gN=gN, b=[1.0] * n, Dbar=0.0, shift=0.0, vars=v,
                       yN=float(np.mean(np.log10([pl[i]["gobs"] / gN[i] for i in range(n)])))))
    assert k == len(S)
    sS = float(np.sqrt(np.mean([s["ex"] ** 2 for s in sp])))
    for s in sp: s["sig"] = sS; s["target"] = True
    rows += sp
    # ellipticals after IMF (QX26 nominal b_imf); no per-system errors carried -> SE2 raw sd x sqrt(n)
    en = sorted({p["name"] for p in E}); sE_ = cell(f, "ellipticals")["raw_stat_only"]["sd"] * math.sqrt(len(en))
    for nm in en:
        pts = [p for p in E if p["name"] == nm]; e = [q for q in EL if q["name"] == nm][0]
        b = [b_imf(p["feat"]) for p in pts]; gN = [p["feat"]["x"] * a0 for p in pts]; D = [p["D"] for p in pts]
        rh = e["Re"] / 1.8153 * (1 + math.sqrt(2)) * KPC
        pl = [pvars(gN[i] * b[i], glaw(gN[i], a0) * 10 ** D[i], pts[i]["feat"]["Mb"] * b[i], pts[i]["feat"]["r"], pts[i]["feat"]["depth"], a0) for i in range(3)]
        v = agg(pl); v["r_rhalf"] = gmean([p["feat"]["r"] / rh for p in pts]); v["sigma"] = pts[0]["feat"]["sigma"]
        v["x_e"] = EV1["ELL:" + nm][f]["x_e_noclu"]; v["f_gas"] = 0.0; v["colour"] = RC3.get(nname(nm))
        rows.append(dict(cls="ellipticals", name=nm, gN=gN, b=b, Dbar=float(np.mean(D)), shift=0.0, sig=sE_, vars=v, target=False,
                         yN=float(np.mean([math.log10(pl[i]["gobs"] / (gN[i] * b[i])) for i in range(3)]))))
    # X-COP, SE2 reading
    xs = cell(f, "X-COP")["post"]["median"] - cell(f, "X-COP")["raw_stat_only"]["median"]
    for nm in sorted({z["name"] for z in XC}):
        ii = [i for i, z in enumerate(XC) if z["name"] == nm]; pts = [X[i] for i in ii]; zz = [XC[i] for i in ii]
        gN = [p["feat"]["x"] * a0 for p in pts]; D = [p["D"] for p in pts]
        sl = [z["eM"] / (z["M_obs"] * LN10) for z in zz]
        Mbl = zz[0]["Mb_last"]; rh = rhalf_from([z["r_kpc"] for z in zz] + [Mbl[1]], [z["M_b"] for z in zz] + [Mbl[0]], Mbl[0]) * KPC
        pl = [pvars(gN[i], glaw(gN[i], a0) * 10 ** D[i], pts[i]["feat"]["Mb"], pts[i]["feat"]["r"], pts[i]["feat"]["depth"], a0) for i in range(len(pts))]
        v = agg(pl); v["r_rhalf"] = gmean([p["feat"]["r"] / rh for p in pts]); j = int(np.argmax([z["r_kpc"] for z in zz]))
        v["sigma"] = math.sqrt(G * zz[j]["M_obs"] * MS / (2 * zz[j]["r_kpc"] * KPC)) / 1e3
        v["x_e"] = None; v["f_gas"] = float(np.mean([p["feat"]["fgas"] for p in pts])); v["colour"] = None
        rows.append(dict(cls="X-COP", name=nm, gN=gN, b=[1.0] * len(gN), Dbar=float(np.mean(D)), shift=xs, sig=math.sqrt(sum(s * s for s in sl)) / len(sl),
                         vars=v, target=False, yN=float(np.mean([math.log10(pl[i]["gobs"] / gN[i]) for i in range(len(pts))]))))
    # groups at f* = 0.5
    G5 = NS["groups_pts"](a0, 0.5); gs = cell(f, "groups")["post"]["median"] - float(np.median([p["D"] for g in G5 for p in g["pts"]]))
    for g, gp in zip(G5, GR):
        assert g["name"] == gp["name"]; pts = g["pts"]
        gN = [p["feat"]["x"] * a0 for p in pts]; D = [p["D"] for p in pts]
        sl = math.log(gp["g5"] / gp["pts"][0]["M_gas"]) / math.log(gp["R5"] / gp["R25"])
        rh = gp["R25"] * (0.5 * gp["g5"] / gp["pts"][0]["M_gas"]) ** (1 / sl) * KPC
        pl = [pvars(gN[i], glaw(gN[i], a0) * 10 ** D[i], pts[i]["feat"]["Mb"], pts[i]["feat"]["r"], pts[i]["feat"]["depth"], a0) for i in range(2)]
        v = agg(pl); v["r_rhalf"] = gmean([p["feat"]["r"] / rh for p in pts])
        v["sigma"] = math.sqrt(gp["kT"] * 1.602176634e-16 / (0.6 * 1.67262192e-27)) / 1e3
        v["x_e"] = None; v["f_gas"] = 1 / 1.5; v["colour"] = None
        rows.append(dict(cls="groups", name=g["name"], gN=gN, b=[1.0, 1.0], Dbar=float(np.mean(D)), shift=gs,
                         sig=math.sqrt(sum(p["sl"] ** 2 for p in pts)) / 2, vars=v, target=False,
                         yN=float(np.mean([math.log10(pl[i]["gobs"] / gN[i]) for i in range(2)]))))
    # dSphs: bright M31 (SE2 A1 + A2 admissible) and LG field (target)
    DS = NS["dsphs"](f, a0); adm = SE2["footings"][f]["admissibility"]
    def dsph_row(cls, p, target):
        n = p["name"]; x1 = X1R[(f, n)]; ft = p["feat"]; Ms = 10 ** float(x1["logMstar"]); r = 4 / 3 * ft["r"]; gN = ft["x"] * a0
        pv = pvars(gN, glaw(gN, a0) * 10 ** p["D"], Ms / 2, r, tail_phi(Ms * MS, r, a0) / CC ** 2, a0)
        if not pv["depth"] > 0: pv["depth"] = None      # law field below QX5's cut at r_1/2: tail 0 -> NO VERDICT row (disclosed)
        lv = LVD.get(n, {}); mhi = (lv.get("mass_HI", "") or "").strip()
        MHI = 1.33 * 10 ** float(mhi) if mhi else 0.0
        pv.update(r_rhalf=1.0, sigma=ft["sigma"], x_e=ft["xe"], f_gas=MHI / (Ms + MHI), colour=None)
        return dict(cls=cls, name=n, gN=[gN], b=[1.0], Dbar=p["D"] - anchor, shift=0.0, sig=float(x1["sdMC[Newton]"]), vars=pv, target=target,
                    yN=math.log10(pv["gobs"] / gN))
    rem = set(adm["bright M31"]["removed_A1"]) | set(adm["bright M31"]["removed_A2"])
    bm = [dsph_row("bright M31", p, False) for p in DS["bright M31"] if p["name"] not in rem]
    bs = cell(f, "bright M31")["post"]["median"] - cell(f, "bright M31")["raw_stat_only"]["median"]
    for r_ in bm: r_["shift"] = bs
    rows += bm
    lg = [dsph_row("LG field", p, True) for p in DS["LG field"]]
    sL = float(np.sqrt(np.mean([r_["Dbar"] ** 2 for r_ in lg])))
    for r_ in lg: r_["sig"] = sL
    rows += lg
    # Coma UDGs (9; pericentre reading keeps tau x 3^(2/3) < 0.375 and A2)
    U = NS["udgs"](f, a0); ur = [r_ for r_ in UROWS if r_["footing"] == f]; ad = adm["Coma UDGs"]
    us = cell(f, "Coma UDGs")["post"]["median"] - cell(f, "Coma UDGs")["raw_stat_only"]["median"]
    assert len(U) == len(ur) == len(ad["tau"]) == 9
    for i, (p, r0) in enumerate(zip(U, ur)):
        if peri and not (ad["tau"][i] * PERI < TAU_LINE and ad["tc_to"][i] <= 0.1): continue
        ft = p["feat"]; Ms = float(r0["Mstar"]); r = ft["r"]; gN = ft["x"] * a0
        pv = pvars(gN, glaw(gN, a0) * 10 ** p["D"], Ms / 2, r, tail_phi(Ms * MS, r, a0) / CC ** 2, a0)
        pv.update(r_rhalf=1.0, sigma=ft["sigma"], x_e=ft["xe"], f_gas=0.0, colour=None)
        rows.append(dict(cls="Coma UDGs", name=r0["name"], gN=[gN], b=[1.0], Dbar=p["D"], shift=us, sig=float(r0["sE"]) / LN10, vars=pv,
                         target=False, yN=math.log10(pv["gobs"] / gN)))
    SYS = {"SPARC": 0.057 / 2, "ellipticals": sysw(f, "ellipticals"), "X-COP": sysw(f, "X-COP"), "groups": sysw(f, "groups"),
           "bright M31": sysw(f, "bright M31"), "Coma UDGs": sysw(f, "Coma UDGs"), "LG field": sysw(f, "LG field")}
    for r_ in rows:
        r_["sys"] = SYS[r_["cls"]]
        if r_["target"]: r_["y"] = 0.0; r_["J"] = jac(0.0, r_["gN"], r_["b"], a0)
        else: r_["y"] = y_of(r_["Dbar"] - r_["shift"], r_["gN"], r_["b"], a0); r_["J"] = jac(r_["Dbar"] - r_["shift"], r_["gN"], r_["b"], a0)
    return rows, dict(sigma_SPARC_exact=sS, sigma_LG=sL, sys=SYS, shifts=dict(X_COP=xs, groups=gs, bright_M31=bs, Coma_UDGs=us), anchor=anchor)

# ------------------------------------------------------------------ fitting machinery
def tr(name, x): return float(x) if name in LINEAR else math.log10(x)
def cov_blocks(rows, newton=False):
    idx = {}
    for i, r in enumerate(rows): idx.setdefault(r["cls"], []).append(i)
    W = {}
    for c, ii in idx.items():
        J = np.array([1.0 if newton else rows[i]["J"] for i in ii]); s = np.array([rows[i]["sig"] for i in ii]); sy = rows[ii[0]]["sys"]
        C = np.diag((J * s) ** 2) + np.outer(J * sy, J * sy); W[c] = (np.array(ii), C, np.linalg.inv(C))
    return W
def Wfull(n, W):
    M = np.zeros((n, n))
    for c, (ii, C, Wi) in W.items(): M[np.ix_(ii, ii)] = Wi
    return M
def qp(H, g, A):
    """min 1/2 t'Ht - g't  s.t.  A t >= 0; exact via the dual NNLS."""
    t0 = np.linalg.solve(H, g)
    if A is None or len(A) == 0 or np.all(A @ t0 >= -1e-10): return t0
    Hi = np.linalg.inv(H); Hi = 0.5 * (Hi + Hi.T); L = np.linalg.cholesky(Hi + 1e-15 * np.trace(Hi) / len(Hi) * np.eye(len(Hi)))
    M = L.T @ A.T; b = -np.linalg.solve(L, t0)
    try:
        lam = nnls(M, b, maxiter=max(500, 100 * A.shape[0]))[0]; t = t0 + Hi @ A.T @ lam
        if np.all(A @ t >= -1e-8 * max(1.0, np.abs(t).max())): return t
    except RuntimeError: pass
    # fallback: primal SLSQP from the dual-free start (same QP, same optimum)
    from scipy.optimize import minimize
    o = minimize(lambda t: 0.5 * t @ H @ t - g @ t, t0, jac=lambda t: H @ t - g, method="SLSQP",
                 constraints=[dict(type="ineq", fun=lambda t: A @ t, jac=lambda t: A)], options=dict(maxiter=2000, ftol=1e-14))
    return o.x
def score(y, yh, W):
    r = y - yh; chi = 0.0; cls = {}
    for c, (ii, C, Wi) in W.items():
        rc = r[ii]; chi += float(rc @ Wi @ rc); one = np.ones(len(ii)); s1 = float(one @ Wi @ one)
        rb = float(one @ Wi @ rc) / s1; sc = 1 / math.sqrt(s1); cls[c] = dict(n=len(ii), rbar=rb, sigma=sc, z=rb / sc)
    return chi, cls
def fit_iso(u, v, y, Wf, so):
    uu, vv = so[0] * u, so[1] * v; keys = {}; node = np.zeros(len(u), int)
    for i, kk in enumerate(zip(np.round(uu, 10), np.round(vv, 10))): node[i] = keys.setdefault(kk, len(keys))
    k = len(keys); Pm = np.zeros((len(u), k)); Pm[np.arange(len(u)), node] = 1.0
    nu = np.array([kk[0] for kk in keys]); nv = np.array([kk[1] for kk in keys])
    dom = (nu[:, None] <= nu[None, :]) & (nv[:, None] <= nv[None, :]); np.fill_diagonal(dom, False)
    di = dom.astype(np.int32); red = dom & ~((di @ di) > 0)
    ei, ej = np.nonzero(red); A = np.zeros((len(ei), k)); A[np.arange(len(ei)), ej] = 1.0; A[np.arange(len(ei)), ei] = -1.0
    H = Pm.T @ Wf @ Pm; g = Pm.T @ Wf @ y
    return Pm @ qp(H, g, A), dict(nodes=k, edges=int(len(ei)))
def fit_quad(u, v, y, Wf, so):
    su, sv = (u.std() or 1.0), (v.std() or 1.0); a = (u - u.mean()) / su; b = (v - v.mean()) / sv
    X = np.stack([np.ones_like(a), a, b, a * a, b * b, a * b], 1)
    H = X.T @ Wf @ X; H = H + 1e-10 * np.trace(H) / 6 * np.eye(6); g = X.T @ Wf @ y
    s1, s2 = so; Z = np.zeros_like(a)
    A = np.concatenate([np.stack([Z, s1 + Z, Z, 2 * s1 * a, Z, s1 * b], 1), np.stack([Z, Z, s2 + Z, Z, 2 * s2 * b, s2 * a], 1)])
    # gradients are linear in (a, b): sign constraints at every row hold iff they hold at the rows on the convex hull
    try:
        from scipy.spatial import ConvexHull
        hv = np.unique(ConvexHull(np.stack([a, b], 1)).vertices); Ah = np.concatenate([A[hv], A[len(a) + hv]])
    except Exception:
        Ah = A
    beta = qp(H, g, Ah); gr = A @ beta
    return X @ beta, dict(coef=[float(x) for x in beta], monotone=bool(np.all(gr >= -1e-8)), min_grad=float(gr.min()))
def fit_grid6(u, v, y, Wf, so):
    """A2: monotone bilinear surface on a 2 x 3 or 3 x 2 knot grid (6 free numbers); best of the two shapes."""
    best = None
    for shape in ((2, 3), (3, 2)):
        ku = np.unique(np.quantile(u, [0, 0.5, 1]) if shape[0] == 3 else np.array([u.min(), u.max()]))
        kv = np.unique(np.quantile(v, [0, 0.5, 1]) if shape[1] == 3 else np.array([v.min(), v.max()]))
        nu_, nv_ = len(ku), len(kv); X = np.zeros((len(u), nu_ * nv_))
        def w1(k, x):
            if len(k) == 1: return np.ones((len(x), 1))
            i = np.clip(np.searchsorted(k, x, side="right") - 1, 0, len(k) - 2); t = np.clip((x - k[i]) / (k[i + 1] - k[i]), 0, 1)
            W_ = np.zeros((len(x), len(k))); W_[np.arange(len(x)), i] = 1 - t; W_[np.arange(len(x)), i + 1] += t; return W_
        Wu, Wv = w1(ku, u), w1(kv, v)
        for i in range(nu_):
            for j in range(nv_): X[:, i * nv_ + j] = Wu[:, i] * Wv[:, j]
        A = []
        for i in range(nu_ - 1):
            for j in range(nv_):
                a = np.zeros(nu_ * nv_); a[(i + 1) * nv_ + j] = so[0]; a[i * nv_ + j] = -so[0]; A.append(a)
        for i in range(nu_):
            for j in range(nv_ - 1):
                a = np.zeros(nu_ * nv_); a[i * nv_ + j + 1] = so[1]; a[i * nv_ + j] = -so[1]; A.append(a)
        A = np.array(A) if A else None
        H = X.T @ Wf @ X; H = H + 1e-12 * np.trace(H) / len(H) * np.eye(len(H)); g = X.T @ Wf @ y
        t = qp(H, g, A); yh = X @ t; r = y - yh; c2 = float(r @ Wf @ r)
        mono = bool(A is None or np.all(A @ t >= -1e-8))
        if best is None or c2 < best[0]: best = (c2, yh, dict(shape=list(shape), knots_u=ku.tolist(), knots_v=kv.tolist(), values=t.tolist(), monotone=mono))
    return best[1], best[2]
FITS = {"grid6": fit_grid6, "quadratic": fit_quad}          # gating (A2)
REPORTED = {"isotonic_free": fit_iso}                       # reported only (A2)

def fit_pair(rows, pair, newton=False, drop=None, yover=None, report=False):
    """all orientations, both families; returns per family the best orientation and the line verdict."""
    keep = [i for i, r in enumerate(rows) if r["vars"][pair[0]] is not None and r["vars"][pair[1]] is not None and r["cls"] != drop]
    present = sorted({rows[i]["cls"] for i in keep}); need = [c for c in CLASSES if c != drop]
    nv = [c for c in need if c not in present]
    R = [rows[i] for i in keep]; W = cov_blocks(R, newton); Wf = Wfull(len(R), W)
    y = np.array([(r["yN"] if newton else r["y"]) for r in R]) if yover is None else np.asarray(yover)[keep]
    u = np.array([tr(pair[0], r["vars"][pair[0]]) for r in R]); v = np.array([tr(pair[1], r["vars"][pair[1]]) for r in R])
    out = {}
    for fam, fn in (dict(FITS, **REPORTED) if report else FITS).items():
        best = None
        for so in ORIENT:
            yh, info = fn(u, v, y, Wf, so); chi, cls = score(y, yh, W); N = len(R)
            worst = max(cls, key=lambda c: abs(cls[c]["z"]))
            mono = info.get("monotone", True)
            ok_line = bool(chi / N <= 2 and all(abs(x["z"]) <= 2 for x in cls.values()) and mono)
            rec = dict(orient=list(so), chi2=chi, N=N, chi2N=chi / N, worst_class=worst, worst_z=cls[worst]["z"], monotone=mono,
                       line_on_present=ok_line, classes={c: dict(n=x["n"], z=x["z"], rbar=x["rbar"], sigma=x["sigma"]) for c, x in cls.items()})
            if best is None or (rec["line_on_present"], -rec["chi2N"]) > (best["line_on_present"], -best["chi2N"]): best = rec
        best["no_verdict_classes"] = nv; best["carries"] = bool(best["line_on_present"] and not nv)
        out[fam] = best
    return out

# ------------------------------------------------------------------ checkpoint
CK = json.load(open(CKPT)) if os.path.exists(CKPT) else {}
def ck_get(key, fn):
    if key in CK: return CK[key]
    v = fn(); CK[key] = v
    if STOP["flag"]:
        json.dump(CK, open(CKPT, "w")); P(f"SIGTERM: checkpoint written ({len(CK)} fits); exit 3"); sys.exit(3)
    if len(CK) % 200 == 0: json.dump(CK, open(CKPT, "w"))
    return v
def pkey(*a): return "|".join(str(x) for x in a)

def search(rows, f, tagr, newton=False, loo=True):
    tab = {}
    for pr in PAIRS:
        tab["+".join(pr)] = ck_get(pkey(tagr, f, "+".join(pr), "all"), lambda: fit_pair(rows, pr, newton, report=not MUT))
    loo_t = {}
    if loo:
        for c in CLASSES:
            loo_t[c] = {"+".join(pr): ck_get(pkey(tagr, f, "+".join(pr), "drop", c), lambda: fit_pair(rows, pr, newton, drop=c)) for pr in PAIRS}
    return tab, loo_t

def best_pair(tab):
    cand = [(k, fam, v[fam]) for k, v in tab.items() for fam in FITS if not v[fam]["no_verdict_classes"]]
    k, fam, r = min(cand, key=lambda t: t[2]["chi2N"])                     # lowest chi2/N among pairs with every class present
    return dict(pair=k, family=fam, chi2N=r["chi2N"], worst_class=r["worst_class"], worst_z=r["worst_z"], orient=r["orient"],
                carries_line=r["line_on_present"], classes=r["classes"])
def best_by_max(tab):
    """the pair closest to the line by the larger of chi2/N / 2 and max|z| / 2 (reported)."""
    cand = [(k, fam, v[fam]) for k, v in tab.items() for fam in FITS if not v[fam]["no_verdict_classes"]]
    k, fam, r = min(cand, key=lambda t: max(t[2]["chi2N"] / 2, abs(t[2]["worst_z"]) / 2))
    return dict(pair=k, family=fam, chi2N=r["chi2N"], worst_class=r["worst_class"], worst_z=r["worst_z"], orient=r["orient"], score=max(r["chi2N"] / 2, abs(r["worst_z"]) / 2))

def carriers(tab, loo_t, foot_tabs=None):
    out = []
    for k, v in tab.items():
        for fam in FITS:
            if v[fam]["carries"] and all(loo_t[c][k][fam]["line_on_present"] for c in CLASSES): out.append((k, fam))
    return out

# ------------------------------------------------------------------ KA
def ka(f, a0):
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
    st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / LN10
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=NS["udgs"](f, a0), D=NS["dsphs"](f, a0), sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    o = {}
    # KA3: GB1 L0 class means
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d3 = max(abs(cm[k] - NS["KA20"][f][k]) for k in cm); o["KA3"] = dict(maxdiff=float(d3), ok=bool(d3 <= 1e-6))
    # KA1: KD1's diagnostic, its own procedure, on GB1's battery
    def U_(fr): return lambda ft: dict(b=1.0 + fr, F=1.0, T=0.0)
    lo, hi = 0.0, 10.0
    for _ in range(60):
        m_ = 0.5 * (lo + hi); lo, hi = (m_, hi) if NS["g_sparc"](U_(m_), B, a0)[0] else (lo, m_)
    diag = dict(SPARC_f_max=lo)
    def need_f(meanfn):
        g = lambda lf: meanfn(U_(10 ** lf))
        try: return 10 ** brentq(g, -4, 4)
        except ValueError: return None
    diag["Xcop_f_need"] = need_f(lambda c: NS["g_xcop"](c, B, a0)[1]["mean"])
    diag["ell_f_need"] = need_f(lambda c: NS["g_ell"](c, B, a0)[1]["mean"])
    diag["udg_f_need"] = need_f(lambda c: NS["g_udg"](c, B, a0)[1]["mean"])
    for fst in (0, 1):
        diag[f"groups_fst{fst}_f_need"] = need_f(lambda c: float(np.mean([p["D"] - delta(c, p["feat"], a0) for g in B["GR"][fst] for p in g["pts"]])))
    for cls in ("bright M31", "MW classical"):
        diag[f"dsph_{cls}_f_need"] = need_f(lambda c: float(np.median([p["D"] - delta(c, p["feat"], a0) for p in B["D"][cls]])))
    ref = KD1["footings"][f]["uniform_f_diag"]; d1 = {k: abs(v / ref[k] - 1) for k, v in diag.items() if v is not None and ref.get(k)}
    o["KA1"] = dict(values=diag, kd1={k: ref[k] for k in diag}, max_rel=float(max(d1.values())), ok=bool(max(d1.values()) <= 1e-9 and len(d1) == len(diag)))
    # KA2: this lane's inversion on pooled classes
    k2 = {}
    k2["Xcop"] = 10 ** y_of(float(np.mean([p["D"] for p in X])), [p["feat"]["x"] * a0 for p in X], [1.0] * len(X), a0) - 1
    k2["ell"] = 10 ** y_of(float(np.mean([p["D"] for p in E])), [p["feat"]["x"] * a0 for p in E], [1.0] * len(E), a0) - 1
    k2["udg"] = 10 ** y_of(float(np.mean([p["D"] for p in B["U"]])), [p["feat"]["x"] * a0 for p in B["U"]], [1.0] * len(B["U"]), a0) - 1
    rr = {"Xcop": diag["Xcop_f_need"], "ell": diag["ell_f_need"], "udg": diag["udg_f_need"]}
    d2 = max(abs(k2[k] / rr[k] - 1) for k in k2); o["KA2"] = dict(values=k2, max_rel=float(d2), ok=bool(d2 <= 1e-6))
    return o

def planted(rows, noise_seed=None):
    u0 = np.array([math.log10(r["vars"]["gN"]) for r in rows]); v0 = np.array([math.log10(r["vars"]["sigma"]) for r in rows])
    yp = 0.5 + 0.4 * (u0 - u0.mean()) / u0.std() - 0.3 * (v0 - v0.mean()) / v0.std()
    if noise_seed is not None:
        rng = np.random.default_rng(noise_seed); W = cov_blocks(rows)
        for c, (ii, C, Wi) in W.items(): yp[ii] += rng.multivariate_normal(np.zeros(len(ii)), C)
    return yp

def rss_gb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ main
ROWS = {}
for f, a0 in A0.items():
    rows, meta = build_rows(f, a0); ROWS[f] = rows
    FO = dict(meta=meta, rows=[dict(cls=r["cls"], name=r["name"], y=r["y"], f=10 ** r["y"] - 1, yN=r["yN"], J=r["J"], sig_dex=r["sig"], sys_dex=r["sys"],
                                    Dbar=r["Dbar"], shift=r["shift"], vars=r["vars"]) for r in rows])
    cnt = {c: sum(1 for r in rows if r["cls"] == c) for c in CLASSES}; FO["counts"] = cnt
    P(f"[{f}] rows: " + ", ".join(f"{c} {n}" for c, n in cnt.items()) + f"; SPARC exact-field sigma {meta['sigma_SPARC_exact']:.4f} dex, LG field sigma {meta['sigma_LG']:.4f} dex")
    for c in CLASSES:
        ys = [r["y"] for r in rows if r["cls"] == c]
        P(f"[{f}]   {c:12s} y = log10(1+f): median {np.median(ys):+.3f} (f {10**np.median(ys)-1:+.3f}), range [{min(ys):+.3f}, {max(ys):+.3f}]; sigma_sys {meta['sys'][c]:.4f} dex")
    nvc = {v: sorted({r['cls'] for r in rows if r['vars'][v] is None}) for v in VARS}
    FO["variable_missing_classes"] = nvc
    P(f"[{f}]   NO VERDICT variable x class: " + "; ".join(f"{v}: {', '.join(c)}" for v, c in nvc.items() if c))
    RES["footings"][f] = FO

if "--rows-only" in sys.argv: sys.exit(0)                          # debug: rows only, nothing written
if not MUT:
    kaok = True
    for f, a0 in A0.items():
        o = ka(f, a0); RES["KA"][f] = o; kaok &= all(x["ok"] for x in o.values())
        P(f"[{f}] KA1 KD1 f table: " + ", ".join(f"{k.replace('_f_need','').replace('_f_max',' max')} {v:.4g}" for k, v in o["KA1"]["values"].items())
          + f"; max rel diff {o['KA1']['max_rel']:.1e} -> {'PASS' if o['KA1']['ok'] else 'FAIL'}")
        P(f"[{f}] KA2 pooled inversion vs KD1: max rel {o['KA2']['max_rel']:.1e} -> {'PASS' if o['KA2']['ok'] else 'FAIL'}")
        P(f"[{f}] KA3 GB1 L0 class means max|d| {o['KA3']['maxdiff']:.1e} -> {'PASS' if o['KA3']['ok'] else 'FAIL'}")
        # KA4 planted, noiseless (gating)
        rows = ROWS[f]; yp = planted(rows); pr = ("gN", "sigma")
        full = fit_pair(rows, pr, yover=yp); lo_ = {c: fit_pair(rows, pr, drop=c, yover=yp) for c in CLASSES}
        ok4 = all(full[fam]["carries"] and all(lo_[c][fam]["line_on_present"] for c in CLASSES) for fam in FITS)
        o["KA4"] = dict(full={fam: dict(chi2N=full[fam]["chi2N"], worst_z=full[fam]["worst_z"], carries=full[fam]["carries"]) for fam in FITS}, ok=bool(ok4))
        kaok &= ok4
        P(f"[{f}] KA4 planted (g_N, sigma) noiseless: " + ", ".join(f"{fam} chi2/N {full[fam]['chi2N']:.2e} carries {full[fam]['carries']}" for fam in FITS)
          + f", all LOO -> {'PASS' if ok4 else 'FAIL'}")
        # KA4n reported: noisy plant, seeds 1-20
        share = {fam: 0 for fam in FITS}
        for sd in range(1, 21):
            r_ = fit_pair(rows, pr, yover=planted(rows, sd))
            for fam in FITS: share[fam] += int(r_[fam]["carries"])
        o["KA4n_share_of_20"] = share
        P(f"[{f}] KA4n (reported) noisy plant carries in {share['grid6']}/20 grid6, {share['quadratic']}/20 quadratic seeds")
    RES["KA_all"] = bool(kaok)
    if not kaok:
        RES["label"] = "NO VERDICT (KA FAIL)"; P("KA FAIL: nothing graded.")
    else:
        for reading in ("main", "pericentre"):
            per = {}
            for f, a0 in A0.items():
                rows = ROWS[f] if reading == "main" else build_rows(f, a0, peri=True)[0]
                if reading == "pericentre":
                    RES["footings"][f]["pericentre_UDG_rows"] = [r["name"] for r in rows if r["cls"] == "Coma UDGs"]
                tab, loo_t = search(rows, f, reading)
                per[f] = (tab, loo_t)
                bp = best_pair(tab); bm = best_by_max(tab)
                nl = sum(1 for k, v in tab.items() for fam in FITS if v[fam]["carries"])
                np_ = sum(1 for k, v in tab.items() for fam in FITS if v[fam]["line_on_present"])
                P(f"[{f}] {reading}: pairs x families carrying (all classes) {nl}; passing on present classes only {np_} of {2*len(PAIRS)}")
                P(f"[{f}] {reading}: best pair (lowest chi2/N, all classes) {bp['pair']} [{bp['family']}, orient {bp['orient']}]: chi2/N {bp['chi2N']:.3f}; worst class {bp['worst_class']} z {bp['worst_z']:+.2f}")
                P(f"[{f}] {reading}: closest to the line (max(chi2/N/2, |z|max/2)) {bm['pair']} [{bm['family']}]: chi2/N {bm['chi2N']:.3f}, worst {bm['worst_class']} z {bm['worst_z']:+.2f} (score {bm['score']:.2f}, 1 passes)")
                lt = {c: sum(1 for k in tab for fam in FITS if loo_t[c][k][fam]["line_on_present"] and not loo_t[c][k][fam]["no_verdict_classes"]) for c in CLASSES}
                iso = [(k, v["isotonic_free"]) for k, v in tab.items() if not v["isotonic_free"]["no_verdict_classes"]]
                ni = sum(1 for k, v in iso if v["line_on_present"])
                P(f"[{f}] {reading}: (reported, A2) free isotonic passes the line on {ni} of {len(iso)} all-class pairs (antichain freedom; not gating)")
                P(f"[{f}] {reading}: leave-one-class-out, pair-families passing the line on the rest: " + ", ".join(f"-{c} {n}" for c, n in lt.items()))
                bl = {c: best_pair(loo_t[c]) for c in CLASSES}
                for c in CLASSES:
                    P(f"[{f}] {reading}:    drop {c:12s} best {bl[c]['pair']} [{bl[c]['family']}] chi2/N {bl[c]['chi2N']:.3f}, worst {bl[c]['worst_class']} z {bl[c]['worst_z']:+.2f}")
                bpl = {c: loo_t[c][bp["pair"]][bp["family"]] for c in CLASSES}
                RES["footings"][f][reading] = dict(table=tab, loo_pass_counts=lt, best_pair=bp, closest=bm, loo_best=bl,
                                                  best_pair_loo={c: dict(chi2N=v["chi2N"], worst_class=v["worst_class"], worst_z=v["worst_z"], line=v["line_on_present"]) for c, v in bpl.items()})
                RES["footings"][f][reading + "_loo_full"] = {c: {k: {fam: dict(chi2N=v[fam]["chi2N"], worst_z=v[fam]["worst_z"], line=v[fam]["line_on_present"], nv=v[fam]["no_verdict_classes"]) for fam in FITS} for k, v in loo_t[c].items()} for c in CLASSES}
                print(f"  [rss {rss_gb():.3f} GB, {time.time()-T_START:.0f} s]", flush=True)
            # carriers: same family, both footings, all classes, all LOO
            car = None
            for f in A0:
                tab, loo_t = per[f]; s = set(carriers(tab, loo_t)); car = s if car is None else car & s
            RES[reading + "_carriers"] = sorted(car)
            P(f"{reading}: pairs carrying on both footings, every class, every leave-one-out: {sorted(car) if car else 'none'}")
        lm = ("PAIR FOUND: " + ", ".join(f"{k} [{fam}]" for k, fam in RES["main_carriers"])) if RES["main_carriers"] else "NO PAIR"
        lp = ("PAIR FOUND: " + ", ".join(f"{k} [{fam}]" for k, fam in RES["pericentre_carriers"])) if RES["pericentre_carriers"] else "NO PAIR"
        RES["label_main"] = lm; RES["label_pericentre"] = lp
        RES["label_pending_mutate"] = lm if lm == lp else f"{lm} (main) / {lp} (pericentre UDG reading)"
        P(f"LABEL (before MUTATE): {RES['label_pending_mutate']}")
else:
    MJ = dict()
    for f, a0 in A0.items():
        rows = ROWS[f]
        # M1 shuffled class labels: permute the variable vectors across rows
        perm = np.random.default_rng(3).permutation(len(rows)); sh = [dict(r) for r in rows]
        for i, j in enumerate(perm): sh[i]["vars"] = rows[j]["vars"]
        t1, _ = search(sh, f, "M1", loo=False)
        n1 = sum(1 for v in t1.values() for fam in FITS if v[fam]["carries"]); b1 = best_pair(t1)
        # M2 Newtonian f (law off)
        t2, l2 = search(rows, f, "M2", newton=True)
        n2 = len(carriers(t2, l2)); b2 = best_pair(t2)
        MJ[f] = dict(M1=dict(n_carry=n1, best=b1, bites=bool(n1 == 0)), M2=dict(n_carry_with_loo=n2, n_carry_full=sum(1 for v in t2.values() for fam in FITS if v[fam]["carries"]), best=b2, bites=bool(n2 == 0)),
                     M1_table=t1, M2_table=t2)
        P(f"[{f}] M1 shuffled: {n1} pair-families carry; best {b1['pair']} [{b1['family']}] chi2/N {b1['chi2N']:.3f}, worst {b1['worst_class']} z {b1['worst_z']:+.2f} -> {'BITES' if n1 == 0 else 'NO BITE'}")
        P(f"[{f}] M2 Newtonian f: {MJ[f]['M2']['n_carry_full']} carry on the full set, {n2} also through every leave-one-out; best {b2['pair']} [{b2['family']}] chi2/N {b2['chi2N']:.3f}, worst {b2['worst_class']} z {b2['worst_z']:+.2f} -> {'BITES' if n2 == 0 else 'NO BITE'}")
        print(f"  [rss {rss_gb():.3f} GB, {time.time()-T_START:.0f} s]", flush=True)
    RES["mutate"] = MJ
    RES["MUTATE_bites"] = bool(all(MJ[f]["M1"]["bites"] and MJ[f]["M2"]["bites"] for f in A0))
    P(f"MUTATE M1 + M2: {'BITE on both footings' if RES['MUTATE_bites'] else 'DO NOT BITE'}")

RES["peak_rss_GB"] = rss_gb(); RES["wall_s"] = time.time() - T_START
P(f"peak RSS {RES['peak_rss_GB']:.3f} GB; wall {RES['wall_s']:.0f} s. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=0, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
if os.path.exists(CKPT): os.remove(CKPT)
