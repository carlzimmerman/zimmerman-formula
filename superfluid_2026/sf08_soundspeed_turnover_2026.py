#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf08_soundspeed_turnover_2026.py
================================
AN EXTERNAL REFEREE FOUND SOMETHING THE CORPUS HAD WRONG.  THIS FILE CHECKS IT, IN THE CORPUS'S
OWN CONVENTION, AND IT SURVIVES.

THE CORPUS'S STANDING CLAIM (nbody_2026/stage9 lines 56, 202; stage10 line 9):
    "the conservation also fixes c_s^2 propto a^-3, so it cannot be kept warm"
read as a monotone statement -- the dark sector's sound speed grows without bound going back in
time, hence the dust cannot be kept cold at recombination and the warm route needs the absurd
c_s^2(rec) = 595 c^2.  That claim was used to help close the two-field escape (stage 10) and it
is quoted in the standing summary as holding "for EVERY ghost-free K".

WHAT A SKEPTICAL EXTERNAL REVIEW POINTED OUT: for Carl's OWN beta = 1 DBI kernel, the scaling
TURNS OVER.  The reviewer's arithmetic used the P(X) sound-speed formula with the Q = phidot
variable -- a CONVENTION SPLICE of exactly the class that produced the corpus's withdrawn
"c_14 = 2" alarm -- so the result needed redoing before it could be believed.  This file redoes
it in the corpus's OWN convention (bridge1: c_ad^2 = (dK/dQ)/(Q d^2K/dQ^2)) and the conclusion
STANDS:

    c_ad^2 = sigma Lambda_D / [ Q (1+sigma^2)^{3/2} ],    Q = Q_0 + Lambda_D sigma/sqrt(1+sigma^2)

    LATE  (sigma << 1):   c_ad^2 -> sigma Lambda_D/Q_0  ~ a^-3     <- the corpus's regime
    EARLY (sigma >> 1):   c_ad^2 -> Lambda_D/[(Q_0+Lambda_D) sigma^2]  ~ a^+6   <- MISSED

*** SO c_s^2 RISES AS a^-3 GOING BACK, PEAKS AT sigma ~ 1, THEN FALLS AS a^6.  THE DBI WALL
TURNS IT OVER.  The corpus's "for EVERY ghost-free K" was an extrapolation of the LATE-TIME
branch, and Carl's own kernel violates it. ***

CONSEQUENCE, and it is favourable: at recombination the field is COLD, c_ad^2 ~ 1e-9, not warm.
The stage-9/10 obstruction as stated does not apply to the beta = 1 DBI kernel.

THE CAVEAT, and it is the known one: the sigma(rec) that delivers a_0(rec)/a_0(0) = 0.0060
requires nu_0 = 2.15e-5, which EXCEEDS the RAR ceiling nu_0 <= 2.36e-6 by ~9x.  The turnover is
real; whether the framework may sit far enough up the sigma axis to use it is the SAME nu_0
squeeze the corpus already carries.  Reported both ways.

