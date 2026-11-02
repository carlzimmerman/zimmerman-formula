"""MX1: g = max(law(g_b), g_b + g_c), own implementation, criteria FROZEN_CRITERIA.md. A test of a cold term beside the law; reinstates nothing. Cold dark energy, no particle. kappa = 1/2 FITTED; not theory closed."""
import math, os, json
import numpy as np
_D = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "."
RB = os.path.dirname(_D); REPO = os.path.dirname(RB)
GN, MSUN, PCM = 6.674e-11, 1.989e30, 3.0857e16
HUB = 0.672; RHOC = 3 * (100e3 * HUB / (PCM * 1e6)) ** 2 / (8 * math.pi * GN) / MSUN  # Msun/m^3
MUT = os.environ.get("MX1_MUTATE") == "1"; SHARE = 5.35 * (0.5 if MUT else 1.0); FCOLD = SHARE / (1 + SHARE)
_S = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json")))
LNX = np.log(np.asarray(_S["x"], float))
_T = sorted((float(_S[k]["0.00"]["lgM"]), np.asarray(_S[k]["0.00"]["lnm"], float)) for k in ("1e10", "1e11", "1e12", "1e13", "1e14"))
_TL = np.array([t[0] for t in _T]); _TM = np.vstack([t[1] for t in _T])
def lnm_at(lg):
    i = int(np.clip(np.searchsorted(_TL, lg) - 1, 0, len(_TL) - 2)); w = float(np.clip((lg - _TL[i]) / (_TL[i + 1] - _TL[i]), 0, 1)); return _TM[i] * (1 - w) + _TM[i + 1] * w
def r200_of(M): return (3 * M / (800 * math.pi * RHOC)) ** (1 / 3)
def law(g, a):
    g = np.asarray(g, float); p = np.maximum(g, 0); return np.where(g > 0, 0.5 * p + np.sqrt(0.25 * p * p + a * p), g)
def mfrac(x, ln):
    lx = np.log(np.maximum(x, 1e-300)); return np.exp(np.where(lx < LNX[0], ln[0] + 2 * (lx - LNX[0]), np.interp(lx, LNX, ln)))
class Halo:
    """Native cold mass for a given total M200."""
    def __init__(s, M200, cap=True):
        s.M = M200; s.R = r200_of(M200); s.ln = lnm_at(math.log10(M200)); s.cap = cap
    def M0(s, r):
        r = np.asarray(r, float); q = np.minimum(r, s.R) if s.cap else r; return FCOLD * s.M * mfrac(q / s.R, s.ln)
def m200_rule(Mb_of_R, mass, start):
    """Solves M200 = rule(M_b(<R200(M200))) by damped substitution."""
    rule = (lambda m: (1 + SHARE) * m) if mass == "share" else (lambda m: 10 ** (11.18 + 0.9 * (math.log10(max(m, 1e-30)) - 10)))
    M = rule(max(start, 1e-30))
    for _ in range(60):
        n = rule(max(Mb_of_R(r200_of(M)), 1e-30)); d = math.sqrt(M * n)
        if abs(d / M - 1) < 1e-10: M = d; break
        M = d
    return M
def contracted(rq, hal, r_arr, Mb_arr, Mb_tot, f):
    """rq in m ascending. Blumenthal-type: r_i M0(r_i)(1 + F) = r_f (M_b(r_f) + M0(r_i)), by bisection in ln r_f on a fixed grid; M_b inside the array's first point ~ r^2, flat past its end."""
    M0q = hal.M0(rq)
    if f == 0: return M0q
    lo_ = min(rq[0], hal.R) * 0.03; hi_ = max(hal.R * 1.3, rq[-1] * 1.02); ri = np.geomspace(lo_, hi_, 140); M0 = hal.M0(ri); Mc_tot = FCOLD * hal.M; F = Mb_tot / Mc_tot; lra = np.log(r_arr)
    def Mbf(x): return np.where(x < r_arr[0], Mb_arr[0] * (x / r_arr[0]) ** 2, np.interp(np.log(x), lra, Mb_arr))
    A = np.log(ri * 1e-4); B = np.log(ri * 1.5); T = ri * M0 * (1 + F)
    for _ in range(34):
        C = 0.5 * (A + B); x = np.exp(C); ok = x * (Mbf(x) + M0) < T; A = np.where(ok, C, A); B = np.where(ok, B, C)
    rf = np.maximum.accumulate(np.exp(0.5 * (A + B))); Mc = np.interp(np.log(rq), np.log(rf), M0, left=0.0, right=M0[-1]); low = rq < rf[0]
    if low.any(): Mc = np.where(low, M0[0] * (rq / rf[0]) ** 2, Mc)
    return M0q + f * (Mc - M0q)
