"""Clusters: K (15 keys, both h) and X (X-COP). Section 4. Writes cache/k_*.npz per cell, partials/K_*.json, partials/X_*.json."""
from crg1_core import *
import crg1_efe as EFE
from crg1_zoom import get_nr
from scipy.interpolate import PchipInterpolator
from astropy.io import fits

np.seterr(all="ignore")  # numpy-on-Accelerate raises spurious FP flags in matmul; results checked finite
N_BIN = 8
BANDS = dict(INNER=[0, 1, 2], MID=[3, 4, 5], OUTER=[6, 7])
HS = [(0.672, 1, 0, "h0672"), (0.686, 2, 1, "h0686")]

# ---- grids
RG = np.logspace(-3, math.log10(30), 3000); RM = RG * F.Mpc; lnRG = np.log(RG)
RF = np.logspace(math.log10(2e-3), math.log10(3.5), 90); lnRF = np.log(RF)
EDGES = np.logspace(math.log10(0.15), math.log10(3), 9); RC = np.sqrt(EDGES[:-1] * EDGES[1:]); lnRC = np.log(RC)
UU = np.linspace(0, 1, 2001)
_umax = np.arccosh(RG[-1] / RF)
_rr = RF[:, None] * np.cosh(_umax[:, None] * UU[None, :])
_lrr = np.log(_rr)
_ix = np.clip(np.searchsorted(lnRG, _lrr, side="right") - 1, 0, len(RG) - 2)
_fx = np.clip((_lrr - lnRG[_ix]) / (lnRG[_ix + 1] - lnRG[_ix]), 0, 1)
_wu = _rr * F.Mpc * _umax[:, None] * (UU[1] - UU[0]); _wu[:, 0] *= 0.5; _wu[:, -1] *= 0.5
PHI = np.linspace(0, math.pi, 181); _wphi = np.full(181, PHI[1] - PHI[0]); _wphi[[0, -1]] *= 0.5; _cphi = np.cos(PHI)

# ---- distances
_DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295)
_DMb = math.sqrt(7.942 ** 3 / (0.295 * _DHb))
_PCH = PchipInterpolator([0, 0.295, 0.510, 0.706, 0.934, 1.321, 1.484, 2.330], [0, _DMb, 13.588, 17.351, 21.576, 27.601, 30.512, 38.988])
def D_M(z, h): return float(_PCH(min(z, 2.33))) * 101.54 / h
def DA_cat(z):
    zz = np.linspace(0, z, 600)
    return float(np.trapz(1 / np.sqrt(0.3 * (1 + zz) ** 3 + 0.7), zz)) * 2.998e8 / (1e3 * 70) / (1 + z)

# ---- turnaround constants
_H0T = h_nat * 1e5 / T.Mpc; _rhocT = 3 * _H0T ** 2 / (8 * math.pi * T.G)
_ObT = Ob_nat; _OcT = R_nat * _ObT; _OmT = _ObT + _OcT; _rhomT = _OmT * _rhocT
def rta_com(Mb): return (3 * (_OmT / _ObT) * Mb / (4 * math.pi * 5.55 * _rhomT)) ** (1.0 / 3)

def cumtrap(y, x):
    out = np.zeros_like(y); out[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x)); return out

def sh_core(r, rc): return 1 / (1 + (r / rc) ** 2)
def sh_tail(r, R500p, s):
    sh = sh_core(r, 0.15 * R500p); m = r > R500p
    sh[m] = sh_core(R500p, 0.15 * R500p) * (r[m] / R500p) ** (-s)
    return sh
def sh_P(r, R500p, tail_s=None):
    """gas P profile: core form to 2.2 R500', r^-3 beyond, zero beyond 3 Mpc. tail_s: NA1(b), GS1 tail to 2.2 R500'."""
    rc = 0.15 * R500p; b = 2.2 * R500p
    if tail_s is None:
        sh = sh_core(r, rc); vb = sh_core(b, rc)
    else:
        sh = sh_tail(r.copy(), R500p, tail_s); vb = sh_core(R500p, rc) * (b / R500p) ** (-tail_s)
    m = r > b; sh[m] = vb * (r[m] / b) ** (-3); sh[r > 3] = 0
    return sh
def mass_norm(sh, R500p):
    M = cumtrap(4 * math.pi * (RG * F.Mpc) ** 2 * sh, RG)
    return M / np.interp(R500p, RG, M)

