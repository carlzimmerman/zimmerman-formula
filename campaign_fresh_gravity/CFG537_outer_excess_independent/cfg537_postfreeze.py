#!/usr/bin/env python3
"""CFG537 POST-FREEZE verification (added 2026-10-09 after the frozen runs; NO verdict weight).
Why: the frozen matched() statistic estimates each bin's variance from the class samples; with 2-5 galaxies per class a bin can get a
spuriously tiny variance (WALLABY S4 T<=2 gave Z -4.2 from one bin with two early galaxies 0.003 dex apart), and the MU1 shuffle null
has sd 1.2-1.3 rather than 1. So every headline Z is re-expressed three ways, for SPARC (CFG534, fixed and B1 free M/L) and WALLABY:
  p_shuffle  fraction of 4000 within-bin label shuffles with Z >= observed (one-sided; calibrates the nominal Z)
  Z_pooled   same bins/means, but one pooled within-bin variance per bin (both classes) instead of per-class variances
  sig_boot   galaxy bootstrap (resampling within class within bin, 2000x) of the matched difference
plus SPARC - WALLABY difference of Delta_out.  Reads the frozen results JSONs; recomputes SPARC rows with CFG534's code.
Run: nice -n 10 python3 cfg537_postfreeze.py > cfg537_postfreeze.out
"""
import os, json, math
import numpy as np
from scipy.stats import norm

try:
    os.nice(10)
except OSError:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
CONV = 3.0857e19 / 1e6
EDG = np.arange(7.0, 12.2 + 1e-9, 0.4)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def wmean(r, w, m):
    m = m & np.isfinite(r)
    return float((r[m] * w[m]).sum() / w[m].sum()) if m.sum() >= 2 else np.nan


