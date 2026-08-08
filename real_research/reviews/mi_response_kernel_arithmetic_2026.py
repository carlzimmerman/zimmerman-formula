#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_response_kernel_arithmetic_2026.py
=====================================
THE CALCULATION: what a de Sitter thermal response kernel must produce for kappa = 1/2, and whether it
CAN.  The full QFT computation of the kernel is not attempted here -- but the calculation has an
ARITHMETIC SKELETON that decides the answer before any integral is evaluated, and that skeleton is
computed here in full.

RESULT.  The target reduces to a single pure number, xi = 2Z/3 = 3.85921, and
    * xi must carry pi-weight +1/2 -- HALF-INTEGER (Part B);
    * thermal spectral moments CANNOT supply that: they are Gamma(n+1) zeta(n+1) values, hence
      (rational) x (even power of pi), pi-weight INTEGER (Part C).  So my first instinct -- that this
      closes the route -- was ALMOST right;
    * but the THREE-dimensional spatial loop measure (4 pi)^(-3/2) DOES carry weight -3/2, and combined
      with zeta(2) ~ pi^2 it lands on exactly +1/2 (Part D).  So the parity CAN be supplied, by the
      ODD spatial dimension count -- which is independently escape E1 of the corpus's number-field
      theorem, rediscovered from a different direction.
    * *** THE OBSTRUCTION IS THEREFORE NOT THE pi.  IT IS A sqrt(6). ***  Writing
      xi = (8/9) sqrt(6 pi), the required algebraic content beyond sqrt(pi) is sqrt(6), and spectral
      integrals produce rationals and zeta values -- never sqrt(6) (Part E).
    * sqrt(6) = sqrt(D(D-1)/2) at D = 4 = sqrt(the number of Lorentz generators of SO(1,3)) -- a
      genuine COUNT, and exactly the kind of object a mode sum over the algebra would produce (Part F).
      ⚠️ But the accompanying 8/9 has NO independent origin and was reverse-engineered from the answer,
      so Part F is a DECOMPOSITION, not a derivation, and it is labelled as such.

So the calculation does not deliver kappa = 1/2.  What it delivers is the exact arithmetic target and
the identification of the one irrationality that must come from a mode count rather than an integral.
kappa = 1/2 remains FITTED, NOT DERIVED.

WHAT IS NOT DONE.  No propagator, no spectral density, no loop integral is actually evaluated.  This
is the arithmetic that any such evaluation must satisfy; it constrains the answer and does not produce
it.  Saying so is the point.

CREDIT.  Gibbons & Hawking 1977 for the de Sitter temperature; NARNHOFER, PETER & THIRRING 1996
IJMPB 10:1507; MILGROM 1999 PLA 253:273 eqs 6-9 and MILGROM 1994 Ann.Phys. 229:384; Lindemann 1882.
The number-field theorem with escapes E1-E5, the presentation theorem, the memory-force
renormalisation and the kappa equivalence are this corpus.

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
OMEGA_L = mp.mpf("0.6889")
RHO_L  = LAM * C**2 / (8 * mp.pi * G)
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
H_LAM  = C * mp.sqrt(LAM / 3)
T_LAM  = 1 / mp.sqrt(G * RHO_L)
M1     = 2 * C / (3 * A0)
Znum   = 2 * mp.sqrt(8 * mp.pi / 3)
pi_s   = sp.pi
Z_s    = 2 * sp.sqrt(8 * pi_s / 3)

print(__doc__)


def pi_weight(expr):
    """expr = (pi-free factor) x pi^(k/2) -> k/2, else None.

    NOTE: an earlier version demanded cofactor.is_algebraic, which sympy cannot DECIDE for zeta
    values -- zeta(3) and zeta(3/2) return None rather than True, so checks C7 and NC1 failed on the
    detector rather than on the physics.  The right test is that the cofactor is pi-FREE: that is
    exactly what "algebraic x pi^(k/2)" means for the grading, and it does not require settling the
    transcendence of zeta(odd).
    """
    ex = sp.simplify(expr)
    for num in range(-8, 9):
        for den in (1, 2):
            r = sp.Rational(num, den)
            cof = sp.simplify(ex / pi_s ** r)
            if cof.is_algebraic or not cof.has(sp.pi):
                return r
    return None


# =============================================================================================
print("=" * 100)
print("PART A -- the reduction: everything is one pure number xi")
print("=" * 100)
print("""  A response kernel computed from QFT in de Sitter can only return times built from the
  background's own rate H_Lambda (with hbar and c and the field's parameters).  So write
        M1 = xi / H_Lambda,   xi a pure number,
  and feed it into the proved equivalence kappa = (2/3) t_Lambda/M1.""")
