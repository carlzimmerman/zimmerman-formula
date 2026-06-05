#!/usr/bin/env python3
"""
THE 32pi COEFFICIENT -- is it un-derivable numerology, or data-selected? An honest landscape.
=============================================================================================
a0 = c^2 sqrt(Lambda/32pi),  and  32pi = 4 x 8pi.
  * the 8pi is the Einstein coupling rho_Lambda = Lambda c^2/(8 pi G) -- FORCED, not a choice.
  * the remaining factor 4 = (1/2)^2 is the prefactor in the equivalent form a0 = (c/2) sqrt(G rho_Lambda).
So the WHOLE coefficient question reduces to one number: the '1/2'. Is it forced?

We define the dimensionless coefficient via  a0 = c H_Lambda / Z,  H_Lambda = c sqrt(Lambda/3)  (the de Sitter rate),
so the framework is exactly  Z = sqrt(32pi/3) = 5.789.  Different physical principles predict different Z. The
decisive question is NOT 'which O(1) is prettiest' but 'which Z values does the DATA allow?' -- because a0 is
measured (to within the interpolating-function systematic). If the data excludes the naive guesses and selects
Z ~ 5-6, then 32pi is data-selected and well-motivated, NOT free numerology.

This script computes Z for each candidate principle and the data-allowed band, and reports the honest verdict.
Reproducible: `python coefficient_landscape.py`. Needs numpy.
"""
import numpy as np

C = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
LAM = 3 * OmL * H0**2 / C**2                 # cosmological constant (1/m^2)
H_LAM = C * np.sqrt(LAM / 3)                  # de Sitter (asymptotic) Hubble rate
cH_LAM = C * H_LAM                            # = c^2 sqrt(Lambda/3), the 'Z=1' acceleration
A0_FRAME = C**2 * np.sqrt(LAM / (32 * np.pi))  # framework a0 = 9.36e-11

# observed a0 spans the interpolating-function systematic:
A0_SIMPLE = 9.1e-11     # simple-mu best fit to SPARC (min RAR scatter)
A0_RAR = 1.20e-10       # McGaugh RAR-function normalization
A0_LO, A0_HI = 9.0e-11, 1.30e-10   # honest spread


def Z_of_a0(a0):
    return cH_LAM / a0


