#!/usr/bin/env python3
r"""mi_2Z_is_the_friedmann_root_2026.py -- WITHDRAWS my "2Z carries sqrt(pi) and has no mechanism" framing.

WHAT I SAID, AND WHY IT WAS UNFAIR. In mi_crossover_master_formula_2026.py check C2b, and in section 3.3 of
DOI 10.5281/zenodo.21782600, I wrote that the crossover ratio this framework requires,
r = 2Z = 11.577620, "carries sqrt(pi), which no detector-response normalisation supplies", and set that against
Milgrom 2020's r = 4 pi, which "has an obvious mechanism". I stated that as an arrow pointing at HIS coefficient.

That framing is WRONG, and wrong in the direction of dismissing the framework. The sqrt(pi) in 2Z is not exotic:

    2Z  =  4 sqrt(8 pi / 3)

and 8 pi / 3 is EXACTLY the Friedmann factor -- the same 8 pi/3 that converts a density into the square of an
expansion rate, H^2 = 8 pi G rho / 3. So 2Z is nothing more mysterious than "4, divided by the square root of the
Friedmann factor". Asking "where would sqrt(pi) come from" is a non-question: it comes from Friedmann, which is
about as motivated as a factor in cosmology gets. What I had presented as an exotic transcendental is a
bookkeeping constant that is already in the theory.

WHAT THE REAL FORK IS. Both live proposals are ONE round factor applied to a natural rate:

    Milgrom 2020    floor = c H_Lambda / (4 pi)          rate = the horizon expansion rate
    this framework  floor = (1/4) c sqrt(G rho_Lambda)   rate = the LOCAL response rate to the vacuum density

The question is not the arithmetic, it is WHICH RATE the inertia floor tracks. That is a physics question, and it
is the framework's own premise -- a modified-INERTIA law responds to the local vacuum density, and a global
expansion rate is arguably not something a local inertia law has any business knowing.

WHAT SURVIVES AGAINST THE FRAMEWORK, unchanged: Deser & Levin's construction DERIVES the floor as the
Gibbons-Hawking temperature, which is proportional to H. So H is the mechanism-GIVEN rate and sqrt(G rho) is a
SUBSTITUTION for it. That argument is untouched by anything here, and it is the real objection. kappa = 1/2
remains FITTED, NOT DERIVED. The correction is only that "2Z is unnatural arithmetic" was never a good objection,
and I should not have offered it as one.

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


G, rho, cc, Lam = sp.symbols("G rho c Lambda", positive=True)
Z = 2 * sp.sqrt(8 * sp.pi / 3)
r_fw = sp.simplify(2 * Z)

print("=" * 104)
print("  A1  THE ARITHMETIC, PINNED TO 12 FIGURES")
print("=" * 104)
zf, rf = sp.N(Z, 20), sp.N(r_fw, 20)
print(f"  Z    = 2 sqrt(8 pi/3) = {zf}")
print(f"  2Z   = 4 sqrt(8 pi/3) = {rf}")
print(f"  1/Z                   = {sp.N(1/Z, 20)}")
check(abs(float(rf) - 11.577620072932) < 5e-12 and abs(float(zf) - 5.788810036466) < 5e-12,
      f"A1a 2Z = 11.577620072932 and Z = 5.788810036466. Earlier in this corpus I relayed 2Z = 11.577626 and "
      f"11.577627, from carrying Z = 5.788813 -- wrong in the 6th digit. The value 11.577620 IS correct")
check(abs(float(rf) - 11.577626) > 1e-6 and abs(float(rf) - 11.577627) > 1e-6,
      f"A1b and the two stale values are genuinely OUTSIDE 1e-6 of the true one, so this is a real correction to "
      f"the relayed digits and not a rounding difference")
check(sp.simplify(r_fw - 8 * sp.sqrt(6 * sp.pi) / 3) == 0,
      f"A1c 2Z = 8 sqrt(6 pi)/3 exactly, an independent closed form giving the same number")

print("\n" + "=" * 104)
print("  A2  *** 8 pi/3 IS THE FRIEDMANN FACTOR, SO THE sqrt(pi) IS NOT EXOTIC ***")
print("=" * 104)
# Friedmann for a pure-Lambda universe: H^2 = 8 pi G rho / 3. Build cH_Lambda and the framework floor from it.
H_L = sp.sqrt(8 * sp.pi * G * rho / 3)
floor_fw = sp.Rational(1, 4) * sp.sqrt(G * rho)          # = a0/2 at kappa = 1/2, since a0 = (1/2) c sqrt(G rho)
ratio = sp.simplify(H_L / floor_fw)
print(f"  H_Lambda        = sqrt(8 pi G rho/3)   <- Friedmann, and 8 pi/3 is ITS factor")
print(f"  framework floor = (1/4) sqrt(G rho)    <- a bare sqrt(G rho), NO Friedmann factor")
print(f"  ratio           = {ratio}")
check(sp.simplify(ratio - r_fw) == 0,
      f"A2a *** the ratio c H_Lambda / (a0/2) IS 2Z, derived here straight from Friedmann with no numerology. So "
      f"2Z = 4/sqrt(3/(8 pi)) is literally '4 over the square root of the Friedmann factor'. THE sqrt(pi) IN 2Z "
      f"IS FRIEDMANN'S sqrt(pi). My claim that it 'carries sqrt(pi), which no normalisation supplies' is "
      f"WITHDRAWN -- it was a bad objection and it ran against the framework ***")
# and the same statement with Lambda instead of rho, to show it is footing-independent in FORM
rho_L = Lam * cc**2 / (8 * sp.pi * G)
check(sp.simplify(H_L.subs(rho, rho_L) - cc * sp.sqrt(Lam / 3)) == 0,
      f"A2b consistency: substituting rho_Lambda = Lambda c^2/(8 pi G) turns H_Lambda into c sqrt(Lambda/3), "
      f"which is Milgrom 1994's a_lambda/c. The 8 pi cancels EXACTLY, confirming 8 pi/3 is bookkeeping between "
      f"the density and the curvature form and not an independent constant")

print("\n" + "=" * 104)
print("  A3  THE FORK RESTATED HONESTLY -- one round factor each, on DIFFERENT rates")
print("=" * 104)
Hnum = 1.0                                        # work in units of c H_Lambda
sq = float(sp.sqrt(3 / (8 * sp.pi)))              # sqrt(G rho) in units of H_Lambda
ROWS = [("Milgrom 1999", "c H_Lambda",                 2.0 * 1.0,            "horizon rate, factor 1"),
        ("Milgrom 2020", "c H_Lambda / (4 pi)",        2.0 / (4 * math.pi),  "horizon rate, factor 1/4pi"),
        ("framework, kappa=1/2", "(1/4) c sqrt(G rho_L)", 2.0 * 0.25 * sq,   "LOCAL rate, factor 1/4"),
        ("kappa=1", "(1/2) c sqrt(G rho_L)",          2.0 * 0.5 * sq,       "LOCAL rate, factor 1/2")]
print(f"  {'proposal':<22}{'floor':<26}{'q = 2 k/cH_L':>14}{'r = 2/q':>10}   what it is")
print("  " + "-" * 100)
for nm, k, q, w in ROWS:
    print(f"  {nm:<22}{k:<26}{q:>14.8f}{2/q:>10.6f}   {w}")
check(abs(2.0 * 0.25 * sq - float(1 / Z)) < 1e-14 and abs(2.0 / (4 * math.pi) - float(1 / (2 * sp.pi))) < 1e-14,
      f"A3a both rows reproduce their published coefficients from the floor alone, so the table is a real "
      f"reparametrisation and not a fit: the framework's 1/4 on a bare sqrt(G rho) gives q = 1/Z = "
      f"{float(1/Z):.8f}, and Milgrom 2020's 1/4pi on the horizon rate gives 1/2pi = {float(1/(2*sp.pi)):.8f}")
check(abs(2.0 * 0.5 * sq / float(1 / Z) - 2.0) < 1e-12,
      f"A3b prove-by-moving-the-number: doubling the floor factor from 1/4 to 1/2 (kappa 1/2 -> 1) doubles q "
      f"exactly, confirming q is linear in the floor and the table is not accidentally degenerate")

print("""
  SO THE HONEST COMPARISON IS: each proposal is ONE round number on ONE natural rate. Neither is derived.
  Roundness does NOT adjudicate -- and it does not favour Milgrom 2020, which is what I wrongly implied.
  The fork is WHICH RATE the inertia floor tracks:
     the GLOBAL expansion rate H_Lambda            (Milgrom 1999, 2020)
     the LOCAL response rate sqrt(G rho_Lambda)    (this framework)
  For a modified-INERTIA law the local rate is a defensible choice on the framework's own premises, since a local
  inertia law has no obvious access to a global expansion rate.

  WHAT STILL CUTS AGAINST THE FRAMEWORK, and is the real objection:
  Deser & Levin DERIVE the floor as the Gibbons-Hawking temperature, T_GH proportional to H. So H is
  MECHANISM-GIVEN and sqrt(G rho) is a SUBSTITUTION for it. Nothing above touches that. Also untouched: r is a
  free parameter, so this is a reparametrisation and NOT a derivation; and r = 2Z kernel admissibility against the
  ephemeris bound and the 30.6% shape range remains UNTESTED.""")
check(float(r_fw) < float(4 * sp.pi),
      f"A3c and the residual's direction, recorded once more because it is small and real: 2Z = {float(r_fw):.6f} "
      f"is a SMALLER departure from Milgrom 1999's r = 1 than 4 pi = {float(4*sp.pi):.6f} is. Direction, not "
      f"evidence")

print("\n" + "=" * 104)
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. 11.577620 IS the right number. And '2Z is unnatural arithmetic' is WITHDRAWN as an objection:")
print("  2Z = 4/sqrt(Friedmann factor). The live objection is Deser-Levin's, that the horizon FIXES the floor at")
print("  H. kappa = 1/2 remains FITTED, NOT DERIVED.")
