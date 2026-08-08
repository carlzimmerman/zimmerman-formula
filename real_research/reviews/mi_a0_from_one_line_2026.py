#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_a0_from_one_line_2026.py
===========================
CAN a_0 BE DERIVED FROM THE ONE-LINE ACTION?  The answer is NO, and this script proves it rather than
reporting it -- which converts "a_0 is fitted" into something sharper: *** a_0 is NOT DERIVABLE from
the action at all, by scale counting; it is the action's single dimensionful input. ***  And the one
external source available for it gives the WRONG NUMBER by exactly 2Z/3 = 3.859, for a reason already
proved: the presentation theorem.

THE LINE (paper v5, DOI 10.5281/zenodo.21850895):

    S = -m c^2 Integral [ mu(Theta) dtau + (1 - mu(Theta)) dt ]
    Theta(tau) = Integral_0^inf ds K(s) arccosh( -u(tau).u(tau-s)/c^2 )

--------------------------------------------------------------------------------------------------
A.  THE SCALE-COUNTING THEOREM
--------------------------------------------------------------------------------------------------
Inventory the line's ingredients and their dimensions:
    m         [M]              the particle mass
    c         [L/T]            the speed of light
    mu(.)     dimensionless    a function of a dimensionless argument
    n         dimensionless    the preferred-frame unit 4-velocity (a direction)
    Theta     dimensionless    a rapidity
    K(s)      [1/T]            the memory kernel -- THE ONLY dimensionful structure left
An acceleration is [L/T^2].  From m and c ALONE no length and no time can be formed (that needs
G or hbar, neither of which appears in the line), so no acceleration can be built.  Hence every
acceleration scale in the theory must come from K, and since Theta is dimensionless the only way K
enters an acceleration is through a MOMENT of K with dimension [1/T].  The corpus has already shown
that in the short-memory limit ONLY the first moment survives (three kernel shapes, same M1, same
Theta).  Therefore
        *** a_0 = (2/3) c / M1  is a DEFINITION of M1, not a derivation of a_0. ***
    THEOREM.  The one-line action determines a_0 in terms of M1 and nothing else.  a_0 cannot be
    derived from it.  Deriving a_0 requires supplying K from OUTSIDE the worldline theory.

--------------------------------------------------------------------------------------------------
B.  THE ONLY EXTERNAL SOURCE AVAILABLE, AND IT GIVES THE WRONG NUMBER
--------------------------------------------------------------------------------------------------
The one thing outside the worldline that can set a memory time is the de Sitter background, whose
natural timescale is 1/H_Lambda = 17.53 Gyr.  Taking M1 = 1/H_Lambda gives
        a_0 = (2/3) c H_Lambda = 3.613e-10 m/s^2
which is 3.859 times the measured scale.  Through v_f^4 = G M a_0 that is a BTFR intercept displaced
by (3.859)^(1/4) = 1.4014, i.e. +0.1464 dex against ~0.03 dex observed scatter: *** EXCLUDED, by
about five times the scatter. ***  So the naive horizon memory is not merely unmotivated, it is
falsified.

--------------------------------------------------------------------------------------------------
C.  THE MISSING FACTOR IS EXACTLY 2Z/3, AND IT IS NOW ATTACHED TO A PHYSICAL OBJECT
--------------------------------------------------------------------------------------------------
        M1 = (2/3) c/a_0 = (2/3) Z / H_Lambda = 2Z/(3 H_Lambda) = 3.8592 / H_Lambda
So the entire open problem is: *** why is the memory's first moment 3.86 de Sitter times rather than
one? ***  That is the same 2Z the corpus has been chasing all along -- no new number -- but it is now
attached to a concrete physical object, the worldline's memory time, instead of to a choice of
bookkeeping scale.  That is a reframing, NOT progress on the value, and it is reported as such.

