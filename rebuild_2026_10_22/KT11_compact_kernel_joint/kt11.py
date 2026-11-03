#!/usr/bin/env python3
"""KT11: compact p = 1 kernel, one global stellar scale, SPARC + Cassini + trend. See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../../real_research/data/sparc_data")
MUT = os.environ.get("KT11_MUTATE") == "1"
KPC = 3.0857e19
RAW = []
for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
    R, V, e, Vg, Vd, Vb = (d[:, j] for j in range(6))
    m = (R > 0) & (V > 0) & (e > 0) & (e / V < .1)
    if m.sum() < 3: continue
    RAW.append(dict(R=R[m] * KPC, go=V[m] ** 2 * 1e6 / (R[m] * KPC), G2=Vg[m] * abs(Vg[m]), D2=Vd[m] * abs(Vd[m]), B2=Vb[m] * abs(Vb[m]), bulge=bool(np.any(Vb != 0))))
mu_p1 = lambda Y: np.where(Y <= 1, 2 * Y - Y * Y, 1.0)
mu_or2 = lambda Y: 1 - (1 + Y) ** -2.0
def pred(gb, s, mu):
    lo, hi = gb.copy(), gb * 10 + np.sqrt(gb * s) * 10 + 1e-13
    for _ in range(70):
        mid = .5 * (lo + hi); f = mid * mu(mid / s) - gb
        lo, hi = np.where(f < 0, mid, lo), np.where(f < 0, hi, mid)
    return .5 * (lo + hi)
def per_gal(s, mu, f, fb=None, gobs=None):
    out = []
    for i, g in enumerate(RAW):
        B = g["G2"] + .5 * f * g["D2"] + .7 * (f if fb is None else fb) * g["B2"]
        k = B > 0
        if k.sum() < 3: out.append(None); continue
        gb = B[k] * 1e6 / g["R"][k]
        go = (g["go"] if gobs is None else gobs[i])[k]
        out.append((np.log10(gb) + 10.5, np.log10(go) - np.log10(pred(gb, s, mu))))
    return out
def stat(pg, w=None):
    ms = np.array([np.mean(r**2) if p is not None else np.nan for p in pg for r in [p[1] if p is not None else None]])
    ok = ~np.isnan(ms)
    w = np.ones(len(pg)) if w is None else w
    rms = math.sqrt(np.sum((ms * w)[ok]) / np.sum(w[ok]))
    med = float(np.median(np.concatenate([p[1] for p in pg if p is not None])))
    return rms, med, ms
FG = np.round(np.arange(.5, 2.0001, .01), 3)
def fit_f(s, mu, fb=None, gobs=None):
    tab = np.array([stat(per_gal(s, mu, f, None if fb is None else fb, gobs))[2] for f in FG])  # F x Ngal
    return tab
def best_f(tab, w=None):
    w = np.ones(tab.shape[1]) if w is None else w
    ok = ~np.isnan(tab[0])
    M = (tab[:, ok] * w[ok]).sum(1) / w[ok].sum()
    return FG[np.argmin(M)], math.sqrt(M.min())
def boot_f(tab, nd=2000):
    rng = np.random.default_rng(20261102); n = tab.shape[1]
    return np.array([best_f(tab, np.bincount(rng.integers(0, n, n), minlength=n).astype(float))[0] for _ in range(nd)])
def t2(pg, idx):
    n = d = 0.
    for i in idx:
        p = pg[i]
        if p is None: continue
        x, r = p; xx, rr = x - x.mean(), r - r.mean(); n += (xx * rr).sum(); d += (xx * xx).sum()
    return n / d
def t2ci(pg, sel):
    idx0 = [i for i in range(len(pg)) if sel(i)]
    rng = np.random.default_rng(20261102)
    B = [t2(pg, rng.choice(idx0, len(idx0))) for _ in range(2000)]
    return round(t2(pg, idx0), 4), [round(float(np.percentile(B, 2.5)), 4), round(float(np.percentile(B, 97.5)), 4)]
# Cassini, explicit-corner integrator from argon_p1_recheck.py
GM = 6.6743e-11 * 1.98892e30
def nu_p1(y):
    y = np.asarray(y, float); out = np.ones_like(y)
    for i, yy in np.ndenumerate(y):
        if yy < 2: out[i] = brentq(lambda x: x * x - x**3 / 4 - yy, 0, 2) / yy
    return out
def nu_exp(y):
    y = np.asarray(y, float); out = np.ones_like(y)
    for i, yy in np.ndenumerate(y):
        if yy < 40: out[i] = brentq(lambda x: x * (-math.expm1(-x)) - yy, 1e-12, yy + 50) / yy
    return out
def Q(nu, eN, cut, nv=1200, nm=500, vmax=None):
    vs = np.linspace(1e-4, vmax or math.sqrt(eN + cut) * 1.0001, nv); tot = np.zeros(nv)
    x, w = np.polynomial.legendre.leggauss(nm)
    for i, v in enumerate(vs):
        hi = min((cut**2 - eN**2 - v**4) / (2 * eN * v * v), 1.0)
        if hi <= -1: continue
        mu = -1 + (x + 1) * (hi + 1) / 2
        Dd = np.sqrt(np.maximum(eN**2 + v**4 + 2 * eN * v * v * mu, 1e-30))
        tot[i] = np.sum(w * (nu(Dd) - 1) * (eN * (3 * mu - 5 * mu**3) + v * v * (1 - 3 * mu * mu))) * (hi + 1) / 2
    return abs(1.5 * np.trapz(tot, vs))
def cassini(a0, nu, cut, vmax=None, nv=1200, nm=500):
    et = 2.32e-10 / a0; qp = 5.2e-27 / (1.5 * a0**1.5 / math.sqrt(GM))
    eN = brentq(lambda x: x * float(nu(np.array([x]))[0]) - et, 1e-6, 1e4)
    return Q(nu, eN, cut, nv, nm, vmax) / qp
c, Gv = 2.99792458e8, 6.674e-11
rc = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * Gv)
S = {"rho_DE": c * math.sqrt(Gv * .685 * rc), "rho_crit": c * math.sqrt(Gv * rc)}
A0 = {"rho_DE": 9.3619e-11, "rho_crit": 1.1279e-10}
if MUT:
    print("MUTATE Cassini exponential canonical:", round(cassini(A0["rho_DE"], nu_exp, 40.0, 7.0, 800, 120), 3), "x (expect 3.76, must fail)")
    rng = np.random.default_rng(5)
    sh = [rng.permutation(g["go"]) for g in RAW]
    sh_all = np.concatenate(sh); rng.shuffle(sh_all); cuts = np.cumsum([0] + [len(g["go"]) for g in RAW])
    sh = [sh_all[cuts[i]:cuts[i + 1]] for i in range(len(RAW))]
    print("MUTATE SPARC shuffled rms:", round(stat(per_gal(S["rho_DE"], mu_p1, 1.0, gobs=sh))[0], 4), "(must exceed 0.3)")
    sys.exit(1)
out = {}
# planted
s0 = S["rho_DE"]
pg1 = per_gal(s0, mu_p1, 1.2)
mock = []
for i, g in enumerate(RAW):
    B = g["G2"] + .6 * g["D2"] + .84 * g["B2"]
    gb = np.maximum(B, 1e-6) * 1e6 / g["R"]
    sc = np.zeros(len(gb))
    if pg1[i] is not None:
        k = (g["G2"] + .6 * g["D2"] + .84 * g["B2"]) > 0
        sc[k] = np.random.default_rng(i).permutation(pg1[i][1] - pg1[i][1].mean())
    mock.append(pred(gb, s0, mu_p1) * 10**sc)
fpl = best_f(fit_f(s0, mu_p1, gobs=mock))[0]
okp = abs(fpl - 1.2) <= .05
print(f"PLANTED f = 1.2 recovered {fpl}: {'PASS' if okp else 'FAIL'}"); out["planted"] = [float(fpl), bool(okp)]
ce = cassini(A0["rho_DE"], nu_exp, 40.0, 7.0, 800, 120)
print(f"Cassini control exponential {ce:.3f}x (3.76 expected): {'PASS' if abs(ce-3.76) <= .05 else 'FAIL'}")
for fn, s in S.items():
    tab = fit_f(s, mu_p1); f, rms = best_f(tab); bf = boot_f(tab)
    f95 = [float(np.percentile(bf, 2.5)), float(np.percentile(bf, 97.5))]
    pg = per_gal(s, mu_p1, f); r_, med, _ = stat(pg)
    ref = stat(per_gal(s, mu_or2, 1.0))
    tabo = fit_f(s, mu_or2); fo, rmso = best_f(tabo)
    a2, ci2 = t2ci(pg, lambda i: True); b2, cb2 = t2ci(pg, lambda i: not RAW[i]["bulge"])
    cq = cassini(A0[fn], nu_p1, 2.0)
    tabb = fit_f(s, mu_p1, fb=1.0); fd, _ = best_f(tabb)
    G1 = .79 <= f <= 1.26; G2 = r_ <= ref[0] + .005 and abs(med) <= .05; G3 = cq < 1; G4 = cb2[0] <= 0 <= cb2[1]
    print(f"\n== {fn}\n f {f} [{f95[0]}, {f95[1]}] (disc {0.5*f:.3f}, bulge {0.7*f:.3f}); G1 {'PASS' if G1 else 'FAIL'}")
    print(f" rms {r_:.4f}, median {med:+.4f}; OR mu_2 at f=1 rms {ref[0]:.4f} med {ref[1]:+.4f}; G2 {'PASS' if G2 else 'FAIL'}")
    print(f" OR mu_2 own best f {fo} rms {rmso:.4f}")
    print(f" Cassini {cq:.3f}x; G3 {'PASS' if G3 else 'FAIL'}")
    print(f" T2 all {a2} {ci2}; bulgeless {b2} {cb2}; G4 {'PASS' if G4 else 'FAIL'}")
    print(f" G5: disc f with bulge 0.7 fixed: {fd} (disc {0.5*fd:.3f}); bulge at best f {0.7*f:.3f} vs Sani median 0.862")
    gates = {"G1": G1, "G2": G2, "G3": G3, "G4": G4}
    lab = "JOINT PASS" if all(gates.values()) else "FAILS " + ", ".join(k for k, v in gates.items() if not v)
    print(" LABEL", lab)
    out[fn] = dict(f=float(f), f95=f95, rms=r_, med=med, or2=ref[:2], or2_best=[float(fo), rmso], cassini=cq, t2=[a2, ci2], t2_bulgeless=[b2, cb2], fdisc=float(fd), label=lab)
json.dump(out, open(os.path.join(HERE, "kt11.json"), "w"), indent=1)
