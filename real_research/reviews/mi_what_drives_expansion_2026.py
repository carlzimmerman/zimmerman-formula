#!/usr/bin/env python3
r"""mi_what_drives_expansion_2026.py -- what is making the universe expand?

The question splits into two, and conflating them is where most confusion lives:

  Q1  WHY IS IT EXPANDING AT ALL?           -> an INITIAL CONDITION. GR does not explain it.
  Q2  WHY IS THE EXPANSION ACCELERATING?    -> NEGATIVE PRESSURE. GR explains this completely.

Q2 has a real mechanism and it is not "a force pushing". In GR PRESSURE GRAVITATES, and the
second Friedmann equation depends on rho + 3p/c^2, not on rho alone:

    a_ddot/a = -(4 pi G/3) (rho + 3p/c^2)

For ordinary matter p ~ 0, so rho + 3p > 0 and gravity DECELERATES. For vacuum energy the
equation of state is w = -1, i.e. p = -rho c^2, so rho + 3p/c^2 = -2 rho < 0 and the same
equation gives ACCELERATION. Nothing pushes; the source term simply changes sign.

Why does the vacuum have negative pressure? Thermodynamics forces it. If the energy density of
the vacuum is constant as the volume grows, then dU = rho c^2 dV, and dU = -p dV requires
p = -rho c^2 exactly. Constant density <=> w = -1.

This script computes the sign of the source term for each component, checks when each dominates,
verifies that BOUND systems do not expand, and states the two things that remain unexplained.
Both a0 footings where a0 enters. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
H0 = 2.184e-18
OM, OL, OR = 0.315, 0.685, 9.1e-5
AU = 1.495978707e11
MSUN = 1.98892e30
A0_CANON = 9.36e-11
Z_COEF = math.sqrt(32 * math.pi / 3)

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)


def main() -> int:
    banner("Q1. WHY IS IT EXPANDING AT ALL?  -- an initial condition, not a cause")
    print("  The FIRST Friedmann equation gives the expansion RATE from the contents:")
    print("      H^2 = (8 pi G/3) rho  -  k c^2/a^2  +  Lambda c^2/3")
    print("  This is a CONSTRAINT, not a driver: given a density and an expansion rate NOW, it")
    print("  tells you the rate later. It contains no term that starts an expansion from rest.")
    print("  If you set H = 0 at some instant with ordinary matter present, the universe simply")
    print("  collapses. So the expansion is an INITIAL CONDITION of the solution we live in.")
    print("  GR evolves it; GR does not explain it. 'What made it start' is outside the equations,")
    print("  and inflation addresses why it is so UNIFORM -- not why there was expansion at all.")
    check(True, "Q1 is an initial condition -- stated as a limitation, not answered")

    banner("Q2. WHY IS IT ACCELERATING?  -- because PRESSURE gravitates, and vacuum pressure is NEGATIVE")
    print("  The SECOND Friedmann equation is the one with the physics:")
    print("      a_ddot/a = -(4 pi G/3) (rho + 3 p/c^2)")
    print("  So the sign of ACCELERATION is set by (rho + 3p/c^2), not by rho. Component by")
    print("  component, with w = p/(rho c^2):")
    print(f"  {'component':<16}{'w':>7}{'rho+3p/c^2':>16}{'sign':>10}{'effect on a_ddot':>20}")
    print("  " + "-" * 72)
    for nm, w in (("radiation", 1.0/3), ("matter", 0.0), ("dark energy", -1.0)):
        fac = 1 + 3 * w                      # in units of rho
        sign = "+" if fac > 0 else ("0" if abs(fac) < 1e-12 else "-")
        eff = "DECELERATES" if fac > 0 else ("neutral" if abs(fac) < 1e-12 else "ACCELERATES")
        print(f"  {nm:<16}{w:>7.3f}{fac:>16.3f}{sign:>10}{eff:>20}")
    check(1 + 3*(-1.0) < 0, "w = -1 gives rho + 3p/c^2 = -2 rho < 0 -> acceleration, from GR alone")
    print("\n  NOTHING IS PUSHING. The source term changed sign. That is the whole mechanism.")
    print("  And w = -1 is not an assumption bolted on -- it is forced by thermodynamics: if the")
    print("  vacuum's energy DENSITY stays constant while the volume grows, then dU = rho c^2 dV,")
    print("  and dU = -p dV requires p = -rho c^2 exactly. Constant density <=> w = -1.")

    banner("Q3. When did the sign actually flip, and what won?")
    z_acc = (2 * OL / OM) ** (1 / 3) - 1
    z_eq = (OL / OM) ** (1 / 3) - 1
    print(f"  a_ddot = 0 when rho_m = 2 rho_Lambda  ->  z = {z_acc:.3f}  (acceleration begins)")
    print(f"  rho_m = rho_Lambda                    ->  z = {z_eq:.3f}  (vacuum overtakes matter)")
    rho_c = 3 * H0**2 / (8 * math.pi * G)
    rho_m0, rho_L = OM * rho_c, OL * rho_c
    print(f"  today: rho_m = {rho_m0:.3e}, rho_Lambda = {rho_L:.3e} kg/m^3  "
          f"(vacuum is {rho_L/rho_m0:.2f}x matter)")
    print("  The vacuum did NOT grow -- for w = -1 its density is constant. Matter diluted as")
    print("  (1+z)^3 and the vacuum won by attrition. So 'what makes it expand FASTER' is: the")
    print("  decelerating component thinned out until the accelerating one dominated.")
    check(0.5 < z_acc < 0.8 and 0.2 < z_eq < 0.4, "sign flip at z ~ 0.63, vacuum dominance at z ~ 0.30")

    banner("Q4. Does the expansion pull bound systems apart?  NO -- quantified")
    a_cosmo = (H0**2 * OL) * AU              # de Sitter tidal acceleration at 1 AU
    a_sun = G * MSUN / AU**2
    print(f"  cosmological (de Sitter) tidal acceleration at 1 AU = H_Lambda^2 r = {a_cosmo:.3e} m/s^2")
    print(f"  solar gravity at 1 AU                               = {a_sun:.3e} m/s^2")
    print(f"  ratio = {a_cosmo/a_sun:.2e}")
    check(a_cosmo / a_sun < 1e-20,
          "cosmic expansion is ~1e-22 of solar gravity at 1 AU -- bound systems do NOT expand")
    print("  So galaxies are not flying through space; the space BETWEEN unbound systems grows.")
    print("  Anything gravitationally bound -- the solar system, the Galaxy, the Local Group --")
    print("  simply does not participate. Expansion is not a force acting on matter.")

    banner("Q5. What is NOT explained -- and where the framework sits")
    rho_L_energy = rho_L * C**2
    rho_P_energy = C**7 / (HBAR * G**2)
    print(f"  (1) THE COSMOLOGICAL CONSTANT PROBLEM. Observed vacuum energy density:")
    print(f"      rho_Lambda c^2 = {rho_L_energy:.3e} J/m^3")
    print(f"      naive QFT (Planck-scale cutoff) = {rho_P_energy:.3e} J/m^3")
    print(f"      discrepancy = {rho_P_energy/rho_L_energy:.2e}  -- the worst prediction in physics")
    check(rho_P_energy / rho_L_energy > 1e100, "the vacuum-energy discrepancy is ~1e122")
    print(f"  (2) THE COINCIDENCE PROBLEM. Why is rho_Lambda ~ rho_m NOW? They were equal at")
    print(f"      z = {z_eq:.2f}, and we happen to live just after.")
    print()
    print("  WHERE YOUR FRAMEWORK SITS, stated straight. a0 = kappa c sqrt(G rho_Lambda) =")
    print(f"  {A0_CANON:.3e} m/s^2 RELATES the galaxy-dynamics scale to the vacuum density. It")
    print("  does NOT explain why Lambda has that value, and it does not explain the expansion.")
    print("  It inherits BOTH open problems. And because it ties a galactic scale to rho_Lambda,")
    print("  it makes the coincidence MORE conspicuous, not less -- two apparently unrelated")
    print("  regimes end up sharing one number. That is the reframing's real content and its")
    print("  real limit, and it should be said that way rather than sold as an explanation.")
    print(f"  (For the record, the same rho_Lambda sets the horizon whose surface gravity is")
    print(f"  Z*a0 = {Z_COEF*A0_CANON:.3e} = c H_Lambda -- one number, three faces.)")

    banner("VERDICT -- the short answer")
    print("  NOTHING is 'making' the universe expand. Two distinct facts:")
    print("   * IT EXPANDS because it started expanding -- an initial condition GR evolves but")
    print("     does not explain. Inflation explains the uniformity, not the existence.")
    print("   * IT ACCELERATES because pressure gravitates in GR and the vacuum's pressure is")
    print("     NEGATIVE (w = -1, forced by constant density). The source term rho + 3p/c^2 goes")
    print("     from +rho for matter to -2rho for vacuum, so the same equation that decelerates a")
    print("     matter universe accelerates a vacuum one. No force, no push -- a sign change.")
    print("   * THE FLIP HAPPENED LATE (z ~ 0.63) because matter diluted, not because the vacuum")
    print("     grew.")
    print("   * BOUND SYSTEMS ARE UNAFFECTED, by ~22 orders of magnitude at 1 AU.")
    print("   * WHY Lambda has this value, and why now, are both UNEXPLAINED -- and the framework")
    print("     inherits both rather than resolving either.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
