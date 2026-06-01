#!/usr/bin/env python3
"""
Is Z²=32π/3 the UNIQUE geometry that works? Carl's strongest pro-framework argument, tested.
============================================================================================

Carl's argument (steelmanned): "8×(4π/3)=32π/3 is the ONE parameter put in; it works; it's
the only geometry that fits, and the whole web follows -- isn't that evidence?" This tests the
uniqueness claim honestly rather than dismissing it. Three tests:

  1. is the coefficient Z=cH0/a0 uniquely 5.79, or degenerate with the (H0,a0) you adopt?
  2. how many SIMPLE constants fall in the data-allowed Z band?
  3. does the over-constrained WEB actually confirm the VALUE 32π/3?

What it credits (this is NOT a dismissal): the density form a0=(c/2)√(Gρ_c) is Friedmann-real
-- the √(8π/3) inside Z=2√(8π/3) IS the Friedmann factor, not arbitrary geometry. And the
EVOLUTION a0∝E(z) is *derived* (horizon thermodynamics, route-independent; horizon_a0_derivation.py).
The question here is narrower: is the specific VALUE 32π/3 uniquely selected? Run it and see.

Run:  python real_research/coefficient_uniqueness_test.py
"""

import math

c = 2.99792458e8
MPC = 3.0857e22
Z2 = 32 * math.pi / 3
Zf = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2


def Zof(H0, a0):
    return c * (H0 * 1e3 / MPC) / (a0 * 1e-10)


def main():
    print("=" * 78)
    print(f"  the framework number: Z = √(32π/3) = 2√(8π/3) = {Zf:.4f}")
    print("  HONEST CREDIT FIRST: the √(8π/3) IS the Friedmann factor (real physics);")
    print("  only the factor of 2 is posited. So this is NOT arbitrary geometry -- the")
    print("  question is whether the specific VALUE is uniquely forced. Three tests:")
    print("=" * 78)

    print("\n(1) Is Z uniquely 5.79, or DEGENERATE with the (H0,a0) choice?")
    print(f"   {'H0':>7}{'a0':>8}{'Z=cH0/a0':>11}   lands on")
    named = {5.789: "√(32π/3)  [framework]", 6.000: "6         [Verlinde]",
             6.283: "2π        [Milgrom]"}
    for H0, a0 in [(67.4, 1.13), (67.4, 1.20), (69.8, 1.13), (73.0, 1.13), (73.0, 1.20)]:
        Z = Zof(H0, a0)
        tag = next((n for v, n in named.items() if abs(Z - v) < 0.03), "")
        print(f"   {H0:>7.1f}{a0:>8.2f}{Z:>11.3f}   {tag}")
    print("   => DEGENERATE with H0: (Planck,SPARC)->√(32π/3); (TRGB)->6=Verlinde;")
    print("      (SH0ES)->2π=Milgrom. 32π/3 is what you get IF you pick Planck H0 + a0=1.13.")
    print("      All three 'famous' coefficients appear for currently-valid data choices.")

    print("\n(2) How many SIMPLE constants fall in the data-allowed Z band?")
    Zlo, Zhi = Zof(67, 1.30), Zof(73, 1.00)
    print(f"   band (H0∈[67,73], a0∈[1.0,1.3]e-10):  Z ∈ [{Zlo:.2f}, {Zhi:.2f}]  (±{(Zhi-Zlo)/(Zhi+Zlo)*100:.0f}%)")
    cands = {"3√π": 3*math.sqrt(math.pi), "2e": 2*math.e, "π√3": math.pi*math.sqrt(3),
             "11/2": 5.5, "2^(5/2)": 2**2.5, "18/π": 18/math.pi, "√(32π/3)": Zf,
             "√34": math.sqrt(34), "π+e": math.pi+math.e, "6": 6.0, "2π": 2*math.pi,
             "4φ": 4*PHI, "13/2": 6.5, "7": 7.0, "39/2π": 39/(2*math.pi)}
    hits = sorted([(v, n) for n, v in cands.items() if Zlo <= v <= Zhi])
    print(f"   {len(hits)} of {len(cands)} simple constants land in the band:")
    print("     " + "  ".join(f"{n}={v:.2f}" for v, n in hits))
    print("   => a ±17% band holds MANY simple constants. 32π/3 is not singled out by the data.")

    print("\n(3) Does the WEB confirm the VALUE 32π/3? ('it fits all the other stuff')")
    print("   a0(z)/a0(0)=E(z): Z CANCELS. H0=Z a0/c, the Λ floor, RAR, BTFR -- every web edge")
    print("   uses a0/cH=1/Z as an INVARIANT; none pins the VALUE of Z. The over-constrained")
    print("   web (the real evidence, +4) is INDIFFERENT to whether Z=5.79, 6, or 2π.")
    print("   It confirms a0 EVOLVES; it says nothing about the coefficient's origin.")

    print("\n(4) Carl's sharper question: is √(32π/3) the ONLY/closest form that hits 5.79?")
    print("    [CORRECTION: an earlier version compared distance to √(32π/3) ITSELF -- circular,")
    print("     so it trivially read '0.00%'. Compare to the actual DATA value instead.]")
    Zdata = Zof(67.4, 1.13)        # the real cH0/a0, NOT the framework's own number
    fried = math.sqrt(8 * math.pi / 3)
    print(f"   DATA value Z = cH0/a0 (Planck 67.4, SPARC 1.13) = {Zdata:.4f}. Ranked honestly:")
    forms = {"√(32π/3) [framework]": Zf, "29/5": 5.8, "√34": math.sqrt(34), "23/4": 5.75,
             "35/6": 35 / 6, "18/π": 18 / math.pi, "6 [Verlinde]": 6.0, "2π [Milgrom]": 2 * math.pi}
    for n, v in sorted(forms.items(), key=lambda x: abs(x[1] - Zdata)):
        print(f"     {v:.4f}   {abs(v-Zdata)/Zdata*100:5.2f}%   {n}")
    print("   => 29/5 = 5.800 is CLOSER to the data than √(32π/3). So √(32π/3) is NOT even the")
    print("      closest fit, let alone the only one -- several tie. NOT unique, full stop.")
    print("   The ONLY thing distinguishing √(32π/3): Z = F·√(8π/3), √(8π/3)=2.894 is FRIEDMANN")
    print("   (locked physics), and F=2 is the Schwarzschild READING (F=2.07->6, F=2.17->2π also")
    print("   fit). Its basis is a physical FORM, not a unique or closest number.")

    print("\n" + "=" * 78)
    print("  VERDICT -- engaging the argument, not dismissing it")
    print("=" * 78)
    print("  * 32π/3 is a LEGITIMATE value -- it follows from the density form a0=(c/2)√(Gρ),")
    print("    whose √(8π/3) is real Friedmann physics. It is not arbitrary numerology.")
    print("  * BUT it is NOT uniquely selected: degenerate with H0 (Verlinde's 6 and Milgrom's")
    print("    2π appear for other valid data), and a ±17% band holds many simple constants.")
    print("  * AND the web does not confirm the value (Z cancels). So 'only this geometry works")
    print("    and the web follows' does not hold: the web follows for ANY coefficient.")
    print("  * The eta-invariant 'derivation' of 8×(4π/3) is a category error (eta_local_...py),")
    print("    and you don't need it -- 32π/3 already follows from the density form.")
    print("  * The genuinely DERIVED, route-independent win is the EVOLUTION a0∝E(z) -- which")
    print("    needs NO Z (horizon_a0_derivation.py). THAT is where the real evidence lives,")
    print("    not in the coefficient's geometric packaging.")


if __name__ == "__main__":
    main()
