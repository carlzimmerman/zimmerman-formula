#!/usr/bin/env python3
"""
DESI x MOND: the measured dark-energy evolution turns a0(z) into a PREDICTION (a novel cross-test).
==================================================================================================
A unifying consequence for the emergent-horizon TOE. Milgrom's a0-cosmology connection says MOND and dark
energy come from the SAME term, controlled by a0, with a0 ~ cH0 ~ c^2 sqrt(Lambda). If a0 tracks the dark-
energy density -- a0 ~ c sqrt(rho_DE) (the event-horizon / sqrt(Lambda) reading) -- then DESI's MEASURED
evolution of dark energy DIRECTLY PREDICTS the evolution of the galaxy-scale MOND acceleration a0(z). It is no
longer a free dial. DESI DR2 (2025) + SNe prefers EVOLVING dark energy (w0 > -1, wa < 0) over a constant
Lambda at 2.8-4.2 sigma, so this is a live, data-driven prediction.

a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)),  rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)).

Three distinct, NOW DATA-DRIVEN branches (which horizon sources a0):
  apparent horizon  a0 ~ cH(z)        : RISES steeply, ~E(z) (x4.6 at z=3)   -- disfavored by high-z disks
  event horizon     a0 ~ c sqrt(rhoDE): with DESI w0wa, DECLINES mildly (~0.65-0.78x at z=3, non-monotonic)
  geometric mean    a0 ~ c sqrt(H H_L): mild rise (~2x at z=3)               -- survives

The high-z rotation-curve evidence (Big Wheel etc.: a0 NOT risen x5; massive disks baryon-dominated) favors the
EVENT-horizon/declining or the MILD branches over the steep apparent-horizon rise -- and the event-horizon
branch now carries a concrete DESI-fixed SHAPE that is independently falsifiable with clean z~1-3 disks.

HONEST CAVEATS: (1) a0 ~ c sqrt(rho_DE) (the "same term") is Milgrom's CONJECTURE (FUNDAMOND), not derived.
(2) DESI's evolving DE is 2.8-4.2 sigma and SNe-combination-dependent (Pantheon+ vs Union3 vs DES) -- not
settled. (3) the DSSYK = de Sitter dual assumes CONSTANT Lambda; an evolving-DE dual is an open problem (the
T^2-deformed DSSYK of Aguilar-Gutierrez 2026 is an early step toward moving off exact de Sitter). So this is a
falsifiable UNIFYING prediction of the program, flagged as conjecture-dependent -- not an established result.
Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
ELCDM = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def rho_de(z, w0, wa):
    a = 1/(1+z)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))


def main():
    print("#"*92)
    print("# DESI x MOND -- evolving dark energy PREDICTS a0(z) (a novel falsifiable cross-test)")
    print("#"*92 + "\n")

    print("="*92); print("a0(z)/a0(0) under each horizon reading; DESI w0wa makes the event-horizon branch concrete"); print("="*92)
    combos = [("-0.80", "-0.70", -0.80, -0.70), ("-0.75", "-1.00", -0.75, -1.00)]
    print(f"  {'z':>5}{'apparent ~H':>13}{'event ~sqrt(rhoDE) [w0,wa]':>30}{'constant':>10}")
    print(f"  {'':>5}{'(xE(z))':>13}{'DESI('+combos[0][0]+','+combos[0][1]+')  DESI('+combos[1][0]+','+combos[1][1]+')':>30}{'Lambda':>10}")
    for z in (0.3, 0.5, 1.0, 2.0, 3.0):
        e = ELCDM(z)
        r1 = np.sqrt(rho_de(z, *combos[0][2:]))
        r2 = np.sqrt(rho_de(z, *combos[1][2:]))
        print(f"  {z:>5.1f}{e:>13.2f}{r1:>16.2f}{r2:>14.2f}{1.0:>10.2f}")
    print()

    print("="*92); print("WHAT IT MEANS"); print("="*92)
    print("""  Milgrom: MOND and dark energy are the SAME term, controlled by a0 ~ c sqrt(Lambda). DESI now MEASURES
  that "Lambda" evolving. So a0(z) is PREDICTED, branch by branch:
   * apparent horizon (a0~cH): steep rise to ~4.6x at z=3. The high-z disks (a0 NOT risen x5; baryon-dominated)
     DISFAVOR this -- the framework's original headline bet.
   * event horizon (a0~sqrt(rho_DE)): with DESI's evolving DE this DECLINES mildly (rho_DE was lower in the
     quintessence past), ~0.65-0.78x at z=3, slightly non-monotonic (a small bump near z~0.4 then fall). This
     is CONSISTENT with massive high-z disks being baryon-dominated (lower a0 = more Newtonian).
   * geometric mean (a0~sqrt(H H_L)): mild rise ~2x at z=3 -- also survives.
  => DESI converts "does a0 rise?" into "WHICH horizon sources a0?", a sharper, data-anchored question, and
     ties the galaxy-scale MOND scale to a cosmological measurement for the first time.\n""")

    print("="*92); print("VERDICT -- honest"); print("="*92)
    print("""  A genuine UNIFYING, falsifiable cross-prediction of the emergent-horizon program: DESI's evolving dark
  energy + the a0 ~ c sqrt(rho_DE) identification fixes the SHAPE of a0(z) with NO free galaxy-scale parameter.
  The event-horizon branch predicts a mild DECLINE (~0.7x by z=3) that a clean z~1-3 deep-MOND disk sample
  tests directly -- and which is already broadly consistent with the baryon-dominated high-z disks (whereas the
  steep apparent-horizon rise is not). CAVEATS kept loud: a0~sqrt(rho_DE) is Milgrom's CONJECTURE; DESI's
  evolving DE is 2.8-4.2 sigma and SNe-dependent (could revert to Lambda); and the DSSYK=de Sitter dual assumes
  constant Lambda, so an evolving-DE microscopic dual is unbuilt. Net: not proof -- but the first quantitative
  bridge from a cosmological dark-energy measurement to the galaxy MOND scale, and it points away from the
  steep rise the framework originally bet on, toward a mild decline or mild rise.""")
    print("="*92)


if __name__ == "__main__":
    main()
