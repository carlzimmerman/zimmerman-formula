"""HB1 solver front: Form A, Form B (E1, E2, E3), numeric Form B for tabulated shapes. kappa = 1/2 FITTED, unused; no a0 in here; not theory closed."""
import ctypes as ct, math, os, subprocess
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); SO = os.path.join(HERE, "cache_hb1_solve.so")
if not os.path.exists(SO) or os.path.getmtime(SO) < os.path.getmtime(os.path.join(HERE, "hb1_solve.c")):
    t_ = SO + f".{os.getpid()}"; subprocess.run(["cc", "-O2", "-shared", "-fPIC", os.path.join(HERE, "hb1_solve.c"), "-o", t_, "-lm"], check=True); os.replace(t_, SO)
L = ct.CDLL(SO); DP = ct.POINTER(ct.c_double); D = ct.c_double; I = ct.c_int
L.hb_mass.restype = D; L.hb_mass.argtypes = [I, DP, DP, D, D, I, D, DP, D, D, D, I, D, I]
L.hb_solve.restype = D; L.hb_solve.argtypes = [I, DP, DP, D, D, D, I, D, DP, D, D, D, I, D, I, DP, DP, ct.POINTER(I), ct.POINTER(I), I, ct.POINTER(I)]
_p = lambda a: a.ctypes.data_as(DP)
BS = lambda x: 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
# the core's own EOS, H in (0, 1)
_x = np.geomspace(1e-5, 1e12, 3000001); _Hx = np.arcsinh(_x) / _x; _Rx = (1 + _x * _x) ** -1.5
NT = 200001; DH = 1.0 / (NT - 1); _Hg = np.arange(NT) * DH; TAB_B = np.interp(_Hg, np.r_[0.0, _Hx[::-1], 1.0], np.r_[0.0, _Rx[::-1], 1.0]); TAB_B[-1] = 1.0
del _x, _Hx, _Rx
# E2's continuation, H in (0, pi/2), table to rho^ 1e6
_y = 1 - np.geomspace(1e-7, 1, 400001)[::-1]; _y = _y[(_y > 1e-6)]; _HE2 = np.arcsin(_y) / _y; _RE2 = (1 - _y * _y) ** -1.5; HT2 = float(_HE2[-1]); N2 = 400001; D2 = HT2 / (N2 - 1); _H2 = np.arange(N2) * D2
TAB_E2 = np.where(_H2 <= 1.0, np.interp(_H2, _Hg, TAB_B), np.interp(_H2, _HE2, _RE2)); RT2 = float(TAB_E2[-1])
SUB = [int(os.environ.get("HB_NSUB", "2"))]; LASTN = [0]; BRANCH = [0]
ST = dict(calls=0, noroot=0, wall=0, shots=0, Hc=[], nulls=0, nullmax=0.0, r0err=0.0, r0bad=0)
def eos(form, q=None):
    """(n, dH, tab, Htop, rtop, slope, ext, wall, Href)"""
    e0 = np.zeros(2)
    if form == "A": return (0, 1.0, e0, 0.0, 0.0, 1.0 / q, 1, 0.0, q)
    if form == "A2": return (0, 1.0, e0, 0.0, 0.0, 0.5 / q, 1, 0.0, 2 * q)   # P/rho = c_s0^2 reading, rho^ = H/(2q)
    if form == "A215": q2 = 2.15 * (math.asinh(1.0) - math.sqrt(0.5)); return (0, 1.0, e0, 0.0, 0.0, 1.0 / q2, 1, 0.0, q2)   # Argon's quoted c_s0^2 = 2.15 G M_c0(r0)/r0
    if form == "E1": return (NT, DH, TAB_B, 1.0, 1.0, 9.0, 1, 0.0, 1.0)
    if form == "E3": return (NT, DH, TAB_B, 1.0, 1.0, 9.0, 3, 0.0, 1.0)
    if form == "E2": return (N2, D2, TAB_E2, HT2 - D2, RT2, 0.0, 2, RT2, 1.0)
    raise ValueError(form)
def solve_scaled(x, mb, xe, mt, E, nsub=None, branch=0):
    n = len(x); o = np.zeros(n); Ho = np.zeros(n); st = I(0); ns = I(0); nr = I(0); LASTN[0] = 0; x = np.asarray(x, float); mb = np.asarray(mb, float)
    Hc = L.hb_solve(n, _p(x), _p(mb), xe, mt, E[8], E[0], E[1], _p(E[2]), E[3], E[4], E[5], E[6], E[7], nsub or SUB[0], _p(o), _p(Ho), ct.byref(st), ct.byref(ns), branch, ct.byref(nr)); LASTN[0] = nr.value
    return o, Hc, st.value, ns.value, Ho
def mass_at(x, mb, xe, Hc, E, nsub=None):
    x = np.asarray(x, float); mb = np.asarray(mb, float); return L.hb_mass(len(x), _p(x), _p(mb), xe, Hc, E[0], E[1], _p(E[2]), E[3], E[4], E[5], E[6], E[7], nsub or SUB[0])
def infer_r0(r, M0, B=BS):
    """as DR8's: r0 from M0's own shape below any truncation"""
    inc = np.where(np.diff(M0) > 0)[0]; n = int(inc[-1]); i1 = int(np.searchsorted(M0[:n + 1], 1e-3 * M0[n])); i1 = min(i1, n - 1); lq = math.log(M0[i1] / M0[n])
    f = lambda l: float(np.log(B(r[i1] / math.exp(l)) / B(r[n] / math.exp(l))) - lq)
    l0 = brentq(f, math.log(r[n]) - 12, math.log(r[n]) + 6, xtol=1e-13); r0 = math.exp(l0); return r0, float(M0[n] / B(r[n] / r0)), n
