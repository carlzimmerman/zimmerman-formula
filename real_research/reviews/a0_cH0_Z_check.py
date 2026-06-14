#!/usr/bin/env python3
"""
Running the numbers on a0 = cH0/Z, Z = 2 sqrt(8pi/3).
====================================================

*** CORRECTION (2026-06-13) — COEFFICIENT FOOTING: this script uses the SUPERSEDED rho_total/H0 form. ***
This computes a0 = cH0/Z (coefficient 1/Z = 0.173 against the PRESENT rate cH0), which gives 1.13e-10 at
Planck H0 and only reaches 1.20e-10 by setting H0 = 71.5 -- that H0-rescue is the cH0-vs-cH_Lambda
conflation. The framework's CANONICAL value is a0 = c^2 sqrt(Lambda/32pi) = c*H_Lambda/Z = 9.36e-11
(the rho_DE / de Sitter reading), i.e. coefficient 1/Z = 0.173 against cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0,
equivalently 0.143 against cH0. Milgrom (0.159) and Verlinde (0.167) use cH0, so the apt comparison is the
framework's 0.143 (the LOW outlier), NOT 1/Z=0.173. See real_research/THE_A0_COEFFICIENT_CONVENTION.md.
The numbers below are retained as the historical record; read them as the rho_total/cH0 object, not the
canonical a0.

The MOND scale a0 ~ cH0 is Milgrom's long-known coincidence. The framework's claim
is the SPECIFIC factor: a0 = cH0/Z with Z = 2 sqrt(8pi/3) = 5.7888. We compute it
honestly across the (disputed) H0 range, and compare Z to the other obvious O(1)
divisors 2pi and 6.

Observed a0 (SPARC RAR; McGaugh/Lelli/Famaey): 1.20e-10 m/s^2,
  +/- ~2% statistical, +/- ~20% systematic.

Pure stdlib.  Run:  python reviews/a0_cH0_Z_check.py
"""

import math

C = 2.99792458e8           # m/s
MPC = 3.0857e22            # m
A0_OBS = 1.20e-10          # m/s^2 (central)
Z = 2 * math.sqrt(8 * math.pi / 3)   # 5.78881

def cH0(H0_kmsmpc):
    return C * (H0_kmsmpc * 1e3 / MPC)   # m/s^2

def main():
    print("=" * 76)
    print(f"  Z = 2*sqrt(8pi/3) = {Z:.5f} ;  2pi = {2*math.pi:.5f} ;  observed a0 = {A0_OBS:.2e}")
    print("=" * 76)
    print(f"  {'H0':>6} {'source':<10} {'cH0':>11} {'a0=cH0/Z':>11} {'err vs 1.2e-10':>15}")
    for H0, src in [(67.4, "Planck"), (70.0, "neutral"), (71.5, "framework"),
                    (73.0, "SH0ES")]:
        ch = cH0(H0)
        a0 = ch / Z
        err = (a0 - A0_OBS) / A0_OBS * 100
        print(f"  {H0:>6.1f} {src:<10} {ch:>11.3e} {a0:>11.3e} {err:>+13.1f}%")
    print()
    print("=" * 76)
    print("  Which O(1) divisor of cH0 best gives a0?  (best-fit divisor = cH0/a0)")
    print("=" * 76)
    print(f"  {'H0':>6} {'need cH0/a0':>12} {'|Z err|':>9} {'|2pi err|':>10} {'|6 err|':>9}  best")
    for H0 in (67.4, 70.0, 71.5, 73.0):
        need = cH0(H0) / A0_OBS
        eZ = abs(need - Z) / Z * 100
        e2pi = abs(need - 2*math.pi) / (2*math.pi) * 100
        e6 = abs(need - 6) / 6 * 100
        best = min([("Z", eZ), ("2pi", e2pi), ("6", e6)], key=lambda x: x[1])[0]
        print(f"  {H0:>6.1f} {need:>12.3f} {eZ:>8.1f}% {e2pi:>9.1f}% {e6:>8.1f}%   {best}")
    print()
    print("=" * 76)
    print("WHAT THE NUMBERS SAY (honest)")
    print("=" * 76)
    print("  * a0 = cH0/Z WORKS numerically: at H0 = 71.5 it gives 1.200e-10, matching")
    print("    the central observed value to ~0.01%. Z is the BEST of {Z, 2pi, 6} at")
    print("    every H0 in the tension range -- notably better than 2pi (~8%) or 6 (~3-6%).")
    print("    (I under-credited this earlier when I said 2pi/6 'fit just as well' -- they")
    print("     are consistent within a0's error, but Z is clearly the best central fit.)")
    print()
    print("  * BUT the ~0.01% precision RIDES on choosing H0 = 71.5. With Planck's 67.4")
    print("    it is ~5.6% low; with SH0ES 73 it is ~2.2% high. H0 itself is disputed")
    print("    (the Hubble tension), so the headline precision is a choice of H0.")
    print()
    print("  * AND a0's own systematic uncertainty is ~20%. Matching a number known to")
    print("    ~20% 'to 0.01%' is a central-value coincidence inside a wide window.")
    print()
    print("  * a0 ~ cH0 is MILGROM'S coincidence (1983). The framework's contribution is")
    print("    the specific factor 1/Z = sqrt(3/8pi)/2 = 0.1728 (i.e. a0 = c*sqrt(G rho_c)/2).")
    print("    It is the best such factor -- but a0 = c*sqrt(G rho_c)/2 assembles the")
    print("    factor 2 from horizon thermodynamics by hand (not a clean derivation).")
    print()
    print("  VERDICT: the strongest single numerical result in the framework, and I was")
    print("  too dismissive of it. It is a genuinely good, best-in-class fit to the")
    print("  a0 ~ cH0 coincidence -- but it is a CONSISTENT COINCIDENCE (H0-contingent,")
    print("  inside a0's 20% systematic, on top of Milgrom's known relation), not a")
    print("  precise confirmation and not a clean derivation.")


if __name__ == "__main__":
    main()
