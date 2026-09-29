#!/usr/bin/env python3
"""q4_kosmoplex_checks.py -- lane Q4: checks on the Macedonia 'Kosmoplex' derivation of 1/alpha (poster Zenodo 18650923; Principia Kosmoplex V20 Zenodo 17861153;
preprints.org 202508.1294 v3 abstract).  Imports lane D's checker modules UNMODIFIED (bar_lib) only for the target constant and sigma.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q4_kosmoplex_checks.py            -> exit 0 iff the flags equal the finding vector recorded in Amendment 3 of Q4_PREREGISTRATION.md:
              (1) poster formula reproduces the printed 137.035999143 to 1e-9: False; (2) V20 no-x formula reproduces the printed 137.036015319 to 1e-9: False;
              (3) V20's '1.62 sigma' for it is really > 100 sigma: True; (4) the OBMT product (9.19) has term n=1 equal to 0 and terms growing ~n^2: True;
              (5) the poster's altitude slope 4.6e-16 per km is > 100x what its own formula gives: True.
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q4_kosmoplex_checks.py --mutate   -> substitutes the PRINTED values (137.035999143, 137.036015319) for the computed ones;
              flags (1) and (2) become True, the recorded vector no longer matches, exit 1.
"""
import sys, os, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "D_calibration_bar"))
import mpmath as mp
import bar_lib as B
mp.mp.dps = 40
MUTATE = "--mutate" in sys.argv
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

T = mp.mpf("137.035999177")            # CODATA 2022
SIG = mp.mpf("0.000000021")            # its absolute 1-sigma (21 in the last two digits)
pi, g, z3 = mp.pi, mp.euler, mp.zeta(3)
lnn = 14 * pi ** 2 + mp.log(8)

def formula(x, C=137, glyph_denom=20):
    CA = C + 1 / (8 * pi)
    return CA - g / (CA - x) + z3 / (C * glyph_denom)

def xterm(lnn_, C=137, N_states=42, N_lines=7):
    return lnn_ / (2 * C) + mp.log(lnn_) / (N_states * N_lines)

x0 = xterm(lnn)
val = formula(x0)
P("ln n = %s (n = %s) ; x = %s" % (mp.nstr(lnn, 12), mp.nstr(mp.e ** lnn, 6), mp.nstr(x0, 12)))
P("poster formula: 1/alpha = 137 + 1/(8pi) - gamma/(137 + 1/(8pi) - x) + zeta(3)/(137*20) = %s" % mp.nstr(val, 15))
miss = abs(val / T - 1)
P("  miss vs CODATA 2022 137.035999177: %s = %.3g sigma_rel(1.6e-10) ; in the source's own unit (2.1e-8 absolute): %s sigma" % (mp.nstr(miss, 4), float(miss / mp.mpf("1.6e-10")), mp.nstr(abs(val - T) / SIG, 4)))
if MUTATE:
    val = mp.mpf("137.035999143")
c1 = abs(val - mp.mpf("137.035999143")) < mp.mpf("1e-9")
for lab, ln_ in (("ln n from n = 8.07e60 (printed)", mp.log(mp.mpf("8.07e60"))), ("ln n = 140.25 (printed recipe)", mp.mpf("140.25")), ("ln n = 14 pi^2 + ln 8 (printed formula)", lnn)):
    P("    variant %-42s: x = %s ; 1/alpha = %s ; miss vs printed 137.035999143 = %s" % (lab, mp.nstr(xterm(ln_), 10), mp.nstr(formula(xterm(ln_)), 13), mp.nstr(formula(xterm(ln_)) - mp.mpf("137.035999143"), 4)))
xp = mp.findroot(lambda x: formula(x) - mp.mpf("137.035999143"), x0)
P("    the x that WOULD reproduce the printed 137.035999143 is %s (printed formula gives %s; difference %s, %.2e relative)" % (mp.nstr(xp, 10), mp.nstr(x0, 10), mp.nstr(xp - x0, 4), float(abs(xp - x0) / x0)))
P("(1) reproduces printed 137.035999143 to 1e-9: %s (difference %s)" % (c1, mp.nstr(val - mp.mpf("137.035999143"), 4)))

