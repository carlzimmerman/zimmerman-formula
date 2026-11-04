#!/usr/bin/env python3
"""KT30 MW arm (copy of KT29; filter length per cell = TRACE-FREE tidal rule sqrt6 tau_TF^3/(tau_TF'^2 g*) at (R0, 0), tau_TF = |T - trT/3 I|; KT29's full-norm value kept as check R1). Older text: KT29 (copy of KT28's MW arm; filter length per cell = full-tensor tidal rule at (R0, 0), T_zz from nu 4 pi G rho_b; T1 keeps KT28's observed-curve value as a check. Older text: MW filter length = tidal rule xi_tid(R0) = (4/sqrt3) tau^3/(tau'^2 g*) from the observed curve, V linear in R, one value per footing; Cassini and dwarf parts run at eps 0.5 as a reproduction of KT25). KT17: filtered QUMOND with xi = eps sqrt(G M_b / a0), eps = 1 and 0.55, on Cassini (KT16's integral), 24 dwarfs (KT15's model) and the Milky Way's in-prior cells (KT14's solver). python3 kt17.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
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
# ---------- Cassini (KT16) ----------
GMs = 6.6743e-11 * 1.98892e30; GEXT, CEIL = 2.32e-10, 5.2e-27
def gh_pt(r, xi):
    x = r / xi; out = np.empty_like(r); s = x < 1e-3; out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi ** 3; return out
def qcas(eta, xi, nr=20000, nm=200):
    u = np.linspace(math.log(1e-7), math.log(1e5), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm); g = gh_pt(r, xi)[:, None]; M = mu[None, :]
    A = nu(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; return abs(1.5 * float(np.trapz(((A * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w) / r, u)))
for foot, a0 in A0SI.items():
    eta = GEXT / a0; rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM)
    for e in EPS:
        qq = qcas(eta, e); RES[f"cassini|{foot}|{e}"] = dict(q=qq, x_ceiling=qq / qp, ok=bool(qq < qp)); P(f"Cassini [{foot}] eps {e}: xi {e * rM / 1.495978707e11:.0f} AU, q {qq:.4g} = {qq / qp:.3g} x ceiling: {'PASS' if qq < qp else 'FAIL'}")
# ---------- dwarfs (KT15) ----------
DATA = os.path.join(RB, "../real_research/data/dsph/mcconnachie2012_dsph.csv"); UPS = np.linspace(1, 3, 41)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth_sph(r, rho, s):
    if s <= 0: return rho
    R, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * s * R)) * (np.exp(-(R - Rp) ** 2 / (2 * s * s)) - np.exp(-(R + Rp) ** 2 / (2 * s * s))); return np.trapz(K * rho[None, :], r, axis=1)
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, xi, a0, ge):
    r = rgrid(a, xi); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gh = gN if xi <= 0 else Gk * menc(r, smooth_sph(r, rho, xi)) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M))
rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
for foot, a0s in A0SI.items():
    a0 = a0s * CONV; cnt = {}
    for e in [0.0] + EPS:
        n = 0; det = []
        for d in rows:
            ge = (200.0 ** 2 / d["D"]) if d["sub"] == "MW" else 0.0; sp = []
            for u in UPS:
                M = u * d["L"] + 1.33 * d["MHI"]; sp.append(sig_los(M, d["a"], e * math.sqrt(Gk * M / a0), a0, ge))
            sp = np.array(sp); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok; det.append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), xi_U2=e * math.sqrt(Gk * (2 * d["L"] + 1.33 * d["MHI"]) / a0), passed=ok))
        cnt[e] = n; RES[f"dwarf|{foot}|{e}"] = dict(n_pass=n, rows=det)
    for e in EPS:
        n, ref = cnt[e], cnt[0.0]; lab = "KILLED" if n <= ref / 2 else "SURVIVES" if n >= ref - 2 else "HURT"; RES[f"dwarf_label|{foot}|{e}"] = lab; P(f"Dwarfs [{foot}] eps {e}: {n}/24 vs plain {ref}/24: {lab}; Fornax pred {RES[f'dwarf|{foot}|{e}']['rows'][[r['name'] for r in rows].index('Fornax')]['pred_U2']:.1f} (plain {RES[f'dwarf|{foot}|0.0']['rows'][[r['name'] for r in rows].index('Fornax')]['pred_U2']:.1f}, obs 11.7)")

# ---------- KT26 parts A, B, D ----------
KAP = 0.5; GSI = 6.6743e-11; MSUN = 1.98892e30; KPCM = 3.0857e19; AUM = 1.495978707e11
nu_b = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
XIL = {}
for foot, a0 in A0SI.items():
    gs = a0 / KAP; e1 = 0.0
    for Mm in (1.0, 1e11):
        M = Mm * MSUN; rM = math.sqrt(GSI * M / a0); Vi2 = (GSI * M * a0) ** 0.5; e1 = max(e1, abs((Vi2 / gs) / (KAP * rM) - 1))
    P(f"A1 [{foot}] xi = V_inf^2/g* vs kappa r_M, max rel {e1:.1e}: {'PASS' if e1 <= 1e-12 else 'FAIL'}")
    M = 1e11 * MSUN; rM = math.sqrt(GSI * M / a0); gf = lambda r: nu_b(GSI * M / r ** 2 / a0) * GSI * M / r ** 2
    for k in (100.0, 1e4):
        r = k * rM; h = 1e-5 * r; dg = (gf(r + h) - gf(r - h)) / (2 * h); xl = gf(r) ** 2 / (abs(dg) * gs)
        P(f"B1 [{foot}] point mass at r = {k:g} r_M: xi_loc / (kappa r_M) = {xl / (KAP * rM):.5f}" + ("" if k != 100.0 else f" (frozen tolerance 1e-3: {'PASS' if abs(xl / (KAP * rM) - 1) <= 1e-3 else 'FAIL'})"))
    V0 = 229.1e3; R0m = 8.178 * KPCM; sl = 8.178 * (-1.7) / 229.1; sv = -1.7e3 / KPCM; Vf = lambda R: V0 + sv * (R - R0m); gf2 = lambda R: Vf(R) ** 2 / R
    def tauf(R):
        h = 1e-4 * R; gp = (gf2(R + h) - gf2(R - h)) / (2 * h); return math.sqrt(gp ** 2 + 2 * (gf2(R) / R) ** 2)
    h = 1e-3 * R0m; tp = (tauf(R0m + h) - tauf(R0m - h)) / (2 * h); xi = 4 / math.sqrt(3) * tauf(R0m) ** 3 / (tp ** 2 * gs) / KPCM; XIL[foot] = xi
    P(f"C [{foot}] xi_tid(R0): dlnV/dlnR {sl:+.4f}, g* {gs:.4e}, xi_loc {xi:.3f} kpc")
    ge = 2.32e-10; Ms = MSUN
    for nm, r in (("Saturn 9.58 AU", 9.58 * AUM), ("r_M", math.sqrt(GSI * Ms / a0))):
        gi = lambda rr: nu_b(math.sqrt(ge ** 2 + (GSI * Ms / rr ** 2) ** 2) / a0) * 0 + GSI * Ms / rr ** 2
        gm = lambda rr: math.sqrt(gi(rr) ** 2 + ge ** 2); h = 1e-5 * r; dg = (gm(r + h) - gm(r - h)) / (2 * h); xl = gm(r) ** 2 / (abs(dg) * gs)
        P(f"D [{foot}] Sun at {nm}, with g_e 2.32e-10 (Newtonian internal field): xi_loc {xl / AUM:.3g} AU = {xl / math.sqrt(GSI * Ms / a0):.3g} r_M (KT25 uses 0.5 r_M)")
    Mf, af, Df = 4.3e7 * MSUN, 0.71 * KPCM, 147 * KPCM; gef = (200e3) ** 2 / Df
    gi = lambda rr: GSI * Mf * rr / (rr ** 2 + af ** 2) ** 1.5; gm = lambda rr: math.sqrt(gi(rr) ** 2 + gef ** 2); r = af; h = 1e-5 * r; dg = (gm(r + h) - gm(r - h)) / (2 * h); xl = gm(r) ** 2 / (abs(dg) * gs)
    P(f"D [{foot}] Fornax-like (Plummer 4.3e7 Msun, a 0.71 kpc, g_e {gef:.2e}) at r = a: xi_loc {xl / KPCM:.3g} kpc vs KT25 {0.5 * math.sqrt(GSI * Mf / a0) / KPCM:.3g} kpc")
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
for foot, a0s in A0SI.items():
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g); st = [json.loads(l) for l in open(os.path.join(RB, "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))]; IP = []
    for c, sx in zip(cells(), st):
        _, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        if L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]: IP.append((c, sx, ms))
    if not MUT:
        rhog = lambda R, z: (HI * np.exp(-4.0 / np.maximum(R, 1e-6) - np.maximum(R, 1e-6) / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(np.abs(z) / 0.17, 300)) ** 2 + (H2 * np.exp(-12.0 / np.maximum(R, 1e-6) - np.maximum(R, 1e-6) / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(np.abs(z) / 0.09, 300)) ** 2
        mg = float(np.sum(g.rho_axisym(lambda R, z: rhog(R, z) / Mu, nq=4) * g.vol)) * Mu; e3 = abs(mg / MGAS - 1); ok = e3 <= 1e-2; fail += not ok; P(f"C3 [{foot}] gas mass on solver grid {mg:.4g} vs integral, rel {e3:.1e}: {'PASS' if ok else 'FAIL'}")
        e1 = 0.0
        for c, sx, ms in IP:
            o = solve(c, 0.0, a0, g, Mu, LU); e1 = max(e1, abs(o["Q"]["vc"] / sx["Q"]["vc"] - 1), abs(o["Q"]["K0"] / sx["Q"]["K0"] - 1))
        ok = e1 <= 1e-6; fail += not ok; P(f"C1 [{foot}] xi 0 vs UX5 form Q, {len(IP)} cells, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    a0k = a0s * CONV; gsk = a0k / KAP; RQ = R0 + np.array([-0.5, -0.25, 0.0, 0.25, 0.5]); XT = {}; XP = {}; XZ = {}; XF = {}; XFZ = {}
    for c, _, ms in IP:
        rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); PN = LU.newton(g.rho_axisym(lambda R_, z_: rf(R_, z_) / Mu, nq=4)); PQ = LU.qumond(PN)
        V = C.L.vc_plane(ns, g, PQ, a0, RQ); VN = C.L.vc_plane(ns, g, PN, a0, RQ); gq = V ** 2 / RQ; gN = VN ** 2 / RQ
        TRR = np.gradient(gq, RQ)[1:4]; Tpp = (gq / RQ)[1:4]; rho0 = np.array([float(rf(np.array([x]), np.array([0.0]))[0]) for x in RQ[1:4]])
        lap = nu_b(gN[1:4] / a0k) * 4 * math.pi * Gk * rho0; Tzz = lap - TRR - Tpp; tau = np.sqrt(TRR ** 2 + Tpp ** 2 + Tzz ** 2); dt = (tau[2] - tau[0]) / 0.5
        tf = np.sqrt(np.maximum(TRR ** 2 + Tpp ** 2 + Tzz ** 2 - lap ** 2 / 3, 0.0)); XF[id(c)] = min(math.sqrt(6) * tf[1] ** 3 / (((tf[2] - tf[0]) / 0.5) ** 2 * gsk), 200.0)
        XT[id(c)] = min(4 / math.sqrt(3) * tau[1] ** 3 / (dt * dt * gsk), 200.0); tp = np.sqrt(TRR ** 2 + 2 * Tpp ** 2); XP[id(c)] = 4 / math.sqrt(3) * tp[1] ** 3 / (((tp[2] - tp[0]) / 0.5) ** 2 * gsk)
        zq = np.array([1.0, 1.1, 1.2]); rz = np.array([float(rf(np.array([R0]), np.array([z]))[0]) for z in zq]); tz = nu_b(gN[2] / a0k) * 4 * math.pi * Gk * rz; XZ[id(c)] = 4 / math.sqrt(3) * tz[1] ** 3 / (((tz[2] - tz[0]) / 0.2) ** 2 * gsk); XFZ[id(c)] = math.sqrt(6) * math.sqrt(2 / 3) * tz[1] ** 3 / (((tz[2] - tz[0]) / 0.2) ** 2 * gsk)
    v = np.array(list(XT.values())); vp = np.array(list(XP.values())); vz = np.array(list(XZ.values())); RES[f"xi|{foot}"] = dict(full=[float(x) for x in np.percentile(v, [0, 50, 100])], inplane=[float(x) for x in np.percentile(vp, [0, 50, 100])], z11_approx=[float(x) for x in np.percentile(vz, [0, 50, 100])], n_clip=int(np.sum(v >= 200.0)))
    P(f"[{foot}] full-tensor xi_tid(R0, 0) min/median/max {v.min():.2f}/{np.median(v):.2f}/{v.max():.2f} kpc (clipped {int(np.sum(v >= 200))}); in-plane only, cell's own V: {vp.min():.2f}/{np.median(vp):.2f}/{vp.max():.2f}; beside at z 1.1 kpc (T_zz only, approx): {vz.min():.3g}/{np.median(vz):.3g}/{vz.max():.3g}")
    vf = np.array(list(XF.values())); vfz = np.array(list(XFZ.values())); RES[f"xi|{foot}"].update(tracefree=[float(x) for x in np.percentile(vf, [0, 50, 100])], tracefree_z11_approx=[float(x) for x in np.percentile(vfz, [0, 50, 100])], n_clip_tf=int(np.sum(vf >= 200.0)))
    P(f"[{foot}] TRACE-FREE xi_TF(R0, 0) min/median/max {vf.min():.2f}/{np.median(vf):.2f}/{vf.max():.2f} kpc (clipped {int(np.sum(vf >= 200))}), ratio to full median {np.median(vf / v):.3f}; beside at z 1.1 kpc: {vfz.min():.3g}/{np.median(vfz):.3g}/{vfz.max():.3g}")
    K29 = json.load(open(os.path.join(RB, "KT29_tidal_rule_mw_full_tensor/kt29.json")))[f"xi|{foot}"]["full"]; e1 = max(abs(a / b - 1) for a, b in zip(RES[f"xi|{foot}"]["full"], K29)); ok = e1 <= 1e-3; fail += not ok; P(f"R1 [{foot}] full-norm xi range reproduces KT29: max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    ok = abs(XIL[foot] - {"canonical": 8.78, "alt": 7.26}[foot]) <= 0.01; fail += not ok; P(f"T1 [{foot}] observed-curve in-plane value {XIL[foot]:.3f} kpc vs KT28: {'PASS' if ok else 'FAIL'}")
    for e in EPS:
        xs = {id(c): math.exp(round(math.log(XF[id(c)]) / 0.005) * 0.005) for c, _, ms in IP}; order = sorted(IP, key=lambda t: xs[id(t[0])]); P(f"\n[{foot}] TRACE-FREE TIDAL RULE (MW arm keyed eps {e}): xi range {min(xs.values()):.2f}-{max(xs.values()):.2f} kpc, {len(set(xs.values()))} distinct after quantisation")
        if not MUT:
            for nm, (c, _, ms) in (("lightest", order[0]), ("heaviest", order[-1])):
                s = xs[id(c)]; f = rho_xi(c, s); rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); m1 = float(np.sum(g.rho_axisym(lambda R_, z_: f(R_, z_) / Mu, nq=4) * g.vol)); m0 = float(np.sum(g.rho_axisym(lambda R_, z_: rf(R_, z_) / Mu, nq=4) * g.vol)); e2 = abs(m1 / m0 - 1); ok = e2 <= 2e-3; fail += not ok; P(f"C2 [{foot}] eps {e} {nm} cell xi {s:.2f}: mass ratio - 1 {m1 / m0 - 1:+.1e}: {'PASS' if ok else 'FAIL'}")
        out = []
        for c, _, ms in order:
            o = solve(c, xs[id(c)], a0, g, Mu, LU); o.update({k: c[k] for k in KEYS if k in c}); o["xi"] = xs[id(c)]; out.append(o)
        q = [o["Q"] for o in out]; n4 = [o for o in out if all(o["Q"][l] for l in ("L1", "L2a", "L2b", "L3"))]; cnt = {l: sum(x[l] for x in q) for l in ("L1", "L2a", "L2b", "L3", "Lh")}; b = min(out, key=lambda o: o["Q"]["D"]); bq = b["Q"]; kl1 = min((x["K0"] for x in q if x["L1"]), default=None)
        R = RES[f"mw|{foot}|{e}"] = dict(n_pass=len(n4), strict=sum(o["Q"]["Lh"] for o in n4), lines=cnt, K_min_L1=kl1, vc_max=max(x["vc"] for x in q), best={k: b.get(k) for k in KEYS + ("Mstar", "xi")} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")}, passing=[{k: o.get(k) for k in KEYS + ("Mstar", "xi")} | {k: o["Q"][k] for k in ("vc", "K0", "cK", "cO", "h")} for o in sorted(n4, key=lambda o: o["Q"]["D"])][:30])
        P(f"MW [{foot}] eps {e}: all four {len(n4)} (strict h {R['strict']}); L1 {cnt['L1']} L2a {cnt['L2a']} L2b {cnt['L2b']} L3 {cnt['L3']} Lh {cnt['Lh']}; v_c max {R['vc_max']:.1f}; lowest K with v_c in line {('%.1f' % kl1) if kl1 else 'none'}; best D {bq['D']:.2f} ({b['box']} Rd {b['rd']} Sb {b['sb']} Mbb {b['mbb']:.3g} ht {b.get('ht')} hk {b.get('hk')} fk {b.get('fk')} xi {b['xi']:.2f}) v_c {bq['vc']:.1f} K {bq['K0']:.1f} cK {bq['cK']:.1f} Ou {bq['cO']:.0f} h {bq['h']:.2f}")
        if n4 and not MUT:
            c0 = min(n4, key=lambda o: o["Q"]["D"]); gh2, _ = C.grid(a0, hi=True); LH = C.Lapl(gh2); o1 = solve({k: c0[k] for k in KEYS if k in c0}, c0["xi"], a0, gh2, Mu, LH); R["Q5"] = dict(dK=o1["Q"]["K0"] - c0["Q"]["K0"], dv=o1["Q"]["vc"] - c0["Q"]["vc"]); P(f"    Q5 doubled grid: dK {R['Q5']['dK']:+.2f} dv {R['Q5']['dv']:+.2f}{' [GRID-DEPENDENT]' if abs(R['Q5']['dK']) > 1 else ''}")
for foot in A0SI:
    for e in EPS:
        mw = RES[f"mw|{foot}|{e}"]["n_pass"] > 0; dw = RES[f"dwarf_label|{foot}|{e}"]; ca = RES[f"cassini|{foot}|{e}"]["ok"]
        lab = "T0 MW PASS" if mw else "T0 MW FAIL"; RES[f"label|{foot}|{e}"] = lab; P(f"LABEL [{foot}] trace-free rule: {lab}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt30_mw{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt30_mw{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
