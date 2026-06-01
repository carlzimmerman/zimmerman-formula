#!/usr/bin/env python3
"""
Can a radion potential V(R) be DERIVED with its minimum at R = Z^2 l_P/(2pi)?
=============================================================================

The framework needs the size of the internal T^3/Z2 stabilized at
    R = Z^2 l_P / (2pi)  =>  R/l_P = Z^2/(2pi) = 32pi/3/(2pi) = 16/3 = 5.333...
so that Vol(T^3/Z2) = (Z^2)^3 l_P^3 / 2 reproduces the gauge coupling.

This is the Goldberger-Wise question: does any natural modulus-stabilization
potential put its minimum there WITHOUT tuning the answer in?

We test it honestly. Result: stabilization is possible, but the minimum is a
SMOOTH function of the potential's continuous parameters -- you solve for those
parameters to land on 5.333, i.e. you insert the answer. Nothing selects 32pi/3.

Targets:  R_min/l_P = Z^2/(2pi) = 16/3 = 5.3333

Pure stdlib + numpy.  Run:  python reviews/radion_stabilization_test.py
"""

import math
import numpy as np

PI = math.pi
Z2 = 32 * PI / 3
R_TARGET = Z2 / (2 * PI)          # = 16/3 = 5.3333 (in Planck units)


def part1_massless_no_stabilization():
    print("=" * 84)
    print("(1) Massless bulk content alone CANNOT stabilize -- dimensional no-go")
    print("=" * 84)
    print("  A massless bulk field has only ONE scale: R. So the 4D vacuum energy")
    print("  density (mass^4) is forced by dimensions to be")
    print("        V_Casimir(R) = C / R^4 ,   C = an Epstein-zeta number.")
    print("  dV/dR = -4C/R^5 != 0 for all finite R: monotonic, NO minimum.")
    print("  (C>0 -> runs to R->infinity [decompactify]; C<0 -> R->0 [collapse].)")
    # the coefficient is an Epstein value, NOT 4*pi/3 -- show a convergent proxy:
    epstein_4 = 0.0
    for a in range(-30, 31):
        for b in range(-30, 31):
            ab = a * a + b * b
            for c in range(-30, 31):
                m = ab + c * c
                if m:
                    epstein_4 += m ** -2.0      # sum |k|^-4 (converges)
    print(f"\n  (the Casimir coefficient is an Epstein number, e.g. sum|k|^-4 = "
          f"{epstein_4:.4f}, not 4pi/3={4*PI/3:.4f})")
    print("  => you MUST add a second scale (mass / flux / tension) to get a min.\n")


def part2_two_term_minimum_is_tunable():
    print("=" * 84)
    print("(2) Add a second scale -> a real minimum, but its location is TUNABLE")
    print("=" * 84)
    print("  Representative stabilizing potential (Casimir attraction balanced by a")
    print("  higher-order/curvature term):")
    print("        V(R) = -C/R^4 + D/R^6 .")
    print("  dV/dR = 4C/R^5 - 6D/R^7 = 0  =>  R_min = sqrt(3D/(2C)).")
    print("  The minimum is set entirely by the ratio D/C (a continuous input).\n")
    # To land on the target you simply SOLVE for D/C:
    DC_needed = (2.0 / 3.0) * R_TARGET ** 2
    print(f"  To force R_min = {R_TARGET:.4f} l_P you need  D/C = (2/3)R^2 = "
          f"{DC_needed:.4f} l_P^2.")
    print("  Nothing derives that value -- it is chosen to hit the answer.\n")
    # show the minimum is smooth in D/C: NO attractor at the target
    print("  Sweep D/C, read off R_min -- a smooth curve, no special point at 5.333:")
    print(f"    {'D/C [l_P^2]':>12} | {'R_min/l_P':>10}")
    for DC in [1, 5, 10, 18.96, 30, 60, 120]:
        R_min = math.sqrt(1.5 * DC)
        flag = "  <- target (by construction)" if abs(R_min - R_TARGET) < 0.05 else ""
        print(f"    {DC:>12.2f} | {R_min:>10.4f}{flag}")
    print("  R_min slides continuously with the input; 5.333 is not preferred.\n")


