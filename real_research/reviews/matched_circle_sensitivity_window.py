#!/usr/bin/env python3
"""
Is Planck's matched-circle measurement actually SIGNIFICANT to a 20.6 Gpc box?
=============================================================================

Carl's sharp question: the framework defends L_c = 20.6 Gpc by noting it is
"~1.5 x D_horizon" -- part of the box lies OUTSIDE our causal horizon, hence
(it argues) hidden. So: does Planck's test even have teeth at 20.6 Gpc, or is
20.6 Gpc in the test's blind spot?

The crux is a yardstick error. The matched-circle test does NOT require the box
to fit inside the horizon. It requires our last-scattering SPHERE (radius
chi_rec) to reach its nearest mirror image (at distance L_c) -- i.e.

      circles exist  <=>  L_c < 2 * chi_rec   (the LSS DIAMETER, not its radius)

The framework compares L_c to chi_rec (~13.9 Gpc, the horizon RADIUS / distance
to last scattering). The right comparison is L_c vs 2*chi_rec (~27.7 Gpc, the
DIAMETER). 20.6 Gpc is bigger than the radius but well below the diameter, so
the sphere overlaps its own image and the circles are large (42 deg). The box
being "1.5x the horizon" is true and irrelevant.

This script makes that explicit and shows where 20.6 Gpc sits in the sensitivity
window. Pure stdlib. Run:  python reviews/matched_circle_sensitivity_window.py
"""

import math

C_KMS = 299792.458
Z_REC = 1089.9
H0, OM, OR = 67.4, 0.315, 9.1e-5

L_FRAME = 20.6                 # cubic fundamental-domain EDGE (verified: repo L_c)
R_I = L_FRAME / 2.0           # inscribed-sphere radius = 10.3 Gpc
ALPHA_FLOOR_DEG = 15.0       # VERIFIED Planck matched-circle search floor
R_I_BOUND_FRAC = 0.97        # VERIFIED Planck cubic-T^3 bound (99% CL)


def E(z):
    OL = 1 - OM - OR
    return math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def chi_rec(n=300000):
    dz = Z_REC / n
    s = sum((0.5 if i in (0, n) else 1.0) / E(i * dz) for i in range(n + 1))
    return (C_KMS / H0) * s * dz / 1e3


