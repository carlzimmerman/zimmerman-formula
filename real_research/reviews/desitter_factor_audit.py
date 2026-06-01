#!/usr/bin/env python3
"""
Is the factor in Z = 2 sqrt(8pi/3) really from the de Sitter horizon?
=====================================================================

Carl's claim: "the 2 is from the de Sitter horizon." This is a real, checkable
physics statement, so let us check it properly rather than wave it away.

We compute the de Sitter horizon's OWN natural O(1) numbers and ask which (if
any) reproduce a0 = cH/Z with Z = 2 sqrt(8pi/3) = 5.789.

Honest preview of the finding:
  * The horizon DOES hand you a divisor of cH -- but its cleanest one is 2pi
    (the Gibbons-Hawking TEMPERATURE), giving a0 = cH/2pi = 1.11e-10, within 8%
    of observed. So Carl is RIGHT that the divisor is horizon-set, in the form
    a0 ~ cH/2pi.
  * A literal factor of *2* is NOT the clean horizon number: pure de Sitter
    surface gravity gives kappa = cH (factor 1); a factor 2 only appears in
    enclosed-critical-mass arguments that MIX the ball volume 4pi/3 with the
    Friedmann 8pi/3, and that gives a0 = cH/2 = 3.5e-10 -- 2.9x too big.
  * The framework's specific 2 sqrt(8pi/3) = sqrt(32pi/3) = 5.789 is a GEOMETRIC
    number (8 x 4pi/3 = cube x sphere = the compactification modulus root), 8%
    away from the horizon's 2pi -- and a0's ~20% systematic cannot tell them
    apart. So: horizon supports a0 ~ cH/2pi; the exact 2 sqrt(8pi/3) is geometric,
    observationally tied to the horizon value but not derived from it.

Pure stdlib. Run:  python reviews/desitter_factor_audit.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
G = 6.674e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
H0 = 71.5 * 1e3 / MPC          # 1/s
A0_OBS = 1.20e-10
A0_SYS = 0.20                   # ~20% systematic on a0 (SPARC RAR)
cH0 = C * H0
Z = 2 * math.sqrt(8 * math.pi / 3)     # 5.78881
TWO_PI = 2 * math.pi


def part1_horizon_numbers():
    print("=" * 80)
    print("(1) The de Sitter horizon's OWN natural quantities (H0 = 71.5)")
    print("=" * 80)
    R_dS = C / H0
    kappa = C * H0                      # de Sitter horizon surface gravity ~ cH
    T_dS = HBAR * H0 / (2 * math.pi * KB)
    print(f"   horizon radius      R_dS = c/H0      = {R_dS:.3e} m  (~{R_dS/MPC/1e3:.1f} Gpc)")
    print(f"   surface gravity     kappa = cH0      = {kappa:.3e} m/s^2   (factor 1)")
    print(f"   Gibbons-Hawking T   = hbar H0/2pi kB = {T_dS:.3e} K")
    print(f"   horizon acceleration cH0             = {cH0:.3e} m/s^2")
    print("   The horizon hands you cH0 (surface gravity, factor 1) and, via the")
    print("   temperature, the factor 2pi. Those are its clean O(1) numbers.\n")


def part2_divisor_table():
    print("=" * 80)
    print("(2) Which divisor of cH0 reproduces a0?  (a0 = cH0 / divisor)")
    print("=" * 80)
    band_lo, band_hi = A0_OBS * (1 - A0_SYS), A0_OBS * (1 + A0_SYS)
    print(f"   observed a0 = {A0_OBS:.3e}  (systematic band {band_lo:.2e} - {band_hi:.2e})")
    print()
    print(f"   {'divisor':<34}{'value':>8}{'a0 pred':>12}{'vs obs':>9}{'in band?':>10}")
    cands = [
        ("1   (surface gravity kappa=cH)",      1.0),
        ("2   (enclosed crit-mass, 4pi/3 vs 8pi/3)", 2.0),
        ("2pi (Gibbons-Hawking TEMPERATURE)",   TWO_PI),
        ("6   (round)",                         6.0),
        ("2 sqrt(8pi/3)  (FRAMEWORK Z)",        Z),
    ]
    for name, d in cands:
        a0 = cH0 / d
        inb = "yes" if band_lo <= a0 <= band_hi else "no"
        print(f"   {name:<34}{d:>8.3f}{a0:>12.2e}{a0/A0_OBS:>8.2f}x{inb:>10}")
    print()
    print("   Reading: divisor 1 and 2 overshoot (a0 too big). The TEMPERATURE")
    print("   divisor 2pi lands at 1.11e-10 (8% low, in band). The framework's")
    print("   2 sqrt(8pi/3)=5.79 lands on the central value (by construction). 2pi and")
    print("   5.79 differ by only 8% -- both sit well inside a0's 20% systematic.\n")


def part3_is_the_2_from_dS():
    print("=" * 80)
    print("(3) So -- is 'the 2' from the de Sitter horizon? Carefully:")
    print("=" * 80)
    print(f"   framework Z = 2 sqrt(8pi/3) = sqrt(32pi/3) = {Z:.4f}")
    print(f"   horizon temperature 2pi                     = {TWO_PI:.4f}")
    print(f"   ratio Z / 2pi = {Z/TWO_PI:.4f}  ->  they differ by {abs(Z/TWO_PI-1)*100:.1f}%")
    print()
    print("   * The clean HORIZON divisor is 2pi (the Gibbons-Hawking temperature),")
    print("     NOT 2. a0 ~ cH/2pi is a genuine horizon statement and fits to 8%.")
    print("   * A literal factor of 2 is NOT a clean de Sitter number: surface")
    print("     gravity gives factor 1 (cH); the '2' only shows up when you compute")
    print("     the Newtonian pull of the enclosed critical mass, g=GM_c/R_H^2=cH/2,")
    print("     which MIXES the 3-ball volume (4pi/3) with Friedmann (8pi/3). That")
    print("     gives a0=cH/2=3.5e-10 -- 2.9x too big. So '2' alone does not fit.")
    print("   * The framework's 2 sqrt(8pi/3) is a GEOMETRIC number: 32pi/3 = 8x(4pi/3)")
    print("     = cube x sphere = the (T^2)^3/(Z2xZ2) VOLUME MODULUS. Its root is the")
    print("     divisor. That is a compactification quantity, not a horizon quantity.\n")


def part4_verdict():
    print("=" * 80)
    print("VERDICT -- crediting the intuition, and locating the real gap")
    print("=" * 80)
    print("  CARL IS PARTLY RIGHT, and I was too flat to call it purely 'fit':")
    print("   * the DIVISOR of cH0 is plausibly HORIZON-set -- the de Sitter")
    print("     temperature gives 2pi, and a0 ~ cH/2pi fits the data to ~8%. That is")
    print("     a real, clean, horizon-thermodynamic origin for 'a0 is a few times")
    print("     smaller than cH'. Good intuition.")
    print()
    print("  BUT the SPECIFIC factor is not literally '2 from the horizon':")
    print("   * the horizon's clean number is 2pi (=6.28), not 2, and not the")
    print("     framework's 2 sqrt(8pi/3) (=5.79);")
    print("   * 5.79 is a GEOMETRIC number (root of the 32pi/3 volume modulus), 8%")
    print("     from the horizon's 2pi -- and a0's 20% systematic cannot separate them.")
    print()
    print("  HONEST NET: 'the divisor is from the de Sitter horizon' is defensible in")
    print("  the form a0 ~ cH/2pi (Gibbons-Hawking). The framework instead uses the")
    print("  geometric 2 sqrt(8pi/3); it fits the central value 8% better but is")
    print("  observationally indistinguishable from the horizon's 2pi. To claim the")
    print("  geometric value over 2pi you still need the unproven link 'coupling =")
    print("  sqrt(volume modulus)'. The horizon gives you 2pi for free; it does not")
    print("  give you sqrt(32pi/3). That 8% is exactly the unclosed seam.")


def main():
    part1_horizon_numbers()
    part2_divisor_table()
    part3_is_the_2_from_dS()
    part4_verdict()


if __name__ == "__main__":
    main()