def bins_of(x, lm, early):
    out = []
    for lo, hi in zip(EDG[:-1], EDG[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        a, b = x[m & early], x[m & ~early]
        if len(a) >= 2 and len(b) >= 2:
            out.append((a, b))
    return out


def stat(x, lm, early, pooled=False):
    num = den = 0.0
    for a, b in bins_of(x, lm, early):
        if pooled:
            s2 = (a.var(ddof=1) * (len(a) - 1) + b.var(ddof=1) * (len(b) - 1)) / (len(a) + len(b) - 2)
            v = s2 / len(a) + s2 / len(b)
        else:
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
        num += (a.mean() - b.mean()) / v; den += 1 / v
    return (num / den, den ** -0.5, num / den ** 0.5) if den else (np.nan, np.nan, np.nan)


def analyse(name, x, lm, T, cut=3, seed=537):
    x, lm, T = np.asarray(x, float), np.asarray(lm, float), np.asarray(T, float)
    early = T <= cut
    d, s, Z = stat(x, lm, early)
    dp, sp, Zp = stat(x, lm, early, pooled=True)
    rng = np.random.default_rng(seed)
    zs = []
    for _ in range(4000):
        Ts = T.copy()
        for lo, hi in zip(EDG[:-1], EDG[1:]):
            idx = np.where((lm >= lo) & (lm < hi))[0]
            Ts[idx] = rng.permutation(Ts[idx])
        zs.append(stat(x, lm, Ts <= cut)[2])
    zs = np.array(zs); zs = zs[np.isfinite(zs)]
    p_sh = float((zs >= Z).mean()) if Z >= 0 else float((zs <= Z).mean())
    # bootstrap within class within bin
    bd = []
    bl = bins_of(x, lm, early)
    for _ in range(2000):
        num = den = 0.0
        for a, b in bl:
            aa, bb = rng.choice(a, len(a)), rng.choice(b, len(b))
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)     # weights fixed at the observed ones
            num += (aa.mean() - bb.mean()) / v; den += 1 / v
        bd.append(num / den)
    sb = float(np.std(bd, ddof=1))
    r = dict(diff=d, sig=s, Z=Z, null_mean=float(zs.mean()), null_sd=float(zs.std()), p_shuffle=p_sh,
             Z_equiv_shuffle=float(norm.isf(p_sh)) * (1 if Z >= 0 else -1) if 0 < p_sh < 1 else None,
             diff_pooled=dp, sig_pooled=sp, Z_pooled=Zp, sig_boot=sb, Z_boot=d / sb)
    ze = r["Z_equiv_shuffle"]
    zes = "" if ze is None else f" (Z-equiv {ze:+.2f})"
    P(f"  {name:44s}: {d:+.4f} +- {s:.4f} (Z {Z:+.2f}) | shuffle null {zs.mean():+.2f}+-{zs.std():.2f}, one-sided p {p_sh:.4f}{zes}"
      f" | pooled-var {dp:+.4f} +- {sp:.4f} (Z {Zp:+.2f}) | boot sig {sb:.4f} (Z {d / sb:+.2f})")
    return r


# SPARC rows (CFG534 code), fixed Upsilon and B1 free Upsilon
keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        TAB[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
    except ValueError:
        continue
SAMP = []
for f in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not f.endswith("_rotmod.dat"):
        continue
    d = np.genfromtxt(os.path.join(DATA, "sparc_data", f), comments="#")
    nm = f.replace("_rotmod.dat", "")
    if d.ndim != 2 or d.shape[1] < 6 or nm not in TAB:
        continue
    g = dict(name=nm, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], m=TAB[nm])
    if int(g["m"]["Q"]) <= 2 and g["m"]["Inc"] >= 30:
        SAMP.append(g)
ML = json.load(open(os.path.join(HERE, "cfg537_sparc_ml_results.json")))
WA = json.load(open(os.path.join(HERE, "cfg537_wallaby_results.json")))


def sparc_dout(a0, ups):
    out = []
    for g in SAMP:
        u = ups(g)
        Vb2 = g["Vg"] * np.abs(g["Vg"]) + u * g["Vd"] ** 2 + 1.4 * u * g["Vb"] ** 2
        gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]; ok = (gb > 0) & (gobs > 0)
        r = np.full(len(g["R"]), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
        w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
        out.append(wmean(r, w, ok & (g["R"] >= 3 * g["m"]["Rdisk"])))
    return np.array(out)


lmS = np.array([math.log10((0.5 * g["m"]["L36"] + 1.33 * g["m"]["MHI"]) * 1e9) for g in SAMP])
TS = np.array([g["m"]["T"] for g in SAMP])
RES = {"lane": "CFG537", "script": "cfg537_postfreeze", "dated": "2026-10-09, after the frozen runs; NO verdict weight"}
for f in FOOTS:
    P(f"\n[{f}]")
    a0 = A0SI[f] * CONV
    U1 = ML["variants"][f]["B1 global free"]["per_galaxy_ups"]
    rows = WA["per_galaxy"][f]
    xw = np.array([np.nan if r["d_out"] is None else r["d_out"] for r in rows]); lw = np.array([r["lMb"] for r in rows]); tw = np.array([r["T"] for r in rows])
    o = {}
    o["SPARC fixed (CFG534)"] = analyse("SPARC Delta_out fixed Upsilon (CFG534)", sparc_dout(a0, lambda g: 0.5), lmS, TS)
    o["SPARC B1 free"] = analyse("SPARC Delta_out B1 free Upsilon", sparc_dout(a0, lambda g: U1[g["name"]]), lmS, TS)
    o["WALLABY T<=3"] = analyse("WALLABY Delta_out (frozen, T<=3)", xw, lw, tw)
    o["WALLABY T<=2"] = analyse("WALLABY Delta_out S4 T<=2", xw, lw, tw, cut=2)
    o["SPARC T<=2"] = analyse("SPARC Delta_out T<=2 (fixed)", sparc_dout(a0, lambda g: 0.5), lmS, TS, cut=2)
    s, w = o["SPARC fixed (CFG534)"], o["WALLABY T<=3"]
    dd = s["diff"] - w["diff"]; ss = math.hypot(s["sig"], w["sig"]); ssb = math.hypot(s["sig_boot"], w["sig_boot"])
    o["SPARC_minus_WALLABY"] = dict(diff=dd, sig=ss, Z=dd / ss, sig_boot=ssb, Z_boot=dd / ssb)
    P(f"  SPARC - WALLABY Delta_out: {dd:+.4f} +- {ss:.4f} (Z {dd / ss:+.2f}; bootstrap sig {ssb:.4f}, Z {dd / ssb:+.2f})")
    RES[f] = o
json.dump(RES, open(os.path.join(HERE, "cfg537_postfreeze_results.json"), "w"), indent=1, default=float)