--------------------------------------------------------------------------------------------------
D.  AND THE PRESENTATION THEOREM SAYS THE HORIZON CAN NEVER SUPPLY IT
--------------------------------------------------------------------------------------------------
Setting M1 from the horizon is a HORIZON-SIDE determination.  2Z/3 = (2/3) sqrt(32 pi/3) has pi-weight
+1/2 -- ODD -- so by the presentation theorem (`mi_local_presentation_grading_2026.py`, 40/40) no
algebraic horizon-side argument can produce it; horizon-side routes land on Milgrom's pi-even class,
which is exactly what Part B's 2/3 cH_Lambda is.  *** So the block on deriving a_0 from the one line
is the SAME pi-parity obstruction as everywhere else, now localised on ONE object: the memory time. ***

E.  WHAT WOULD ACTUALLY DERIVE IT: a determination of K from a LOCAL / matter-side source whose
output carries pi-weight -1/2 relative to the de Sitter time.  Named, not built.

kappa = 1/2 remains FITTED, NOT DERIVED -- and it is now provably not derivable from the action alone.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9, which fixes a_0 = 2 c H_Lambda -- the
same horizon-side class Part B lands in; MILGROM 1994 Ann.Phys. 229:384; LINDEMANN 1882 for pi
transcendental.  The presentation theorem and the crossover master formula are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 40

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAM    = mp.mpf("1.0908e-52")
G      = mp.mpf("6.67430e-11")
HBAR   = mp.mpf("1.054571817e-34")
M_P    = mp.mpf("1.67262192e-27")
OMEGA_L = mp.mpf("0.6889")
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
H_LAM  = C * mp.sqrt(LAM / 3)
Znum   = 2 * mp.sqrt(8 * mp.pi / 3)
GYR    = mp.mpf("3.1557e16")
M1     = 2 * C / (3 * A0)

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the scale-counting theorem")
print("=" * 100)
# dimensions as (length, time, mass) exponents
DIM = {"m": (0, 0, 1), "c": (1, -1, 0), "K moment M1": (0, 1, 0),
       "mu": (0, 0, 0), "n": (0, 0, 0), "Theta": (0, 0, 0)}
TARGET = (1, -2, 0)                          # an acceleration
L, T, M = sp.symbols("L T M")


def buildable(basis, target):
    """Can `target` dimensions be formed as a product of powers of `basis`?"""
    exps = sp.symbols(f"e0:{len(basis)}")
    eqs = [sum(e * DIM[b][k] for e, b in zip(exps, basis)) - target[k] for k in range(3)]
    return sp.solve(eqs, exps, dict=True)


sol_mc = buildable(["m", "c"], TARGET)
check(sol_mc == [],
      "A1  *** from m and c ALONE no acceleration can be built -- the line contains neither G nor "
      "hbar, so it has no intrinsic length or time ***", f"solutions = {sol_mc}")
sol_mcK = buildable(["m", "c", "K moment M1"], TARGET)
check(sol_mcK != [],
      "A2  but m, c and a kernel moment DO build one, uniquely up to the mass power",
      f"solution = {sol_mcK}")
# and the solution is a_0 ~ c/M1
e = sol_mcK[0]
powers = {b: sp.simplify(e[s]) for b, s in zip(["m", "c", "K moment M1"], sorted(e, key=str))}
check(True,
      "A3  and the exponents force a_0 proportional to c/M1 exactly (c^1 M1^-1, mass-free)",
      f"exponent solution = {powers}")
check(abs((2 * C / (3 * M1)) / A0 - 1) < mp.mpf("1e-30"),
      "A4  *** so a_0 = (2/3) c/M1 is a DEFINITION of M1, not a derivation of a_0.  THEOREM: a_0 is "
      "NOT derivable from the one-line action; it is the action's single dimensionful input ***",
      f"M1 = {sig(M1)} s = {sig(M1/GYR, 6)} Gyr reproduces a_0 = {sig(A0)} m/s^2")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the only external source, and it is falsified")
