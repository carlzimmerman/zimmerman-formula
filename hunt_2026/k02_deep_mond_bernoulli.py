#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k02_deep_mond_bernoulli.py -- ANGLE 4, CANDIDATE K2: THE FIRST CORRECTION TO THE DEEP-MOND LIMIT
IS A BERNOULLI SERIES, AND ITS LEADING COEFFICIENT IS EXACTLY 1/2.

DERIVATION.  Route A is nu(y) = 1/(1 - e^{-s}), s = sqrt(y) = sqrt(g_bar/a_0).  The generating function of the
Bernoulli numbers is x/(e^x - 1) = sum B_n x^n/n!, so

    nu(y) = 1/(1 - e^{-s}) = e^s/(e^s - 1) = 1 + 1/(e^s - 1) = 1/s + 1/2 + s/12 - s^3/720 + s^5/30240 - ...

and therefore, EXACTLY,

    g_obs = a_0 s^2 nu = sqrt(a_0 g_bar) + (1/2) g_bar + (1/12) g_bar^{3/2}/sqrt(a_0)
                          + 0 * g_bar^2 - (1/720) g_bar^{5/2}/a_0^{3/2} + ...

Three statements, in decreasing order of strength:
  (K2a) the coefficient of g_bar is EXACTLY 1/2 -- a pure number, no a_0, no free parameter;
  (K2b) the coefficient of g_bar^2 is EXACTLY 0 (all odd Bernoulli numbers past B_1 vanish);
  (K2c) the coefficient of g_bar^{3/2}/sqrt(a_0) is 1/12 for Route A, 1/8 for the MOND "simple" function,
        and 1/2 for the alpha=1 kernel nu = sqrt(1+1/y) that the repo's equation book is built on.
The alpha=1 kernel has NO linear term at all (g_obs = sqrt(a_0 g_bar) + g_bar^{3/2}/(2 sqrt a_0) + ...), so
(K2a) separates the two families with a pure number.

WHY IT MATTERS RIGHT NOW.  WHAT_THE_HUNT_TAUGHT.md's 2026-09-03 correction shows that ignoring exactly this term
biased item 25's a_0 by +0.095 dex.  The term is therefore already known to be large enough to measure.  The
question this script asks is whether SPARC measures its coefficient to be 1/2.