# V20 no-x formula
val20 = formula(mp.mpf(0))
if MUTATE:
    val20 = mp.mpf("137.036015319")
c2 = abs(val20 - mp.mpf("137.036015319")) < mp.mpf("1e-9")
P("V20 (33.36) without x: %s ; printed 137.036015319 -> reproduces to 1e-9: %s" % (mp.nstr(val20, 15), c2))
s2018 = mp.mpf("137.035999084")
sig_v20 = abs(val20 - s2018) / SIG
P("(3) V20 computes (137.036015319 - 137.035999084)/0.000000021 and prints '1.62 sigma'; the arithmetic gives %s sigma (against its 2018-value; against 2022: %s sigma). 137.035999084(21) is the CODATA 2018 value, printed as 'CODATA 2022'."
  % (mp.nstr(sig_v20, 5), mp.nstr(abs(val20 - T) / SIG, 5)))
c3 = sig_v20 > 100
P("    sigma of the poster value 137.035999143 vs 2022: %s ; vs the 2018 value: %s" % (mp.nstr(abs(mp.mpf("137.035999143") - T) / SIG, 4), mp.nstr(abs(mp.mpf("137.035999143") - s2018) / SIG, 4)))

# x needed to hit T exactly, and its window
xs = mp.findroot(lambda x: formula(x) - T, x0)
dfdx = -g / (137 + 1 / (8 * pi) - xs) ** 2
P("x* that would hit T exactly = %s ; the source's x = %s ; d(1/alpha)/dx = %s per unit x" % (mp.nstr(xs, 12), mp.nstr(x0, 12), mp.nstr(dfdx, 6)))
P("    window of x within 1 sigma_CODATA (2.1e-8 abs): +-%s = %.2e relative to x ; within the bar 5e-10 (6.9e-8 abs): +-%s" % (mp.nstr(SIG / abs(dfdx), 4), float(SIG / abs(dfdx) / x0), mp.nstr(mp.mpf("6.85e-8") / abs(dfdx), 4)))
P("    the missing correction between V20's formula and 137.035999143 is %s = x-term effect on gamma/(C_A - x)" % mp.nstr(val - val20, 8))

# family count for the x-term: x = ln n/(p*137) + ln(ln n)/q
import numpy as np
lnnf = float(14 * math.pi ** 2 + math.log(8))
CAf = 137 + 1 / (8 * math.pi)
zf = float(z3); gf = float(g)
ps = np.arange(1, 9, dtype=float)[:, None]
qs = np.arange(1, 2001, dtype=float)[None, :]
xx = lnnf / (ps * 137.0) + math.log(lnnf) / qs
vv = CAf - gf / (CAf - xx) + zf / (137.0 * 20.0)
rel = np.abs(vv / float(T) - 1)
n_all = rel.size
for tol in (5e-10, 1.6e-10, 1e-9, 1e-8):
    P("    x-term family (p 1..8, q 1..2000; %d members): members within %.1e of T: %d" % (n_all, tol, int((rel <= tol).sum())))
span = float(vv.max() - vv.min())
P("    values of the family span %.3g in 1/alpha; a uniform density predicts %.2f members within 5e-10 relative (6.9e-8 abs) of any given target inside the span" % (span, n_all * 2 * 6.85e-8 / span))
hit = np.argwhere(rel <= 5e-10)
P("    hits (p,q,miss): " + "; ".join("(%d,%d,%.2e)" % (int(ps[i, 0]), int(qs[0, j]), rel[i, j]) for i, j in hit))

# OBMT product (9.19)
def obmt_terms(nmax):
    KH, KF = (3, 5, 6), (0, 1, 2, 4)
    r = []
    for n in range(1, nmax + 1):
        num = sum(math.comb(2 * n, k) for k in KH)
        den = sum(math.comb(2 * n, k) for k in KF)
        r.append(mp.mpf(num) / den)
    return r