S_GS1 = SC["gs1_s_meas"]
def chain(Mg500, R500p, fs, z, msun, seed=None):
    """Measured chain: returns M_bx, M_b (capped), M_bt, r_ta."""
    Mbx = (1 + fs) * mass_norm(sh_tail(RG.copy(), R500p, S_GS1), R500p) * Mg500 * msun
    if seed is None:
        seed = float(mass_norm(sh_P(RG.copy(), R500p), R500p)[-1]) * (1 + fs) * Mg500 * msun
    Mbt = seed
    for _ in range(199):
        rta = rta_com(Mbt) / (1 + z)
        new = float(np.interp(rta, RM, Mbx))
        ch = abs(new / Mbt - 1); Mbt = new
        if ch < 1e-6: break
    rta = rta_com(Mbt) / (1 + z)
    Mb = np.where(RM <= rta, Mbx, Mbt)
    return Mbx, Mb, Mbt, rta

# ---- projection
def sigma_of(Msrc):
    rho = np.gradient(Msrc, RM) / (4 * math.pi * RM ** 2)
    lr = np.where(rho > 0, np.log(np.where(rho > 0, rho, 1.0)), math.log(1e-300))
    v = lr[_ix] * (1 - _fx) + lr[_ix + 1] * _fx
    return 2 * (np.exp(v) * _wu).sum(1)

def offset(Sig, d):
    if d <= 1e-4: return Sig
    Rp = np.sqrt(RF[:, None] ** 2 + d * d + 2 * RF[:, None] * d * _cphi[None, :])
    v = np.exp(np.interp(np.log(Rp), lnRF, np.log(np.maximum(Sig, 1e-300))))
    return (v * _wphi).sum(1) / math.pi

def vec(Msrc, ctx):
    """V_i, 8 bins."""
    Sg = offset(sigma_of(Msrc), ctx["d"])
    y = Sg * RF
    cum = 0.5 * Sg[0] * RF[0] ** 2 + cumtrap(y, RF)
    dS = 2 * cum / RF ** 2 - Sg
    P = np.exp(np.interp(lnRC, lnRF, np.log(np.maximum(dS, 1e-30)))) / KG_PC2
    Sb = np.exp(np.interp(lnRC, lnRF, np.log(np.maximum(Sg, 1e-300))))
    fr = np.ones(N_BIN); den = ctx["den"]; pos = den > 0
    s = np.zeros(N_BIN)
    for p in range(6):
        s += Sb ** (p + 1) * ctx["m"][p]
    fr[pos] = 1 + s[pos] / den[pos]
    return ctx["W"] * P * fr

def m_cstar(Mb, a0, Cs):
    gN = F.G * Mb / RM ** 2
    sc = math.sqrt(F.G * float(np.interp(3.0, RG, Mb)) / a0) / F.Mpc
    gC = (0.5 * gN + np.sqrt(0.25 * gN ** 2 + gN * a0)) * Cs(RG / sc)
    return gC * RM ** 2 / F.G

# ---- data
class Data:
    def __init__(s):
        c = np.load(os.path.join(INP, "clusters", "x7_measure_percluster.npz"))
        x = np.load(os.path.join(INP, "clusters", "x2_catalogue_columns.npz"))
        s.N = 326; s.name = x["name"]; s.z = x["z"]; s.ra = x["ra"]; s.Mgas = x["Mgas500"]; s.R500 = x["R500"]; s.off = x["off_deg"]
        s.c = {k: c[k] for k in ("D", "E", "den", "den_r", "DRR", "Dx", "m3to8", "leakP")}
        kt = {r["name"]: r["KT_keV"] for r in csv.DictReader(open(os.path.join(INP, "clusters", "erass1_kt.csv")))}
        KT = np.array([float(kt.get(n, "nan") or "nan") for n in s.name]); s.KT = KT
        s.I = np.nonzero(np.isfinite(KT) & (KT > 0))[0]
        xkt = np.log10(KT[s.I] / np.median(KT[s.I])); s.xkt = xkt
        qt = np.quantile(xkt, [1 / 3, 2 / 3]); s.Tt = np.digitize(xkt, qt)
        s.X1 = np.column_stack([np.ones(len(xkt)), xkt])
        qm = np.quantile(s.Mgas, [1 / 3, 2 / 3]); s.Mt = np.digitize(s.Mgas, qm)
        o = np.argsort(s.ra); s.PATCH = np.zeros(s.N, int); s.PATCH[o] = np.arange(s.N) * 30 // s.N
        bc = {r["name"]: float(r["bcg_Msun_or_nan"]) for r in csv.DictReader(open(os.path.join(INP, "clusters", "bcg_per_cluster.csv")))}
        B = np.array([bc[n] for n in s.name]); s.BCGraw = B
        s.BCG = B.copy()
        for t in range(3):
            med = np.median(B[(s.Mt == t) & np.isfinite(B)])
            s.BCG[(s.Mt == t) & ~np.isfinite(B)] = med
        s.cal = json.load(open(os.path.join(INP, "clusters", "x7_outer_mgas_cal.json")))
        s.DACAT = np.array([DA_cat(z) for z in s.z])
        s.geo = {}
        for h, hi, hx, hn in HS:
            DM = np.array([D_M(z, h) for z in s.z]); DA = DM / (1 + s.z)
            q = DA / s.DACAT
            E_ = s.c["E"][:, hi]; W = np.where(E_ < 1e8, 1 / E_ ** 2, 0.0)
            Bst = s.c["den"][:, hi].sum(0) / s.c["den_r"][:, hi].sum(0)
            s.geo[h] = dict(hi=hi, hx=hx, hn=hn, q=q, d=np.radians(s.off) * DA, W=W, Bst=Bst)

