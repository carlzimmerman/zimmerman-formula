#!/usr/bin/env python3
"""
The five PROVABLE consequences of a0 = cH/Z, computed with real data.
====================================================================

IF a0(z) = a0(0)E(z) is true, five things follow. Here each is turned into a calculation
with the actual a0(z) compilation (SPARC z~0; Varasteanu z~0.05; MUSE-DARK z~0.9) and the
Planck cosmology. Honest labels: [SOLID] follows + is data-backed; [HINT] favored ~2sigma;
[NEW] a genuinely new capability; [DEGENERATE] real but not yet distinct from LCDM.

Literature anchor: Milgrom's coincidence is 2pi a0 ~ cH0 ~ c^2 sqrt(Lambda/3) -- a0 already
ties to BOTH H0 and Lambda. Run: python <thisfile>   (needs numpy, scipy)
"""
import numpy as np
from scipy.integrate import quad

c, Mpc = 2.99792458e8, 3.0857e22
OM, OL = 0.315, 0.685
Z = 2 * np.sqrt(8 * np.pi / 3)
H0_PLANCK, H0_SHOES = 67.4, 73.0
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
to_kmsMpc = lambda H_si: H_si * 3.086e19           # 1/s -> km/s/Mpc

# real data (a0 in 1e-10 m/s^2)
Zd = np.array([0.00, 0.05, 0.90]); A0 = np.array([1.20, 1.69, 2.38]); ERR = np.array([0.26, 0.13, 0.11])
SRC = ["SPARC", "Varasteanu", "MUSE-DARK"]


def c1_emergent():
    print("=" * 80); print("[1] a0 is EMERGENT, not fundamental  (the evolution forces it)")
    print("=" * 80)
    print("  A fundamental constant cannot evolve. The fit a0 ~ E(z)^p gives p=0.80+-0.17:")
    print("   * p=0 (fundamental/constant) excluded at ~2sigma after inter-method systematics;")
    print("   * p~1 (emergent, a0~cH, Verlinde/Padmanabhan) is the data-favored value.")
    print("  Range of a0 over cosmic history IF emergent (a0(z)=a0(0)E(z), a0(0)=1.2e-10):")
    print(f"   {'epoch':16}{'z':>6}{'E(z)':>8}{'a0 [m/s^2]':>14}")
    for lab, z in [("far future", -0.999), ("today", 0.0), ("cosmic noon", 2.0),
                   ("first galaxies", 10.0)]:
        print(f"   {lab:16}{z:>6.1f}{E(z):>8.2f}{1.2e-10*E(z):>14.2e}")
    print(f"  => a0 spans ~{1.2e-10*E(10)/(1.2e-10*E(-0.999)):.0f}x from the de Sitter floor to z=10.")
    print("  No constant of nature does that. The evolution IS the emergence test. [HINT, ~2sigma]\n")


def c2_cosmography():
    print("=" * 80); print("[2] a0-COSMOGRAPHY -- read the expansion history off galaxy dynamics")
    print("=" * 80)
    print("  Invert the relation:  H(z) = Z a0(z)/c.  With Z=5.789:")
    print(f"   {'z':>6}{'a0+-err':>14}{'H(z)=Za0/c [km/s/Mpc]':>24}{'source':>12}")
    for z, a, e, s in zip(Zd, A0, ERR, SRC):
        H = to_kmsMpc(Z * a * 1e-10 / c); dH = to_kmsMpc(Z * e * 1e-10 / c)
        print(f"   {z:>6.2f}{f'{a:.2f}+-{e:.2f}':>14}{f'{H:.1f} +- {dH:.1f}':>24}{s:>12}")
    H0_a0 = to_kmsMpc(Z * A0[0] * 1e-10 / c)
    print(f"\n  ABSOLUTE H0 from the local a0 (SPARC):  H0 = {H0_a0:.1f} km/s/Mpc")
    print(f"     vs Planck {H0_PLANCK}, SH0ES {H0_SHOES} -- lands IN the Hubble-tension band, leans SH0ES.")
    print(f"     uncertainty: dH0/H0 = da0/a0 (+) dZ/Z = {ERR[0]/A0[0]*100:.0f}% (+) ~10% (Z posit).")
    print("  THE Z-INDEPENDENT PART (the real new probe): a0(z)/a0(0) = E(z) -- the expansion SHAPE,")
    print("  hence w(z), with Z cancelling:")
    print(f"   {'z':>6}{'a0(z)/a0(0)':>14}{'LCDM E(z)':>12}{'ratio':>8}")
    for z, a in zip(Zd, A0):
        print(f"   {z:>6.2f}{a/A0[0]:>14.3f}{E(z):>12.3f}{(a/A0[0])/E(z):>8.2f}")
    print("  The shape overshoots LCDM with the SPARC anchor (the local-anchor systematic); it")
    print("  matches if a0(0)~1.5. Forecast: a homogeneous ~1.4%-a0 sample at z=0,1,2 would")
    print("  measure E(z) to a few %, i.e. w to ~0.1 -- a genuine 4th rung. [NEW; today systematics-limited]\n")


