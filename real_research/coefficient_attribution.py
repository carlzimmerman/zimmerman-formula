#!/usr/bin/env python3
"""
Who gets credit for what: the exact coefficient vs the literature.
==================================================================

Carl's point: nobody writes "a0 = cH0/5.78881" exactly. True. This does the precise
math and separates, cleanly, what is established literature (credit it) from the one
piece I could not source (potentially original) -- with the caveats that keep it honest.

Run:  python real_research/coefficient_attribution.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)     # = sqrt(32pi/3)


def main():
    print("=" * 74)
    print("(1) The exact number and the exact identity")
    print("=" * 74)
    print(f"   Z = 2 sqrt(8pi/3) = sqrt(32pi/3) = {Z:.6f}")
    print(f"   a0/cH0 = 1/Z = {1/Z:.6f}")
    print("   a0 = (c/2) sqrt(G rho_c). Via Friedmann rho_c = 3H^2/(8piG):")
    print(f"     a0 = (c/2) sqrt(3/8pi) H = cH / (2 sqrt(8pi/3)) = cH/Z.  [exact]")
    print()

    print("=" * 74)
    print("(2) What the LITERATURE actually writes (and how close)")
    print("=" * 74)
    H0 = 67.4 * 1e3 / MPC
    cH0 = c * H0
    print(f"   {'source / form':<46}{'coeff':>8}{'a0 [m/s^2]':>13}")
    rows = [
        ("Milgrom 1983, 2011:  2pi*a0 = cH0", 2 * math.pi, "literature"),
        ("Milgrom: a0 ~ c sqrt(Lambda/3)/2pi", 2 * math.pi, "literature"),
        ("Verlinde 2016: a0 = cH0/6 (de Sitter entropy)", 6.0, "literature"),
        ("THIS: a0=(c/2)sqrt(Grho)=cH0/sqrt(32pi/3)", Z, "candidate-original"),
    ]
    for name, k, _ in rows:
        print(f"   {name:<46}{k:>8.4f}{cH0/k:>13.3e}")
    print(f"   {'measured a0 (SPARC, McGaugh 2016)':<46}{'':>8}{1.20e-10:>13.3e}")
    print()
    print(f"   the coefficient sqrt(32pi/3)=5.789 differs from:")
    print(f"     Milgrom's 2pi = 6.283  by {(Z-2*math.pi)/(2*math.pi)*100:+.1f}%")
    print(f"     Verlinde's 6          by {(Z-6)/6*100:+.1f}%")
    print("   So it is NOT either literature value -- it is a DIFFERENT coefficient,")
    print("   8% from Milgrom's. The form (c/2)sqrt(G rho) (density, not Lambda or H)")
    print("   I also could not find in Milgrom's papers or the MOND reviews.\n")

    print("=" * 74)
    print("(3) The attribution ledger -- credit precisely")
    print("=" * 74)
    print("   CREDIT THE LITERATURE (these are NOT yours):")
    print("    * a0 ~ cH0  (the order-unity coincidence)        -> Milgrom 1983")
    print("    * the specific coefficient 2pi (2pi a0 = cH0)    -> Milgrom")
    print("    * a0 ~ c sqrt(Lambda) (dark-energy form)         -> Milgrom")
    print("    * a0 = cH0/6 (entropy coefficient)               -> Verlinde 2016")
    print("    * the IDEA that a0 may EVOLVE with z             -> Milgrom (noted);")
    print("      tested Gnedin 2008; MEASURED Tortora/MUSE-DARK 2026, de Graaff 2024")
    print()
    print("   POTENTIALLY YOURS (I could not source these):")
    print("    * the specific coefficient sqrt(32pi/3) = 5.78881, i.e. a0 = cH0/5.78881")
    print("    * the density / surface-gravity FORM a0 = (c/2)sqrt(G rho_c) = c^2/2R_dyn")
    print("    * the reading Z^2 = 32pi/3 = (2)^2 x (8pi/3) Friedmann factor\n")

    print("=" * 74)
    print("(4) The honest caveats on the 'potentially yours' part")
    print("=" * 74)
    print("   1. It is ALGEBRAICALLY a0 ~ cH0 re-coefficiented: the sqrt(32pi/3) is just")
    print("      '1/2 (Schwarzschild) x sqrt(8pi/3) (Friedmann/dynamical time)'. A new")
    print("      EXPRESSION/coefficient of Milgrom's coincidence, not new physics.")
    print("   2. The coefficient (5.789) sits 8% from Milgrom's (6.283), well inside a0's")
    print("      ~20% systematic -- so it is a different VALUE of the same coincidence,")
    print("      not yet a distinct measured prediction.")
    print("   3. It is NOT derived (the eta-invariant 'derivation' is false; the coefficient")
    print("      is a posit, Z2_vindication.py).")
    print("   4. 'I could not find it' is not 'it does not exist': the MOND literature is")
    print("      vast (Milgrom alone has dozens of papers). VERIFY with a proper search /")
    print("      the MOND community (McGaugh, Lelli, Milgrom) before claiming priority.\n")

    print("=" * 74)
    print("(5) An honest sentence you could actually write")
    print("=" * 74)
    print('   "Following Milgrom\'s coincidence a0 ~ cH0, we adopt the specific form')
    print('    a0 = (c/2) sqrt(G rho_c) = cH(z)/sqrt(32pi/3), i.e. half the surface gravity')
    print('    of the cosmic dynamical scale. We do not derive the coefficient; we note it')
    print('    is within ~8% of Milgrom\'s 2pi value and, unlike a constant a0, predicts an')
    print('    evolution a0(z) prop E(z) consistent with the measured RAR evolution')
    print('    (MUSE-DARK 2026)." -- credits Milgrom + MUSE-DARK, claims only the specific')
    print("   form/coefficient, and is honest that it is a posit, not a theorem.")


if __name__ == "__main__":
    main()
