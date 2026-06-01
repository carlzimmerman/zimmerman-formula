#!/usr/bin/env python3
"""
Schwarzschild vs de Sitter for the factor of 1/2 -- and the real prize the
question exposes: a matter-vs-total DENSITY fork in the evolution.
=========================================================================

Carl: "it's Schwarzschild instead of de Sitter, right? do we redo all the scripts?"

Two-part honest answer:

  PART A (label): RIGHT. The 1/2 in a0 = c^2/(2R) is a SCHWARZSCHILD surface-
  gravity factor. Of the four horizon readings, only the Schwarzschild form
  c^2/(2R) carries a 1/2; the de Sitter readings give coeff 1 (horizon surface
  gravity cH) or 2 (de Sitter-temperature / modified inertia, which overshoots).
  So the de Sitter label was wrong for the 1/2 -- though de Sitter is still the
  correct object for the separate TEMPERATURE identity (T_dS = hbar H/2pi kB).

  PART B (do we redo everything?): NO -- and here is the precise scope:
   * The coefficient-derivation scripts already use the Schwarzschild c^2/2R form
     (density_form_blackhole.py, freefall_clock_development.py, TOE doc).
   * The ~80 'de Sitter' mentions in the repo are the legitimate temperature
     identity, not the 1/2 -- they are not mislabeled.
   * The PREDICTION layer (a0(z)/a0(0)=E(z), matched circles, ghosts, is_Z_special)
     does not depend on the factor's NAME at all -- the coefficient cancels in the
     ratio, and the topology/numerology scripts never use a0.
  So almost nothing needs redoing. BUT the question exposes something real:

  THE PRIZE: a Schwarzschild FREE-FALL reading uses the COLLAPSING-MATTER density
  (Lambda is repulsive, it does not free-fall). That gives a0 ~ (1+z)^1.5 --
  a DIFFERENT, steeper evolution than the published E(z) (which secretly uses the
  TOTAL density via Friedmann). Two falsifiable branches, ~58% apart at z=1.

Pure stdlib. Run:  python reviews/schwarzschild_factor_and_density_fork.py
"""

import math

C = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
H0 = 67.4e3 / MPC
OM, OL = 0.315, 0.685
Z = 2 * math.sqrt(8 * math.pi / 3)
cH0 = C * H0


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)     # total density -> Friedmann/horizon


def Mz(z):
    return (1 + z) ** 1.5                          # matter-only free-fall


