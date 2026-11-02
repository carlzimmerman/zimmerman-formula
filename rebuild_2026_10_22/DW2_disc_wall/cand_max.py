"""DW2 A1 candidate: g = max(law(g_b), g_b + g_c). Env DW2_CAND = mass|f|mode. Own contraction (bisection on r_f). No action; a description. kappa = 1/2 FITTED; cold dark energy, never a particle; reinstates nothing."""
import json, math, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "."; _RB = os.path.dirname(_HERE)
_mass, _f, _mode = os.environ.get("DW2_CAND", "share|0.872|linear").split("|"); _f = float(_f); _X = float(os.environ.get("DW2_COLDX", "1"))
NAME = f"MAX {_mass} f {_f} {_mode}" + (f" cold x{_X}" if _X != 1 else "")
_GN, _MS, _PC = 6.674e-11, 1.989e30, 3.0857e16; _H = 0.672; _RC = 3 * (100e3 * _H / (_PC * 1e6)) ** 2 / (8 * math.pi * _GN); _FC = 5.35 / 6.35
_SJ = json.load(open(os.path.join(_RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); _LX = np.log(np.array(_SJ["x"])); _TG = sorted(((float(_SJ[m]["0.00"]["lgM"]), np.array(_SJ[m]["0.00"]["lnm"])) for m in ("1e10", "1e11", "1e12", "1e13", "1e14")), key=lambda t: t[0]); _LG = np.array([t[0] for t in _TG]); _LN = np.array([t[1] for t in _TG])
def _shape(lg): return np.array([np.interp(lg, _LG, _LN[:, j]) for j in range(_LN.shape[1])])
def _cold(r, Mb):
    """r ascending m, Mb enclosed Msun, cumulative. Returns g_c on r."""
    Mt = float(Mb.max())
    if Mt <= 0: return r * 0
    _M2 = lambda m: 10 ** (11.18 + 0.9 * (math.log10(m) - 10)) if _mass == "em1" else 6.35 * m
    if _mode == "r200":
        for _ in range(40):
            R_ = (3 * _M2(Mt) * _MS / (4 * math.pi * 200 * _RC)) ** (1 / 3); Mn = float(np.interp(math.log(R_), np.log(r), Mb)) if R_ > r[0] else float(Mb[0]); Mt = math.sqrt(Mt * max(Mn, 1e-30))
    M200 = _M2(Mt)
    R2 = (3 * M200 * _MS / (4 * math.pi * 200 * _RC)) ** (1 / 3)
    if _mode == "linear" and r[-1] < R2: pass
    sh = _shape(math.log10(M200))
    def M0(x):
        lx = np.log(np.maximum(np.minimum(x, R2) / R2, 1e-300)); return _FC * M200 * np.exp(np.where(lx >= _LX[0], np.interp(lx, _LX, sh), sh[0] + 2 * (lx - _LX[0])))
    if _f == 0: return _X * _GN * M0(r) * _MS / r ** 2
    lo_ = min(r[0], R2) * 0.05; rg = np.geomspace(lo_, max(R2 * 1.2, r[-1] * 1.01), 100); M0g = M0(rg); lrb = np.log(r); Mbg = np.where(rg < r[0], Mb[0] * (rg / r[0]) ** 2, np.interp(np.log(rg), lrb, Mb)); F = Mt / float(M0g[-1])
    a, b = rg * 1e-3, rg * 1.0001; Rt = rg * M0g * (1 + F)
    for _ in range(26):
        c = np.sqrt(a * b); v = c * (np.interp(np.log(c), np.log(rg), Mbg) + M0g); a, b = np.where(v < Rt, c, a), np.where(v < Rt, b, c)
    rf = np.maximum.accumulate(np.sqrt(a * b)); Mf = np.interp(np.log(r), np.log(rf), M0g, left=0.0, right=M0g[-1]); M = M0(r) + _f * (Mf - M0(r)); return _X * _GN * M * _MS / r ** 2
def _one(gb, r, a):
    o = np.argsort(r); rs = r[o]; Mb = np.maximum.accumulate(np.maximum(gb[o] * rs ** 2 / _GN / _MS, 0)); gc_ = np.empty_like(gb); gc_[o] = _cold(rs, Mb); return gc_
def _law(gb, a):
    with np.errstate(all="ignore"): return np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
def g(Q):
    gb = np.asarray(Q["gb"], float); r = np.asarray(Q["r"], float); a = Q["a0"]; L = _law(gb, a)
    if not np.all(np.isfinite(r)) or r.size == 0: return L
    pos = np.maximum(gb, 0)
    if gb.ndim == 2:
        gc_ = np.stack([_one(pos[i], r[i], a) for i in range(gb.shape[0])])
    elif "r500" in Q:
        r5 = np.asarray(Q["r500"], float); gc_ = np.zeros_like(gb)
        if r5.ndim == 0 or np.unique(r5).size == 1:
            gc_ = _x_cluster(pos, r, a, float(np.max(r5)))
        else:
            for u in np.unique(r5): m = r5 == u; gc_[m] = _x_cluster(pos[m], r[m], a, float(u))
    else:
        gc_ = _one(pos, r, a)
    return np.where(gb > 0, np.maximum(L, gb + gc_), gb)
def _x_cluster(gb, r, a, r5):
    o = np.argsort(r); rs = r[o]; Mb = np.maximum.accumulate(gb[o] * rs ** 2 / _GN / _MS); Mt = float(Mb[-1])
    if _mode in ("linear", "r200") and rs[-1] < 2 * r5:
        M = Mt
        for _ in range(20):
            R2 = (3 * 6.35 * M * _MS / (4 * math.pi * 200 * _RC)) ** (1 / 3) if _mass == "share" else (3 * 10 ** (11.18 + 0.9 * (math.log10(M) - 10)) * _MS / (4 * math.pi * 200 * _RC)) ** (1 / 3); M = Mt * max(R2 / rs[-1], 1)
        rx = np.append(rs, R2) if R2 > rs[-1] else rs; Mx = np.append(Mb, M) if R2 > rs[-1] else Mb; gcx = _cold(rx, Mx)[:len(rs)]
    else:
        gcx = _cold(rs, Mb)
    out = np.empty_like(gb); out[o] = gcx; return out
