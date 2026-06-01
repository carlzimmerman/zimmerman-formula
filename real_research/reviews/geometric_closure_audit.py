#!/usr/bin/env python3
"""
Does the geometric closure actually CLOSE? A parameter count.
=============================================================

The geometric_closure/ folder claims "ALL of physics emerges from Z^2 = 8x(4pi/3)".
Carl's own HONEST_ASSESSMENT.md tiers it honestly:
  T1 = mathematical identities (tautologies, "not predictions")
  T2 = a0 = cH0/Z (a HYPOTHESIS; a0(z) is the confirming test)
  T3 = the constant-fits (alpha, masses, angles) -- "striking coincidences ...
       lack theoretical explanation", self-rated 70%.

A genuine "theory of everything" closure must COMPRESS: far FEWER free inputs than
outputs (the Standard Model: ~19 parameters -> infinitely many predictions). We test
T3 directly: count the free integer coefficients used to produce each "derived"
constant, and compare to the number of constants produced.

Pure stdlib.  Run:  python reviews/geometric_closure_audit.py
"""

# (observable, formula, list of CHOSEN small integers in that formula)
# taken from research/geometric_closure/INDEX.md and HONEST_ASSESSMENT.md
T3 = [
    ("alpha^-1",      "4Z^2 + 3",            [4, 3]),
    ("sin^2 theta_W", "6/(5Z - 3)",          [6, 5, 3]),
    ("m_mu/m_e",      "6Z^2 + Z",            [6, 1]),
    ("m_p/m_e",       "54Z^2 + 6Z - 8",      [54, 6, 8]),
    ("m_nu",          "m_e*10^(-Z)/8",       [10, 8]),
    ("Higgs lambda",  "1/8",                 [8]),
    ("Cabibbo",       "2/9",                 [2, 9]),
    ("sin^2 th12",    "1/3 - 1/(3Z^2)",      [3, 3]),
    ("sin^2 th23",    "1/2 - 1/(4Z)",        [2, 4]),
    ("sin^2 th13",    "1/(Z^2 + 11)",        [11]),
    ("Omega_Lambda",  "3Z/(8 + 3Z)",         [3, 8, 3]),
    ("cosm. const.",  "log = 4Z^2 - 12",     [4, 12]),
    ("M_Pl/m_W",      "log = 3Z",            [3]),
    ("'42'",          "round(Z^2 + 8)",      [8]),
]

# the same observable, derived with DIFFERENT formulas elsewhere in the repo
MULTIPLE = {
    "sin^2 theta_W": ["6/(5Z-3)", "3/13", "1/4 - alpha_s/2pi"],
    "Omega_Lambda":  ["3Z/(8+3Z)", "13/19", "sqrt(3pi/2)/(1+sqrt(3pi/2))"],
    "m_p/m_e":       ["54Z^2+6Z-8", "(4Z^2+3)*67/5", "alpha^-1 * 2Z^2/5"],
    "m_mu/m_e":      ["6Z^2+Z", "37Z^2/6", "Z(6Z+1)"],
}


def main():
    print("=" * 78)
    print("(1) Parameter count of the constant-value closure (Tier 3)")
    print("=" * 78)
    n_out = len(T3)
    total_int = 0
    print(f"  {'observable':<15}{'formula':<22}{'chosen integers':<18}{'#':>3}")
    for name, formula, ints in T3:
        total_int += len(ints)
        print(f"  {name:<15}{formula:<22}{str(ints):<18}{len(ints):>3}")
    print()
    print(f"  INPUTS:  1 continuous constant (Z^2)  +  {total_int} chosen integers")
    print(f"  OUTPUTS: {n_out} physical constants")
    print(f"  => free choices ({1+total_int}) EXCEED outputs ({n_out}) by "
          f"{(1+total_int)/n_out:.1f}x.")
    print(f"     About {total_int/n_out:.1f} freely chosen integers PER constant.")
    print("  A closure must COMPRESS (inputs << outputs). This INFLATES (inputs > outputs).")
    print("  It is a parametrization with more knobs than data, not a derivation.\n")

    print("=" * 78)
    print("(2) The closure is not even unique: multiple formulas per observable")
    print("=" * 78)
    for obs, forms in MULTIPLE.items():
        print(f"  {obs}:")
        for f in forms:
            print(f"      = {f}")
    print("  One number cannot be DERIVED several incompatible ways. Multiple formulas")
    print("  per observable is the signature of FITTING -- you pick the one that lands.\n")

    print("=" * 78)
    print("VERDICT -- does the geometric framework close? Partly, honestly:")
    print("=" * 78)
    print("  YES, the DISCRETE/STRUCTURAL geometry closes (this is real):")
    print("   * cube (8 vtx, 12 edges, 6 faces) -> orbifold (T^2)^3/(Z2xZ2) ->")
    print("     E6 GUT -> SM gauge group + 3 chiral generations. A legitimate")
    print("     construction (reviews/e6_orbifold_spectrum.py). Tier 1 geometry is")
    print("     genuine; the structure genuinely maps to the SM's discrete data.")
    print("   * a0(z) ~ H(z) (Tier 2) -- your own confirming test; the one forward,")
    print("     falsifiable prediction (reviews/a0_evolution_predictions.py).")
    print()
    print("  NO, the constant-VALUE closure (Tier 3) does not close:")
    print("   * it uses MORE freely chosen integers than constants produced (above);")
    print("   * several constants have 2-3 incompatible formulas;")
    print("   * your own HONEST_ASSESSMENT rates it 70% with 'no theoretical")
    print("     explanation'. That is the honest rating, and the count confirms it.")
    print()
    print("  So 'working on the geometric framework' rigorously gives: the geometry")
    print("  closes into a real construction + a real prediction; the CONSTANTS do not")
    print("  close -- they are fit, one tunable formula at a time. The first half is")
    print("  the breakthrough worth having; the second half is the parametrization.")


if __name__ == "__main__":
    main()
