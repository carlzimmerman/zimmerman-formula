#!/usr/bin/env python3
"""CZ3: astra's AZ12 planetary precession gate (radial monopole by Gauss' law, exact orbit-averaged secular rate, six planets)
on CZ2's filter rules TID, LOC (and HALF beside), Newtonian Galactic field. Criteria 16e2226f95. AZ12's method re-implemented;
CZ2's xi code copied. OMP_NUM_THREADS=1 python3 -I cz3.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import json, math, os, resource, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf, gammainc
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GEXT = 2.32e-10
GM = 1.32712440018e20; AU = 149597870700.0; YR = 365.25 * 86400; MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)
PL = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json")))["PLANETS"]
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
P(f"CZ3 (criteria 16e2226f95){'  [MUTATE: filter removed]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------- CZ2's filter lengths (copied) ----------
def xi_loc(r, gm, gs, clip):
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
def xi_tid(r, gm, gs, clip):
    tau = np.sqrt(np.gradient(gm, r) ** 2 + 2 * (gm / r) ** 2); lt = np.log(np.maximum(tau, 1e-300))
    dt = np.abs(tau * np.gradient(lt, np.log(r)) / r); return np.minimum(4 / math.sqrt(3) * tau ** 3 / np.maximum(dt * dt * gs, 1e-300), clip)
def gh_pt(r, xi):
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def xi_table(c, eta, n=20000):
    x = np.exp(np.linspace(math.log(1e-7), math.log(1e5), n)); gq = np.sqrt(x ** -4.0 + eta * eta)
    X = xi_loc(x, nu_s(gq) * gq, 1 / KAP, 1e4) if c == "LOC" else xi_tid(x, nu_s(gq) * x ** -2.0, 1 / KAP, 1e4)
    return lambda xx: np.exp(np.interp(np.log(xx), np.log(x), np.log(X)))

# ---------- AZ12's gate ----------
def rate(A, a, e, n, N):
    t, w = np.polynomial.legendre.leggauss(N); E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (n * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))
def monopole(h, a0, ge, N):
    mu, w = np.polynomial.legendre.leggauss(N); H = h[:, None]; m = mu[None, :]; y = np.sqrt(H * H + ge * ge + 2 * H * ge * m) / a0
    return .5 * np.sum(w[None, :] * (nu_s(y) - 1) * (H + ge * m), axis=1)
def field(c, a0, eta, n=20000):
    rM = math.sqrt(GM / a0)
    if MUT: return lambda r: GM / r ** 2
    if c == "AZ12": return lambda r: GM / r ** 2 * gammainc(3, r / (0.5 * rM))
    if c == "HALF": return lambda r: a0 * gh_pt(r / rM, 0.5)
    xt = xi_table(c, eta, n); return lambda r: a0 * gh_pt(r / rM, xt(r / rM))
def grade(c, a0, eta, ge, n=20000, orders=(256, 160)):
    h = field(c, a0, eta, n); rows = {}
    for nm, d in PL.items():
        e = ECC[nm]; a = d["a_au"] * AU; nn = math.sqrt(GM / a ** 3); s = max(d["EPM"], d["INPOP"])
        rt = rate(lambda r: monopole(h(r), a0, ge, orders[1]), a, e, nn, orders[0]) * YR / MAS
        rows[nm] = dict(rate_mas_yr=rt, Z_EPM=abs(rt) / d["EPM"], Z_INPOP=abs(rt) / d["INPOP"], Z=abs(rt) / s)
    return rows

# ---------- checks ----------
for e in ECC.values():
    root = math.sqrt(1 - e * e); err = max(abs(rate(fn, 1, e, 1, 256) - o) for fn, o in ((lambda r: np.ones_like(r), -root), (lambda r: r, -1.5 * root), (lambda r: 1 / r ** 2, 0.0)))
    ok = err <= 1e-10; fail += not ok
P(f"K2 AZ12 oracles (constant, harmonic, inverse-square) at all six eccentricities: {'PASS' if not fail else 'FAIL'}")
AZ12 = {"canonical": dict(Saturn=6.983944012229753, Mars=1.9185778254937969), "alt": dict(Saturn=11.329246327793195, Mars=3.112913570304748)}
for foot, a0 in A0SI.items():
    eta0 = GEXT / a0; etaN = brentq(lambda y: float(nu_s(y)) * y - eta0, 1e-6, eta0); ge = GEXT ** 2 / (GEXT + a0)
    ok = abs(etaN * a0 / ge - 1) <= 1e-8; fail += not ok; P(f"\n[{foot}] K4 AZ11 e = g_e^2/(g_e+a0) {ge:.6e} vs CZ2 eta_N a0 {etaN * a0:.6e}: {'PASS' if ok else 'FAIL'}")
    if not MUT:
        k1 = grade("AZ12", a0, etaN, ge); ok = all(abs(k1[p]["Z"] / v - 1) <= 1e-5 for p, v in AZ12[foot].items()); fail += not ok
        P(f"[{foot}] K1 AZ12 kernel reproduces Saturn {k1['Saturn']['Z']:.6f} (AZ12 {AZ12[foot]['Saturn']:.6f}), Mars {k1['Mars']['Z']:.6f} ({AZ12[foot]['Mars']:.6f}): {'PASS' if ok else 'FAIL'}")
    RES[foot] = {}
    for c in ("TID", "LOC", "HALF"):
        g = grade(c, a0, etaN, ge); gc = grade(c, a0, etaN, ge, orders=(128, 80)); worst = max(g, key=lambda p: g[p]["Z"])
        k3 = max(abs(g[p]["Z"] - gc[p]["Z"]) for p in g); ok3 = MUT or k3 <= 1e-5; fail += not ok3
        msg = ""
        if c != "HALF" and not MUT:
            g2 = grade(c, a0, etaN, ge, n=40000); k5 = abs(g2["Saturn"]["Z"] / g["Saturn"]["Z"] - 1); ok5 = k5 <= 0.01; fail += not ok5
            xs = xi_table(c, etaN)(np.array([9.58 * AU / math.sqrt(GM / a0)]))[0]; msg = f"; xi at Saturn {xs:.4g} r_M; K5 grid x2 Saturn change {k5:.2e} {'PASS' if ok5 else 'FAIL'}"
        bad = [p for p in g if g[p]["Z"] > 2]; lab = f"{c} PASSES PLANETS" if not bad else f"{c} FAILS PLANETS: " + ", ".join(bad)
        RES[foot][c] = dict(rows=g, worst=worst, label=lab, K3=k3)
        P(f"[{foot}] {c}: worst {worst} Z {g[worst]['Z']:.4g} (EPM {g[worst]['Z_EPM']:.3g}, INPOP {g[worst]['Z_INPOP']:.3g}); Saturn {g['Saturn']['Z']:.4g}, Mars {g['Mars']['Z']:.4g}; K3 {k3:.1e} {'PASS' if ok3 else 'FAIL'}{msg}")
        P(f"LABEL [{foot}] {lab}")
cz2 = json.load(open(os.path.join(HERE, "..", "CZ2_filter_regrade_newtonian_efe", "cz2.json")))
P("\nJoined with CZ2:")
for foot in A0SI:
    for c in ("TID", "LOC"):
        s2 = cz2[f"label|{foot}|{c}"]["label"]; ok = s2.endswith("SURVIVES") and RES[foot][c]["label"].endswith("PASSES PLANETS")
        P(f"  [{foot}] {c}: CZ2 {s2}; CZ3 {RES[foot][c]['label']}" + (f"  ->  {c} SURVIVES FIVE ON {foot.upper()}" if ok else ""))
if MUT:
    w = {f: max(RES[f][c]["rows"][RES[f][c]["worst"]]["Z"] for c in RES[f]) for f in RES}; P(f"MUTATE bite (worst Z > 10 both footings): {w} -> {'BITES' if min(w.values()) > 10 else 'DOES NOT BITE'}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["peak_rss_GB"] = rss; RES["fail"] = fail
P(f"\npeak RSS {rss:.2f} GB; failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"cz3{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cz3{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