def stacks():
    d = np.load(os.path.join(CACHE, "shape_stacks.npz"))
    return {k: d[k] for k in d.files}

OPT = dict(xe_all=False, c2x_capped=False)
def ztag(z): return "0.00" if z < 0.125 else ("0.25" if z < 0.375 else "0.50")

def cold_profile(ST, Mb, z, Mfair, rta, cnt):
    """Section 4.4. Returns M_h callable on metres. Uses Mb on RM for M200 at fair share."""
    bA = bg(BGS[0]); rc0 = rho_crit0(bA.h, E.G, E.Mpc)
    thr = 200 * rc0 * (Om_nat * (1 + z) ** 3 + 1 - Om_nat)
    with np.errstate(divide="ignore"):
        dens = (1 + R_nat) * Mb / (4.0 / 3 * math.pi * RM ** 3)
    ii = np.nonzero(dens >= thr)[0]
    if len(ii) and ii[-1] < len(RM) - 1:
        i = ii[-1]
        t = (math.log(thr) - math.log(dens[i])) / (math.log(dens[i + 1]) - math.log(dens[i]))
        R2 = math.exp(math.log(RM[i]) + t * (math.log(RM[i + 1]) - math.log(RM[i])))
        M2 = thr * 4.0 / 3 * math.pi * R2 ** 3
    else:
        cnt["no_fair_share"] += 1
        M2, R2 = fallback(Mb, Mfair, rta, thr, rc0)
    zt = ztag(z); tags = ("1e13", "1e14", "1e15")
    nodes = [float(ST["lgM_%s_%s" % (t, zt)]) for t in tags]; lg = math.log10(M2 / E.Msun)
    a = 0
    while a + 1 < 2 and lg > nodes[a + 1]: a += 1
    w = min(max((lg - nodes[a]) / (nodes[a + 1] - nodes[a]), 0), 1)
    lna, lnb = ST["lnm_%s_%s" % (tags[a], zt)], ST["lnm_%s_%s" % (tags[a + 1], zt)]
    lnm = (1 - w) * lna + w * lnb
    xe = min(float(ST["xe_%s_%s" % (tags[a], zt)]), float(ST["xe_%s_%s" % (tags[a + 1], zt)]))
    if OPT["xe_all"]: xe = min(float(ST["xe_%s_%s" % (t, zt)]) for t in tags)
    X = ST["X"]; lX = np.log(X)
    def lnmx(x):
        x = np.asarray(x, float); out = np.interp(np.log(x), lX, lnm)
        low = x < X[0]; out = np.where(low, lnm[0] + 2 * np.log(x / X[0]), out)
        return out
    def Mc(r): return f_c * M2 * np.exp(lnmx(np.asarray(r, float) / R2))
    re = xe * R2
    if re >= rta:
        cnt["edge_beyond_rta"] += 1
        return lambda r: Mc(np.minimum(r, rta))
    Me = float(Mc(re))
    k = int(np.searchsorted(lX, math.log(xe), side="left"))
    dln = (lnm[k] - lnm[k - 8]) / (lX[k] - lX[k - 8])
    rhoe = Me * dln / (4 * math.pi * re ** 3)
    if Me >= Mfair:
        cnt["no_tail"] += 1
        return lambda r: np.where(np.asarray(r) <= re, Mc(r), Me)
    L = math.log(rta / re); tgt = (Mfair - Me) / (4 * math.pi * rhoe * re ** 3)
    def I(g):
        if abs(3 - g) < 1e-9: return L
        return math.expm1(min((3 - g) * L, 700)) / (3 - g)
    lo, hi = -40.0, 60.0; widen = False
    while not ((I(lo) - tgt) * (I(hi) - tgt) <= 0):
        lo = 3 - 2 * (3 - lo); hi = 3 + 2 * (hi - 3); widen = True
        if hi > 1e7: raise RuntimeError("gamma bracket")
    if widen: cnt["wide_gamma"] += 1
    gam = brentq(lambda g: I(g) - tgt, lo, hi, xtol=1e-9)
    def Mh(r):
        r = np.asarray(r, float); rr = np.minimum(r, rta); y = np.maximum(rr / re, 1.0)
        tail = Me + 4 * math.pi * rhoe * re ** 3 * (np.log(y) if abs(3 - gam) < 1e-9 else (y ** (3 - gam) - 1) / (3 - gam))
        return np.where(r <= re, Mc(r), tail)
    return Mh

