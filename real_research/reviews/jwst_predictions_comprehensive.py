#!/usr/bin/env python3
"""
Comprehensive JWST predictions of the evolving-a0 framework -- calculated properly.
==================================================================================
Premise: a0(z) = a0(0) E(z),  E(z)=sqrt(Om(1+z)^3+OL).  Every prediction below is a
consequence, computed from first principles, with the ACCELERATION-REGIME check done
explicitly (the boosts are DEEP-MOND predictions; compact galaxies are Newtonian and
show NO boost). Honest labels:
  [DERIVED]    forced by deep-MOND algebra
  [DEGENERATE] real but LCDM also produces it (apparent a0 rises with z)
  [DISTINCTIVE] DM-forbidden / not faked by halo evolution
  [REGIME]     only applies where g_bar < a0(z) (extended, low-surface-brightness)
Run: python jwst_predictions_comprehensive.py   (numpy)
"""
import numpy as np

c, G, Msun, pc, kpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
OM, OL = 0.315, 0.685
A0 = 1.2e-10
E  = lambda z: np.sqrt(OM*(1+z)**3 + OL)
nu = lambda x: 0.5*(1.0+np.sqrt(1.0+4.0/x))           # boost M_dyn/M_bar = nu(g_bar/a0)
ZL = [0, 1, 2, 4, 6, 8, 10.6, 14]                     # redshift ladder (10.6 = GN-z11)


def part1_ladder():
    print("="*86)
    print("PART 1 -- the redshift ladder: a0(z) and the four scaling boosts (DEEP-MOND)")
    print("="*86)
    print(f"  {'z':>5}{'E(z)':>8}{'a0(z)[m/s^2]':>15}{'M_dyn/M_b xsqrtE':>18}"
          f"{'v x E^1/4':>11}{'Sig_c xE':>10}{'EFE x1/E':>10}")
    for z in ZL:
        Ez = E(z)
        print(f"  {z:>5}{Ez:>8.2f}{A0*Ez:>15.2e}{np.sqrt(Ez):>18.2f}"
              f"{Ez**0.25:>11.2f}{Ez:>10.1f}{1/Ez:>10.3f}")
    print("""
  COLUMNS (all = consequence of a0(z)=a0(0)E(z)):
   * M_dyn/M_bar ~ sqrt(E)   apparent 'dark matter' of a galaxy rises [DERIVED, DEGENERATE]
   * v_rot, sigma ~ E^(1/4)  Tully-Fisher / Faber-Jackson velocities at fixed M_bar [DERIVED, DEGENERATE]
   * Sigma_c ~ E             Freeman critical surface density; early disks denser [DERIVED, DEGENERATE]
   * EFE ~ 1/E               External Field Effect WEAKENS [DERIVED, DISTINCTIVE -- DM-forbidden]
  BTFR/FJ zero-point shifts by -log10 E(z): -0.48 dex (z=2), -1.0 (z=6), -1.3 (z=10.6).
  ALL boosts are [REGIME]: they need g_bar < a0(z). The next part shows when that fails.\n""")


def part2_regime():
    print("="*86)
    print("PART 2 -- the regime check: WHICH galaxies show the boost (extended) vs none (compact)")
    print("="*86)
    print("  A galaxy of baryonic mass M_b and half-light radius R has g_bar = G M_b/R^2.")
    print("  The MOND transition is at g_bar = a0(z), i.e. radius r_M = sqrt(G M_b/a0(z)).")
    print("  Inside r_M: Newtonian (no boost). Outside: deep-MOND (full sqrt(E) boost).\n")
    Mb = 1e9*Msun
    print(f"  Worked at fixed M_bar=1e9 Msun; r_M and boost nu(g_bar/a0(z)) vs (z, R):")
    print(f"     {'z':>5}{'a0(z)':>11}{'r_M[pc]':>10}   boost nu at R = 100pc / 500pc / 2kpc")
    for z in (2, 6, 10.6):
        a0z = A0*E(z); rM = np.sqrt(G*Mb/a0z)
        boosts = []
        for R in (100*pc, 500*pc, 2*kpc):
            gbar = G*Mb/R**2
            boosts.append(nu(gbar/a0z))
        print(f"     {z:>5}{a0z:>11.2e}{rM/pc:>10.0f}        "
              f"{boosts[0]:.2f}      /  {boosts[1]:.2f}   /  {boosts[2]:.2f}")
    print("""
  READ: a 1e9-Msun galaxy is Newtonian (boost ~1) at R=100 pc but deep-MOND (boost
  >2-4) at R=2 kpc. So the framework's distinctive boosts live in EXTENDED, low-
  surface-brightness high-z galaxies -- NOT the compact ones JWST most easily finds.\n""")


