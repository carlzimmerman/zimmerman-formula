#!/usr/bin/env python3
"""
DOOR A: derive a0 from de Sitter static-patch thermodynamics -- where it closes, where it breaks. Verified.
========================================================================================================
Goal: turn a0 = c^2 sqrt(Lambda/32pi) = cH/Z (Z=2sqrt(8pi/3)=5.789) from a dimensional-analysis ASSEMBLY into a
THERMODYNAMIC DERIVATION from the de Sitter horizon. Honest outcome stated plainly: the SCALE and the sqrt(Lambda)
dependence are FORCED; the exact coefficient Z is STRONGLY MOTIVATED and data-consistent but not uniquely forced
(it clusters with the thermal-Unruh 2pi at the ~8% level, the residual being the physical identification of the
relevant density/horizon).

THE TWO ROUTES (both genuine "gravity from the de Sitter horizon"):

  (a) UNRUH / de Sitter horizon temperature.
      de Sitter Gibbons-Hawking temperature  T_dS = hbar H / (2 pi k_B).
      Unruh:  an acceleration a has temperature  T = hbar a / (2 pi c k_B)  =>  a = 2 pi c k_B T / hbar.
      Feeding T_dS gives the horizon acceleration scale  a_hor = c H.
      Milgrom's coincidence identifies the MOND scale with the THERMAL scale:  a0 = c H / (2 pi).  Coefficient 2pi.

  (b) FRIEDMANN free-fall of the cosmic critical density.
      a0 = (c/2) sqrt(G rho_crit),  rho_crit = 3 H^2 / (8 pi G).
      = (c/2) H sqrt(3/8pi) = cH sqrt(3/32pi) = cH / sqrt(32pi/3) = cH / Z,  Z = 2 sqrt(8pi/3) = 5.789.
      Physical reading: c/2 (a horizon surface-gravity factor) times the free-fall rate sqrt(G rho) of the cosmic
      mean density. The 8pi is the Einstein coupling (forced by GR); the 3 is the Friedmann factor (forced); the
      1/2 is the surface-gravity convention (a choice). Coefficient Z.

WHAT IS FORCED vs CHOSEN:
  FORCED:   a0 proportional to c sqrt(Lambda) = cH (de Sitter). Robust across both routes and Verlinde's entropic
            derivation. This IS the horizon origin of the MOND scale.
  CHOSEN:   the exact O(1). Thermal-Unruh gives 2pi=6.283; Friedmann-free-fall gives Z=5.789. They agree to ~8%.
            The observed cH0/a0 (5.46 at H0=67.4 .. 5.91 at H0=73) actually sits ON Z and slightly BELOW 2pi,
            so the data mildly FAVOR the Friedmann coefficient -- but a0's ~20% error bar makes this soft.

VERDICT: the derivation CLOSES at the level of the scale and the sqrt(Lambda) dependence (genuine, not assembled);
it does NOT uniquely FORCE Z from below -- Z is the well-motivated Friedmann-free-fall value, one of a tight
cluster of O(1)~6 horizon coefficients, and the one the data prefer. Honest: strong, not airtight.
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34; kB = 1.381e-23
Z = 2*np.sqrt(8*np.pi/3)
a0_obs = 1.2e-10
Mpc = 3.086e22


def Hofkm(H0km):
    return H0km*1e3/Mpc


def main():
    print("#"*92)
    print("# DOOR A: deriving a0 from de Sitter static-patch thermodynamics")
    print("#"*92 + "\n")

    H0 = Hofkm(70.0)

    print("="*92); print("(a) UNRUH / de Sitter horizon temperature route"); print("="*92)
    T_dS = hbar*H0/(2*np.pi*kB)
    a_hor = 2*np.pi*c*kB*T_dS/hbar              # = c H0 (horizon acceleration scale)
    a0_unruh = c*H0/(2*np.pi)
    print(f"  T_dS = hbar H/(2pi kB) = {T_dS:.3e} K  (de Sitter Gibbons-Hawking temperature, H0=70)")
    print(f"  Unruh inversion a = 2pi c kB T/hbar = c H = {a_hor:.3e} m/s^2  (horizon accel scale)")
    print(f"  a0 = cH/(2pi) = {a0_unruh:.3e} m/s^2  (Milgrom thermal coincidence; coefficient 2pi={2*np.pi:.3f})\n")

    print("="*92); print("(b) FRIEDMANN free-fall of the critical density route"); print("="*92)
    rho_crit = 3*H0**2/(8*np.pi*G)
    a0_fried = (c/2)*np.sqrt(G*rho_crit)
    print(f"  rho_crit = 3H^2/8piG = {rho_crit:.3e} kg/m^3")
    print(f"  a0 = (c/2) sqrt(G rho_crit) = {a0_fried:.3e} m/s^2")
    print(f"  = cH/Z, Z = 2 sqrt(8pi/3) = {Z:.4f}.  check cH/Z = {c*H0/Z:.3e} m/s^2\n")

    print("="*92); print("COEFFICIENT SHOOT-OUT: which O(1) does the data pick?"); print("="*92)
    print(f"  {'route':<34}{'coefficient cH/a0':>20}")
    print(f"  {'Friedmann free-fall  Z':<34}{Z:>20.3f}")
    print(f"  {'thermal Unruh        2pi':<34}{2*np.pi:>20.3f}")
    print(f"  {'Verlinde-ish         6':<34}{6.0:>20.3f}")
    for H0km in (67.4, 70.0, 73.0):
        coeff = c*Hofkm(H0km)/a0_obs
        print(f"  {'OBSERVED cH0/a0 at H0='+str(H0km):<34}{coeff:>20.3f}")
    print(f"  => observed coefficient 5.46-5.91 sits ON Z={Z:.2f}, slightly BELOW 2pi={2*np.pi:.2f}: data mildly favor Z.")
    print(f"     (a0 ~20% uncertain, so 'favor' is soft. Z and 2pi agree to {100*abs(Z-2*np.pi)/(2*np.pi):.0f}%.)\n")

    print("="*92); print("VERDICT"); print("="*92)
    print("""  FORCED (the derivation genuinely closes): a0 proportional to c sqrt(Lambda) = cH -- the de Sitter horizon
  sets the MOND scale, via Unruh temperature AND via the Friedmann free-fall of the critical density AND via
  Verlinde's entropic displacement. This is a real horizon origin, not a dimensional-analysis assembly.
  NOT UNIQUELY FORCED (where it stops short): the exact coefficient. Z=2sqrt(8pi/3)=5.79 is the Friedmann-
  free-fall value -- 8pi from the Einstein coupling, 3 from Friedmann, 1/2 from the surface-gravity convention --
  sitting in a tight cluster with the thermal 2pi=6.28. The data (cH0/a0=5.5-5.9) land on Z and mildly prefer it
  over 2pi, but a0's error bar keeps this soft. Honest status: the scale is derived; Z is the data-preferred,
  well-motivated O(1), not an airtight first-principles constant.""")
    print("#"*92)


if __name__ == "__main__":
    main()
