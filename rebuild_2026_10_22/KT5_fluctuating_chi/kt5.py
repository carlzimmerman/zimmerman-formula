#!/usr/bin/env python3
"""KT5: fluctuating chi. Part 1 option space, Part 2 kernel on SPARC and Cassini. See FROZEN_CRITERIA.md."""
import glob, itertools, json, math, os, sys
import numpy as np, sympy as sp
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "../../real_research/data/sparc_data")
MUT = os.environ.get("KT5_MUTATE") == "1"
res = {}
# ---- Part 1
chi, N, cE, n, Ys, rc2, m0, T, G, s = sp.symbols("chi N c_E n Y rc2 m0 T G s", positive=True)
d = sp.Symbol("delta", positive=True)
pow_m = 2 if MUT else 1
m = m0 * (1 - chi) ** pow_m
V = -N * T * m**3 / (12 * sp.pi)
Vp = sp.simplify(sp.diff(V, chi).subs(T, cE * rc2 / m0**3))
print("V'(chi) =", Vp)
# n chi^(n-1) g^2/(8 pi G) = V', with rc2 = s^2/G
g2 = sp.simplify(Vp.subs(rc2, s**2 / G) * 8 * sp.pi * G / (n * chi ** (n - 1)))
print("g^2/s^2 =", sp.simplify(g2 / s**2))
if MUT:
    print("MUTATE: near vacuum g ~ delta^%d, mu ~ delta, so mu ~ Y^(1/%d): no linear slope; kappa formula void" % (3 * pow_m - 1 if False else 2 * pow_m + (pow_m - 1), 2 * pow_m + (pow_m - 1)))
    print("MUTATE bites")
    sys.exit(1)
yy = sp.sqrt(sp.simplify(g2 / s**2).subs(chi, 1 - d))
slope = sp.simplify(sp.limit(n * d / yy, d, 0))  # mu ~ n delta
k2 = sp.simplify(1 / slope**2)
print("kappa^2 =", k2)
rows = []
cs = {"1": 1.0, "2": 2.0, "3/4pi": 3 / (4 * math.pi), "12pi": 12 * math.pi}
for NN, nn, (cn, cv) in itertools.product((1, 2), (1, 2, 3, 4), cs.items()):
    kv = math.sqrt(2 * NN * cv / nn**3)
    rows.append((NN, nn, cn, kv))
    print(f"  N {NN} n {nn} c_E {cn:6s} kappa {kv:.4f} {'WINDOW' if .227 <= kv <= .607 else ''} {'HALF' if abs(kv-.5) < 1e-12 else ''}")
pw = sum(.227 <= r[3] <= .607 for r in rows) / len(rows)
ph = sum(abs(r[3] - .5) < 1e-12 for r in rows) / len(rows)
print(f"p_data {pw:.3f}, p_half {ph:.3f}, distinct {len({round(r[3],6) for r in rows})}: MENU, 1/2 SPURIOUS unless a selector exists")
print("half rows:", [r[:3] for r in rows if abs(r[3] - .5) < 1e-12])
c_l, Gv, hb = 2.99792458e8, 6.674e-11, 1.0546e-34
H0 = 67.4e3 / 3.0857e22
rc = 3 * H0**2 / (8 * math.pi * Gv)
rhoL = .685 * rc
HL = H0 * math.sqrt(.685)
Tds = hb * HL / (2 * math.pi)
m_req = (rhoL * c_l**2 / Tds) ** (1 / 3)
print(f"H3 with T_dS: m0 = {m_req:.3e} /m, length {1/m_req:.3e} m; H4 ratio T/(hbar c m0) = {Tds/(hb*c_l*m_req):.3e} (needs >> 1): {'H4 holds' if Tds/(hb*c_l*m_req) > 10 else 'H4 FAILS, T_dS not allowed'}")
L = c_l / math.sqrt(Gv * rhoL)
Tneed = rhoL * c_l**2 * L**3
print(f"H3 with m0 = sqrt(G rho)/c: T = {Tneed:.3e} J; T/T_dS = {Tneed/Tds:.3e}; T/(rho c^2 L^3) = 1 by construction: T is unnamed")
res["part1"] = dict(p_data=pw, p_half=ph, rows=rows)

# ---- Part 2 kernel
Y = sp.Symbol("Y", positive=True)
t = (sp.sqrt(Y**2 + 4) - Y) / 2
ok1 = sp.simplify(1 / t - t - Y) == 0
num = [abs((1 - float(t.subs(Y, v)) ** 4) - (1 - math.exp(-4 * math.asinh(v / 2)))) < 1e-12 for v in (.1, 1, 7, 90)]
print("kernel: Y = 1/t - t", ok1, "; mu = 1-exp(-4 asinh(Y/2)) numeric", all(num), "; slope", sp.limit((1 - t**4) / Y, Y, 0), "; tail Y^4(1-mu) ->", sp.limit(t**4 * Y**4, Y, sp.oo))
mu_new = lambda Yv: -np.expm1(-4 * np.arcsinh(Yv / 2))
mu_or2 = lambda Yv: 1 - (1 + Yv) ** -2.0