def fallback(Mb, Mfair, rta, thr, rc0):
    bA = bg(BGS[0]); thr0 = 200 * rc0
    M = (Mfair + Mb[-1]) / F.Msun
    fs = "0.034"
    for _ in range(100):
        S = max(A0["canonical"] / (2 * math.pi * E.G), f_c * float(eta_A3(M, fs)) * float(bA.sigcoll(M)) * E.Msun / PC2)
        r0 = solve_r0(Mfair, rta, S, B_S)
        m = lambda r: float(np.interp(r, RM, Mb)) + math.pi * S * r0 ** 2 * float(B_S(r / r0))
        R2 = brentq(lambda r: math.log(m(r) / (thr0 * 4.0 / 3 * math.pi * r ** 3)), 1e-3 * rta, rta, xtol=1e-12 * rta)
        Mn = thr0 * 4.0 / 3 * math.pi * R2 ** 3 / E.Msun
        d = abs(math.log(Mn / M)); M = Mn
        if d <= 1e-8: break
    M2 = M * E.Msun
    return M2, (3 * M2 / (4 * math.pi * thr)) ** (1.0 / 3)

# ---- cell builders
def ctx_of(D, h, i):
    g = D.geo[h]; hi = g["hi"]
    return dict(d=g["d"][i], den=D.c["den"][i, hi], m=D.c["m3to8"][i, hi], W=g["W"][i])

def _cstars(Mb, c, CSS):
    return {k: vec(m_cstar(Mb, A0[k.split("_")[1]], Cs), c) for k, Cs in CSS.items()}

def build_cell(D, ST, CSS, h, kind, fs=None, gdex=None, nr=None, tail_s=None):
    """kind: C1, C2, C4. Returns V, vC dict, counters."""
    N = D.N; V = np.zeros((N, N_BIN)); vC = {k: np.zeros((N, N_BIN)) for k in CSS}
    extra = {}
    if kind == "C2": vCb = {k: np.zeros((N, N_BIN)) for k in CSS}
    cnt = dict(no_fair_share=0, no_tail=0, wide_gamma=0, edge_beyond_rta=0)
    gas = 10 ** gdex if gdex is not None else 1.0
    g_ = D.geo[h]; bA = bg(BGS[0])
    for i in range(N):
        z = D.z[i]; q = g_["q"][i]; c = ctx_of(D, h, i)
        Mg = D.Mgas[i] * q ** 2.5 * gas; Rp = D.R500[i] * q
        if kind == "C4":
            Mb = (1 + fs) * mass_norm(sh_P(RG.copy(), Rp, tail_s), Rp) * Mg * F.Msun
            for k in vC: 
                pass
            pos = Mb > 0; Ms = Mb.copy()
            MsV = {}
            for k, Cs in CSS.items():
                a0 = A0[k.split("_")[1]]
                if a0 not in MsV:
                    t = Mb.copy(); t[pos] = Mb[pos] * nu(F.G * Mb[pos] / RM[pos] ** 2 / a0); MsV[a0] = vec(t, c)
                vC[k][i] = vec(m_cstar(Mb, a0, Cs), c)
            extra.setdefault("V_by_a0", {})
            for a0, v in MsV.items():
                extra["V_by_a0"].setdefault(a0, np.zeros((N, N_BIN)))[i] = v
            continue
        Mbx, Mb, Mbt, rta = chain(Mg, Rp, fs, z, F.Msun)
        Mfair = R_nat * Mbt
        if kind == "C1":
            Mh = cold_profile(ST, Mb, z, Mfair, rta, cnt)
            V[i] = vec(Mb + Mh(RM), c)
        elif kind == "C2":
            Mt = (Mfair + Mb[-1]) / F.Msun
            S = nr.S(Mt, bA); r0 = solve_r0(Mfair, rta, S, B_S)
            M0 = math.pi * S * r0 ** 2 * B_S(np.minimum(RM, rta) / r0)
            Mbf = Mb + D.BCG[i] * E.Msun * RM ** 2 / (RM + 10 * E.pc * 1e3) ** 2
            Fv = float(np.interp(rta, RM, Mbf)) / Mfair
            Mf = contract(RM, Mbf, M0, Fv)
            V[i] = vec(Mbf + Mf, c)
            for k, Cs in CSS.items():
                vCb[k][i] = vec(m_cstar(Mbf, A0[k.split("_")[1]], Cs), c)
        for k, v in _cstars(Mb, c, CSS).items(): vC[k][i] = v
    if kind == "C2": extra["vC_Mbf"] = vCb
    return V, vC, cnt, extra

