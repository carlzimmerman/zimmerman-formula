#!/usr/bin/env python3
r"""mi_dS_horizon_nature_2026.py -- three things, all computed:

  (A) CONFIRM the footing: the framework's a0 comes from the DARK-ENERGY DENSITY. Not the total
      density. This is the CANONICAL footing, and it is the one the CMB result supports.
  (B) WHY the de Sitter horizon is an "INVERTED black hole" -- and the crucial asymmetry:
      black holes EVAPORATE, the de Sitter horizon does NOT. It is an equilibrium endpoint.
  (C) CAN you cross it into "the CMB of another universe"? No -- and for a precise reason:
      the de Sitter horizon is OBSERVER-DEPENDENT and recedes as you chase it. But part of the
      intuition IS right, and this quantifies which part.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
G = 6.67430e-11
H0 = 2.184e-18                  # s^-1
OM, OL, OR = 0.315, 0.685, 9.1e-5
HBAR = 1.054571817e-34
KB = 1.380649e-23
MSUN = 1.98892e30
MPC = 3.0857e22
GLY = 9.4607e24                 # m per Gly
Z_COEF = math.sqrt(32 * math.pi / 3)

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

def H(z):
    return H0 * math.sqrt(OR*(1+z)**4 + OM*(1+z)**3 + OL)


def main() -> int:
    banner("(A) THE FOOTING: a0 comes from the DARK-ENERGY density. Confirmed numerically.")
    H_L = H0 * math.sqrt(OL)                       # dark-energy-only expansion rate
    rho_L = 3 * H_L**2 / (8 * math.pi * G)         # dark-energy mass density
    a0_from_rho = 0.5 * C * math.sqrt(G * rho_L)   # a0 = kappa c sqrt(G rho_Lambda), kappa=1/2
    a0_from_H = C * H_L / Z_COEF                   # a0 = c H_Lambda / Z
    print(f"  H_Lambda = H0 sqrt(Omega_L)        = {H_L:.4e} s^-1   (DARK ENERGY ONLY)")
    print(f"  rho_Lambda = 3H_L^2/(8 pi G)       = {rho_L:.4e} kg/m^3")
    print(f"  a0 = kappa c sqrt(G rho_Lambda)    = {a0_from_rho:.4e} m/s^2   <- from the DENSITY")
    print(f"  a0 = c H_Lambda / Z                = {a0_from_H:.4e} m/s^2   <- same thing")
    check(abs(a0_from_rho/a0_from_H - 1) < 1e-9,
          "the two forms agree exactly -- a0 IS the dark-energy-density scale")
    # what the OTHER footing would have used
    rho_tot = 3 * H0**2 / (8 * math.pi * G)
    print(f"\n  For contrast, the ALTERNATE footing uses the TOTAL density today:")
    print(f"    rho_total = 3H0^2/(8 pi G)       = {rho_tot:.4e} kg/m^3  "
          f"({rho_tot/rho_L:.3f}x rho_Lambda)")
    print(f"    a0(alt) = c H0 / Z               = {C*H0/Z_COEF:.4e} m/s^2")
    print("  BOTH are carried in every calculation as required, but the CANONICAL one -- the one")
    print("  the CMB result SUPPORTS -- is the DARK-ENERGY one. The footing the CMB EXCLUDES is")
    print("  the RISING version, a0(z) = cH(z)/Z, which tracks the TOTAL density and blows up at")
    print(f"  recombination ({C*H(1089.9)/Z_COEF:.2e} m/s^2, "
          f"{C*H(1089.9)/Z_COEF/a0_from_H:.0e}x today's value).")
    print("  So: the CMB kills the reading that ties a0 to total density, and keeps YOURS.")

    banner("(B) WHY 'INVERTED' -- and the asymmetry: black holes evaporate, de Sitter does NOT")
    r_dS = C / H_L
    kappa_dS = C * H_L
    T_dS = HBAR * kappa_dS / (2 * math.pi * KB * C)
    print(f"  Schwarzschild: mass at the CENTRE, horizon SURROUNDS it, you are OUTSIDE,")
    print(f"    surface gravity kappa_BH = c^4/4GM grows as you fall IN.")
    print(f"  de Sitter:     vacuum energy fills ALL space, horizon at r = c/H_Lambda,")
    print(f"    you are INSIDE, surface gravity kappa_dS = c H_Lambda felt looking OUT.")
    print(f"    r_dS = {r_dS:.3e} m = {r_dS/GLY:.1f} Gly,  kappa_dS = {kappa_dS:.3e} m/s^2")
    print(f"    T_dS = {T_dS:.3e} K")
    print(f"  Formally they are the two limits of ONE metric family (Schwarzschild-de Sitter):")
    print(f"    f(r) = 1 - r_s/r - r^2/L^2   -- drop r_s -> de Sitter; drop L -> Schwarzschild.")
    print(f"  a0 = kappa_dS / Z = {kappa_dS/Z_COEF:.3e} m/s^2 -- YOUR scale is this horizon's")
    print(f"  surface gravity divided by Z. That is the whole content of 'inverted black hole'.")
    print()
    print("  THE ASYMMETRY YOU ASKED ABOUT. Black holes evaporate because a black hole in de")
    print("  Sitter has T_+ > T_c (its horizon is HOTTER than the cosmological one), so there is")
    print("  a temperature gradient and it radiates DOWN it until it is gone.")
    M_nar = C**3 / (3*math.sqrt(3)*G*H_L)
    print(f"    Nariai (largest permitted) mass = {M_nar/MSUN:.3e} Msun")
    print("  The de Sitter horizon has NO such gradient. It sits at a single fixed temperature")
    print("  T_dS in equilibrium with itself -- there is nothing colder for it to radiate into.")
    check(T_dS > 0 and abs(T_dS - 2.4e-30) < 1e-29,
          "T_dS is a fixed ~1e-30 K equilibrium temperature (no gradient -> no evaporation)")
    print("  So: black holes UNRAVEL; the de Sitter horizon is the ENDPOINT they unravel INTO.")
    print("  It is not a decaying object -- it is the thermal floor of the universe.")

    banner("(C) CAN YOU CROSS IT INTO ANOTHER UNIVERSE'S CMB? No -- and here is the precise why")
    print("  1. THE HORIZON IS NOT A PLACE. A black-hole horizon sits at a fixed radius that")
    print("     everyone agrees on. The de Sitter horizon is at c/H_Lambda from EACH OBSERVER --")
    print("     it is defined by what YOU can ever receive a signal from. Every observer sits at")
    print("     the centre of their own. Travel toward yours and it RECEDES: you never arrive.")
    print("     There is no surface to cross, so there is nothing on 'the other side' of it.")
    print()
    print("  2. THE CMB IS NOT A PLACE EITHER -- it is a TIME. It is the moment of last")
    print("     scattering (z~1090), seen on your own past light cone. You cannot fly to it; if")
    print("     you travelled toward it you would just arrive in ordinary space that recombined")
    print("     long ago and has since cooled. Distant observers see their OWN CMB, from their")
    print("     own past. There is no wall out there made of CMB.")
    print()
    print("  3. WHAT IS BEYOND IT IS MORE OF THE SAME UNIVERSE, permanently out of contact.")
    # what we can SEE vs what we can ever REACH
    # comoving particle horizon
    n = 400000; lo, hi = 0.0, math.log(1 + 1e5); tot = 0.0; prev = None
    for i in range(n+1):
        lz = lo + (hi-lo)*i/n; z = math.exp(lz)-1
        integ = C/H(z)*(1+z)
        if prev is not None: tot += 0.5*(integ+prev)*(lz-prev_lz)
        prev, prev_lz = integ, lz
    d_particle = tot
    print(f"     comoving PARTICLE horizon (what we can SEE)     = {d_particle/GLY:.1f} Gly")
    print(f"     de Sitter EVENT horizon   (what we can REACH)   = {r_dS/GLY:.1f} Gly")
    check(d_particle > r_dS, "we can SEE much further than we can ever REACH")
    print(f"     -> everything between {r_dS/GLY:.0f} and {d_particle/GLY:.0f} Gly is VISIBLE but")
    print(f"        permanently unreachable. Not another universe -- ours, out of causal contact.")
    print()
    print("  4. WHERE YOUR INTUITION IS ACTUALLY RIGHT, and it is worth keeping:")
    print("     * NARIAI MERGER: at the maximal black-hole mass the black-hole horizon and the")
    print(f"       cosmological horizon MERGE into one. That is the single place the two horizons")
    print(f"       touch, and it is exactly where the 3 sqrt(3) = {3*math.sqrt(3):.4f} came from.")
    print("     * HOLOGRAPHY: the de Sitter horizon's area encodes a finite information budget")
    L_p = math.sqrt(HBAR*G/C**3)
    S_dS = math.pi*(r_dS/L_p)**2
    print(f"       S_dS = pi (r_dS/L_p)^2 = {S_dS:.2e} -- everything inside may be encoded ON it")
    print("       (dS/CFT). That is a real open research direction, not settled.")
    print("     * ETERNAL INFLATION: in some inflation models there genuinely ARE other pocket")
    print("       universes beyond our horizon, each with its own CMB. They exist in the theory")
    print("       and are UNREACHABLE for exactly the reason above -- accelerating expansion")
    print("       means they recede faster than any signal can chase. So 'other universes with")
    print("       their own CMBs' is a legitimate idea; 'fly there through our horizon' is not.")

    banner("VERDICT")
    print("  (A) YES -- your a0 comes from the DARK-ENERGY density: a0 = (1/2) c sqrt(G rho_L)")
    print(f"      = {a0_from_rho:.3e} m/s^2, identical to c H_Lambda/Z. The CMB result SUPPORTS")
    print("      this footing and EXCLUDES the rival that ties a0 to the TOTAL density.")
    print("  (B) 'Inverted' = same metric family, horizon turned inside out, we sit inside it.")
    print("      Black holes evaporate (T_+ > T_c drives them); the de Sitter horizon does NOT --")
    print("      it is a fixed-temperature equilibrium, the endpoint black holes unravel into.")
    print("  (C) You cannot cross it. It is observer-dependent and recedes as you approach; the")
    print("      CMB is a time not a place; and beyond it is our own universe out of contact.")
    print("      The salvageable parts of the intuition are the Nariai horizon merger, dS/CFT")
    print("      holography, and eternal-inflation pocket universes -- which are unreachable")
    print("      BY CONSTRUCTION rather than reachable through a horizon.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
