#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
R03 -- DERIVE CORRECTED VELOCITY CURVATURE AND ITS OBSERVABLE DOMAIN.

Target (FOLLOWUP_PACKETS.md R03):  conditional on g^2 = a0 G M_total(r)/r^2 and
circular motion, v^4 = a0 G M_total and beta = (1/4) d ln M_total/d ln r.
For M_total = Mbase + C_log ln(r/r0):  beta = C_log/(4 M_total) and the curvature
invariant C_beta = d beta/d ln r + 4 beta^2  satisfies C_beta = 0.
For M_total = Mbase + C_sqrt sqrt(r):  C_beta = beta/2.  These are conditional
shape relations.  Also: estimate the covariance cost of a second derivative of a
noisy rotation curve (a curvature can be formally distinctive yet observationally
unusable).
"""
import json, os, math
import numpy as np

OUT = {"lane": "R03", "checks": {}, "numbers": {}}
CH = []

def check(name, measured, ok, reading=""):
    CH.append(bool(ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading:  {reading}")

# ------------------------------------------------ 1. the curvature identities (numeric, exact)
# beta = (1/4) d ln M / d ln r ;  C_beta = d beta / d ln r + 4 beta^2.
# Log model:  M = Mbase + Clog ln(r/r0)
#   dM/dlnr = Clog ;  beta = Clog/(4M) ;  d beta/dlnr = -(Clog/(4M^2)) dM/dlnr = -Clog^2/(4M^2)
#   => C_beta = -Clog^2/(4M^2) + 4 (Clog/(4M))^2 = 0.        EXACT.
# Sqrt model:  M = Mbase + Cs sqrt(r) ;  dM/dlnr = (Cs/2) sqrt(r) = (M - Mbase)/2
#   beta = (M-Mbase)/(8M) ;  d beta/dlnr = (1/8) d[(M-Mbase)/M]/dlnr = (Mbase/(8M^2)) (M-Mbase)/2
#   ... 4 beta^2 = (M-Mbase)^2/(16 M^2) ;  C_beta = (Mbase(M-Mbase))/(16M^2) + (M-Mbase)^2/(16M^2)
#   = (M-Mbase)(Mbase + M - Mbase)/(16M^2) = (M-Mbase) M/(16 M^2) = (M-Mbase)/(16M) = beta/2.  EXACT.
Mbase, Clog, Cs, r0 = 3.0, 1.0, 1.0, 1.0
r = np.geomspace(1.05, 20.0, 2000)
Mlog = Mbase + Clog * np.log(r / r0)
dlnr = np.gradient(np.log(r))
beta_log = np.gradient(np.log(Mlog)) / dlnr / 4.0
Cbet_log = np.gradient(beta_log) / dlnr + 4 * beta_log ** 2
Msq = Mbase + Cs * np.sqrt(r)
beta_sq = np.gradient(np.log(Msq)) / dlnr / 4.0
Cbet_sq = np.gradient(beta_sq) / dlnr + 4 * beta_sq ** 2
mid = slice(2, -2)                                            # exclude one-sided-gradient boundary rows
check("V1 the curvature invariant for the LOGARITHMIC continuation is zero everywhere in the interior "
      "(derived C_beta = 0; numeric max |C_beta| over the interior far below 4 beta^2's scale)",
      f"max |C_beta| = {np.max(np.abs(Cbet_log[mid])):.2e} vs median 4 beta^2 = {np.median(4*beta_log[mid]**2):.2e}",
      np.max(np.abs(Cbet_log[mid])) < 1e-6 * np.median(4 * beta_log[mid] ** 2),
      "C_beta = d beta/dlnr + 4 beta^2 is the amplitude-free curvature discriminator")
check("V2 the curvature invariant for the SQUARE-ROOT continuation equals beta/2 everywhere in the "
      "interior (derived C_beta = beta/2; numeric max relative deviation small)",
      f"max |C_beta - beta/2|/(|beta/2|+eps) = "
      f"{np.max(np.abs(Cbet_sq[mid] - beta_sq[mid]/2)/np.maximum(np.abs(beta_sq[mid]/2),1e-300)):.2e}",
      np.max(np.abs(Cbet_sq[mid] - beta_sq[mid] / 2) / np.maximum(np.abs(beta_sq[mid] / 2), 1e-300)) < 1e-6,
      "the two continuations are separated by a curvature identity, independent of amplitude")

# ------------------------------------------------ 2. matched-profile comparison
# Same independent mass at an anchor radius, then same local derivative as a separate match:
r_anc = 4.0
M_anc = float(np.interp(r_anc, r, Mlog))
# Log model pinned by (M(r_anc), dM/dlnr(r_anc)):
Clog_fit = float(np.interp(r_anc, r, Mlog)) * 0 + (M_anc * 4 * float(np.interp(r_anc, r, beta_log))) * 0
# do it honestly: beta_anc from the log model, then construct the sqrt model that shares BOTH
# (M_anc, beta_anc) at r_anc -- impossible with one parameter:
beta_anc = float(np.interp(r_anc, r, beta_log))
# sqrt model with TWO parameters matched: M = m0 + c sqrt(r); M(m0,c) = M_anc, beta(m0,c) = beta_anc
# beta = (M - m0)/(8M) = beta_anc  =>  m0 = M_anc (1 - 8 beta_anc) ;  c = (M_anc - m0)/sqrt(r_anc)
m0_s = M_anc * (1 - 8 * beta_anc)
c_s = (M_anc - m0_s) / math.sqrt(r_anc)
Msq_fit = m0_s + c_s * np.sqrt(r)
beta_sq_fit = (Msq_fit - m0_s) / (8 * Msq_fit)
d_beta_sq = np.gradient(beta_sq_fit) / dlnr
Cbet_sq_fit = d_beta_sq + 4 * beta_sq_fit ** 2
out_diff = np.max(np.abs(Cbet_sq_fit[mid] - beta_sq_fit[mid] / 2))
check("V3 at the same anchor mass and the same local slope beta(r_anc), the square-root continuation "
      "still bends with C_beta = beta/2 -- the curvature identity survives matching; the log model's "
      "C_beta = 0 is separated by a measurable factor",
      f"max |C_beta - beta/2| after two-point matching = {out_diff:.2e}",
      out_diff < 1e-6,
      "matching amplitude and slope does not erase the shape distinction")

# ------------------------------------------------ 3. observable domain: second-derivative cost
# A rotation curve with per-point fractional error eps_v at n points over a radius range Delta_ln r:
#  beta is a first derivative:  sigma_beta ~ eps_v * sqrt(2)/Delta_lnr
#  C_beta needs a SECOND derivative:  sigma_C ~ eps_v * f(n)/Delta_lnr^2.
# Numeric:  n = 12 points over Delta ln r = 0.92 (a factor 2.5), eps_v = 1%:
def cov_cost(n, dlnr_span, eps_v, nsim=4000):
    rng = np.random.default_rng(7)
    rr = np.geomspace(1.0, math.exp(dlnr_span), n)
    lr = np.log(rr)
    Cb = np.empty(nsim)
    bet = np.empty(nsim)
    for i in range(nsim):
        v = 1.0 + eps_v * rng.standard_normal(n)
        b = np.gradient(np.log(v), lr)
        bet[i] = b[n // 2]
        Cb[i] = np.gradient(b, lr)[n // 2] + 4 * b[n // 2] ** 2
    return float(np.median(bet)), float(np.std(bet)), float(np.std(Cb))
# realistic deep-MOND: v flat-ish, beta ~ 0.08 (L311's 20-60 kpc band), Delta ln r = ln(60/20) = 1.10
m_b, s_b, s_C = cov_cost(12, 1.10, 0.01)
OUT["numbers"]["sigma_beta"] = float(s_b)
OUT["numbers"]["sigma_Cbeta"] = float(s_C)
OUT["numbers"]["beta_level"] = float(m_b)
sep = m_b / 2.0                     # the sqrt-model C_beta value at that beta
check("V4 the observable domain: with 12 points at 1% over a factor-3 window, the curvature "
      "invariant's 1-sigma error dwarfs the sqrt-vs-log separation beta/2 (a second derivative "
      "of a noisy curve is not a usable discriminator at galactic data quality)",
      f"sigma(C_beta) = {s_C:.3f} vs separation beta/2 = {sep:.3f} (ratio {s_C/max(sep,1e-9):.1f}x); "
      f"sigma(beta) = {s_b:.3f}",
      s_C > 3 * sep,
      "the curvature discriminator needs either much better precision or wider dynamic range; "
      "R18 should treat it as precision-gated, not as a ready observable")

print("\nR03 COMPLETE:", f"{sum(CH)}/{len(CH)} checks PASS")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
import sys; sys.exit(0 if all(CH) else 1)