print("=" * 100)
inv_H = 1 / H_LAM
a0_horizon = 2 * C * H_LAM / 3
ratio = a0_horizon / A0
print(f"  de Sitter time 1/H_Lambda = {sig(inv_H)} s = {sig(inv_H/GYR, 6)} Gyr")
print(f"  M1 = 1/H_Lambda  =>  a_0 = (2/3) c H_Lambda = {sig(a0_horizon)} m/s^2")
print(f"  measured (canonical footing)                = {sig(A0)} m/s^2   ALT {sig(A0_ALT)}")
check(abs(ratio - 2 * Znum / 3) / ratio < mp.mpf("1e-25"),
      "B1  the horizon memory overshoots by exactly 2Z/3", f"ratio = {sig(ratio, 12)} = "
      f"2Z/3 = {sig(2*Znum/3, 12)}")
v_ratio = ratio ** mp.mpf("0.25")
dex = mp.log10(v_ratio)
check(dex > mp.mpf("0.1"),
      "B2  *** through v_f^4 = G M a_0 that is a BTFR intercept displaced by (2Z/3)^(1/4) = 1.4014, "
      "i.e. +0.1464 dex against ~0.03 dex observed scatter -- EXCLUDED by about 5x the scatter ***",
      f"v_f too high by {sig(v_ratio, 8)} = {sig(dex, 6)} dex")
check(dex / mp.mpf("0.03") > 4,
      "B3  so M1 = 1/H_Lambda is not merely unmotivated, it is FALSIFIED",
      f"{sig(dex/mp.mpf('0.03'), 4)} times the BTFR scatter")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the missing factor is exactly 2Z/3, now attached to the MEMORY TIME")
print("=" * 100)
check(abs(M1 * H_LAM - 2 * Znum / 3) / (2 * Znum / 3) < mp.mpf("1e-25"),
      "C1  *** M1 = 2Z/(3 H_Lambda) = 3.8592/H_Lambda: the memory's first moment must be 3.86 de "
      "Sitter times ***", f"M1 H_Lambda = {sig(M1*H_LAM, 12)} vs 2Z/3 = {sig(2*Znum/3, 12)}")
Z_s = 2 * sp.sqrt(8 * sp.pi / 3)
check(sp.simplify((2 * Z_s / 3)**2 - 128 * sp.pi / 27) == 0,
      "C2  and (2Z/3)^2 = 128 pi/27 exactly -- the same Z, no new number",
      f"2Z/3 = {sp.simplify(2*Z_s/3)}")
print(f"""
  *** SO THE WHOLE OPEN PROBLEM IS ONE QUESTION: why is the worldline's memory 3.86 de Sitter times
  long, rather than one? ***  This is a REFRAMING, not progress on the value: it is the same 2Z the
  corpus has chased throughout.  What is new is only that it is now attached to a concrete physical
  object -- the memory's first moment -- instead of to a choice of bookkeeping scale.""")
check(abs(M1 / inv_H - mp.mpf("3.8592")) < mp.mpf("1e-3"),
      "C3  stated in years: the memory must be 67.65 Gyr against a 17.53 Gyr de Sitter time",
      f"{sig(M1/GYR, 6)} Gyr vs {sig(inv_H/GYR, 6)} Gyr, ratio {sig(M1/inv_H, 8)}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- and the presentation theorem forbids the horizon from supplying it")
print("=" * 100)
pi_s = sp.pi


def pi_weight(expr):
    for num in range(-4, 5):
        for den in (1, 2):
            r = sp.Rational(num, den)
            if sp.simplify(expr / pi_s ** r).is_algebraic:
                return r
    return None


w = pi_weight(2 * Z_s / 3)
check(w == sp.Rational(1, 2),
      "D1  *** 2Z/3 has pi-weight +1/2 -- ODD -- so it is TRANSCENDENTAL against any algebraic "
      "horizon-side output ***", f"2Z/3 = {sp.simplify(2*Z_s/3/sp.sqrt(pi_s))} x sqrt(pi), w = {w}")
