#!/usr/bin/env python3
"""UX7 shared: UX3's X-COP rows (read only), forms on X-COP, form fits on X-COP train. Every form FITTED. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
sys.path.insert(0, os.path.join(RB, "UX3_cluster_gas_term"))
from ux3_common import xcop, law, A0S, G, MS, PC, st
import numpy as np
from astropy.io import fits
from scipy.optimize import minimize_scalar
FORMS = ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]; RIV = ["R1", "R2"]
def xcop_full():
    X, nm = xcop(); D = os.path.join(REPO, "real_research", "data", "xcop"); M5 = {}; Mg5 = {}
    for j, n in enumerate(nm):
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: M5[j] = float(h[1].header["M500"]) * 1e14; r5 = float(h[1].header["R500"])
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        Mg5[j] = float(10 ** np.interp(np.log10(r5), np.log10(ga["RADIUS"] * rg), np.log10(ga["MGAS"])))
    j = X[:, 4].astype(int); return X, nm, np.array([M5[q] for q in j]), np.array([Mg5[q] for q in j])
def model(A, M5, Mg5, a0, form, k, pqt=None):
    gb = A[:, 0]; R = A[:, 2]; f = A[:, 3]; S = np.maximum(A[:, 8], 0.0); u = A[:, 6]; gg = gb * f; x = gg / a0; L = law(gb, a0); Mg = gg * R * R / (G * MS); s = Mg / Mg5; gM = G * MS * M5 * s / R ** 2
    if form == "F0": return L * (1 + k * x)
    if form == "F1": return L * (1 + k * x * S)
    if form == "F2": return L * (1 + k * x / (1 + x))
    if form == "F3": return L * (1 + k * gb / a0)
    if form == "F4": return law(gb, a0 * (1 + k * x))
    if form == "F5": return L + k * gg
    if form == "F6": return L * (1 + k * x * x)
    if form == "F7": return L + k * S * gg
    if form == "F8": return L * (1 + k * x * np.exp(-u))
    if form == "R1": return L * (1 + k * gM / a0)
    if form == "R2": return L + k * gM
    if form == "P": p, q, t = pqt; return L * (1 + k * x ** p * u ** q * S ** t)
    raise KeyError(form)
def resid(A, M5, Mg5, a0, form, k, pqt=None): return np.log10(A[:, 1] / model(A, M5, Mg5, a0, form, k, pqt))
def fit(A, M5, Mg5, a0, form, pqt=None, lo=-5.0, hi=7.0):
    c = lambda lk: float((resid(A, M5, Mg5, a0, form, 10 ** lk, pqt) ** 2).sum()); g = np.linspace(lo, hi, 481); v = [c(q) for q in g]; i = int(np.argmin(v)); a, b = g[max(i - 1, 0)], g[min(i + 1, 480)]; r = minimize_scalar(c, bounds=(a, b), method="bounded", options=dict(xatol=1e-9)); return float(10 ** r.x), bool(i == 0 or i == 480)
def controls():
    rg = np.random.default_rng(20261102); return [(float(a), float(b), float(c)) for a, b, c in zip(rg.uniform(.5, 2.5, 40), rg.uniform(-2, 1, 40), rg.uniform(0, 2, 40))]
