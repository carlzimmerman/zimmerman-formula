#!/usr/bin/env python3
"""
The falsification matrix: for each test, the exact outcome that BREAKS one model and VALIDATES the other.
========================================================================================================
Sharpens TESTABLE_PREDICTIONS.md into decision criteria. The honest organizing fact: only a LCDM-IMPOSSIBLE
signal can break LCDM, and only a MOND-impossible result can break the framework. We compute the discriminating
numbers AND state the kill-thresholds AND the current lean -- including the uncomfortable ASYMMETRY (the tests
that could kill LCDM are contested/split; the tests that could kill the framework are partly ALREADY realized).
Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0/y)


def g_obs(gN, gext, a0=1.0):
    if gext <= 0:
        return nu(gN/a0)*gN
    return nu((gN+gext)/a0)*(gN+gext) - nu(gext/a0)*gext


def main():
    print("#"*96)
    print("# THE FALSIFICATION MATRIX -- where each model breaks or lives")
    print("#"*96 + "\n")

    print("="*96); print("TEST 1 -- EXTERNAL FIELD EFFECT  [can KILL LCDM]"); print("="*96)
    print("  Internal boost g_obs/g_N on a deep-MOND system (g_N=0.01 a0) vs external field g_ext:")
    gN = 0.01
    print(f"    {'g_ext/a0':>10}{'g_obs/g_N (MOND)':>18}{'LCDM':>8}")
    for ge in (0.0, 0.3, 1.0, 3.0, 10.0):
        print(f"    {ge:>10.1f}{g_obs(gN, ge)/gN:>18.2f}{1.0:>8.1f}")
    print("  LCDM: boost = 1 ALWAYS (shell theorem forbids env-dependence). MOND: boost COLLAPSES 10.5 -> 1 as")
    print("  the external field rises. KILL LCDM: rotation-curve amplitude declines with environment (Chae 4-5sig).")
    print("  KILL MOND: rotation curves independent of environment. LEAN: Chae positive, CONTESTED.\n")

    print("="*96); print("TEST 2 -- WIDE BINARIES  [can KILL LCDM, or kill the MOND premise]"); print("="*96)
    print("  Separation s>~7000 AU (the MOND radius r_M=(8pi/3)^1/4 sqrt(r_s R_H)). MW field g_ext~1.86 a0 (EFE).")
    print("  framework boost (= standard MOND + MW EFE): +3-15% velocity (derived-interpolation end ~3-5%).")
    print("  LCDM/Newton: 0% boost. KILL LCDM: a robust velocity boost. KILL MOND-premise: pure Newtonian.")
    print("  LEAN: SPLIT (Banik ~19sig Newtonian vs Chae ~4sig MOND); methods-limited; Gaia DR4 decides ~2026-27.")
    print("  NOTE: this is the FOUNDATION test (is local MOND real?), shared with standard MOND -- NOT framework-distinctive.\n")

    print("="*96); print("TEST 3 -- a0(z) EVOLUTION  [framework-distinctive; can kill the framework]"); print("="*96)
    print(f"    {'z':>4}{'framework E(z)':>16}{'constant':>10}{'SIV':>8}")
    siv = {1: 0.70, 2: 0.52, 3: 0.42}
    for z in (1, 2, 3):
        print(f"    {z:>4}{E(z):>16.2f}{1.0:>10.2f}{siv[z]:>8.2f}")
    print("  KILL constant-MOND + SIV / validate framework: a0 rises EXACTLY as E(z) (halo-free, x4.6 at z=3).")
    print("  KILL framework: a0 constant (-> standard MOND) OR a0 falls (-> SIV).")
    print("  *** does NOT distinguish framework from LCDM (LCDM apparent-a0 also rises). LEAN: UNFAVORABLE")
    print("      (MUSE rises FASTER than E(z) & halo-dependent; McGaugh/Milgrom favor constant).\n")

    print("="*96); print("TEST 4 -- CMB 3rd ACOUSTIC PEAK  [ALREADY broke pure MOND]"); print("="*96)
    print("  LCDM: fits all peaks (non-baryonic CDM boosts the 3rd peak). Pure baryonic MOND: 3rd peak too LOW.")
    print("  STATUS: REALIZED -- LCDM wins. The framework survives ONLY via a relativistic completion (AeST,")
    print("  Skordis-Zlosnik 2021) that ADDS a dark field -- losing the galaxy-scale economy. A standing partial loss.\n")

    print("="*96); print("TEST 5 -- GALAXY CLUSTERS  [ALREADY broke MOND]"); print("="*96)
    print("  LCDM: fits with dark matter. MOND: under-predicts cluster-core mass by ~2x (residual even in MOND).")
    print("  STATUS: REALIZED -- LCDM wins. The framework's environmental-a0 fix is DISFAVORED by the RAR")
    print("  (sparc_environmental_a0_test.py: the cluster-fixing smoothing breaks the RAR ~4x). A standing loss.\n")

    print("="*96); print("THE HONEST ASYMMETRY"); print("="*96)
    print("""  CAN KILL LCDM (LCDM-impossible signals):  EFE (Chae 4-5sig, CONTESTED) ; wide-binary boost (SPLIT).
                                            -> both UNCONFIRMED. No clean LCDM kill is in hand.
  CAN KILL THE FRAMEWORK:                   CMB 3rd peak (REALIZED -> needs AeST+dark field) ; clusters
                                            (REALIZED -> MOND x2 residual) ; a0(z) (LEANING constant, unfavorable).
                                            -> partly ALREADY realized.
  => The framework currently carries MORE live falsification exposure than LCDM. To flip the verdict, a
     LCDM-IMPOSSIBLE signal (EFE or wide binaries) must be CONFIRMED -- the only place LCDM can actually break.
     Near-term deciders: Gaia DR4 (wide binaries) + independent EFE confirmation + halo-free high-z a0(z).""")
    print("#"*96)


if __name__ == "__main__":
    main()
