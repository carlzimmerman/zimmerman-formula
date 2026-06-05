#!/usr/bin/env python3
"""
Resolving the rho_DE-vs-rho_total fork, and the consistency of the faithful (declining) reading. a0(z) = a DE probe.
====================================================================================================================
Two results that consolidate the dark-energy-tracking reading (THE_DARK_ENERGY_TRACKING_READING.md):

(1) THE FORK RESOLVES toward sqrt(rho_DE). The two forms a0=cH(z)/Z [~sqrt rho_total] and a0=c^2 sqrt(Lam/32pi)
    [~sqrt rho_DE, constant] agree ONLY at z=0 (the cH0 ~ c^2 sqrt(Lam) 'why-now' coincidence) and diverge in the
    past. The framework's DEEP structures -- the de Sitter horizon, the CKN bound, the cosmic seesaw, the 32pi
    itself -- all tie a0 to LAMBDA = rho_DE. Conceptually a0 is 'MOND as a vacuum effect' (Milgrom), a vacuum/dark-
    energy scale, not a total-density scale; and the DATA (Limbach 2008, Milgrom 2017) disfavor the rising rho_total
    form. So BOTH the framework's own logic and the data select a0 ~ sqrt(rho_DE). cH(z)/Z was the Friedmann
    packaging mistaken for the fundamental law by over-extrapolating the today-coincidence.

(2) THE FAITHFUL (declining-under-DESI) READING IS CLEANER ON CONSISTENCY:
    * CMB: a0(z=1100) ~ 0.7% of today (rho_DE -> 0 in the phantom past) -> early universe Newtonian, CMB trivially
      safe -- even cleaner than the Hubble version (which needed gradient suppression to tame a huge a0).
    * CLUSTERS: residual D ~ a0 DECLINES at high z (0.81 at z=2) -> the MOND cluster discrepancy SHRINKS, reversing
      the Hubble version's worsening. A genuine improvement on the one front that had gotten worse.
    * sigma8: a0 absent from LINEAR growth (O(delta^3)) so linear sigma8 unchanged; the NONLINEAR enhancement
      weakens as a0 declines -> HELPS the low-S8 tension, but WEAKENS the El Gordo/high-tail pro-MOND argument. A
      genuine trade-off (a soft, contested win for help on a real tension).

REFRAME: a0(z) tracks the dark-energy density, so a0(z) is a GALAXY-SCALE PROBE OF DARK ENERGY -- measuring a0 at
z~3 tests whether DE is constant (a0 flat) or evolving (a0 ~ 0.7x). HONEST: the distinctive (declining) branch is
contingent on DESI (~2-4 sigma, contested); under constant Lambda the reading is just the safe constant core. Needs
numpy.
"""
import numpy as np

Om,OL=0.315,0.685; c=2.998e8; Mpc=3.086e22; H0=67.4e3/Mpc; Z=2*np.sqrt(8*np.pi/3)
Lam=3*OL*H0**2/c**2; E=lambda z: np.sqrt(Om*(1+z)**3+OL)
w0,wa=-0.83,-0.75
rhoDE=lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
a0DE=lambda z: np.sqrt(rhoDE(1/(1+z)))
a0_geom=c**2*np.sqrt(Lam/(32*np.pi))


def main():
    print("#"*96); print("# Resolving the rho_DE-vs-rho_total fork; consistency of the faithful reading; a0(z)=a DE probe"); print("#"*96+"\n")

    print("="*96); print("(1) THE FORK: the two forms agree only at z=0, diverge in the past -> select sqrt(rho_DE)"); print("="*96)
    print(f"  {'z':>4}{'a0=cH(z)/Z':>16}{'a0=c^2 sqrt(Lam/32pi)':>24}{'ratio':>8}")
    for z in (0,1,2,3):
        print(f"  {z:>4}{c*H0*E(z)/Z:>16.3e}{a0_geom:>24.3e}{(c*H0*E(z)/Z)/a0_geom:>8.2f}")
    print("  deep structures (de Sitter, CKN, seesaw, 32pi) tie a0 to LAMBDA=rho_DE; conceptually 'MOND as a vacuum")
    print("  effect' (Milgrom); data (Limbach/Milgrom) disfavor the rising rho_total form. => a0 ~ sqrt(rho_DE).\n")

    print("="*96); print("(2) CONSISTENCY of the faithful sqrt(rho_DE)+DESI reading (a0 DECLINES at high z)"); print("="*96)
    print(f"  CMB:      a0(z=1100)/a0(0) = {a0DE(1100):.4f}  -> ~0.7% of today -> early universe Newtonian -> trivially safe.")
    print(f"  CLUSTERS: D(z)/D0 ~ a0 = {a0DE(0.5):.2f},{a0DE(1):.2f},{a0DE(2):.2f} at z=0.5,1,2 -> discrepancy SHRINKS at high z -> IMPROVES.")
    print(f"  sigma8:   linear unchanged (a0 is O(delta^3)); nonlinear enhancement weakens -> helps low-S8, weakens El Gordo. Trade-off.\n")

    print("="*96); print("REFRAME + VERDICT"); print("="*96)
    print(f"""  a0(z) TRACKS THE DARK-ENERGY DENSITY. The framework's faithful formula a0=(c/2)sqrt(G rho_Lambda) makes a0 a
  GALAXY-SCALE PROBE OF DARK ENERGY: constant if Lambda is constant; a mild decline (a0~{a0DE(3):.2f} at z=3) if dark
  energy evolves as DESI hints. Both the framework's deep structure (de Sitter/CKN/seesaw) and the data select this
  sqrt(rho_DE) reading over the rising sqrt(rho_total) one, and the declining reading is CLEANER on consistency --
  CMB trivially safe (a0->0 early), clusters improved (discrepancy shrinks), sigma8 a favorable trade-off. HONEST:
  the distinctive declining branch is contingent on DESI (contested); under constant Lambda it is the safe constant
  core; and it trades the soft El Gordo win for help on low-S8. Net: the framework's most faithful, most data-
  consistent, and cleanest-on-consistency reading is 'a0 tracks dark energy' -- and that makes a0(z) a new, testable
  probe of whether dark energy evolves.""")
    print("#"*96)


if __name__=="__main__":
    main()