# ---- measurement + keys
class Meas:
    def __init__(s, D, h, Dov=None, leak0=False):
        g = D.geo[h]; hi, hx = g["hi"], g["hx"]; s.D = D; s.h = h; s.g = g
        W, Bst = g["W"], g["Bst"]
        DD = D.c["D"][:, hi] if Dov is None else Dov
        leak = D.c["leakP"][:, hx, 0] * (0 if leak0 else 1)
        s.n = W * Bst * (DD - leak); s.nraw = W * Bst * DD
        s.nx = W * Bst * D.c["Dx"][:, hi]; s.nRR = W * Bst * D.c["DRR"][:, hi]

def bs(key, nsel):
    idx = np.random.default_rng([20261024, key]).integers(0, nsel, size=(2000, nsel))
    W = np.zeros((2000, nsel))
    rows = np.arange(2000)[:, None]
    np.add.at(W, (np.repeat(rows, nsel, 1), idx), 1.0)
    return W
_BS = {}
def bsw(key, nsel):
    if (key, nsel) not in _BS: _BS[(key, nsel)] = bs(key, nsel)
    return _BS[(key, nsel)]

def jk_weights(patch):
    qs = [q for q in range(30) if (patch == q).any()]
    return np.array([(patch != q).astype(float) for q in qs])

def jk_sig(v):
    n = len(v); return math.sqrt((n - 1) / n * ((v - v.mean()) ** 2).sum())

def sig_ratio(D, sel, key, nraw, d):
    Wb = bsw(key, len(sel))
    rb = (Wb @ nraw) / (Wb @ d)
    sb = rb.std(ddof=1)
    Wj = jk_weights(D.PATCH[sel]); rj = (Wj @ nraw) / (Wj @ d)
    return max(sb, jk_sig(rj)), sb

def beta1_w(n, d, X, Wt):
    # Wt: replicates x clusters
    a00 = Wt @ d; a01 = Wt @ (d * X[:, 1]); a11 = Wt @ (d * X[:, 1] ** 2)
    y0 = Wt @ n; y1 = Wt @ (n * X[:, 1])
    return (a00 * y1 - a01 * y0) / (a00 * a11 - a01 ** 2)

def keys_table(M, V, vC, cal_foot, mode="template", ):
    """mode: template = own A, sigma s_CAL A/A_CAL; given = A_CAL, s_CAL (C4 A8a)."""
    D = M.D; I = D.I; out = {}
    def band(a, b): return a[:, BANDS[b]].sum(1)
    def rat(sel, b, a=None): 
        return band(a if a is not None else M.n, b)[sel].sum() / band(vC, b)[sel].sum()
    def pred(sel, b): return band(V, b)[sel].sum() / band(vC, b)[sel].sum()
    def rec(k, A, s, p, **kw):
        out[k] = dict(A=A, sigma=s, pred=p, Z=(A - p) / s, **kw)
    calk = cal_foot + "|" + M.g["hn"]
    all_ = np.arange(D.N)
    # G-IN
    for nm, sel in (("G-IN-all", I), ("G-IN-Mall", all_)):
        A = rat(sel, "INNER"); ss, _ = sig_ratio(D, sel, 0, band(M.nraw, "INNER")[sel], band(vC, "INNER")[sel])
        Ax = rat(sel, "INNER", M.nx); Ar = rat(sel, "INNER", M.nRR)
        rec(nm, A, math.sqrt(ss ** 2 + Ax ** 2 + Ar ** 2), pred(sel, "INNER"), sigma_stat=ss, A_x=Ax, A_RR=Ar)
    for t in range(3):
        sel = I[D.Tt == t]
        for b, tag in (("MID", "G-MID-T%d"), ("OUTER", "G-OUT-T%d")):
            A = rat(sel, b); ss, _ = sig_ratio(D, sel, 20100 + t, band(M.nraw, b)[sel], band(vC, b)[sel])
            rec(tag % (t + 1), A, ss, pred(sel, b))
    A = rat(I, "OUTER"); ss, _ = sig_ratio(D, I, 0, band(M.nraw, "OUTER")[I], band(vC, "OUTER")[I])
    rec("G-OUT-all", A, ss, pred(I, "OUTER"))
    for b, nm in (("MID", "G-MID-b"), ("OUTER", "G-OUT-b")):
        n_, d_, v_ = band(M.n, b)[I], band(vC, b)[I], band(V, b)[I]
        A = wls(n_, d_, D.X1)[1]; p = wls(v_, d_, D.X1)[1]
        Wb = bsw(5010, len(I)); sb = beta1_w(n_, d_, D.X1, Wb).std(ddof=1)
        Wj = jk_weights(D.PATCH[I]); sj = jk_sig(beta1_w(n_, d_, D.X1, Wj))
        rec(nm, A, max(sb, sj), p)
    for lab, sel, key in [("Mall", all_, 0)] + [("M%d" % (t + 1), np.nonzero(D.Mt == t)[0], 200 + t) for t in range(3)]:
        Aown = rat(sel, "OUTER"); c = D.cal[calk][lab]
        ss, _ = sig_ratio(D, sel, key, band(M.nraw, "OUTER")[sel], band(vC, "OUTER")[sel])
        if mode == "template":
            rec("G-OUT-" + lab, Aown, c["s_CAL"] * Aown / c["A_CAL"], pred(sel, "OUTER"), own_sigma_stat=ss, A_CAL=c["A_CAL"], s_CAL=c["s_CAL"])
        else:
            rec("G-OUT-" + lab, c["A_CAL"], c["s_CAL"], pred(sel, "OUTER"), own_A=Aown, own_sigma_stat=ss)
    return out