S = {"rho_DE": c_l * math.sqrt(Gv * rhoL), "rho_crit": c_l * math.sqrt(Gv * rc)}
def load(fu=1.0):
    gb, go, gal = [], [], []; i = 0
    for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: dd = np.genfromtxt(fn, comments="#")
        except Exception: continue
        if dd.ndim != 2 or dd.shape[1] < 6 or len(dd) < 3: continue
        Rr, Vo, eV, Vg, Vd, Vb = (dd[:, j] for j in range(6))
        mm = (Rr > 0) & (Vo > 0) & (eV > 0) & (eV / Vo < .10)
        if mm.sum() < 3: continue
        Rr, Vo, Vg, Vd, Vb = Rr[mm], Vo[mm], Vg[mm], Vd[mm], Vb[mm]
        Vb2 = Vg * abs(Vg) + fu * .5 * Vd * abs(Vd) + fu * .7 * Vb * abs(Vb)
        k = Vb2 > 0
        if k.sum() < 3: continue
        r = Rr[k] * 3.0857e19
        gb.append(Vb2[k] * 1e6 / r); go.append(Vo[k] ** 2 * 1e6 / r); gal.append(np.full(k.sum(), i)); i += 1
    return map(np.concatenate, (gb, go, gal))
def pred(gb, s_, mu):
    lo, hi = gb.copy(), gb * 10 + np.sqrt(gb * s_) * 10 + 1e-13
    for _ in range(70):
        mid = .5 * (lo + hi); f = mid * mu(mid / s_) - gb
        lo, hi = np.where(f < 0, mid, lo), np.where(f < 0, hi, mid)
    return .5 * (lo + hi)
def stat(gb, go, gal, s_, mu):
    r = np.log10(go) - np.log10(pred(gb, s_, mu))
    ng = gal.max() + 1
    return math.sqrt((np.bincount(gal, r**2) / np.bincount(gal)).mean()), float(np.median(r))
gb, go, gal = load()
print(f"SPARC {gal.max()+1} galaxies {len(gb)} points")
for f, s_ in S.items():
    a = stat(gb, go, gal, s_, mu_new); b = stat(gb, go, gal, s_, mu_or2)
    gate = a[0] <= b[0] + .005 and abs(a[1]) <= .05
    print(f"Gate S {f}: new rms {a[0]:.4f} median {a[1]:+.4f}; OR mu_2 rms {b[0]:.4f} median {b[1]:+.4f}; {'PASS' if gate else 'FAIL'}")
    res["S_" + f] = dict(new=a, or2=b, passed=bool(gate))
for fu in (.8, 1.25):
    a_, b_, c_ = load(fu)
    for f, s_ in S.items():
        print(f"  Upsilon x{fu} {f}: new {stat(a_, b_, c_, s_, mu_new)}, OR2 {stat(a_, b_, c_, s_, mu_or2)}")
scat = np.log10(go) - np.log10(pred(gb, S["rho_DE"], mu_new))
mock = pred(gb, S["rho_DE"], mu_new) * 10 ** (scat - scat.mean())
pa, pb = stat(gb, mock, gal, S["rho_DE"], mu_new)[0], stat(gb, mock, gal, S["rho_DE"], mu_or2)[0]
print(f"Planted: new {pa:.4f} vs OR2 {pb:.4f}: {'ranks new first' if pa < pb else 'FAILS TO RANK'}")

# ---- Cassini, copied from fc_cassini_CORRECTED_2026.py
GM_SUN = 6.6743e-11 * 1.98892e30
GEXT, Q2_CEIL = 2.32e-10, 5.2e-27
PREF = lambda a0: 1.5 * a0**1.5 / math.sqrt(GM_SUN)
def nu_from_mu(mux):
    def f(y):
        y = np.atleast_1d(np.asarray(y, float)); out = np.empty_like(y)
        for i, yy in enumerate(y):
            out[i] = brentq(lambda x: x * mux(x) - yy, 1e-12, yy + 50.0, xtol=1e-14) / yy
        return out if out.size > 1 else out[0]
    return f
def nu_routeA(y):
    y = np.asarray(y, float); s_ = np.sqrt(y)
    out = np.where(s_ < 1e-8, 1.0 / np.maximum(s_, 1e-300), 1.0 / (1.0 - np.exp(-np.minimum(s_, 700.0))))
    return np.where(s_ > 40.0, 1.0 + np.exp(-np.minimum(s_, 700.0)), out)
def solve_eN(nu, et):
    return brentq(lambda x: x * float(np.asarray(nu(x)).ravel()[0]) - et, 1e-12, 1e10, xtol=1e-15, rtol=8.9e-16)
def q_direct2D(nu, et, vmax=400.0):
    eN = solve_eN(nu, et)
    def ig(mu, v):
        D = eN * eN + v**4 + 2.0 * eN * v * v * mu
        if D <= 0: return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv - 1.0) * (eN * (3 * mu - 5 * mu**3) + v * v * (1 - 3 * mu * mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-7, epsrel=1e-5)
    return abs(1.5 * val)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
new_x = lambda x: -math.expm1(-4 * math.asinh(x / 4))
or2_x = lambda x: 1 - (1 + x / 2) ** -2.0
mil = lambda k: (lambda x: x / (1 + x**k) ** (1 / k))
for name, a0 in A0.items():
    et, qp = GEXT / a0, Q2_CEIL / PREF(a0)
    if name == "canonical":
        g_ = q_direct2D(nu_routeA, et)
        print(f"guard routeA q {g_:.4f} (anchor 0.221) eta {et:.3f} Q_PASS {qp:.4f}")
    for nm, fn_ in [("NEW", new_x), ("OR mu_2", or2_x), ("Milgrom 3", mil(3)), ("Milgrom 4", mil(4))]:
        qv = q_direct2D(nu_from_mu(fn_), et)
        print(f"Gate C {name} {nm}: q {qv:.4f} = {qv/qp:.2f} x ceiling {'PASS' if qv < qp else 'FAIL'}", flush=True)
        res[f"C_{name}_{nm}"] = dict(q=qv, ratio=qv / qp)
json.dump(res, open(os.path.join(HERE, "kt5.json"), "w"), indent=1, default=str)