def part3_goldberger_wise_exponential():
    print("=" * 84)
    print("(3) Goldberger-Wise exponential -> log-enhanced minimum, still tunable")
    print("=" * 84)
    print("  GW-type potential from a bulk scalar (mass m, boundary VEVs):")
    print("        V(R) = P e^{-2 m R} - Q e^{-m R}   (+const)")
    print("  Minimum at e^{-mR} = Q/(2P)  =>  R_min = (1/m) ln(2P/Q).")
    print("  Location set by m and the VEV ratio P/Q -- both continuous inputs.\n")
    print(f"  e.g. choose m, P/Q to make R_min = {R_TARGET:.4f}:")
    for m in [0.5, 1.0, 2.0]:
        PQ = math.exp(m * R_TARGET) / 2          # solve ln(2P/Q)=m*R_target
        print(f"    m={m:>4} (1/l_P):  need 2P/Q = {2*PQ:>10.3f}  -> R_min = "
              f"{(1/m)*math.log(2*PQ):.4f} l_P")
    print("  Any target is reachable by choosing (m, P/Q). The number 32pi/3 plays")
    print("  no role; you'd be fitting the boundary data to the answer.\n")


def part4_where_4pi3_actually_hides():
    print("=" * 84)
    print("(4) The ONE place 4pi/3 appears 'for free' -- and it's renormalized away")
    print("=" * 84)
    print("  Mode counting (Weyl law): #modes with |p|<k is")
    print("        N(<k) = Vol * (4*pi/3) k^3 / (2*pi)^3 .")
    print(f"  The 4*pi/3 = {4*PI/3:.5f} here is the volume of the unit ball in")
    print("  MOMENTUM space -- the phase-space factor. It multiplies the leading")
    print("  UV-DIVERGENT (cutoff^4) term of the vacuum energy:")
    print("        V ~ (4*pi/3) Lambda^4 Vol/(2pi)^3 + ... ")
    print("  That divergent piece is absorbed into the bulk cosmological constant /")
    print("  brane tension by renormalization. The FINITE, physical Casimir energy")
    print("  is the subleading Epstein-zeta number (part 1), which is NOT 4*pi/3.")
    print("  So every appearance of 4pi/3 is a scale-dependent VOLUME coefficient,")
    print("  never the finite dynamical quantity that could be 'derived'.\n")


def part5_only_escape_is_blocked():
    print("=" * 84)
    print("(5) The only way to FORCE a special R_min -- and why it can't give 32pi/3")
    print("=" * 84)
    print("  A minimum could be protected (not tunable) by QUANTIZATION: integer flux")
    print("  N through cycles, integer winding, etc. Then e.g. V ~ N^2/R^4 + ... and")
    print("  R_min ~ sqrt(N) * (continuous scales).")
    print("  But quantization yields INTEGERS / algebraic numbers. 32pi/3 is a")
    print("  TRANSCENDENTAL volume. No flux integer can produce it; the pi would have")
    print("  to come from the continuous scales, which are tunable again.")
    print("  => even the protected case cannot select 32pi/3.\n")


def main():
    print(f"\n  TARGET: stabilize R at Z^2/(2pi) = {R_TARGET:.4f} Planck lengths.\n")
    part1_massless_no_stabilization()
    part2_two_term_minimum_is_tunable()
    part3_goldberger_wise_exponential()
    part4_where_4pi3_actually_hides()
    part5_only_escape_is_blocked()
    print("=" * 84)
    print("VERDICT")
    print("=" * 84)
    print("  Can a radion potential sit at R = Z^2 l_P/(2pi)?  YES -- by choosing the")
    print("  potential's parameters (ratio D/C, or GW's m and P/Q) to put it there.")
    print("  Is that a DERIVATION of Z^2?  NO. The minimum R_min is a smooth function")
    print("  of continuous inputs; demanding R_min = 16/3 is one equation that you")
    print("  solve for the inputs -- the unexplained number 32pi/3 just moves down one")
    print("  level, into the potential parameters. Nothing dynamically prefers it, and")
    print("  the only quantization-protected alternative gives integers, not a")
    print("  transcendental volume.")
    print()
    print("  So stabilization does not rescue the derivation -- it relocates the")
    print("  scale-setting. Honestly, R = Z^2 l_P/(2pi) is still an INPUT (the radion")
    print("  VEV is chosen), consistent with the 40-invariant no-go and Option A:")
    print("  Z^2 = 32pi/3 is the Friedmann definition 8 x (4pi/3), not a derived scale.")


if __name__ == "__main__":
    main()
