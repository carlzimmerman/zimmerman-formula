#!/usr/bin/env python3
"""
The E6 skyscraper, floor: the dim-6 proton lifetime, pinned with real numbers.
==============================================================================

The DT-splitting floor (e6_doublet_triplet.py) removed the dim-5 proton decay
that excludes minimal 4D SUSY SU(5). What SURVIVES is the dimension-6 mode:
superheavy gauge-boson (X,Y) exchange driving

        p -> e+ pi0   (and p -> e+ pi0 - like channels).

This is the ONE genuinely forward, falsifiable particle-physics prediction the
construction makes. Here we compute tau(p->e+pi0) with the standard dim-6
formula and honest inputs, instead of quoting "~10^36 yr" as an order of
magnitude. The point of the exercise is to show (a) the central value, and
(b) that it depends on M_X^4 -- so "a Hyper-K target" is true only at the low
end of the GUT-scale range. We do NOT get to pretend this is a sharp number.

Standard rate (Nath & Fileviez Perez, Phys.Rept. 441 (2007) 191; PDG review):

  Gamma(p->e+ pi0) = C_op * (g_GUT^4 / M_X^4) * (m_p / (8 pi f_pi^2))
                          * |alpha_H|^2 * A_R^2 * (1 + D + F)^2

  g_GUT^4 = (4 pi alpha_GUT)^2 ;  C_op = 2 (two chiral operators, same e+ pi0).

Inputs and their provenance are printed. Pure stdlib.
Run:  python reviews/e6_proton_lifetime.py
"""

import math

# ---- physical constants -------------------------------------------------
HBAR_GeV_s = 6.582119569e-25     # GeV * s
SEC_PER_YR = 3.1557e7            # s / yr  (Julian year)

# ---- hadronic / low-energy inputs (lattice + chiral Lagrangian) ----------
M_P   = 0.9383      # GeV   proton mass
F_PI  = 0.1302      # GeV   pion decay constant (PDG, f_pi normalization)
D, F  = 0.804, 0.463  # GeV  baryon chiral axial couplings -> 1+D+F = 2.27
ALPHA_H = 0.0120    # GeV^3 lattice hadronic matrix element <pi0|(ud)u|p>
                    #        (range 0.010-0.014; JLQCD/RBC-UKQCD ~0.012)
A_R   = 2.5         # short+long-distance renormalization (A_SR*A_L ~ 2.0-2.7)
C_OP  = 2.0         # two chiral operators contributing to e+ pi0

# ---- GUT inputs (the SENSITIVE ones) ------------------------------------
ALPHA_GUT_INV = 24.0         # alpha_GUT^-1 at unification (SUSY)
M_X_CENTRAL   = 2.0e16       # GeV  superheavy gauge-boson mass ~ M_GUT

# experimental landmarks (p -> e+ pi0)
SK_LIMIT  = 2.4e34   # yr   Super-Kamiokande 90% CL (2020)
HK_REACH  = 1.0e35   # yr   Hyper-Kamiokande ~10 yr reach (conservative)


def rate_GeV(M_X, alpha_gut_inv=ALPHA_GUT_INV):
    """Dimension-6 p->e+pi0 decay rate in GeV."""
    alpha_gut = 1.0 / alpha_gut_inv
    g4 = (4.0 * math.pi * alpha_gut) ** 2
    pref = M_P / (8.0 * math.pi * F_PI ** 2)
    gamma = (C_OP * (g4 / M_X ** 4) * pref
             * ALPHA_H ** 2 * A_R ** 2 * (1.0 + D + F) ** 2)
    return gamma


def tau_yr(M_X, alpha_gut_inv=ALPHA_GUT_INV):
    g = rate_GeV(M_X, alpha_gut_inv)
    tau_s = HBAR_GeV_s / g
    return tau_s / SEC_PER_YR


