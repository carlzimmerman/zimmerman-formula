#!/usr/bin/env python3
"""
Did I exclude the 20.6 Gpc T^3 correctly, against what Planck ACTUALLY measured?
==============================================================================

Fair challenge: re-verify the matched-circle exclusion against the real Planck
2015 XVIII numbers, not from memory. Verified facts (A&A 594 A18; arXiv:1502.01593):

  * matched-circle search minimum angular radius:  alpha_min ~ 15 deg
    (below this the matching statistic drops below the false-detection level).
  * cubic-T^3 constraint from matched circles: R_i > 0.97 chi_rec at 99% CL.
    (I had half-remembered 0.94; the actual value 0.97 is MORE excluding.)

This script re-derives the circle radius, checks it against those verified bounds,
quantifies the margin, and is honest about the real caveats (obscuration, galactic
mask, COMPACT). Pure stdlib. Run:  python reviews/matched_circle_planck_verification.py
"""

import math

C_KMS = 299792.458
Z_REC = 1089.9
H0, OM, OR = 67.4, 0.315, 9.1e-5
R_S = 144.4
THETA_STAR = 0.0104085

L_FRAME = 20.6                 # cubic fundamental-domain edge (Gpc)
R_I = L_FRAME / 2.0           # inscribed-sphere radius = 10.3 Gpc

ALPHA_MIN_DEG = 15.0         # VERIFIED Planck matched-circle search floor
R_I_BOUND_FRAC = 0.97        # VERIFIED Planck cubic-T^3 matched-circle bound (99% CL)


def E(z):
    OL = 1 - OM - OR
    return math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def chi_rec(n=300000):
    dz = Z_REC / n
    s = sum((0.5 if i in (0, n) else 1.0) / E(i * dz) for i in range(n + 1))
    return (C_KMS / H0) * s * dz / 1e3


def main():
    chi = chi_rec()
    cosa = R_I / chi
    alpha = math.degrees(math.acos(cosa))
    print("=" * 78)
    print("(1) The geometry I used -- re-derived")
    print("=" * 78)
    print(f"   chi_rec (comoving distance to last scattering) = {chi:.2f} Gpc")
    print(f"   framework: cubic edge L = {L_FRAME} Gpc -> R_i = L/2 = {R_I} Gpc")
    print(f"   matched-circle radius: cos(alpha) = R_i/chi_rec = {cosa:.3f}")
    print(f"     alpha = {alpha:.1f} deg")
    print()

    print("=" * 78)
    print("(2) Against VERIFIED Planck 2015 XVIII numbers")
    print("=" * 78)
    bound_Ri = R_I_BOUND_FRAC * chi
    alpha_bound = math.degrees(math.acos(R_I_BOUND_FRAC))
    print(f"   Planck search floor:    alpha_min ~ {ALPHA_MIN_DEG:.0f} deg")
    print(f"   Planck cubic-T^3 bound: R_i > {R_I_BOUND_FRAC} chi_rec = {bound_Ri:.2f} Gpc")
    print(f"     (equivalently: excludes matched circles with alpha > {alpha_bound:.0f} deg)")
    print()
    print(f"   framework R_i        = {R_I:.2f} Gpc   (R_i/chi_rec = {cosa:.3f})")
    print(f"   Planck requires R_i  > {bound_Ri:.2f} Gpc   (R_i/chi_rec > {R_I_BOUND_FRAC})")
    excluded = R_I < bound_Ri
    print(f"   {R_I:.1f} < {bound_Ri:.1f}  ->  EXCLUDED: {excluded}")
    print(f"   margin: R_i is {(bound_Ri-R_I)/bound_Ri*100:.0f}% below the bound;")
    print(f"   its circles ({alpha:.0f} deg) are {alpha/alpha_bound:.1f}x larger than the")
    print(f"   smallest detectable ({alpha_bound:.0f} deg) -- deep inside the searched range.")
    print(f"   This is NOT a borderline case. It is excluded by a wide margin. ✓\n")

    print("=" * 78)
    print("(3) Honest caveats -- and why none rescues a torus this small")
    print("=" * 78)
    print("   * OBSCURATION (ISW, Doppler, integrated terms): the circles are clean only")
    print("     for the Sachs-Wolfe temperature; other contributions are unmatched and")
    print("     dilute the statistic. But the SW term keeps the correlation high, and a")
    print("     42 deg circle has thousands of pixels -- a strong residual signal. At")
    print("     R_i=0.74 chi_rec (vs the 0.97 bound) the dilution cannot hide it.")
    print("   * GALACTIC MASK: part of a large circle crosses the masked plane, lowering")
    print("     sensitivity. Planck folds the mask into the statistic; with 3 axis-pairs")
    print("     (6 directions) some lie in low-mask regions. Does not rescue 0.74.")
    print("   * COMPACT (2024): argues matched-circle bounds are model-dependent and")
    print("     softer than headline -- but for topologies AT/BEYOND the horizon and for")
    print("     general manifolds. A cubic torus with R_i = 0.74 chi_rec sits far INSIDE")
    print("     the horizon, where matched circles are unavoidable. COMPACT does not")
    print("     rescue it (matched_circle_ghost_location.py).\n")

    print("=" * 78)
    print("VERDICT -- yes, I calculated it correctly; re-verified against Planck")
    print("=" * 78)
    print(f"  * The circle radius ({alpha:.0f} deg) is correct standard geometry.")
    print(f"  * Planck's verified numbers: alpha_min ~ 15 deg, R_i > 0.97 chi_rec.")
    print("    (I had loosely recalled 0.94; the real 0.97 is MORE excluding, not less --")
    print("     so the slip was in the conservative direction.)")
    print(f"  * The framework's R_i = 0.74 chi_rec is excluded by a wide margin; its 42 deg")
    print("    circles sit ~3x above the detection floor and are absent in the data.")
    print("  * The real caveats (obscuration, mask, COMPACT) soften the bound NEAR")
    print("    0.97 chi_rec / at the horizon -- not at 0.74. They do not rescue it.")
    print("  Honest conclusion: the exclusion stands, and now it is verified against what")
    print("  Planck actually measured -- not asserted. The 20.6 Gpc cubic T^3 is out.")
    print("  (This is independent of the cosmology surviving: evolving-a0 needs no topology.)")


if __name__ == "__main__":
    main()
