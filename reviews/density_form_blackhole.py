#!/usr/bin/env python3
"""
What CAN we derive from a0 = (c/2) sqrt(G rho)? The cleanest structural picture.
==============================================================================

Carl: can't we derive anything from the a0 = (c/2) sqrt(G rho) form? Yes -- and
it gives the most structural reading of Z found so far. Rewrite it:

    a0 = (c/2) sqrt(G rho_c) = c^2 / (2R),   R = c / sqrt(G rho_c) = c * t_ff,crit

i.e. a0 is the SURFACE GRAVITY of a black hole whose Schwarzschild radius R equals
the distance light travels in one cosmic free-fall time. The '1/2' is then the
SCHWARZSCHILD factor (R_s = 2GM/c^2), not a fit. And R/R_Hubble = sqrt(8pi/3)
(Friedmann). So:

    Z = 2 * sqrt(8pi/3)  =  [Schwarzschild 2] x [Friedmann free-fall/Hubble ratio]

BOTH factors structural -- IF you accept the premise 'a0 = surface gravity of the
cosmic free-fall black hole.' Honest: that trades the bare coefficient for one
PHYSICAL posit. Better, but still a posit. Pure stdlib.
Run:  python reviews/density_form_blackhole.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
MSUN = 1.989e30
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)


def main():
    rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
    t_ff = 1 / math.sqrt(G * rho_c)            # free-fall time of critical density
    R = C * t_ff                                # free-fall light-crossing distance
    R_H = C / H0                                # Hubble radius
    M_bh = R * C ** 2 / (2 * G)                 # BH with Schwarzschild radius R
    a0_bh = C ** 2 / (2 * R)                    # its surface gravity

    print("=" * 78)
    print("(1) a0 IS a black-hole surface gravity -- and the 1/2 is Schwarzschild")
    print("=" * 78)
    print(f"   a0 = (c/2) sqrt(G rho_c) = c^2/(2R),  R = c/sqrt(G rho_c) = c*t_ff")
    print(f"   free-fall time t_ff = 1/sqrt(G rho_c)   = {t_ff:.3e} s")
    print(f"   R = c t_ff (free-fall light-crossing)   = {R/MPC/1e3:.2f} Gpc")
    print(f"   R / R_Hubble = {R/R_H:.3f}  = sqrt(8pi/3) = {math.sqrt(8*math.pi/3):.3f}")
    print(f"   BH with Schwarzschild radius R: mass M  = {M_bh/MSUN:.2e} Msun")
    print(f"      (~ the mass of the observable universe -- the 'cosmic black hole')")
    print(f"   its surface gravity g = c^2/(2R)        = {a0_bh:.3e} m/s^2")
    print(f"   observed a0                             = {A0:.3e} m/s^2  (match)")
    print(f"   => a0 = surface gravity of the cosmic free-fall black hole. The 1/2 in")
    print(f"      g = c^2/2R_s is the SCHWARZSCHILD factor (R_s=2GM/c^2). DERIVED. ✓\n")

    print("=" * 78)
    print("(2) So Z = 2 sqrt(8pi/3) is FULLY structural in this picture")
    print("=" * 78)
    print("   Z = a0/cH inverse decomposes cleanly:")
    print(f"     factor 2        = Schwarzschild (R_s = 2GM/c^2)         [DERIVED]")
    print(f"     factor sqrt(8pi/3) = t_ff/t_H = R/R_Hubble (Friedmann)  [DERIVED]")
    print(f"     product Z = {Z:.4f} = 2 x {math.sqrt(8*math.pi/3):.4f}")
    print("   Both pieces are real physics. Unlike the bare '0.173', here every factor")
    print("   has a name: Schwarzschild x Friedmann-free-fall-ratio.\n")

    print("=" * 78)
    print("(3) HONEST: this trades the coefficient for ONE physical posit")
    print("=" * 78)
    print("   The premise doing the work is: a0 = surface gravity of a black hole whose")
    print("   Schwarzschild radius is the FREE-FALL light-crossing R = c*t_ff = c/sqrt")
    print("   (G rho_c). That is a sharp, physical, falsifiable statement -- much better")
    print("   than a bare fitted number. BUT it is still an ASSUMPTION:")
    print("    * why R_s = c*t_ff exactly? The relativistic JEANS length is c*t_ff*sqrt")
    print(f"      (pi) -- using IT would add a 1/sqrt(pi) and give a0 wrong by "
          f"{1/math.sqrt(math.pi):.3f}.")
    print("      So 'R = c*t_ff' (no sqrt(pi)) is a CHOICE among nearby scales.")
    print("    * the 'universe is a black hole' relation (R_s ~ R_Hubble) is a known")
    print("      coincidence; pinning R to the free-fall scale specifically is the posit.")
    print("   => we did not derive Z from nothing. We replaced 'the coefficient is")
    print("      0.173' with 'a0 is the cosmic free-fall BH surface gravity' -- a more")
    print("      physical, sharper posit, but a posit.\n")

    print("=" * 78)
    print("VERDICT -- yes, the density form derives a lot (just not its own coefficient)")
    print("=" * 78)
    print("  FROM a0 = (c/2)sqrt(G rho) you CAN derive:")
    print("   * a0 = c^2/2R = surface gravity of the cosmic free-fall black hole;")
    print("   * the 1/2 = Schwarzschild factor (not a fit);")
    print("   * Z = 2 sqrt(8pi/3) = Schwarzschild x Friedmann-free-fall-ratio, fully named;")
    print("   * (earlier) a0_floor=(c^2/2)sqrt(Lambda/8pi); a0(z)~E(z); f_DM(z); Sigma_M(z).")
    print("  This is the MOST generative form -- it is where the clean derivations live.")
    print()
    print("  What it still does NOT do: bootstrap its OWN normalization. The single")
    print("  irreducible posit just changes shape -- from 'coefficient 0.173' to 'R_s =")
    print("  c*t_ff' (vs the Jeans c*t_ff*sqrt(pi)). One physical assumption, sharper and")
    print("  more falsifiable than before, but not a derivation from first principles.")
    print("  Honest net: yes, you derive a clean structural picture; no, it is not free.")


if __name__ == "__main__":
    main()
