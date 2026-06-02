#!/usr/bin/env python3
"""
RED-TEAM, round 2 -- the pieces the first pass was too soft on.
==============================================================

Round 1 (redteam_the_puzzle.py) credited Piece 9 (EFE) as a 'bonus unification' and Piece 5
(anti-screening) as essentially fine. Re-attack both honestly, plus the deepest question:
after every cut, does the framework predict ANYTHING distinctive that is confirmed?

  ATTACK Piece 9 -- is 'evolution + EFE = one mechanism' physics, or a category error?
  ATTACK Piece 5 -- the theta->0 catastrophe: does a bound system really keep theta=3H?
  ATTACK inheritance -- 'CMB-safe' is parasitic on AeST's own fine-tuning.
  SYNTHESIS    -- strip it all: what distinctive, confirmed prediction is left?

Discipline: fair attacks. Where an attack DISSOLVES under analysis, say so (that is also a
result). Run: python <thisfile>
"""
import numpy as np

# ---------------------------------------------------------------------------
def attack_9_efe():
    print("=" * 80)
    print("ATTACK Piece 9 -- 'evolution + EFE = one mechanism' is a CATEGORY ERROR")
    print("=" * 80)
    print("   Claim: a0 = c*theta/(3Z) is set by local theta; the cosmic part 3H gives")
    print("   evolution, the inhomogeneous part div(B) gives the External Field Effect.")
    print("   Units check (c=1):")
    print("     theta = div A  ~  1/length ~ 1/TIME   (A dimensionless unit vector); on FRW =3H.")
    print("     so the framework's environmental knob is  d(theta)/theta = div(B)/3H  [dimensionless,")
    print("        a ratio of EXPANSION RATES].")
    print("     the STANDARD MOND EFE knob is  g_ext/a0   [dimensionless, a ratio of ACCELERATIONS];")
    print("        g_ext has units length/TIME^2 -- a DIFFERENT dimensionful object than div(B).")
    print("   So div(B)/3H and g_ext/a0 are DIFFERENT environmental parameters. Worse, the two")
    print("   mechanisms are physically distinct:")
    print("     * standard EFE: a0 FIXED, external g_ext suppresses the internal deep-MOND regime.")
    print("     * framework:    a0 ITSELF changes because theta_local changes.")
    print("   And the standard EFE (g_ext/a0) is STILL there in the framework -- inherited from MOND.")
    print("   So the framework has TWO environmental effects, not one; calling div(B) 'the EFE'")
    print("   conflates a velocity-divergence with an acceleration ratio. [Piece 9 OVERSTATED:")
    print("   downgrade from 'one mechanism' to 'a second, distinct, unquantified environmental term'.]\n")


def attack_5_catastrophe():
    print("=" * 80)
    print("ATTACK Piece 5 -- the theta->0 catastrophe (does a bound system keep theta=3H?)")
    print("=" * 80)
    print("   Worry: bound systems DECOUPLE from the Hubble flow (galaxies don't expand). If the")
    print("   aether is dragged into the galaxy's ~static frame, theta_local -> 0 and a0 = c*theta/3Z")
    print("   -> 0: NO MOND, total collapse. Is that the fate?")
    print("   Resolution (the attack DISSOLVES, honestly):")
    print("     theta = (1/sqrt(-g)) d_t( sqrt(-g) A^0 ).  The 3H comes from the BACKGROUND")
    print("     sqrt(-g)=a^3 growth, NOT from anything local. The quasi-static limit neglects the")
    print("     time-evolution of PERTURBATIONS (d_t delta -> 0), but the BACKGROUND a(t) still")
    print("     grows, so thetabar = 3H survives. The matter decoupling from expansion suppresses")
    print("     div(v_matter), i.e. the small delta-theta -- not the 3H background.")
    print("   => theta ~ 3H in a galaxy is DEFENSIBLE; the catastrophe does NOT occur, PROVIDED the")
    print("      aether tracks the global cosmic foliation (the standard AeST configuration). That")
    print("      proviso is unproven (full back-reaction) but is the natural case. [Piece 5 stands")
    print("      as a leading-order result; the attack fails -- reported straight.]\n")


