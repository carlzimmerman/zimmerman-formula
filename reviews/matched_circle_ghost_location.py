#!/usr/bin/env python3
"""
Where are the ghosts? Matched-circle geometry for a 20.6 Gpc cubic torus.
=========================================================================

Fair challenge from Carl: when I said the 20.6 Gpc T^3 is excluded, I used the
Bayesian R_i bound and never computed WHERE the topological ghost images
(matched circles) actually land. If they fell at an angular scale Planck did not
probe, the exclusion would be wrong. So let us do the geometry.

Matched-circle fact (Cornish-Spergel-Starkman): in a multiply-connected space
the last-scattering sphere (radius chi_rec) self-intersects with its translated
copies. For a translation of length L, the two LSS spheres (each radius chi_rec)
overlap in a CIRCLE whose angular radius alpha seen by us satisfies

        cos(alpha) = (L/2) / chi_rec .

Planck's blind search detects circles down to alpha ~ 15 deg (smaller circles
drown in noise), over ALL sky directions and both correlation signs. So a
topology predicting circles with alpha > ~15 deg is testable -- and was tested.

Pure stdlib. Run:  python reviews/matched_circle_ghost_location.py
"""

import math

C_KMS = 299792.458
Z_REC = 1089.9
# Planck 2018 background
H0, OM, OR = 67.4, 0.315, 9.1e-5
R_S = 147.0          # Mpc, comoving sound horizon at last scattering (Planck)
THETA_STAR = 0.0104085   # measured angular size of sound horizon (Planck, ~0.03%)

L_FRAME = 20.6       # Gpc, cubic fundamental-domain edge
ALPHA_MIN_DEG = 15.0 # Planck matched-circle detection floor (deg)


def E(z):
    OL = 1.0 - OM - OR
    return math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def chi_rec_Gpc(n=300000):
    dz = Z_REC / n
    s = 0.0
    for i in range(n + 1):
        z = i * dz
        w = 0.5 if (i == 0 or i == n) else 1.0
        s += w / E(z)
    return (C_KMS / H0) * s * dz / 1e3


def alpha_deg(L, chi):
    x = (L / 2.0) / chi
    if x >= 1.0:
        return None              # no circles: domain bigger than the LSS
    return math.degrees(math.acos(x))


