#!/usr/bin/env python3
"""
More first-principles derivations from a0 = (c/2)sqrt(G rho) = cH/Z, evolving as E(z).
=====================================================================================

Each result is derived honestly and labelled:
  [DERIVED]  follows by algebra/calculus from the premise + standard deep-MOND.
  [FOLLOWS]  a clean consequence, weaker than a theorem.
  [LIMIT]    an honest negative -- something the premise does NOT give.

New here: (D2) the a0-SLOPE measures the cosmic acceleration q(z) -- not just H(z) but
dark energy, from galaxy dynamics. Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, G, Msun, pc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e16, 3.0857e22
OM, OL = 0.315, 0.685
Z = 2 * np.sqrt(8 * np.pi / 3)
H0 = 67.4e3 / Mpc
A0 = 1.2e-10
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
dlnE_dz = lambda z: 0.5 * (3 * OM * (1 + z) ** 2) / E(z) ** 2     # d ln E / dz


def d1_phantom_density():
    print("=" * 80); print("[D1, DERIVED] the phantom dark-matter density MOND mimics, and its evolution")
    print("=" * 80)
    print("  Deep MOND, point mass M_b:  g = sqrt(g_N a0) = sqrt(G M_b a0)/r.")
    print("  Newtonian dynamical mass:   M_dyn(r) = g r^2/G = r sqrt(M_b a0/G)  (rises linearly: a halo).")
    print("  Phantom density:  rho_ph = (1/4pi r^2) dM_dyn/dr = sqrt(M_b a0/G)/(4pi r^2).")
    print("   * shape:  rho_ph ~ 1/r^2  -- the isothermal 'dark halo', DERIVED, no dark matter.")
    print("   * scale:  rho_ph ~ sqrt(a0)  ->  rho_ph(z)/rho_ph(0) = sqrt(E(z)):")
    print(f"        {'z':>4}{'sqrt(E)':>9}  (apparent-DM density vs today, fixed baryons)")
    for z in (0, 2, 6, 10):
        print(f"        {z:>4}{np.sqrt(E(z)):>9.2f}")
    print("   => high-z galaxies carry sqrt(E)-denser phantom halos: x3.2 by z=6. [DERIVED]\n")


def d2_cosmic_acceleration():
    print("=" * 80); print("[D2, DERIVED] the a0 SLOPE measures the cosmic acceleration q(z) -- dark energy")
    print("=" * 80)
    print("  H(z) = Z a0(z)/c, so ln H = const + ln a0. The deceleration parameter is")
    print("    q(z) = -1 - Hdot/H^2 = -1 + (1+z) d ln H/dz = -1 + (1+z) d ln a0/dz.")
    print("  So a0(z) gives H(z); the SLOPE d ln a0/dz gives q(z) -- whether the universe")
    print("  accelerates -- straight from galaxy dynamics. For the premise (a0 ~ E(z)):")
    print(f"     {'z':>5}{'d ln a0/dz':>12}{'q(z)':>9}{'accelerating?':>15}")
    for z in (0.0, 0.5, 1.0):
        q = -1 + (1 + z) * dlnE_dz(z)
        print(f"     {z:>5.1f}{dlnE_dz(z):>12.3f}{q:>9.3f}{'yes' if q<0 else 'no':>15}")
    q0 = -1 + dlnE_dz(0)
    print(f"  q0 = {q0:.3f}  (LCDM: Om/2 - OL = {OM/2-OL:.3f}). A measured d ln a0/dz|0 ~ 0.47 at z=0")
    print("  would confirm cosmic ACCELERATION (q0<0) -- i.e. dark energy -- from rotation curves.")
    print("  This is the deep content of a0-cosmography: a0's value gives H, its slope gives q. [DERIVED]\n")


def d3_surface_density():
    print("=" * 80); print("[D3, DERIVED] the critical (Freeman) surface density and its evolution")
    print("=" * 80)
    Sig = A0 / (2 * np.pi * G)                       # kg/m^2
    Sig_Msun_pc2 = Sig * pc ** 2 / Msun
    print(f"  MOND critical surface density: Sigma_c = a0/(2 pi G) = {Sig:.3f} kg/m^2 = "
          f"{Sig_Msun_pc2:.0f} Msun/pc^2")
    print("  (this is Freeman's law -- the HSB/LSB disk-stability boundary, DERIVED from a0).")
    print(f"  It evolves as a0(z): Sigma_c(z) = a0(z)/(2 pi G) ~ E(z):")
    print(f"     {'z':>5}{'Sigma_c [Msun/pc^2]':>20}")
    for z in (0, 2, 6):
        print(f"     {z:>5}{Sig_Msun_pc2*E(z):>20.0f}")
    print("   => the disk-stability ceiling RISES with z: high-z disks can be ~10x denser by z=6")
    print("      before going unstable. A clean, testable structural prediction. [DERIVED]\n")


def d4_minimum_acceleration():
    print("=" * 80); print("[D4, FOLLOWS] a0 floors at the de Sitter acceleration -- a cosmic minimum")
    print("=" * 80)
    a0_floor = A0 * np.sqrt(OL)
    HL = H0 * np.sqrt(OL)
    print(f"  Future (matter dilutes): a0 -> a0(0)sqrt(Omega_L) = {a0_floor:.2e} m/s^2 = c H_Lambda/Z,")
    print(f"  H_Lambda = H0 sqrt(Omega_L). a0 never drops below this de Sitter floor.")
    print(f"  So the MOND scale is bounded:  a0 in [{a0_floor:.2e}, infinity), floor set by Lambda.")
    print("  Interpretation: ~ a cosmic minimum acceleration -- the smallest 'meaningful' g is set")
    print("  by the cosmological constant, c^2 sqrt(Lambda/3)/Z. [FOLLOWS]\n")


def d5_whynow():
    print("=" * 80); print("[D5, DERIVED] the premise DISSOLVES the 'why now' coincidence")
    print("=" * 80)
    print("  If a0 were a CONSTANT, then a0 = cH(z)/Z holds at exactly ONE epoch (cH falls with")
    print("  time, a0 does not). That we live at that epoch is a 'why now' coincidence. Quantify")
    print("  the mismatch a CONSTANT-a0 universe would show, |cH(z)/Z - a0(0)|/a0(0):")
    print(f"     {'z':>5}{'constant-a0 mismatch':>22}{'premise (a0~E) mismatch':>26}")
    for z in (0.0, 1.0, 3.0):
        const_mis = abs(c * H0 * E(z) / Z / 1 - A0) / A0     # cH(z)/Z vs fixed a0(0)
        # express cH(z)/Z in units of A0: cH0/Z = A0 (today), so cH(z)/Z = A0 E(z)
        const_mis = abs(E(z) - 1.0)
        print(f"     {z:>5.1f}{const_mis*100:>20.0f}%{0.0:>24.0f}%")
    print("  The premise (a0 tracks cH) makes a0 = cH/Z hold at EVERY epoch -- mismatch 0 always.")
    print("  The coincidence is removed by construction: 'a0 ~ cH' is a law, not a now-only accident.")
    print("  [DERIVED -- this is the conceptual motivation, made quantitative]\n")


def d6_honest_limit():
    print("=" * 80); print("[D6, LIMIT] what the premise does NOT give: the cosmic dark-matter budget")
    print("=" * 80)
    print("  The phantom density (D1) is LOCAL -- it lives in galaxies and integrates to far less")
    print("  than the cosmic Omega_DM ~ 0.265 the CMB requires. MOND's a0/Y-sector does NOT supply")
    print("  the smooth cosmological dark matter. That is exactly why the relativistic completion")
    print("  (AeST) needs a SEPARATE temporal K(Q) 'dust' mode for cosmology (Paper I/II). So the")
    print("  'dark matter' is TWO things here -- galaxy phantom (Y-sector) + cosmic dust (Q-sector)")
    print("  -- not one. Stating this is what keeps the unification claim (D3 of the consequences)")
    print("  honest: a0 ties the SCALES, it does not collapse DM and DE into a single substance.\n")


def main():
    d1_phantom_density(); d2_cosmic_acceleration(); d3_surface_density()
    d4_minimum_acceleration(); d5_whynow(); d6_honest_limit()
    print("=" * 80); print("LEDGER")
    print("=" * 80)
    print("  DERIVED:  phantom halo rho~1/r^2 & ~sqrt(E) (D1); q(z) from a0's slope, cosmic")
    print("            acceleration from galaxies (D2); Freeman Sigma_c ~ E(z) (D3); why-now")
    print("            dissolved (D5).")
    print("  FOLLOWS:  a0 floors at the de Sitter value, a cosmic minimum acceleration (D4).")
    print("  LIMIT:    the cosmic DM budget is NOT from a0 -- it needs the separate Q-sector;")
    print("            'dark matter' here is two things, not one (D6).")
    print("  The strongest new result is D2: a0-cosmography measures not just H0 but q0 (dark")
    print("  energy) from rotation curves -- a0 gives H, its slope gives the acceleration.")
    print("=" * 80)


if __name__ == "__main__":
    main()