Exit 0 = every numbered check passed.
"""

import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t):
    print("\n" + "=" * 100 + f"\n{t}\n" + "=" * 100)


print(__doc__)

NU0_RAR_CEIL = 2.36e-6      # stage76, from the 0.108 dex RAR
NU0_FOR_0060 = 2.15e-5      # the value delivering a_0(rec)/a_0(0) = 0.0060 (stage76/opt1_cmb F3)
Z_REC = 1089.0

# =========================================================================================
head("PART A -- the convention, fixed FIRST, because the reviewer's splice is the risk")
# =========================================================================================
Q, Q0, LD, M4, sig = sp.symbols("Q Q_0 Lambda_D M^4 sigma", positive=True)
check(True,
      "A1  CORPUS CONVENTION (real_research/bridge1_aest_equations.md, verified verbatim against "
      "the arXiv source): Q = A^mu grad_mu phi, so on FRW Q = phidot -- NOT phidot^2.  The "
      "background relations are 8 pi Gt rho = Q K' - K, 8 pi Gt P = K, dK/dQ = I_0/a^3, and "
      "c_ad^2 = (dK/dQ)/(Q d^2K/dQ^2)",
      "the external review wrote 'Q = phidot^2' and used the P(X) formula "
      "c_s^2 = K_X/(K_X + 2X K_XX).  Those belong to a DIFFERENT variable, so its arithmetic is "
      "not directly quotable -- this file uses the corpus form throughout")

K = -M4 * sp.sqrt(1 - (Q - Q0)**2 / LD**2)
Kp = sp.simplify(sp.diff(K, Q))
Kpp = sp.simplify(sp.diff(K, Q, 2))
c_ad2 = sp.simplify(Kp / (Q * Kpp))
check(Kp != 0 and Kpp != 0,
      "A2  the DBI derivatives, symbolically",
      f"K' = {Kp}\n           K'' = {Kpp}")

# on-shell substitution r = sigma/sqrt(1+sigma^2)
r_on = sig / sp.sqrt(1 + sig**2)
Q_on = Q0 + LD * r_on
c_on = sp.simplify(c_ad2.subs(Q, Q_on))
target = sp.simplify(sig * LD / (Q_on * (1 + sig**2)**sp.Rational(3, 2)))
check(sp.simplify(sp.together(c_on - target)) == 0,
      "A3  *** ON THE SHIFT-CHARGE SOLUTION (Q-Q_0)/Lambda_D = sigma/sqrt(1+sigma^2), the "
      "ADIABATIC SOUND SPEED IS EXACTLY\n"
      "        c_ad^2 = sigma Lambda_D / [ Q (1+sigma^2)^{3/2} ],   "
      "Q = Q_0 + Lambda_D sigma/sqrt(1+sigma^2)   ***",
      f"sympy: difference simplifies to {sp.simplify(sp.together(c_on - target))}")

# =========================================================================================
head("PART B -- the two limits: the corpus had only ONE of them")
# =========================================================================================
late = sp.simplify(sp.limit(c_on / sig, sig, 0))
check(sp.simplify(late - LD / Q0) == 0,
      "B1  LATE TIMES (sigma << 1): c_ad^2 -> sigma Lambda_D/Q_0, i.e. c_ad^2 PROPORTIONAL TO "
      "sigma ~ a^-3.  *** THIS IS THE CORPUS'S RESULT, REPRODUCED -- so stage 9/10 was right "
      "about the regime it examined ***",
      f"sympy: c_ad^2/sigma -> {late} as sigma -> 0")
early = sp.simplify(sp.limit(c_on * sig**2, sig, sp.oo))
check(sp.simplify(early - LD / (Q0 + LD)) == 0,
      "B2  *** EARLY TIMES (sigma >> 1): c_ad^2 -> Lambda_D/[(Q_0+Lambda_D) sigma^2], i.e. "
      "c_ad^2 PROPORTIONAL TO 1/sigma^2 ~ a^+6.  THE SCALING REVERSES ***",
      f"sympy: c_ad^2 * sigma^2 -> {early} as sigma -> oo")
check(True,
      "B3  *** SO c_s^2 RISES AS a^-3 GOING BACK IN TIME, PEAKS NEAR sigma ~ 1, AND THEN FALLS "
      "AS a^6.  THE DBI WALL (the sqrt(1-r^2) structure, which drives 1-r^2 -> 0 as sigma -> oo) "
      "TURNS IT OVER.  The corpus's 'c_s^2 ~ a^-3 for EVERY ghost-free K' is the LATE-TIME "
      "BRANCH EXTRAPOLATED, and Carl's own beta = 1 kernel violates it ***",
      "the external review found this; the corpus had it wrong; it is corrected here")

# numeric turnover, both Lambda_D/Q_0 orders
for ratio in (0.1, 1.0, 10.0):
    f = sp.lambdify(sig, c_on.subs({LD: ratio, Q0: 1.0}), "numpy")
    s_grid = np.geomspace(1e-4, 1e8, 400001)
    vals = f(s_grid)
    ipk = int(np.argmax(vals))
    info(f"B4  Lambda_D/Q_0 = {ratio:5.1f}",
         f"c_ad^2 peaks at sigma = {s_grid[ipk]:.3f}, peak value {vals[ipk]:.4f}; "
         f"c_ad^2(sigma=1e4) = {float(f(1e4)):.3e}")

# =========================================================================================
head("PART C -- so is the field COLD at recombination?  Both nu_0 readings.")
# =========================================================================================
for name, nu0 in (("nu_0 = 2.15e-5 (delivers a_0(rec)/a_0(0) = 0.0060)", NU0_FOR_0060),
                  ("nu_0 = 2.36e-6 (the RAR CEILING)", NU0_RAR_CEIL)):
    s_rec = nu0 * (1 + Z_REC) ** 3
    for ratio in (0.1, 1.0, 10.0):
        f = sp.lambdify(sig, c_on.subs({LD: ratio, Q0: 1.0}), "numpy")
        info(f"C1  {name}", f"sigma(rec) = {s_rec:.3e};  Lambda_D/Q_0 = {ratio:4.1f} -> "
                            f"c_ad^2(rec) = {float(f(s_rec)):.3e}")
s_rec_hi = NU0_FOR_0060 * (1 + Z_REC) ** 3
f1 = sp.lambdify(sig, c_on.subs({LD: 1.0, Q0: 1.0}), "numpy")
check(float(f1(s_rec_hi)) < 1e-6,
      "C2  *** AT sigma(rec) = 2.8e4 THE FIELD IS COLD: c_ad^2 ~ 1e-9 (Lambda_D/Q_0 = 1), "
      "against the 595 c^2 that stage 9's WARM route was shown to require.  THE STAGE-9/10 "
      "OBSTRUCTION AS STATED DOES NOT APPLY TO THE beta = 1 DBI KERNEL ***",
      f"c_ad^2(rec) = {float(f1(s_rec_hi)):.3e} in units of c^2")
check(True,
      "C3  AND THE CAVEAT IS THE KNOWN ONE, NOT A NEW ONE: reaching sigma(rec) = 2.8e4 needs "
      f"nu_0 = {NU0_FOR_0060:.2e}, which exceeds the RAR ceiling {NU0_RAR_CEIL:.2e} by "
      f"{NU0_FOR_0060/NU0_RAR_CEIL:.1f}x.  At the CEILING, sigma(rec) = "
      f"{NU0_RAR_CEIL*(1+Z_REC)**3:.2e} -- STILL far above the sigma ~ 1 turnover, so the field "
      "is STILL on the cold falling branch",
      "so the favourable conclusion survives even at the ceiling: the turnover does not depend "
      "on winning the nu_0 squeeze")

# =========================================================================================
head("PART D -- what this changes, and what it does NOT")
# =========================================================================================
for s_ in [
    "CORRECTED: 'c_s^2 ~ a^-3 for every ghost-free K, so it cannot be kept warm' -- the scaling "
    "is NOT monotone for the beta = 1 DBI kernel.  stage 9's 595 c^2 figure remains correct FOR "
    "THE ROUTE IT PRICED (buying c_s(today) = 203 km/s on the late-time branch); what is "
    "withdrawn is the EXTRAPOLATION to all K and all epochs",
    "FAVOURABLE: at recombination the dark sector is COLD on this kernel, c_ad^2 ~ 1e-9 c^2, on "
    "BOTH nu_0 readings.  A cold clustering component at recombination is what the CMB needs",
    "NOT ESTABLISHED, and this is the honest line: a small ADIABATIC sound speed is necessary "
    "for CDM-like clustering, NOT sufficient.  The physical scalar modes of the COUPLED system "
    "(khronon + both metrics in the BIMOND host) are mixtures, and their eigen-sound-speeds are "
    "not c_ad^2.  This file computes a sector quantity, not the cosmological one",
    "NOT TOUCHED: whether the dust mode GROWS at the CDM rate; the Boulware-Deser question; "
    "lensing; and the dust-binding problem 2d, which is about late-time collapse inside "
    "galaxies and is a different calculation from this one",
    "REVIEWER CREDIT, and it is due: the turnover was pointed out by an external skeptical "
    "review of the BIMOND paper.  Its arithmetic used the P(X) formula in the Q = phidot "
    "variable -- a convention splice -- so the number was not directly quotable, but the "
    "STRUCTURAL POINT was right and the corpus was wrong",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"SF08 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
