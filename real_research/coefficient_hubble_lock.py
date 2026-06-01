#!/usr/bin/env python3
"""
The coefficient-Hubble lock: "which MOND coefficient" IS "what is H0".
=====================================================================

Deepening the cascade. The MOND scale is a0 = k * cH0 for some O(1) coefficient k.
Invert: H0 = a0/(k c). So at fixed (measured) a0, the COEFFICIENT k and the HUBBLE
CONSTANT H0 are rigidly locked -- they are not two questions, they are one.

The striking part: at the SPARC value a0 = 1.13e-10, the three competing coefficient
THEORIES map almost exactly onto the three competing H0 MEASUREMENTS:
   1/2pi (Milgrom / de Sitter temperature) -> 73.1  ~ SH0ES (Cepheid ladder, late)
   1/6   (Verlinde de Sitter volume entropy) -> 69.8  ~ TRGB / CCHP (middle)
   1/Z   (geometric, this program)          -> 67.3  ~ Planck (CMB, early)
and the coefficient spread (8.5%) matches the Hubble-tension spread (8.3%).

This is NOT evidence for any coefficient (it is anchored on a0=1.13 and the matching
spreads are partly coincidental). It IS a clean reframing: resolving the Hubble
tension resolves the MOND coefficient, and vice versa.

Run:  python real_research/coefficient_hubble_lock.py
"""

import math

c = 2.99792458e8
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)

COEFFS = [("1/2pi  Milgrom / de Sitter temperature", 1 / (2 * math.pi)),
          ("1/6    Verlinde de Sitter volume entropy", 1 / 6),
          ("1/Z    geometric (this program)", 1 / Z)]
CAMPS = [("Planck CMB (early)", 67.4, 0.5),
         ("TRGB / CCHP (middle)", 69.8, 1.7),
         ("SH0ES ladder (late)", 73.0, 1.0)]


def H0_of(a0, k):
    return a0 / (k * c) * MPC / 1e3


def main():
    print("=" * 76)
    print("(1) The lock: H0 = a0/(k c). Coefficient and H0 are one question.")
    print("=" * 76)
    print("   a0 is measured (galaxy rotation curves). c is exact. So choosing the MOND")
    print("   coefficient k FIXES H0, and measuring H0 FIXES k. They cannot be chosen")
    print("   independently -- sigma(H0)/H0 = sigma(k)/k exactly.\n")

    print("=" * 76)
    print("(2) The three-way map at a0 = 1.13e-10 (SPARC RAR fit)")
    print("=" * 76)
    print(f"   {'coefficient theory':<42}{'-> H0':>8}{'nearest camp':>22}")
    for name, k in COEFFS:
        H0 = H0_of(1.13e-10, k)
        near = min(CAMPS, key=lambda t: abs(t[1] - H0))
        print(f"   {name:<42}{H0:>8.1f}{near[0]:>22}")
    print()
    print(f"   coefficient spread 1/2pi..1/Z : {(1/Z - 1/(2*math.pi))/(1/(2*math.pi))*100:.1f}%")
    print(f"   Hubble tension spread 67.4..73: {(73-67.4)/67.4*100:.1f}%   (they match)")
    print("   => the three MOND-coefficient theories land on the three H0 camps almost")
    print("      exactly. Milgrom<->SH0ES, Verlinde<->TRGB, geometric-Z<->Planck.\n")

    print("=" * 76)
    print("(3) Honest caveats -- why this is a reframing, NOT evidence")
    print("=" * 76)
    print("   * It is anchored on a0 = 1.13e-10. With McGaugh's a0 = 1.20e-10 everything")
    print("     shifts up (1/Z -> 71.5, all three land 71-78), and the clean map breaks:")
    for name, k in COEFFS:
        print(f"       a0=1.20: {name.split()[0]:<6} -> H0 = {H0_of(1.20e-10, k):.1f}")
    print("   * The spread match (8.5% vs 8.3%) is between UNRELATED quantities (theory")
    print("     factors vs observational systematics) -- partly coincidental.")
    print("   So: a memorable alignment that illustrates the lock, not proof of Z.\n")

    print("=" * 76)
    print("(4) The forward path: the Hubble tension will pick the coefficient")
    print("=" * 76)
    print("   Because of the lock, the SAME data resolving the Hubble tension also picks")
    print("   the MOND coefficient (once a0 is pinned). Concretely, with a0 ~ 1.13e-10:")
    print("     * if the true H0 -> Planck 67  => coefficient is 1/Z (geometric)  [Z WINS]")
    print("     * if the true H0 -> TRGB  70   => coefficient is 1/6 (Verlinde)")
    print("     * if the true H0 -> SH0ES 73   => coefficient is 1/2pi (Milgrom)  [Z DEAD]")
    print("   So the geometric Z is a BET on the early-universe (Planck) H0. The JWST-era")
    print("   resolution of the Hubble tension is, through this lock, also the verdict on Z.")
    print("   (Pinning a0 to ~2% with gas-rich rotators sharpens the anchor either way.)\n")

    print("=" * 76)
    print("VERDICT")
    print("=" * 76)
    print("  * The lock H0 = a0/(k c) is rigorous: the MOND coefficient and H0 are a single")
    print("    fork. This converts an un-pin-down-able dimensionless number into a question")
    print("    the cosmology community is ALREADY answering (the Hubble tension).")
    print("  * At a0=1.13e-10 the three coefficient theories map cleanly onto Planck/TRGB/")
    print("    SH0ES -- striking, but a0-anchored and partly coincidental, so a reframing")
    print("    not evidence.")
    print("  * The actionable bet: the geometric Z corresponds to Planck H0. If the tension")
    print("    resolves early (67), Z is favoured; if late (73), Milgrom's 1/2pi is, and Z")
    print("    is dead. Z's fate rides on the Hubble tension -- a clean, near-term verdict.")


if __name__ == "__main__":
    main()
