#!/usr/bin/env python3
"""CZ5: frozen re-grade of the local filter rule LOC on the 3D field (vector Newtonian field in |g|, full gradient,
field-gather smoothing) on CZ2's gates plus CZ3's planets. Criteria c805085c2f.
OMP_NUM_THREADS=1 python3 -I -B cz5.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.special import erf, erfc
T00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok) or MUT; P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0; M_MW = 7.0e10
G, MS, AU = 6.6743e-11, 1.98892e30, 1.495978707e11; GCAS, CEIL = 2.32e-10, 5.2e-27
P(f"CZ5 (criteria c805085c2f){'  [MUTATE: nu = 1]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
if MUT:
    nu = lambda y: np.ones_like(np.asarray(y, float)); Gf = lambda y: np.asarray(y, float); dGf = lambda y: np.ones_like(np.asarray(y, float))
else:
    nu = nu_s; Gf = lambda y: y * nu_s(y)
    dGf = lambda y: nu_s(y) - 1 / (2 * np.maximum(y, 1e-300) * np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def eta_newton(gobs, a0):
    eo = gobs / a0; return eo if MUT else brentq(lambda y: float(Gf(y)) - eo, 1e-9, eo)

# =============== CZ2's dwarf code, verbatim (R0, K1) ===============
UPS = np.linspace(1, 3, 41)
def xi_loc(r, gm, gs, clip):
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth_rows(r, rho, s, mask_small=False):
    s = np.broadcast_to(np.asarray(s, float), r.shape); R, Rp, S = r[:, None], r[None, :], s[:, None]
    K = (Rp / (math.sqrt(2 * math.pi) * S * R)) * (np.exp(-(R - Rp) ** 2 / (2 * S * S)) - np.exp(-(R + Rp) ** 2 / (2 * S * S))); out = np.trapz(K * rho[None, :], r, axis=1)
    if mask_small:
        dr = np.gradient(r); m = s < 3 * dr; out[m] = rho[m]
    return out
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, mode, a0, ge, xi0=0.0):
    if mode == "LOC":
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge)
        X = xi_loc(r, nu(gq / a0) * gq, a0 / KAP, XCLIP)
    else:
        X = xi0; r = rgrid(a, X); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2
    gh = gN if mode == "plain" else Gk * menc(r, smooth_rows(r, rho, X, mode == "LOC")) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M))
DATA = os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"); rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
cz1 = json.load(open(os.path.join(HERE, "..", "CZ1_newtonian_external_field", "cz1.json")))
E2G = {r_["name"]: r_["ge_over_a0"] for r_ in cz1["dwarf|alt|E2|plain"]["rows"]}
GEV = {"E1": lambda d: Gk * M_MW / d["D"] ** 2 if d["sub"] == "MW" else 0.0, "E2": lambda d: E2G[d["name"]] * A0SI["alt"] * CONV}
fi = [r_["name"] for r_ in rows].index("Fornax")

# =============== Gaussian-smoothed Plummer table T(r/a, xi/a) = M_s(< r) / M ===============
P("\n== Smoothed Plummer table")
LR = np.linspace(math.log(1e-4), math.log(1e5), 361); LS = np.linspace(math.log(1e-4), math.log(1e5), 361)
RP = np.exp(np.linspace(math.log(1e-6), math.log(1e6), 4000)); RHO1 = 3 / (4 * math.pi) * (1 + RP ** 2) ** -2.5; WQ = 4 * math.pi * RP ** 2 * RHO1 * RP   # integrand weight in ln r'
def mplum(x): return x ** 3 / (1 + x * x) ** 1.5
def tab_row(s, rr):
    """M_s(< rr) for one width s (a = 1, M = 1)."""
    out = np.empty_like(rr); small = s < 0.05 * rr
    if small.any():
        x = rr[small]; drho = 3 / (4 * math.pi) * (-5 * x) * (1 + x * x) ** -3.5; out[small] = mplum(x) + 0.5 * s * s * 4 * math.pi * x * x * drho
    big = ~small
    if big.any():
        R = rr[big][:, None]; Rp = RP[None, :]; q = 1 / (math.sqrt(2) * s)
        e1 = np.where(Rp <= R, 0.5 * (erf((R - Rp) * q) + erf((R + Rp) * q)), 0.5 * (erfc((Rp - R) * q) - erfc((Rp + R) * q)))
        z = R * Rp / (s * s)
        with np.errstate(over="ignore", invalid="ignore"):
            t2 = np.where(z < 1, 2 * np.exp(-(R * R + Rp * Rp) / (2 * s * s)) * np.sinh(np.minimum(z, 1.0)), np.exp(-(R - Rp) ** 2 / (2 * s * s)) - np.exp(-(R + Rp) ** 2 / (2 * s * s)))
        Pk = e1 - s / (Rp * math.sqrt(2 * math.pi)) * t2
        out[big] = np.trapz(WQ[None, :] * Pk, np.log(RP), axis=1)
    return out
TAB = np.stack([tab_row(math.exp(ls), np.exp(LR)) for ls in LS], 1)   # (n_r, n_s)
def _cr(t):
    """Catmull-Rom weights for neighbours -1, 0, 1, 2."""
    t2, t3 = t * t, t * t * t; return ((-t3 + 2 * t2 - t) / 2, (3 * t3 - 5 * t2 + 2) / 2, (-3 * t3 + 4 * t2 + t) / 2, (t3 - t2) / 2)
def Tint(x, s):
    """Bicubic (Catmull-Rom) in (ln r/a, ln xi/a); xi below the table is the Plummer limit; beyond, clamped."""
    x = np.asarray(x, float); s = np.asarray(s, float)
    lx = np.clip(np.log(np.maximum(x, 1e-300)), LR[0], LR[-1]); ls = np.log(np.maximum(s, 1e-300))
    fx = (lx - LR[0]) / (LR[1] - LR[0]); i = np.clip(fx.astype(int), 0, LR.size - 2); ax = fx - i
    lsc = np.clip(ls, LS[0], LS[-1]); fs = (lsc - LS[0]) / (LS[1] - LS[0]); j = np.clip(fs.astype(int), 0, LS.size - 2); bs = fs - j
    wx, ws = _cr(ax), _cr(bs); v = np.zeros_like(lx)
    for da, wa in zip((-1, 0, 1, 2), wx):
        ii = np.clip(i + da, 0, LR.size - 1)
        for db, wb in zip((-1, 0, 1, 2), ws): v = v + wa * wb * TAB[ii, np.clip(j + db, 0, LS.size - 1)]
    return np.where(ls < LS[0], mplum(x), v)
xs = np.array([0.01, 0.3, 1.0, 3.0, 30.0]); k2a = float(np.max(np.abs(Tint(xs, np.full(5, 1e-5)) / mplum(xs) - 1)))
k2b = float(np.max(np.abs(Tint(np.array([1e4, 3e4]), np.array([1.0, 10.0])) - 1)))
fsm = lambda t: erf(t / math.sqrt(2)) - math.sqrt(2 / math.pi) * t * np.exp(-t * t / 2)
xs2 = np.array([30.0, 300.0, 1000.0]); k2c = float(np.max(np.abs(Tint(xs2, np.full(3, 300.0)) - fsm(xs2 / 300.0))))
rr_ = np.exp(LR); jj = np.searchsorted(LS, math.log(0.3)); s_ = math.exp(LS[jj]); m_ = (s_ >= 0.05 * rr_) & (s_ < 0.08 * rr_)
k2d = float(np.max(np.abs(tab_row(s_, rr_[m_]) - (mplum(rr_[m_]) + 0.5 * s_ ** 2 * 4 * math.pi * rr_[m_] ** 2 * 3 / (4 * math.pi) * (-5 * rr_[m_]) * (1 + rr_[m_] ** 2) ** -3.5)))) if m_.any() else 0.0
check("K2", (k2a <= 1e-6 and k2b <= 1e-4 and k2c <= 1e-4) or MUT, f"table: xi->0 vs Plummer {k2a:.1e} (1e-6); large r -> 1 {k2b:.1e}; xi >> a vs point mass {k2c:.1e} (1e-4); quadrature vs expansion at the switch {k2d:.1e} (reported)")

# =============== 3D dwarf rows (field-gather, l = 0 monopole) ===============
MU, WMU = np.polynomial.legendre.leggauss(64); ST = np.sqrt(1 - MU ** 2)
def sig_new(M, a, a0, ge, row, xi_c=None):
    """row: 'plain3' (vector nu, no filter), 'R2' (3D xi, vector nu), 'R3' (1D xi, vector nu), 'R1' (1D xi, quadrature nu), 'C1' (constant xi_c, quadrature)."""
    r = rgrid(a, XCLIP); x = r / a; rho = plummer(r, M, a); gi = Gk * M * mplum(x) / r ** 2; gip = 4 * math.pi * Gk * rho - 2 * gi / r; gs = a0 / KAP
    if row == "plain3": h = np.broadcast_to(gi[:, None], (r.size, MU.size))
    elif row == "C1": h = Gk * M * Tint(x, np.full_like(x, xi_c / a)) / r ** 2
    elif row in ("R1", "R3"):
        gq = np.sqrt(gi * gi + ge * ge); y = gq / a0; dg = np.abs(dGf(y) * gi * gip / gq); xi = np.minimum((a0 * Gf(y)) ** 2 / np.maximum(dg * gs, 1e-300), XCLIP)
        h = Gk * M * Tint(x, xi / a) / r ** 2
        if row == "R3": h = np.broadcast_to(h[:, None], (r.size, MU.size))
    elif row == "R2":
        R, Mu = r[:, None], MU[None, :]; G_, Gp = gi[:, None], gip[:, None]
        g2 = G_ * G_ + ge * ge - 2 * ge * G_ * Mu; gn = np.sqrt(np.maximum(g2, 1e-300)); y = gn / a0
        dgn = np.sqrt((2 * Gp * (G_ - ge * Mu)) ** 2 + (2 * ge * G_ * ST[None, :] / R) ** 2) / (2 * gn)
        xi = np.minimum((a0 * Gf(y)) ** 2 / np.maximum(dGf(y) * dgn * gs, 1e-300), XCLIP)
        h = Gk * M * Tint(np.broadcast_to(x[:, None], xi.shape), xi / a) / R ** 2
    else: raise ValueError(row)
    if row in ("R1", "C1"):
        ph = (nu(np.sqrt(ge * ge + h * h) / a0) - 1) * h
    else:
        Mu = MU[None, :]; gf = np.sqrt(np.maximum(h * h + ge * ge - 2 * ge * h * Mu, 1e-300)); Fr = (nu(gf / a0) - 1) * (-h + ge * Mu)
        if ge > 0: Fr = Fr - (float(nu(ge / a0)) - 1) * ge * Mu
        ph = -0.5 * (Fr @ WMU)
    g = gi + ph; return math.sqrt(max(np.trapz(rho * r * g * 4 * math.pi * r * r, r), 0) / (3 * M))
P("\n== T2 dwarfs (line >= 15/24; STRICT >= plain in 3D)")
T2 = {}; DW = {}
for foot, a0s in A0SI.items():
    a0 = a0s * CONV; T2[foot] = {}
    for ev in ("E1", "E2"):
        cnt, forn = {}, {}
        for row in (("R0plain", "R0LOC", "R0HALF", "plain3", "R2", "R3", "R1", "C1") if ev == "E1" else ("plain3", "R2", "R3", "R1")):
            n = 0; det = []
            for d in rows:
                ge = GEV[ev](d)
                def one(u_):
                    Mx = u_ * d["L"] + 1.33 * d["MHI"]
                    if row == "R0plain": return sig_los(Mx, d["a"], "plain", a0, ge)
                    if row == "R0LOC": return sig_los(Mx, d["a"], "LOC", a0, ge)
                    if row == "R0HALF": return sig_los(Mx, d["a"], "const", a0, ge, 0.5 * math.sqrt(Gk * Mx / a0))
                    if row == "C1": return sig_new(Mx, d["a"], a0, ge, "C1", 0.5 * math.sqrt(Gk * Mx / a0))
                    return sig_new(Mx, d["a"], a0, ge, row)
                sp = np.array([one(u_) for u_ in UPS]); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok
                det.append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), passed=ok, ge_over_a0=ge / a0))
            cnt[row] = n; forn[row] = det[fi]["pred_U2"]; DW[f"{foot}|{ev}|{row}"] = dict(n_pass=n, rows=det)
        T2[foot][ev] = dict(counts=cnt, fornax=forn)
        P(f"  [{foot} {ev}] " + ", ".join(f"{k} {v}/24" for k, v in cnt.items()) + "; Fornax U2 " + ", ".join(f"{k} {forn[k]:.2f}" for k in cnt) + " (obs 11.7)")
        if ev == "E1":
            ch = [(x_["name"].split(" (")[0], x_["passed"]) for x_, y_ in zip(DW[f"{foot}|E1|R2"]["rows"], DW[f"{foot}|E1|R0LOC"]["rows"]) if x_["passed"] != y_["passed"]]
            if ch: P(f"      R2 (3D) vs CZ2's LOC: " + ", ".join(f"{nm} {'now PASS' if p else 'now fail'}" for nm, p in ch))
RES["dwarfs"] = DW
K1R = {"canonical": dict(R0LOC=17, R0plain=18, R0HALF=18, forn=11.94), "alt": dict(R0LOC=17, R0plain=18, R0HALF=18, forn=12.52)}
k1 = all(T2[f]["E1"]["counts"][k] == v for f in A0SI for k, v in K1R[f].items() if k != "forn") and all(abs(round(T2[f]["E1"]["fornax"]["R0LOC"], 2) - K1R[f]["forn"]) < 1e-9 for f in A0SI)
check("K1", k1, "R0 = CZ2's sig_los reproduces CZ2's E1 counts (LOC 17, plain 18, HALF 18) and Fornax LOC 11.94 / 12.52: " + "; ".join(f"{f} " + str({k: T2[f]['E1']['counts'][k] for k in ('R0LOC', 'R0plain', 'R0HALF')}) + f" Fornax {T2[f]['E1']['fornax']['R0LOC']:.2f}" for f in A0SI))
check("K5", all(T2[f]["E1"]["counts"]["C1"] == 18 for f in A0SI), "constant width 0.5 r_M, field-gather (C1) reproduces CZ2's HALF E1 count 18: " + ", ".join(f"{f} {T2[f]['E1']['counts']['C1']}" for f in A0SI))

# =============== T1 Cassini and T4 planets, 3D (CW1's solver, copied) ===============
def fsm2(t):
    t = np.asarray(t, float); out = np.empty_like(t); s = t < 1e-3
    out[~s] = erf(t[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * t[~s] * np.exp(-t[~s] ** 2 / 2); out[s] = math.sqrt(2 / math.pi) / 3 * t[s] ** 3; return out
def legendre(L, mu):
    Pl = np.zeros((L + 1, mu.size)); dP = np.zeros((L + 1, mu.size)); Pl[0] = 1
    if L >= 1: Pl[1] = mu; dP[1] = 1
    for l in range(1, L): Pl[l + 1] = ((2 * l + 1) * mu * Pl[l] - l * Pl[l - 1]) / (l + 1); dP[l + 1] = dP[l - 1] + (2 * l + 1) * Pl[l]
    return Pl, dP
class Solver:
    """CW1's multipole QUMOND solver (point mass in a uniform Newtonian field, units r_M), forms PQ and LOC3."""
    def __init__(s, eta, form, gs=2.0, L=64, nmu=96, per_dec=200, xmin=1e-7, xmax=1e5):
        s.u = np.linspace(math.log(xmin), math.log(xmax), int(round(per_dec * math.log10(xmax / xmin))) + 1); s.du = s.u[1] - s.u[0]; s.x = np.exp(s.u)
        s.mu, s.w = np.polynomial.legendre.leggauss(nmu); s.st = np.sqrt(1 - s.mu ** 2); s.Pl, s.dP = legendre(L, s.mu)
        X, M = s.x[:, None], s.mu[None, :]; STt = s.st[None, :]
        if form == "PQ": f = np.ones_like(X * M)
        else:
            g2 = X ** -4.0 + eta * eta - 2 * eta * X ** -2.0 * M; gn = np.sqrt(np.maximum(g2, 1e-300))
            dr = -4 * X ** -5.0 + 4 * eta * X ** -3.0 * M; dt = 2 * eta * X ** -3.0 * np.sqrt(1 - M ** 2); dgn = np.sqrt(dr ** 2 + dt ** 2) / (2 * gn)
            xi = np.minimum(Gf(gn) ** 2 / np.maximum(dGf(gn) * dgn * gs, 1e-300), 1e4); f = fsm2(X / xi)
        gfr = -X ** -2.0 * f + eta * M; gft = -eta * STt * np.ones_like(X); gm = np.sqrt(gfr ** 2 + gft ** 2); nue = float(nu(eta)); nf = nu(gm)
        Fr = (nf - 1) * gfr - (nue - 1) * eta * M; Ft = -(nf - nue) * eta * STt * np.ones_like(X); l = np.arange(L + 1)[None, :]
        with np.errstate(all="ignore"):
            s.a = (Fr * s.w[None, :]) @ s.Pl.T * (2 * l + 1) / 2; bb = (Ft * s.w[None, :] * (-STt)) @ s.dP.T
        s.b = np.zeros_like(s.a); s.b[:, 1:] = bb[:, 1:] * (2 * l[:, 1:] + 1) / (2 * l[:, 1:] * (l[:, 1:] + 1))
        d = s.a - l * s.b; s.C2 = 0.6 * float(np.trapz(d[:, 2] / s.x, s.u)); s.spl0 = CubicSpline(s.u, s.a[:, 0] * s.x ** 2)
    def q(s): return 2 * abs(s.C2)
