#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f28 -- the one-argument pincer: is there ANY member of the mu_n family that is both Cassini-safe and galaxy-tolerated?

The closure handoff (RESUME_HERE.md, 2026-08-20) established that which field carries the halo cannot move the
Solar-System EFE quadrupole -- "only the interpolation function can".  f23/f24 put the framework's own kernel at
6-9x the Park 2026 ceiling; f25 showed mu_5 and mu_10 lose to it on SPARC with a_0 and the disc M/L free.  This file
closes the gap between those two by scanning the standard one-argument family mu_n(x) = x/(1+x^n)^{1/n}, n = 1..10,
on BOTH axes with the SAME machinery:

    Cassini axis : Q_2 = (3/2) q a_0^{3/2}/sqrt(GM_sun), q from the committed DHF eq. 10 integral (f23 section 6),
                   at the solar-circle field g_ext = 2.32e-10, both footings, against the 5.2e-27 s^-2 ceiling.
    galaxy axis  : the lead's paired-galaxy resampling with a_0 AND a global disc M/L profiled per kernel (f25),
                   equal-galaxy MSE against nu_RAR; a kernel is 'tolerated' if the 95% interval of MSE(mu_n) - MSE(RAR)
                   contains zero, 'rejected' if it loses in >= 99% of resamples.

