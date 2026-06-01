#!/usr/bin/env python3
"""
r = 0.0149 = 1/(2Z^2): the tensor-to-scalar ratio -- forward-testable, but a moving target.
==========================================================================================

r = 1/(2Z^2) = 0.0149 is a CMB inflation observable (tensor-to-scalar ratio),
testable by LiteBIRD (~2028-29) / CMB-S4 (2030+). So unlike the cosmic-Weinberg
coincidence, it IS forward-falsifiable -- a point in its favor. But the QUESTION
is whether it is a derived prediction or numerology, and the repo's OWN status
file answers it. This script verifies the history with numbers.

Pure stdlib. Run:  python reviews/tensor_scalar_r_audit.py
"""

import math

ALPHA = 1 / 137.035999
Z2 = 32 * math.pi / 3
R_BOUND_2021 = 0.036       # BICEP/Keck 2021, 95% CL upper limit on r
LITEBIRD_SIGMA = 0.001     # LiteBIRD target precision on r


def main():
    print("=" * 78)
    print("(1) The three 'predicted' values of r -- a moving target")
    print("=" * 78)
    r_8alpha = 8 * ALPHA
    r_inv2Z2 = 1 / (2 * Z2)
    r_8overZ2 = 8 / Z2
    print(f"   version 1:  r = 8*alpha   = {r_8alpha:.4f}   (the FIRST Z2 prediction)")
    print(f"   version 2:  r = 8/Z^2     = {r_8overZ2:.4f}   (perturbation_theory.md App. D)")
    print(f"   version 3:  r = 1/(2Z^2)  = {r_inv2Z2:.4f}   (the CURRENT prediction)")
    print()
    print(f"   current data bound:  r < {R_BOUND_2021}  (BICEP/Keck 2021, 95% CL)")
    for name, r in [("8*alpha", r_8alpha), ("8/Z^2", r_8overZ2), ("1/(2Z^2)", r_inv2Z2)]:
        status = "RULED OUT" if r > R_BOUND_2021 else "consistent"
        print(f"     r({name}) = {r:.4f}  -> {status}")
    print()
    print("   The framework settled on r = 1/(2Z^2) = 0.0149 -- the ONLY one of its")
    print("   three formulas that survives the current bound. Per the repo's own")
    print("   Z2_FRAMEWORK_STATUS_MAY2026.md: 'r = 0.015 was adopted AFTER r = 8*alpha")
    print("   = 0.058 was ruled out by data ... has NO derivation.' That is a")
    print("   prediction that TRACKS THE DATA, not the theory. \n")

    print("=" * 78)
    print("(2) The repo's OWN verdict (not mine)")
    print("=" * 78)
    print("   Z2_FRAMEWORK_STATUS_MAY2026.md:")
    print("     * 'r (tensor/scalar) | 1/(2Z2) = 0.015 | NO VALID DERIVATION'")
    print("     * 'The claimed derivation relied on h_x being projected out (WRONG)'")
    print("     * 'Appendix D gets r ~ 8/Z2 ~ 0.24, not 0.015'")
    print("     * 'It fits current constraints but has NO derivation'")
    print("     * 'r != 0.015 | Only a conjecture'")
    print("   The author already classified this correctly. I agree.\n")

    print("=" * 78)
    print("(3) Is it forward-testable? Yes -- but confirmation would carry little weight")
    print("=" * 78)
    print(f"   LiteBIRD precision sigma(r) ~ {LITEBIRD_SIGMA}; r=0.015 would be a "
          f"~{r_inv2Z2/LITEBIRD_SIGMA:.0f} sigma detection if real.")
    print("   So it IS falsifiable (a genuine point). BUT:")
    print("    * r ~ 0.01-0.02 is generic to many inflation models -- not distinctive to Z2;")
    print("    * the value was RETROFITTED (0.058 -> 0.015 after data), so a hit confirms")
    print("      the data-fitting, not the theory;")
    print("    * the target has already MOVED once -- if LiteBIRD finds r != 0.015, the")
    print("      track record says a fourth formula would appear. That is the opposite")
    print("      of a real falsifiable commitment.\n")

    print("=" * 78)
    print("VERDICT -- balanced, and it is NOT the same tier as a0(z)")
    print("=" * 78)
    print("  CONCEDE: r = 1/(2Z^2) = 0.0149 is forward-testable by LiteBIRD, and it sits")
    print("  comfortably inside current bounds. That is more than the cosmic-Weinberg")
    print("  coincidence offers.")
    print("  BUT: it is numerology by the repo's own assessment (NO derivation), and a")
    print("  MOVING TARGET (8*alpha=0.058 ruled out -> 1/(2Z^2)=0.015 adopted; App. D")
    print("  gives 0.24). Three incompatible formulas, the surviving one chosen to fit.")
    print()
    print("  The sharp contrast: a0(z) ~ E(z) is Z-INDEPENDENT and PRE-REGISTERED -- the")
    print("  prediction does not move when Z or the data move. r = 1/(2Z^2) is")
    print("  Z-DEPENDENT and POST-HOC -- it already moved once. Same 'CMB prediction'")
    print("  label, opposite epistemics. Keep r off the survivor tier; keep a0(z) on it.")


if __name__ == "__main__":
    main()
