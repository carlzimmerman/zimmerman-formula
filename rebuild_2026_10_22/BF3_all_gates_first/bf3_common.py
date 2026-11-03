#!/usr/bin/env python3
"""BF3 shared: data, gates cheap and exact, closure, RQ3 loader. Criteria FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, pickle, sys, types
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
np.seterr(all="ignore")
LANE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(LANE); REPO = os.path.dirname(RB); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); CRG = os.path.join(RB, "CRG1_clean_room_regrade"); BF1 = os.path.join(RB, "BF1_exhaustive_law_search"); CACHE = os.path.join(LANE, "cache"); os.makedirs(CACHE, exist_ok=True)
MUT = os.environ.get("BF3_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; HMUT = 1.5 if MUT else 1.0
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); C = 299792458.0
S_LENS = 0.125; L_ABS = 56 + 2 * math.sqrt(112); L_DELTA = 2 * math.sqrt(112); GF = (0.3, 0.6); GFALL = (0.3, 0.6, 0.85)
SEEDS = dict(c1=20261102, c2=1, c3=2)
FN = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi)
def H_of(s, y, ell, f, fam):
    """s is T for family A, H otherwise."""
    T = eval(s, {"__builtins__": {}}, dict(FN, y=y, ell=ell, f=f)) * np.ones_like(y + f)
    return HMUT * ((1 + f * T) if fam in ("A", "E") else T)
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def wrap(w, g, a, H): return law(g, a * H) if w == 1 else law(g * H, a) if w == 2 else law(g, a) * H
# ---------- RQ3 read-only, outputs in this lane (BF2's pattern)
_M = {}
def rq3():
    if "A" in _M: return _M["A"]
    p = os.path.join(RQ3, "acceptance.py"); s = open(p).read(); W = LANE
    for d in ("p", "c"): os.makedirs(os.path.join(W, "cache_crg", d), exist_ok=True)
    SUBS = [('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {W!r}; RB = {RB!r}'), ('TOL = json.load(open(os.path.join(HERE, "tolerances.json")))', f'TOL = json.load(open(os.path.join({RQ3!r}, "tolerances.json")))'), ('MARKS = J(HERE, "row_marks.json")', f'MARKS = J({RQ3!r}, "row_marks.json")')]
    for a, b in SUBS:
        assert s.count(a) >= 1, a; s = s.replace(a, b, 1)
    s = s.split('if __name__ == "__main__":')[0]; m = types.ModuleType("rq3acc"); m.__file__ = p; sys.modules["rq3acc"] = m; sys.path.insert(0, RQ3); exec(compile(s, p, "exec"), m.__dict__); _M["A"] = m; return m
def mods():
    A = rq3(); A.crg(); import crg1_lens as Le, crg1_groups as Gr, crg1_sparc as Cs; return A, Le, Gr, Cs
# ---------- X-COP, RQ3 rows_xcop arithmetic
def xcop_rows():
    from astropy.io import fits
    Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16; D = os.path.join(REPO, "real_research", "data", "xcop"); out = []
    li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    names = sorted(n for n in os.listdir(D) if os.path.isdir(os.path.join(D, n)) and os.path.exists(os.path.join(D, n, f"{n}_mstar.fits")))
    for j, name in enumerate(names):
        p = os.path.join(D, name)
        with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (.1, .2, .3, .5, .7):
            r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
            if np.all(np.isfinite([mh, mg, ms])):
                R = r * 1e3 * PCm; u = Gm * MSm / R ** 2; out.append((u * (mg + ms), u * mg, R, math.log10(u * mh), j))
    return np.array(out)
# ---------- cheap-path geometry, footing free, cached
LM_NODES = np.array([7.0, 8.0, 9.0, 9.5, 10.0, 10.3, 10.6, 10.8, 11.0, 11.2, 11.5, 11.8]); R_NODES = np.unique(np.r_[np.logspace(3, 9, 37), 1e5]); X_NODES = np.logspace(-2.5, 2.5, 16)
def geom():
    P = os.path.join(CACHE, "geom.pkl")
    if os.path.exists(P): return pickle.load(open(P, "rb"))
    A, Le, Gr, Cs = mods(); L = Le.load(); st = Le.Stencil(L["Rn"] * 1e6); TH = Le.TwoHalo(L); rex = [.343, .442, .433, .429]; T0 = np.array([TH.esd2h(L["R"][b], rex[b]) * Le.FF for b in range(4)])
    lr = np.log(R_NODES); hats = [np.interp(Le.LR, lr, np.eye(len(lr))[k]) for k in range(len(lr))]
    Wm = np.array([np.interp(Le.LMG, LM_NODES, np.eye(len(LM_NODES))[a]) for a in range(len(LM_NODES))]); na, nk = len(LM_NODES), len(lr); Pm = np.zeros((60, na, nk)); tab = np.zeros((len(Le.LMG), nk, 60))
    for i, lm in enumerate(Le.LMG):
        MB, _ = Le.baryon(float(lm))
        for k in range(nk): tab[i, k] = st.dsig(MB * hats[k], "linear")
    for a in range(na):
        for k in range(nk): Pm[:, a, k] = Le.stack(L, Wm[a][:, None] * tab[:, k, :])
    gbL, ggL, rL = [], [], []; SIk = 1e6 / 3.0857e16
    for lm in LM_NODES:
        MB, _ = Le.baryon(float(lm)); mb = np.exp(np.interp(lr, Le.LR, np.log(MB))); gbL.append(Le.Gpc * mb / R_NODES ** 2 * SIk); ggL.append(Le.Gpc * (mb - 10 ** float(lm)) / R_NODES ** 2 * SIk); rL.append(R_NODES * 3.0857e16)
    P_ = Gr.P; rows = Gr.load(); lx = np.log(X_NODES); hx = np.array([np.interp(Gr.LX, lx, np.eye(len(lx))[k]) for k in range(len(lx))]); WX = np.array([np.trapz(4 * math.pi * Gr.XG ** 2 * Gr.RHO_H * Gr.XG * Gr.gN_t * Gr.XG * hx[k], Gr.LX) for k in range(len(lx))]); gnt = np.exp(np.interp(lx, Gr.LX, np.log(Gr.gN_t)))
    gbG, rG, WG, ls = [], [], [], []
    for sg, lM, Re in rows:
        a = Re * (P_.pc * 1e3) / 1.8153; Mb = 10 ** lM * P_.Msun; U = P_.G * Mb / a ** 2; gbG.append(gnt * U); rG.append(X_NODES * a); WG.append(WX * P_.G * Mb / a / 3); ls.append(sg)
    o = dict(T0=T0, Pm=Pm.reshape(60, -1), gbL=np.array(gbL).ravel(), ggL=np.array(ggL).ravel(), rL=np.array(rL).ravel(), gbG=np.array(gbG).ravel(), rG=np.array(rG).ravel(), WG=np.array(WG), ls=np.array(ls), Yn=L["Yn"].ravel(), Cn=L["Cn"])
    pickle.dump(o, open(P + ".tmp", "wb")); os.replace(P + ".tmp", P); return o
def whiten(Y, Cn, T0, Pm, s):
    from scipy.linalg import cholesky, solve_triangular
    C_ = Cn + s * s * np.outer(Y, Y) if s else Cn; Lc = cholesky(C_, lower=True); Af = np.zeros((60, 4))
    for b in range(4): Af[15 * b:15 * (b + 1), b] = T0[b]
    A = solve_triangular(Lc, Af, lower=True); Q, _ = np.linalg.qr(A, mode="complete"); U = Q[:, 4:]
    return U.T @ solve_triangular(Lc, Y, lower=True), U.T @ solve_triangular(Lc, Pm, lower=True)
# ---------- grid of cheap-path vectors for a footing and arm
PROBE_Y = np.geomspace(1e-5, 1e7, 49); PROBE_E = (1e-12, 1e-6, 1e-2)
class Rows:
    """Layout of V: X 35 | lens | groups f .3 | groups f .6 | f=0 probes."""
    def __init__(s, foot, arm="real"):
        g = geom(); s.foot = foot; s.arm = arm; a = s.a0 = A0[foot]; X = xcop_rows(); s.gbX, s.ggX, s.rX, s.obsX, s.cl = X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4].astype(int); s.nX = len(X)
        yx, fx, ex = s.gbX / a, np.clip(s.ggX / s.gbX, 0, 1), s.rX * a / C ** 2
        if arm in SEEDS:
            p = np.random.default_rng(SEEDS[arm]).permutation(s.nX); yx, fx, ex = yx[p], fx[p], ex[p]
        s.gbL, s.gbG = g["gbL"], g["gbG"]; yl, fl, el = s.gbL / a, np.clip(g["ggL"] / s.gbL, 0, 1), g["rL"] * a / C ** 2; yg, eg = s.gbG / a, g["rG"] * a / C ** 2
        y0 = np.tile(PROBE_Y, len(PROBE_E)); e0 = np.repeat(PROBE_E, len(PROBE_Y))
        s.y = np.r_[yx, yl, yg, yg, y0]; s.ell = np.r_[ex, el, eg, eg, e0]; s.f = np.r_[fx, fl, yg * 0 + GF[0], yg * 0 + GF[1], y0 * 0]
        nl, ng = len(yl), len(yg); s.sX = slice(0, s.nX); s.sL = slice(s.nX, s.nX + nl); s.sG0 = slice(s.nX + nl, s.nX + nl + ng); s.sG1 = slice(s.nX + nl + ng, s.nX + nl + 2 * ng); s.sP = slice(s.nX + nl + 2 * ng, len(s.y)); s.ng = ng; s.W = g["WG"]; s.ls = g["ls"].copy()
        s.Yn = g["Yn"].copy(); s.T0 = g["T0"]; s.Pm = g["Pm"]; s.Cn = g["Cn"]; s.yw, s.Mw = whiten(s.Yn, s.Cn, s.T0, s.Pm, S_LENS)
        Sb = sparc_sub(a); s.nEV = np.r_[np.arange(s.nX), np.arange(s.sL.start, s.sL.stop), np.arange(s.sG1.start, s.sG1.stop, 16)]; s.sub = Sb
    def planted(s, Hfn, w):
        """Every target generated from a known H. Cheap vectors from the same map; exact path rebuilt in Exact."""
        a = s.a0; Hx = Hfn(s.y[s.sX], s.ell[s.sX], s.f[s.sX]); s.obsX = np.log10(wrap(w, s.gbX, a, Hx))
        Hl = Hfn(s.y[s.sL], s.ell[s.sL], s.f[s.sL]); s.Yn = s.Pm @ (wrap(w, s.gbL, a, Hl) / s.gbL); s.yw, s.Mw = whiten(s.Yn, s.Cn, s.T0, s.Pm, S_LENS)
        Hg = Hfn(s.y[s.sG1], s.ell[s.sG1], s.f[s.sG1]); bg = (wrap(w, s.gbG, a, Hg) / s.gbG).reshape(63, len(X_NODES)); s.ls = .5 * np.log10((bg * s.W).sum(1)) - 3
def sparc_sub(a):
    P = os.path.join(CACHE, f"sub_{a:.4e}.npy")
    if os.path.exists(P): return np.load(P)
    A, Le, Gr, Cs = mods(); G = Cs.load_gal(); o = []
    for g in G:
        gb = Cs.gB_mat(g)[20]; gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; ok = gb > 0
        o.append(np.c_[gb[ok] / a, g["R"][ok] * a / C ** 2, np.clip(gg[ok] / gb[ok], 0, 1)])
    o = np.vstack(o); o = o[np.random.default_rng(20261102).choice(len(o), 240, replace=False)]; np.save(P, o); return o
# ---------- closure, BF1's logic on this lane's rows
U = dict(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x)
B = {"+": np.add, "-": np.subtract, "*": np.multiply, "/": np.divide}
def tree(s, y, ell, f): return eval(s, {"__builtins__": {}}, dict(FN, y=y, ell=ell, f=f)) * np.ones_like(y + f)
def closure(R, levels, cap):
    y = np.r_[R.y[R.nEV], R.sub[:, 0]]; e = np.r_[R.ell[R.nEV], R.sub[:, 1]]; f = np.r_[R.f[R.nEV], R.sub[:, 2]]
    L0 = [("y", 1), ("ell", 1), ("f", 1), ("1.0", 1), ("2.0", 1), ("0.5", 1), ("pi", 1)]; seen = set()
    def add(s, n, v, out):
        if not np.all(np.isfinite(v)) or np.max(np.abs(v)) > 1e30: return
        k = np.round(v / (np.abs(v).max() + 1e-300), 9).tobytes() + np.float64(np.round(np.log(np.abs(v).max() + 1e-300), 6)).tobytes()
        if k in seen: return
        seen.add(k); out.append((s, n, v))
    L = []
    for s, n in L0: add(s, n, tree(s, y, e, f), L)
    prev = list(L); sets = [list(L)]
    for level in levels:
        new = []; pool_ = [t for st in sets for t in st]
        for s, n, v in prev:
            for u, fn in U.items(): add(f"{u}({s})", n + 1, fn(v), new)
        for s1, n1, v1 in prev:
            for s2, n2, v2 in pool_:
                for o, fn in B.items():
                    add(f"({s1}{o}{s2})", n1 + n2 + 1, fn(v1, v2), new)
                    if o in "-/": add(f"({s2}{o}{s1})", n1 + n2 + 1, fn(v2, v1), new)
            if len(new) > 4 * cap: break
        new.sort(key=lambda t: (t[1], t[0])); sets.append(new); prev = new
    al = [t for st in sets for t in st]; al.sort(key=lambda t: (t[1], t[0])); return [(t[0], t[1]) for t in al[:cap]], len(al)
def pool(foot, arm, ext=False):
    """names, nodes, memmap n x V. Controls and footings build their own closure."""
    tag = f"{foot}_{'real' if arm in ('real', 'planted', 'r10') else arm}{'_ext' if ext else ''}"; pn = os.path.join(CACHE, f"pool_{tag}.json"); pv = os.path.join(CACHE, f"pool_{tag}.dat"); R = Rows(foot, arm)
    if not os.path.exists(pn):
        al, tot = closure(R, (1, 2, 3) if ext else (1, 2), 80000 if ext else 150000); names = [a[0] for a in al]; v = np.memmap(pv + ".tmp", dtype="f8", mode="w+", shape=(len(names), len(R.y)))
        for i, s in enumerate(names): v[i] = tree(s, R.y, R.ell, R.f)
        v.flush(); del v; os.replace(pv + ".tmp", pv); json.dump(dict(names=names, nodes=[a[1] for a in al], total=tot), open(pn + ".tmp", "w")); os.replace(pn + ".tmp", pn)
    d = json.load(open(pn)); return d, np.memmap(pv, dtype="f8", mode="r", shape=(len(d["names"]), len(R.y))), R
# ---------- exact paths
class Exact:
    def __init__(s, foot, planted=None):
        s.foot = foot; s.a0 = A0[foot]; s.A, s.Le, s.Gr, s.Cs = mods(); s.g = geom(); s.L = s.Le.load(); s.st = s.Le.Stencil(s.L["Rn"] * 1e6); s.SIk = 1e6 / 3.0857e16; s.G = s.Cs.load_gal(); G = s.G; X = xcop_rows(); s.X = X; s.rows = s.Gr.load()
        s.ofs = np.r_[0, np.cumsum([len(g["R"]) for g in G])]; s.GB = np.hstack([s.Cs.gB_mat(g) for g in G]); s.RR = np.hstack([g["R"] for g in G]); GO = np.hstack([(g["Vobs"] * 1e3) ** 2 / g["R"] for g in G]); VO = np.hstack([g["Vobs"] for g in G]); s.W = np.hstack([1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2 for g in G]); GG = np.hstack([np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"] for g in G])
        s.OK = (s.GB > 0) & (GO > 0) & np.isfinite(s.GB) & (VO > 0); s.GQ = np.where(s.GB > 0, s.GB, 1.0); s.FF = np.clip(GG / s.GQ, 0, 1); s.LOGO = np.log10(np.where(GO > 0, GO, 1.0)); s.WOK = s.W[None, :] * s.OK; s.BS = np.add.reduceat(s.WOK, s.ofs[:-1], axis=1)
        Vf = np.array([g["Vflat"] for g in G]); Qq = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G]); s.LO, s.HI = Qq & (Vf > 0) & (Vf < 100), Qq & (Vf > 150); s.UPS = s.Cs.UPS; s.Yn = s.L["Yn"].ravel().copy(); s.obsX = X[:, 3].copy(); s.ls = np.array([x[0] for x in s.rows]); s.Cn = s.L["Cn"]; s.Csys = s.Cn + S_LENS ** 2 * np.outer(s.Yn, s.Yn)
        if planted:
            Hf, w = planted; a = s.a0; s.obsX = np.log10(wrap(w, X[:, 0], a, Hf(X[:, 0] / a, X[:, 2] * a / C ** 2, np.clip(X[:, 1] / X[:, 0], 0, 1)))); s.Yn = s.lens_model(Hf, w)
            s.Csys = s.Cn + S_LENS ** 2 * np.outer(s.Yn, s.Yn); s.ls = np.array([s.ls_model(Hf, w, x[1], x[2], 0.0, GF[1]) for x in s.rows])
            p = np.clip(np.argmin(np.abs(s.UPS - .65)), 0, None); m = wrap(w, s.GQ, a, Hf(s.GQ / a, s.RR * a / C ** 2, s.FF)); s.LOGO = np.broadcast_to(np.log10(np.maximum(m[p], 1e-300)), s.GB.shape).copy()
    def lens_model(s, Hf, w):
        Tb = np.zeros((len(s.Le.LMG), 60)); a = s.a0
        for i, lm in enumerate(s.Le.LMG):
            MB, _ = s.Le.baryon(float(lm)); gb = s.Le.Gpc * MB / s.Le.RGRID ** 2 * s.SIk; gg = s.Le.Gpc * (MB - 10 ** float(lm)) / s.Le.RGRID ** 2 * s.SIk; r = s.Le.RGRID * 3.0857e16; Tb[i] = s.st.dsig(MB * wrap(w, gb, a, Hf(gb / a, r * a / C ** 2, np.clip(gg / gb, 0, 1))) / gb, "linear")
        return s.Le.stack(s.L, Tb)
    def chi(s, m, Y, Cc):
        L = dict(s.L, Yn=Y.reshape(4, 15), Cn=Cc); return s.Le.fit(L, m, list(range(15)), s.g["T0"])
    def lens(s, Hf, w, b0=False):
        m = s.lens_model(Hf, w)
        if not np.isfinite(m).all(): return dict(cov=float("inf"), sys=float("inf"), b_sys=[], nonfinite=True, sys_b0=float("inf"))
        c0, b = s.chi(m, s.Yn, s.Cn); c1, b1 = s.chi(m, s.Yn, s.Csys); o = dict(cov=c0, sys=c1, b_sys=[float(x) for x in b1], nonfinite=not np.isfinite(m).all())
        if b0: r = s.Yn - m; o["sys_b0"] = float(r @ np.linalg.solve(s.Csys, r))
        return o
    def ls_model(s, Hf, w, lM, Re, dl, fx):
        P = s.Gr.P; a0 = s.a0; a = Re * (P.pc * 1e3) / 1.8153; Mb = 10 ** (lM + dl) * P.Msun; U_ = P.G * Mb / a ** 2; v = s.Gr.gN_t * U_; r = s.Gr.XG * a; gt = wrap(w, v, a0, Hf(v / a0, r * a0 / C ** 2, v * 0 + fx)) / U_; s2 = np.trapz(4 * math.pi * s.Gr.XG ** 2 * s.Gr.RHO_H * s.Gr.XG * gt * s.Gr.XG, s.Gr.LX) / 3 * P.G * Mb / a; return .5 * math.log10(s2) - 3 if s2 > 0 and np.isfinite(s2) else float("nan")
    def groups(s, Hf, w, fx):
        d = np.array([y - s.ls_model(Hf, w, x[1], x[2], 0.0, fx) for y, x in zip(s.ls, s.rows)]); sl = np.array([(s.ls_model(Hf, w, x[1], x[2], .01, fx) - s.ls_model(Hf, w, x[1], x[2], -.01, fx)) / .02 for x in s.rows]); m = d.mean(); t = math.hypot(d.std(ddof=1) / math.sqrt(len(d)), .10 * sl.mean()); return dict(v=float(-m), t=float(t), Z=float(-m / t))
    def xcop(s, Hf, w):
        X = s.X; a = s.a0; g = wrap(w, X[:, 0], a, Hf(X[:, 0] / a, X[:, 2] * a / C ** 2, np.clip(X[:, 1] / X[:, 0], 0, 1))); d = s.obsX - np.log10(g); by = np.array([d[X[:, 4] == j].mean() for j in np.unique(X[:, 4])]); m = float(d.mean()); t = math.hypot(by.std(ddof=1) / math.sqrt(len(by)), .12)
        return dict(mean=m, Z=m / t, scatter=float(d.std()), rms=float(np.sqrt((d * d).mean())), strict=bool(abs(m) <= .05 and np.sqrt((d * d).mean()) <= .10))
    def sparc(s, Hf, w):
        a = s.a0; gp = wrap(w, s.GQ, a, Hf(s.GQ / a, s.RR * a / C ** 2, s.FF)); gp = np.where(s.GB > 0, gp, s.GB); r = np.where(s.OK, s.LOGO - np.log10(np.maximum(gp, 1e-300)), 0.0); Aa = np.add.reduceat(s.WOK * r * r, s.ofs[:-1], axis=1); q = np.where(s.BS > 0, Aa / s.BS, np.inf); i = np.argmin(np.where(np.isnan(q), np.inf, q), axis=0); ii = np.arange(len(s.G)); bad = ~np.isfinite(q).any(axis=0); ww = Aa[i, ii]; wb = s.BS[i, ii]; ww[bad] = 0; wb[bad] = 0; Yb = s.UPS[i].astype(float); Yb[bad] = np.nan
        return dict(rms=float(math.sqrt(ww.sum() / wb.sum())) if wb.sum() > 0 else float("inf"), U=float(np.nanmedian(Yb)), tilt=float(np.nanmedian(Yb[s.LO]) - np.nanmedian(Yb[s.HI])), nf=bool(not np.isfinite(gp[s.OK]).all()))
    def all(s, Hf, w, b0=True):
        o = dict(lens=s.lens(Hf, w, b0), X=s.xcop(Hf, w), S=s.sparc(Hf, w)); o["G"] = {str(fx): s.groups(Hf, w, fx) for fx in GFALL}; return o
def S_pass(r): return r["rms"] <= .110 and .50 <= r["U"] <= .80 and not r["nf"]
def X_pass(r): return abs(r["Z"]) <= 2 and r["scatter"] <= .10
def G_pass(o): return all(abs(o[str(fx)]["Z"]) <= 2 for fx in GF)
def form_fn(s, fam):
    return lambda y, e, f: H_of(s, y, e, f, fam)
