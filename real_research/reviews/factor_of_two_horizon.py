#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
Did you have the horizon argument for the factor of 2 in Z = 2 sqrt(8pi/3)?
==========================================================================

Carl: 'I thought I had the a_horizon thing for the 2.' Let us reconstruct it
carefully -- because there IS a clean horizon argument that gives a factor of 2,
and it is worth seeing exactly what it delivers and where it falls short.

Target:  a0 = cH/Z,  Z = 2 sqrt(8pi/3) = 5.789.  Equivalently a0 = (c/2)sqrt(G rho_c).
Question: does the de Sitter / Hubble horizon supply the '2'?

Pure stdlib. Run:  python reviews/factor_of_two_horizon.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
A0_OBS = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)
cH0 = C * H0


def main():
    rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
    c_sqrt_Grho = C * math.sqrt(G * rho_c)         # the 'density' acceleration
    a0_framework = 0.5 * c_sqrt_Grho               # = (c/2) sqrt(G rho_c)

    print("=" * 78)
    print("(1) YOUR ARGUMENT, RECONSTRUCTED -- and it IS a real horizon factor of 2")
    print("=" * 78)
    R_H = C / H0
    M_c = rho_c * (4 * math.pi / 3) * R_H ** 3      # critical mass in the Hubble sphere
    g_surface = G * M_c / R_H ** 2                  # its surface gravity at R_H
    print("   The critical mass inside the Hubble sphere R_H = c/H:")
    print(f"     M_c = rho_c (4pi/3) R_H^3")
    print("   Its Newtonian surface gravity at the horizon:")
    print(f"     g = G M_c / R_H^2 = (4pi/3) G rho_c R_H")
    print(f"   Substituting rho_c = 3H^2/(8piG):")
    print(f"     g = (4pi/3)(3/8pi) H^2 R_H = (1/2) cH")
    print(f"   THE 1/2 = (4pi/3)/(8pi/3) = ball-volume / Friedmann-coefficient. CLEAN.")
    print(f"     g (computed) = {g_surface:.3e} m/s^2 ;  cH/2 = {cH0/2:.3e}  (match)")
    print("   => YES: the horizon DOES give a clean factor of 2. You had this. ✓\n")

    print("=" * 78)
    print("(2) THE CATCH: that '2' gives a0 = cH/2, which OVERSHOOTS the data")
    print("=" * 78)
    print(f"   horizon-2 value:  a0 = cH/2     = {cH0/2:.3e} m/s^2")
    print(f"   observed:         a0            = {A0_OBS:.3e} m/s^2")
    print(f"   overshoot factor: {(cH0/2)/A0_OBS:.3f}  =  sqrt(8pi/3) = {math.sqrt(8*math.pi/3):.3f}")
    print("   The horizon-2 is too BIG by exactly sqrt(8pi/3). To reach a0 you still")
    print("   need an EXTRA factor of sqrt(8pi/3) -- so Z = 2 x sqrt(8pi/3), not 2.\n")

    print("=" * 78)
    print("(3) WHY: there are TWO different '2's, on TWO different base accelerations")
    print("=" * 78)
    print(f"   cH (Hubble accel)        = {cH0:.3e}")
    print(f"   c sqrt(G rho_c) (density)= {c_sqrt_Grho:.3e}   (smaller by sqrt(8pi/3))")
    print(f"   note  cH = sqrt(8pi/3) x c sqrt(G rho_c)  ->  ratio "
          f"{cH0/c_sqrt_Grho:.3f} = {math.sqrt(8*math.pi/3):.3f}")
    print()
    print(f"   YOUR 2:       a0 = cH/2          = (1/2) on the HUBBLE accel  -> {cH0/2:.2e}")
    print(f"   FRAMEWORK 2:  a0 = (c/2)sqrt(Grho)= (1/2) on the DENSITY accel -> {a0_framework:.2e}")
    print(f"   cH/2 in density units = {(cH0/2)/c_sqrt_Grho:.3f} x c sqrt(G rho_c)  (NOT 0.5)")
    print("   => the horizon surface-gravity '2' sits on cH; the framework '2' sits on")
    print("      c sqrt(G rho_c). They are DIFFERENT factors. The horizon-2 does not")
    print("      become the framework-2 -- the sqrt(8pi/3) is the gap between the bases.\n")

    print("=" * 78)
    print("(4) Reconcile with desitter_factor_audit.py")
    print("=" * 78)
    print("   The horizon offers a SMALL menu of O(1) factors on cH:")
    print(f"     surface gravity of horizon itself : 1     -> a0=cH   = {cH0:.2e} (5.8x high)")
    print(f"     enclosed-critical-mass (YOUR 2)    : 2     -> a0=cH/2 = {cH0/2:.2e} (2.9x high)")
    print(f"     Gibbons-Hawking temperature        : 2pi   -> a0=cH/2pi = {cH0/(2*math.pi):.2e} (0.9x, BEST)")
    print(f"     FRAMEWORK Z=2sqrt(8pi/3)           : 5.789 -> a0      = {cH0/Z:.2e} (exact)")
    print("   Your factor-2 is real but it OVERSHOOTS; the horizon number that actually")
    print("   FITS is 2pi (temperature), and the framework's 5.789 sits between 2pi and")
    print("   nothing else horizon-y -- it is the GEOMETRIC sqrt(32pi/3), not a horizon O(1).\n")

    print("=" * 78)
    print("VERDICT -- you did have a horizon-2; it just is not the one that lands a0")
    print("=" * 78)
    print("  HONEST yes: the surface gravity of the Hubble-enclosed critical mass is")
    print("  cH/2 -- a clean, real, horizon-derived factor of 2 (the 1/2 = ball/Friedmann).")
    print("  You remembered a genuine argument.")
    print()
    print("  BUT it gives a0 = cH/2 = 3.5e-10, which is sqrt(8pi/3) = 2.9x too big. The")
    print("  observed a0 needs Z = 2 sqrt(8pi/3): the horizon-2 plus a SEPARATE sqrt(8pi/3)")
    print("  that the same argument does not supply. And the framework '2' lives on a")
    print("  different base (c sqrt(G rho_c), not cH), so it is not literally that horizon-2.")
    print()
    print("  Bottom line: the de Sitter horizon DOES hand you a factor of 2 -- it just")
    print("  does not hand you a0. The clean horizon value that fits is 2pi (cH/2pi); the")
    print("  exact Z = 2 sqrt(8pi/3) remains a geometric number, the O(1) still unfixed.")


if __name__ == "__main__":
    main()
