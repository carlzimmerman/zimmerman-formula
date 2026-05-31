#!/usr/bin/env python3
"""
Model-building step 2: does the E6 SUSY-GUT structure predict gauge unification?
================================================================================

The (T^2)^3/(Z2xZ2) orbifold preserves N=1 SUSY and gives an E6 GUT. A GUT makes a
RIGOROUS, semi-testable structural prediction the v11 numerology never did: the three
SM gauge couplings, run up, should MEET -- and the unification condition PREDICTS
sin^2(theta_W) at M_Z given alpha_em and alpha_s.

This is the HONEST origin of the weak mixing angle: sin^2 = 3/8 at the GUT scale,
running down to ~0.231 -- not the v11 fit '3/13'. We compute the one-loop prediction
for both the non-SUSY SM and the SUSY (MSSM) spectrum and compare to the measured
value. (The construction is SUSY, so the MSSM line is the relevant one.)

Pure stdlib.  Run:  python reviews/e6_gauge_unification.py
"""

import math

# measured inputs at M_Z (PDG)
MZ = 91.1876
A_EM_INV = 127.951      # alpha_em^-1(M_Z)
A_S_INV = 1 / 0.1179    # alpha_s^-1(M_Z) = 8.482
SIN2_MEAS = 0.23122     # measured sin^2(theta_W), MS-bar

# one-loop beta coefficients (GUT-normalized alpha_1 = 5/3 alpha_Y)
B_SM = (41/10, -19/6, -7)        # Standard Model
B_MSSM = (33/5, 1, -3)           # MSSM (SUSY)


def predict_sin2(b):
    """Predict sin^2(theta_W)(M_Z) from one-loop unification of alpha_1,2,3,
    given alpha_em and alpha_s. Imposing alpha_1=alpha_2=alpha_3 at one scale:
        (a1^-1 - a2^-1)/(b1-b2) = (a2^-1 - a3^-1)/(b2-b3),
    with a1^-1=(3/5)(1-s)A, a2^-1=sA, a3^-1=alpha_s^-1, A=alpha_em^-1.
    Solve for s."""
    b1, b2, b3 = b
    A = A_EM_INV
    r = (b1 - b2) / (b2 - b3)
    # A(0.6 - 1.6 s) = r (s A - A_S_INV)  ->  s = (0.6 A + r A_S_INV)/(A(r+1.6))
    s = (0.6 * A + r * A_S_INV) / (A * (r + 1.6))
    return s


def unification_scale(b, sin2):
    """Scale and coupling where alpha_2 meets alpha_3 (one loop)."""
    b1, b2, b3 = b
    a2_inv = sin2 * A_EM_INV
    a3_inv = A_S_INV
    t = (a2_inv - a3_inv) / ((b2 - b3) / (2 * math.pi))     # t = ln(mu/M_Z)
    mu = MZ * math.exp(t)
    aG_inv = a2_inv - (b2 / (2 * math.pi)) * t
    return mu, aG_inv


def main():
    print("=" * 78)
    print("Gauge coupling unification as a structural prediction of the E6 SUSY GUT")
    print("=" * 78)
    print(f"   inputs at M_Z:  alpha_em^-1 = {A_EM_INV},  alpha_s^-1 = {A_S_INV:.3f}")
    print(f"   measured sin^2(theta_W) = {SIN2_MEAS}\n")

    for label, b in [("Standard Model (no SUSY)", B_SM), ("MSSM / SUSY  <-- this case", B_MSSM)]:
        s = predict_sin2(b)
        err = (s - SIN2_MEAS) / SIN2_MEAS * 100
        mu, aG = unification_scale(b, SIN2_MEAS)
        print(f"   {label}")
        print(f"     predicted sin^2(theta_W) = {s:.4f}   (measured {SIN2_MEAS}, off {err:+.1f}%)")
        print(f"     unification: M_GUT ~ {mu:.1e} GeV,  alpha_GUT^-1 ~ {aG:.1f}")
        print()

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("  REAL, RIGOROUS, AND IT WORKS (for SUSY):")
    print("   * The SUSY (MSSM) spectrum predicts sin^2(theta_W) = 0.231, matching the")
    print("     measured 0.2312 to ~0.1%. The non-SUSY SM predicts 0.208 (~10% off).")
    print("   * Couplings unify at M_GUT ~ 2x10^16 GeV, alpha_GUT^-1 ~ 24 -- the famous")
    print("     SUSY-GUT success. This is a genuine structural prediction (group theory")
    print("     + RG running), NOT moduli-dependent at leading order.")
    print("   * This is the HONEST origin of sin^2(theta_W): the GUT relation 3/8 at")
    print("     M_GUT, run down to ~0.231 at M_Z. It REPLACES the v11 fit 'sin^2 = 3/13'")
    print("     (0.2308) with real physics that also explains WHY it is ~0.23.")
    print()
    print("  HONEST CAVEATS:")
    print("   * This is a success of SUSY GUTs IN GENERAL (any SU(5)/SO(10)/E6) -- it is")
    print("     INHERITED by the framework, not distinctive to it. Good, but not unique.")
    print("   * SUSY has not been found at the LHC (superpartners > ~1 TeV) -- the")
    print("     prediction's premise is under experimental pressure.")
    print("   * Two-loop + threshold corrections shift these at the ~% level; the absolute")
    print("     M_GUT/alpha_GUT carry threshold/moduli dependence.")
    print()
    print("  NET: adopting the real E6 SUSY-GUT structure buys a genuine, ~0.1%")
    print("  prediction for sin^2(theta_W) from gauge unification -- a real upgrade over")
    print("  the 3/13 fit -- at the price of predicting SUSY, which is so far unseen.")


if __name__ == "__main__":
    main()
