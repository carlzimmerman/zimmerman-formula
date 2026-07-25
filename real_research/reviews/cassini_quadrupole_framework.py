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


def nu_frame(y):   # *** THE FRAMEWORK'S OWN de Sitter-Unruh interpolation -- USE THIS ONE ***
    # g_obs = sqrt(g_bar^2 + g_bar a0)  <=>  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0.
    # Equivalent to the exact excess identity g_obs^2 - g_bar^2 = a0 g_bar.
    return np.sqrt(1.0 + 1.0 / y)


# --- REFERENCE ONLY: McGaugh's fitting functions. NOT the framework's kernel. ------------------
# RULE-1 FIX 2026-07-25 (flagged F1 by AUDIT_rule2_foreign_a0_bounds_2026.py): this script
# previously reported the solar-position boost using ONLY these two McGaugh functions, giving
# 28.2% / 32.8%, and those numbers propagated into BOUNDS.md sec 3 and the Door-A scoreboard row.
# The framework's OWN nu gives 19.8% (canonical a0). The Q2 wall SURVIVES the correction -- only
# the number moves -- but the framework must be judged on its own kernel, never McGaugh's.
def nu_rar(y):     # McGaugh/RAR fitting function -- REFERENCE VALUE ONLY
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def nu_simple(y):  # 'simple' nu -- REFERENCE VALUE ONLY
    return (1.0 + np.sqrt(1.0 + 4.0 / y)) / 2.0


def main():
    # external field at the Sun from the Galaxy: g_ext ~ V_sun^2 / R_sun
    V, R = 233e3, 8.2 * 3.0857e19
    g_ext = V**2 / R
    print("#" * 92)
    print("# Cassini solar-system quadrupole vs the framework's MOND boost at the solar position")
    print("#" * 92)
    print(f"\n  Milky Way external field at the Sun: g_ext = V^2/R = {g_ext:.3e} m/s^2  (V=233 km/s, R=8.2 kpc)\n")
    print(f"  {'a0 [m/s^2]':<26}{'g_ext/a0':>9}{'FRAMEWORK nu-1':>16}{'(McG RAR)':>11}{'(McG simple)':>13}"
          f"   vs Cassini 2% bound")
    print("  " + "-" * 92)
    for a0, lab in [(A0_FRAME, "FRAMEWORK 0.936e-10"), (A0_CANON, "McGaugh fit 1.20e-10")]:
        y = g_ext / a0
        bF, bR, bS = nu_frame(y) - 1, nu_rar(y) - 1, nu_simple(y) - 1
        verdict = "over the 2% bound -> tension" if bF > CASSINI_BOUND else "ok"
        print(f"  {lab:<26}{y:>9.2f}{bF:>15.1%}{bR:>11.1%}{bS:>13.1%}   {verdict}")
    yF = g_ext / A0_FRAME
    print(f"\n  HEADLINE, on the framework's OWN kernel and OWN a0: boost = {nu_frame(yF)-1:.1%} "
          f"(NOT the 28-33% the McGaugh fitting functions give).")
    print(f"  Still {(nu_frame(yF)-1)/CASSINI_BOUND:.1f}x over the 2% Cassini allowance, so the wall stands "
          f"-- but on the right number.")
    print(f"""
  READING (honest, and it goes against the framework's solar-system comfort):
  - The standard interpolating functions that fit the SPARC RAR give a ~28-40% MOND boost at the solar
    position, where the 2026 Cassini quadrupole allows <= 2%. That is the Desmond 8.7 sigma (2024) ->
    3-15 sigma (2026) RAR-vs-quadrupole tension, reproduced at order of magnitude here.
  - The framework's a0 is ~22% LOWER than canonical, pushing the Sun marginally deeper into the Newtonian
    regime (g_ext/a0: 1.79 -> 2.29; on the FRAMEWORK's own nu the boost is 19.8%, not the 28-33%
    the McGaugh fits give -- see the RULE-1 FIX note above). It helps a little. It does NOT clear a multi-sigma
    tension.
  - The framework's MG limb is EXPOSED: its covariant/CMB-safe realization (AeST) has a QUMOND-like
    weak-field limit -- modified GRAVITY, the class Desmond constrains.
  - *** UPDATED 2026-07-25: the "modified inertia evades it" escape is NO LONGER unavailable. ***
    The covariant MI action IS now written (MI_FIELD_THEORY_RESULTS_2026), and the multipole-grading
    result (mi_q1_efe_order_count_2026.py, mi_quasistatic_efe_multipoles_2026.py) DERIVES that the
    l=2 quadrupole enters only at eps^2, eps = theta g_ext/g_bar = 4.7e-6 at Saturn, so Q2(MI) is
    ~6e6x UNDER the Park+2026 bound with NO gate applied. The 3-15 sigma tension therefore does NOT
    transfer to the MI reading -- it stays on the MG/AeST limb. NOTE the honest scope: prior art is
    thin here (Milgrom 2009 MNRAS 399:474 already asserted no inner-SS EFE for the Milgrom-1999
    de Sitter-Unruh toy theory; what is new is the ORDER COUNTING and the both-directions correction
    that the l=0 MONOPOLE is UNSUPPRESSED and needs the gate).
  - NOT a clean kill: AeST carries a free function K(Q) that can in principle screen the solar-system fifth
    force; whether the SAME K(Q) that fits the RAR also satisfies Cassini is the Desmond tension transplanted
    into AeST, and it is UNCOMPUTED. So: a real, shared, strengthening tension the framework inherits -- a
    SECOND framework-relevant exposure alongside the declining a0(z), both pointing at the same missing
    calculation: AeST's quasi-static limit worked out in detail (solar-system quadrupole AND high-z a0).
""")
    print("#" * 92)


if __name__ == "__main__":
    main()
