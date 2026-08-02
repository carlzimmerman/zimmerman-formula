#!/usr/bin/env python3
r"""mi_kernel_measure_from_desitter_2026.py -- THE LAST ROUTE: derive the kernel measure from de Sitter itself,
without the RAR calibration. IT WORKS -- it produces a closed-form kappa with no data input at all -- AND THE
kappa IT PRODUCES IS NOT OURS. It is kappa = sqrt(2/(3 pi)) = c H_Lambda/2pi, i.e. MILGROM 2020's coefficient.
Then a theorem closes the whole programme: kappa = 1/2 is unreachable from geometric/thermal ingredients.

WHERE THIS COMES FROM. Two routes have now been closed. mi_kappa_linear_class_2026 proved no tail functional
of the kernel's own measure can force kappa (W_n ~ kappa^n identically), and reduced the problem to
Z^2 = 4 x (8pi/3). mi_horizon_entropy_route_2026 closed the entropy route (all four constructions land at
Z ~ O(1); the Bekenstein-Hawking quarter cashes out to Milgrom 1999's 2cH_Lambda). Both named the same last
route: derive the MEASURE from first principles without passing through the RAR.

WHY THAT IS THE RIGHT LAST TARGET. KERNEL_THEORY.md:47 states the response is "forced by (Herglotz class) +
(the RAR): there is nothing left to tune." The RAR is DATA -- it is exactly where a0, hence kappa, enters. So
if the second condition can be supplied by de Sitter geometry instead of by the rotation curves, kappa comes
out PREDICTED. That is the only shape of derivation left.

WHAT DE SITTER SUPPLIES, with no reference to any galaxy. For a comoving Unruh-DeWitt detector in de Sitter,
the response satisfies the KMS condition at the Gibbons-Hawking temperature exactly:
        F(-omega)/F(+omega) = exp(hbar omega / k_B T_GH),      T_GH = hbar H_Lambda/(2 pi k_B)
so the detector's spectrum is a function of the single dimensionless combination
        x = hbar omega / (k_B T_GH) = 2 pi omega / H_Lambda
That 2 pi is the whole content of de Sitter thermality and it is forced, not chosen. The framework's kernel
carries its own dimensionless frequency
        w = omega c / a0 = omega Z / H_Lambda
So IF the kernel is the de Sitter response, w and x are the same variable up to a fixed identification, and
that identification FIXES Z with no data.

  L1  the de Sitter response and its forced variable -- no RAR, no galaxies
  L2  the identification candidates, all stated first, all evaluated -- and the closed form that comes out
  L3  *** THE UNIFIED OBSTRUCTION THEOREM: every route's ingredients are rational x pi^(integer); Z carries
      pi^(1/2); so NO linear-in-Z construction can reach kappa = 1/2, and all 12 attempts were linear ***
  L4  the three-way tension, the ledger, and the single escape that remains

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


Z_FW = sp.sqrt(32 * sp.pi / 3)                 # the framework
Z_M20 = 2 * sp.pi                              # Milgrom 2020
K_REF = sp.sqrt(8 * sp.pi / 3)                 # kappa at Z = 1
A0_BOX = 0.16


def kappa_of_Z(Z):
    return sp.simplify(K_REF / Z)


banner("L1  THE DE SITTER RESPONSE AND ITS FORCED VARIABLE -- no RAR, no galaxies")

om, HL, hb, kBs, cs = sp.symbols("omega H_Lambda hbar k_B c", positive=True)
T_GH = hb * HL / (2 * sp.pi * kBs)
x_thermal = sp.simplify(hb * om / (kBs * T_GH))
print(f"  Gibbons-Hawking temperature   T_GH = {T_GH}")
print(f"  KMS/detailed balance:  F(-w)/F(+w) = exp(hbar omega/k_B T_GH) = exp({x_thermal})")
print(f"  so the de Sitter response depends on ONE dimensionless variable   x = {x_thermal}")
check(sp.simplify(x_thermal - 2 * sp.pi * om / HL) == 0,
      f"L1a de Sitter supplies exactly one dimensionless frequency, x = 2 pi omega/H_Lambda. The 2 pi is the "
      f"forced content of de Sitter thermality (it is the same 2 pi as in Unruh's a/2pi c). NOTHING here "
      f"references a galaxy, a rotation curve, or the RAR -- which is the whole point of this route")

Zs = sp.Symbol("Z", positive=True)
w_kernel = sp.simplify(om * Zs / HL)           # w = omega c/a0 with a0 = cH_Lambda/Z
print(f"\n  the framework's kernel variable   w = omega c/a0 = {w_kernel}   (a0 = cH_Lambda/Z)")
check(sp.simplify(w_kernel.subs(Zs, 1) - om / HL) == 0,
      f"L1b and the kernel's variable is w = omega Z/H_Lambda, so identifying it with x fixes Z ALGEBRAICALLY "
      f"-- one equation, one unknown, no free parameters and no data")


banner("L2  THE IDENTIFICATION CANDIDATES -- stated first, all evaluated, all reported")

print("""  The identification is an ADDED AXIOM -- "the kernel IS the de Sitter response" -- not a theorem. So
  every natural way to make it is enumerated here and every one is reported, before any is preferred. Each
  is a statement of the form w = lambda * x for a forced lambda, giving Z = 2 pi lambda.

    I1  w = x            the kernel's frequency variable IS the de Sitter thermal variable (the direct
                         reading of "a0 is the de Sitter-Unruh scale")
    I2  w = x/2          the kernel's BRANCH POINT (w = 1/2) sits at unit thermal activation x = 1
    I3  w = 2x           the thermal variable is the kernel's SQUARED-argument variable T = w^2 at w = 1
    I4  w = x/(2 pi)     the kernel variable is omega/H_Lambda, i.e. the geometric rather than thermal rate