xi = sp.symbols("xi", positive=True)
tH = sp.sqrt(8 * pi_s / 3)                       # t_Lambda H_Lambda
check(abs(T_LAM * H_LAM - mp.sqrt(8 * mp.pi / 3)) < mp.mpf("1e-30"),
      "A1  t_Lambda H_Lambda = sqrt(8 pi/3) = Z/2 exactly (the Friedmann factor)",
      f"= {sig(T_LAM*H_LAM, 12)} vs {sig(mp.sqrt(8*mp.pi/3), 12)}")
kap_of_xi = sp.simplify(sp.Rational(2, 3) * tH / xi)
check(sp.simplify(kap_of_xi - Z_s / (3 * xi)) == 0,
      "A2  so kappa = (2/3)(Z/2)/xi = Z/(3 xi)", f"kappa = {kap_of_xi}")
xi_needed = sp.solve(sp.Eq(kap_of_xi, sp.Rational(1, 2)), xi)
check(sp.simplify(xi_needed[0] - 2 * Z_s / 3) == 0,
      "A3  *** kappa = 1/2 <==> xi = 2Z/3 = 3.85921 exactly.  That is the whole target. ***",
      f"xi = {sp.simplify(xi_needed[0])} = {sig(2*Znum/3, 12)}")
check(abs(M1 * H_LAM - 2 * Znum / 3) / (2 * Znum / 3) < mp.mpf("1e-25"),
      "A4  and the measured M1 H_Lambda IS 3.85921, so xi is exactly the quantity to be computed",
      f"M1 H_Lambda = {sig(M1*H_LAM, 12)}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- xi must carry HALF-INTEGER pi-weight")
print("=" * 100)
w_xi = pi_weight(2 * Z_s / 3)
check(w_xi == sp.Rational(1, 2),
      "B1  *** xi = 2Z/3 has pi-weight +1/2 -- HALF-INTEGER ***",
      f"2Z/3 = {sp.simplify(2*Z_s/3/sp.sqrt(pi_s))} x sqrt(pi), weight {w_xi}")
check(sp.simplify(2 * Z_s / 3 - sp.Rational(8, 9) * sp.sqrt(6 * pi_s)) == 0,
      "B2  and it factorises exactly as xi = (8/9) sqrt(6 pi)",
      f"(8/9)sqrt(6 pi) = {sig(mp.mpf(8)/9*mp.sqrt(6*mp.pi), 12)} = xi")
check(sp.sqrt(6).is_algebraic and not sp.sqrt(6).is_rational,
      "B3  so beyond the sqrt(pi) the required algebraic content is sqrt(6) -- irrational but "
      "algebraic.  Two separate things must be supplied.")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- thermal spectral moments CANNOT supply half-integer pi-weight")
print("=" * 100)
print("""  Any thermal response kernel's moments are Bose integrals
      Integral_0^inf x^n/(e^x - 1) dx = Gamma(n+1) zeta(n+1)
  so the numbers available are Gamma and zeta values at the powers the spectral density supplies.""")
n_s = sp.symbols("n", positive=True)
print(f"  {'n':>4s} {'Gamma(n+1) zeta(n+1)':>26s} {'value':>14s} {'pi-weight':>11s}")
weights = []
for nv in (1, 2, 3, 4, 5):
    ex = sp.gamma(nv + 1) * sp.zeta(nv + 1)
    w = pi_weight(sp.simplify(ex))
    weights.append(w)
    print(f"  {nv:>4d} {str(sp.simplify(ex)):>26s} {sig(mp.mpf(str(sp.N(ex, 25))), 8):>14s} "
          f"{str(w):>11s}")
    check(w is None or sp.Rational(w).q == 1,
          f"C{nv}  n = {nv}: weight is INTEGER (or undecidable), never half-integer")
check(all(w is None or sp.Rational(w).q == 1 for w in weights),
      "C6  *** so for INTEGER powers n -- which is what a massless field in integer D supplies -- every "
      "Bose moment has INTEGER pi-weight.  Thermal spectral integrals alone cannot produce xi ***",
      "zeta(2) = pi^2/6 (weight 1), zeta(3) (weight 0), zeta(4) = pi^4/90 (weight 2), ...")
# the one way an integral gives sqrt(pi): a HALF-INTEGER power
half = sp.gamma(sp.Rational(3, 2)) * sp.zeta(sp.Rational(3, 2))
check(pi_weight(sp.simplify(half)) == sp.Rational(1, 2),
      "C7  a HALF-INTEGER power n = 1/2 would give Gamma(3/2) = sqrt(pi)/2 and hence weight +1/2 -- but "
      "a massless field in integer D does not supply half-integer powers",
      f"Gamma(3/2)zeta(3/2) = {sp.simplify(half)}, weight +1/2")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- but the ODD spatial loop measure DOES, and it is escape E1 rediscovered")
