#!/usr/bin/env python3
"""
The cascade, continued: galaxy structure, early growth, and the kinematics of a0.
=================================================================================

More forced consequences of the premise a0(z) = a0(0) E(z) (from a0=(c/2)sqrt(Grho)).
Each step is a rigorous implication (Steps 8, 10) or a robust qualitative direction
with the magnitude flagged as needing MOND N-body (Step 9).

Run:  python real_research/Z2_cascade_part2.py
"""

import math

OM, OL = 0.315, 0.685
A0 = 1.13e-10
H0_GYR = 1 / 14.4   # H0 in 1/Gyr (for the rate)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def q(z):
    # deceleration parameter q = Om/2 (1+z)^3/E^2 - OL/E^2
    e2 = OM * (1 + z) ** 3 + OL
    return (0.5 * OM * (1 + z) ** 3 - OL) / e2


def main():
    print("=" * 76)
    print("STEP 8 [FORCED, DIRECTLY TESTABLE] the RAR 'knee' moves to higher g at high z")
    print("=" * 76)
    print("   The radial-acceleration relation transitions from Newtonian to MOND at")
    print("   g_bar ~ a0. If a0(z)=a0(0)E(z), the knee is at g_bar ~ a0(0)E(z):")
    print(f"   {'z':>5}{'a0(z) = knee [m/s^2]':>24}{'shift vs local':>16}")
    for z in (0, 1, 2, 4, 6):
        print(f"   {z:>5}{A0*E(z):>24.2e}{E(z):>15.1f}x")
    print("   => a galaxy of FIXED baryonic acceleration crosses from Newtonian into the")
    print("   MOND regime as z rises and a0(z) climbs past it. The high-z RAR is OFFSET to")
    print("   higher accelerations -- the single most DIRECT signature of a0(z).")
    print("   [TEST] build the RAR from high-z rotation curves (ALMA [CII] disks, JWST IFU)")
    print("   and look for the knee shifting up by E(z). Clean, no f_geom, no gas degeneracy.\n")

    print("=" * 76)
    print("STEP 9 [FORCED DIRECTION] accelerated EARLY structure -> the JWST 'impossible")
    print("        early galaxies'")
    print("=" * 76)
    print("   MOND boosts gravity in the deep regime by sqrt(a0/g_N); with a0(z) larger at")
    print("   high z, the boost grows as sqrt(E(z)):")
    print(f"   {'z':>5}{'gravity boost vs z=0  sqrt(E(z))':>34}")
    for z in (0, 6, 10, 14):
        print(f"   {z:>5}{math.sqrt(E(z)):>34.1f}x")
    print("   => structure collapses EARLIER and FASTER than even constant-a0 MOND (which")
    print("   already beats LCDM). DIRECTION is robust; magnitude needs MOND N-body.")
    print("   [STATUS] JWST finds far more massive/UV-bright galaxies at z=10-14 than LCDM")
    print("   predicts ('impossible early galaxies', e.g. Labbe+2023, the z>10 UVLF excess).")
    print("   Evolving a0 pushes in EXACTLY this direction -- a topical qualitative match,")
    print("   not yet a quantitative claim.\n")

    print("=" * 76)
    print("STEP 10 [FORCED] a0 is presently DECREASING: dot(a0)/a0 = -(1+q) H")
    print("=" * 76)
    print("   a0 ~ H(z) => dot(a0)/a0 = dot(H)/H = -(1+q)H, with q the deceleration param.")
    print(f"   {'z':>5}{'q(z)':>9}{'dot(a0)/a0  [units of H]':>26}")
    for z in (0, 1, 3, 10):
        print(f"   {z:>5}{q(z):>9.2f}{-(1+q(z)):>26.2f}")
    rate0 = -(1 + q(0)) * H0_GYR
    print(f"   today (q0={q(0):.2f}): a0 falls at {-(1+q(0)):.2f} H0 = {rate0*100:.1f}% per Gyr.")
    print("   In the FUTURE q->-1 (de Sitter) => dot(a0)->0: a0 FREEZES at its Lambda floor.")
    print("   In the PAST (matter era) q->+1/2 => a0 fell fast. So a0's whole history is")
    print("   FIXED by the expansion history q(z) -- a0(z) and the deceleration are one curve.\n")

    print("=" * 76)
    print("STEP 11 [FORCED] the smallness of a0 is the dilution of the universe")
    print("=" * 76)
    print("   a0 = (c/2)sqrt(G rho_c). rho_c ~ 9e-27 kg/m^3 is tiny because the universe is")
    print("   old and dilute, so a0 ~ 1e-10 is tiny for the SAME reason. 'Why is a0 so small")
    print("   and ~ cH0?' is answered: a0 IS the cosmic density in acceleration units, and")
    print("   it shrinks as the universe expands. No separate small number to explain.\n")

    print("#" * 76)
    print("# NET (parts 1+2): the premise is load-bearing across THREE domains")
    print("#" * 76)
    print("  GALAXIES:   evolving RAR knee (Step 8), high-z dark-matter-richness (Step 6),")
    print("              the BTFR/dispersion zero-point vs z (tested, leans evolving).")
    print("  COSMOLOGY:  a0->H0 at the Planck value (Step 2) and the coefficient-Hubble lock;")
    print("              a0(z) as a chronometer/w(z) probe (Step 3); accelerated early")
    print("              structure matching the JWST excess (Step 9); a0 frozen-to-Lambda")
    print("              in the future (Steps 4,10).")
    print("  DARK SECTOR: dark matter scale = dark energy = one evolving a0(z) (Step 4);")
    print("              Machian/thermal inertia (Step 7); a0 small because rho_c small (11).")
    print("  Every one is a forced, falsifiable consequence -- the premise is a tightly")
    print("  coupled physical package whose verdict arrives with precision a0, z>10 RAR/")
    print("  kinematics, and the Hubble-tension resolution. THAT is what 'if true' buys.")


if __name__ == "__main__":
    main()