PL = json.load(open(os.path.join(RB, "RQ3_acceptance_v2/tolerances.json")))["PLANETS"]; GMs = 1.32712440018e20; YR = 365.25 * 86400; MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)
def rate(A, a, e, nn, N):   # CZ3 / AZ12 verbatim
    t, w = np.polynomial.legendre.leggauss(N); E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (nn * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))
P("\n== T1 Cassini and T4 planets, 3D (Sun as a point mass, eta from 2.32e-10 inverted)")
T1, T4 = {}, {}; K34 = {"canonical": dict(cas=13.3, pl=3.13e-07), "alt": dict(cas=18.11, pl=6.75e-07)}; k3, k4 = [], []
for foot, a0 in A0SI.items():
    rM = math.sqrt(G * MS / a0); qp = CEIL / (1.5 * a0 / rM); eta = eta_newton(GCAS, a0); sv = Solver(eta, "LOC3"); xq = sv.q() / qp
    rM_s = math.sqrt(GMs / a0); A = lambda r, sv=sv, rM_s=rM_s, a0=a0: -a0 * sv.spl0(np.log(r / rM_s)) / (r / rM_s) ** 2; zz = {}
    for nm, dd in PL.items():
        e = ECC[nm]; aa = dd["a_au"] * AU; nn = math.sqrt(GMs / aa ** 3); zz[nm] = abs(rate(A, aa, e, nn, 256) * YR / MAS) / max(dd["EPM"], dd["INPOP"])
    pw = max(zz.values()); T1[foot] = dict(x_ceiling=xq, ok=bool(xq <= 1)); T4[foot] = dict(Z=zz, worst=pw, ok=bool(pw <= 2))
    if not MUT: k3.append(abs(xq / K34[foot]["cas"] - 1)); k4.append(abs(pw / K34[foot]["pl"] - 1))
    P(f"  [{foot}] Cassini {xq:.4g} x ceiling ({'PASS' if xq <= 1 else 'FAIL'}); planets worst Z {pw:.3g} ({'PASS' if pw <= 2 else 'FAIL'}); Saturn {zz['Saturn']:.3g}, Mars {zz['Mars']:.3g}")