def main():
    chi = chi_rec_Gpc()
    print("=" * 80)
    print("Matched-circle ghosts of a cubic T^3, edge L, given chi_rec")
    print("=" * 80)
    print(f"  chi_rec (comoving distance to last scattering) = {chi:.2f} Gpc")
    print(f"  matched-circle angular radius:  cos(alpha) = (L/2)/chi_rec")
    print(f"  Planck detects circles with alpha > ~{ALPHA_MIN_DEG:.0f} deg (blind, all sky).")
    print()
    a_frame = alpha_deg(L_FRAME, chi)
    print(f"  FRAMEWORK  L = {L_FRAME} Gpc  ->  (L/2)/chi_rec = {(L_FRAME/2)/chi:.3f}")
    print(f"             matched-circle radius alpha = {a_frame:.1f} deg")
    print(f"             {a_frame:.0f} deg  >>  {ALPHA_MIN_DEG:.0f} deg detection floor "
          f"-> Planck WOULD have seen these circles. It did not. EXCLUDED.")
    print()
    print("  The ghosts are NOT 'somewhere else' -- they are big ~42 deg circles,")
    print("  right in the heart of the searched range. Sweep of L:")
    print(f"  {'L [Gpc]':>9} {'(L/2)/chi':>10} {'alpha [deg]':>12} {'Planck':>22}")
    for L in (14, 18, 20.6, 24, 27, 28, 30):
        a = alpha_deg(L, chi)
        if a is None:
            tag = "no circles (L>2chi_rec)"
            astr = "  --"
        else:
            tag = "DETECTABLE -> excluded" if a > ALPHA_MIN_DEG else "too small to detect"
            astr = f"{a:.1f}"
        mark = " <== framework" if abs(L - L_FRAME) < 0.01 else ""
        print(f"  {L:>9.1f} {((L/2)/chi if (L/2)/chi<1 else float('nan')):>10.3f} "
              f"{astr:>12} {tag:>22}{mark}")
    L_safe = 2 * chi * math.cos(math.radians(ALPHA_MIN_DEG))
    print(f"\n  To hide the ghosts (alpha < {ALPHA_MIN_DEG:.0f} deg) a cubic torus needs")
    print(f"  L > {L_safe:.1f} Gpc, OR no circles at all needs L > 2 chi_rec = "
          f"{2*chi:.1f} Gpc. The framework's {L_FRAME} Gpc is well below both.")
    print()

    print("=" * 80)
    print("Could the framework move chi_rec to hide them? No -- the CMB pins it.")
    print("=" * 80)
    chi_needed = (L_FRAME / 2) / math.cos(math.radians(ALPHA_MIN_DEG))
    theta_if = R_S / (chi_needed * 1e3)
    print(f"  To push alpha below {ALPHA_MIN_DEG:.0f} deg you would need chi_rec < "
          f"{chi_needed:.1f} Gpc")
    print(f"  (a {(1-chi_needed/chi)*100:.0f}% reduction from {chi:.1f} Gpc).")
    print(f"  But chi_rec is fixed by the CMB acoustic scale theta* = r_s/chi_rec:")
    print(f"     measured theta*           = {THETA_STAR:.6f} rad  (Planck, ~0.03%)")
    print(f"     theta* if chi_rec={chi_needed:.1f} Gpc = {theta_if:.6f} rad  "
          f"({(theta_if/THETA_STAR-1)*100:+.0f}%)")
    print(f"  A {abs(theta_if/THETA_STAR-1)*100:.0f}% shift in theta* is thousands of")
    print("  sigma off the acoustic peaks. Any cosmology that fits the CMB has")
    print("  chi_rec ~ 14 Gpc -- so the ghosts stay at ~42 deg. chi_rec is not a free knob.\n")

    print("=" * 80)
    print("Does the Z2 (in T^3/Z2) move them, or the evolving-a0?  No.")
    print("=" * 80)
    print("  * T^3/Z2 still CONTAINS the three T^3 translations, so the translation")
    print("    circles at ~42 deg are still predicted. The Z2 ADDS inversion circles;")
    print("    it cannot delete the translation ones. Planck searches both correlation")
    print("    signs (S+ and S-) and all relative orientations, so the extra Z2")
    print("    (anti-)circles are covered too.")
    print("  * evolving-a0 modifies GALAXY-scale dynamics (a < a0), not the smooth")
    print("    background expansion or CMB photon geodesics, so it does not distort")
    print("    the circles or move chi_rec.")
    print()
    print("  HONEST loophole (the only one): the matched-circle search assumes")
    print("  ~undistorted ghost images (the COMPACT-2024 model-dependence point). A")
    print("  theory that smeared the ghosts could evade circle-matching. The framework")
    print("  supplies NO such mechanism -- so for THIS construction the ghosts are")
    print("  sharp circles at ~42 deg, and their absence excludes it.\n")

    print("=" * 80)
    print("VERDICT -- I did the math you asked for; the ghosts are not hidden")
    print("=" * 80)
    print(f"  A 20.6 Gpc cubic torus predicts matched circles of angular radius")
    print(f"  alpha ~ {a_frame:.0f} deg -- large, blind-searchable, and squarely inside")
    print("  Planck's sensitivity. They are absent in the data. To put the ghosts")
    print("  'somewhere else' you would need L > ~27 Gpc or chi_rec < ~11 Gpc, and the")
    print("  CMB acoustic scale forbids moving chi_rec. So the exclusion stands, now")
    print("  via the exact geometry rather than a generic bound. (And note: this is in")
    print("  tension with the BOSS parity-odd claim being read as a 20.6 Gpc signal --")
    print("  the same topology would have rung these CMB circles, and it didn't.)")


if __name__ == "__main__":
    main()
