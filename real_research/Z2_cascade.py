#!/usr/bin/env python3
"""
IF a0 = (c/2) sqrt(G rho_c) is exactly true, what does it force? The cascade.
============================================================================

A conditional exploration (Carl's request): ASSUME the premise -- a0 is half the
surface gravity of the cosmic dynamical scale, a0 = (c/2)sqrt(G rho_c) = cH/Z,
Z = 2 sqrt(8pi/3) -- is EXACT, and trace its logical consequences. Each step is a
rigorous implication of the premise (not a new fit), tagged:
  [FORCED]    must follow if the premise holds
  [TEST]      how it becomes falsifiable
  [STATUS]    what current data says

Run:  python real_research/Z2_cascade.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
HBAR = 1.054571817e-34
KB = 1.380649e-23
Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL = 0.315, 0.685
A0 = 1.13e-10            # SPARC RAR (the measured anchor)


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def main():
    print("#" * 78)
    print("# PREMISE:  a0 = (c/2) sqrt(G rho_c) = cH/Z   (Z = 2 sqrt(8pi/3) = 5.789)")
    print("#" * 78)
    print()

    print("=" * 78)
    print("STEP 1 [FORCED] a0 MUST evolve -- constant-a0 MOND is INCONSISTENT")
    print("=" * 78)
    print("   rho_c(z) = rho_c0 E(z)^2 (Friedmann) => a0(z) = a0(0) E(z). The premise does")
    print("   NOT permit constant a0; that is the whole point. Z cancels in the ratio.")
    print(f"   {'z':>5}{'a0(z)/a0(0)=E(z)':>20}")
    for z in (0, 1, 2, 6, 10):
        print(f"   {z:>5}{E(z):>20.2f}")
    print("   [TEST] deep-MOND BTFR zero-point vs z. [STATUS] de Graaff z~6 leans this way;")
    print("   clean z>10 test pending (highz_kinematic_test.py).\n")

    print("=" * 78)
    print("STEP 2 [FORCED] a0 is a LATE-UNIVERSE, gravitational measurement of H0")
    print("=" * 78)
    print("   Invert the premise:  H0 = Z a0 / c.  Galaxy dynamics -> a0 -> H0, with NO")
    print("   distance ladder and NO CMB. What value?")
    for a0, tag in [(1.13e-10, "SPARC (this fit)"), (1.20e-10, "McGaugh")]:
        H0 = Z * a0 / c * MPC / 1e3
        print(f"     a0 = {a0:.2e} ({tag:16}) -> H0 = {H0:.1f} km/s/Mpc")
    print("   => the premise yields H0 = 67-72, i.e. the PLANCK / early-universe value,")
    print("      NOT SH0ES (73). At H0=73 the premise needs a0=1.23e-10 (8% above SPARC).")
    print("   [FORCED CONSEQUENCE] the premise implies the local distance-ladder H0 is")
    print("   biased high and the true H0 ~ 67-71. [TEST] pin a0 to 2% (gas-rich rotators)")
    print("   -> a THIRD H0, adjudicating the Hubble tension. This is the sharpest cascade.\n")

    print("=" * 78)
    print("STEP 3 [FORCED] a0(z) is a COSMIC CHRONOMETER -> independent H(z), w(z)")
    print("=" * 78)
    print("   H(z) = Z a0(z) / c. Measuring a0 at several z (deep-MOND BTFR) reconstructs")
    print("   the expansion history from GALAXY DYNAMICS -- independent of SNe/BAO/CMB,")
    print("   hence an independent probe of dark energy w(z).")
    for z in (0, 1, 2):
        Hz = Z * (A0 * E(z)) / c * MPC / 1e3
        print(f"     z={z}: a0={A0*E(z):.2e} -> H(z)={Hz:.0f} km/s/Mpc")
    print("   [TEST] requires a0(z) to ~few % at z=1-2. A genuinely new cosmological probe.\n")

    print("=" * 78)
    print("STEP 4 [FORCED] a0 floors at the COSMOLOGICAL CONSTANT")
    print("=" * 78)
    HL = math.sqrt(OL)                      # H_Lambda/H0
    a0_floor = A0 * HL
    Lam_term = (c ** 2 / 2) * math.sqrt((3 * (math.sqrt(OL)*A0*Z/c)**2 / c**2) / (8*math.pi))
    print(f"   far future rho->rho_Lambda: a0_floor = a0(0) sqrt(OL) = {a0_floor:.2e} m/s^2")
    print("   = (c^2/2) sqrt(Lambda/8pi). So the dark-MATTER scale a0 and dark ENERGY (Lambda)")
    print("   are ONE quantity: a0 is the cosmic density in acceleration units, evolving from")
    print(f"   today's {A0:.2e} down to the Lambda floor {a0_floor:.2e}. (Today a0 is")
    print(f"   {(1/HL-1)*100:.0f}% above its floor.) [STATUS] verified identity (a0_derived_relations).\n")

    print("=" * 78)
    print("STEP 5 [FORCED] a0 is ENVIRONMENT-INDEPENDENT (global, not local rho)")
    print("=" * 78)
    print("   a0 is set by the GLOBAL rho_c(z), not a galaxy's local density -- else a0 would")
    print("   vary ~sqrt(200/0.2)=32x from clusters to voids. Observed UNIVERSAL to <25%.")
    print("   [FORCED + OBSERVED] the premise REQUIRES the observed universality of a0.")
    print("   [TEST] a0 vs environment at fixed z (WALLABY void vs cluster) -- must be flat.\n")

    print("=" * 78)
    print("STEP 6 [FORCED] high-z galaxies look DARK-MATTER-RICH: M_dyn/M_bar ~ sqrt(E(z))")
    print("=" * 78)
    print("   MOND boost = sqrt(a0(z)/g_bar) ~ sqrt(E(z)) at fixed baryonic acceleration.")
    print(f"   {'z':>5}{'boost vs z=0  sqrt(E(z))':>26}")
    for z in (0, 2, 6, 10):
        print(f"   {z:>5}{math.sqrt(E(z)):>26.2f}")
    print("   => apparent dark-matter fraction RISES with z. [STATUS] de Graaff find")
    print("   M_dyn/M_* up to 40 at z~6 -- which constant-a0 MOND cannot make but this can.\n")

    print("=" * 78)
    print("STEP 7 [INTERPRETATION] MOND IS cosmology -- a Machian / thermal reading")
    print("=" * 78)
    T_a0 = HBAR * A0 / (2 * math.pi * c * KB)
    T_dS = HBAR * (A0 * Z / c) / (2 * math.pi * KB)
    print("   * Inertia is cosmic (Mach/Sciama): the inertial transition a0 = half the")
    print("     surface gravity of the cosmic dynamical scale -- inertia set by cosmic mass.")
    print(f"   * Thermal: T_a0 = hbar a0/2pi c kB = {T_a0:.2e} K = T_dS/Z; dynamics change when")
    print(f"     a body's Unruh temperature falls to the de Sitter temperature / Z.")
    print("   * The dark sector is unified: ONE evolving scale a0(z) is dark matter (the RAR)")
    print("     AND dark energy (its Lambda floor). No separate dark components.\n")

    print("#" * 78)
    print("# NET: what the premise buys, and what kills it")
    print("#" * 78)
    print("  IF a0=(c/2)sqrt(Grho) is exact, then -- forced, not optional:")
    print("   * a0 evolves as E(z) (constant-a0 MOND is excluded);")
    print("   * a0 measures H0 from galaxy dynamics, landing on PLANCK (~67-71), implying")
    print("     SH0ES is biased -- the sharpest, most consequential prediction;")
    print("   * a0(z) is a new cosmic chronometer / dark-energy probe;")
    print("   * a0 floors at Lambda (dark matter scale = dark energy, one quantity);")
    print("   * a0 is environment-independent (matches observed universality);")
    print("   * high-z galaxies look dark-matter-rich, rising as sqrt(E(z)) (matches de Graaff).")
    print("  FALSIFIERS: if the true H0 is SH0ES (73) with a0<1.2e-10; if precise a0/cH0 lands")
    print("  on 1/6 or 1/2pi not 1/Z; if a0 varies with environment; if z>10 deep-MOND BTFR")
    print("  shows NO evolution. Each is a clean, near-term kill. The premise is a tightly")
    print("  coupled, falsifiable package -- not a free parameter.")


if __name__ == "__main__":
    main()