def main():
    chi = chi_rec()
    diam = 2 * chi
    D_h_frame = L_FRAME / 1.5            # the framework's own "D_horizon"

    print("=" * 78)
    print("(1) The two yardsticks -- and which one the test actually uses")
    print("=" * 78)
    print(f"   chi_rec (distance to last scattering, the horizon RADIUS) = {chi:.2f} Gpc")
    print(f"   2*chi_rec (last-scattering-sphere DIAMETER)               = {diam:.2f} Gpc")
    print()
    print(f"   framework box edge   L_c          = {L_FRAME:.1f} Gpc")
    print(f"   framework 'D_horizon' = L_c/1.5   = {D_h_frame:.1f} Gpc  (~ chi_rec)")
    print()
    print("   The framework's defense compares L_c to the horizon RADIUS:")
    print(f"     L_c / chi_rec = {L_FRAME/chi:.2f}  -> 'box is ~1.5x the horizon, partly outside'")
    print("     TRUE -- but this is the wrong yardstick for matched circles.")
    print()
    print("   The matched-circle condition compares L_c to the LSS DIAMETER:")
    print(f"     L_c / (2*chi_rec) = {L_FRAME/diam:.3f}  < 1  ->  the sphere OVERLAPS its image")
    print("     so the matched circles EXIST. The 'outside the horizon' part of the")
    print("     box is irrelevant: the circles form from the LSS we DO see.\n")

    print("=" * 78)
    print("(2) Three regimes -- where does 20.6 Gpc fall?")
    print("=" * 78)
    print(f"   A. L_c < chi_rec        (< {chi:.1f} Gpc): box inside horizon, huge circles.")
    print(f"   B. chi_rec < L_c < 2chi ({chi:.1f}-{diam:.1f} Gpc): box BIGGER than horizon,")
    print("      but the sphere still reaches its image -> circles STILL EXIST.")
    print(f"   C. L_c > 2*chi_rec      (> {diam:.1f} Gpc): box exceeds the LSS diameter,")
    print("      sphere never reaches its image -> NO circles, truly invisible.")
    print()
    print(f"   --> 20.6 Gpc is in regime B ({chi:.1f} < 20.6 < {diam:.1f}). The framework")
    print("       THINKS being bigger than the horizon (regime B vs A) hides it. It does")
    print("       not: only regime C (box > LSS diameter) is invisible, and 20.6 is far")
    print(f"       from it ({diam:.1f} Gpc needed; 20.6 is {(diam-L_FRAME)/diam*100:.0f}% short).\n")

    print("=" * 78)
    print("(3) The circle size and Planck's reach, in this box")
    print("=" * 78)
    cosa = R_I / chi
    alpha = math.degrees(math.acos(cosa))
    # Planck-allowed minimum box edge: R_i > 0.97 chi  ->  L_c > 1.94 chi
    L_allowed = 2 * R_I_BOUND_FRAC * chi
    # detection floor in terms of box edge: alpha > 15 deg  ->  R_i < cos15 * chi
    L_detect_max = 2 * math.cos(math.radians(ALPHA_FLOOR_DEG)) * chi
    print(f"   framework circles:  cos(alpha)=R_i/chi_rec={cosa:.3f} -> alpha = {alpha:.0f} deg")
    print(f"   Planck search floor: alpha_min ~ {ALPHA_FLOOR_DEG:.0f} deg")
    print(f"     -> detectable for any box with edge L_c < {L_detect_max:.1f} Gpc")
    print(f"   Planck cubic bound:  R_i > {R_I_BOUND_FRAC} chi_rec")
    print(f"     -> a cube is ALLOWED only if L_c > {L_allowed:.1f} Gpc")
    print()
    print(f"   framework L_c = {L_FRAME:.1f} Gpc  <  allowed {L_allowed:.1f} Gpc")
    print(f"     EXCLUDED. To escape, the box must grow to > {L_allowed:.1f} Gpc")
    print(f"     -- {(L_allowed/L_FRAME-1)*100:.0f}% bigger -- which is essentially regime C")
    print(f"     ({diam:.1f} Gpc), i.e. so large the topology is unobservable anyway.\n")

    print("=" * 78)
    print("(4) The sensitivity window, swept over box size")
    print("=" * 78)
    print(f"   {'L_c [Gpc]':>10}{'R_i/chi':>9}{'alpha [deg]':>12}{'status':>26}")
    for L in [8, 12, 16, 20.6, 24, 26.9, 27.74, 32]:
        Ri = L / 2
        frac = Ri / chi
        if frac >= 1.0:
            status, a = "NO circles (regime C)", float("nan")
        else:
            a = math.degrees(math.acos(frac))
            if frac > R_I_BOUND_FRAC:
                status = "circles too small to detect"
            else:
                status = "EXCLUDED by Planck" if frac < R_I_BOUND_FRAC else "marginal"
        mark = "  <-- framework" if abs(L - L_FRAME) < 0.01 else ""
        astr = f"{a:.0f}" if not math.isnan(a) else "--"
        print(f"   {L:>10.1f}{frac:>9.3f}{astr:>12}{status:>26}{mark}")
    print()

    print("=" * 78)
    print("VERDICT -- yes, the measurement is significant; maximally so, in fact")
    print("=" * 78)
    print(f"  * 20.6 Gpc is NOT in the test's blind spot. The blind spot is L_c > {diam:.1f}")
    print(f"    Gpc (box > LSS diameter). 20.6 Gpc sits at L_c/2chi = {L_FRAME/diam:.2f} -- deep")
    print("    in the high-sensitivity regime, with 42 deg circles vs a 15 deg floor.")
    print("  * The framework's 'box is 1.5x the horizon, partly hidden' defense uses the")
    print("    wrong yardstick (horizon RADIUS, not LSS DIAMETER). Being bigger than the")
    print("    horizon does not hide a topology from matched circles; only being bigger")
    print("    than the LSS DIAMETER does, and 20.6 Gpc is well below that.")
    print(f"  * Planck allows a cube only if L_c > {L_allowed:.1f} Gpc; 20.6 is {(L_allowed/L_FRAME-1)*100:.0f}% too small.")
    print("    (The T^3/Z2 orbifold adds MORE image pairs, not fewer -- it cannot help.)")
    print("  So what Planck measured is directly, fully significant to the 20.6 Gpc box,")
    print("  and it excludes it. (Unchanged: evolving-a0 needs no topology at all.)")


if __name__ == "__main__":
    main()
