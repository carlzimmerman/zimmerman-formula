#!/usr/bin/env python3
"""UX3 shared loaders. BF1's rows, with extra columns, read only. kappa = 1/2 FITTED; not theory closed."""
import math, os, pickle
import numpy as np
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
A0S = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); C = 299792458.0; G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; KMS2 = 1e6
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
PI2 = math.pi ** 2
BMEM = {"sqrt(.5)(1+f)": lambda f: math.sqrt(.5) * (1 + f), "sqrt(pi)-1/(1+f)": lambda f: math.sqrt(math.pi) - 1 / (1 + f), "1.5/(2-f)": lambda f: 1.5 / (2 - f)}
BF1LINE = {"sqrt(.5)(1+f)": (.030, .096, .235, -.012, .073, .222), "sqrt(pi)-1/(1+f)": (.043, .099, .229, .002, .069, .218), "1.5/(2-f)": (.028, .098, .227, -.014, .077, .217)}
def sparc():
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]; meta = {g["name"]: g for g in Q}; names = sorted(meta); out = {0: [], 1: []}; D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod")
    for i, n in enumerate(names):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30: continue
        t = np.atleast_2d(np.loadtxt(os.path.join(D, n + "_rotmod.dat"), comments="#")); Rl = t[:, 0].max(); vf = float(meta[n]["vf"]) if meta[n]["vf"] is not None else 0.0; vf = vf if np.isfinite(vf) else 0.0
        Mg = np.maximum(np.abs(t[:, 3]) * t[:, 3], 1e-9) * t[:, 0]; sl = np.gradient(np.log(Mg), np.log(t[:, 0])) if len(t) > 1 else np.ones(1)
        for k, (r, v, e, vg, vd, vb, *_) in enumerate(t):
            m = abs(vg) * vg + 0.5 * abs(vd) * vd + 0.7 * abs(vb) * vb; R = r * 1e3 * PC
            if r <= 0 or v <= 0 or m <= 0: continue
            out[i % 2].append((m * KMS2 / R, v * v * KMS2 / R, R, min(1.0, max(0.0, abs(vg) * vg / m)), i, v, r / Rl, vf, sl[k]))
    return {k: np.array(v) for k, v in out.items()}
def xcop(xs=(0.1, 0.2, 0.3, 0.5, 0.7)):
    D = os.path.join(REPO, "real_research", "data", "xcop"); out = []; nm = []
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for j, n in enumerate(sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))):
        nm.append(n)
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        for x in xs:
            r = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(ga["RADIUS"] * rg, ga["MGAS"], r); ms = li(st["RADIUS"], st[st.names[1]], r)
            if not np.all(np.isfinite([mh, mg, ms])): continue
            R = r * 1e3 * PC; f = 1 / R ** 2 * G * MS; mgb = li(ga["RADIUS"] * rg, ga["MGAS"], r * 1.05); mga = li(ga["RADIUS"] * rg, ga["MGAS"], r / 1.05)
            out.append((f * (mg + ms), f * mh, R, mg / (mg + ms), j, 0.0, x, 0.0, math.log(mgb / mga) / (2 * math.log(1.05))))
    return np.array(out), nm
def apply(A, a0, Hfn):
    y = A[:, 0] / a0; f = A[:, 3]; return law(A[:, 0], a0) * Hfn(y, f, A)
def resid(A, a0, Hfn): return np.log10(A[:, 1] / apply(A, a0, Hfn))
def st(d): return float(d.mean()), float(np.sqrt((d * d).mean())), float(np.median(d))
def H1(k, theta): return lambda y, f, A: 1 + theta(A) * k * y * f
def theta_c1(sig, p=1.0):
    def th(A):
        V = A[:, 5]; t = sig ** 2 / (sig ** 2 + V ** 2); return t ** p
    return th
