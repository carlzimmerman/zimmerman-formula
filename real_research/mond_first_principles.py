#!/usr/bin/env python3
"""
From first principles: derive the web's dynamical edges from the ONE MOND field equation.
=========================================================================================

The web's edges were ENUMERATED (REAL_WEB.py) and FILTERED (web_search_relations.py). This
block does the harder thing Carl asked for -- DERIVE them, block by block, from the single
MOND field equation with a0 = cH(z)/Z. Deriving instead of asserting earns two things:

  (1) the edges become theorems off one equation, not separate claims;
  (2) it catches an error -- the phantom-density scaling I asserted as ~E(z) is, when
      actually derived, ~sqrt(E(z)). The derivation CORRECTS the enumeration (Part 4).

THE ONE EQUATION (AQUAL, Bekenstein-Milgrom 1984):
    div[ mu(|grad phi|/a0) grad phi ] = 4 pi G rho_b
with the deep-MOND limit mu(x) -> x for x = g/a0 << 1. Everything below is that limit,
plus a0(z) = a0(0) E(z) from the premise. Each result is tagged [DERIVED] or, where a
choice of interpolating function enters, [DERIVED up to the mu-function].

Read-only, published numbers only. Run:  python real_research/mond_first_principles.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
KPC = 3.0857e19
MSUN = 1.989e30
PC = 3.0857e16

Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL = 0.315, 0.685
A0 = 1.13e-10
V_LSR = 233e3          # m/s, Solar circular speed (GRAVITY/Reid-Brunthaler)
R0 = 8.18 * KPC        # m, Galactocentric radius (GRAVITY 2019)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


# ====================================================================================
def part1_field_equation():
    print("#" * 84)
    print("# PART 1 -- the one field equation and its deep-MOND limit")
    print("#" * 84)
    print("   AQUAL:   div[ mu(|grad phi|/a0) grad phi ] = 4 pi G rho_b")
    print("   spherical, enclosed baryonic mass M(r):   mu(g/a0) g = g_N = G M / r^2")
    print("   deep-MOND (g << a0):  mu(x) -> x  =>  (g/a0) g = g_N  =>  g = sqrt(g_N a0).")
    print("   THIS single limit -- g = sqrt(g_N a0) -- generates every edge below.\n")


# ====================================================================================
def part2_btfr():
    print("#" * 84)
    print("# PART 2 [DERIVED] Baryonic Tully-Fisher: v^4 = G M a0  (edge E8/A1)")
    print("#" * 84)
    print("   circular orbit: g = v^2/r.  deep-MOND: g = sqrt(g_N a0) = sqrt(GM a0)/r.")
    print("   set equal:  v^2/r = sqrt(GM a0)/r  =>  v^2 = sqrt(GM a0)  =>  v^4 = G M a0.")
    print("   => slope d log M / d log v = 4 EXACTLY, independent of a0 (hence of z);")
    print("      the a0(z) enters ONLY as the zero-point, M = v^4/(G a0) ~ 1/E(z).")
    v = 200e3
    print(f"   {'z':>5}{'M(v=200) [Msun]':>20}{'~ 1/E(z)':>12}")
    for z in (0, 1, 2):
        M = v ** 4 / (G * A0 * E(z)) / MSUN
        print(f"   {z:>5}{M:>20.2e}{1/E(z):>12.3f}")
    print("   [DERIVED] slope 4 is forced; LCDM does not force it. A clean high-z separator.\n")


# ====================================================================================
def part3_faber_jackson():
    print("#" * 84)
    print("# PART 3 [DERIVED] Faber-Jackson for dispersions: sigma^4 = (4/9) G M a0  (A4)")
    print("#" * 84)
    print("   Milgrom (1984) deep-MOND isothermal sphere integrates the same equation to")
    print("   sigma^4 = (4/9) G M a0.  So at fixed baryonic M:  sigma ~ (M a0)^1/4 ~ E(z)^1/4.")
    print("   This is the PRESSURE-supported twin of the BTFR -- and it is the channel")
    print("   de Graaff's high-z masses come from (velocity dispersion, not rotation):")
    print(f"   {'z':>5}{'sigma/sigma0 = E^1/4':>22}{'Mdyn/Mbar boost ~ sqrt(E)':>28}")
    for z in (2, 4, 6):
        print(f"   {z:>5}{E(z) ** 0.25:>22.3f}{math.sqrt(E(z)):>28.2f}")
    print("   [DERIVED] de Graaff's z~6 'too-much-dynamical-mass' = this zero-point shift.\n")


# ====================================================================================
def part4_phantom():
    print("#" * 84)
    print("# PART 4 [DERIVED + CORRECTION] phantom dark-matter density ~ sqrt(a0), NOT a0")
    print("#" * 84)
    print("   a LCDM observer ascribes the MOND boost to a fictitious 'phantom' density")
    print("   rho_ph = (1/4 pi G) div(g_MOND - g_N).  Point mass, deep-MOND:")
    print("     g_MOND = sqrt(GM a0)/r   (falls as 1/r)")
    print("     div(A/r) in spherical = A/r^2,  A = sqrt(GM a0)")
    print("     => rho_ph(r) = sqrt(GM a0)/(4 pi G r^2) = sqrt(M a0/G)/(4 pi r^2)")
    print("   So rho_ph ~ sqrt(a0) ~ SQRT(E(z)) at fixed M, r.")
    M, r = 1e11 * MSUN, 20 * KPC
    print(f"   {'z':>5}{'rho_ph(20kpc) [Msun/pc^3]':>27}{'ratio = sqrt(E(z))':>20}")
    for z in (0, 1, 2, 6):
        rho = math.sqrt(M * A0 * E(z) / G) / (4 * math.pi * r ** 2) * PC ** 3 / MSUN
        print(f"   {z:>5}{rho:>27.2e}{math.sqrt(E(z)):>20.3f}")
    print()
    print("   *** CORRECTS web_search_relations.py A3, which said rho_ph ~ E(z). ***")
    print("   The error: conflating the SURFACE density Sigma_M = a0/G ~ a0 (first power,")
    print("   correct in C2) with the VOLUME phantom density ~ sqrt(a0). Deriving it -- rather")
    print("   than asserting it -- gives sqrt(E(z)). The fixed value matches the M_dyn boost")
    print("   sqrt(E) (Part 3): the 'phantom halo' and the 'extra dynamical mass' are one thing.\n")


# ====================================================================================
def part5_efe():
    print("#" * 84)
    print("# PART 5 [DERIVED regime] the External Field Effect pins the wide-binary test (B2)")
    print("#" * 84)
    print("   MOND is non-linear: a subsystem feels its environment's field g_ext. The Solar")
    print("   neighborhood's external field, from first principles (circular equilibrium):")
    gext = V_LSR ** 2 / R0
    y = gext / A0
    print(f"     g_ext = V_LSR^2 / R0 = ({V_LSR/1e3:.0f}e3)^2 / (8.18 kpc) = {gext:.2e} m/s^2")
    print(f"     g_ext / a0 = {y:.2f}   => the Solar neighborhood is TRANS-EFE (g_ext > a0),")
    print("     NOT deep-MOND. Wide binaries are therefore PARTIALLY Newtonized by the Galaxy.")
    print()
    print("   Leading-order internal boost G_eff/G ~ 1/mu(g_ext/a0), v-boost = sqrt(G_eff/G)-1:")
    for name, mu in [("simple   mu=x/(1+x)", y / (1 + y)),
                     ("standard mu=x/sqrt(1+x^2)", y / math.sqrt(1 + y * y))]:
        Geff = 1 / mu
        print(f"     {name:28} mu={mu:.3f}  G_eff/G={Geff:.3f}  v-boost = {(math.sqrt(Geff)-1)*100:+.0f}%")
    print("   => predicted boost spans ~6% to ~24% for the SAME g_ext/a0=1.9, purely from the")
    print("   choice of interpolating function. THAT sensitivity is why the data is contested:")
    print("   Chae (2023) reports a MOND-like signal; Banik et al. / Pittordis-Sutherland find")
    print("   Newtonian. The test sits exactly on the function-sensitive knee. [caveat: the")
    print("   exact EFE adds an O(1) anisotropy term; full QUMOND needed for a sharp number.]")
    print()
    print("   z-evolution [DERIVED]: at fixed external field, g_ext/a0 ~ 1/E(z), so the EFE")
    print(f"   suppression WEAKENS with z -- at z=1 the same field is only {y/E(1):.2f} a0. High-z")
    print("   analogues of EFE-suppressed systems are more deeply in the MOND regime.\n")


# ====================================================================================
def verdict():
    print("#" * 84)
    print("# VERDICT")
    print("#" * 84)
    print("  Four web edges are now DERIVED from the one field equation, not asserted:")
    print("   * BTFR v^4 = G M a0 (slope 4 forced, intercept ~1/E(z));")
    print("   * Faber-Jackson sigma^4 = (4/9) G M a0 (the de Graaff dispersion channel);")
    print("   * phantom density rho_ph ~ sqrt(a0) ~ sqrt(E(z))  -- which CORRECTS the earlier")
    print("     asserted ~E(z); deriving beat asserting;")
    print("   * the EFE: g_ext = 1.9 a0 in the Solar neighborhood, so the wide-binary boost")
    print("     is 6-24% (mu-dependent) -- a first-principles account of why B2 is contested.")
    print()
    print("  Block by block, the web's dynamical edges reduce to one limit, g = sqrt(g_N a0),")
    print("  plus a0(z)=a0(0)E(z). The boundary is unchanged: this is the NON-relativistic")
    print("  theory; lensing/CMB still need a covariant completion (not derived here).")


def main():
    part1_field_equation()
    part2_btfr()
    part3_faber_jackson()
    part4_phantom()
    part5_efe()
    verdict()


if __name__ == "__main__":
    main()
