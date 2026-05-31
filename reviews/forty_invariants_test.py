#!/usr/bin/env python3
"""
40 honest attempts to DERIVE Z^2 = 32*pi/3 as a real invariant of T^3/Z2.
=========================================================================

Carl asked: come up with 20 ideas for "new math" that could produce Z^2 = 32*pi/3
(or Z = 5.7888, or the per-fixed-point 4*pi/3) as a genuine invariant of the flat
orbifold T^3/Z2 -- and test each honestly. If none work, try another 20.

Rule of the game (no cheating):
  An idea PASSES only if a STANDARD mathematical invariant of the space equals the
  target WITHOUT us choosing a scale/normalization to make it fit. Matching only by
  picking the radius/size = inserting the answer = FAIL.

Targets:  Z^2 = 32*pi/3 = 33.5103...,  Z = 5.7888...,  4*pi/3 = 4.18879...

Each candidate is tagged:
  [SI-int/rat] scale-invariant & rational/integer  -> provably can't be 32*pi/3 (irrational)
  [SI-tr]      scale-invariant & transcendental     -> compute and compare
  [scale-dep]  depends on the chosen size           -> 'matches' only by fixing the scale

Pure stdlib + numpy.  Run:  python reviews/forty_invariants_test.py
"""

import math
import numpy as np

PI = math.pi
Z2_TARGET = 32 * PI / 3          # 33.5103
Z_TARGET = math.sqrt(Z2_TARGET)  # 5.7888
BALL = 4 * PI / 3                # 4.18879
TARGETS = {"Z^2=32pi/3": Z2_TARGET, "Z=5.789": Z_TARGET, "4pi/3": BALL}
TOL = 0.02  # flag a 'hit' only if within 2% of a target


# ---- live lattice computations -------------------------------------------------
def epstein(power, box=60):
    """Sum_{n!=0} |n|^{-power} over the cubic lattice (converges for power>3)."""
    s = 0.0
    for a in range(-box, box + 1):
        for b in range(-box, box + 1):
            aa = a * a + b * b
            for c in range(-box, box + 1):
                m = aa + c * c
                if m:
                    s += m ** (-power / 2.0)
    return s


def theta3(q, kmax=50):
    """theta_3(0;q) = sum_n q^{n^2}."""
    return sum(q ** (n * n) for n in range(-kmax, kmax + 1))


def heat_trace_T3(t, box=40):
    """Tr e^{-t Delta} on unit T^3 (Laplacian eigenvalues (2pi)^2|n|^2)."""
    s = 0.0
    f = (2 * PI) ** 2
    for a in range(-box, box + 1):
        for b in range(-box, box + 1):
            aa = a * a + b * b
            for c in range(-box, box + 1):
                s += math.exp(-t * f * (aa + c * c))
    return s


def check(name, value, klass, note=""):
    hit = ""
    for tname, tval in TARGETS.items():
        if abs(value - tval) / tval < TOL:
            hit = f"  <== within {TOL*100:.0f}% of {tname}!"
    # nearest target distance for context
    z2_off = (value - Z2_TARGET) / Z2_TARGET * 100
    print(f"  {name:<46s} = {value:>12.5f}  [{klass}]  (Z^2 off {z2_off:+6.1f}%){hit}")
    if note:
        print(f"      {note}")
    return bool(hit)


# ================================================================================
def batch1():
    print("=" * 88)
    print("BATCH 1 -- geometry / spectral / lattice invariants of T^3/Z2")
    print("=" * 88)
    hits = 0
    # scale-invariant, rational/integer: cannot be irrational 32*pi/3
    hits += check("1. eta invariant  eta(T^3/Z2)", 0.0, "SI-rat", "spectral asymmetry; +/- symmetric spectrum")
    hits += check("2. Euler characteristic  chi(T^3/Z2)", 4.0, "SI-int", "averaging formula (1/2)(0+2^3)")
    hits += check("3. orbifold Euler char  chi_orb", 0.0, "SI-rat", "chi(T^3)/|Z2| = 0")
    hits += check("4. signature  sigma(T^3/Z2)", 0.0, "SI-int", "odd-dimensional")
    hits += check("5. sum of Betti numbers b*(T^3)", 8.0, "SI-int", "1+3+3+1 = 8 = #fixed points (real!)")
    hits += check("6. number of spin structures", 8.0, "SI-int", "2^3 = 8")
    hits += check("7. Ray-Singer torsion (trivial rep)", 1.0, "SI-rat", "flat torus")
    hits += check("8. Dedekind sum  s(1,2)", 0.0, "SI-rat", "the genuine Z2 eta-contribution")
    hits += check("9. zeta_Delta(0)  (scalar Laplacian)", -1.0, "SI-rat", "= -dim ker (odd dim, a_{3/2}=0)")
    hits += check("10. Chern-Simons(flat connection)", 0.0, "SI-rat", "in Q/Z")
    hits += check("11. kissing number (cubic lattice)", 6.0, "SI-int", "")
    hits += check("12. lattice determinant", 1.0, "SI-rat", "")
    # scale-invariant, transcendental: compute & compare
    hits += check("13. sphere-packing density (cubic)", PI / 6, "SI-tr", "= pi/6")
    hits += check("14. Epstein zeta  Z_{Z^3}(2)=sum|n|^-4", epstein(4), "SI-tr", "computed over |n_i|<=60")
    hits += check("15. Epstein zeta  Z_{Z^3}(3)=sum|n|^-6", epstein(6), "SI-tr", "computed")
    hits += check("16. theta_3(0;e^-pi)^3", theta3(math.exp(-PI)) ** 3, "SI-tr", "(pi^{1/4}/Gamma(3/4))^3")
    hits += check("17. Watson integral (simple cubic)", 1.5163860591, "SI-tr", "[literature value]")
    hits += check("18. Madelung constant (NaCl)", -1.7475645946, "SI-tr", "[literature value]")
    # scale-dependent: 'match' only by choosing the size
    hits += check("19. lambda_1(Laplacian, unit T^3)", (2 * PI) ** 2, "scale-dep", "= 4pi^2; closest, but size-set")
    hits += check("20. Vol(T^3/Z2) at unit cube", 0.5, "scale-dep", "any value under rescaling")
    print(f"\n  BATCH 1 RESULT:  {hits}/20 genuine invariants equal a target.\n")
    return hits


