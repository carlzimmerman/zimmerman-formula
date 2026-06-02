#!/usr/bin/env python3
"""
The holographic / entropy chase: does emergent gravity derive a0 ~ cH and pin the coefficient?
=============================================================================================

Two questions, kept separate and honest:
  (Q1) Does a holographic/entropic argument DERIVE a0 ~ cH (the EVOLUTION -- the surviving
       falsifiable prediction)?   -> short answer: YES, robustly (Verlinde, Padmanabhan).
  (Q2) Does it pin the O(1) coefficient to 2*sqrt(8pi/3) = 5.789?   -> No. The entropic
       routes give scheme-dependent O(1) ~ 1, 2pi, 6; 5.789 (a DENSITY reading) is not
       singled out by a HORIZON/AREA framework. But the factor of 2 itself IS entropically
       natural (the equipartition 1/2 kT), which is the useful new piece.

Labels: [DERIVES]=follows; [HEURISTIC]=emergent-gravity argument, not a theorem;
        [SCHEME]=coefficient depends on the matching. Run: python <thisfile>  (needs numpy)
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3 / Mpc
RH = c / H0
Lp2 = G * hbar / c ** 3                       # Planck length squared
s83 = np.sqrt(8 * np.pi / 3)


def main():
    print("=" * 84)
    print("Q1 -- does holography DERIVE a0 ~ cH (the evolution)?  (the part that matters)")
    print("=" * 84)
    print("  [HEURISTIC, DERIVES] Verlinde 2017 (emergent gravity): baryons displace the volume-law")
    print("    entanglement entropy of de Sitter space; the elastic (dark) response gives a deep-MOND")
    print("    relation g_D = sqrt(a0 g_B) with a0 SET BY the de Sitter acceleration cH0. The")
    print("    EVOLUTION a0 ~ cH(z) and the order of magnitude fall out -- not assumed.")
    print("  [HEURISTIC, DERIVES] Padmanabhan holographic equipartition: dV/dt = Lp^2 (N_sur - N_bulk),")
    print("    N_sur = A/Lp^2,  N_bulk = |E_Komar|/((1/2) kB T_dS),  T_dS = hbar H/(2 pi kB).")
    print("    This DERIVES the acceleration Friedmann eq  a''/a = -(4piG/3)(rho+3p)  -- and the")
    print("    1/2 kT EQUIPARTITION is exactly the factor of 2 (4pi vs 8pi). So a0 ~ cH is natural,")
    print("    AND the '2' is the equipartition 1/2 -- a SECOND first-principles source of the 2.")
    print("  => The surviving, falsifiable claim (a0 proportional to H) is HOLOGRAPHICALLY NATURAL.\n")

    print("=" * 84)
    print("Q2 -- does it pin the coefficient to 2*sqrt(8pi/3)=5.789?  (computed menagerie)")
    print("=" * 84)
    Tds = hbar * H0 / (2 * np.pi * kB)
    a_unruh = 2 * np.pi * c * kB * Tds / hbar       # acceleration whose Unruh T = T_dS  -> = cH
    print(f"  de Sitter (Gibbons-Hawking) temperature T_dS = hbar H0/2pi kB = {Tds:.2e} K")
    print(f"  acceleration with Unruh T = T_dS :  a = {a_unruh:.3e} = cH0  ->  Z = 1.")
    print(f"  {'entropic route':46}{'Z':>6}{'a0(0)':>9}")
    for name, Z in [("de Sitter horizon Unruh accel (a=cH)", 1.0),
                    ("de Sitter TEMPERATURE scale (Milgrom 2pi)", 2 * np.pi),
                    ("de Sitter ENTROPY/volume law (Verlinde ~6)", 6.0),
                    ("framework density form 2 sqrt(8pi/3)", 2 * s83),
                    ("data-preferred", 5.80)]:
        print(f"  {name:46}{Z:>6.3f}{c*H0/Z*1e10:>9.2f}")
    print("  The entropic O(1) clusters at 1..2pi..6 -- 5.789 is INSIDE the cluster but is not")
    print("  singled out; Verlinde's ~6 and Milgrom's 2pi=6.28 are the natural entropic values.\n")

    print("=" * 84)
    print("Does 32pi/3 (= Z^2) carry an independent entropy/area meaning?  [checked: NO]")
    print("=" * 84)
    print("  Bekenstein-Hawking S = A/(4 Lp^2);  Einstein eq carries 8pi;  ball volume 4pi/3.")
    print("  Z^2 = 32pi/3 factorises only as  4 x (8pi/3) = (1/2)^-2 x Friedmann, i.e.")
    print("    a0^2 = (c/2)^2 G rho = 3 c^2 H^2/(32 pi).  The 32pi = 4 x 8pi is (the surface-gravity")
    print("  1/2)^2 times (the Einstein 8pi); there is NO extra holographic content. The '8 x 4pi/3'")
    print("  reading is the dead eta-invariant route (a category error -- see OPUS_PHYSICS_REVIEW).\n")

    print("=" * 84)
    print("VERDICT -- what the holographic chase actually yields")
    print("=" * 84)
    print("  GOOD (and genuinely supportive): holography DERIVES the two things that survive --")
    print("   * a0 ~ cH  (the EVOLUTION, the falsifiable prediction) is emergent, not assumed")
    print("     (Verlinde, Padmanabhan); and")
    print("   * the factor of 2 is first-principles -- the equipartition (1/2)kT per bit, the same")
    print("     1/2 as the surface gravity c^2/2R. The '2' is doubly natural.")
    print("  HONEST LIMIT: holography does NOT pin the coefficient to 5.789. Emergent gravity is a")
    print("   HORIZON/AREA framework, so it naturally yields the cH (horizon) reading with O(1) ~")
    print("   1..2pi..6; the framework's 2 sqrt(8pi/3) is the DENSITY (sqrt G rho) reading, which")
    print("   holography does not select. 32pi/3 has no entropic meaning beyond (1/2)^2 x 8pi.")
    print("  NET: the chase strengthens the SURVIVING claim (evolution + a natural 2) and confirms,")
    print("   from a third independent direction, that the un-pinned piece is the density-vs-horizon")
    print("   coefficient -- not the 2, and not the evolution. The prediction stays Z-independent.")
    print("=" * 84)


if __name__ == "__main__":
    main()