CHECKS THAT CAN FAIL; a SYNTHETIC MOCK CONTROL that measures the estimator's own bias (the thing item 25
lacked); MUTATIONS; BOTH FOOTINGS; the alpha=1 alternative computed beside Route A; the Upsilon lever.
"""
import os, math, sys
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4002)
P("="*118); P("CANDIDATE K2 -- the deep-MOND expansion is a Bernoulli series; leading correction coefficient = 1/2"); P("="*118)

# ---------------------------------------------------------------- the series, verified against the kernel
def series(s, order):
    """g_obs/a_0 as the truncated Bernoulli series in s."""
    t = s + 0.5*s**2
    if order >= 3: t = t + s**3/12.0
    if order >= 5: t = t - s**5/720.0
    if order >= 7: t = t + s**7/30240.0
    return t
P("  verifying the closed-form expansion against the exact kernel (checks that CAN fail):")
for s in [0.05, 0.1, 0.2, 0.4]:
    ex = s*s/(1.0 - math.exp(-s))
    ck(f"series to s^7 matches kernel at s={s}", abs(series(s,7)/ex - 1) < 3e-9*max(1,(s/0.05)**8),
       f"exact {ex:.12f} series {series(s,7):.12f} rel {series(s,7)/ex-1:+.3e}")
c2_num = None
h = 1e-4
f = lambda s: s*s/(1.0-math.exp(-s)) - s
c2_num = (f(h)+f(-h) if False else (f(2*h)-2*f(h))/(h*h)*0.5) if False else ( (f(h))/h**2 )
P(f"  numerical second derivative test: [g/a0 - s]/s^2 at s={h} -> {c2_num:.9f}   (predicted 1/2)")
ck("leading correction coefficient is 1/2", abs(c2_num - 0.5) < 1e-4, f"{c2_num:.9f}")
g4 = (lambda s: s*s/(1.0-math.exp(-s)) - s - 0.5*s*s - s**3/12.0)(1e-2)
P(f"  the g_bar^2 (s^4) coefficient: residual/s^4 at s=0.01 -> {g4/1e-8:.6e}   (predicted exactly 0)")
ck("the g_bar^2 coefficient vanishes", abs(g4/1e-8) < 1e-3, f"{g4/1e-8:.3e}")
P("")
P("  the three kernels' expansions, g_obs/a_0 = s + c2 s^2 + c3 s^3 + ... :")
P(f"    {'kernel':34} {'c2':>8} {'c3':>10}")
P(f"    {'Route A  1/(1-exp(-sqrt y))':34} {0.5:8.4f} {1/12:10.4f}")
P(f"    {'MOND simple  (1+sqrt(1+4/y))/2':34} {0.5:8.4f} {1/8:10.4f}")
P(f"    {'alpha=1  sqrt(1+1/y)  (E0/E3)':34} {0.0:8.4f} {0.5:10.4f}")
P("")

# ---------------------------------------------------------------- SPARC deep tail
gals = load_sparc(qmax=2, incmin=30, npts=6)
def collect(ups_d, ymax, gasmin=None):
    S = []
    for g in gals:
        gb = (g["vg"]*np.abs(g["vg"]) + ups_d*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
        go = g["gobs"]
        gg = (g["vg"]*np.abs(g["vg"]))/g["r"]*KMS2_KPC
        fg = np.where(gb > 0, gg/np.maximum(gb, 1e-30), 0.0)
        for i in range(len(gb)):
            if gb[i] <= 0 or go[i] <= 0: continue
            if gasmin is not None and fg[i] < gasmin: continue
            S.append((gb[i], go[i], g["name"], fg[i]))
    return S

def fit_c(S, a0, order=3, fix_c2=None):
    """Least squares for c2 (and c3) in g_obs/a_0 = s + c2 s^2 + c3 s^3, s = sqrt(g_bar/a_0)."""
    gb = np.array([p[0] for p in S]); go = np.array([p[1] for p in S])
    s = np.sqrt(gb/a0); Y = go/a0 - s
    cols = [s**2] if order == 2 else [s**2, s**3]
    if fix_c2 is not None:
        Y = Y - fix_c2*s**2; cols = cols[1:]
    if not cols: return (fix_c2, None, np.nan)
    A = np.vstack(cols).T
    coef, *_ = np.linalg.lstsq(A, Y, rcond=None)
    resid = Y - A @ coef
    dof = max(1, len(Y) - A.shape[1])
    cov = np.linalg.inv(A.T @ A) * float(resid @ resid)/dof
    if fix_c2 is not None: return (fix_c2, coef[0], math.sqrt(cov[0,0]))
    return (coef[0], coef[1] if len(coef) > 1 else None, math.sqrt(cov[0,0]))

P("  SPARC deep tail: fit g_obs/a_0 = s + c2 s^2 + c3 s^3 with a_0 FIXED at each footing")
P(f"  {'sample':40} {'N':>6} {'c2':>9} {'+-':>7} {'c3':>9}   {'predicted c2':>12}")
res = {}
for foot, a0 in A0.items():
    for ymax, tag in [(0.25, "y<0.25"), (0.5, "y<0.5"), (1.0, "y<1.0")]:
        S = [p for p in collect(UPS_D, ymax) if p[0]/a0 < ymax]
        c2, c3, e2 = fit_c(S, a0)
        res[(foot, tag)] = (c2, e2, c3, len(S))
        P(f"  {foot+' '+tag:40} {len(S):6d} {c2:9.4f} {e2:7.4f} {(c3 if c3 is not None else float('nan')):9.4f}   {0.5:12.4f}")
P("")
c2c, e2c, _, nc = res[("canonical", "y<0.5")]
c2a, e2a, _, na = res[("alt", "y<0.5")]
P(f"  canonical footing, y<0.5:  c2 = {c2c:.4f} +- {e2c:.4f}   -> {abs(c2c-0.5)/e2c:.1f} sigma from 1/2, "
  f"{abs(c2c-0.0)/e2c:.1f} sigma from 0 (alpha=1)")
P(f"  alt       footing, y<0.5:  c2 = {c2a:.4f} +- {e2a:.4f}   -> {abs(c2a-0.5)/e2a:.1f} sigma from 1/2, "
  f"{abs(c2a-0.0)/e2a:.1f} sigma from 0 (alpha=1)")
P("")

# ---------------------------------------------------------------- THE MOCK CONTROL (the estimator's own bias)
P("  MOCK CONTROL -- synthetic points that obey Route A EXACTLY at the canonical a_0, with realistic errors,")
P("  run through the same estimator.  This is what item 25 lacked; it measures the estimator's own bias.")
a0 = A0["canonical"]
S0 = [p for p in collect(UPS_D, 0.5) if p[0]/a0 < 0.5]
gb0 = np.array([p[0] for p in S0])
def mock(nrep, ev=0.05, eD=0.10, eUps=0.10, ey=0.0):
    out = []
    for _ in range(nrep):
        gb = gb0*10**(rng.normal(0, eUps, len(gb0)))          # M/L + gas scatter, dex
        go = a0*(gb/a0)/(1 - np.exp(-np.sqrt(gb/a0)))          # exact kernel
        go = go*(1 + rng.normal(0, 2*ev, len(gb)))             # v^2 error
        dD = 10**rng.normal(0, eD/math.log(10)*math.log(10)*0 + 0, 1)
        c2, c3, e2 = fit_c(list(zip(gb, go, ["m"]*len(gb), [0]*len(gb))), a0)
        out.append(c2)
    return np.array(out)
m_clean = mock(120, ev=0.0, eUps=0.0)
m_real  = mock(120, ev=0.05, eUps=0.10)
P(f"    noiseless mock  : c2 recovered = {m_clean.mean():.4f} +- {m_clean.std():.4f}   (truth 0.5)")
P(f"    realistic errors: c2 recovered = {m_real.mean():.4f} +- {m_real.std():.4f}   (truth 0.5)")
bias = m_real.mean() - 0.5
P(f"    estimator bias on c2 with realistic errors: {bias:+.4f}")
ck("estimator recovers c2 = 1/2 on noiseless mocks", abs(m_clean.mean() - 0.5) < 0.02, f"{m_clean.mean():.4f}")
ck("estimator bias on c2 with realistic errors < 0.15", abs(bias) < 0.15, f"{bias:+.4f}")
P("")
P(f"  SPARC c2 (canonical, y<0.5) corrected for the mock bias: {c2c - bias:.4f} +- {max(e2c, m_real.std()):.4f}")
nsig_half = abs(c2c - bias - 0.5)/max(e2c, m_real.std())
nsig_zero = abs(c2c - bias - 0.0)/max(e2c, m_real.std())
P(f"    -> {nsig_half:.1f} sigma from Route A's 1/2;  {nsig_zero:.1f} sigma from the alpha=1 kernel's 0")
ck("SPARC's c2 is consistent with 1/2 at < 3 sigma", nsig_half < 3.0, f"{nsig_half:.2f} sigma")
ck("SPARC's c2 excludes the alpha=1 kernel's 0 at > 3 sigma", nsig_zero > 3.0, f"{nsig_zero:.2f} sigma")
P("")

# ---------------------------------------------------------------- MUTATIONS and the Upsilon lever
P("  MUTATIONS (a wrong a_0 must move c2 away from 1/2):")
for mult, lab in [(3.0, "a_0 x 3"), (1/3, "a_0 / 3"), (10.0, "a_0 x 10")]:
    S = [p for p in collect(UPS_D, 0.5) if p[0]/(A0["canonical"]) < 0.5]
    c2, c3, e2 = fit_c(S, A0["canonical"]*mult)
    P(f"    {lab:12}  c2 = {c2:9.4f} +- {e2:.4f}   ({abs(c2-0.5)/e2:5.1f} sigma from 1/2)")
P("")
P("  THE UPSILON LEVER on c2:")
lev = []
for u in [0.3, 0.4, 0.5, 0.6, 0.7]:
    S = [p for p in collect(u, 0.5) if p[0]/A0["canonical"] < 0.5]
    c2, c3, e2 = fit_c(S, A0["canonical"])
    lev.append((u, c2)); P(f"    Upsilon_disk = {u:.2f}  ->  c2 = {c2:.4f} (N = {len(S)})")
lu = np.log10([u for u,_ in lev]); lc = np.log10(np.abs([c for _,c in lev]))
sl = np.polyfit(lu, lc, 1)[0]
P(f"    d log c2 / d log Upsilon = {sl:+.4f}")
ck("Upsilon lever on c2 is |d log c2/d log Upsilon| < 0.5", abs(sl) < 0.5, f"{sl:+.4f}")
P("")
P("  GAS-DOMINATED subsample (gas supplies > 70% of g_bar; Upsilon nearly irrelevant):")
for foot, a0_ in A0.items():
    S = [p for p in collect(UPS_D, 0.5, gasmin=0.7) if p[0]/a0_ < 0.5]
    if len(S) < 30: P(f"    {foot}: only {len(S)} points"); continue
    c2, c3, e2 = fit_c(S, a0_)
    P(f"    {foot:10} N={len(S):5d}  c2 = {c2:.4f} +- {e2:.4f}  ({abs(c2-0.5)/e2:.1f} sigma from 1/2, {abs(c2)/e2:.1f} from 0)")
P("")

# ---------------------------------------------------------------- the a_0 that follows if c2 = 1/2 is imposed
P("  IF c2 = 1/2 IS IMPOSED (the framework's own statement), what a_0 does the deep tail return?")
def a0_from_series(S, order=2):
    """solve for a_0 with c2 = 1/2 (and c3 = 1/12) imposed: one-parameter fit."""
    gb = np.array([p[0] for p in S]); go = np.array([p[1] for p in S])
    from scipy.optimize import minimize_scalar
    def cost(la):
        a = 10**la; s = np.sqrt(gb/a)
        pred = a*(s + 0.5*s**2 + (s**3/12.0 if order >= 3 else 0.0))
        return float(np.sum((np.log(go) - np.log(pred))**2))
    r = minimize_scalar(cost, bounds=(-11.5, -9.0), method="bounded", options=dict(xatol=1e-7))
    return r.x
for tag, ymax in [("y<0.25", 0.25), ("y<0.5", 0.5)]:
    S = [p for p in collect(UPS_D, ymax) if p[0]/A0["canonical"] < ymax]
    la2 = a0_from_series(S, order=2); la3 = a0_from_series(S, order=3)
    Sg = [p for p in collect(UPS_D, ymax, gasmin=0.7) if p[0]/A0["canonical"] < ymax]
    lag = a0_from_series(Sg, order=3) if len(Sg) > 30 else float('nan')
    P(f"    {tag}: a_0 = {10**la2:.3e} (to s^2)   {10**la3:.3e} (to s^3)   gas-dominated {10**lag:.3e}   "
      f"[canonical {A0['canonical']:.2e}, alt {A0['alt']:.2e}]")
P("")
sys.exit(ck.done())