If some n is Cassini-safe on at least one footing AND galaxy-tolerated, the one-argument class has a survivor and the
length-scale conclusion of the addendum is wrong.  If none is, no local static law mu(g/a_0) survives both, on this
family.  Scope: the mu_n family spans the transition-sharpness axis DHF identify as the only lever on Q_2; it is not
every conceivable one-argument function, and the checks say so.
"""
import os, sys, math
import numpy as np
from scipy import integrate
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(28)
GM_SUN = 6.6743e-11*1.98892e30; GEXT = 2.32e-10; Q2_CEIL = 5.2e-27
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)
NS = [1, 2, 3, 4, 5, 7, 10]

# ---- kernels as nu(y) tables (spherical inverse partners)
YG = np.logspace(-7, 7, 2801); lyg = np.log(YG)
def nu_table(mu):
    out = np.empty_like(YG)
    for i, yy in enumerate(YG):
        out[i] = brentq(lambda x: x*mu(x) - yy, 1e-14, yy + 60.0, xtol=1e-14)/yy if yy < 300 else 1.0
    return out
def mk(tab): return lambda y: np.exp(np.interp(np.log(np.clip(np.asarray(y, float), 1e-7, 1e7)), lyg, tab))
NU = {"nu_rar": lambda y: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-30))))}
for n in NS: NU[f"mu_{n}"] = mk(np.log(nu_table(lambda x, n=n: x/(1 + x**n)**(1.0/n))))

# ---- Cassini axis
def solve_eN(nu, et): return brentq(lambda e: float(np.asarray(nu(e)).ravel()[0])*e - et, 1e-9, et*1.5, xtol=1e-14)
def q_direct2D(nu, et, vmax=400.0):
    eN = solve_eN(nu, et)
    def ig(mu, v):
        D = eN*eN + v**4 + 2.0*eN*v*v*mu
        if D <= 0: return 0.0
        nv = float(np.asarray(nu(math.sqrt(D))).ravel()[0])
        return (nv - 1.0)*(eN*(3*mu - 5*mu**3) + v*v*(1 - 3*mu*mu))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-12, epsrel=1e-10)
    return abs(1.5*val)
P("=" * 118); P("f28 -- the one-argument pincer on the mu_n family"); P("=" * 118)
P("\n1.  Cassini axis: Q_2 / ceiling at the solar-circle external field (QUMOND integral; exact AQUAL is 8-30% higher, f24)")
CAS = {}
for k in NU:
    CAS[k] = {f: q_direct2D(NU[k], GEXT/a0)*PREF(a0)/Q2_CEIL for f, a0 in A0.items()}
    info(f"{k:7s}: Q2/ceiling canonical {CAS[k]['canonical']:.3f}, alt {CAS[k]['alt']:.3f}")
ck("C1 anchors reproduce: the framework's kernel at 6.2x/6.8x (f23), mu_10 under 0.2x",
   abs(CAS["nu_rar"]["canonical"] - 6.23) < 0.1 and abs(CAS["nu_rar"]["alt"] - 6.83) < 0.1 and CAS["mu_10"]["canonical"] < 0.2,
   f"RAR {CAS['nu_rar']['canonical']:.2f}/{CAS['nu_rar']['alt']:.2f}, mu_10 {CAS['mu_10']['canonical']:.3f}")
safe = {k: any(v < 1.0 for v in CAS[k].values()) for k in NU}
n_c = min((n for n in NS if safe[f"mu_{n}"]), default=None)
info(f"Cassini-safe members (Q2 < ceiling on at least one footing, QUMOND): {[k for k in NU if safe[k]]}; the boundary is n_c = {n_c}")

# ---- galaxy axis (f25's design)
P("\n2.  galaxy axis: a_0 and a global disc M/L profiled per kernel, paired galaxy resampling against nu_RAR")
gals0 = load_sparc()
UPS = np.array([0.30, 0.40, 0.50, 0.60, 0.70, 0.80]); LOGA = np.linspace(-10.8, -9.2, 161)
gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gals0)])
vg = np.concatenate([g["vg"] for g in gals0]); vd = np.concatenate([g["vd"] for g in gals0]); vb = np.concatenate([g["vb"] for g in gals0]); rr = np.concatenate([g["r"] for g in gals0])
go = np.concatenate([g["vobs"]**2/g["r"] for g in gals0])*KMS2_KPC
def gbar_of(ups): return (vg*np.abs(vg) + ups*vd**2 + 1.4*ups*vb**2)/rr*KMS2_KPC
names, ids = np.unique(gid, return_inverse=True); NG = len(names)
def loss_cube(kernel):
    L = np.full((NG, len(UPS), len(LOGA)), np.nan)
    for iu, ups in enumerate(UPS):
        gb = gbar_of(ups); ok = (gb > 0) & (go > 0); cnt = np.maximum(np.bincount(ids[ok], minlength=NG), 1)
        for ia, la in enumerate(LOGA):
            res = np.log10(go[ok]/(NU[kernel](gb[ok]/10**la)*gb[ok]))
            L[:, iu, ia] = np.bincount(ids[ok], weights=res**2, minlength=NG)/cnt
    return L
def profiled(L, W):
    m = np.tensordot(W, L, axes=(1, 0)); flat = m.reshape(len(W), -1); j = np.argmin(flat, axis=1)
    return flat[np.arange(len(W)), j], np.unravel_index(j, m.shape[1:])
W0 = np.full((1, NG), 1.0/NG); W = rng.multinomial(NG, np.full(NG, 1.0/NG), size=999)/NG
GAL = {}
Lr = loss_cube("nu_rar"); fr, (iu, ia) = profiled(Lr, W0); br, _ = profiled(Lr, W)
GAL["nu_rar"] = dict(rms=math.sqrt(float(fr[0])), ups=float(UPS[iu[0]]), a0=float(10**LOGA[ia[0]]))
info(f"nu_rar : RMS {GAL['nu_rar']['rms']:.4f} dex at (Upsilon, a_0) = ({GAL['nu_rar']['ups']:.2f}, {GAL['nu_rar']['a0']:.2e})")
for n in NS:
    k = f"mu_{n}"; L = loss_cube(k); f_, (iu, ia) = profiled(L, W0); b_, _ = profiled(L, W)
    d = b_ - br; pc = np.percentile(d, [2.5, 50, 97.5]); frac = float(np.mean(d > 0))
    GAL[k] = dict(rms=math.sqrt(float(f_[0])), ups=float(UPS[iu[0]]), a0=float(10**LOGA[ia[0]]), pc=pc, frac=frac,
                  verdict="tolerated" if pc[0] < 0 < pc[2] else ("rejected" if frac >= 0.99 else "disfavoured"))
    info(f"{k:7s}: RMS {GAL[k]['rms']:.4f} at ({GAL[k]['ups']:.2f}, {GAL[k]['a0']:.2e}); paired dMSE [{pc[0]:+.5f}, {pc[1]:+.5f}, {pc[2]:+.5f}], worse in {frac:.3f} -> {GAL[k]['verdict']}")

# ---- the pincer
P("\n3.  the pincer")
P(f"    {'kernel':7s} {'Q2/ceil can':>11s} {'Q2/ceil alt':>11s} {'Cassini':>8s} {'galaxy RMS':>10s} {'worse frac':>10s} {'galaxy':>10s}")
for k in NU:
    g_ = GAL[k]; v = g_.get("verdict", "reference")
    P(f"    {k:7s} {CAS[k]['canonical']:11.3f} {CAS[k]['alt']:11.3f} {'safe' if safe[k] else 'FAIL':>8s} {g_['rms']:10.4f} {g_.get('frac', float('nan')):10.3f} {v:>10s}")
survivors = [k for k in NU if k != "nu_rar" and safe[k] and GAL[k]["verdict"] == "tolerated"]
ck("P1 (THE PINCER, and it can fail) no member of the mu_n family, n = 1..10, is both Cassini-safe and galaxy-tolerated: "
   "every Cassini-safe member is rejected on SPARC with a_0 and the disc M/L free, and every galaxy-tolerated member "
   "fails Cassini.  If this FAILS the one-argument class has a survivor and the length-scale argument is wrong",
   len(survivors) == 0, f"survivors: {survivors}; Cassini-safe: {[k for k in NU if safe[k]]}; tolerated: {[k for k in NU if GAL[k].get('verdict') == 'tolerated']}")
ck("P2 the boundary is sharp on both sides: the softest Cassini-safe member is rejected on galaxies in >= 99% of "
   "resamples, and the sharpest galaxy-tolerated member exceeds the ceiling by more than 2x on both footings",
   n_c is not None and GAL[f"mu_{n_c}"]["frac"] >= 0.99 and all(min(CAS[k].values()) > 2.0 for k in NU if GAL[k].get("verdict") == "tolerated"),
   f"n_c = {n_c}: worse in {GAL[f'mu_{n_c}']['frac'] if n_c else float('nan'):.3f}; tolerated members' min Q2/ceiling = "
   + ", ".join(f"{k} {min(CAS[k].values()):.2f}" for k in NU if GAL[k].get("verdict") == "tolerated"))
ck("P3 mutation: the galaxy axis has sensitivity to sharpness in the right direction -- the profiled RMS rises "
   "monotonically with n from n = 2 upward", all(GAL[f"mu_{a}"]["rms"] <= GAL[f"mu_{b}"]["rms"] + 1e-4 for a, b in zip(NS[1:-1], NS[2:])),
   ", ".join(f"n={n}: {GAL[f'mu_{n}']['rms']:.4f}" for n in NS))
P("\n  scope: QUMOND quadrupole (AQUAL is 8-30% higher, f24, which only widens the Cassini side); descriptive galaxy MSE")
P("  with catalogue distances and inclinations; the mu_n family is the standard sharpness axis, not every one-argument law.")
sys.exit(ck.done())