check("K3", MUT or max(k3) <= 0.01, f"3D Cassini reproduces CW1's 13.3 / 18.11, max rel {max(k3) if k3 else 0:.1e} (1 %)")
check("K4", MUT or max(k4) <= 0.01, f"3D planets reproduce CW1's worst Z 3.13e-7 / 6.75e-7, max rel {max(k4) if k4 else 0:.1e} (1 %)")

# =============== T0 MW and T3 SPARC, carried ===============
J = lambda p: json.load(open(os.path.join(RB, p))); mwj = J("KT26_local_filter_rule/kt26.json"); spj = J("KT27_local_rule_alt_grade/kt27.json"); T0, T3 = {}, {}
for foot in A0SI:
    n = mwj[f"mw|{foot}|0.5"]["n_pass"]; s = spj[f"sparc|{foot}"]; T0[foot] = dict(n=n, ok=n >= 1); T3[foot] = dict(d_rms=s["d_rms"], ok=bool(s["ok"]))
    P(f"  T0 [{foot}] MW cells {n} ({'PASS' if n >= 1 else 'FAIL'}), carried from KT26; T3 SPARC d rms {s['d_rms']:+.4f} ({'PASS' if s['ok'] else 'FAIL'}), carried from KT27")

# =============== labels ===============
P("\nLABELS (3D local rule, Newtonian external field)"); LAB = {}
for foot in A0SI:
    c = T2[foot]["E1"]["counts"]; t2ok = c["R2"] >= 15; strict = c["R2"] >= c["plain3"]
    bad = [t for t, ok in (("T0 MW", T0[foot]["ok"]), ("T1 Cassini", T1[foot]["ok"]), ("T2 dwarfs", t2ok), ("T3 SPARC", T3[foot]["ok"]), ("T4 planets", T4[foot]["ok"])) if not ok]
    lab = "LOC SURVIVES" if not bad else "LOC FAILS: " + ", ".join(bad)
    if any(k in FAILS for k in ("K1", "K3", "K4", "K5")): lab = "NOT EVALUABLE (" + lab + ")"
    LAB[foot] = dict(label=lab, strict=bool(strict), dwarfs_3D=c["R2"], dwarfs_plain3=c["plain3"], cassini=T1[foot]["x_ceiling"], planets_worst=T4[foot]["worst"], T0=T0[foot], T3=T3[foot])
    P(f"LABEL [{foot}] {lab}  (dwarfs 3D {c['R2']}/24, plain 3D {c['plain3']}/24: STRICT {'pass' if strict else 'fail'}; Cassini {T1[foot]['x_ceiling']:.3g}x)")
RES.update(T1=T1, T4=T4, T0=T0, T3=T3, labels=LAB, T2_counts={f: T2[f] for f in T2})
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
P(f"\nfailed checks: {len(FAILS)} {FAILS}; wall {time.time() - T00:.0f} s; peak RSS {rss:.2f} GB"); RES["failed"] = FAILS; RES["peak_rss_gb"] = rss
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"cz5{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cz5{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