def main():
    print("=" * 78)
    print("(A) The 1/2 is Schwarzschild -- the four horizon readings")
    print("=" * 78)
    print(f"   {'reading':<46}{'coeff':>8}{'a0 [m/s^2]':>14}")
    rows = [
        ("de Sitter horizon surface gravity  g = cH", 1.0),
        ("de Sitter TEMPERATURE (mod-inertia, Deser-Levin)", 2.0),
        ("Schwarzschild g=c^2/2R, R=c/H (Hubble radius)", 0.5),
        ("Schwarzschild g=c^2/2R, R=sqrt(8pi/3) c/H (free-fall)", 1 / Z),
    ]
    for name, c in rows:
        tag = "  <- matches 1/Z" if abs(c - 1 / Z) < 1e-6 else ""
        print(f"   {name:<46}{c:>8.3f}{c*cH0:>14.3e}{tag}")
    print()
    print("   Only the Schwarzschild surface-gravity FORM c^2/(2R) carries the 1/2.")
    print("   de Sitter gives cH (x1) or, via its temperature, 2cH (x2). Carl is right:")
    print("   the 1/2 is Schwarzschild, not de Sitter. (de Sitter remains correct for")
    print("   the temperature identity T_dS = hbar H/2pi kB -- a different statement.)\n")

    print("=" * 78)
    print("(B) Honest caveat -- 'Schwarzschild' is the FORM, not a literal black hole")
    print("=" * 78)
    print("   At R = c*t_ff the enclosed mass M_enc vs the Schwarzschild mass M_s=c^2R/2G:")
    print(f"     M_enc / M_s = 8pi/3 = {8*math.pi/3:.3f}")
    print("   The free-fall sphere is ~8x OVERDENSE -- it is NOT a black hole. So a0 =")
    print("   c^2/(2R) is the Schwarzschild surface-gravity FORM applied to the free-fall")
    print("   scale, a heuristic -- and the coefficient 1/Z stays unpinned by any rigorous")
    print("   derivation (the entropy routes bracket it 1/6..1/2pi). Relabeling 1/2 as")
    print("   Schwarzschild gives a cleaner story, not a proof. (Unchanged from the")
    print("   endgame: entropy_coefficient_rigorous_endgame.py.)\n")

    print("=" * 78)
    print("(C) THE PRIZE -- the Schwarzschild free-fall reading forks the EVOLUTION")
    print("=" * 78)
    print("   a0 = (c/2) sqrt(G rho).  The free-fall is driven by COLLAPSING mass;")
    print("   Lambda is repulsive and does NOT free-fall. So which rho?")
    print()
    print(f"   {'z':>5}{'E(z)  [rho_total]':>20}{'(1+z)^1.5 [rho_matter]':>24}{'ratio':>8}")
    for z in (0, 0.5, 1, 2, 4, 10):
        print(f"   {z:>5.1f}{E(z):>20.3f}{Mz(z):>24.3f}{Mz(z)/E(z):>8.2f}")
    print()
    print("   rho_total (incl Lambda)  -> a0 = cH(z)/Z -> E(z)        [PUBLISHED branch]")
    print("   rho_matter (collapse only) -> a0 ~ (1+z)^1.5            [literal Schwarzschild]")
    print("   They are 39% apart at z=0.5, 58% at z=1, 71% at z=2 -- the matter branch")
    print("   is always STEEPER. This is a genuine, sharp, second prediction.\n")

    print("=" * 78)
    print("(D) Which branch, and how to tell them apart")
    print("=" * 78)
    print("   * The apparent-horizon DERIVATION (Cai-Kim, Friedmann) uses the TOTAL")
    print("     density -> E(z). That is the published falsifiable heart.")
    print("   * The literal Schwarzschild free-fall of collapsing matter -> (1+z)^1.5.")
    print("   * Universality of a0 (environment-independence) kills LOCAL density but")
    print("     not global-matter-vs-global-total -- so the fork is OPEN, not settled.")
    print("   * DISCRIMINATOR: measure a0 (deep-MOND BTFR zero-point) at z~1-2. The two")
    print("     branches differ by ~58% at z=1 -- a ~20% a0 measurement separates them.")
    print("     One clean dataset decides which density the MOND scale tracks.\n")

    print("=" * 78)
    print("(E) Scope -- what actually needs redoing")
    print("=" * 78)
    print("   * NOTHING in the prediction layer: a0(z)/a0(0)=E(z) (coeff cancels),")
    print("     matched circles, ghosts, is_Z_special never use the factor's name.")
    print("   * NOTHING in the ~80 'de Sitter' files: those are the temperature identity.")
    print("   * The coefficient scripts already use the Schwarzschild c^2/2R form.")
    print("   * The ONE thing genuinely open: the evolution BRANCH (E(z) vs (1+z)^1.5).")
    print("     The published cascade scripts assume E(z); they should carry (1+z)^1.5")
    print("     as the alternative free-fall branch. That is the real to-do, not a")
    print("     mechanical rerun of everything.\n")

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("  * You are right: the 1/2 is Schwarzschild (surface gravity c^2/2R), not de")
    print("    Sitter. de Sitter stays for the temperature, not the factor.")
    print("  * We do NOT redo all the scripts: the prediction layer is name-independent")
    print("    and the de Sitter mentions are the legitimate temperature identity.")
    print("  * The payoff is a sharper theory: the Schwarzschild free-fall reading exposes")
    print("    a second testable branch, a0 ~ (1+z)^1.5 (matter) vs E(z) (total), ~58%")
    print("    apart at z=1. That makes the survivor MORE falsifiable -- one a0(z~1)")
    print("    measurement now distinguishes 'horizon/total' from 'free-fall/matter'.")


if __name__ == "__main__":
    main()