def k_summary(tables):
    """tables: {hname: keys}. Fail if |Z|>2 in either h."""
    fl = sorted({k for t in tables.values() for k, v in t.items() if abs(v["Z"]) > 2})
    n = len(next(iter(tables.values())))
    return dict(failing=fl, n_keys=n, n_pass=n - len(fl), passed=len(fl) == 0)

def load_or_build(name, fn):
    p = os.path.join(CACHE, "k_%s.npz" % name)
    if os.path.exists(p):
        d = np.load(p); return {k: d[k] for k in d.files}
    t = time.time(); out = fn()
    tmp = p + ".tmp%d.npz" % os.getpid(); np.savez(tmp, **out); os.replace(tmp, p)
    log("built %s %.1fs mem %.0fMB" % (name, time.time() - t, peak_mb()))
    return out

CSS_KEYS = ["own_canonical", "own_alt", "tab_canonical", "tab_alt"]
def all_css():
    return {"own_canonical": EFE.get("canonical", "own"), "own_alt": EFE.get("alt", "own"),
            "tab_canonical": EFE.get("canonical", "tab"), "tab_alt": EFE.get("alt", "tab")}

def fn_C1(D, ST, CSS, h, fs, gd):
    def f():
        V, vC, cnt, _ = build_cell(D, ST, CSS, h, "C1", fs=fs, gdex=gd)
        d = dict(V=V, cnt=np.array([cnt[k] for k in sorted(cnt)]))
        d.update({"vC_" + k: v for k, v in vC.items()}); return d
    return f
def fn_C2(D, ST, CSS, h, nr):
    def f():
        V, vC, cnt, ex = build_cell(D, ST, CSS, h, "C2", fs=SC["fstar"]["primary"], gdex=None, nr=nr)
        d = dict(V=V); d.update({"vC_" + k: v for k, v in vC.items()}); d.update({"vCb_" + k: v for k, v in ex["vC_Mbf"].items()}); return d
    return f
def fn_C4(D, ST, CSS, h, tail_s=None):
    def f():
        V, vC, cnt, ex = build_cell(D, ST, CSS, h, "C4", fs=SC["fstar"]["harness"], gdex=None, tail_s=tail_s)
        d = {"V_canonical": ex["V_by_a0"][A0["canonical"]], "V_alt": ex["V_by_a0"][A0["alt"]]}
        d.update({"vC_" + k: v for k, v in vC.items()}); return d
    return f

def K_block(D, cellf, Vk, vCk, cal_foot, mode="template"):
    tabs = {}
    for h, _, _, hn in HS:
        d = cellf(h); tabs[hn] = keys_table(Meas(D, h), d[Vk], d[vCk], cal_foot, mode)
    return dict(tables=tabs, **k_summary(tabs))

def max_dZ(a, b):
    return max(abs(a["tables"][h][k]["Z"] - b["tables"][h][k]["Z"]) for h in a["tables"] for k in a["tables"][h])

CNT_NAMES = ["edge_beyond_rta", "no_fair_share", "no_tail", "wide_gamma"]