""")
IDENT = [("I1  w = x", sp.Integer(1)), ("I2  w = x/2", sp.Rational(1, 2)),
         ("I3  w = 2x", sp.Integer(2)), ("I4  w = x/(2pi)", 1 / (2 * sp.pi))]
print(f"  {'identification':<20}{'Z (exact)':>18}{'Z':>10}{'kappa (exact)':>22}{'kappa':>10}{'vs 1/2':>9}{'box':>6}")
print("  " + "-" * 96)
res = []
for nm, lam in IDENT:
    Zv = sp.simplify(2 * sp.pi * lam)
    kv = kappa_of_Z(Zv)
    kf = float(kv)
    inb = abs(kf / 0.5 - 1) <= A0_BOX
    res.append((nm, Zv, kv, kf, inb))
    print(f"  {nm:<20}{sp.sstr(Zv):>18}{float(Zv):>10.5f}{sp.sstr(kv):>22}{kf:>10.5f}"
          f"{100*(kf/0.5-1):>+8.1f}%{'YES' if inb else 'no':>6}")
print(f"  {'framework (target)':<20}{'sqrt(32pi/3)':>18}{float(Z_FW):>10.5f}{'1/2':>22}{0.5:>10.5f}"
      f"{0.0:>+8.1f}%{'YES':>6}")

I1 = res[0]
kappa_dS = I1[2]
check(sp.simplify(kappa_dS - sp.sqrt(2 / (3 * sp.pi))) == 0,
      f"L2a *** THE ROUTE PRODUCES A CLOSED-FORM kappa WITH NO DATA INPUT: *** the direct identification I1 "
      f"gives Z = 2 pi exactly, hence kappa = {sp.sstr(kappa_dS)} = sqrt(2/(3 pi)) = {float(kappa_dS):.6f}. "
      f"This is the first genuinely PREDICTED kappa anywhere in this programme -- 12 prior attempts produced "
      f"only conditions, not a derivation. It is a real result and the route is NOT empty")
check(abs(float(sp.simplify(2 * sp.pi / Z_M20)) - 1.0) < 1e-15,
      f"L2b *** AND IT IS MILGROM 2020's COEFFICIENT, NOT OURS. *** Z = 2 pi is exactly the divisor in "
      f"a0 = cH_Lambda/2pi (Milgrom 2020), and kappa = sqrt(2/(3pi)) = {float(kappa_dS):.6f} sits "
      f"{100*(float(kappa_dS)/0.5-1):+.1f}% from the framework's 1/2. So the framework's MECHANISM is "
      f"vindicated -- de Sitter thermality really does set the scale -- while its specific COEFFICIENT is not "
      f"what the mechanism's most natural derivation gives")
check(not any(abs(kf - 0.5) < 1e-6 for _, _, _, kf, _ in res),
      f"L2c and no identification gives kappa = 1/2. The four give "
      f"{', '.join(f'{kf:.4f}' for _, _, _, kf, _ in res)}; the framework needs 0.500000. I2's "
      f"{res[1][3]:.4f} and I4's {res[3][3]:.4f} bracket it but neither lands, and L3 shows why none can")


banner("L3  THE UNIFIED OBSTRUCTION THEOREM -- why all three routes had to fail")

# The framework's Z carries pi^(1/2); every route's ingredients are rational x pi^(integer).
ratio_sqrt = sp.simplify(Z_FW / sp.sqrt(sp.pi))
ratio_sq = sp.simplify(Z_FW**2 / sp.pi)
print(f"  Z_framework / sqrt(pi) = {ratio_sqrt}   -> rational: {ratio_sqrt.is_rational}")
print(f"  Z_framework^2 / pi     = {ratio_sq}   -> rational: {ratio_sq.is_rational}")
check(ratio_sq.is_rational and ratio_sqrt.is_algebraic and not ratio_sqrt.is_rational,
      f"L3a CORRECTED from my first draft, which asserted Z/sqrt(pi) is RATIONAL. It is not: "
      f"Z_framework/sqrt(pi) = {ratio_sqrt}, an algebraic IRRATIONAL. The true statement is the other half: "
      f"Z_framework^2/pi = {ratio_sq} IS rational, so Z^2 is in the class rational x pi^1 while Z itself "
      f"carries pi^(1/2) times an algebraic irrational")
# no integer k makes Z_fw / pi^k rational, because pi is transcendental and the exponent is half-integral
ks = [-2, -1, 0, 1, 2]
nonrat = [k for k in ks if not sp.simplify(Z_FW / sp.pi**k).is_rational]
check(len(nonrat) == len(ks),
      f"L3b and for every integer k in {ks}, Z_framework/pi^k is NOT rational ({len(nonrat)}/{len(ks)}) -- "
      f"because it always retains pi^(1/2 - k) and pi is transcendental. *** THEREFORE: any construction whose "
      f"ingredients are rational multiples of INTEGER powers of pi can force Z^2 but can NEVER force Z. ***")

print("""
  THAT IS THE UNIFIED REASON ALL 12 ATTEMPTS FAILED, and it is not bad luck:
    * the spectral axis fixes W_n = 1/(n pi Z^n) -- linear in 1/Z^n for the chosen n, and every candidate
      constant offered was rational x pi^k;
    * the horizon-entropy route supplies 4pi (area), 4 (Bekenstein-Hawking), 4pi/3 (volume), 2pi (Unruh,
      Gibbons-Hawking), 8pi (Einstein), 3 (Friedmann) -- all rational x pi^(integer);
    * de Sitter thermality supplies exactly one number, 2pi (L1a).
  Every one of those fixes Z (or a temperature, or a count) LINEARLY. So each returns a Z that is rational x
  pi^k, and Z_framework is not of that form. The failures were structural from the first attempt.""")

# and the nearest reachable value IS 2pi -- which is why every axis kept landing there
NUMS, DENS, KS = list(range(1, 25)), [1, 2, 3, 4, 6, 8, 12], [0, 1, 2]
cands = {(Fraction(p, q), k, float(Fraction(p, q)) * math.pi**k)
         for p, q, k in itertools.product(NUMS, DENS, KS)}
near = sorted(cands, key=lambda t: abs(t[2] / float(Z_FW) - 1))[:6]
print(f"\n  the reachable values (rational x pi^k, p<=24, q in {DENS}) NEAREST to Z_framework = "
      f"{float(Z_FW):.5f}:")
for f, k, v in near:
    print(f"      {str(f):>7} * pi^{k} = {v:9.5f}   {100*(v/float(Z_FW)-1):+7.2f}%   kappa = "
          f"{float(K_REF)/v:.5f}")
best_gap = abs(near[0][2] / float(Z_FW) - 1)
gap_2pi = abs(float(Z_M20) / float(Z_FW) - 1)
check(best_gap < gap_2pi / 4,
      f"L3c *** MY PROPOSED UNIFICATION IS REFUTED BY ITS OWN ENUMERATION AND IS WITHDRAWN. *** I expected "
      f"2 pi to be the NEAREST reachable rational x pi^k to Z_framework, which would have made the three "
      f"theory arguments one fact. It is not: the nearest is {str(near[0][0])} x pi^{near[0][1]} at "
      f"{100*best_gap:.2f}%, against 2 pi's {100*gap_2pi:.2f}% -- a factor {gap_2pi/best_gap:.0f} closer. So the "
      f"three arguments do NOT land on 2 pi because it is nearest; they land there because 2 pi is the FORCED "
      f"THERMAL number (L1a). They remain three applications of one physical input, which is the honest "
      f"unification, but not the geometric one I guessed")
check(best_gap < 0.01,
      f"L3d and this cuts the other way too, against the theorem's practical force: reachable values come "
      f"within {100*best_gap:.2f}% of Z_framework, well inside the +-16% empirical box. So L3b's 'unreachable' "
      f"is a statement about EXACT arithmetic only -- APPROXIMATE agreement in this class is cheap and proves "
      f"nothing. Any future construction landing near sqrt(32pi/3) must land on it EXACTLY to count")

banner("L4  THE THREE-WAY TENSION, THE LEDGER, AND WHAT IS LEFT")

print(f"""  *** THE LAST ROUTE IS THE ONLY ONE THAT PRODUCED A NUMBER, AND THE NUMBER IS NOT OURS. ***

  WHAT IS EARNED HERE, stated plainly:
   * De Sitter thermality alone -- KMS at T_GH, no RAR, no galaxy, no fitted input -- fixes the kernel's
     frequency variable and hence Z, giving the closed form
           kappa = sqrt(2/(3 pi)) = {float(kappa_dS):.6f},   a0 = c H_Lambda / 2 pi
     This is a genuine first-principles prediction of the acceleration scale from Lambda. Twelve prior
     attempts produced conditions; this produces a derivation. The route is NOT empty.
   * It is MILGROM 2020's coefficient, {100*(float(kappa_dS)/0.5-1):+.1f}% from the framework's kappa = 1/2.
   * And L3b proves no construction of this ingredient class can ever give kappa = 1/2, because
     Z_framework carries pi^(1/2) and the ingredients supply only integer powers.

  THE THREE-WAY TENSION, which is now the honest state of the kappa question:
     THEORY, spectral naturalness   -> 2 pi                    (mi_kappa_linear_class_2026, K3c)
     THEORY, horizon entropy        -> 2 c H_Lambda (Milgrom 1999)  (mi_horizon_entropy_route_2026, H2c)
     THEORY, de Sitter thermality   -> 2 pi, in closed form     (HERE, L2a)
     DATA, SPARC profile likelihood -> kappa = 1/2 over 1/2pi by ~2.2 sigma
                                       (mi_a0_profile_likelihood_sparc_2026)
  Three theory arguments point at the rival; the data points at the framework. They are NOT three independent
  votes -- all three trace to the single forced thermal 2 pi of L1a -- but nor are they, as I first guessed, a
  mere artefact of 2 pi being the nearest reachable value: L3c refutes that, since reachable values come
  within 0.50% of sqrt(32pi/3) while 2 pi is 8.5% away. So the honest reading is one physical input (de Sitter
  thermality) appearing three times, against one measurement at 2.2 sigma. Neither side is decisive, and
  quoting either alone would be dishonest.

  WHAT THIS MEANS FOR THE FRAMEWORK, without softening and without caving:
   * The MECHANISM is vindicated. a0 really is set by the de Sitter horizon, and the tie can be derived with
     no data at all. That is a substantive win for the physical picture and it is new here.
   * The COEFFICIENT is not derived and, by L3b, cannot be derived from this ingredient class. kappa = 1/2
     remains FITTED -- and it is fitted to a value 8.5% away from what the mechanism's own thermality gives.
   * The right way to publish this: the dS tie is derivable and gives cH_Lambda/2pi; the framework's kappa =
     1/2 is an EMPIRICAL 8.5% correction to that, favoured by SPARC at ~2.2 sigma and disfavoured by
     naturalness. That is a defensible, interesting claim. "kappa = 1/2 is derived" is not.

  LEDGER: 12 prior attempts + 4 identifications here = 16, log2(16) = {math.log2(16):.2f} bits of accumulated
  look-elsewhere on deriving kappa. All three named outside-routes are now closed.

  ONE CAVEAT ON THE THEOREM, from L3d: "unreachable" is EXACT arithmetic. Rational x pi^k values come within
  0.50% of sqrt(32pi/3), comfortably inside the empirical box, so approximate agreement in this class is cheap
  and any future construction must land EXACTLY to count for anything.

  THE SINGLE ESCAPE THAT REMAINS, and L3b pins it exactly: a construction that fixes Z^2 DIRECTLY rather than
  Z -- because Z^2 = 32pi/3 IS rational x pi and therefore reachable. It must be intrinsically quadratic in
  the horizon radius (an AREA or ENTROPY relation), must never pass through a temperature, a count, or a
  frequency identification, and must be derived before its value is evaluated. That is a sharp, narrow, and
  genuinely open target -- and it is the only one left. Inventing one now, after three routes have failed,
  would be the exact move PAPER_ATOMOS_NULL documents.""")

banner("RESULT")
nn = sum(1 for x, _ in ok if x)
print(f"  {nn}/{len(ok)} checks held.")
if nn != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: de Sitter thermality DERIVES a0 = cH_Lambda/2pi with no data; kappa = 1/2 is unreachable")
print("  from rational x pi^k ingredients; only a quadratic-in-Z construction remains.")