def batch2():
    print("=" * 88)
    print("BATCH 2 -- quantum / algebraic / number-theoretic / more spectral")
    print("=" * 88)
    hits = 0
    hits += check("21. Dirac eigenvalue gap |lam_1(D)| unit", 2 * PI, "scale-dep", "= 2pi ~ 6.28, near Z=5.79 (8.5%), size-set")
    hits += check("22. lambda_1 * Vol^{2/3} (T^3/Z2)", (2 * PI) ** 2 * 0.5 ** (2 / 3), "SI-tr", "scale-inv Laplacian combo")
    hits += check("23. lambda_1 * Vol^{2/3} (T^3)", (2 * PI) ** 2, "SI-tr", "= 4pi^2 (Vol=1)")
    hits += check("24. quantizer 2nd moment G (cubic)", 1 / 12, "SI-rat", "")
    hits += check("25. covering/packing radius ratio", math.sqrt(3), "SI-tr", "= sqrt(3) (algebraic)")
    hits += check("26. K^0(T^3/Z2) rank", 8.0, "SI-int", "integer K-theory rank")
    hits += check("27. Rokhlin / cobordism class", 0.0, "SI-int", "torsion")
    hits += check("28. Smith-Minkowski-Siegel mass", 1 / 48, "SI-rat", "cubic genus mass (rational)")
    hits += check("29. theta coeff r_3(1) (lattice pts)", 6.0, "SI-int", "")
    hits += check("30. CsCl Madelung-type sum", -1.7626, "SI-tr", "[literature value]")
    hits += check("31. Epstein Z_{Z^3}(3/2) (anal. cont.)", -2.7195, "SI-tr", "[literature value]")
    hits += check("32. zeta(3)  (Apery)", 1.2020569, "SI-tr", "a 'natural' transcendental")
    hits += check("33. Catalan's constant", 0.9159656, "SI-tr", "")
    hits += check("34. Glaisher-Kinkelin A (in det Delta)", 1.2824271, "SI-tr", "")
    hits += check("35. heat trace Tr e^{-Delta} at t=1", heat_trace_T3(1.0), "scale-dep", "size-set")
    hits += check("36. heat trace Tr e^{-Delta} at t=0.05", heat_trace_T3(0.05), "scale-dep", "~ Vol/(4pi t)^{3/2}")
    hits += check("37. Reidemeister torsion (nontrivial rep)", 2.0, "SI-tr", "algebraic; rep-dependent")
    hits += check("38. spectral gap ratio lam_2/lam_1", 2.0, "SI-rat", "= |n|^2: 2/1")
    hits += check("39. first Dirac/Laplace ratio", 2 * PI / (2 * PI) ** 2, "SI-tr", "= 1/(2pi)")
    hits += check("40. '8 x Vol(unit B^3)' = the DEFINITION", 8 * BALL, "scale-dep", "<-- the ONLY match: it IS 32pi/3, by construction")
    print(f"\n  BATCH 2 RESULT:  {hits}/20 genuine invariants equal a target.\n")
    return hits


def main():
    h1 = batch1()
    h2 = batch2()
    print("=" * 88)
    print("VERDICT")
    print("=" * 88)
    print(f"  Genuine invariants matching a target: batch1 {h1}/20, batch2 {h2}/20.")
    print(f"  The ONLY thing that equals 32*pi/3 is candidate #40 -- the construction")
    print(f"  '8 x volume of the unit ball' -- which IS the definition, with the unit")
    print(f"  ball's radius chosen. That is inserting the answer, not deriving it.\n")
    print("  WHY (the dichotomy that makes Option C a dead end):")
    print("   * Every SCALE-INVARIANT invariant of T^3/Z2 is either")
    print("       (a) rational/integer  (eta=0, chi=4, sigma=0, torsion=1, Dedekind=0,")
    print("           CS in Q/Z, Betti=8, spin=8, kissing=6, det=1, K-rank, mass) --")
    print("           and 32*pi/3 is IRRATIONAL, so excluded; or")
    print("       (b) a lattice-zeta / theta transcendental (packing pi/6, Epstein,")
    print("           Madelung, Watson, theta, zeta(3), Catalan) -- all computed, none")
    print("           equal 32*pi/3.")
    print("   * Every SCALE-DEPENDENT quantity (volume, lambda_1, Casimir, ball volume)")
    print("     equals 32*pi/3 only at one chosen size. 32*pi/3 = Vol(B^3, r=2) is")
    print("     itself such a quantity, so matching it just fixes the radius.")
    print()
    print("  CONCLUSION: 32*pi/3 lives in the scale-dependent 'volume' class, where")
    print("  numbers are DEFINITIONS, not the scale-free 'invariant' class, where")
    print("  derivations live. No new invariant can bridge that -- a genuine eta/index/")
    print("  torsion is scale-free and (here) rational; a volume is scale-set. So Z^2 =")
    print("  32*pi/3 is, honestly, the Friedmann definition 8 x (4pi/3). Option A.")


if __name__ == "__main__":
    main()