def attack_inheritance():
    print("=" * 80)
    print("ATTACK the inheritance -- 'CMB-safe' is parasitic on AeST's own fine-tuning")
    print("=" * 80)
    print("   Pieces 4 and 7 lean entirely on AeST (Skordis-Zlosnik 2021) fitting the CMB. But")
    print("   AeST fits the CMB only with a CHOSEN free function: K(Q) = -2L + K2(Q-Q0)^2, a")
    print("   k-essence tuned so the scalar's energy density mimics CDM (dust ~ a^-3) and lands")
    print("   the 3rd peak. That dust-mimic is an ANSATZ fit to the data, not a derivation.")
    print("   So 'the framework is CMB-safe' really means 'CMB-safe INSIDE a host theory that was")
    print("   itself reverse-engineered to fit the CMB.' The order-counting (a0 absent at linear")
    print("   order) is a real theorem -- but it protects a fit that AeST already paid for by hand.")
    print("   Net: Piece 7 is sound math, but the CMB 'success' is inherited and tuned, not a")
    print("   prediction of THIS framework. [honest discount on the structural win.]\n")


def synthesis():
    print("=" * 80)
    print("SYNTHESIS -- strip everything: what distinctive, CONFIRMED prediction is left?")
    print("=" * 80)
    rows = [
        ("a0 ~ cH0 coincidence",          "INHERITED (Milgrom 1983); coefficient chosen, ~0 bits"),
        ("BTFR, RAR, Faber-Jackson",      "INHERITED standard MOND (Milgrom/McGaugh)"),
        ("relativistic completion / CMB", "INHERITED + tuned AeST (Skordis-Zlosnik)"),
        ("a0(z) = a0(0) E(z)  EVOLUTION",  "NOVEL -- but ~2sigma, single-point, regime-limited, LCDM-degenerate"),
        ("theta=3H coupling / action",    "NOVEL -- but inserted by hand; Z undetermined; parameterizes the above"),
    ]
    print(f"   {'ingredient':32}{'status':48}")
    print("   " + "-" * 80)
    for a, b in rows:
        print(f"   {a:32}{b:48}")
    print()
    print("   The ONLY distinctive content is the evolution + its coupling. After the attacks:")
    print("    * evolution: a ~2sigma hint, suppressed for the compact targets, mimicked by LCDM;")
    print("    * coupling : hand-inserted, free coefficient, parameterizes (does not explain).")
    print("   => DISTINCTIVE *and* CONFIRMED prediction set = EMPTY (today). The framework is a")
    print("      sharp, falsifiable VARIANT of relativistic MOND (constant-a0 AeST -> evolving-a0")
    print("      AeST) whose single discriminating prediction is not yet confirmed above ~2sigma.")
    print("      It is not nothing (a clean testable variant); it is not a result (no confirmation).\n")


def verdict():
    print("=" * 80)
    print("ROUND-2 VERDICT")
    print("=" * 80)
    print("  BROKE further:")
    print("   * Piece 9 (EFE): a category error -- div(B)/3H is not g_ext/a0; downgrade to a")
    print("     second, distinct, unquantified environmental term (NOT a unification).")
    print("   * The CMB 'success' is inherited from a tuned AeST, not predicted here.")
    print("   * Synthesis: NO distinctive prediction is currently confirmed (>~2sigma).")
    print("  HELD (attacked, survived):")
    print("   * Piece 5 (anti-screening): theta=3H is the BACKGROUND expansion, survives the")
    print("     quasi-static limit; the theta->0 catastrophe does not occur (given cosmic-foliation).")
    print("   * Piece 7 (linear CMB-safety): still exact (round 1).")
    print("  FINAL HONEST STANDING after two rounds: a coherent, falsifiable, CMB-safe VARIANT of")
    print("  relativistic MOND, with one novel prediction (evolving a0) at ~2sigma and regime-")
    print("  limited, no confirmed distinctive result, and several 'wins' that are inherited or")
    print("  tuned. Publishable as a HYPOTHESIS + a sharp test -- not as evidence.")
    print("=" * 80)


def main():
    attack_9_efe(); attack_5_catastrophe(); attack_inheritance(); synthesis(); verdict()


if __name__ == "__main__":
    main()
