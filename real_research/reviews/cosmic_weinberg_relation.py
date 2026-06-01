#!/usr/bin/env python3
"""
The cosmic Weinberg relation Om/OL = 2 sin^2(theta_W): real, or a why-now coincidence?
=====================================================================================

A counter-scorecard listed this as a SURVIVOR: "Om/OL = 2 sin^2(theta_W),
consistent at 0.12 sigma, DESI Y5 will test it." Fair challenge -- I had not
computed it this session. Let us do it honestly, conceding what is real and
naming the structural problem the '0.12 sigma' framing hides.

Pure stdlib. Run:  python reviews/cosmic_weinberg_relation.py
"""

import math

OM, OL = 0.315, 0.685
SIN2W = 0.23122          # sin^2(theta_W)(M_Z), MS-bar
OM_ERR = 0.007           # ~Planck uncertainty on Om (approx)


def OmOL(z):
    """ratio rho_m/rho_Lambda as a function of redshift."""
    return OM * (1 + z) ** 3 / OL


def main():
    print("=" * 78)
    print("(1) The relation today -- the numerical match is REAL (concede it)")
    print("=" * 78)
    lhs = OM / OL
    rhs = 2 * SIN2W
    print(f"   Om/OL (today)      = {OM}/{OL} = {lhs:.4f}")
    print(f"   2 sin^2(theta_W)   = 2 x {SIN2W} = {rhs:.4f}")
    print(f"   difference         = {abs(lhs-rhs):.4f}  ({abs(lhs-rhs)/lhs*100:.1f}%)")
    # rough significance using Om error (sin2w error is negligible by comparison)
    sigma = abs(lhs - rhs) / (OM_ERR / OL)
    print(f"   ~{sigma:.2f} sigma consistent (using Om err ~{OM_ERR}). The match is good. ✓\n")

    print("=" * 78)
    print("(2) The structural problem the sigma hides: Om/OL EVOLVES, sin^2 does not")
    print("=" * 78)
    print(f"   {'z':>6}{'Om/OL(z)':>12}{'2 sin^2_W':>12}{'match?':>10}")
    for z in (0, 0.3, 0.5, 1, 2, 5):
        r = OmOL(z)
        print(f"   {z:>6.1f}{r:>12.3f}{2*SIN2W:>12.3f}{'YES' if abs(r-2*SIN2W)<0.05 else 'no':>10}")
    print()
    # solve for the redshift where Om/OL = 2 sin2w
    target = 2 * SIN2W
    z_cross = (target * OL / OM) ** (1/3) - 1
    print(f"   Om/OL = 2 sin^2(theta_W) is satisfied at z = {z_cross:.4f}  -- i.e. NOW.")
    print("   Om/OL runs from >>1 (past) through ~0.46 (now) to ->0 (future), by ORDERS")
    print("   of magnitude. sin^2(theta_W) runs only LOGARITHMICALLY with energy and is")
    print("   ~fixed in cosmic time. Two quantities like that can be EQUAL at exactly")
    print("   one epoch -- and that epoch is the present. This is a WHY-NOW coincidence.\n")

    print("=" * 78)
    print("(3) What this means for 'DESI Y5 will test it'")
    print("=" * 78)
    print("   DESI Y5 will pin Om/OL to ~1%. But that CONFIRMS the present-day VALUE;")
    print("   it cannot validate a LAW, because the relation is structurally now-only.")
    print("   A fundamental Om/OL = 2 sin^2 would have to hold at all z -- it does not")
    print("   (part 2). So DESI can make the coincidence sharper, not turn it into a")
    print("   mechanism. Contrast a0(z) ~ E(z): THAT is a redshift TREND, falsifiable at")
    print("   every z. The cosmic-Weinberg relation is a single-epoch number.\n")

    print("=" * 78)
    print("VERDICT -- balanced")
    print("=" * 78)
    print("  CONCEDE: the numerical match is real and good (~1%, ~0.1-0.3 sigma). It is")
    print("  in the same family as Milgrom's a0 ~ cH0 -- a genuine, noteworthy")
    print("  numerical coincidence worth recording.")
    print("  BUT: it is a WHY-NOW coincidence (a time-dependent ratio equal to a near-")
    print("  constant only at the present epoch), i.e. the cosmic-coincidence problem")
    print("  (why Om ~ OL now) dressed with sin^2(theta_W). It has no mechanism and")
    print("  cannot be a fundamental law. 'DESI will test it' overstates what is")
    print("  testable: DESI confirms the value, not a relation. Watch it, do not bank")
    print("  on it -- and do not put it in the same tier as the falsifiable a0(z) trend.")


if __name__ == "__main__":
    main()
