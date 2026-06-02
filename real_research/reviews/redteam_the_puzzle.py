#!/usr/bin/env python3
"""
RED-TEAM the whole surviving theory -- attack every piece, report what breaks.
==============================================================================

Piece 3 (the data) was already cut from 5sigma to a ~2sigma hint
(stresstest_piece3_evolution.py). This goes after the rest of THE_SURVIVING_THEORY.md.
Two attacks are computable and are computed here, not opined:

  ATTACK on Piece 7 (CMB linear-safety): the order-counting kept only ONE term. Does
     delta-Y really vanish at linear order when the AETHER is also perturbed (delta A)?
  ATTACK on Piece 8 (the 'decisive' JWST cascade): are the actual high-z targets even in
     the deep-MOND regime where the a0(z) predictions live -- or are they Newtonian?

The rest (Pieces 1,2,4,5) get honest conceptual attacks with their supporting numbers.
Discipline: I am trying to BREAK each piece. Run: python <thisfile>  (needs sympy, numpy)
"""
import numpy as np
import sympy as sp

# ============================================================================
def attack_1_premise():
    print("=" * 80); print("ATTACK Piece 1 -- the premise a0=cH/Z is a re-dressed coincidence")
    print("=" * 80)
    c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
    Z = 2 * np.sqrt(8 * np.pi / 3)
    print("   a0 ~ cH0 is Milgrom's 40-year-old coincidence; Z=5.79 just replaces his 2pi=6.28")
    print("   with a 9%-different O(1) number. The match is H0-dependent and only ~few %:")
    for H0 in (67.4, 70.0, 73.0):
        a0 = c * (H0 * 1e3 / Mpc) / Z
        print(f"     H0={H0}: cH0/Z = {a0*1e10:.2f}e-10  vs obs 1.20  ({(a0/1.2e-10-1)*100:+.0f}%)")
    print("   And Z is NOT unique: 29/5=5.800 fits the data value (5.795) BETTER than")
    print("   sqrt(32pi/3)=5.789 (coefficient_uniqueness_test.py). One number, one free")
    print("   coefficient -> ~0 bits, same trap as the dead alpha numerology. [WEAK by construction]\n")


def attack_2_evolution():
    print("=" * 80); print("ATTACK Piece 2 -- 'coefficient-free' is not 'assumption-free'")
    print("=" * 80)
    print("   a0(z)=a0(0)E(z) is forced ONLY if a0 tracks sqrt(rho_TOTAL). The same premise")
    print("   read as a0~sqrt(Lambda) (de Sitter/horizon -- the MORE natural geometric origin)")
    print("   gives a0=const, NO evolution. So the 'one falsifiable prediction' smuggles in the")
    print("   choice of WHICH density. The evolution is a prediction of a chosen model, not a")
    print("   theorem from Piece 1. [the fork is real; Piece 2 overstates 'forced']\n")


def attack_4_action():
    print("=" * 80); print("ATTACK Piece 4 -- 'field-equation output' overstates a hand-put coupling")
    print("=" * 80)
    print("   a0 -> c*theta/(3Z) is INSERTED, not derived. Nothing selects theta over sqrt(Lambda)")
    print("   except that theta=3H gives the answer we wanted -- reverse-engineering at the level")
    print("   of a coupling. It PARAMETERIZES the finding; it does not explain it. Z stays a free")
    print("   constant, so the action adds no predictive content beyond the (already-claimed)")
    print("   evolution. [honest, but 'output' should read 'parameterization']\n")


def attack_5_screening():
    print("=" * 80); print("ATTACK Piece 5 -- anti-screening is a TEST-FIELD result, not self-consistent")
    print("=" * 80)
    print("   theta~3H(z) in a galaxy was computed with the aether PRESCRIBED (cosmic-aligned,")
    print("   div B ~ 0 assumed). The aether EOM was NOT solved in the bound system, and the")
    print("   a0(theta) coupling back-reacts. 'div B ~ 0 for a virialized system' is an")
    print("   ASSUMPTION. If the aether is dragged, theta_local can deviate. [plausible, not proven]\n")


# ============================================================================
def attack_7_cmb_linear():
    print("=" * 80); print("ATTACK Piece 7 -- does delta-Y REALLY vanish with the aether perturbed?")
    print("=" * 80)
    print("   The order-counting kept only 2*qbar*grad(phibar)*grad(dphi). But delta-Y also gets")
    print("   delta(q^{mu nu})*grad(phibar)*grad(phibar). If delta q^{00} != 0, a0 LEAKS to linear")
    print("   order and CMB-safety FAILS. Compute delta q^{00} with the constrained aether:")
    eps, Psi = sp.symbols('epsilon Psi', real=True)
    # g^{00} = -1/(1+2 eps Psi);  A^0 from unit constraint g_{00}(A^0)^2=-1
    g00_inv = -1 / (1 + 2 * eps * Psi)
    A0 = sp.sqrt(-1 / (-(1 + 2 * eps * Psi)))            # = 1/sqrt(1+2eps Psi)
    q00 = g00_inv + A0 * A0                              # q^{00}=g^{00}+A^0 A^0
    q00_lin = sp.series(q00, eps, 0, 2).removeO()
    dq00 = sp.simplify(sp.diff(q00_lin, eps).subs(eps, 0))
    print(f"     delta g^00 = {sp.series(g00_inv,eps,0,2).removeO()}  (= +2Psi at O(eps))")
    print(f"     A^0 = 1 - eps Psi (unit constraint) -> delta(A^0 A^0) = -2Psi")
    print(f"     delta q^00 = {dq00}")
    if dq00 == 0:
        print("   RESULT: delta q^00 = 0 EXACTLY -- the metric and the unit-timelike constraint")
        print("   cancel. So delta-Y = delta q^00 (phibar')^2 = 0: a0 stays O(dphi^3) at linear")
        print("   order even with the aether perturbed. [Piece 7 SURVIVES -- and more rigorously")
        print("   than the original derivation, which silently dropped this term.]\n")
    else:
        print(f"   RESULT: delta q^00 != 0 -> a0 LEAKS to linear order. CMB-safety BREAKS.\n")
    return dq00


