#!/usr/bin/env python3
"""CQ2: v3s's Gaia DR4 wide-binary prediction through CW1's machinery. Criteria 532e0dc567.
OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq2.py [--mutate]
Static limit: switch state from X3's D2 rows; linear response about the Galactic background; relative acceleration from
C6's Route F monopole (copied from c6_solver.py, not imported): gamma_r = 1 + rho^2 F(rho; x_e), rho = r / L*.
DR3 Q (KT21's estimator) and the frozen DR4 pipeline (imported read only, bytecode off) copied from CW1's cw1.py; CW1's
random sequence is replayed so its Newton and plain numbers are reproduced; V3S is fitted on Newton's draws (paired).
--mutate: the switch inverted (stiffness only where D.P < 0, i.e. nowhere near the binaries), so the binary sees the
unscreened law; stand-in = CW1's plain QUMOND curve.  kappa = 1/2 FITTED; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import contextlib, copy, gc, io, json, math, re, resource, sys, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
CW1D = os.path.join(REPO, "cw_lanes_2026_11_04", "CW1_wide_binary_seal_dr4")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
G, MS, AU, PC = 6.6743e-11, 1.98892e30, 1.495978707e11, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GOBS = (1.778e-10, 1.9e-10, 2.32e-10); GPRI = 1.9e-10
LFL = {"canonical": 21.682, "alt": 22.849}; LOTH = (24.0, 50.0, 90.0)          # X3's switched L* floors (pc); C6's L* rows
S_KAU = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], float); MASSES = (0.5, 1.0, 1.5, 2.5); SSYS = 0.020; SGT = 0.028
P(f"CQ2 (criteria 532e0dc567){'  [MUTATE: switch inverted, unscreened stand-in = plain QUMOND]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
RES["inputs"] = dict(A0=A0, GOBS=GOBS, GPRI=GPRI, Lstar_floor_pc=LFL, Lstar_rows_pc=LOTH, s_kAU=S_KAU.tolist(), masses=MASSES, mutate=MUT)

# ================= Route F (C6's c6_solver.py, r_F = 0 closed-form kernel, copied) =================
def chi_c6(kap, c, xe):
    m = (1 - c * c) / (1 + xe) + c * c / (1 + xe) ** 2
    return m / (1 - m + kap ** 2 * m / 2)
def routeF_radial(GM, L, xe, r, nc=48, kmul=400.0, nk=200000):
    """Monopole anomalous radial acceleration at r of a point mass GM in a uniform Galactic field x_e = g/a0 (screened, L*)."""
    rho = r / L
    cg, cw = np.polynomial.legendre.leggauss(nc)
    K = kmul / rho
    lk = np.linspace(np.log(1e-6), np.log(K), nk); k = np.exp(lk)
    c0 = np.concatenate([0.5 * (chi_c6(kk[:, None], cg[None, :], xe) * cw).sum(1) for kk in np.array_split(k, 20)])
    z = k * rho
    j1 = np.where(z < 1e-3, z / 3 - z ** 3 / 30, np.sin(z) / z ** 2 - np.cos(z) / z)
    head = np.trapz(k * k * j1 * c0, lk)
    a = K * rho
    t1 = quad(lambda zz: 1 / zz ** 3, a, np.inf, weight="sin", wvar=1.0)[0]
    t2 = quad(lambda zz: 1 / zz ** 2, a, np.inf, weight="cos", wvar=1.0)[0]
    return 2 * GM / (np.pi * L ** 2) * (head + 2 * (t1 - t2))
def Fof(rho, xe, **kw): return routeF_radial(1.0, 1.0, xe, rho, **kw)   # F = Delta a L*^2 / (G M): a function of rho, x_e only

P("\n== K1: Route F copy vs C6's recorded wide binary (1.5 Msun, 20 kAU, gamma_v - 1)")
c6 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json")))["R3_wide_binary"]
d7b = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json")))["grid"]
A0C6 = {"canonical": 9.36e-11, "alt": 1.13e-10}; GMS = 1.32712440018e20; s20 = 20e3 * AU; e1 = 0.0; K1R = {}
for f in A0C6:
    for Lpc in LOTH:
        vals = [math.sqrt(1 + routeF_radial(1.5 * GMS, Lpc * PC, v["ge_total"] / A0C6[f], s20) / (1.5 * GMS / s20 ** 2)) - 1 for E, v in d7b[f]["none"].items()]
        ref = c6[f"{f}|{Lpc:g}"]["gamma_minus_1"]; e1 = max(e1, max(abs(a / b - 1) for a, b in zip(vals, ref))); K1R[f"{f}|{Lpc:g}"] = dict(mine=vals, c6=ref)
        P(f"  [{f}] L* {Lpc:g} pc: " + " ".join(f"{v:.6e}" for v in vals) + "  (C6 " + " ".join(f"{v:.6e}" for v in ref) + ")")
RES["K1"] = K1R
check("K1", e1 <= 1e-6, f"C6's 24 wide-binary numbers reproduced, max rel {e1:.2e} (line 1e-6)")

# ================= switch state and linearity =================
P("\n== Switch state (X3 D2 rows, read only) and linearity")
x3 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness_results.json")))["D2"]
mar = []
for row in x3["rows"]:
    mb = row["rho_gal_min"] / (2.5 * row["max_neg_lobe_Msun_pc3"]); mar.append(mb)
    P(f"  [{row['foot']}] x_e {row['x_e']}, L* {row['Lstar_pc']} pc: 1 Msun lobe {row['max_neg_lobe_Msun_pc3']:.3e} Msun/pc^3 at {row['at_r_pc']:.0f} pc; rho_gal,min {row['rho_gal_min']:.4f}; margin 1 Msun {row['margin']:.3g}, 2.5 Msun {mb:.3g}")
RES["switch"] = dict(binary_margins=mar, min_binary_margin=min(mar), near_zone_min=x3["H4_C3_min"], galactic=x3["galactic"])
check("K4", min(mar) >= 10 and x3["H4_C3_min"] > 0, f"min binary margin (M_tot 2.5 Msun) {min(mar):.3g} (line 10); near-zone minimum {x3['H4_C3_min']:+.4f} Msun/pc^3 > 0")
eps = {}
for foot, a0 in A0.items():
    for go in GOBS:
        xe = go / a0; eps[f"{foot}|{go:.4g}"] = (G * 2.5 * MS / (LFL[foot] * PC) ** 2) / (a0 * xe / (1 + xe))
P("  epsilon (hedgehog over background p, 2.5 Msun at the floor): " + "; ".join(f"{k} {v:.2e}" for k, v in eps.items()))
RES["epsilon"] = eps
check("K5", max(eps.values()) <= 1e-4, f"linearity, max epsilon {max(eps.values()):.2e} (line 1e-4)")

# ================= gamma_r(s): sealed grid, direct =================
P("\n== gamma_r(s) - 1 of v3s-REST (Route F monopole, L* floor); analytic screened limit (s/L*)^2 beside")
GR = {}; TAB = {}
for foot, a0 in A0.items():
    L = LFL[foot] * PC; r = S_KAU * 1e3 * AU; P(f"[{foot}] L* {LFL[foot]} pc; s kAU " + " ".join(f"{v:9.0f}" for v in S_KAU))
    P(f"  analytic (s/L*)^2          " + " ".join(f"{v:9.3e}" for v in (r / L) ** 2))
    for go in GOBS:
        xe = go / a0
        for m in (MASSES if go == GPRI else (1.0,)):
            GM = G * m * MS; da = np.array([routeF_radial(GM, L, xe, ri) for ri in r]); gm1 = da / (GM / r ** 2); F = gm1 / (r / L) ** 2
            GR[f"{foot}|{go:.4g}|M{m}"] = dict(gamma_r_minus_1=gm1.tolist(), F=F.tolist(), analytic=((r / L) ** 2).tolist(), x_e=xe)
            P(f"  g {go:.4g}, M {m:3.1f}: " + " ".join(f"{v:9.3e}" for v in gm1) + f"   F {F.min():.4f}-{F.max():.4f}")
    # log-rho table at the primary field for the injections (F depends on rho and x_e only)
    # beyond r = L* (rho > 1: no bound binary; only rare DR3 projection draws) the unscreened linear far value
    # gamma - 1 -> c0(k -> 0) = (1/2) int m/(1 - m) dc is used (Route F's rho -> infinity limit)
    xe = GPRI / a0; rho = np.geomspace(10 * AU / L, 1.0, 61); Fv = np.array([Fof(v, xe) for v in rho])
    cg_, cw_ = np.polynomial.legendre.leggauss(64); m_ = (1 - cg_ ** 2) / (1 + xe) + cg_ ** 2 / (1 + xe) ** 2
    TAB[foot] = dict(lnrho=np.log(rho), F=Fv, spl=CubicSpline(np.log(rho), Fv), c0lin=float(0.5 * np.sum(m_ / (1 - m_) * cw_)))
    P(f"  table: F(rho = 1) {Fv[-1]:.4f}; unscreened far value c0_lin {TAB[foot]['c0lin']:.4f} (used only for rho > 1); min F {Fv.min():.4f}, max F {Fv.max():.4f}")
    for Lpc in LOTH:
        rh = r / (Lpc * PC); g_ = rh ** 2 * TAB[foot]["spl"](np.log(rh)); GR[f"{foot}|{GPRI:.4g}|L{Lpc:g}"] = dict(gamma_r_minus_1=g_.tolist())
        P(f"  L* {Lpc:g} pc (table):     " + " ".join(f"{v:9.3e}" for v in g_))
RES["gamma_r"] = GR; RES["table"] = {f: dict(lnrho=TAB[f]["lnrho"].tolist(), F=TAB[f]["F"].tolist(), c0lin=TAB[f]["c0lin"]) for f in TAB}
def Fspl(foot, rho):
    t = TAB[foot]; return t["spl"](np.clip(np.log(rho), t["lnrho"][0], t["lnrho"][-1]))
def gam_v3s(r, foot, far="c0lin"):
    rho = np.atleast_1d(np.asarray(r, float)) / (LFL[foot] * PC); g = 1 + np.minimum(rho, 1.0) ** 2 * Fspl(foot, rho)
    if far == "c0lin": g = np.where(rho > 1.0, 1 + TAB[foot]["c0lin"], g)
    return g
fdev = max(max(abs(v - 1) for v in g["F"]) for k, g in GR.items() if "F" in g)
check("K6", fdev <= 0.05, f"screened limit, max |F - 1| on the sealed grid {fdev:.4f} (line 0.05)")
k7a, k7b = 0.0, 0.0
for foot, a0 in A0.items():
    L = LFL[foot] * PC; xe = GPRI / a0
    for j, sk in ((0, 1.0), (8, 30.0)):
        hi = routeF_radial(G * MS, L, xe, sk * 1e3 * AU, nc=96, kmul=800.0, nk=400000) / (G * MS / (sk * 1e3 * AU) ** 2)
        k7a = max(k7a, abs(hi / GR[f"{foot}|{GPRI:.4g}|M1.0"]["gamma_r_minus_1"][j] - 1))
    for rk in (1.37, 4.3, 12.9, 26.1, 150.0):
        rh = rk * 1e3 * AU / L; k7b = max(k7b, abs(float(Fspl(foot, rh)) / Fof(rh, xe) - 1))
check("K7", k7a <= 1e-3 and k7b <= 1e-4, f"Route F doubled resolution moves gamma_r - 1 by {k7a:.2e} rel (line 1e-3); table interpolation {k7b:.2e} rel (line 1e-4)")
Q2C6 = {"canonical": 1.86e-34, "alt": 1.58e-34}   # C6 README: max Q2 (s^-2) at L* = 24 pc, 1 Msun, E0-E3
ANI = {f: Q2C6[f] * (24.0 / LFL[f]) ** 3 * (30e3 * AU) ** 3 / (G * MS) for f in A0}
P("  anisotropic (quadrupole) part relative to Newton at 30 kAU, from C6's Q2 scaled to the floor: " + "; ".join(f"{f} {v:.1e}" for f, v in ANI.items()) + " (reported, not injected)")
RES["anisotropy_bound_30kAU"] = ANI

# ================= CW1's machinery (copied from cw1.py; the forms CW1 used, for the replayed sequence) =================
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
Gf = lambda y: y * nu(y)
dGf = lambda y: nu(y) - 1 / (2 * np.maximum(y, 1e-300) * np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def eta_newton(gobs, a0):
    eo = gobs / a0; return brentq(lambda y: float(Gf(y)) - eo, 1e-9, eo)
def fsm(t):
    t = np.asarray(t, float); out = np.empty_like(t); s = t < 1e-3
    out[~s] = erf(t[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * t[~s] * np.exp(-t[~s] ** 2 / 2); out[s] = math.sqrt(2 / math.pi) / 3 * t[s] ** 3; return out
def legendre(L, mu):
    Pl = np.zeros((L + 1, mu.size)); dP = np.zeros((L + 1, mu.size)); Pl[0] = 1; dP[0] = 0
    if L >= 1: Pl[1] = mu; dP[1] = 1
    for l in range(1, L):
        Pl[l + 1] = ((2 * l + 1) * mu * Pl[l] - l * Pl[l - 1]) / (l + 1); dP[l + 1] = dP[l - 1] + (2 * l + 1) * Pl[l]
    return Pl, dP
class Solver:
    def __init__(s, eta, form, gs=2.0, L=64, nmu=96, per_dec=200, xmin=1e-7, xmax=1e5):
        s.eta, s.form, s.gs, s.L = eta, form, gs, L
        s.u = np.linspace(math.log(xmin), math.log(xmax), int(round(per_dec * math.log10(xmax / xmin))) + 1); s.du = s.u[1] - s.u[0]; s.x = np.exp(s.u)
        s.mu, s.w = np.polynomial.legendre.leggauss(nmu); s.st = np.sqrt(1 - s.mu ** 2); s.Pl, s.dP = legendre(L, s.mu)
        X, M = s.x[:, None], s.mu[None, :]; ST = s.st[None, :]
        s.xi = s.width(X, M)
        f = np.ones_like(X * M) if s.xi is None else fsm(X / s.xi)
        gfr = -X ** -2.0 * f + eta * M; gft = -eta * ST * np.ones_like(X); gm = np.sqrt(gfr ** 2 + gft ** 2); nue = float(nu(eta)); nf = nu(gm)
        Fr = (nf - 1) * gfr - (nue - 1) * eta * M; Ft = -(nf - nue) * eta * ST * np.ones_like(X)
        l = np.arange(L + 1)[None, :]
        with np.errstate(all="ignore"):
            s.a = (Fr * s.w[None, :]) @ s.Pl.T * (2 * l + 1) / 2
            bb = (Ft * s.w[None, :] * (-ST)) @ s.dP.T
        s.b = np.zeros_like(s.a); s.b[:, 1:] = bb[:, 1:] * (2 * l[:, 1:] + 1) / (2 * l[:, 1:] * (l[:, 1:] + 1))
        assert np.all(np.isfinite(s.a)) and np.all(np.isfinite(s.b)), "non-finite multipole coefficients"
        c = s.a + (l + 1) * s.b; d = s.a - l * s.b; n = s.x.size; lv = np.arange(L + 1)
        A = np.zeros_like(c); B = np.zeros_like(d); q = math.exp(-s.du); qa = q ** (lv + 2); qb = q ** (lv - 1.0)
        A[0] = c[0] / (lv + 2)
        for i in range(n - 1): A[i + 1] = qa * A[i] + 0.5 * s.du * (qa * c[i] + c[i + 1])
        B[-1] = d[-1] / (lv + 1)
        for i in range(n - 2, -1, -1): B[i] = qb * B[i + 1] + 0.5 * s.du * (d[i] + qb * d[i + 1])
        s.gr = s.a - (lv * (lv + 1) / (2 * lv + 1))[None, :] * (A + B)
        s.gself = float(s.gr[0, 1]) if L >= 1 else 0.0
        s.spl = CubicSpline(s.u, s.gr * s.x[:, None] ** 2, axis=0); s.spl0 = CubicSpline(s.u, s.a[:, 0] * s.x ** 2)
        del s.a, s.b, s.gr, s.Pl, s.dP
    def width(s, X, M):
        f, eta, gs = s.form, s.eta, s.gs
        if f in ("PQ", "N"): return None
        if f == "E55": return 0.55 * np.ones_like(X * M)
        if f == "HALF": return 0.5 * np.ones_like(X * M)
        if f == "LOC1":
            gq = np.sqrt(X ** -4.0 + eta * eta); dg = np.abs(dGf(gq) * (-2 * X ** -5.0 / gq)); xi = Gf(gq) ** 2 / np.maximum(dg * gs, 1e-300)
            return np.minimum(xi, 1e4) * np.ones_like(M)
        if f == "LOC3":
            g2 = X ** -4.0 + eta * eta - 2 * eta * X ** -2.0 * M; gn = np.sqrt(np.maximum(g2, 1e-300))
            dr = -4 * X ** -5.0 + 4 * eta * X ** -3.0 * M; dt = 2 * eta * X ** -3.0 * np.sqrt(1 - M ** 2); dgn = np.sqrt(dr ** 2 + dt ** 2) / (2 * gn)
            xi = Gf(gn) ** 2 / np.maximum(dGf(gn) * dgn * gs, 1e-300); return np.minimum(xi, 1e4)
        raise ValueError(f)
    def gamma(s, x, mu):
        x = np.atleast_1d(np.asarray(x, float)); mu = np.atleast_1d(np.asarray(mu, float)); uu = np.log(np.clip(x, s.x[0], s.x[-1]))
        y2 = s.spl(uu); Pm, _ = legendre(s.L, mu)
        pair = x.size == mu.size
        with np.errstate(all="ignore"): g2 = np.sum(y2 * Pm.T, 1) if pair else y2 @ Pm
        xx = x if pair else x[:, None]; mm = mu if pair else mu[None, :]
        return 1 - g2 + xx ** 2 * s.gself * mm
    def gamma_avg(s, x):
        x = np.asarray(x, float); return 1 - s.spl0(np.log(np.clip(x, s.x[0], s.x[-1])))
    def table(s, xlo=1e-4, xhi=1e4, nx=1601, nm=201):
        tx = np.geomspace(xlo, xhi, nx); tm = np.linspace(-1, 1, nm); return tx, tm, s.gamma(tx, tm)
def interp2(tx, tm, T, x, mu):
    lx = np.log(np.clip(x, tx[0], tx[-1])); fx = (lx - math.log(tx[0])) / (math.log(tx[-1] / tx[0])) * (tx.size - 1); i = np.clip(fx.astype(int), 0, tx.size - 2); a = fx - i
    fm = (np.clip(mu, -1, 1) + 1) / 2 * (tm.size - 1); j = np.clip(fm.astype(int), 0, tm.size - 2); b = fm - j
    return (1 - a) * (1 - b) * T[i, j] + a * (1 - b) * T[i + 1, j] + (1 - a) * b * T[i, j + 1] + a * b * T[i + 1, j + 1]
def orbits3(rng, alpha, m):
    e = rng.uniform(0, 1, m) ** (1 / (alpha + 1)); Mn = rng.uniform(0, 2 * math.pi, m); E = Mn.copy()
    for _ in range(60): E = E - (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E); x = np.cos(E) - e; y = np.sqrt(1 - e * e) * np.sin(E); vx = -np.sin(E) / r; vy = np.sqrt(1 - e * e) * np.cos(E) / r
    ci = rng.uniform(-1, 1, m); w = rng.uniform(0, 2 * math.pi, m)
    X = x * np.cos(w) - y * np.sin(w); Y = x * np.sin(w) + y * np.cos(w); VX = vx * np.cos(w) - vy * np.sin(w); VY = vx * np.sin(w) + vy * np.cos(w)
    rs = np.hypot(X, Y * ci); vs = np.hypot(VX, VY * ci); si = np.sqrt(1 - ci * ci)
    return rs, vs * np.sqrt(rs), r / rs, X / r, Y * ci / r, Y * si / r
def Qs(v, y): return math.log(np.median(v[(y >= 2) & (y < 10)])) - math.log(np.median(v[y >= 10]))
FORMS = ("PQ", "LOC3", "LOC1", "E55", "HALF")
SOLV = {(foot, f): Solver(eta_newton(GPRI, a0), f) for foot, a0 in A0.items() for f in (FORMS if foot == "canonical" else ("PQ",))}
cw1 = json.load(open(os.path.join(CW1D, "cw1.json"))); cw1out = open(os.path.join(CW1D, "cw1.out")).read()
# sealed-grid maximum of the injected curve (V3S-REST, or the plain stand-in under MUTATE)
SEALMAX = {}
for foot, a0 in A0.items():
    if MUT: SEALMAX[foot] = max(float(np.max(SOLV[(foot, "PQ")].gamma_avg(S_KAU * 1e3 * AU / math.sqrt(G * m * MS / a0)))) - 1 for m in MASSES)
    else: SEALMAX[foot] = max(max(g["gamma_r_minus_1"]) for k, g in GR.items() if k.startswith(foot + "|") and "|L" not in k)

# ================= DR3 inner shape: KT21's Q =================
P("\n== DR3 inner shape (KT21's Q, CW1's machinery; primary field 1.9e-10)")
CSV = os.path.join(REPO, "real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv"); d = np.genfromtxt(CSV, delimiter=",", names=True)
s = d["sep_kAU"] * 1e3 * AU; Mt = (d["M1_msun"] + d["M2_msun"]) * MS; vp = d["v_perp_kms"] * 1e3; vt = vp / np.sqrt(G * Mt / s); n = len(s); K = 40
lg, bg = np.radians(d["l_gal"]), np.radians(d["b_gal"]); GL, GB, GN = -np.sin(lg), -np.sin(bg) * np.cos(lg), np.cos(bg) * np.cos(lg)
def zl(z): return "CONSISTENT" if abs(z) <= 2 else "TENSION" if abs(z) <= 3 else "EXCLUDED"
DR3 = {}; e2 = 0.0
for foot, a0 in A0.items():
    y = G * Mt / (a0 * s * s); qo = Qs(vt, y); bs = []
    for seed in (11, 12):
        rng = np.random.default_rng(seed); b = []
        for _ in range(2000): i = rng.integers(0, n, n); b.append(Qs(vt[i], y[i]))
        bs.append(float(np.std(b)))
    sig = math.sqrt(bs[0] ** 2 + SSYS ** 2)
    rng = np.random.default_rng(2026110302); idx = np.repeat(np.arange(n), K); _, vN, ratio, ux, uy, uz = orbits3(rng, 1.2, n * K)
    om = np.random.default_rng(2026110402).uniform(0, 2 * math.pi, n * K); mu = (np.cos(om) * ux - np.sin(om) * uy) * GL[idx] + (np.sin(om) * ux + np.cos(om) * uy) * GB[idx] + uz * GN[idx]
    r3 = s[idx] * ratio; Mi = Mt[idx]; yi = y[idx]; x3 = r3 / np.sqrt(G * Mi / a0)
    tx, tm, T = SOLV[(foot, "PQ")].table(); gPQ = np.maximum(interp2(tx, tm, T, x3, mu), 0); del T
    g3 = gPQ if MUT else gam_v3s(r3, foot)
    pr = dict(N=Qs(vN, yi), PQ=Qs(vN * np.sqrt(gPQ), yi), V3S=Qs(vN * np.sqrt(g3), yi))
    ref = cw1["DR3"][foot]; rp = ref["pred"]["1.9e-10"]
    e2 = max(e2, abs(qo - ref["Q_obs"]), abs(sig - ref["sigma"]), abs(pr["N"] - rp["N"]["Q_pred"]), abs(pr["PQ"] - rp["PQ"]["Q_pred"]))
    rho3 = r3 / (LFL[foot] * PC); qalt = Qs(vN * np.sqrt(gam_v3s(r3, foot, far="clip")), yi) if not MUT else float("nan")
    P(f"  orbit draws with r3 > L* (unbound; far value used): {int(np.sum(rho3 > 1))} of {rho3.size}; V3S Q with rho clipped at 1 instead: {qalt:+.6f}")
    DR3[foot] = dict(Q_obs=qo, sigma=sig, sigma_stat=bs, n_pairs=n, r3_kAU_range=[float(r3.min() / AU / 1e3), float(r3.max() / AU / 1e3)], v3s_max_gamma_minus_1=float(np.max(g3) - 1),
                     v3s_median_gamma_minus_1=float(np.median(g3) - 1), n_rho_gt_1=int(np.sum(rho3 > 1)), n_draws=int(rho3.size), Q_v3s_far_clip=qalt,
                     pred={k: dict(Q_pred=v, z=(qo - v) / sig, label=zl((qo - v) / sig)) for k, v in pr.items()})
    P(f"[{foot}] {n} pairs; Q_obs {qo:+.4f} +- {sig:.4f}; r3 {DR3[foot]['r3_kAU_range'][0]:.2f}-{DR3[foot]['r3_kAU_range'][1]:.0f} kAU; V3S gamma - 1 median {DR3[foot]['v3s_median_gamma_minus_1']:.2e}, max {DR3[foot]['v3s_max_gamma_minus_1']:.2e}")
    P("  " + "; ".join(f"{k} {v['Q_pred']:+.6f} (z {v['z']:+.3f}, {v['label']})" for k, v in DR3[foot]["pred"].items()) + f";  Q(V3S) - Q(N) {pr['V3S'] - pr['N']:+.2e}")
    del vN, ratio, ux, uy, uz, om, mu, r3, Mi, yi, x3, gPQ, g3; gc.collect()
RES["DR3"] = DR3
check("K2", e2 <= 1e-9, f"CW1's DR3 Q_obs, sigma, Q_pred(N), Q_pred(PQ) reproduced, max abs {e2:.1e} (line 1e-9)")

# ================= DR4 pipeline (read only), CW1's random sequence replayed =================
P("\n== Frozen DR4 pipeline: gamma_inf it would return (imported read only, bytecode off)")
PIPE = os.path.join(REPO, "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py")
P(f"pipeline SHA-256 as recorded by CW1 (not recomputed here): {cw1['pipeline']['sha256']}")
sys.path.insert(0, os.path.dirname(PIPE)); import wide_binary_pipeline as wbp; sys.path.pop(0)
assert sys.dont_write_bytecode
rng = np.random.default_rng(20261216); NM = 1_000_000; pop_m = wbp.make_population(NM, rng, dr4=True); nsel = len(pop_m["s_obs"])
with contextlib.redirect_stdout(io.StringIO()):
    MOD = {"canonical": wbp.model_medians(pop_m, wbp.A0_CAN, wbp.GRID, rng), "alt": wbp.model_medians(pop_m, wbp.A0_ALT, wbp.GRID, rng)}
del pop_m; gc.collect()
PA0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}; ND = 30000; NREAL = 4
def vt_custom(pop, gv):
    vX = (gv * pop['pmx'] + pop['npmx']) * 4.74e3 * (pop['d_obs'] / 1000.); vY = (gv * pop['pmy'] + pop['npmy']) * 4.74e3 * (pop['d_obs'] / 1000.); return np.hypot(vX, vY) / pop['vc_obs']
def draw():
    pop = wbp.make_population(int(ND * 2.7), rng, dr4=True); keep = rng.permutation(len(pop['s_obs']))[:ND]; return {k: v[keep] for k, v in pop.items()}
def fit(foot, vt_d, pop, r=None):
    with contextlib.redirect_stdout(io.StringIO()): g, sg, med, sgm, cnt = wbp.run_fit(np.log10(pop['g_proj'] / PA0[foot]), vt_d, MOD[foot], rng if r is None else r, "cq2")
    return g, sg, med
P(f"master population {NM:,} ({nsel:,} after selection), N_data {ND:,}, {NREAL} realisations")
K6 = []
for gi in (1.00, 1.1614):
    pop = draw(); g, sg, _ = fit("canonical", wbp.vtilde_of(pop, gi, wbp.A0_CAN), pop); K6.append(dict(inject=gi, got=g, sg=sg)); P(f"  K6 replay: inject {gi:.4f} -> {g:.4f} +- {sg:.4f}")
cw1k6 = [tuple(map(float, t)) for t in re.findall(r"K6 inject declared shape ([0-9.]+) -> ([0-9.]+) \+- ([0-9.]+)", cw1out)]
e3k6 = max(max(abs(a["got"] - b[1]), abs(a["sg"] - b[2])) for a, b in zip(K6, cw1k6))
PO = {}; rmax = {}
for foot, a0 in A0.items():
    PO[foot] = {}; seq = ("N",) + (FORMS if foot == "canonical" else ("PQ",))
    for f in seq:
        gs_, med_, g3_, med3_ = [], [], [], []
        for _ in range(NREAL):
            pop = draw(); xt = (pop['g_true'] / a0) ** -0.5
            if f == "N":
                rc = copy.deepcopy(rng); g, sg, med = fit(foot, vt_custom(pop, np.ones_like(xt)), pop)
                if MUT: gv3 = np.sqrt(np.maximum(SOLV[(foot, "PQ")].gamma_avg(xt), 0))
                else:
                    rp_ = np.sqrt(wbp.G * pop['M_obs'] * wbp.MSUN / pop['g_true']); gv3 = np.sqrt(gam_v3s(rp_, foot)); rmax[foot] = max(rmax.get(foot, 0.0), float(rp_.max() / AU / 1e3))
                g3, sg3, med3 = fit(foot, vt_custom(pop, gv3), pop, rc); g3_.append(g3); med3_.append(med3)
            else:
                g, sg, med = fit(foot, vt_custom(pop, np.sqrt(np.maximum(SOLV[(foot, f)].gamma_avg(xt), 0))), pop)
            gs_.append(g); med_.append(med)
        PO[foot][f] = dict(gamma_inf=float(np.mean(gs_)), spread=float(np.std(gs_)), each=gs_, bin_median=np.nanmean(np.array(med_), 0).tolist())
        if f == "N": PO[foot]["V3S"] = dict(gamma_inf=float(np.mean(g3_)), spread=float(np.std(g3_)), each=g3_, bin_median=np.nanmean(np.array(med3_), 0).tolist(),
                                            paired_diff=[a - b for a, b in zip(g3_, gs_)], bin_median_ratio_to_N=(np.nanmean(np.array(med3_), 0) / np.nanmean(np.array(med_), 0)).tolist())
    for f in PO[foot]: P(f"  [{foot}] {f:5s} gamma_inf {PO[foot][f]['gamma_inf']:.4f} (spread {PO[foot][f]['spread']:.4f}); each " + " ".join(f"{v:.4f}" for v in PO[foot][f]["each"]))
    P(f"  [{foot}] V3S - N paired per realisation: " + " ".join(f"{v:+.4f}" for v in PO[foot]["V3S"]["paired_diff"]) + "; bin medians V3S / N " + " ".join(f"{v:.6f}" for v in PO[foot]["V3S"]["bin_median_ratio_to_N"]))
e3 = max(abs(a - b) for foot in A0 for f in (("N",) + (FORMS if foot == "canonical" else ("PQ",))) for a, b in zip(PO[foot][f]["each"], cw1["pipeline"]["out"][foot][f]["each"]))
RES["pipeline"] = dict(sha256_from_cw1=cw1["pipeline"]["sha256"], n_master=NM, n_sel=nsel, n_data=ND, n_real=NREAL, K6=K6, out=PO, r_max_kAU=rmax)
check("K3", e3 <= 1e-9 and e3k6 <= 6e-5, f"CW1's gamma_inf for every realisation (N, PQ; and canonical LOC3/LOC1/E55/HALF) reproduced, max abs {e3:.1e} (line 1e-9); K6 vs CW1's printed 4 decimals {e3k6:.1e} (6e-5)")

# ================= separation labels =================
P("\n== Separation (CW1's rule: dQ / 0.020, dgamma_inf / 0.028; SEPARABLE >= 3, MARGINAL >= 2)")
def lab(a, b): m = max(a, b); return "SEPARABLE" if m >= 3 else "MARGINAL" if m >= 2 else "NOT SEPARABLE"
SEP = {}
for foot in A0:
    pr = DR3[foot]["pred"]; po = PO[foot]
    for nm, ref in (("vs_plain", "PQ"), ("vs_newton", "N")):
        dq = abs(pr["V3S"]["Q_pred"] - pr[ref]["Q_pred"]) / SSYS; dg = abs(po["V3S"]["gamma_inf"] - po[ref]["gamma_inf"]) / SGT
        SEP.setdefault(foot, {})[nm] = dict(dQ=dq, dgamma=dg, label=lab(dq, dg))
    dq = abs(pr["PQ"]["Q_pred"] - pr["N"]["Q_pred"]) / SSYS; dg = abs(po["PQ"]["gamma_inf"] - po["N"]["gamma_inf"]) / SGT; SEP[foot]["PQ_vs_newton"] = dict(dQ=dq, dgamma=dg, label=lab(dq, dg))
    P(f"  [{foot}] V3S vs plain: {SEP[foot]['vs_plain']['dQ']:.2f}, {SEP[foot]['vs_plain']['dgamma']:.2f} -> {SEP[foot]['vs_plain']['label']};  V3S vs Newton: {SEP[foot]['vs_newton']['dQ']:.4f}, {SEP[foot]['vs_newton']['dgamma']:.4f} -> {SEP[foot]['vs_newton']['label']};  plain vs Newton {dq:.2f}, {dg:.2f} -> {SEP[foot]['PQ_vs_newton']['label']}")
RES["separation"] = SEP

# ================= verdict =================
P("\n== Verdict lines (frozen)")
VER = {}; scr = RES["checks"]["K4"]["ok"] and RES["checks"]["K5"]["ok"]
for foot in A0:
    dQ = abs(DR3[foot]["pred"]["V3S"]["Q_pred"] - DR3[foot]["pred"]["N"]["Q_pred"]); dG = max(abs(v) for v in PO[foot]["V3S"]["paired_diff"])
    dQ, dG = float(dQ), float(dG); req = dict(max_gamma_minus_1=bool(SEALMAX[foot] <= 1e-3), dQ=bool(dQ <= 1e-3), dgamma_paired=bool(dG <= 1e-3))
    lb = ("NEWTONIAN" if all(req.values()) else "SCREENED, DR4-VISIBLE RESIDUAL") if scr else "SCREENING LIFTED"
    if MUT: lb = "MUTATE (unscreened stand-in): " + ("NEWTONIAN lines fail" if not all(req.values()) else "NEWTONIAN lines still pass")
    VER[foot] = dict(screened_K4_K5=scr, max_gamma_minus_1=SEALMAX[foot], dQ=dQ, dgamma_paired_max=dG, requirements=req, label=lb, vs_newton=SEP[foot]["vs_newton"]["label"], vs_plain=SEP[foot]["vs_plain"]["label"])
    P(f"  [{foot}] screened {scr}; max gamma_r - 1 on the sealed grid {SEALMAX[foot]:.2e}; |Q(V3S) - Q(N)| {dQ:.2e}; paired |dgamma_inf| {dG:.4f} -> {lb}")
RES["verdict"] = VER
if MUT:
    bites = all(not all(VER[f]["requirements"].values()) and VER[f]["vs_newton"] == "SEPARABLE" for f in A0)
    RES["mutate_bites"] = bites; P(f"MUTATE {'BITES' if bites else 'DOES NOT BITE (machinery blind: verdict void)'}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
P(f"\nfailed checks: {len(FAILS)} {FAILS}; wall {time.time() - T0:.0f} s; peak RSS {rss:.2f} GB; kappa = 1/2 FITTED; not theory closed")
RES["failed"] = FAILS; RES["wall_s"] = time.time() - T0; RES["peak_rss_gb"] = rss
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cq2{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cq2{sfx}.json"), "w"), indent=1, default=float)
sys.exit((1 if RES["mutate_bites"] else 0) if MUT else (1 if FAILS else 0))