def xcop_load():
    out = []
    for n in sorted(os.listdir(os.path.join(INP, "xcop"))):
        p = os.path.join(INP, "xcop", n, n)
        with fits.open(p + "_hydro_mass.fits") as H:
            R500 = float(H[1].header["R500"]); z = float(H[1].header["REDSHIFT"]); hr = np.array(H[1].data["RADIUS"], float); hm = np.array(H[1].data["M_FORW"], float)
        with fits.open(p + "_fgas_profile.fits") as H:
            Rg = float(H[1].header["R500"]); gr = np.array(H[1].data["RADIUS"], float) * Rg; gm = np.array(H[1].data["MGAS"], float)
        with fits.open(p + "_mstar.fits") as H:
            sr = np.array(H[2].data["RADIUS"], float); sm = np.array(H[2].data["MSTAR"], float)
        out.append(dict(name=n, R500=R500, z=z, hr=hr, hm=hm, gr=gr, gm=gm, sr=sr, sm=sm))
    return out

def li(r, m, t):
    ok = (r > 0) & (m > 0)
    r, m = r[ok], m[ok]
    if t < r[0] or t > r[-1]: return float("nan")
    return float(np.exp(np.interp(math.log(t), np.log(r), np.log(m))))

XS = (0.1, 0.2, 0.3, 0.5, 0.7)
def x_cell(XC, ST, kind, fs, g=1.0, nr=None):
    """X-COP. g != 1 only in A6(b)."""
    bA = bg(BGS[0]); rows = []; cnt = dict(no_fair_share=0, no_tail=0, wide_gamma=0, edge_beyond_rta=0)
    for c in XC:
        Mg = li(c["gr"], c["gm"], c["R500"]) * g; Rp = c["R500"] / 1e3
        Mbx, Mb, Mbt, rta = chain(Mg, Rp, fs, c["z"], E.Msun, seed=3 * 1.2 * Mg * E.Msun)
        Mfair = R_nat * Mbt
        if kind == "C1":
            Mh = cold_profile(ST, Mb, c["z"], Mfair, rta, cnt)
            Mhf = lambda r: float(Mh(np.array([min(r, rta)]))[0])
        else:
            Mt = (Mfair + Mb[-1]) / E.Msun; S = nr.S(Mt, bA); r0 = solve_r0(Mfair, rta, S, B_S)
            M0 = math.pi * S * r0 ** 2 * B_S(np.minimum(RM, rta) / r0)
            Mcp = contract(RM, Mb if OPT["c2x_capped"] else Mbx, M0, Mbt / Mfair)
            Mhf = lambda r: float(np.interp(r, RM, Mcp))
        for x in XS:
            r = x * c["R500"]
            mh, mg, ms = li(c["hr"], c["hm"], r), li(c["gr"], c["gm"], r) * g, li(c["sr"], c["sm"], r)
            if not all(map(np.isfinite, (mh, mg, ms))): continue
            rm = r * 1e3 * E.pc
            d = math.log10(mh * E.Msun / ((mg + ms) * E.Msun + Mhf(rm)))
            rows.append(dict(cluster=c["name"], x=x, d=d))
    ds = np.array([r["d"] for r in rows])
    by_x = {str(x): float(np.mean([r["d"] for r in rows if r["x"] == x])) for x in XS}
    by_c = {c["name"]: float(np.mean([r["d"] for r in rows if r["cluster"] == c["name"]])) for c in XC}
    return dict(mean=float(ds.mean()), rms=float(math.sqrt((ds ** 2).mean())), n_rows=len(rows), n_clusters=len(by_c), by_x=by_x, per_cluster=by_c, counts=cnt,
                passed=bool(abs(ds.mean()) <= 0.05 and math.sqrt((ds ** 2).mean()) <= 0.10))

