#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage43_kappa_reduction_one_factor_2026.py
==========================================
"WHY 1/(32 pi)" IS NOT A NEW QUESTION.  It is "why kappa = 1/2" solved for epsilon_tot.  Four
apparently-separate open items in the corpus are ONE unknown, and that unknown is a FACTOR OF 2.

This stage does not derive kappa.  It shortens the question, retires a misleading phrasing, and
identifies a circularity that may explain why the epsilon_tot route always "nearly" works.

--------------------------------------------------------------------------------------------------
THE REDUCTION
--------------------------------------------------------------------------------------------------
The Friedmann equation already supplies the only pi in the problem:
        H_Lambda = sqrt(8 pi G rho_Lambda / 3)   =>   H_Lambda = sqrt(8pi/3) sqrt(G rho_Lambda)
so the committed a_0 = c H_Lambda / Z becomes
        a_0 = [ sqrt(8pi/3) / Z ] c sqrt(G rho_Lambda)  ==  kappa c sqrt(G rho_Lambda)
        *** kappa = sqrt(8pi/3) / Z,  and with Z = sqrt(32pi/3) this is EXACTLY 1/2 ***
The pi CANCELS -- which is the precise reason the corpus records "kappa is pi-free; sqrt(pi)
constrains Z, not kappa".  So:
        kappa = 1/2   <=>   Z = 2 sqrt(8pi/3)   <=>   Z is exactly TWICE the Friedmann factor.

--------------------------------------------------------------------------------------------------
AND THE epsilon_tot FRAMING ADDS NOTHING
--------------------------------------------------------------------------------------------------
The crossover master formula is kappa^2 = 8 pi epsilon_tot (exact, graviton-bath CTP, with
S_dS G H^2 = pi cancelling the Planck suppression).  Solve it at kappa = 1/2:
        epsilon_tot = kappa^2/(8 pi) = 1/(32 pi)
The 8 pi is carried over from the formula's own left-hand side, and the 4 in 32 pi is literally
1/kappa^2 = 2^2.  *** So "why 1/(32 pi)" contains no information beyond "why 1/2".  It is the same
unknown re-expressed, and the phrasing made the problem look deeper than it is. ***

FOUR NAMES, ONE UNKNOWN -- fixing any one fixes all four:
        kappa = 1/2  ·  Z/sqrt(8pi/3) = 2  ·  32 pi epsilon_tot = 1  ·  a_0/[c sqrt(G rho_L)] = 1/2

--------------------------------------------------------------------------------------------------
THE CIRCULARITY THIS EXPOSES, which is the actually useful finding
--------------------------------------------------------------------------------------------------
32 pi is the STANDARD canonical normalisation of the graviton: g_munu = eta_munu + sqrt(32 pi G) h_munu
is what makes h's kinetic term canonical.  If epsilon_tot is defined through that normalisation, then
epsilon_tot = 1/(32 pi) is a CONVENTION IDENTITY, not a prediction -- and the derivation would be
circular by construction.  That would explain, at once:
  (i)  why the epsilon_tot computation always lands suspiciously close to the wanted answer;
  (ii) why the TT-gauge choice kills it -- the five variants differ in how the 2 physical polarisations
       are counted, i.e. in exactly the factor under dispute; and
  (iii) why those five variants span 161.6x rather than clustering.
So the sharp question is not "compute epsilon_tot better".  It is: *is the 32 pi in the crossover
formula an input or an output?*  That is checkable, and it should be checked before any further effort
is spent on this route.

