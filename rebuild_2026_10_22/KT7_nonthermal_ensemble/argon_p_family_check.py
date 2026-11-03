#!/usr/bin/env python3
"""Grade Argon's second reply: u' = chi^p (1-chi)^2 and chi ln^2 chi on KT5's Cassini integral and SPARC gate. a0 = s/2, so x = g/a0 = 2Y."""
import glob, math, os
import numpy as np
from scipy import integrate
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "../../real_research/data/sparc_data")
def chi_p(Y, p):
    if Y <= 0: return 1.0
    if p == 1: return max(1 - Y, 0.0)
    return brentq(lambda c: c ** ((p - 1) / 2) * (1 - c) - Y, 1e-300, 1 - 1e-15, xtol=1e-300, rtol=1e-13)
kern = {"p=-1 form a": lambda Y: 1 - chi_p(Y, -1) ** 2, "p=0 form b": lambda Y: 1 - chi_p(Y, 0) ** 2, "p=0.5": lambda Y: 1 - chi_p(Y, .5) ** 2,
        "p=1 polynomial": lambda Y: 1 - chi_p(Y, 1) ** 2, "exponential chi=exp(-Y)": lambda Y: -math.expm1(-2 * Y)}
GM = 6.6743e-11 * 1.98892e30
GEXT, CEIL = 2.32e-10, 5.2e-27
PREF = lambda a0: 1.5 * a0**1.5 / math.sqrt(GM)
def nu_of(mux):
    return lambda y: brentq(lambda x: x * mux(x) - y, 1e-12, y + 50.0, xtol=1e-13) / y
def q(nu, et, vmax=400.0):
    eN = brentq(lambda x: x * nu(x) - et, 1e-9, 1e6, xtol=1e-12)
    def ig(mu, v):
        D = eN * eN + v**4 + 2 * eN * v * v * mu
        if D <= 0: return 0.0
        return (nu(math.sqrt(D)) - 1) * (eN * (3 * mu - 5 * mu**3) + v * v * (1 - 3 * mu * mu))
    return abs(1.5 * integrate.dblquad(ig, 0, vmax, lambda v: -1, lambda v: 1, epsabs=1e-6, epsrel=1e-4)[0])
gb, go, gal, i = [], [], [], 0
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6))
    m = (R > 0) & (Vo > 0) & (eV > 0) & (eV / Vo < .1)
    if m.sum() < 3: continue
    R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
    B = Vg * abs(Vg) + .5 * Vd * abs(Vd) + .7 * Vb * abs(Vb)
    k = B > 0
    if k.sum() < 3: continue
    r = R[k] * 3.0857e19
    gb.append(B[k] * 1e6 / r); go.append(Vo[k] ** 2 * 1e6 / r); gal.append(np.full(k.sum(), i)); i += 1
gb, go, gal = map(np.concatenate, (gb, go, gal))
c, G = 2.99792458e8, 6.674e-11
rc = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
S = {"rho_DE": c * math.sqrt(G * .685 * rc), "rho_crit": c * math.sqrt(G * rc)}
def stat(s, mu):
    pr = np.array([brentq(lambda g: g * mu(g / s) - b, b * .999, b * 10 + math.sqrt(b * s) * 10) for b in gb])
    r = np.log10(go) - np.log10(pr)
    return math.sqrt((np.bincount(gal, r**2) / np.bincount(gal)).mean()), float(np.median(r))
a0 = 9.3619e-11
et, qp = GEXT / a0, CEIL / PREF(a0)
print(f"eta {et:.3f} Q_PASS {qp:.4f}; g_e/s at 1.9e-10 = {1.9e-10/(2*a0):.3f} (Argon 0.79)")
ref = {f: stat(s, kern["p=-1 form a"]) for f, s in S.items()}
for nm, mu in kern.items():
    qv = q(nu_of(lambda x, mu=mu: mu(x / 2)), et)
    st = {f: stat(s, mu) for f, s in S.items()}
    gate = {f: st[f][0] <= ref[f][0] + .005 and abs(st[f][1]) <= .05 for f in S}
    print(f"{nm}: Cassini {qv/qp:.2f} x ceiling (Q2 {qv/qp*CEIL:.2e}) {'PASS' if qv < qp else 'FAIL'}; SPARC rho_DE rms {st['rho_DE'][0]:.4f} med {st['rho_DE'][1]:+.4f} {'PASS' if gate['rho_DE'] else 'FAIL'}; rho_crit rms {st['rho_crit'][0]:.4f} med {st['rho_crit'][1]:+.4f} {'PASS' if gate['rho_crit'] else 'FAIL'}", flush=True)