# ---------- X-COP measured baryons, by R500 value
_XT = {}
def xcop_table():
    if _XT: return _XT
    from astropy.io import fits
    D = os.path.join(REPO, "real_research", "data", "xcop")
    for n in sorted(os.listdir(D)):
        p = os.path.join(D, n)
        if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{n}_mstar.fits"))): continue
        with fits.open(os.path.join(p, f"{n}_hydro_mass.fits")) as h: r5 = float(h[1].header["R500"])
        with fits.open(os.path.join(p, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = float(h[1].header["R500"])
        with fits.open(os.path.join(p, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        rq = np.geomspace(5.0, 8000.0, 400); lg = np.log(np.asarray(ga["RADIUS"], float) * rg); ls = np.log(np.asarray(st["RADIUS"], float)); Mg = np.interp(np.log(rq), lg, np.maximum.accumulate(np.asarray(ga["MGAS"], float))); Ms = np.interp(np.log(rq), ls, np.maximum.accumulate(np.asarray(st["MSTAR"], float)))
        _XT[r5 * 1e3 * PCM] = (n, rq * 1e3 * PCM, Mg + Ms, Mg, Ms, float(ga["RADIUS"].max() * rg * 1e3 * PCM))
    return _XT
def xcop_lookup(r5):
    for k, v in xcop_table().items():
        if abs(k / r5 - 1) < 1e-6: return v
    return None
# ---------- candidate
class Rule:
    def __init__(s, mass="share", f=0.872, cap=True, xcop="fits", p=None, X=1.0, name="P", use_lg=True, a0x=1.0):
        s.mass, s.f, s.cap, s.xcop, s.p, s.X, s.name, s.use_lg, s.a0x = mass, f, cap, xcop, p, X, name, use_lg, a0x
    def gc_sorted(s, rs, gb, lg=None, r5=None):
        """rs ascending m, gb there. Returns g_c on rs."""
        Marr = np.maximum.accumulate(np.maximum(gb * rs ** 2 / GN / MSUN, 0.0))
        if Marr[-1] <= 0 and lg is None: return rs * 0
        rarr, marr = rs, Marr
        tab = xcop_lookup(r5) if (r5 is not None and s.xcop == "fits") else None
        if lg is not None and s.use_lg:
            tot = 10 ** float(lg); Mbf = lambda R: tot
        elif tab is not None:
            lr = np.log(tab[1]); Mbf = lambda R: float(np.interp(math.log(R), lr, tab[2]))
        elif r5 is not None and s.xcop == "linear" and rs[-1] < 2 * r5:
            Mbf = lambda R: float(Marr[-1] * max(R / rs[-1], 1.0)) if R > rs[-1] else float(np.interp(math.log(R), np.log(rs), Marr))
        else:
            lr = np.log(rs); Mbf = lambda R: float(Marr[0] * (R / rs[0]) ** 2) if R < rs[0] else float(np.interp(math.log(R), lr, Marr))
        M = m200_rule(Mbf, s.mass, float(max(Marr[-1], 10 ** float(lg) if (lg is not None and s.use_lg) else 0.0)))
        h = Halo(M, s.cap); tot = Mbf(h.R)
        if r5 is not None and s.xcop == "linear" and h.R > rs[-1]: rarr, marr = np.append(rs, h.R), np.append(Marr, tot)
        return s.X * GN * contracted(rs, h, rarr, marr, tot, s.f) * MSUN / rs ** 2
    def one(s, r, gb, lg=None, r5=None):
        o = np.argsort(r); out = np.empty_like(gb, dtype=float); out[o] = s.gc_sorted(r[o], gb[o], lg, r5); return out
    def combine(s, gb, gc, a):
        L = law(gb, a); C = gb + gc
        if s.p is None: return np.maximum(L, C)
        Lp = np.maximum(L, 0); Cp = np.maximum(C, 0); N = np.maximum(np.maximum(Lp, Cp), 1e-300); v = N * ((Lp / N) ** s.p + (Cp / N) ** s.p) ** (1 / s.p); return np.where(gb > 0, v, C)
    def g(s, Q):
        gb = np.asarray(Q["gb"], float); r = np.asarray(Q["r"], float); a = Q["a0"] * s.a0x
        if r.size == 0 or not np.all(np.isfinite(r)): return law(gb, a)
        lg = Q["lgMb"] if "lgMb" in Q else None; pos = np.maximum(gb, 0)
        if gb.ndim == 2:
            rr = np.broadcast_to(r, gb.shape); gc = np.stack([s.one(rr[i], pos[i], lg) for i in range(gb.shape[0])])
        elif "r500" in Q:
            r5 = np.asarray(Q["r500"], float)
            if r5.ndim == 0 or np.unique(r5).size == 1: gc = s.one(r, pos, lg, float(np.max(r5)))
            else:
                gc = np.zeros_like(gb)
                for u in np.unique(r5):
                    m = r5 == u; gc[m] = s.one(r[m], pos[m], lg, float(u))
        else: gc = s.one(np.broadcast_to(r, gb.shape).copy(), pos, lg)
        return s.combine(gb, gc, a)
CELLS = dict(P=dict(), F0=dict(f=0.0), E1=dict(mass="em1"), U=dict(cap=False), FL=dict(xcop="array"), S2=dict(p=2.0), S4=dict(p=4.0), S8=dict(p=8.0), K0=dict(X=0.0), D2=dict(xcop="linear", use_lg=False), MUT=dict(X=10.0), KM=dict(X=0.0, a0x=1.5))
def rule(cell): return Rule(name=cell, **CELLS[cell])