def main():
    D = Data(); ST = stacks(); CSS = all_css(); NRa, NRb = get_nr("a"), get_nr("b")
    FS = SC["fstar"]; GD = SC["gas_dex"]
    Tags = "[recomputed]"
    def cell_C1(fs, gd):
        def f(h):
            nm = "C1_f%g_g%g_h%s" % (fs, gd, h)
            return load_or_build(nm, fn_C1(D, ST, CSS, h, fs, gd))
        return f
    # C1, with C3's alt = alt C*
    if not have_part("K_C1"):
        out = {}
        for fs in (FS["primary"], FS["reported"]):
            for gd in (GD["gs4"], GD["xcop"]):
                cf = cell_C1(fs, gd); name = "f%s_g%s" % (fs, gd)
                r = K_block(D, cf, "V", "vC_own_canonical", "canonical")
                r["A9b_alt_Cstar"] = K_block(D, cf, "V", "vC_own_alt", "alt")
                t = K_block(D, cf, "V", "vC_tab_canonical", "canonical"); r["A10b_max_dZ_canonical"] = max_dZ(r, t)
                if r["A10b_max_dZ_canonical"] > 0.10: r["A10b_given_table"] = t
                ta = K_block(D, cf, "V", "vC_tab_alt", "alt"); r["A10b_max_dZ_alt"] = max_dZ(r["A9b_alt_Cstar"], ta)
                if r["A10b_max_dZ_alt"] > 0.10: r["A10b_given_table_alt"] = ta
                if fs == FS["primary"] and gd == GD["gs4"]:
                    OPT["xe_all"] = True
                    def cfx(h): return load_or_build("C1_NA4b_h%s" % h, fn_C1(D, ST, CSS, h, fs, gd))
                    r["NA4b_x_edge_min_all_nodes"] = K_block(D, cfx, "V", "vC_own_canonical", "canonical")
                    OPT["xe_all"] = False
                    keep = {h: D.geo[h]["Bst"] for h, *_ in HS}
                    for h, hi, *_ in HS:
                        D.geo[h]["Bst"] = D.c["den"][D.I][:, hi].sum(0) / D.c["den_r"][D.I][:, hi].sum(0)
                    r["NA9b_Bst_over_I"] = K_block(D, cf, "V", "vC_own_canonical", "canonical")
                    for h in keep: D.geo[h]["Bst"] = keep[h]
                r["counts_per_h"] = {str(h): dict(zip(CNT_NAMES, [int(v) for v in cf(h)["cnt"]])) for h, *_ in HS}
                out[name] = r
        save_part("K_C1", out); log("K C1 done")
    if not have_part("K_C2"):
        def cf(h): return load_or_build("C2_h%s" % h, fn_C2(D, ST, CSS, h, NRa))
        def cfb(h): return load_or_build("C2_A1b_h%s" % h, fn_C2(D, ST, CSS, h, NRb))
        r = K_block(D, cf, "V", "vC_own_canonical", "canonical")
        r["A9b_alt_Cstar"] = K_block(D, cf, "V", "vC_own_alt", "alt")
        t = K_block(D, cf, "V", "vC_tab_canonical", "canonical"); r["A10b_max_dZ_canonical"] = max_dZ(r, t)
        if r["A10b_max_dZ_canonical"] > 0.10: r["A10b_given_table"] = t
        r["NA3b_Cstar_on_Mbf"] = K_block(D, cf, "V", "vCb_own_canonical", "canonical")
        r["A1b"] = K_block(D, cfb, "V", "vC_own_canonical", "canonical")
        save_part("K_C2", r); log("K C2 done")
    if not have_part("K_C4"):
        def cf(h): return load_or_build("C4_h%s" % h, fn_C4(D, ST, CSS, h))
        def cft(h): return load_or_build("C4_NA1b_h%s" % h, fn_C4(D, ST, CSS, h, tail_s=S_GS1))
        out = {}
        for foot in ("canonical", "alt"):
            r = K_block(D, cf, "V_" + foot, "vC_own_" + foot, foot, mode="given")
            r["A8b_one_template"] = K_block(D, cf, "V_" + foot, "vC_own_" + foot, foot, mode="template")
            t = K_block(D, cf, "V_" + foot, "vC_tab_" + foot, foot, mode="given"); r["A10b_max_dZ"] = max_dZ(r, t)
            if r["A10b_max_dZ"] > 0.10: r["A10b_given_table"] = t
            r["NA1b_GS1_tail_in_gas_P"] = K_block(D, cft, "V_" + foot, "vC_own_" + foot, foot, mode="given")
            out[foot] = r
        save_part("K_C4", out); log("K C4 done")
    if not have_part("X_all"):
        XC = xcop_load(); out = {}
        for fs in (FS["primary"], FS["reported"]):
            out["C1_f%s" % fs] = x_cell(XC, ST, "C1", fs)
            out["C1_f%s_A6b_g0.005" % fs] = x_cell(XC, ST, "C1", fs, g=10 ** GD["gs4"])
            out["C1_f%s_A6b_g0.111" % fs] = x_cell(XC, ST, "C1", fs, g=10 ** GD["xcop"])
        out["C2_f0.034"] = x_cell(XC, ST, "C2", FS["primary"], nr=NRa)
        out["C2_f0.034_A1b"] = x_cell(XC, ST, "C2", FS["primary"], nr=NRb)
        OPT["c2x_capped"] = True
        out["C2_f0.034_NA13b_capped_Mb"] = x_cell(XC, ST, "C2", FS["primary"], nr=NRa)
        OPT["c2x_capped"] = False
        OPT["xe_all"] = True
        out["C1_f0.034_NA4b"] = x_cell(XC, ST, "C1", FS["primary"])
        OPT["xe_all"] = False
        save_part("X_all", out); log("X done"); log("solve_r0 counts clusters %s" % COUNT)

if __name__ == "__main__": main()
