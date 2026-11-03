"""MB1's rule. A one-object system is the law; in a multi-member system objects add linearly and each member keeps its own law halo to r_t. A description, no action. kappa = 1/2 FITTED. See FROZEN_CRITERIA.md."""
import json, os
import numpy as np
G = 6.6743e-11; MS = 1.98847e30; HERE = os.path.dirname(os.path.abspath(__file__)); MULTI = ("cluster", "group")
ALPHA = float(os.environ.get("MB1_ALPHA", "-1.2")); ICL = float(os.environ.get("MB1_ICL", "0")); GROUPF = float(os.environ.get("MB1_GROUPF", "0.5")); BASE = os.environ.get("MB1_BASE", "gas")
LM = np.linspace(8.0, 12.5, 37); _x = 10 ** (LM - 10.9); W = _x ** (ALPHA + 1) * np.exp(-_x); W = W / W.sum(); M = 10 ** LM * MS
def law(g, a):
    g = np.asarray(g, float)
    with np.errstate(all="ignore"): return np.where(g > 0, 0.5 * g + np.sqrt(0.25 * g * g + a * g), g)
def mdyn(d, m, a): return d * d * law(G * m / (d * d), a) / G
def rt_hill(r, Mc, gamma, m, a):
    """r_t^3 (3 - gamma) Mc / r^3 = M_dyn(<r_t), r_t <= r; bisection in log r_t, arrays r (n) by m (k)."""
    r = r[:, None]; D = (np.maximum(3 - gamma, 0.5) * Mc)[:, None] / r ** 3; lo = np.log(r * 1e-8) * np.ones((1, m.size)); hi = np.log(r) * np.ones((1, m.size)); top = np.exp(hi)
    capped = top ** 3 * D < mdyn(top, m[None, :], a)
    for _ in range(36):
        mid = 0.5 * (lo + hi); d = np.exp(mid); up = d ** 3 * D < mdyn(d, m[None, :], a); lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    return np.where(capped, top, np.exp(0.5 * (lo + hi)))
def ratio(arm, r, Mc, gamma, a):
    """R(r): stellar-mass-weighted phantom over stars."""
    if arm == "F": d = rt_hill(r, Mc, gamma, M, a)
    elif arm == "N": d = np.broadcast_to(r[:, None], (r.size, M.size))
    elif arm == "E":
        gc = np.maximum(G * Mc / r ** 2, 1e-300); xN = gc * gc / (gc + a); d = np.minimum(np.sqrt(G * M[None, :] / xN[:, None]), r[:, None])
    else: raise ValueError(arm)
    return ((mdyn(d, M[None, :], a) - M[None, :]) * W).sum(1) / (W * M).sum()
def one(arm, r, gg, gs, a, K=0.0, Ms=None):
    """One system, r increasing. Returns total g. Ms overrides M_star(<r) from gs."""
    Ms_ = gs * r * r / G if Ms is None else Ms; gst = G * Ms_ / (r * r); Mem = (1 - ICL) * Ms_
    base = (law(gg, a) + gst) if BASE == "gas" else law(gg + gst, a)
    if arm == "K": return base + K * gst
    if arm == "KG": return base + K * gg
    if arm == "L": return base
    Mb = base * r * r / G; Mx = np.zeros_like(r); inc = np.all(np.diff(r) > 0)
    if not np.any(Mem > 0): return base
    for _ in range(80):
        Mc = Mb + Mx; gamma = np.gradient(np.log(Mc), np.log(r)) if inc and r.size > 1 else np.ones_like(r); R = ratio(arm, r, Mc, gamma, a)
        dM = np.diff(np.r_[0.0, Mem]); Rm = 0.5 * (R + np.r_[R[0], R[:-1]]); new = np.cumsum(Rm * dM); nx = 0.5 * (Mx + new); done = np.max(np.abs(nx - Mx) / np.maximum(Mc, 1e-300)) < 1e-3; Mx = nx
        if done: break
    return base + G * Mx / (r * r)
def nfw_shape(r, r500, c=2.9):
    R200 = 1.5 * r500; x = c * r / R200; x5 = c * r500 / R200; f = lambda u: np.log1p(u) - u / (1 + u)
    return f(x) / f(x5)
def kfit(arm, a):
    if arm not in ("K", "KG"): return 0.0
    return json.load(open(os.path.join(HERE, "mb1_kfit.json")))[arm]["canonical" if a < 1e-10 else "alt"]
def g(Q, arm):
    gb = np.asarray(dict.__getitem__(Q, "gb"), float); a = Q["a0"]; s = Q["sample"]
    if s not in MULTI: return law(gb, a)
    r = np.asarray(Q["r"], float) * np.ones_like(gb); K = kfit(arm, a)
    if s == "group":
        return one(arm, r, GROUPF * gb, (1 - GROUPF) * gb, a, K)
    gg = np.asarray(Q["gg"], float) * np.ones_like(gb); gs = np.asarray(Q["gs"], float) * np.ones_like(gb); r5 = np.asarray(Q["r500"], float) * np.ones_like(gb); out = np.empty_like(gb); keys = dict.__contains__(Q, "S")
    for u in np.unique(r5):
        i = np.where(r5 == u)[0]; i = i[np.argsort(r[i], kind="stable")]; Ms = None
        if keys and not np.all(gs[i] == 0):
            ms5 = np.interp(np.log(u), np.log(r[i]), gs[i] * r[i] ** 2 / G); Ms = ms5 * nfw_shape(r[i], u)
        out[i] = one(arm, r[i], gg[i], gs[i], a, K, Ms)
    return out