# ============================================================================
def attack_8_regime():
    print("=" * 80); print("ATTACK Piece 8 -- are the JWST targets even in the deep-MOND regime?")
    print("=" * 80)
    c, G, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
    Z = 2 * np.sqrt(8 * np.pi / 3); H0 = 67.4e3 / Mpc
    OM, OL = 0.315, 0.685
    E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
    a0z = lambda z: (c * H0 / Z) * E(z)
    print("   The cascade (M_dyn/M*~sqrt(E), v~E^1/4, ...) are DEEP-MOND scalings -- they need")
    print("   g_bar < a0(z). But high-z galaxies are COMPACT (high g_bar). Compute g/a0 at z=6:")
    print(f"   a0(z=6) = {a0z(6):.2e} m/s^2")
    print(f"     {'M* [Msun]':>10}{'R [kpc]':>9}{'g_bar':>12}{'g/a0(z6)':>11}{'regime':>14}")
    for Mstar, Rkpc in [(1e9, 1.0), (1e9, 0.5), (1e10, 1.0), (1e10, 0.5), (3e10, 0.5)]:
        M = Mstar * Msun; R = Rkpc * kpc
        g = G * M / R**2
        ratio = g / a0z(6)
        reg = "deep-MOND" if ratio < 0.3 else ("Newtonian" if ratio > 3 else "TRANSITION")
        print(f"     {Mstar:>10.0e}{Rkpc:>9.1f}{g:>12.2e}{ratio:>11.2f}{reg:>14}")
    print("   At fixed mass, sizes shrink ~ (1+z)^-1 so g~(1+z)^2, while a0(z)~(1+z)^1.5:")
    print("   => g/a0 ~ (1+z)^0.5 RISES with z. High-z galaxies trend NEWTONIAN, not deeper-MOND.")
    print("   The a0(z) boosts are SUPPRESSED for the compact targets the prediction is sold on.\n")
    print("   And the headline 'support' (de Graaff M_dyn/M*~40) does NOT survive the numbers:")
    print("   the MOND boost is M_dyn/M_bar = sqrt(a0(z)/g_bar). To reach 40 needs g_bar tiny:")
    g_need = a0z(6) / 40**2
    M = 1e9 * Msun
    R_need = np.sqrt(G * M / g_need) / kpc
    print(f"     to get boost=40 at z=6: g_bar={g_need:.1e} -> for M*=1e9, R={R_need:.0f} kpc (!!)")
    for Mstar, Rkpc in [(1e9, 0.5), (1e9, 1.0)]:
        M = Mstar * Msun; R = Rkpc * kpc
        boost = np.sqrt(a0z(6) / (G * M / R**2))
        print(f"     realistic JADES (M*={Mstar:.0e}, R={Rkpc}kpc): MOND boost = {boost:.1f}  (NOT 40)")
    print("   => compact JADES galaxies get a MOND boost of ~1.5-3, an ORDER OF MAGNITUDE short")
    print("   of 40. de Graaff's ratios, if real, are EVIDENCE AGAINST the evolving-a0 MOND")
    print("   explanation, not for it. Citing them as support is backwards. [Piece 8 WEAKENED]\n")


def verdict():
    print("=" * 80); print("RED-TEAM VERDICT -- what survived, what broke")
    print("=" * 80)
    print("  SURVIVES:")
    print("   * Piece 7 (linear CMB-safety): delta q^00 = 0 exactly; a0 stays O(dphi^3) even")
    print("     with the aether perturbed. The strongest piece -- and now more rigorous.")
    print("  WEAKENED / BREAKS:")
    print("   * Piece 1: a re-dressed coincidence + a non-unique chosen coefficient (~0 bits).")
    print("   * Piece 2: 'coefficient-free' but requires the sqrt(rho_total) choice (a model).")
    print("   * Piece 4: the theta-coupling is inserted, not derived ('output' overstates).")
    print("   * Piece 5: anti-screening is a test-field result; div B ~ 0 is assumed.")
    print("   * Piece 8: the COMPACT high-z targets trend NEWTONIAN (g/a0 ~ (1+z)^0.5), so the")
    print("     a0(z) boosts are suppressed where the prediction is sold; and de Graaff's")
    print("     M_dyn/M*~40 is ~10x beyond any MOND boost -- it cuts AGAINST the framework.")
    print("  NET: the THEORY (action, CMB-safety) is internally sound; the EMPIRICAL case is")
    print("  weak on every leg (Piece 3 ~2sigma, Piece 8 regime-suppressed + mis-cited). The")
    print("  honest standing: a coherent, falsifiable model with NO current positive evidence")
    print("  above ~2sigma, and one headline 'support' that actually points the other way.")
    print("=" * 80)


def main():
    attack_1_premise(); attack_2_evolution(); attack_4_action(); attack_5_screening()
    attack_7_cmb_linear(); attack_8_regime(); verdict()


if __name__ == "__main__":
    main()
