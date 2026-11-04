#!/usr/bin/env python3
"""KT32 (copy of KT31's definitions; smoothing changed to mass-conserving SCATTER, width set at the source, ladder ratio
1.25, separable cylindrical I0 x Gaussian smoother on a non-uniform mesh). Older text: KT31: Milky Way solve with the filter length varying in (r, theta): xi set at every solver cell from that cell's own
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
LAD = [0.0] + [0.005 * 1.25 ** k for k in range(49)]; LL = np.log(np.array(LAD[1:])); LR = math.log(1.25); RULES = ("F", "TF"); SMOKE = int(os.environ.get("KT32_SMOKE", "0")); CK = os.environ.get("KT32_CK", os.path.join(HERE, "ckpt")); os.makedirs(CK, exist_ok=True)
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
    hi = ~lo; u = (np.log(x[hi]) - LL[0]) / LR; kk = np.minimum(np.floor(u).astype(int), len(LL) - 2); k[hi] = kk + 1; w[hi] = np.clip(u - kk, 0, 1)
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

# ---------- scatter smoother on a cylindrical mesh (half space z >= 0, even in z) ----------
def edges_w(x):
    e = np.r_[x[0], 0.5 * (x[1:] + x[:-1]), x[-1]]; return np.diff(e)
MR = np.unique(np.r_[0.0, np.geomspace(1e-3, 0.5, 60), np.arange(0.5, 30.0, 0.05), np.geomspace(30.0, 150.0, 50)])
MZ = np.unique(np.r_[0.0, np.geomspace(1e-4, 0.05, 40), np.arange(0.05, 1.0, 0.005), np.geomspace(1.0, 80.0, 90)])
dRm = edges_w(MR); dZm = edges_w(MZ); WR = 2 * math.pi * MR * dRm; WR[0] = math.pi * (dRm[0]) ** 2; WZ = 2 * dZm; WZ[0] = dZm[0] * 2
spR = np.gradient(MR); spZ = np.gradient(MZ)
def kern(s):
    """column-normalised scatter kernels: column j spreads a unit of source mass (ring j / slab j) over the mesh."""
    Ro, Ri = MR[:, None], MR[None, :]; KR = np.exp(-(Ro - Ri) ** 2 / (2 * s * s)) * i0e(Ro * Ri / (s * s)); KR /= np.maximum((KR * WR[:, None]).sum(0, keepdims=True), 1e-300)
    idR = s < 1.5 * spR; KR[:, idR] = 0.0; KR[np.where(idR)[0], np.where(idR)[0]] = 1.0 / WR[idR]
    Zo, Zi = MZ[:, None], MZ[None, :]; KZ = np.exp(-(Zo - Zi) ** 2 / (2 * s * s)) + np.exp(-(Zo + Zi) ** 2 / (2 * s * s)); KZ /= np.maximum((KZ * WZ[:, None]).sum(0, keepdims=True), 1e-300)
    idZ = s < 1.5 * spZ; KZ[:, idZ] = 0.0; KZ[np.where(idZ)[0], np.where(idZ)[0]] = 1.0 / WZ[idZ]
    return KR, KZ
KER = {k: kern(LAD[k]) for k in range(1, len(LAD))}; P(f"mesh {len(MR)} x {len(MZ)}, ladder {len(LAD)} widths up to {LAD[-1]:.0f} kpc")
RRm, ZZm = np.meshgrid(MR, MZ, indexing="ij")
def scatter(rho_m, xi_m):
    """rho_s = sum_k S_k[a_k rho]; rho_m, xi_m on the mesh (Msun/kpc^3, kpc)."""
    k, w = weights(xi_m.ravel()); k = k.reshape(xi_m.shape); w = w.reshape(xi_m.shape); M = rho_m * WR[:, None] * WZ[None, :]; out = np.zeros_like(rho_m)
    for kk in range(len(LAD)):
        a = np.where(k == kk, 1 - w, 0.0) + np.where(k == kk - 1, w, 0.0)
        if not a.any(): continue
        if kk == 0: out += a * rho_m; continue
        KR, KZ = KER[kk]; out += KR @ (a * M) @ KZ.T
    return out
def to_cells(f_m, g, Mu):
    from scipy.interpolate import RegularGridInterpolator as RGI
    it = RGI((MR, MZ), f_m, bounds_error=False, fill_value=0.0); return g.rho_axisym(lambda R_, z_: it(np.c_[np.ravel(R_), np.abs(np.ravel(z_))]) / Mu, nq=4)
def mesh_rho(c):
    rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); return rf(RRm.ravel(), ZZm.ravel()).reshape(RRm.shape)
def mesh_xi(g, X): return g.interp_cells(X, RRm.ravel(), ZZm.ravel()).reshape(RRm.shape)
for foot, a0s in A0SI.items():
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g); st = [json.loads(l) for l in open(os.path.join(RB, "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))]; IP = []
    for c, sx in zip(cells(), st):
        _, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        if L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]: IP.append((c, sx, ms))
    if SMOKE: IP = IP[:SMOKE]
    n = len(IP); a0k = a0s * CONV; gsk = a0k / KAP; RQ = R0 + np.array([-0.5, -0.25, 0.0, 0.25, 0.5]); i0 = int(np.argmin(np.abs(g.rc - R0))); c0 = i0 * g.Nt + g.Nt - 1
    cp = os.path.join(CK, f"{foot}.jsonl"); done = {}
    if os.path.exists(cp):
        for l in open(cp): d = json.loads(l); done[d["m"]] = d
        P(f"[{foot}] resumed, {len(done)} cells done")
    fo = open(cp, "a"); e1 = 0.0; emut = 0.0; n2 = []
    for m, (c, sx, ms) in enumerate(IP):
        rho = rho_k(c, 0, g, Mu); PhiN = LU.newton(rho); PQ = LU.qumond(PhiN)
        if m < 2:
            qm, _ = lines_from(rho, PhiN, g, a0, LU, True); oN = ns["mw_obs"](g, PhiN, a0); emut = max(emut, abs(qm["vc"] / oN["vc_R0"] - 1))
        if m in done: continue
        q0 = C.field_lines(g, PQ, a0); e = max(abs(q0["vc"] / sx["Q"]["vc"] - 1), abs(q0["K0"] / sx["Q"]["K0"] - 1))
        rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        V = C.L.vc_plane(ns, g, PQ, a0, RQ); VN = C.L.vc_plane(ns, g, PhiN, a0, RQ); gq = V ** 2 / RQ; gN = VN ** 2 / RQ
        TRR = np.gradient(gq, RQ)[1:4]; Tpp = (gq / RQ)[1:4]; r0 = np.array([float(rf(np.array([x]), np.array([0.0]))[0]) for x in RQ[1:4]])
        lap = nu_b(gN[1:4] / a0k) * 4 * math.pi * Gk * r0; Tzz = lap - TRR - Tpp; tau = np.sqrt(TRR ** 2 + Tpp ** 2 + Tzz ** 2)
        d = dict(m=m, e1=e, n2=float(tidal_tau(g, PQ)[c0] * a0k / tau[1])); XI = tidal_xi(g, PQ); rm = mesh_rho(c); m0 = float(np.sum(rho * g.vol))
        oN = ns["mw_obs"](g, PhiN, a0); d["KN"] = oN["K_R0"]; d["KQ"] = q0["K0"]; d["vQ"] = q0["vc"]
        for r_ in RULES:
            rs = to_cells(scatter(rm, mesh_xi(g, XI[r_])), g, Mu); q, _ = lines_from(rs, PhiN, g, a0, LU); d[r_] = dict(Q=q, mass=float(np.sum(rs * g.vol)) / m0)
        fo.write(json.dumps(d, default=float) + "\n"); fo.flush(); done[m] = d
        if STOP[0]: P("SIGTERM: checkpointed, exiting"); sys.exit(3)
        if m % 100 == 0: P(f"    [{foot}] cell {m}/{n}")
    fo.close()
    e1 = max(done[m]["e1"] for m in done); ok = e1 <= 1e-6; fail += not ok; P(f"R1 [{foot}] xi 0 vs UX5 form Q, {n} cells, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    ok = emut <= 1e-6; fail += not ok; P(f"MUTATE [{foot}] nu = 1 gives Q = N on 2 cells: max rel {emut:.1e}: {'PASS' if ok else 'FAIL'}")
    n2 = np.array([done[m]["n2"] for m in range(n)]); N2 = 0.9 <= float(np.median(n2)) <= 1.1; fail += not N2; P(f"N2 [{foot}] grid tau_F at cell nearest (R0, 0) / KT29 tau: median {np.median(n2):.3f} (min {n2.min():.3f}, max {n2.max():.3f}), line [0.9, 1.1]: {'PASS' if N2 else 'FAIL'}")
    # S2 / S3 on lightest and heaviest cells
    ms_ = [x[2] for x in IP]; e23 = {"S2": [], "S3": []}
    for m in (int(np.argmin(ms_)), int(np.argmax(ms_))):
        c = IP[m][0]; rm = mesh_rho(c); rho = rho_k(c, 0, g, Mu); PhiN = LU.newton(rho)
        for tag, kk in (("S2", 0), ("S3", 0.5)):
            for target in (1.0, 9.0):
                kb = int(round(math.log(target / 0.005) / LR)) + 1; xv = LAD[1] * 1.25 ** (kb - 1 + kk)
                rs = to_cells(scatter(rm, np.full(rm.shape, xv)), g, Mu); qb, _ = lines_from(rs, PhiN, g, a0, LU)
                f = rho_xi(c, xv); rd_ = g.rho_axisym(lambda R_, z_: f(R_, z_) / Mu, nq=4); qd, _ = lines_from(rd_, PhiN, g, a0, LU); e23[tag].append((xv, qb["vc"] - qd["vc"], qb["K0"] - qd["K0"]))
    okS = {}
    for tag, v in e23.items():
        ok = all(abs(a) <= 0.5 and abs(b_) <= 0.5 for _, a, b_ in v); okS[tag] = ok; fail += not ok; RES[f"{tag}|{foot}"] = v
        P(f"{tag} [{foot}] {'smoother at a ladder width' if tag == 'S2' else 'ladder blend at a midpoint'} vs exact rho_xi: " + "; ".join(f"xi {x:.3g} dv {a:+.3f} dK {b_:+.3f}" for x, a, b_ in v) + f": {'PASS' if ok else 'FAIL'}")
    for r_ in RULES:
        mr = np.array([done[m][r_]["mass"] for m in range(n)]); S1 = bool(np.all(np.abs(mr - 1) <= 1e-2)); fail += not S1
        P(f"S1 [{foot}] rule {r_} mass ratio min/med/max {mr.min():.4f}/{np.median(mr):.4f}/{mr.max():.4f}, line |x - 1| <= 1e-2 on every cell: {'PASS' if S1 else 'FAIL'}")
        out = []
        for m, (c, sx, ms) in enumerate(IP):
            o = dict(Q=done[m][r_]["Q"], mass=done[m][r_]["mass"], Mstar=ms, m=m, KN=done[m]["KN"], KQ=done[m]["KQ"], vQ=done[m]["vQ"], **{k: c[k] for k in KEYS if k in c}); out.append(o)
        qq = [o["Q"] for o in out]; n4 = [o for o in out if all(o["Q"][l] for l in ("L1", "L2a", "L2b", "L3"))]; cnt = {l: sum(x[l] for x in qq) for l in ("L1", "L2a", "L2b", "L3", "Lh")}; b = min(out, key=lambda o: o["Q"]["D"]); bq = b["Q"]
        kl1 = min((x["K0"] for x in qq if x["L1"]), default=None)
        tgt = sorted(n4, key=lambda o: o["Q"]["D"])[:2] if n4 else [b]; r5 = []
        for o in tgt:
            c = IP[o["m"]][0]; rho = rho_k(c, 0, g, Mu); PhiN = LU.newton(rho); PQ = LU.qumond(PhiN); X5 = tidal_xi(g, PQ, 1.0)[r_]
            rs = to_cells(scatter(mesh_rho(c), mesh_xi(g, X5)), g, Mu); q5, _ = lines_from(rs, PhiN, g, a0, LU); r5.append(dict(dvc=q5["vc"] - o["Q"]["vc"], dK=q5["K0"] - o["Q"]["K0"], pass4=all(q5[l] for l in ("L1", "L2a", "L2b", "L3"))))
        flip = any(x["pass4"] for x in r5) != bool(n4)
        if not (N2 and S1 and okS["S2"] and okS["S3"]): lab = "NOT EVALUABLE (numerics)"
        elif flip: lab = "NUMERICS-DEPENDENT"
        else: lab = "PASSES MW" if n4 else "FAILS MW"
        R = RES[f"mw|{foot}|{r_}"] = dict(label=lab, n_pass=len(n4), lines=cnt, vc_max=max(x["vc"] for x in qq), K_min_L1=kl1, mass=[float(mr.min()), float(np.median(mr)), float(mr.max())], R5=r5,
                                          best={k: b.get(k) for k in KEYS + ("Mstar", "mass", "KN", "KQ", "vQ")} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")},
                                          passing=[{k: o.get(k) for k in KEYS + ("Mstar", "mass")} | {k: o["Q"][k] for k in ("vc", "K0", "cK", "cO", "h")} for o in sorted(n4, key=lambda o: o["Q"]["D"])][:30])
        P(f"MW [{foot}] rule {r_}: all four {len(n4)}; L1 {cnt['L1']} L2a {cnt['L2a']} L2b {cnt['L2b']} L3 {cnt['L3']} Lh {cnt['Lh']}; v_c max {R['vc_max']:.1f}; lowest K with v_c in line {('%.1f' % kl1) if kl1 else 'none'}; best D {bq['D']:.2f} ({b['box']} Rd {b['rd']} Sb {b['sb']} Mbb {b['mbb']:.3g} ht {b.get('ht')} hk {b.get('hk')} fk {b.get('fk')}) v_c {bq['vc']:.1f} K {bq['K0']:.1f} cK {bq['cK']:.1f} Ou {bq['cO']:.0f} mass {b['mass']:.4f}")
        P(f"    beside, best cell: K(R0) Newton {b['KN']:.1f}, plain QUMOND {b['KQ']:.1f} (v_c {b['vQ']:.1f}), scatter {bq['K0']:.1f}: phantom share of K {(bq['K0'] - b['KN']):.1f}")
        P("    R5 (ln tau smoothed 1 cell): " + "; ".join(f"dv {x['dvc']:+.2f} dK {x['dK']:+.2f} pass {x['pass4']}" for x in r5))
        P(f"LABEL [{foot}] rule {r_}: {lab}")
    try:
        k31 = json.load(open(os.path.join(RB, "KT31_tidal_rule_rz_solve/kt31.json")))
        P(f"    beside, KT31 gather best cells [{foot}]: " + "; ".join(f"{r_} v_c {k31[f'mw|{foot}|{r_}']['best']['vc']:.1f} K {k31[f'mw|{foot}|{r_}']['best']['K0']:.1f}" for r_ in RULES))
    except Exception as ex: P(f"    KT31 compare unavailable: {ex}")
RES["fail"] = fail; P(f"failed checks: {fail}")
if SMOKE: sys.exit(0)
open(os.path.join(HERE, "kt32.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "kt32.json"), "w"), indent=1, default=float)
sys.exit(1 if fail else 0)
