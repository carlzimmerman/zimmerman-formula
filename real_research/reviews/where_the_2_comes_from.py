#!/usr/bin/env python3
"""
Where does the factor of 2 in Z = 2*sqrt(8pi/3) come from, and where does it make sense?
========================================================================================

a0 = (c/2) sqrt(G rho_c) = c^2/(2R),  R = c/sqrt(G rho_c).

Claim to test: the "2" is NOT the mysterious part. It is the universal horizon/Schwarzschild
factor (every surface gravity, Schwarzschild radius, escape velocity, and the EdS deceleration
carries it). The genuine freedom is the RADIUS at which it is applied -- the free-fall scale
sqrt(8pi/3) R_H rather than the causal horizon R_H. We compute the whole catalog.

Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3 / Mpc
rho = 3 * H0 ** 2 / (8 * np.pi * G)
RH = c / H0
s83 = np.sqrt(8 * np.pi / 3)        # 2.894


def main():
    print("=" * 82)
    print("CATALOG -- every factor of 2 in gravity, and the a0-coefficient Z it implies")
    print("=" * 82)
    print("  (Z is defined by a0 = cH/Z, so a0 = the listed Hubble-scale acceleration => its Z)")
    print(f"  {'where the 2 lives':46}{'the 2 is in':14}{'Z':>5}")
    rows = [
        ("Schwarzschild radius   R_s = 2GM/c^2",            "numerator", "-"),
        ("Surface gravity        kappa = c^2/(2R_s) = cH/2", "denominator", "2"),
        ("Escape velocity        v_esc = sqrt(2GM/R)=c@R_H", "under sqrt", "2"),
        ("EdS deceleration       q = 1/2  (4pi vs 8pi)",     "two Friedmann eqs", "2"),
        ("Newtonian g(R_H)=GM/R_H^2 = cH/2 (uses M=R_s)",    "via R_s=2GM/c^2", "2"),
        ("Unruh/de Sitter temp   T = hbar a/(2 pi c)",       "the 2pi", "6.28"),
    ]
    for name, where, Z in rows:
        print(f"  {name:46}{where:14}{Z:>5}")
    print("  -> EVERY clean horizon-scale acceleration carries the SAME factor of 2 and gives")
    print("     Z = 2 (a0 = cH/2). The de Sitter TEMPERATURE route gives 2pi (Milgrom). So the")
    print("     '2' is the standard surface-gravity/horizon factor -- it is NOT arbitrary.\n")

    print("=" * 82)
    print("THE REFRAME -- the framework's a0 IS a surface gravity; the freedom is the RADIUS")
    print("=" * 82)
    R_fw = c / np.sqrt(G * rho)
    a0 = c ** 2 / (2 * R_fw)
    print(f"  a0 = c^2/(2R) with R = c/sqrt(G rho) = {R_fw/RH:.3f} R_H = sqrt(8pi/3) R_H.")
    print(f"     the c^2/(2R) is LITERALLY the surface-gravity formula -- the 2 is forced.")
    print(f"     the choice is R: the FREE-FALL light-crossing radius (c * t_ff), which is")
    print(f"     sqrt(8pi/3) = {s83:.3f} times the Hubble/causal horizon R_H.")
    print(f"  So Z = 2 * sqrt(8pi/3):")
    print(f"     the '2'          = surface-gravity / horizon factor  (universal, forced)")
    print(f"     the 'sqrt(8pi/3)'= R_freefall / R_Hubble = H/sqrt(G rho)  (the actual posit)")
    print(f"  a0 = c^2/2R = {a0*1e10:.2f}e-10  (Z = {c*H0/a0:.3f}). The 2 did its usual job; the")
    print(f"  open question is WHY the free-fall radius, not the horizon (which gives Z=2).\n")

    print("=" * 82)
    print("WHERE THE 2 'MAKES SENSE' -- ranked")
    print("=" * 82)
    print("  1. SURFACE GRAVITY (best): a0 = c^2/2R is the horizon surface-gravity form. The 2 is")
    print("     exactly the Schwarzschild kappa = c^2/2R_s factor. Clean and forced -- the only")
    print("     gap is that R is the free-fall scale, not a causal horizon.")
    print("  2. ESCAPE / 'half the binding': v_esc^2 = 2GM/R. The same 2 (it IS the Schwarzschild")
    print("     2). a0 ~ the acceleration whose work over R equals (1/2) v_esc^2-style energy.")
    print("  3. KINEMATIC: a0 = (c/2)/t_ff -- reaches v=c/2 in one free-fall time. Heuristic but")
    print("     clean (the 1/2 = 'half light speed in a dynamical time').")
    print("  4. EdS DECELERATION q=1/2: a genuine GR factor of 1/2 (acceleration vs energy")
    print("     Friedmann equation), but it lands on Z=2, not 5.789.")
    print()
    print("  CONCLUSION: the factor of 2 is the universal horizon surface-gravity 1/2 -- it is the")
    print("  LEAST mysterious part of the coefficient and it makes complete physical sense. The")
    print("  real, un-derived choice is the RADIUS/RATE: using the local free-fall rate sqrt(G rho)")
    print("  (R = sqrt(8pi/3) R_H) instead of the causal-horizon Hubble rate H (R = R_H, Z=2, which")
    print("  the data exclude). Re-aim the 'why' at sqrt(8pi/3), not at the 2.")
    print("=" * 82)


if __name__ == "__main__":
    main()
