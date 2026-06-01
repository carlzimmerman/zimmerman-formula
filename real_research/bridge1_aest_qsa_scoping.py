#!/usr/bin/env python3
"""
Bridge 1 scoping: the covariant completion (θ-coupled AeST), and why running a0 is CMB-safe.
============================================================================================

The goal of Bridge 1 (BRIDGE_TO_UNIFICATION.md): one Lagrangian giving MOND-in-galaxies + the
CMB + the evolving scale a0(z)=cH/Z. The decisive open calculation is the delta-phi Boltzmann
run, which needs AeST's free function K(Y) coded into a modified CLASS/hi_class -- a software
task, NOT faked here. But there is real analytic scoping that tells us WHERE a0 enters and WHY
the running is plausibly CMB-safe -- and one piece of it is EXACT. Honesty levels are marked:

  [STRUCTURAL]  established AeST formalism (Skordis-Zlosnik 2021), cited not re-derived
  [EXACT]       computed here, follows rigorously from the premise
  [HEURISTIC]   plausibility argument (galactic intuition applied to cosmology)
  [REMAINING]   the real calculation still to do -- named, not faked

Run:  python real_research/bridge1_aest_qsa_scoping.py
"""

import math

c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)
OM, OL, Or = 0.315, 0.685, 9.2e-5
H0 = 67.4e3 / MPC


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL + Or * (1 + z) ** 4)


def part1():
    print("#" * 84)
    print("# PART 1 [STRUCTURAL] where a0 lives in AeST, and where the CMB fit lives")
    print("#" * 84)
    print("   AeST (Skordis-Zlosnik 2021): metric g + unit-timelike vector A_mu (aether) + scalar phi.")
    print("   * the MOND force in galaxies comes from the SCALAR GRADIENT, with a0 set by the part")
    print("     of the free function K(Y) governing the low-gradient (MOND) regime.")
    print("   * the CMB fit comes from a DIFFERENT structure: the scalar's cosmological energy")
    print("     density behaves DUST-LIKE (CDM-mimicking) via the shift-symmetric mass term --")
    print("     which is a0-INDEPENDENT. (This is why SZ fit the CMB at all.)")
    print("   => Promoting a0 -> a0(z) modifies the GALAXY (gradient) sector; the dust-mode that")
    print("      fits the CMB is, structurally, a separate knob. Plausible separability -- the")
    print("      Boltzmann run must confirm the perturbations don't couple (Part 5).")
    print("   The promotion (relativistic_frontier.py): couple a0 to the aether expansion")
    print("      theta = div A = 3H  ->  a0 = c*theta/(3Z) = cH/Z  (a LOCAL field carries H(z)).\n")


def part2():
    print("#" * 84)
    print("# PART 2 [EXACT] the cosmic dynamical acceleration is a_H = cH = Z*a0 at EVERY epoch")
    print("#" * 84)
    print(f"   {'z':>7}{'a0(z)=cH/Z':>14}{'a_H=cH':>13}{'a_H/a0':>9}")
    for z in (0, 1, 2, 1100, 3400):
        Hz = H0 * E(z)
        a0 = c * Hz / Z
        print(f"   {z:>7}{a0:>14.2e}{c*Hz:>13.2e}{(c*Hz)/a0:>9.3f}")
    print("   => g_ext/a0 = Z = 5.789 is EPOCH-INDEPENDENT. The cosmic medium always sits at the")
    print("      SAME fixed multiple Z of the MOND scale -- this is the keystone for Part 3.\n")


def part3():
    print("#" * 84)
    print("# PART 3 [HEURISTIC] therefore the EFE-regulated boost on perturbations is FROZEN in z")
    print("#" * 84)
    print("   Cosmological perturbations have tiny self-gravity (g_N << a0, naive deep-MOND), but")
    print("   they sit in the cosmic field a_H = Z*a0, which EFE-screens them. Treating a_H as the")
    print("   external field, G_eff/G ~ 1/mu(g_ext/a0) = 1/mu(Z):")
    for nm, mu in [("simple   x/(1+x)", Z / (1 + Z)),
                   ("standard x/sqrt(1+x^2)", Z / math.sqrt(1 + Z * Z))]:
        print(f"     {nm:24} mu(Z)={mu:.3f}  ->  G_eff/G = {1/mu:.3f}")
    print("   The VALUE is mu-dependent (~1.01-1.17), but the ROBUST point does not need the value:")
    print("   because g_ext/a0 = Z is epoch-independent (Part 2), WHATEVER the screening is, it is")
    print("   the SAME at every epoch. So the a0-running cancels out of large-scale growth --")
    print("   running a0 is ~INVISIBLE to the CMB / linear structure. [heuristic: the galactic EFE")
    print("   is applied to cosmology; the rigorous version is the perturbed AeST system, Part 5.]\n")


def part4():
    print("#" * 84)
    print("# PART 4 [CONCLUSION] two independent reasons scaling a0 is plausibly CMB-safe")
    print("#" * 84)
    print("   (a) STRUCTURAL: the CMB-fitting dust-mode (delta-phi) is a0-INDEPENDENT (Part 1), so")
    print("       running a0 does not touch the part of the theory that fits the peaks.")
    print("   (b) DYNAMICAL: the a0-dependent MOND boost on cosmological scales is EFE-FROZEN at")
    print("       G_eff/G ~ 1/mu(Z), epoch-independent (Parts 2-3), so the running cancels there too.")
    print("   Both point the same way: the SZ CMB success likely survives a0 -> a0(z). This matches")
    print("   FRAMEWORK.md's note and sharpens it with the exact a_H=Z*a0 invariant. It is a")
    print("   PLAUSIBILITY result, not a proof -- but it tells us the run is worth doing and why.\n")


def part5():
    print("#" * 84)
    print("# PART 5 [REMAINING] the one real calculation -- named, scoped, not faked")
    print("#" * 84)
    print("   Implement theta-coupled AeST in a modified Boltzmann code (hi_class / a CLASS patch):")
    print("    1. AeST background + perturbations with the paper's free function K(Y);")
    print("    2. promote a0 -> a0(z) = c*theta/(3Z), theta = div A (= 3H on the background);")
    print("    3. evolve delta_phi through matter-radiation equality and recombination;")
    print("    4. CHECK: does delta_phi still grow dust-like (the CDM-mimicking mode) and reproduce")
    print("       the 3rd-peak height? Compare C_ell to Planck.")
    print("   PASS -> a0(z)=cH/Z is a genuine relativistic, CMB-viable, evolving-MOND theory")
    print("           (Bridge 1 complete: one Lagrangian for galaxies + CMB + the evolving scale).")
    print("   FAIL -> the running breaks the dust-mode; the framework stays a successful low-z")
    print("           law with a known relativistic gap. Either way it is decisive and honest.")
    print("   Tooling note: hi_class already implements Horndeski/EFT-of-DE perturbations; the AeST")
    print("   vector+constraint sector is the part that needs adding. A real project, days-to-weeks,")
    print("   not a one-liner -- which is exactly why this file scopes it rather than fakes it.\n")


def main():
    part1(); part2(); part3(); part4(); part5()
    print("=" * 84)
    print("  NET: a0 enters the galaxy (gradient) sector, not the CMB dust-mode; and the cosmic")
    print("  EFE parameter g_ext/a0 = Z is epoch-independent, so running a0 is ~invisible to large")
    print("  scales. Scaling a0 is therefore plausibly CMB-safe -- the analytic green light for the")
    print("  delta-phi Boltzmann run, which is Bridge 1's decisive, still-to-do calculation.")
    print("=" * 84)


if __name__ == "__main__":
    main()