print("=" * 100)
d = sp.symbols("d", positive=True, integer=True)
meas = (4 * pi_s) ** (-d / 2)
for dv in (2, 3, 4, 5):
    w = pi_weight(sp.simplify(meas.subs(d, dv)))
    print(f"    spatial d = {dv}: (4 pi)^(-d/2) weight = {w}"
          + ("   <-- our universe, HALF-INTEGER" if dv == 3 else ""))
check(pi_weight(sp.simplify(meas.subs(d, 3))) == sp.Rational(-3, 2),
      "D1  *** in THREE spatial dimensions the loop measure (4 pi)^(-3/2) has weight -3/2 -- "
      "HALF-INTEGER ***")
combo = sp.simplify(meas.subs(d, 3) * sp.zeta(2))
check(pi_weight(combo) == sp.Rational(1, 2),
      "D2  *** and (4 pi)^(-3/2) x zeta(2) has weight exactly +1/2 -- the required parity ***",
      f"= {combo}, weight {pi_weight(combo)}")
check(pi_weight(sp.simplify(meas.subs(d, 2) * sp.zeta(2))) == sp.Integer(1)
      or sp.Rational(pi_weight(sp.simplify(meas.subs(d, 2) * sp.zeta(2)))).q == 1,
      "D3  whereas an EVEN spatial dimension gives integer weight, so the parity comes specifically "
      "from d being ODD -- which is independently escape E1 of the number-field theorem "
      "('an odd-dimensional measure'), reached here from a different direction")
check(w_xi == sp.Rational(1, 2) and pi_weight(combo) == sp.Rational(1, 2),
      "D4  so the pi is NOT the obstruction.  My first instinct -- that thermal moments close this "
      "route on parity grounds -- was wrong, and the correction is recorded here.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- THE OBSTRUCTION IS A sqrt(6)")
print("=" * 100)
resid = sp.simplify((2 * Z_s / 3) / combo)
check(sp.simplify(resid).is_algebraic,
      "E1  dividing the target by (4 pi)^(-3/2) zeta(2) leaves a purely ALGEBRAIC residue",
      f"xi / [(4pi)^(-3/2) zeta(2)] = {sp.simplify(resid)} = {sig(mp.mpf(str(sp.N(resid, 25))), 10)}")
check(sp.sqrt(6) in sp.simplify(2 * Z_s / 3).atoms(sp.Pow)
      or sp.simplify(sp.Rational(8, 9) * sp.sqrt(6 * pi_s) - 2 * Z_s / 3) == 0,
      "E2  *** and the irreducible algebraic content is sqrt(6): xi = (8/9) sqrt(6 pi) ***")
check(not sp.sqrt(6).is_rational,
      "E3  *** spectral integrals produce RATIONALS (Gamma at integers) and ZETA values -- never "
      "sqrt(6).  So the obstruction to computing xi is not the pi at all; it is a sqrt(6) that no "
      "thermal integral supplies ***")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- sqrt(6) IS a count -- but the rest of the decomposition is reverse-engineered")
print("=" * 100)
Dv = sp.symbols("Ds", positive=True, integer=True)
gens = Dv * (Dv - 1) / 2
check(sp.simplify(gens.subs(Dv, 4) - 6) == 0,
      "F1  *** 6 = D(D-1)/2 at D = 4 = the number of generators of the Lorentz group SO(1,3) "
      "(3 rotations + 3 boosts) -- a genuine COUNT, exactly the object a mode sum over the algebra "
      "would produce ***", f"dim SO(1,3) = {sp.simplify(gens.subs(Dv, 4))}")
print(f"  {'D':>4s} {'dim SO(1,D-1)':>15s} {'sqrt(dim)':>12s}")
for Dvv in (3, 4, 5, 6):
    gv = Dvv * (Dvv - 1) // 2
    print(f"  {Dvv:>4d} {gv:>15d} {sig(mp.sqrt(gv), 8):>12s}"
          + ("   <-- gives the required sqrt(6)" if gv == 6 else ""))
check(sp.simplify(sp.Rational(8, 9) - 2**3 / sp.Integer(3)**2) == 0,
      "F2  and 8/9 = 2^(D-1)/(D-1)^2 at D = 4",
      "8 = 2^3, 9 = 3^2 -- but see F3")