r = obmt_terms(2000)
logprod = mp.fsum(mp.log(t) for t in r[1:])
P("(9.19) OBMT terms with K_H = {3,5,6}, K_F = {0,1,2,4}: term n=1: %s ; n=10: %s ; n=100: %s ; n=2000: %s ; ratio term(2000)/term(1000) = %s (n^2 growth would give 4)" % (mp.nstr(r[0], 6), mp.nstr(r[9], 6), mp.nstr(r[99], 6), mp.nstr(r[1999], 6), mp.nstr(r[1999] / r[999], 5)))
P("    term n=1 is exactly 0 (C(2,3)+C(2,5)+C(2,6) = 0), so the product as defined is 0; from n=2 on, log of the partial product to n=2000: %s and the terms do not tend to 1 (the convergence 'proof' of Theorem 9.2 claims ratio -> 1 + O(n^-1/2))" % mp.nstr(logprod, 8))
c4 = (r[0] == 0) and r[1999] > 10 and r[1999] / r[999] > 3

# altitude slope
def f_eps(eps):
    return formula(xterm(lnn + eps))
d_inv = mp.diff(f_eps, 0)                       # d(1/alpha)/d eps
dlna_deps = -d_inv / val                        # d ln alpha / d eps
g0 = mp.mpf("9.80665"); c = mp.mpf("299792458")
eta = mp.mpf("4.2")
eps_km = eta * g0 * 1000 / c ** 2
slope_km = dlna_deps * eps_km
P("altitude: eps(Phi) = eta*dPhi/c^2 with eta = 4.2 ; per km at g = 9.80665: eps = %s ; formula's d ln(alpha)/d eps = %s ; so d alpha/alpha per km = %s" % (mp.nstr(eps_km, 6), mp.nstr(dlna_deps, 6), mp.nstr(slope_km, 6)))
P("    the poster states d alpha/alpha = 4.6e-16 per km and (1/alpha) d alpha/d Phi = 4.7e-17 per m^2/s^2 (i.e. d ln alpha/d eps = 1.1); ratio stated/computed = %s" % mp.nstr(mp.mpf("4.6e-16") / abs(slope_km), 5))
c5 = mp.mpf("4.6e-16") / abs(slope_km) > 100
# cosmic-time drift if n * t_Planck = age (poster: 'n t_Planck ~ 13.8 Gyr')
dlna_dlnn = dlna_deps                            # eps adds to ln n
tage = mp.mpf("13.8e9")
P("cosmic drift if ln n grows as ln(age): d ln alpha / dt = (d ln alpha/d ln n)/age = %s per yr (n = age/t_Planck reading of the poster's consistency line)" % mp.nstr(dlna_dlnn / tage, 4))
P("    (bounds from optical clocks are of order 1e-17 per yr: RECALLED, not computed here)")

# small internal identities
P("base capacity: 2*C(8,4) - 3 = %d ; |GL(3,2)| - 31 = %d" % (2 * math.comb(8, 4) - 3, 168 - 31))
recorded = (False, False, True, True, True)
ok = (c1, c2, c3, c4, c5) == recorded
if MUTATE:
    P("MUTATE: flags (1)-(5) = %s vs recorded %s (a live control mismatches here); exit %d" % ((c1, c2, c3, c4, c5), recorded, 0 if ok else 1))
    open("q4_kosmoplex_checks_MUTATE.out", "w").write("\n".join(out) + "\n")
    sys.exit(0 if ok else 1)
P("flags: (1)=%s (2)=%s (3)=%s (4)=%s (5)=%s ; recorded finding vector %s -> match: %s" % (c1, c2, c3, c4, c5, recorded, ok))
open("q4_kosmoplex_checks.out", "w").write("\n".join(out) + "\n")
sys.exit(0 if ok else 1)
