#!/usr/bin/env python3
"""
Is the factor of 2 in Z = 2*sqrt(8pi/3) derivable from first principles?
Does it come from de Sitter?   -- computed, route by route.
========================================================================

a0 = (c/2) sqrt(G rho_c) = cH/Z, with Z = sqrt(8pi/3)/k and the framework's k = 1/2,
giving Z = 2 sqrt(8pi/3) = sqrt(32pi/3) = 5.789.

Split the question:
  * sqrt(8pi/3) = 2.894 is the EXACT Friedmann factor (rho <-> H). It is DERIVED.
  * the remaining factor (=> k, => the leading "2") is the question. We compute what each
    first-principles route gives for the coefficient Z, and compare to the framework's 5.789
    and to the data-preferred ~5.8.

Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
H0 = 67.4e3 / Mpc
sqrt8pi3 = np.sqrt(8 * np.pi / 3)        # = 2.8944, the Friedmann factor (DERIVED)


def a0_of_Z(Z):
    return c * H0 / Z * 1e10             # in 1e-10 m/s^2


def main():
    print("=" * 80)
    print("The Friedmann part is real; the coefficient on top of it is the question")
    print("=" * 80)
    print(f"  sqrt(8pi/3) = {sqrt8pi3:.4f}   <-- EXACT (H^2 = 8pi/3 G rho); a0 = k*cH/(1)... ")
    print(f"  a0 = k*c*sqrt(G rho_c) = cH/Z,  Z = sqrt(8pi/3)/k.  So Z fixes k and vice versa.\n")

    print("=" * 80)
    print("What each first-principles route gives for the coefficient Z (=> a0 today)")
    print("=" * 80)
    routes = [
        ("de Sitter horizon SURFACE GRAVITY  kappa = c^2/R_H = cH", 1.0,
         "k=2.894; gives a0=cH (no 1/2). Z=1."),
        ("de Sitter apparent-horizon, kappa = c^2/2R_H (half-conv.)", 2.0,
         "HERE is a factor 1/2 -- but it gives Z=2, NOT 5.789 (3x too small)."),
        ("de Sitter Gibbons-Hawking TEMPERATURE (Milgrom 2pi)", 2 * np.pi,
         "the 2pi is T_dS = hbar H/2pi k_B. Z=2pi=6.283."),
        ("de Sitter ENTROPY / volume law (Verlinde)", 6.0,
         "Z~6 from the de Sitter entropy budget."),
        ("framework: DENSITY surface-gravity form (c/2)sqrt(G rho)", 2 * sqrt8pi3,
         "Z = 2*sqrt(8pi/3) = 5.789. The '2' is c^2/2R with R NOT a horizon."),
        ("data-preferred (fit to SPARC a0, H0)", 5.80,
         "Z ~ 5.8; 29/5 = 5.800 fits as well/better; nothing derives it."),
    ]
    print(f"  {'route':52}{'Z':>7}{'a0(0)':>9}")
    for name, Z, note in routes:
        print(f"  {name:52}{Z:>7.3f}{a0_of_Z(Z):>8.2f}")
        print(f"       {note}")
    print()

    print("=" * 80)
    print("Why R is NOT a horizon (so the c^2/2R '1/2' is borrowed, not earned)")
    print("=" * 80)
    print("  Framework R = c/sqrt(G rho). The Schwarzschild radius of the mass enclosed in R:")
    print("    M_enc = (4pi/3) rho R^3 ;  R_s = 2G M_enc/c^2 = (8pi/3) R = 8.38 R.")
    print("  So the enclosed mass is 8pi/3 ~ 8.4x the mass that would put a horizon AT R --")
    print("  R sits deep INSIDE its own would-be horizon, so 'surface gravity at R' = c^2/2R is")
    print("  the Schwarzschild FORM applied to a non-horizon radius. The 1/2 is a posit.\n")

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print("  * sqrt(8pi/3) = 2.894 IS first-principles (Friedmann). That part is derived.")
    print("  * The factor of 2 on top of it is NOT derived. de Sitter does NOT give it cleanly:")
    print("    de Sitter horizon -> Z=1 (cH); apparent-horizon half-convention -> Z=2; the")
    print("    Gibbons-Hawking temperature -> Z=2pi (Milgrom); de Sitter entropy -> Z~6 (Verlinde).")
    print("    None is 2*sqrt(8pi/3)=5.789. The de Sitter values (6, 6.28) are NUMERICALLY NEAR")
    print("    5.789 (within ~4-8%), but they are different physics and different numbers.")
    print("  * The framework's 5.789 is a DENSITY (surface-gravity) reading, not a de Sitter")
    print("    horizon value; its '2' is c^2/2R borrowed from Schwarzschild, but R is not a")
    print("    horizon. So: the 2 is a POSIT.")
    print("  * What horizon thermodynamics DOES derive robustly: a0 ~ cH (the EVOLUTION and the")
    print("    order of magnitude), up to an O(1) that is scheme-dependent. The falsifiable")
    print("    prediction (a0 ~ E(z)) is Z-independent, so the un-derived 2 costs nothing there.")
    print("=" * 80)


if __name__ == "__main__":
    main()