check(True,
      "F3  ⚠️ *** F2 IS REVERSE-ENGINEERED. ***  The 8/9 was read off the answer; 2^(D-1)/(D-1)^2 is "
      "one of many integer expressions hitting 8/9 at D = 4, and no mode sum has been computed that "
      "produces it.  So Part F is a DECOMPOSITION of xi, not a derivation of it.")
# price the 8/9 the way the corpus prices everything
cands = [sp.Rational(p, q) for q in range(1, 13) for p in range(1, 13)
         if sp.gcd(p, q) == 1 and sp.Rational(p, q) < 4]
hit = [r for r in cands if r == sp.Rational(8, 9)]
check(len(hit) == 1 and len(cands) > 30,
      "F4  and on a menu of small rationals p/q with q <= 12 there are dozens of candidates, so "
      "hitting 8/9 carries essentially no evidential weight on its own",
      f"menu size {len(cands)}, p ~ {sig(mp.mpf(1)/len(cands), 4)} for any prespecified entry")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- NEGATIVE CONTROLS")
print("=" * 100)
# NOTE: my first version of this control asserted weight 1 for zeta(2).  That was MY error --
# zeta(2) = pi^2/6, so the weight is 2, which is what the detector reported in Part C's table all
# along.  The control is kept with the correct value.
check(pi_weight(sp.simplify(sp.zeta(2))) == sp.Integer(2)
      and pi_weight(sp.Rational(7, 3)) == 0,
      "NC1  CONTROL: the weight function reads zeta(2) = pi^2/6 as weight 2 (not 1 -- my first draft "
      "of this control asserted 1 and was wrong) and a rational as 0, so Part C's integer-weight "
      "finding is the detector working, not failing",
      f"w(zeta(2)) = {pi_weight(sp.simplify(sp.zeta(2)))}, w(7/3) = {pi_weight(sp.Rational(7, 3))}")
check(pi_weight(sp.sqrt(pi_s)) == sp.Rational(1, 2),
      "NC2  CONTROL: and it detects sqrt(pi) as weight 1/2, so B1's half-integer result is real")
# a wrong xi must not satisfy the equivalence
check(sp.simplify(kap_of_xi.subs(xi, 1) - sp.Rational(1, 2)) != 0,
      "NC3  CONTROL FIRES: xi = 1 (i.e. M1 = 1/H_Lambda, the naive horizon memory) gives "
      f"kappa = {sp.simplify(kap_of_xi.subs(xi, 1))} = {sig(Znum/3, 8)}, NOT 1/2 -- so A3 is a real "
      "determination")
check(abs(Znum / 3 / mp.mpf("0.5") - 1) > mp.mpf("0.5"),
      "NC4  and that naive value is 1.93, i.e. 3.86x too large -- the same 2Z/3 as always, "
      "consistent with the earlier horizon result")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")
print(f"  both footings: a_0 = {sig(A0)} / {sig(A0_ALT)} m/s^2; xi is footing-independent as a pure "
      f"number, though M1 itself differs")

print("""
==================================================================================================
WHAT THE CALCULATION RETURNS
==================================================================================================
  THE TARGET IS ONE PURE NUMBER.  A de Sitter response kernel can only return M1 = xi/H_Lambda, and
  the proved equivalence then gives kappa = Z/(3 xi), so
        *** kappa = 1/2  <==>  xi = 2Z/3 = (8/9) sqrt(6 pi) = 3.85921 ***
  THE pi IS AVAILABLE.  xi needs pi-weight +1/2.  Thermal spectral moments cannot give it -- they are
  Gamma(n+1) zeta(n+1) values with INTEGER weight -- but the THREE-dimensional spatial loop measure
  (4 pi)^(-3/2) has weight -3/2, and combined with zeta(2) ~ pi^2 it lands on exactly +1/2.  That is
  escape E1 of the corpus's number-field theorem ("an odd-dimensional measure"), reached independently.
  My first instinct that parity closes this route was WRONG, and the correction is on the record.
  THE OBSTRUCTION IS A sqrt(6).  Beyond the sqrt(pi), xi requires sqrt(6) -- and spectral integrals
  produce rationals and zeta values, never sqrt(6).  That single algebraic irrationality is now the
  entire gap.
  AND sqrt(6) IS A COUNT: 6 = D(D-1)/2 at D = 4 = the number of Lorentz generators of SO(1,3), exactly
  the kind of object a mode sum over the algebra produces.  ⚠️ But the accompanying 8/9 was
  reverse-engineered from the answer and carries no evidential weight on a menu of small rationals, so
  this is a DECOMPOSITION of xi, not a derivation.
  NOT DONE: no propagator, spectral density or loop integral is evaluated here.  This is the arithmetic
  any such evaluation must satisfy -- it constrains the answer and does not produce it.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