def main():
    print("=" * 78)
    print("Dimension-6 proton decay p -> e+ pi0 in the E6 orbifold GUT")
    print("=" * 78)
    print("  Inputs (and where they come from):")
    print(f"    M_P        = {M_P} GeV         (proton mass)")
    print(f"    f_pi       = {F_PI} GeV        (pion decay constant, PDG)")
    print(f"    1+D+F      = {1+D+F:.3f}          (baryon chiral axial couplings)")
    print(f"    alpha_H    = {ALPHA_H} GeV^3   (lattice matrix element, +/-~15%)")
    print(f"    A_R        = {A_R}            (short+long renormalization)")
    print(f"    alpha_GUT^-1 = {ALPHA_GUT_INV}          (SUSY unification)")
    print(f"    M_X        = {M_X_CENTRAL:.1e} GeV    (superheavy X,Y mass ~ M_GUT)")
    print()

    tau0 = tau_yr(M_X_CENTRAL)
    print("=" * 78)
    print("(1) Central prediction")
    print("=" * 78)
    print(f"    Gamma = {rate_GeV(M_X_CENTRAL):.3e} GeV")
    print(f"    tau(p->e+pi0) = {tau0:.3e} yr   (~10^{math.log10(tau0):.1f} yr)")
    print(f"    Super-K limit:   {SK_LIMIT:.1e} yr  -> prediction is "
          f"{tau0/SK_LIMIT:.0f}x ABOVE the current bound (not excluded). ✓")
    print(f"    Hyper-K reach:   ~{HK_REACH:.0e} yr -> "
          f"{'WITHIN reach' if tau0 <= 10*HK_REACH else 'near/above reach'}.")
    print()

    print("=" * 78)
    print("(2) The honest caveat: tau ~ M_X^4, so it is NOT a sharp number")
    print("=" * 78)
    print(f"  {'M_X [GeV]':>12} {'tau [yr]':>12}  {'vs Super-K':>12}  {'vs Hyper-K':>12}")
    for M_X in (1.0e16, 1.5e16, 2.0e16, 2.5e16, 3.0e16):
        t = tau_yr(M_X)
        sk = "EXCLUDED" if t < SK_LIMIT else f"{t/SK_LIMIT:.0f}x above"
        hk = "in reach" if t < 5 * HK_REACH else "above reach"
        print(f"  {M_X:>12.1e} {t:>12.2e}  {sk:>12}  {hk:>12}")
    print()
    print("  A factor of 3 in M_X (1e16 -> 3e16) swings tau by 3^4 = 81x:")
    print(f"    from {tau_yr(1e16):.1e} yr (just above Super-K, squarely a Hyper-K target)")
    print(f"    to   {tau_yr(3e16):.1e} yr (a decade beyond Hyper-K's reach).")
    print()

    print("=" * 78)
    print("VERDICT -- a real, surviving, but SOFT prediction")
    print("=" * 78)
    print("  * The dim-6 mode is the genuine forward prediction left after the")
    print("    orbifold removes dim-5. At the canonical M_X = 2e16, alpha_GUT^-1 = 24")
    print(f"    it gives tau ~ {tau0:.0e} yr -- above Super-K, near Hyper-K's reach.")
    print("  * BUT tau ~ M_X^4: the GUT scale is only known to a factor ~2-3 (2-loop")
    print("    running + KK thresholds, see e6_two_loop_unification.py), and that")
    print("    factor^4 swamps the ~30% hadronic uncertainty. So 'a Hyper-K target'")
    print("    is honest only at the LOW end of the GUT-scale range; at the high end")
    print("    the proton is effectively stable for Hyper-K.")
    print("  * This is INHERITED SUSY-GUT physics -- the same statement holds for any")
    print("    SUSY SO(10)/E6 with M_GUT ~ 2e16. It is not distinctive to this")
    print("    framework. It is, however, a clean falsifiable claim: a confirmed")
    print("    p->e+pi0 at ~10^34-10^35 yr would be a triumph for the whole GUT idea;")
    print("    a null result at Hyper-K only pushes M_X up, it does not kill it.")


if __name__ == "__main__":
    main()