def contract_hb(r, Mb, M0, form, nsample=500, mutb=1.0):
    """M_f on r: mass inside the edge held. Same return shape as the path's contract."""
    r0, C, n = infer_r0(r, M0); x = r / r0; mt = float(M0[-1]) / C
    if n >= len(r) - 2 and M0[-1] > M0[-2]: xe = float(x[-1])
    else:
        lo, hi = float(x[n]), float(x[n + 1]); xe = brentq(lambda t: float(BS(np.asarray(t))) - mt, lo, hi, xtol=1e-13 * hi)
    mb = np.asarray(Mb, float) / C * mutb; q = 1 - math.asinh(xe) / xe; E = eos(form, q); o, Hc, st, ns, _ = solve_scaled(x, mb, xe, mt, E, branch=BRANCH[0]); ST.setdefault("nroots", []).append(LASTN[0]) if BRANCH[0] else None; ST.setdefault("xe", []).append(xe)
    ST["calls"] += 1; ST["shots"] += ns; ST["wall"] += int(st == 2)
    if st == 1: ST["noroot"] += 1; return np.array(M0, float), np.inf, 1
    ST["Hc"].append(Hc)
    if form.startswith("E") and ST["calls"] % nsample == 1:   # null on a sample of calls inside the path
        o0, H0, s0, _, _ = solve_scaled(x, 0 * mb, xe, mt, E); i = (x <= xe) & (M0 > 1e-6 * M0[-1]); e = float(np.max(np.abs(o0[i] * C / M0[i] - 1))); ST["nulls"] += 1; ST["nullmax"] = max(ST["nullmax"], e)
    return C * o, 0.0, 0
def _pava_decreasing(y, w):
    """isotonic regression, y non-increasing, weights w"""
    v = []; 
    for a, b in zip(y.tolist(), w.tolist()):
        v.append([a, b, 1])
        while len(v) > 1 and v[-2][0] < v[-1][0]:
            c, d, e = v.pop(); a0, b0, e0 = v.pop(); v.append([(a0 * b0 + c * d) / (b0 + d), b0 + d, e0 + e])
    return np.concatenate([np.full(e, a) for a, b, e in v])
def numeric_B(r, Mb, M0, nsub=None):
    """A4: Form B on a tabulated M0(r), flat beyond the edge. lnrho made monotone by mass-weighted isotonic regression, mass and H recomputed from that profile so the EOS is self-consistent; the mass is renormalised to the edge's. Above the innermost density: tangent gamma, as E1. Below the edge density: power law in H from the local slope. Returns M_f, stats."""
    n = int(np.where(np.diff(M0) > 0)[0][-1]) + 1; ru = float(r[n]); Cu = float(M0[n]); x = r / ru; m0 = M0 / Cu; X = x[:n + 1]; M = m0[:n + 1]; lx = np.log(X); lm = np.log(M)
    raw = np.gradient(lm, lx) * M / (4 * X ** 3); nb = int(np.sum(np.diff(raw) > 0)); w = np.maximum(raw * X ** 3, 1e-300); rho_ = np.exp(_pava_decreasing(np.log(np.maximum(raw, 1e-300)), w))
    dm = 4 * X ** 3 * rho_; Ms = np.r_[float(M[0]), float(M[0]) + np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(lx))]; nf = 1.0 / Ms[-1]; rho_ = rho_ * nf; Ms = Ms * nf
    H = np.zeros_like(X); H[-1] = Ms[-1] / (4 * X[-1]); g = Ms / (4 * X); H[:-1] = H[-1] + np.cumsum((g[1:] + g[:-1])[::-1] * 0.5 * np.diff(lx)[::-1])[::-1]
    u, ui = np.unique(H, return_index=True); Hu, Ru = u, rho_[ui]; sl = max(float((np.log(rho_[-1]) - np.log(rho_[-8])) / max(np.log(H[-1]) - np.log(H[-8]), 1e-12)), 0.5); Htop = float(H[0]); Nt = 200001; dH = Htop / (Nt - 1); Hg = np.arange(Nt) * dH
    t = np.where(Hg >= H[-1], np.interp(Hg, Hu, Ru), rho_[-1] * (np.maximum(Hg, 1e-300) / H[-1]) ** sl); k_ = min(5, len(H) - 1); s_ = max(float((rho_[0] - rho_[k_]) / max(H[0] - H[k_], 1e-300)), 0.0); E = (Nt, dH, t, Htop - dH, float(t[-2]), s_, 1, 0.0, Htop - 2 * dH)
    mb = np.asarray(Mb, float) / Cu; o, Hc, st, ns, _ = solve_scaled(x, mb, float(X[-1]), 1.0, E, nsub); o0, H0, s0, _, _ = solve_scaled(x, 0 * mb, float(X[-1]), 1.0, E, nsub); i = M > 1e-4
    return Cu * o if st != 1 else np.array(M0, float), dict(nonmono=nb, null=float(np.max(np.abs(o0[:n + 1][i] / M[i] - 1))) if s0 != 1 else None, st=st, top_ratio=Hc / Htop if st != 1 else None, null_Hc=H0 / Htop if s0 != 1 else None)
