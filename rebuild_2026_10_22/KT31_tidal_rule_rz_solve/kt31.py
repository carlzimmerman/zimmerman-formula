#!/usr/bin/env python3
"""KT31: Milky Way solve with the filter length varying in (r, theta): xi set at every solver cell from that cell's own
plain-QUMOND tidal tensor (rule F = KT28's Frobenius norm, 4/sqrt3; rule TF = KT30's trace-free norm, sqrt6), gather
smoothing via a width ladder of KT29's exact rho_xi, phantom source Phi_N + QUMOND(Phi_N[rho_s]) - Phi_N[rho_s].
MW defs copied from KT29. python3 kt31.py. Checkpoints after each ladder width (resume skips done widths).
kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass"))
import numpy as np
from scipy.special import ive, erf
from scipy.signal import fftconvolve
from scipy.interpolate import RegularGridInterpolator
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
EPS = [1.0] if MUT else [0.5]; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_s
KAP = 0.5
nu_b = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
# ---------- Milky Way (KT14 solver, wider grids) ----------
import ux5_core as C
L = C.L; ns = C.ns; F = C.F; R0 = C.R0
def i0e(x):
    out = np.empty_like(x); b = x > 500; out[~b] = ive(0, x[~b]); xb = x[b]; out[b] = (1 + 1 / (8 * xb) + 9 / (128 * xb * xb)) / np.sqrt(2 * math.pi * xb); return out
RIN = np.arange(0.0, 150.0 + 1e-9, 0.05); WIN = np.full_like(RIN, 0.05); WIN[0] = WIN[-1] = 0.025
ROUT = np.r_[np.arange(0.0, 20.0, 0.02), np.arange(20.0, 130.0 + 1e-9, 0.2)]; ZIN = np.arange(-80.0, 80.0 + 1e-9, 0.002)
def radial_matrix(rout, rin, win, s):
    M = np.empty((len(rout), len(rin)))
    for i in range(0, len(rout), 100):
        Ro = rout[i:i + 100, None]; M[i:i + 100] = (win * rin / s ** 2) * np.exp(-(Ro - rin) ** 2 / (2 * s * s)) * i0e(Ro * rin / (s * s))
    return M
def gauss(s, dz): k = np.arange(-int(6 * s / dz), int(6 * s / dz) + 1) * dz; w = np.exp(-k * k / (2 * s * s)); return w / w.sum()
def vsmooth(h, s): return fftconvolve(h, gauss(s, 0.002), mode="same")
RBA, ABa, R0B, RCB, QB = ns["RHO0_B"], ns["ALPHA_B"], ns["R0_B"], ns["RCUT_B"], ns["Q_B"]; HI, H2 = ns["S0_HI"], ns["S0_H2"]
BR = np.arange(0.0, 8.0 + 1e-9, 0.01); BW = np.full_like(BR, 0.01); BW[0] = BW[-1] = 0.005; BZ = np.arange(-8.0, 8.0 + 1e-9, 0.005); BRo = np.arange(0.0, 80.0 + 1e-9, 0.1); ZB = np.arange(-80.0, 80.0 + 1e-9, 0.05)
def bulge_shape(R, z):
    rp = np.maximum(np.sqrt(R * R + (np.abs(z) / QB) ** 2), 1e-7); return RBA / (1 + rp / R0B) ** ABa * np.exp(-(rp / RCB) ** 2)
Rs_ = np.maximum(RIN, 1e-6); HIr = HI * np.exp(-4.0 / Rs_ - Rs_ / 7.0); H2r = H2 * np.exp(-12.0 / Rs_ - Rs_ / 1.5)
HIz = 1 / (4 * 0.085) / np.cosh(np.minimum(np.abs(ZIN) / 0.17, 300)) ** 2; H2z = 1 / (4 * 0.045) / np.cosh(np.minimum(np.abs(ZIN) / 0.09, 300)) ** 2
Bfine = bulge_shape(BR[:, None], BZ[None, :]); Bbin = Bfine.reshape(len(BR), -1)[:, :-1].reshape(len(BR), 320, 10).sum(axis=2) * 0.005 / 0.05; BZc = BZ[:-1].reshape(320, 10).mean(axis=1)
OPS = {}
def ops(s):
    if s in OPS: return OPS[s]
    OPS.clear(); M = radial_matrix(ROUT, RIN, WIN, s); Mb = radial_matrix(BRo, BR, BW, s); Bs = Mb @ Bbin; Bp = np.zeros((len(BRo), len(ZB))); i0 = int(round((BZc[0] + 80.0) / 0.05)); Bp[:, i0:i0 + 320] = Bs; w = gauss(s, 0.05)
    for i in range(len(BRo)): Bp[i] = fftconvolve(Bp[i], w, mode="same")
    o = OPS[s] = dict(M=M, bI=RegularGridInterpolator((BRo, ZB), Bp, bounds_error=False, fill_value=0.0), HIr=M @ HIr, H2r=M @ H2r, HIz=vsmooth(HIz, s), H2z=vsmooth(H2z, s), cache={}); return o
def comp(o, key, fn):
    if key not in o["cache"]: o["cache"][key] = fn()
    return o["cache"][key]
def amps(c):
    rd = c["rd"]; p = F.params(c["sb"], c["mbb"], rd); ZT = ns["ZD_THIN"] if c.get("ht") is None else c["ht"]; ZK = ns["ZD_THICK"] if c.get("hk") is None else c["hk"]; ft = F.f_thin if c.get("fk") is None else 1 - c["fk"]; rk = rd if c.get("rdk") is None else c["rdk"]; ss = p["sig_star_R0"] * 1e6
    return dict(st=ft * ss * math.exp(R0 / rd), sk=(1 - ft) * ss * math.exp(R0 / rk), fb=p["fb"], rd=rd, rk=rk, ZT=ZT, ZK=ZK)
def rho_xi(c, s):
    a = amps(c); o = ops(s); rt = comp(o, ("r", a["rd"]), lambda: o["M"] @ np.exp(-RIN / a["rd"])); rk = comp(o, ("r", a["rk"]), lambda: o["M"] @ np.exp(-RIN / a["rk"])); zt = comp(o, ("z", a["ZT"]), lambda: vsmooth(np.exp(-np.abs(ZIN) / a["ZT"]) / (2 * a["ZT"]), s)); zk = comp(o, ("z", a["ZK"]), lambda: vsmooth(np.exp(-np.abs(ZIN) / a["ZK"]) / (2 * a["ZK"]), s))
    def f(R, z):
        R = np.asarray(R, float); z = np.asarray(z, float); sh = np.broadcast(R, z).shape; Rf = np.broadcast_to(R, sh).ravel(); zf = np.broadcast_to(z, sh).ravel(); I = lambda x, y, v: np.interp(x, y, v, right=0.0)
        return (a["st"] * I(Rf, ROUT, rt) * I(zf, ZIN, zt) + a["sk"] * I(Rf, ROUT, rk) * I(zf, ZIN, zk) + I(Rf, ROUT, o["HIr"]) * I(zf, ZIN, o["HIz"]) + I(Rf, ROUT, o["H2r"]) * I(zf, ZIN, o["H2z"]) + a["fb"] * o["bI"](np.c_[Rf, zf])).reshape(sh)
    return f
def solve(c, s, a0, g, Mu, LU):
    rhof, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); PhiN = LU.newton(g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4))
    if s == 0.0: Phi = LU.qumond(PhiN)
    else: fx = rho_xi(c, s); PNx = LU.newton(g.rho_axisym(lambda R, z: fx(R, z) / Mu, nq=4)); Phi = PhiN if MUT else PhiN + LU.qumond(PNx) - PNx
    oN = ns["mw_obs"](g, PhiN, a0); return dict(N=dict(vc=oN["vc_R0"], K0=oN["K_R0"]), Q=C.field_lines(g, Phi, a0), Mstar=ms)
Rg = np.linspace(1e-4, 150, 300001); MGAS = float(np.trapz(2 * math.pi * Rg * (HI * np.exp(-4.0 / Rg - Rg / 7.0) + H2 * np.exp(-12.0 / Rg - Rg / 1.5)), Rg)); P(f"M_gas (held, UX5 profiles) {MGAS:.4g} Msun")
HT, HK, FK = (0.25, 0.30, 0.35), (0.72, 0.90, 1.08), (0.12, 0.26, 0.35)
def cells():
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID): yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID, HT, HK, FK): yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, [L.RD_GRID[2], L.RD_GRID[3], L.RD_GRID[4]], HT, HK, FK): yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.0)
KEYS = ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk")

import signal
LAD = [0.0] + [0.005 * 1.5 ** k for k in range(28)]; LL = np.log(np.array(LAD[1:])); RULES = ("F", "TF"); SMOKE = int(os.environ.get("KT31_SMOKE", "0")); CK = os.environ.get("KT31_CK", os.path.join(HERE, "ckpt")); os.makedirs(CK, exist_ok=True)
STOP = [False]; signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__(0, True))
def dth(F, par, tc):
    """(d/dtheta) on cell centres with ghosts: axis mirror at -tc[0], plane mirror at pi - tc[-1]; par +1 even, -1 odd."""
    Fp = np.concatenate([par * F[:, :1], F, par * F[:, -1:]], axis=1); tp = np.r_[-tc[0], tc, math.pi - tc[-1]]
    return (Fp[:, 2:] - Fp[:, :-2]) / (tp[2:] - tp[:-2])[None, :]
def tidal_xi(g, Phi, sm=0.0):
    """xi_F, xi_TF (kpc) on all cells; Phi in solver units (G = a0 = 1, kpc), so g* = 1/kappa."""
    rc, tc = g.rc, g.tc; F = Phi.reshape(g.Nr, g.Nt); r = rc[:, None]; th = tc[None, :]
    Pr = np.gradient(F, rc, axis=0); Q = dth(F, 1, tc) / r
    Trr = np.gradient(Pr, rc, axis=0); Trt = np.gradient(Q, rc, axis=0); Ttt = dth(Q, -1, tc) / r + Pr / r; Tpp = Pr / r + Q / (r * np.tan(th))
    n2 = Trr ** 2 + Ttt ** 2 + 2 * Trt ** 2 + Tpp ** 2; tr = Trr + Ttt + Tpp; out = {}
    for rule, t2, cc in (("F", n2, 4 / math.sqrt(3)), ("TF", np.maximum(n2 - tr * tr / 3, 0.0), math.sqrt(6))):
        tau = np.sqrt(t2)
        if sm > 0:
            from scipy.ndimage import gaussian_filter
            tau = np.exp(gaussian_filter(np.log(np.maximum(tau, 1e-300)), sm, mode="nearest"))
        gt = np.gradient(tau, rc, axis=0) ** 2 + (dth(tau, 1, tc) / r) ** 2
        out[rule] = np.minimum(cc * tau ** 3 * KAP / np.maximum(gt, 1e-300), 200.0).ravel()
    return out
def tidal_tau(g, Phi):
    rc, tc = g.rc, g.tc; F = Phi.reshape(g.Nr, g.Nt); r = rc[:, None]; th = tc[None, :]
    Pr = np.gradient(F, rc, axis=0); Q = dth(F, 1, tc) / r; Trr = np.gradient(Pr, rc, axis=0); Trt = np.gradient(Q, rc, axis=0); Ttt = dth(Q, -1, tc) / r + Pr / r; Tpp = Pr / r + Q / (r * np.tan(th))
    return np.sqrt(Trr ** 2 + Ttt ** 2 + 2 * Trt ** 2 + Tpp ** 2).ravel()
def tidal_xi_r(g, Phi):
    tau = tidal_tau(g, Phi).reshape(g.Nr, g.Nt); return (4 / math.sqrt(3) * tau ** 3 * KAP / np.maximum(np.gradient(tau, g.rc, axis=0) ** 2, 1e-300)).ravel()
def weights(x):
    """ladder index k (lower) and weight on k+1, per cell; LAD[0] = 0, LAD[1] = 0.005 kpc."""
    k = np.zeros(x.shape, int); w = np.zeros(x.shape)
    lo = x < LAD[1]; w[lo] = x[lo] / LAD[1]
    hi = ~lo; u = (np.log(x[hi]) - LL[0]) / math.log(1.5); kk = np.minimum(np.floor(u).astype(int), len(LL) - 2); k[hi] = kk + 1; w[hi] = np.clip(u - kk, 0, 1)
    return k, w
def lines_from(rs, PhiN, g, a0, LU, mut=False):
    PNx = LU.newton(rs); Phi = PhiN + LU.qumond(PNx, mut) - PNx; return C.field_lines(g, Phi, a0), Phi
def rho_k(c, k, g, Mu):
    if k == 0:
        rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); return g.rho_axisym(lambda R_, z_: rf(R_, z_) / Mu, nq=4)
    f = rho_xi(c, LAD[k]); return g.rho_axisym(lambda R_, z_: f(R_, z_) / Mu, nq=4)
GC = {}
def rho_k_fast(c, k, g, Mu):
    """rho_xi(c, LAD[k]) cell averages built from per-component grid averages (cached per width; rho_xi is linear in them)."""
    if k == 0: return rho_k(c, 0, g, Mu)
    s = LAD[k]; a = amps(c); o = ops(s)
    if GC.get("s") != s: GC.clear(); GC["s"] = s
    I = lambda x, y, v: np.interp(x, y, v, right=0.0)
    def cg(key, fn):
        if key not in GC: GC[key] = g.rho_axisym(lambda R_, z_: fn(np.asarray(R_, float).ravel(), np.asarray(z_, float).ravel()), nq=4) / Mu
        return GC[key]
    rt = comp(o, ("r", a["rd"]), lambda: o["M"] @ np.exp(-RIN / a["rd"])); rk = comp(o, ("r", a["rk"]), lambda: o["M"] @ np.exp(-RIN / a["rk"])); zt = comp(o, ("z", a["ZT"]), lambda: vsmooth(np.exp(-np.abs(ZIN) / a["ZT"]) / (2 * a["ZT"]), s)); zk = comp(o, ("z", a["ZK"]), lambda: vsmooth(np.exp(-np.abs(ZIN) / a["ZK"]) / (2 * a["ZK"]), s))
    th = cg(("t", a["rd"], a["ZT"]), lambda R_, z_: I(R_, ROUT, rt) * I(z_, ZIN, zt)); tk = cg(("k", a["rk"], a["ZK"]), lambda R_, z_: I(R_, ROUT, rk) * I(z_, ZIN, zk))
    gs = cg(("gas",), lambda R_, z_: I(R_, ROUT, o["HIr"]) * I(z_, ZIN, o["HIz"]) + I(R_, ROUT, o["H2r"]) * I(z_, ZIN, o["H2z"])); bu = cg(("b",), lambda R_, z_: o["bI"](np.c_[R_, z_]))
    return a["st"] * th + a["sk"] * tk + gs + a["fb"] * bu
def blend(c, XI, g, Mu, cache=None):
    """gather blend of the ladder for one cell and a dict of xi fields; cache maps k -> rho_k."""
    out = {}; kw = {r_: weights(XI[r_]) for r_ in XI}
    for kk in range(len(LAD)):
        need = [r_ for r_, (k, w) in kw.items() if np.any((k == kk) & (w < 1)) or np.any((k == kk - 1) & (w > 0))]
        if not need: continue
        rk = cache[kk] if cache is not None and kk in cache else rho_k_fast(c, kk, g, Mu)
        for r_ in need:
            k, w = kw[r_]; a = np.where(k == kk, 1 - w, 0.0) + np.where(k == kk - 1, w, 0.0); out[r_] = out.get(r_, 0.0) + a * rk
    return out
ZQ = (0.0, 0.1, 0.3, 1.0, 3.0); RQM = (4.0, 8.0, 12.0, 20.0)
for foot, a0s in A0SI.items():
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g); st = [json.loads(l) for l in open(os.path.join(RB, "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))]; IP = []
    for c, sx in zip(cells(), st):
        _, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        if L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]: IP.append((c, sx, ms))
    if SMOKE: IP = IP[:SMOKE]
    n = len(IP); a0k = a0s * CONV; gsk = a0k / KAP; RQ = R0 + np.array([-0.5, -0.25, 0.0, 0.25, 0.5])
    i0 = int(np.argmin(np.abs(g.rc - R0))); j0 = g.Nt - 1; c0 = i0 * g.Nt + j0
    KI = np.zeros((2, n, g.n), np.int8); KW = np.zeros((2, n, g.n), np.float32); RHO0 = np.zeros((n, g.n)); PN = np.zeros((n, g.n)); e1 = 0.0; n1 = []; n1b = []; emut = 0.0
    for m, (c, sx, ms) in enumerate(IP):
        rho = rho_k(c, 0, g, Mu); RHO0[m] = rho; PhiN = LU.newton(rho); PN[m] = PhiN; PQ = LU.qumond(PhiN); q = C.field_lines(g, PQ, a0)
        e1 = max(e1, abs(q["vc"] / sx["Q"]["vc"] - 1), abs(q["K0"] / sx["Q"]["K0"] - 1))
        XI = tidal_xi(g, PQ)
        for ri, r_ in enumerate(RULES): k, w = weights(XI[r_]); KI[ri, m] = k; KW[ri, m] = w
        rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        V = C.L.vc_plane(ns, g, PQ, a0, RQ); VN = C.L.vc_plane(ns, g, PhiN, a0, RQ); gq = V ** 2 / RQ; gN = VN ** 2 / RQ
        TRR = np.gradient(gq, RQ)[1:4]; Tpp = (gq / RQ)[1:4]; r0 = np.array([float(rf(np.array([x]), np.array([0.0]))[0]) for x in RQ[1:4]])
        lap = nu_b(gN[1:4] / a0k) * 4 * math.pi * Gk * r0; Tzz = lap - TRR - Tpp; tau = np.sqrt(TRR ** 2 + Tpp ** 2 + Tzz ** 2); dt = (tau[2] - tau[0]) / 0.5
        x_ro = 4 / math.sqrt(3) * tau[1] ** 3 / (dt * dt * gsk)
        n1b.append((tidal_tau(g, PQ)[c0] * a0k / tau[1], tidal_xi_r(g, PQ)[c0] / min(x_ro, 200.0)))
        n1.append(XI["F"][c0] / min(4 / math.sqrt(3) * tau[1] ** 3 / (dt * dt * gsk), 200.0))
        if m < 2:
            qm, _ = lines_from(rho, PhiN, g, a0, LU, True); oN = ns["mw_obs"](g, PhiN, a0); emut = max(emut, abs(qm["vc"] / oN["vc_R0"] - 1))
    ok = e1 <= 1e-6; fail += not ok; P(f"R1 [{foot}] xi 0 vs UX5 form Q, {n} cells, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    ok = emut <= 1e-6; fail += not ok; P(f"MUTATE [{foot}] nu = 1 gives Q = N on 2 cells: max rel {emut:.1e}: {'PASS' if ok else 'FAIL'}")
    md = float(np.median(n1)); N1 = 0.8 <= md <= 1.25; fail += not N1; RES[f"N1|{foot}"] = dict(median=md, min=float(min(n1)), max=float(max(n1)), ok=N1)
    nb = np.array(n1b); RES[f"N1b|{foot}"] = dict(tau_ratio=float(np.median(nb[:, 0])), xi_radial_only_ratio=float(np.median(nb[:, 1])))
    P(f"N1b [{foot}] beside, added after the freeze (not graded): at the same cell, grid tau_F / KT29 tau median {np.median(nb[:, 0]):.3f}; grid xi_F with the radial gradient only / KT29 median {np.median(nb[:, 1]):.3f}")
    c_ = IP[0][0]; d6 = float(np.max(np.abs(rho_k_fast(c_, 15, g, Mu) / np.maximum(rho_k(c_, 15, g, Mu), 1e-300) - 1)[rho_k(c_, 15, g, Mu) > 1e-12 * rho_k(c_, 15, g, Mu).max()])); ok = d6 <= 1e-9; fail += not ok; P(f"R6 [{foot}] (code check, added) cached component build vs rho_xi at width {LAD[15]:.3g} kpc: max rel {d6:.1e}: {'PASS' if ok else 'FAIL'}")
    P(f"N1 [{foot}] grid xi_F at cell nearest (R0, 0) [r {g.rc[i0]:.2f}, theta {g.tc[j0]:.4f}] / KT29's per-cell xi: median {md:.3f} (min {min(n1):.3f}, max {max(n1):.3f}), line [0.8, 1.25]: {'PASS' if N1 else 'FAIL'}")
    # ---- ladder loop (outermost), checkpointed ----
    ACC = np.zeros((2, n, g.n)); done = -1; cp = os.path.join(CK, f"{foot}.npz")
    if os.path.exists(cp): z = np.load(cp); ACC = z["ACC"]; done = int(z["done"]); P(f"[{foot}] resumed after ladder width {done}")
    for kk in range(done + 1, len(LAD)):
        for m, (c, sx, ms) in enumerate(IP):
            a = [np.where(KI[ri, m] == kk, 1 - KW[ri, m], 0.0) + np.where(KI[ri, m] == kk - 1, KW[ri, m], 0.0) for ri in range(2)]
            if not (a[0].any() or a[1].any()): continue
            rk = RHO0[m] if kk == 0 else rho_k_fast(c, kk, g, Mu)
            for ri in range(2): ACC[ri, m] += a[ri] * rk
        np.savez(cp + ".tmp.npz", ACC=ACC, done=kk); os.replace(cp + ".tmp.npz", cp); P(f"    [{foot}] ladder width {kk} ({LAD[kk]:.4g} kpc) done")
        if STOP[0]: P("SIGTERM: checkpointed, exiting"); sys.exit(3)
    for ri, r_ in enumerate(RULES):
        out = []; mr = []
        for m, (c, sx, ms) in enumerate(IP):
            q, _ = lines_from(ACC[ri, m], PN[m], g, a0, LU); o = dict(Q=q, Mstar=ms, **{k: c[k] for k in KEYS if k in c}); mr.append(float(np.sum(ACC[ri, m] * g.vol) / np.sum(RHO0[m] * g.vol))); o["mass"] = mr[-1]; o["m"] = m
            out.append(o)
        qq = [o["Q"] for o in out]; n4 = [o for o in out if all(o["Q"][l] for l in ("L1", "L2a", "L2b", "L3"))]; cnt = {l: sum(x[l] for x in qq) for l in ("L1", "L2a", "L2b", "L3", "Lh")}; b = min(out, key=lambda o: o["Q"]["D"]); bq = b["Q"]
        mc = bool(n4) and all(o["mass"] < 0.9 for o in n4)
        # R5 on passing cells (up to 2) or the best-D cell
        tgt = sorted(n4, key=lambda o: o["Q"]["D"])[:2] if n4 else [b]; r5 = []
        for o in tgt:
            c = IP[o["m"]][0]; PQ = LU.qumond(PN[o["m"]]); X5 = tidal_xi(g, PQ, 1.0); rs = blend(c, {r_: X5[r_]}, g, Mu)[r_]; q5, _ = lines_from(rs, PN[o["m"]], g, a0, LU)
            r5.append(dict(xi0=float(tidal_xi(g, PQ)[r_][c0]), xi5=float(X5[r_][c0]), dvc=q5["vc"] - o["Q"]["vc"], dK=q5["K0"] - o["Q"]["K0"], pass4=all(q5[l] for l in ("L1", "L2a", "L2b", "L3"))))
        lab_raw = bool(n4); flip = (any(x["pass4"] for x in r5) != lab_raw) if n4 else any(x["pass4"] for x in r5)
        if not N1: lab = "NOT EVALUABLE (numerics)"
        elif flip: lab = "NUMERICS-DEPENDENT"
        elif n4: lab = "PASSES MW, MASS-CONDITIONAL" if mc else "PASSES MW"
        else: lab = "FAILS MW"
        R = RES[f"mw|{foot}|{r_}"] = dict(label=lab, n_pass=len(n4), lines=cnt, vc_max=max(x["vc"] for x in qq), mass=[min(mr), float(np.median(mr)), max(mr)], best={k: b.get(k) for k in KEYS + ("Mstar", "mass")} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")}, R5=r5,
                                          passing=[{k: o.get(k) for k in KEYS + ("Mstar", "mass")} | {k: o["Q"][k] for k in ("vc", "K0", "cK", "cO", "h")} for o in sorted(n4, key=lambda o: o["Q"]["D"])][:30])
        P(f"MW [{foot}] rule {r_}: all four {len(n4)}; L1 {cnt['L1']} L2a {cnt['L2a']} L2b {cnt['L2b']} L3 {cnt['L3']} Lh {cnt['Lh']}; v_c max {R['vc_max']:.1f}; mass ratio min/med/max {min(mr):.3f}/{np.median(mr):.3f}/{max(mr):.3f}; best D {bq['D']:.2f} ({b['box']} Rd {b['rd']} Sb {b['sb']} Mbb {b['mbb']:.3g} ht {b.get('ht')} hk {b.get('hk')} fk {b.get('fk')}) v_c {bq['vc']:.1f} K {bq['K0']:.1f} cK {bq['cK']:.1f} Ou {bq['cO']:.0f} mass {b['mass']:.3f}")
        P("    R5 (ln tau smoothed 1 cell): " + "; ".join(f"xi(R0,0) {x['xi0']:.3g}->{x['xi5']:.3g} dv {x['dvc']:+.2f} dK {x['dK']:+.2f} pass {x['pass4']}" for x in r5))
        PQ = LU.qumond(PN[b["m"]]); XB = tidal_xi(g, PQ)[r_]; tb = {}
        for Rq in RQM:
            row = []
            for zq in ZQ:
                rr = math.hypot(Rq, zq); tt = math.atan2(Rq, zq); i = int(np.argmin(np.abs(np.log(g.rc / rr)))); j = int(np.argmin(np.abs(g.tc - tt))); row.append(float(XB[i * g.Nt + j]))
            tb[str(Rq)] = row
        R["xi_map_best"] = tb; P(f"    xi map, best-D cell, rows R = {RQM} kpc, cols z = {ZQ} kpc: " + " | ".join(f"R{k}: " + " ".join(f"{v:.3g}" for v in vv) for k, vv in tb.items()))
        P(f"LABEL [{foot}] rule {r_}: {lab}")
    # R4 ladder blend on lightest and heaviest cells, constant xi
    if True:
        ms_ = [x[2] for x in IP]; e4 = []
        for m in (int(np.argmin(ms_)), int(np.argmax(ms_))):
            c = IP[m][0]
            for kk in (13, 19):
                xv = LAD[1] * 1.5 ** (kk - 1 + 0.5); XF = np.full(g.n, xv); rs = blend(c, {"F": XF}, g, Mu)["F"]; qb, _ = lines_from(rs, PN[m], g, a0, LU)
                f = rho_xi(c, xv); rd_ = g.rho_axisym(lambda R_, z_: f(R_, z_) / Mu, nq=4); qd, _ = lines_from(rd_, PN[m], g, a0, LU); e4.append((xv, qb["vc"] - qd["vc"], qb["K0"] - qd["K0"]))
        ok = all(abs(a) <= 0.5 and abs(b_) <= 0.5 for _, a, b_ in e4); fail += not ok; RES[f"R4|{foot}"] = e4
        P(f"R4 [{foot}] ladder blend vs direct at constant xi: " + "; ".join(f"xi {x:.3g} dv {a:+.3f} dK {b_:+.3f}" for x, a, b_ in e4) + f": {'PASS' if ok else 'FAIL'}")
RES["fail"] = fail; P(f"failed checks: {fail}")
if SMOKE: sys.exit(0)
open(os.path.join(HERE, "kt31.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "kt31.json"), "w"), indent=1, default=float)
sys.exit(1 if fail else 0)