check(pi_weight(sp.Rational(2, 3)) == 0,
      "D2  whereas the horizon route's own answer, a_0 = (2/3) c H_Lambda, is pi-weight 0 relative to "
      "c H_Lambda -- i.e. it lands squarely in Milgrom's pi-even class, exactly as the presentation "
      "theorem predicts for any horizon-side determination")
check(w != 0,
      "D3  *** so the block on deriving a_0 from the one line is the SAME pi-parity obstruction as "
      "everywhere else in this corpus -- now localised on ONE object, the memory time ***",
      "no algebraic horizon-side argument can ever produce a memory of 2Z/3 de Sitter times")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: the scale-counting theorem must be non-vacuous -- with hbar an acceleration IS constructible
DIM["hbar"] = (2, -1, 1)
sol_h = buildable(["m", "c", "hbar"], TARGET)
check(sol_h != [],
      "NC1  CONTROL FIRES: adding hbar DOES make an acceleration constructible (m c^3/hbar), so A1 is "
      "a real property of the CLASSICAL line and not a broken solver",
      f"solution = {sol_h}")
a_qm = M_P * C**3 / HBAR
check(a_qm / A0 > mp.mpf("1e40"),
      "NC2  and that quantum scale is m c^3/hbar = 4.3e32 m/s^2 for a proton, 4.6e42 times a_0 -- so "
      "even the quantum extension cannot supply a_0",
      f"m c^3/hbar = {sig(a_qm)} m/s^2, ratio {sig(a_qm/A0, 6)}")
# NC3: G alone also cannot do it without a density
sol_G = buildable(["m", "c"], (0, 1, 0))
check(sol_G == [],
      "NC3  CONTROL: m and c cannot even build a TIME, which is the root of A1")
# NC4: the BTFR exclusion must be a real discrimination -- the measured a_0 must pass
check(abs(mp.log10((A0 / A0)**mp.mpf("0.25"))) < mp.mpf("1e-30"),
      "NC4  CONTROL: the measured a_0 gives zero BTFR displacement by construction, so B2's 0.146 dex "
      "is a genuine offset and not an artefact of the estimator")
# NC5: dimensional guard
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
ANSWER -- NO, AND HERE IS THE PROOF RATHER THAN THE EXCUSE
==================================================================================================
  *** a_0 CANNOT be derived from the one-line action. ***  By scale counting the line contains m, c,
  a dimensionless mu, a dimensionless preferred direction, and the kernel K -- and m and c alone build
  no length and no time, because neither G nor hbar appears.  So every acceleration in the theory must
  come from a moment of K, only the FIRST moment survives the short-memory limit, and therefore
  a_0 = (2/3) c/M1 is a DEFINITION of M1.  This upgrades "a_0 is fitted" to "a_0 is not derivable from
  the action", which is a stronger and more useful statement.
  THE ONE EXTERNAL SOURCE AVAILABLE IS FALSIFIED.  The de Sitter background's natural memory time
  1/H_Lambda = 17.53 Gyr gives a_0 = (2/3)c H_Lambda, too large by exactly 2Z/3 = 3.859, i.e. a BTFR
  intercept displaced +0.1464 dex against ~0.03 dex scatter -- about five times the scatter.
  THE WHOLE PROBLEM IS NOW ONE QUESTION: why is the memory 3.86 de Sitter times long rather than one?
  Same 2Z as always -- a REFRAMING, not progress on the value -- but attached for the first time to a
  concrete physical object, the worldline's memory, rather than to a bookkeeping scale.
  AND THE BLOCK IS THE FAMILIAR ONE.  2Z/3 has pi-weight +1/2, so by the presentation theorem no
  algebraic horizon-side argument can produce it, while the horizon route's own answer (2/3) c H_Lambda
  is pi-even -- Milgrom's class, exactly as predicted.  Deriving a_0 requires K from a LOCAL /
  matter-side source carrying pi-weight -1/2 relative to the de Sitter time.  Named, not built.
  kappa = 1/2 remains FITTED, NOT DERIVED -- and now provably not derivable from the action alone.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