def main():
    print("#" * 100)
    print("# THE 32pi COEFFICIENT: un-derivable numerology, or data-selected? (a0 = c H_Lambda / Z)")
    print("#" * 100 + "\n")
    print(f"  Lambda = {LAM:.3e} /m^2 ;  c H_Lambda = {cH_LAM:.3e} m/s^2 (the Z=1 scale) ;  framework a0 = {A0_FRAME:.3e}\n")

    # ---- the data-allowed band on Z ----
    print("=" * 100)
    print("(1) what Z does the DATA allow?  (a0 is measured, up to the interpolating-function systematic)")
    print("=" * 100)
    print(f"   {'a0 measurement':<34}{'a0 [m/s^2]':>13}{'-> Z':>10}")
    for lab, a0 in [("simple-mu best fit (SPARC)", A0_SIMPLE), ("McGaugh RAR normalization", A0_RAR),
                    ("low end of systematic", A0_HI), ("high end of systematic", A0_LO)]:
        print(f"   {lab:<34}{a0:>13.2e}{Z_of_a0(a0):>10.2f}")
    Zlo, Zhi = Z_of_a0(A0_HI), Z_of_a0(A0_LO)
    print(f"\n   DATA-ALLOWED BAND:  Z in [{Zlo:.1f}, {Zhi:.1f}]  (central ~{Z_of_a0(0.5*(A0_SIMPLE+A0_RAR)):.1f}).\n")

    # ---- candidate principles ----
    print("=" * 100)
    print("(2) what Z does each PHYSICAL principle predict?  (does the data keep it or kill it?)")
    print("=" * 100)
    principles = [
        ("naive horizon accel  a0 = c^2/R_dS",          1.0,                       "the simplest guess: a0 = cH_Lambda"),
        ("de Sitter surface gravity (kappa=c^2/2R)",    2.0,                       "factor-2 convention"),
        ("vacuum free-fall, NO 1/2:  c sqrt(G rho_L)",  np.sqrt(8 * np.pi / 3),    "drop the 1/2 prefactor -> Z=sqrt(8pi/3)"),
        ("Unruh-deSitter onset (a ~ a_dS)",             1.0,                       "Milgrom vacuum-MOND transition scale"),
        ("FRAMEWORK: (c/2) sqrt(G rho_Lambda)",         np.sqrt(32 * np.pi / 3),   "8pi forced + 1/2 free-fall prefactor"),
        ("Gibbons-Hawking thermal  a0 = cH_Lambda/2pi", 2 * np.pi,                 "horizon temperature / 2pi periodicity"),
    ]
    print(f"   {'principle':<44}{'Z':>8}{'a0 pred':>12}{'verdict vs data':>20}")
    for name, Z, note in principles:
        a0p = cH_LAM / Z
        keep = "CONSISTENT" if Zlo <= Z <= Zhi else ("edge" if abs(Z - Zlo) < 0.5 or abs(Z - Zhi) < 0.5 else "EXCLUDED")
        star = " <--" if "FRAMEWORK" in name else ""
        print(f"   {name:<44}{Z:>8.2f}{a0p:>12.2e}{keep:>20}{star}")
    print()

    # ---- the honest verdict ----
    print("=" * 100)
    print("(3) HONEST VERDICT")
    print("=" * 100)
    print(f"""   The data band Z in [{Zlo:.1f}, {Zhi:.1f}] is NARROW and it is NOT centered on the simple guesses:
     * Z=1   (a0 = cH_Lambda, naive horizon / Unruh-dS onset)            -> EXCLUDED (a0 would be ~6x too big)
     * Z=2-3 (surface gravity; the no-1/2 vacuum form sqrt(8pi/3)=2.9)   -> EXCLUDED (a0 ~2-6x too big)
     * Z=5.79 (FRAMEWORK, sqrt(32pi/3))                                  -> CONSISTENT (sits in the band)
     * Z=6.28 (thermal 2pi)                                              -> edge / mildly disfavored (upper rim)

   So the coefficient is NOT free numerology. The combination 'a0 is measured' + '8pi is forced' already SELECTS
   Z ~ 5-6 and EXCLUDES every simpler O(1). The framework's sqrt(32pi/3) is the value you get from the one extra,
   standard ingredient -- the 1/2 free-fall prefactor in a0 = (c/2) sqrt(G rho_Lambda) -- and it lands in the band.

   WHAT REMAINS GENUINELY OPEN (stated honestly): the data cannot yet separate sqrt(32pi/3)=5.79 from thermal
   2pi=6.28 -- an ~8% question, well below the ~20-30% interpolating-function systematic. So '32pi is un-derivable'
   was too strong; the accurate statement is:

       The SCALE (a0 ~ c^2 sqrt(Lambda)) and the BALLPARK coefficient (Z ~ 5-6) are forced and data-selected;
       only the last ~8% (sqrt(32pi/3) vs 2pi) is not uniquely pinned -- and it is below current precision.

   And it is MOOT for the empirical program: the coefficient-free bridge (a0(z)/a0(0) = (rho_DE)^(1/2)) cancels Z
   entirely, so the evolution test (beta) does not depend on whether the last 8% is 32pi/3 or 2pi.""")

    print("\n" + "#" * 100)
    print(f"# BOTTOM LINE: data selects Z in [{Zlo:.1f},{Zhi:.1f}]; framework sqrt(32pi/3)={np.sqrt(32*np.pi/3):.2f} is IN it, naive guesses (Z=1-3) are OUT.")
    print("# 32pi is data-selected + well-motivated (8pi forced, 1/2 standard), not numerology. Residual: ~8% vs 2pi, moot for the bridge.")
    print("#" * 100)


if __name__ == "__main__":
    main()