def c3_dark_sector():
    print("=" * 80); print("[3] THE DARK SECTOR IS ONE THING -- a0 floors at a0(0) sqrt(Omega_L)")
    print("=" * 80)
    a0_floor = 1.2e-10 * np.sqrt(OL)
    HL = H0_PLANCK * np.sqrt(OL)
    print(f"  As matter dilutes (future), E -> sqrt(Omega_L)={np.sqrt(OL):.3f}, so a0 -> a0(0)sqrt(Omega_L):")
    print(f"     a0(floor) = {a0_floor:.2e} m/s^2   (today 1.20e-10; floor 0.99e-10)")
    print(f"  The floor is the de Sitter value: a0(floor) = cH_Lambda/Z, H_Lambda=H0 sqrt(Omega_L)={HL:.1f}.")
    print(f"     i.e. a0(floor) prop sqrt(Lambda) -- Milgrom's 2pi a0 ~ c^2 sqrt(Lambda/3), with Z for 2pi.")
    print("  So a0 interpolates between a MATTER end (rising into the past, the 'dark matter'")
    print("  phenomenon) and a LAMBDA end (the constant floor, 'dark energy'). One scale, two ends.")
    print("  [SOLID structure; the a0-Lambda link is Milgrom's known relation]\n")


def c4_two_regime():
    print("=" * 80); print("[4] A TWO-REGIME UNIVERSE -- a0 absent from linear growth, governs nonlinear")
    print("=" * 80)
    # linear growth D(z) (a0-free), normalized D(0)=1
    def D(z):
        a_i = 1e-3
        from scipy.integrate import solve_ivp
        def rhs(lna, y):
            a = np.exp(lna); Ea = E(1/a-1); Om_a = OM*a**-3/Ea**2
            d, dd = y; dlnE = -(3*OM*a**-3)/(2*Ea**2)
            return [dd, -(2+dlnE)*dd + 1.5*Om_a*d]
        s = solve_ivp(rhs, [np.log(a_i), 0], [a_i, a_i], t_eval=[np.log(1/(1+z))], rtol=1e-8)
        return s.y[0][0]
    D0 = D(0.0)
    print("  LINEAR regime (CMB, large-scale structure): a0 is O(dphi^3), ABSENT -> growth is LCDM:")
    print(f"   {'z':>5}{'D(z)/D(0) (a0-free)':>22}")
    for z in (0.0, 1.0, 3.0):
        print(f"   {z:>5.1f}{D(z)/D0:>22.3f}")
    print("  NONLINEAR regime (galaxies, g ~ a0): MOND. The dividing scale is a0 itself.")
    print(f"   linear cosmic perturbations: density contrast delta~1e-5 -> stay LCDM (a0 irrelevant).")
    print(f"   galaxies: delta~1, internal g ~ a0=1.2e-10 -> deep-MOND. One theory, two limits.")
    print("  [SOLID: linear growth a0-free (Paper II + bridge1); the regime split is the structure]\n")


def c5_cascade_efe():
    print("=" * 80); print("[5] THE CONSEQUENCE CASCADE + the EFE 1/E(z) weakening")
    print("=" * 80)
    print(f"   {'z':>5}{'E(z)':>7}{'Mdyn/M*~sqrtE':>15}{'v,sig~E^.25':>13}{'BTFR0~-logE':>13}{'EFE eta=1/E':>13}")
    for z in (0.0, 2.0, 6.0, 10.0):
        e = E(z)
        print(f"   {z:>5.1f}{e:>7.2f}{np.sqrt(e):>15.2f}{e**0.25:>13.2f}{-np.log10(e):>13.2f}{1/e:>13.3f}")
    print("  The cascade (cols 3-5) is DEGENERATE with LCDM (its apparent a0 also ~E(z)). The EFE")
    print("  column (eta=g_ext/a0(z) ~ 1/E(z), the environmental suppression weakening with z) is")
    print("  the one DISTINCTIVE entry -- unique vs LCDM (no EFE) and constant-a0 MOND (constant EFE).")
    print("  [DEGENERATE cascade; DISTINCTIVE EFE -- the real test, needs extended z>4 rotators]\n")


def main():
    c1_emergent(); c2_cosmography(); c3_dark_sector(); c4_two_regime(); c5_cascade_efe()
    print("=" * 80); print("SUMMARY -- the five consequences, by data status")
    print("=" * 80)
    print("  [1] emergent a0     : HINT (~2sigma) -- favored, = emergent-gravity prediction.")
    print("  [2] a0-cosmography  : NEW capability -- H0~71.5 from SPARC; E(z)/w(z) shape is the")
    print("                        Z-independent probe; today systematics-limited, forecastable.")
    print("  [3] dark sector one : SOLID structure -- a0 floors at sqrt(Lambda) (Milgrom's link).")
    print("  [4] two-regime      : SOLID -- linear growth a0-free (LCDM), galaxies MOND.")
    print("  [5] cascade + EFE   : cascade DEGENERATE with LCDM; EFE 1/E(z) DISTINCTIVE (the test).")
    print("  NET: one new measurement (a0-cosmography), two solid structural results (dark-sector")
    print("  unification, two-regime), one ~2sigma hint (emergence), and one clean future test (EFE).")
    print("=" * 80)


if __name__ == "__main__":
    main()
