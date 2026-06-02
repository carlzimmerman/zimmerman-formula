#!/usr/bin/env python3
"""
Is there a physical horizon / holographic scale at exactly R* = sqrt(8pi/3) R_H ~ 2.9 R_H?
==========================================================================================

If a real horizon sits at R* = sqrt(8pi/3) R_H, then a0 = c^2/(2R*) is a genuine surface
gravity and Z = 2 sqrt(8pi/3) = 5.789 is DERIVED. We hunt for it exhaustively: scan the
standard horizons, test whether R* is a collapse/Schwarzschild horizon, and -- crucially --
ask whether sqrt(8pi/3) can be a CONSTANT horizon ratio at all (the standard horizons evolve).

Needs numpy + scipy. Run: python <thisfile>
"""
import numpy as np
from scipy.integrate import quad

OM, OL = 0.315, 0.685
E = lambda a: np.sqrt(OM * a ** -3 + OL)        # H(a)/H0
TARGET = np.sqrt(8 * np.pi / 3)                  # 2.894


def main():
    print("=" * 82)
    print("STEP 1 -- scan every cosmological horizon (in units of R_H = c/H0)")
    print("=" * 82)
    R_apparent = 1.0                              # flat FRW: apparent horizon = R_H
    R_event = quad(lambda a: 1 / (a ** 2 * E(a)), 1, np.inf)[0]
    R_particle = quad(lambda a: 1 / (a ** 2 * E(a)), 1e-8, 1)[0]
    # collapse/Schwarzschild: radius where a uniform sphere = its own Schwarzschild radius
    R_collapse = 1.0                              # = R_H (the Hubble=Schwarzschild fact)
    print(f"  {'scale':40}{'R/R_H':>8}{'vs target 2.894':>16}")
    for name, R, evol in [
        ("apparent / Hubble horizon", R_apparent, "= H^-1 (evolves)"),
        ("collapse horizon (sphere = its R_s)", R_collapse, "= R_H"),
        ("event horizon (future)", R_event, "evolves with Omega"),
        ("TARGET  R* = sqrt(8pi/3) R_H", TARGET, "CONSTANT"),
        ("particle horizon (observable U)", R_particle, "evolves with Omega"),
    ]:
        flag = "  <-- target" if abs(R - TARGET) < 1e-6 else ""
        print(f"  {name:40}{R:>8.3f}   {evol:<18}{flag}")
    print(f"  No standard horizon sits at 2.894 R_H: it is BETWEEN the event ({R_event:.2f}) and")
    print(f"  particle ({R_particle:.2f}) horizons, matching neither.\n")

    print("=" * 82)
    print("STEP 2 -- the decisive obstruction: sqrt(8pi/3) is CONSTANT; the horizons are NOT")
    print("=" * 82)
    print("  R* = sqrt(8pi/3) R_H holds at EVERY epoch (it is fixed by the Friedmann coefficient).")
    print("  But the event and particle horizons drift with the matter/Lambda mix:")
    print(f"   {'z':>5}{'R_event/R_H':>13}{'R_particle/R_H':>16}{'sqrt(8pi/3)':>13}")
    for z in (0.0, 1.0, 3.0):
        ai = 1 / (1 + z)
        # event horizon at scale factor ai: a_i * int_{a_i}^inf da/(a^2 H) , in R_H(z) units = *H(ai)
        Hi = E(ai)
        ev = Hi * quad(lambda a: 1 / (a ** 2 * E(a)), ai, np.inf)[0]
        pa = Hi * quad(lambda a: 1 / (a ** 2 * E(a)), 1e-8, ai)[0]
        print(f"   {z:>5.1f}{ev:>13.3f}{pa:>16.3f}{TARGET:>13.3f}")
    print("  The horizons move (event 1.0->~0.8, particle 3.2->shrinking); sqrt(8pi/3) cannot")
    print("  track a moving horizon. So NO causal horizon can sit at R* for a fundamental reason.\n")

    print("=" * 82)
    print("STEP 3 -- WHY: R* is the COLLAPSE scale, not an expansion/horizon scale")
    print("=" * 82)
    print("  R* = c/sqrt(G rho) = c * t_ff : the radius where the LIGHT-CROSSING time R/c equals")
    print("  the FREE-FALL (collapse) time t_ff = 1/sqrt(G rho). Its enclosed mass has")
    print("  R_s = (8pi/3) R* = 8.4 R*  ->  escape velocity sqrt(8pi/3) c = 2.89c: R* is DEEP")
    print("  INSIDE its own would-be horizon, so it is NOT a causal horizon -- it is a DYNAMICAL")
    print("  (structure-formation) scale. And sqrt(8pi/3) = H/sqrt(G rho) is exactly the ratio")
    print("  EXPANSION rate / COLLAPSE rate. Horizons live on the expansion (causal) side; a0 is")
    print("  read off the collapse (dynamical) side. They differ by sqrt(8pi/3), by construction.\n")

    print("=" * 82)
    print("STEP 4 -- the constructive resolution: the right 'horizon' is R_H, via ENTROPY")
    print("=" * 82)
    print("  The data want Z ~ 5.8. That value is NOT a surface gravity at 2.9 R_H -- it is the")
    print("  de Sitter ENTROPY O(1) at the ORDINARY horizon R_H: Verlinde's volume-law gives")
    print("  Z ~ 6, Milgrom's de Sitter temperature gives Z = 2pi = 6.28. The framework's")
    print(f"  2 sqrt(8pi/3) = {2*TARGET:.3f} sits inside that de Sitter cluster (within ~4-8%).")
    print("  So the coefficient's MAGNITUDE (~6) is first-principles (de Sitter horizon entropy),")
    print("  obtained at R_H -- there is no need for, and no, horizon at 2.9 R_H.\n")

    print("=" * 82)
    print("VERDICT")
    print("=" * 82)
    print("  * There is NO physical horizon at sqrt(8pi/3) R_H, and the reason is structural:")
    print("    sqrt(8pi/3) is a constant (Friedmann), while every causal horizon evolves; and")
    print("    R* is the COLLAPSE scale (inside its own mass's horizon, v_esc=2.9c), not a horizon.")
    print("  * sqrt(8pi/3) = expansion-rate / collapse-rate. It is real and forced, but it is a")
    print("    RATE-CONVERSION, not a horizon location. The hunt for a horizon at 2.9 R_H fails on")
    print("    principle, not for lack of trying.")
    print("  * What IS first-principles: the coefficient's magnitude ~6 = the de Sitter horizon")
    print("    ENTROPY O(1) (Verlinde ~6, Milgrom 2pi), obtained at R_H. The framework's 5.789 is")
    print("    a member of that cluster -- defensible as 'the de Sitter O(1)', not uniquely derived.")
    print("  * Honest target going forward: do not seek a horizon at 2.9 R_H. Seek whether the")
    print("    de Sitter ENTROPY coefficient is EXACTLY 2 sqrt(8pi/3) rather than 6 or 2pi -- that")
    print("    is the only place the specific value could still be earned.")
    print("=" * 82)


if __name__ == "__main__":
    main()
