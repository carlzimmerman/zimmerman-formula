#!/usr/bin/env python3
"""
Bridge 2: can horizon thermodynamics DERIVE the coefficient Z? Report what it gives.
===================================================================================

The deal (Carl's words): take Bridge 2 on with the explicit understanding that we report
whatever the thermodynamics gives -- including 'it doesn't pin the coefficient.' This works
it through rigorously: the EVOLUTION a0 ~ H is robustly derived; the question is the O(1)
coefficient Z (=2sqrt(8pi/3)=5.789), whose only un-derived piece is the factor of 2.

Method: compute the coefficient that each distinct, legitimate thermodynamic/horizon route
gives, check the framework's 'Schwarzschild' reading for self-consistency, and report whether
any route uniquely selects 5.789. No tuning; the answer is whatever the physics says.

Run:  python real_research/bridge2_coefficient_thermodynamics.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 67.4e3 / MPC
Zf = 2 * math.sqrt(8 * math.pi / 3)     # the framework's coefficient = 5.78881


def main():
    print("=" * 80)
    print("(1) THE ROBUST PART -- the EVOLUTION a0 ~ H is derived route-independently")
    print("=" * 80)
    print("   Tying a0 to the instantaneous horizon (apparent-horizon Clausius relation,")
    print("   horizon_a0_derivation.py) forces a0 ∝ H(z) regardless of the O(1). The 5σ-favored,")
    print("   falsifiable prediction needs NO coefficient. Bridge 2 is only about the O(1) Z.\n")

    print("=" * 80)
    print("(2) THE COEFFICIENT from each legitimate route -- Z = cH/a0")
    print("=" * 80)
    routes = [
        ("Unruh(a0) = de Sitter temperature", 1.0,
         "a0 whose Unruh temp = T_dS=hbar H/2pi: a0=cH"),
        ("Milgrom: 2pi a0 = cH (dS temperature)", 2 * math.pi,
         "2pi a0 = cH (1110.2580 Eq.12); a0 ~ c sqrt(Lambda/3)/2pi"),
        ("Verlinde: de Sitter VOLUME entropy", 6.0,
         "elastic response of dark-energy entropy displaced by baryons (~cH/6; contested)"),
        ("FRAMEWORK: (c/2)sqrt(G rho) density form", Zf,
         "Schwarzschild surface gravity c^2/2R of the cosmic free-fall scale R=sqrt(8pi/3)c/H"),
    ]
    print(f"   {'route':<42}{'Z':>8}{'a0 [m/s^2]':>13}")
    for name, Zr, _ in routes:
        print(f"   {name:<42}{Zr:>8.3f}{c*H0/Zr:>13.2e}")
    print("   measured a0 (SPARC) ~ 1.1-1.2e-10  -> Z_data = cH/a0 in [5.0, 7.1] (H0,a0 spread).")
    print("   => the routes span Z=1..6.3. The order of magnitude is robust; the O(1) is NOT")
    print("      fixed -- each route is a DIFFERENT matching of horizon quantities.\n")

    print("=" * 80)
    print("(3) DOES the framework's 'Schwarzschild' reading self-derive the factor of 2? NO.")
    print("=" * 80)
    print("   a0 = c^2/2R with R = c/sqrt(G rho) = sqrt(8pi/3) c/H. 'c^2/2R' is the surface")
    print("   gravity IF R is a Schwarzschild radius (R=2GM/c^2). Check the enclosed mass:")
    # M_enclosed = (4pi/3) R^3 rho ; M_Schwarzschild(R) = R c^2 / 2G
    ratio = 8 * math.pi / 3
    print(f"     M_enclosed(R) / M_Schwarzschild(R) = (4pi/3)R^3 rho / (Rc^2/2G) = 8pi/3 = {ratio:.3f}")
    print("   R is NOT the Schwarzschild radius of its enclosed mass (off by 8pi/3). So 'c^2/2R'")
    print("   is a Schwarzschild surface gravity BY ANALOGY, not for an actual horizon. The factor")
    print("   of 2 is imposed, and the 8pi/3 mismatch is exactly the Friedmann factor that makes")
    print("   Z^2=32pi/3=4*(8pi/3) close -- i.e. the pieces are arranged to the target, not forced.\n")

    print("=" * 80)
    print("(4) WHAT IS and ISN'T pinned -- the honest decomposition of Z = 2 * sqrt(8pi/3)")
    print("=" * 80)
    print(f"   sqrt(8pi/3) = {math.sqrt(8*math.pi/3):.4f}  : the Friedmann factor (H^2=8piG rho/3). DERIVED, real.")
    print(f"   factor of 2                : the Schwarzschild/horizon O(1). A POSIT.")
    print("   The 'physical dark-energy-horizon' readings cluster tightly:")
    cluster = [("framework", Zf), ("Verlinde", 6.0), ("Milgrom", 2 * math.pi)]
    lo = min(v for _, v in cluster); hi = max(v for _, v in cluster)
    for n, v in cluster:
        print(f"     {n:<10} Z={v:.3f}")
    print(f"   spread = {(hi-lo)/lo*100:.1f}% -- inside a0's ~20% systematic, so DATA cannot choose.\n")

    print("=" * 80)
    print("   VERDICT -- Bridge 2, reported straight")
    print("=" * 80)
    print("   Horizon thermodynamics DERIVES the evolution (a0 ∝ H) and the order of magnitude")
    print("   (a0 ~ cH). It does NOT pin the coefficient: legitimate routes give Z = 1, 2pi, 6,")
    print("   and 5.789, and the framework's 5.789 comes from a Schwarzschild-BY-ANALOGY reading")
    print("   (R is not a real horizon; the 8pi/3 mismatch is absorbed by hand). So:")
    print("    * the residual posit is ONE O(1) factor (the '2'); most of Z is real Friedmann;")
    print("    * the data (Z in [5,7.1]) cannot separate 5.79 from 6 from 6.28;")
    print("    * Bridge 2 does NOT close -- the coefficient stays a posit. This is the honest")
    print("      result, and it COSTS the framework nothing: the 5σ-favored prediction is the")
    print("      EVOLUTION, which is Z-INDEPENDENT (a0(z)/a0(0)=E(z), Z cancels).")
    print("   What WOULD pin it: a unique matching principle (none is known) OR a0 measured to")
    print("   ~3% (currently ~20%), which would pick among 5.79 / 6 / 2pi. Neither exists yet.")


if __name__ == "__main__":
    main()