def part3_gnz11():
    print("="*86)
    print("PART 3 -- GN-z11 (z=10.60): the real numbers, done properly")
    print("="*86)
    z = 10.60; Ez = E(z); a0z = A0*Ez
    Mstar = 10**9.1 * Msun                 # Tacchella/Bunker: log M*=9.1 (+0.3/-0.4)
    Mdyn  = 1.1e9 * Msun                    # Xu+2024 (2404.16963): M_dyn=(1.1+-0.4)e9
    Re    = 60*pc                           # very compact half-light radius ~60 pc
    vrot  = 205e3                           # ~205 km/s rotation (AGN-contaminated)
    gbar  = G*Mstar/Re**2
    rM    = np.sqrt(G*Mstar/a0z)
    print(f"  data (Xu+2024 IFS; Tacchella+2023; Bunker+2023; Maiolino+2024 AGN):")
    print(f"     z=10.60   M_* = {Mstar/Msun:.2e}   M_dyn = {Mdyn/Msun:.2e}   R_e ~ 60 pc")
    print(f"     v_rot ~ 205 km/s   AND it hosts an AGN (broad lines, n_e>1e10 cm^-3)")
    print(f"  framework at z=10.60:  E={Ez:.1f}   a0(z)={a0z:.2e} m/s^2 (= {Ez:.0f}x local)")
    print(f"  acceleration regime:")
    print(f"     g_bar = G M_*/R_e^2 = {gbar:.2e} m/s^2  ->  g_bar/a0(z) = {gbar/a0z:.1f}  >> 1")
    print(f"     MOND radius r_M = sqrt(G M_*/a0(z)) = {rM/pc:.0f} pc, but R_e ~ 60 pc")
    print(f"     => GN-z11 is DEEPLY NEWTONIAN inside R_e; predicted boost nu = {nu(gbar/a0z):.2f}")
    print(f"""
  VERDICT [consistent, but NOT a test]:
   * The framework predicts NO MOND boost for GN-z11 -- it is compact (R_e ~ 60 pc),
     so g_bar ~ {gbar/a0z:.0f} a0(z), deep in the Newtonian regime. Predicted M_dyn/M_* ~ 1.
   * OBSERVED: M_dyn/M_* = {Mdyn/Mstar:.2f} -- 'dynamical mass dominated by the stellar
     component' (Xu+2024). So the data AGREE with the framework -- but TRIVIALLY: no
     boost was predicted and none is seen. It also agrees with plain Newton and LCDM.
   * GN-z11 therefore does NOT test the distinctive sqrt(E)=4.7x boost: it is the wrong
     KIND of galaxy (compact, not extended) AND AGN-contaminated. MOND effects would
     only appear beyond r_M~{rM/pc:.0f} pc, in faint outskirts not kinematically probed.
   * Its 'massiveness' (massive/luminous for z=10.6) is a STAR-FORMATION puzzle (SFE,
     IMF, feedback-free) -- which a0(z) does NOT address. The framework changes
     DYNAMICS, not how fast stars form. Do not claim GN-z11 as support.\n""")


def part4_what_would_test():
    print("="*86)
    print("PART 4 -- what a CLEAN test looks like (the galaxy JWST must find)")
    print("="*86)
    z = 8.0; Ez = E(z); a0z = A0*Ez
    Mb = 5e8*Msun; Re = 2*kpc               # extended, gas-rich, low-surface-brightness
    gbar = G*Mb/Re**2
    print(f"  An EXTENDED z=8 galaxy: M_bar=5e8 Msun, R_e=2 kpc (low surface brightness).")
    print(f"     g_bar/a0(z) = {gbar/a0z:.2f}  (deep-MOND) -> predicted boost nu = {nu(gbar/a0z):.2f}")
    print(f"     i.e. M_dyn/M_bar ~ {nu(gbar/a0z):.1f}, and v_flat=(G M_bar a0(z))^(1/4) = "
          f"{(G*Mb*a0z)**0.25/1e3:.0f} km/s")
    print("""  THIS is the test: extended, rotation-supported, AGN-free, with a measured gas
  mass and a known environment, at z>~6. Such galaxies are rare in current samples
  (JWST most easily finds compact/AGN systems). The distinctive EFE-vs-z signal needs
  ~600-1600 of them across z (see EFE_vs_z_Forecast_2026). Individually the sqrt(E)
  boost is LCDM-degenerate; the cross-channel COHERENCE (M_dyn/M_b, v, Sigma all
  scaling with the SAME E(z)) is what selection + halo evolution cannot forge.\n""")


def main():
    part1_ladder(); part2_regime(); part3_gnz11(); part4_what_would_test()
    print("="*86); print("BOTTOM LINE"); print("="*86)
    print("""  * The framework predicts a coherent set of high-z boosts, all driven by E(z):
    M_dyn/M_b~sqrt(E), v~E^1/4, Sigma_c~E, EFE~1/E. By z=10.6, E=22, sqrt(E)=4.7x.
  * Each boost INDIVIDUALLY is LCDM-degenerate; only the EFE weakening (DM-forbidden)
    and the cross-channel coherence are distinctive.
  * The boosts apply ONLY to EXTENDED (deep-MOND) galaxies. The compact, AGN-bearing
    systems JWST most easily resolves (GN-z11; the de Graaff/JADES compacts) are
    Newtonian -> no boost -> NOT tests. GN-z11's M_dyn/M_*~1 is consistent but trivial.
  * The early-MASSIVE-galaxy tension is a star-formation problem; a0(z) does not solve
    it and the framework should not claim it.""")
    print("="*86)


if __name__ == "__main__":
    main()