--------------------------------------------------------------------------------------------------
AND THE REASON NOT TO PUSH HARDER, stated against interest
--------------------------------------------------------------------------------------------------
The data do NOT require kappa = 1/2.  The distance-free measurement is kappa = 0.551 +/- 0.043, which
puts 1/2 at 1.19 sigma, and four candidate values sit within 2 sigma.  A derivation that lands exactly
on 1/2 would therefore be deriving a number the data have not singled out -- and building a derivation
toward a preferred number is the same error as evaluating K at a convenient background point.  Seven
routes have already been spent on this one factor (dS-Unruh, crossover, epsilon_tot, the 2Z ratio,
pi-content, category search, E8) and every one is recorded closed or near-miss.
"""

import sys

import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))
    return True


print(__doc__)

pi = sp.pi
F = sp.sqrt(8 * pi / 3)            # the Friedmann factor
Z = sp.sqrt(32 * pi / 3)           # the committed Z
KAPPA_MEAS, KAPPA_ERR = 0.551, 0.043

print("=" * 100)
print("PART A -- the reduction")
print("=" * 100)

kappa = sp.simplify(F / Z)
check(kappa == sp.Rational(1, 2),
      f"A1  kappa = sqrt(8pi/3)/Z = {kappa} EXACTLY, because H_Lambda = sqrt(8pi/3) sqrt(G rho_Lambda) "
      f"means a_0 = cH_Lambda/Z already IS kappa c sqrt(G rho_Lambda)",
      f"numerically sqrt(8pi/3) = {float(F):.6f}, Z = {float(Z):.6f}, ratio = {float(kappa):.6f}")

check(sp.simplify(2 * F - Z) == 0,
      f"A2  so kappa = 1/2 is IDENTICALLY the statement Z = 2 sqrt(8pi/3): Z is exactly TWICE the "
      f"Friedmann factor.  2 sqrt(8pi/3) = {float(2*F):.6f} = Z",
      "the whole content of the coefficient claim is one factor of 2")

check(sp.simplify(sp.diff(kappa, sp.Symbol('x'))) == 0 and pi not in sp.simplify(kappa).atoms(sp.NumberSymbol),
      f"A3  and the pi CANCELS between numerator and denominator, so kappa is pi-FREE -- which is exactly "
      f"why the corpus records that sqrt(pi) constrains Z and not kappa",
      "any attempt to derive kappa from a pi-counting argument is therefore structurally hopeless")

print()
print("=" * 100)
print("PART B -- the epsilon_tot framing carries no extra information")
print("=" * 100)

e = sp.symbols("e", positive=True)
eps = sp.solve(sp.Eq(kappa ** 2, 8 * pi * e), e)[0]
check(sp.simplify(eps - 1 / (32 * pi)) == 0,
      f"B1  the crossover formula kappa^2 = 8 pi epsilon_tot, solved at kappa = 1/2, gives "
      f"epsilon_tot = {eps} = {float(eps):.8f}",
      "this is a solve, not a derivation -- kappa went in and epsilon_tot came out")

check(sp.simplify(32 * pi - 4 * (8 * pi)) == 0,
      f"B2  *** AND THE 4 IN 32 pi IS LITERALLY 1/kappa^2 = 2^2.  The 8 pi is carried over from the "
      f"formula's own left-hand side.  So 'why 1/(32 pi)' contains NO information beyond 'why 1/2' ***",
      "the phrasing made the open problem look deeper than it is; it should be retired")

info("B3  FOUR NAMES, ONE UNKNOWN -- fixing any one fixes all four:  kappa = 1/2  ·  Z/sqrt(8pi/3) = 2  "
     "·  32 pi epsilon_tot = 1  ·  a_0/[c sqrt(G rho_Lambda)] = 1/2.  The corpus has been carrying these "
     "as separate open items.")

print()
print("=" * 100)
print("PART C -- the circularity this exposes, and the one question worth asking next")
print("=" * 100)

info("C1  32 pi is the STANDARD canonical graviton normalisation: g_munu = eta_munu + sqrt(32 pi G) h_munu "
     "is what makes h's kinetic term canonical.  If epsilon_tot is defined through that normalisation, "
     "epsilon_tot = 1/(32 pi) is a CONVENTION IDENTITY and the crossover derivation is circular by "
     "construction.")

info("C2  that single hypothesis would explain three recorded facts at once: (i) why the epsilon_tot "
     "computation always lands suspiciously near the wanted value; (ii) why the TT-gauge choice kills it, "
     "since the five variants differ precisely in how the 2 physical polarisations are counted -- the "
     "factor under dispute; and (iii) why those variants span 161.6x instead of clustering.")

info("C3  *** SO THE SHARP NEXT QUESTION IS NOT 'compute epsilon_tot better'.  IT IS: is the 32 pi in the "
     "crossover formula an INPUT or an OUTPUT?  That is a short, checkable question, and it should be "
     "settled before any further effort goes into this route. ***")

print()
print("=" * 100)
print("PART D -- and the argument against pushing harder, stated against interest")
print("=" * 100)

sig = abs(KAPPA_MEAS - 0.5) / KAPPA_ERR
check(sig < 2.0,
      f"D1  THE DATA DO NOT REQUIRE kappa = 1/2.  The distance-free measurement is "
      f"{KAPPA_MEAS} +/- {KAPPA_ERR}, which puts 1/2 at {sig:.2f} sigma -- consistent, but not selected.  "
      f"Four candidate values sit within 2 sigma",
      "so a derivation landing exactly on 1/2 would be deriving a number the data have not singled out")

info("D2  and that is the same error as evaluating K at a convenient background point: building a "
     "derivation TOWARD a preferred number.  Seven routes have already been spent on this one factor "
     "(dS-Unruh, crossover, epsilon_tot, the 2Z ratio, pi-content, category search, E8) and every one is "
     "recorded closed or near-miss.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THERE IS NOTHING LEFT TO FINISH IN THE "1/(32 pi)" DIRECTION, BECAUSE IT IS CIRCULAR.

  1. THE REDUCTION.  H_Lambda = sqrt(8pi/3) sqrt(G rho_Lambda) means a_0 = c H_Lambda/Z is ALREADY
     kappa c sqrt(G rho_Lambda) with kappa = sqrt(8pi/3)/Z.  At Z = sqrt(32pi/3) that is exactly 1/2,
     with the pi cancelling.  So kappa = 1/2 IS the statement Z = 2 sqrt(8pi/3):
        *** Z is exactly TWICE the Friedmann factor, and the factor 2 is the entire open question. ***

  2. THE epsilon_tot FRAMING IS A RESTATEMENT.  kappa^2 = 8 pi epsilon_tot solved at kappa = 1/2 returns
     epsilon_tot = 1/(32 pi); the 8 pi comes from the formula's own left side and the 4 in 32 pi is
     1/kappa^2 = 2^2.  "Why 1/(32 pi)" should be retired as a phrasing -- it made one factor of 2 look
     like a deep normalisation problem.

  3. FOUR OPEN ITEMS COLLAPSE TO ONE.  kappa = 1/2, Z/sqrt(8pi/3) = 2, 32 pi epsilon_tot = 1, and
     a_0/[c sqrt(G rho_Lambda)] = 1/2 are the SAME unknown.  The corpus was carrying them separately.

  4. THE USEFUL FINDING IS A SUSPECTED CIRCULARITY.  32 pi is the standard canonical graviton
     normalisation (g = eta + sqrt(32 pi G) h).  If epsilon_tot is defined through it, then
     epsilon_tot = 1/(32 pi) is a convention identity -- which would explain the persistent near-miss,
     the TT-gauge kill, and the 161.6x spread of the five variants in one stroke.  THE NEXT QUESTION IS
     WHETHER THE 32 pi IS AN INPUT OR AN OUTPUT, and it is short.

  5. AND THE CASE FOR STOPPING, against interest: kappa is MEASURED at {KAPPA_MEAS} +/- {KAPPA_ERR}, so 1/2 sits
     {sig:.2f} sigma away and four candidates lie within 2 sigma.  Deriving exactly 1/2 may be deriving the
     wrong number.  Seven routes are already spent.  The honest position is that kappa is a MEASURED
     coefficient of the framework, stated as such -- which is what the published papers already say.

  NOT CLAIMED: that kappa is underivable.  Claimed: that the "1/(32 pi)" formulation is circular, that
  the open content is one factor of 2, and that the next step is a circularity check rather than a
  harder computation.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
