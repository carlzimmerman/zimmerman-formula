#!/usr/bin/env python3
"""
Cassini solar-system quadrupole vs the framework -- is the a0=c2 sqrt(Lambda/32pi) realization exposed?
=======================================================================================================
The constraint (real, recent, and STRENGTHENING):
  * Desmond, Hees, Famaey 2024 (MNRAS 530, 1781; arXiv:2401.04796): classical *modified-gravity* MOND
    (AQUAL / QUMOND) cannot simultaneously fit the SPARC radial-acceleration relation (RAR) and the Cassini
    measurement of the solar-system quadrupole -- 8.7 sigma under fiducial assumptions. The RAR prefers a
    GRADUAL Newton<->MOND transition; the solar-system quadrupole demands a SHARP one.
  * Improved 2026 (arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2 (40% tighter) => the MOND boost to the
    GALACTIC radial acceleration at the solar position is bounded to <= 2% (95%), vs the ~30% the RAR needs.
    Tension 3-15 sigma depending on the Milky Way mass model.

Why this touches THIS framework: the framework's covariant, CMB-safe realization is AeST
(Skordis-Zlosnik), whose quasi-static weak-field limit is QUMOND-like -- i.e. it sits in the very class
Desmond constrains. So the casual "modified inertia evades it" escape is NOT freely available: AeST is
modified GRAVITY. This script grounds the magnitude (an order-of-magnitude check, NOT the full quadrupole
integral, which is in the cited papers) and states the honest disposition. numpy only; reproducible.
"""
import numpy as np

A0_CANON = 1.20e-10        # McGaugh RAR z=0 anchor
A0_FRAME = 9.355e-11       # framework value a0 = (c/2) sqrt(G rho_Lambda) (footing-corrected, low edge)
CASSINI_BOUND = 0.02       # 2026 Cassini Q2 -> <=2% MOND boost at the solar position (95%)


def nu_rar(y):     # McGaugh/RAR interpolation: g_obs = nu(g_N/a0) * g_N
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def nu_simple(y):  # 'simple' nu
    return (1.0 + np.sqrt(1.0 + 4.0 / y)) / 2.0


def main():
    # external field at the Sun from the Galaxy: g_ext ~ V_sun^2 / R_sun
    V, R = 233e3, 8.2 * 3.0857e19
    g_ext = V**2 / R
    print("#" * 92)
    print("# Cassini solar-system quadrupole vs the framework's MOND boost at the solar position")
    print("#" * 92)
    print(f"\n  Milky Way external field at the Sun: g_ext = V^2/R = {g_ext:.3e} m/s^2  (V=233 km/s, R=8.2 kpc)\n")
    print(f"  {'a0 [m/s^2]':<26}{'g_ext/a0':>9}{'boost nu-1 (RAR)':>18}{'boost (simple)':>16}   vs Cassini 2% bound")
    print("  " + "-" * 86)
    for a0, lab in [(A0_CANON, "canonical 1.20e-10"), (A0_FRAME, "framework 0.936e-10")]:
        y = g_ext / a0
        bR, bS = nu_rar(y) - 1, nu_simple(y) - 1
        verdict = "BOTH >> 2% -> in tension" if min(bR, bS) > CASSINI_BOUND else "ok"
        print(f"  {lab:<26}{y:>9.2f}{bR:>17.1%}{bS:>16.1%}   {verdict}")
    print(f"""
  READING (honest, and it goes against the framework's solar-system comfort):
  - The standard interpolating functions that fit the SPARC RAR give a ~28-40% MOND boost at the solar
    position, where the 2026 Cassini quadrupole allows <= 2%. That is the Desmond 8.7 sigma (2024) ->
    3-15 sigma (2026) RAR-vs-quadrupole tension, reproduced at order of magnitude here.
  - The framework's a0 is ~22% LOWER than canonical, pushing the Sun marginally deeper into the Newtonian
    regime (g_ext/a0: 1.79 -> 2.29; boost 36% -> 28%). It helps a little. It does NOT clear a multi-sigma
    tension.
  - The framework is EXPOSED because its covariant/CMB-safe realization (AeST) has a QUMOND-like weak-field
    limit -- it is modified GRAVITY, the class Desmond constrains. The "modified inertia evades it" escape
    belongs to a DIFFERENT realization (Milgrom modified inertia), which the framework does not have a
    covariant version of.
  - NOT a clean kill: AeST carries a free function K(Q) that can in principle screen the solar-system fifth
    force; whether the SAME K(Q) that fits the RAR also satisfies Cassini is the Desmond tension transplanted
    into AeST, and it is UNCOMPUTED. So: a real, shared, strengthening tension the framework inherits -- a
    SECOND framework-relevant exposure alongside the declining a0(z), both pointing at the same missing
    calculation: AeST's quasi-static limit worked out in detail (solar-system quadrupole AND high-z a0).
""")
    print("#" * 92)


if __name__ == "__main__":
    main()
